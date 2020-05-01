from data import *

from FoodChoice.API import *
from FoodChoice.City import *
from FoodChoice.Store import *
from FoodChoice.Product import *
from FoodChoice.Category import *
from FoodChoice.Filter import *
from FoodChoice.CategoryProduct import *
from FoodChoice.ProductLocation import *

import time
import os.path
from progress.bar import Bar

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
        self.database = self.connect()
        return self.database

    def __exit__(self, *args):
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
                    except Error as e:
                        print(f"The error '{e}' occurred")
                        time.sleep(5)
                        imported_products = api.products

                    # create database and tables
                    mycursor.execute(SQL_CREATE_DB)
                    print("\n> Database created successfully")

                    mycursor.execute(SQL_USE_DB)
                    for name, query in TABLES.items():
                        mycursor.execute(query)
                        print(f"> {name} table created successfully")

                    # insert data in DB
                    print("\n-------------> Inserting data in database <-------------\n")

                    products = []  # store product objects
                    prod_mng = ProductManager(db)

                    with Bar('Processing', max=len(imported_products)) as bar:
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
                            tmp_nutrition_grade = imported_product.get("nutrition_grades", "")
                            tmp_energy_100g = imported_product.get("nutriments", "").get("energy_100g", 0)
                            tmp_url = imported_product.get("url", "")
                            tmp_code = imported_product.get("code", (13 * "0"))

                            name, brand, nutrition_grade, energy_100g, url, code = filters.prod_filters(
                                tmp_name, tmp_brand, tmp_nutrition_grade, tmp_energy_100g, tmp_url, tmp_code)

                            products.append(prod_mng.insert(Product(name, brand, nutrition_grade, energy_100g,
                                                    url, code, stores, cities, categories)))
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

            print("\nDatabase connected successfully\n")

        except Error as e:
            print(f"The error '{e}' occurred")

        mycursor.close()

        return db