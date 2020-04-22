from data import *

from FoodChoice.API import API
from FoodChoice.Product import *
from FoodChoice.Category import *

import os.path

import mysql.connector
from mysql.connector import Error


class Database:
    """"The MySQL database"""

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
                    mycursor.execute(SQL_USE_DB.replace("DB", self.database_name))
                else:
                    mycursor.execute(SQL_CREATE_DB.replace("DB", self.database_name))
                    print(">>> Database created successfully")

                    mycursor.execute(SQL_USE_DB.replace("DB", self.database_name))
                    for name, query in TABLES.items():
                        mycursor.execute(query)
                        print(f"> {name} table created successfully")

                    #insert data in Product, Category, Store and City tables
                    api = API()
                    print("\n", " /!\ WAITING: importation of the data, this may take a few minutes ".center(100, '-'), "\n")
                    products_imported, stores_imported, places_imported, categories_imported = api.products

                    #insert categories in Category table
                    categories = [] # a list of category object
                    for category_imported in categories_imported:
                        products = [] # a list of product object
                        for product_imported in products_imported:
                            if product_imported[8].count(category_imported) != 0:
                                name = product_imported[0]
                                brand = product_imported[1]
                                nutrition_grade = product_imported[2]
                                energy_100g = product_imported[3]
                                url = product_imported[4]
                                code = product_imported[5]
                                stores = product_imported[6]
                                places = product_imported[7]
                                categories = product_imported[8]
                                product = Product(name, brand, nutrition_grade, energy_100g,
                                                  url, code, stores, places, categories)
                                products.append(product)
                        category = Category(category_imported, products)
                        cat_mgr = CategoryManager(db)
                        cat_mgr.insert(category)
                    print("categories imported successfully")


            print("Database connected successfully \n")
        except Error as e:
            print(f"The error '{e}' occurred")
        mycursor.close()

        return db