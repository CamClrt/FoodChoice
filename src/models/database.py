"""
    This module manage all operations with the database
"""

import time
import pickle
import os.path
import bcrypt
from progress.bar import Bar
from colorama import Fore, Style

import mysql.connector
from mysql.connector import Error

from api.api import API
from utils import config
from utils import queries
from utils.filter import cat_filter, city_filter, store_filter, prod_filters
from models.city import CityManager
from models.store import StoreManager
from models.product import ProductManager, Product
from models.category import CategoryManager
from models.users import UsersManager
from models.category_product import CategoryProductManager, CategoryProduct
from models.product_location import ProductLocationManager, ProductLocation


class Database:
    """"Represent the MySQL database"""

    def __init__(
        self,
        database_name=config.DATABASE_NAME,
        host_name=config.HOST_NAME,
        user_name=config.USER_NAME,
        user_password=config.USER_PASSWORD,
    ):

        self.database_name = database_name
        self.host_name = host_name
        self.user_name = user_name
        self.user_password = user_password
        self.database = None

    def __enter__(self):
        """Allow the DB connection"""
        self.database = self.connect()
        return self.database

    def __exit__(self, *args):
        """Close the DB connection"""
        self.database.close()

    def connect(self):
        """Init and/or connect database"""
        database = None
        try:
            database = mysql.connector.connect(
                user=self.user_name,
                password=self.user_password,
                host=self.host_name,
            )

            mycursor = database.cursor()
            mycursor.execute(queries.SQL_DB_DIRECTORY)
            path = mycursor.fetchone()

            if len(path) != 0:
                url_db = path[0] + self.database_name
                if os.path.exists(url_db):
                    mycursor.execute(queries.SQL_USE_DB)
                else:

                    # import data from OpenFoodFacts API
                    api = API()
                    try:
                        imported_products = api.products

                    except Error as err:
                        print(f"L'erreur '{err}' est survenue")
                        time.sleep(5)
                        imported_products = api.products

                    # create database and tables
                    mycursor.execute(queries.SQL_CREATE_DB)
                    print(
                        Fore.GREEN + "> Base de données créée avec succès <"
                    )

                    mycursor.execute(queries.SQL_USE_DB)
                    for name, query in queries.TABLES.items():
                        mycursor.execute(query)
                        print(f"> La table '{name}' a été créée avec succès")

                    # insert data in DB
                    print("\n----> Insertion des données en base <----\n")

                    products = []  # store product objects
                    prod_mng = ProductManager(database)

                    with Bar("Progression", max=len(imported_products)) as bar:
                        for imported_product in imported_products:

                            cat_mng = CategoryManager(database)
                            city_mng = CityManager(database)
                            store_mng = StoreManager(database)
                            catprod_mng = CategoryProductManager(database)
                            prodloc_mng = ProductLocationManager(database)

                            categories = []  # store category objects
                            cities = []  # store city objects
                            stores = []  # store store objects

                            # filter & insert categories
                            tmp_categories = imported_product.get(
                                "categories", ""
                            ).split(",")
                            for tmp_category in tmp_categories:
                                category = cat_filter(tmp_category)
                                if category is not None:
                                    categories.append(cat_mng.find(category))

                            # filter & insert cities
                            tmp_cities = imported_product.get(
                                "purchase_places", ""
                            ).split(",")
                            if len(tmp_cities) != 0:
                                for tmp_city in tmp_cities:
                                    city = city_filter(tmp_city)
                                    cities.append(city_mng.find(city))

                            # filter & insert cities
                            tmp_stores = imported_product.get(
                                "stores", "").split(",")
                            if len(tmp_stores) != 0:
                                for tmp_store in tmp_stores:
                                    store = store_filter(tmp_store)
                                    stores.append(store_mng.find(store))

                            # filter & insert products
                            tmp_name = imported_product.get(
                                "product_name_fr", "")
                            tmp_brand = imported_product.get("brands", "")
                            tmp_nutrition_grade = imported_product.get(
                                "nutrition_grades", "z"
                            )
                            tmp_energy_100g = imported_product.get(
                                "nutriments", ""
                            ).get("energy_100g", "999999")
                            tmp_url = imported_product.get("url", "")
                            tmp_code = imported_product.get("code", (13 * "0"))

                            (
                                name,
                                brand,
                                nutrition_grade,
                                energy_100g,
                                url,
                                code,
                            ) = prod_filters(
                                tmp_name,
                                tmp_brand,
                                tmp_nutrition_grade,
                                tmp_energy_100g,
                                tmp_url,
                                tmp_code,
                            )

                            tmp_product_object = Product(
                                name,
                                brand,
                                nutrition_grade,
                                energy_100g,
                                url,
                                code,
                                stores,
                                cities,
                                categories,
                            )

                            product_object = prod_mng.insert(
                                tmp_product_object)

                            # if the product is really stored in DB
                            if product_object is not None:
                                products.append(product_object)

                            bar.next()

                    # insert data in CategoryProduct table
                    categoryproducts = []
                    productlocations = []

                    for product in products:
                        prod_id = product.id
                        for category in product.categories:
                            cat_id = category.id
                            categoryproducts.append(
                                CategoryProduct(prod_id, cat_id))

                        # insert data in ProductLocation table
                        for city in product.cities:
                            city_id = city.id
                            for store in product.stores:
                                store_id = store.id
                                productlocations.append(
                                    ProductLocation(prod_id, store_id, city_id)
                                )

                    catprod_mng.insert(categoryproducts)
                    prodloc_mng.insert(productlocations)

                    # insert default user account
                    users_mng = UsersManager(database)
                    # convert pwd in bytes
                    pwd_hashed = bcrypt.hashpw(
                        bytes(users_mng.default_pw, "utf-8"), bcrypt.gensalt()
                    )
                    # serialize the serial_pwd_hashed object
                    serial_pwd_hashed = pickle.dumps(pwd_hashed)
                    users_mng.create(
                        users_mng.default_username, serial_pwd_hashed)

        except Error as err:
            print(f"L'erreur '{err}' est survenue")

        mycursor.close()
        print(Style.RESET_ALL)

        return database
