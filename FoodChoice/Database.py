from data import *

from FoodChoice.API import *
from FoodChoice.City import *
from FoodChoice.Store import *
from FoodChoice.Product import *
from FoodChoice.Category import *
from FoodChoice.Users import *
from FoodChoice.Filter import *
from FoodChoice.CategoryProduct import *
from FoodChoice.ProductLocation import *

import time
import pickle
import os.path
from progress.bar import Bar
from colorama import Fore, Style

import mysql.connector
from mysql.connector import Error


class Database:
    """"Represent the MySQL database"""

    def __init__(self, database_name=DATABASE_NAME,
                 host_name=HOST_NAME,
                 user_name_root=USER_NAME_ROOT,
                 user_password_root=USER_PASSWORD_ROOT
                 ):

        self.database_name = database_name
        self.host_name = host_name
        self.user_name_root = user_name_root
        self.user_password_root = user_password_root
        self.database = None

    def __enter__(self):
        """TODO ecrire"""
        self.database = self.connect()
        return self.database

    def __exit__(self, *args):
        """TODO ecrire"""
        self.database.close()

    def connect(self):
        """Init and/or connect database"""
        db = None
        try:
            db = mysql.connector.connect(
                user=self.user_name_root,
                password=self.user_password_root,
                host=self.host_name,
            )

            mycursor = db.cursor()
            mycursor.execute(SQL_DB_DIRECTORY)
            path = mycursor.fetchone()

            if len(path) != 0:
                url_db = path[0] + self.database_name
                if os.path.exists(url_db):
                    mycursor.execute(SQL_USE_DB)
                else:

                    # import data from OpenFoodFacts API
                    api = API()
                    try:
                        imported_products = api.products
                        imported_categories = api.categories
                        with open('categories.data', 'wb') as file:
                            pickle.dump(imported_categories, file)

                    except Error as e:
                        print(f"L'erreur '{e}' est survenue")
                        time.sleep(5)
                        imported_products = api.products
                        imported_categories = api.categories
                        with open('categories.data', 'wb') as file:
                            pickle.dump(imported_categories, file)

                    # create database and tables
                    mycursor.execute(SQL_CREATE_DB)
                    print(Fore.GREEN + "> La base de données a été créée avec succès")

                    mycursor.execute(SQL_USE_DB)
                    for name, query in TABLES.items():
                        mycursor.execute(query)
                        print(f"> La table {name} a été créée avec succès")

                    # insert data in DB
                    print("\n------------> Insertion des données en base <------------\n")

                    products = []  # store product objects
                    prod_mng = ProductManager(db)

                    with Bar('Progression', max=len(imported_products)) as bar:
                        for imported_product in imported_products:

                            filters = Filter()
                            cat_mng = CategoryManager(db)
                            city_mng = CityManager(db)
                            store_mng = StoreManager(db)
                            catprod_mng = CategoryProductManager(db)
                            prodloc_mng = ProductLocationManager(db)

                            categories = []  # store category objects
                            cities = []  # store city objects
                            stores = []  # store store objects

                            # filter & insert categories

                            tmp_categories = imported_product.get("categories", "").split(',')
                            for tmp_category in tmp_categories:
                                category = filters.cat_filter(tmp_category)
                                if category is not None:
                                    categories.append(cat_mng.find(category))

                            # filter & insert cities
                            tmp_cities = imported_product.get("purchase_places", "").split(',')
                            if len(tmp_cities) != 0:
                                for tmp_city in tmp_cities:
                                    city = filters.city_filter(tmp_city)
                                    cities.append(city_mng.find(city))

                            # filter & insert cities
                            tmp_stores = imported_product.get("stores", "").split(',')
                            if len(tmp_stores) != 0:
                                for tmp_store in tmp_stores:
                                    store = filters.store_filter(tmp_store)
                                    stores.append(store_mng.find(store))

                            # filter & insert products
                            tmp_name = imported_product.get("product_name_fr", "")
                            tmp_brand = imported_product.get("brands", "")
                            tmp_nutrition_grade = imported_product.get("nutrition_grades", "z")
                            tmp_energy_100g = imported_product.get("nutriments", "").get("energy_100g", "999999")
                            tmp_url = imported_product.get("url", "")
                            tmp_code = imported_product.get("code", (13 * "0"))

                            name, brand, nutrition_grade, energy_100g, url, code = filters.prod_filters(
                                tmp_name, tmp_brand, tmp_nutrition_grade, tmp_energy_100g, tmp_url, tmp_code)

                            tmp_product_object = Product(name, brand, nutrition_grade, energy_100g,
                                               url, code, stores, cities, categories)

                            product_object = prod_mng.insert(tmp_product_object)

                            if product_object != None: # if the product is really stored in DB
                                products.append(product_object)

                            bar.next()

                    # insert data in CategoryProduct table
                    categoryproducts = []
                    productlocations = []

                    for product in products:
                        prod_id = product.id
                        for category in product.categories:
                            cat_id = category.id
                            categoryproducts.append(CategoryProduct(prod_id, cat_id))

                        # insert data in ProductLocation table
                        for city in product.cities:
                            city_id = city.id
                            for store in product.stores:
                                store_id = store.id
                                productlocations.append(ProductLocation(prod_id, store_id, city_id))

                    catprod_mng.insert(categoryproducts)
                    prodloc_mng.insert(productlocations)

                    # insert default user account
                    users_mng = UsersManager(db)
                    pwd_hashed = bcrypt.hashpw(bytes(users_mng.default_pw, 'utf-8'),
                                               bcrypt.gensalt())  # convert pwd in bytes
                    serial_pwd_hashed = pickle.dumps(pwd_hashed)  # serialize the serial_pwd_hashed object
                    users_mng.create(users_mng.default_username, serial_pwd_hashed)

        except Error as e:
            print(f"L'erreur '{e}' est survenue")

        mycursor.close()
        print(Style.RESET_ALL)

        return db