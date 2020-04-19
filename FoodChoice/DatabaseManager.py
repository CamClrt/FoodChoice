from data import *

from FoodChoice.API_Category import API_Category
from FoodChoice.API_Product import API_Product

import mysql.connector
from mysql.connector import Error


class DatabaseManager:
    """"Init database or connect it"""

    def __init__(self):
        self.database_name = DATABASE_NAME
        self.host_name = HOST_NAME
        self.user_name_root = USER_NAME_ROOT
        self.user_password_root = USER_PASSWORD_ROOT


    def init_database(self):
        """"Init database and import data or connect it"""
        db = self.connect_service()
        mycursor = db.cursor()
        mycursor.execute("SHOW DATABASES")
        databases = mycursor.fetchone()
        db.close()

        if not databases.count("FoodChoice") == 1:
            self.create_database()
            self.create_tables()
            self.insert_product_data(self.insert_category_data())
            db.close()

        return self.connect_database()

    def connect_service(self):
        """Connect to the service"""
        db = None
        try:
            db = mysql.connector.connect(
                user= self.user_name_root,
                password= self.user_password_root,
                host= self.host_name,
            )
        except Error as e:
            print(f"The error '{e}' occurred")

        print("Connection to MySQL successfully")

        return db

    def connect_database(self):
        """Connect the database"""
        db = None
        try:
            db = mysql.connector.connect(
                user= self.user_name_root,
                password= self.user_password_root,
                host= self.host_name,
                database= self.database_name,
            )
        except Error as e:
            print(f"The error '{e}' occurred")
        return db

    def create_database(self):
        """At the first connexion, create database"""
        db = None
        try:
            db = mysql.connector.connect(
                user= self.user_name_root,
                password= self.user_password_root,
                host= self.host_name,
            )
        except Error as e:
            print(f"The error '{e}' occurred")

        mycursor = db.cursor()

        try:
            mycursor.execute(SQL_CREATE_DB)
            print("Database created successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def create_tables(self):
        """At the first connexion, create tables"""
        db = self.connect_database()
        for name, query in TABLES.items():
            try:
                mycursor = db.cursor()
                mycursor.execute(query)
                print(f"{name} table created successfully")
            except Error as e:
                print(f"The error '{e}' occurred")
        db.close()

######################### TODO : ici tout à revoir sur l'insertion des données #########################

    def insert_category_data(self):
        """At the first connexion, import categories from the OpenFoodFact API"""
        api_category = API_Category()
        category_list = api_category.categories
        db = self.connect_database()

        for category in category_list:
            try:
                query = SQL_CREATE_CATEGORIES.replace("category", category)
                mycursor = db.cursor()
                mycursor.execute(query)
            except Error as e:
                print(f"The error '{e}' occurred")
        db.commit()
        db.close()
        return category_list

    def insert_product_data(self, categories):
        """At the first start, import products data from the OpenFoodFact API"""
        db = self.connect_database()
        for category in categories:

            """process data to import in Product table"""
            api_product = API_Product(category)
            product_list = api_product.products

            product_details_list = []
            data = []

            for product in product_list:
                for key, item in PRODUCT_PARARMETERS.items():
                    if key == item[0]:
                        int_value = str(product.get(key, ""))
                        product_details_list.append(int_value[:item[1]])
                    else:
                        detail = product.get(key, "")
                        try:
                            detail[item] is item[1]
                            product_details_list.append(detail.get(item, ""))
                        except:
                            product_details_list.append(0)

                data.append(tuple(product_details_list))
                product_details_list = []

            try:
                mycursor = db.cursor()
                mycursor.executemany(SQL_CREATE_PRODUCTS, data)
                db.commit()
            except Error as e:
                print(f"The error '{e}' occurred")

            """process data to import in Store table"""
            for key, item in PRODUCT_STORE_PARARMETERS.items():
                stores = []
                stores = product.get(key)

                if type(stores) is list and len(stores) != 0:
                    for store in stores:
                        try:
                            mycursor = db.cursor()
                            query = SQL_CREATE_STORES.replace("store", store)
                            mycursor.execute(query)
                            db.commit()
                        except Error as e:
                            print(f"The error '{e}' occurred")

            """process data to import in City table"""
            for key, item in PRODUCT_CITY_PARARMETERS.items():
                cities = []
                cities = product.get(key)

                if type(cities) is list and len(cities) != 0:
                    for city in cities:
                        try:
                            mycursor = db.cursor()
                            query = SQL_CREATE_CITIES.replace("city", city)
                            mycursor.execute(query)
                            db.commit()
                        except Error as e:
                            print(f"The error '{e}' occurred")

            """process data to import complete Category table"""
            for key, item in PRODUCT_CATEGORY_PARARMETERS.items():
                categories = []
                categories = product.get(key)

                if type(categories) is list and len(categories) != 0:
                    for category in categories:
                        try:
                            mycursor = db.cursor()
                            query = SQL_CREATE_CATEGORIES.replace("category", category)
                            mycursor.execute(query)
                            db.commit()
                        except Error as e:
                            print(f"The error '{e}' occurred")
        db.close()