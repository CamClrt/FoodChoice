from Cam_FoodChoice.data import *
from Cam_FoodChoice.CategoryManager import CategoryManager
from Cam_FoodChoice.ProductManager import ProductManager

import mysql.connector
from mysql.connector import Error
import os.path
from os import path
import time


class DatabaseManager:
    #TODO : writing docstring

    def __init__(self):
        self.DB_URL = path.join(path.dirname(__file__), "mysql_folder/FoodChoice")
        self.database_name = DATABASE_NAME
        self.host_name = HOST_NAME
        self.user_name_root = USER_NAME_ROOT
        self.user_password_root = USER_PASSWORD_ROOT

    def init_database(self):
        # TODO : writing docstring

        if os.path.isdir(self.DB_URL):
            db = self.connect_database()
        else:
            time.sleep(15)
            self.create_database()
            db = self.connect_database()
            self.create_tables(db)
        return db

    def create_database(self):
        # TODO : writing docstring

        db = None
        try:
            db = mysql.connector.connect(
                user= self.user_name_root,
                password= self.user_password_root,
                host= self.host_name,
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        mycursor = db.cursor()

        try:
            mycursor.execute(SQL_CREATE_DB)
            print("Database created successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def connect_database(self):
        # TODO : writing docstring

        db = None
        try:
            db = mysql.connector.connect(
                user= self.user_name_root,
                password= self.user_password_root,
                host= self.host_name,
                database= self.database_name,
            )
            print("Connection to " + self.database_name + " DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        print("\n **** CONNEXION ****")

        return db

    def create_tables(self, db):
        # TODO : writing docstring

        for query in CREATE_TABLES:
            try:
                mycursor = db.cursor()
                mycursor.execute(query)
                print(f"Table created successfully")
            except Error as e:
                print(f"The error '{e}' occurred")

    def insert_category_data(self, db):
        # TODO : writing docstring

        #insert categories & products
        category_manager = CategoryManager()
        category_list = category_manager.categories

        for category in category_list:
            try:
                #query = "INSERT INTO Category (Name) VALUES ('" + reformat_category + "')" TODO à supprimer si ok
                query = SQL_CREATE_CATEGORY.replace("category", category)
                mycursor = db.cursor()
                mycursor.execute(query)
                #self.insert_product_data(db, reformat_categories)
            except Error as e:
                print(f"The error '{e}' occurred")

"""    def insert_product_data(self, db, categories):
        # TODO : writing docstring

        # insert products
        product_manager = ProductManager(categories)
        product_list = product_manager.import_data()

        for product_dictionnary in product_list:

            for key, item in PARARMETERS_PRODUCT.items():

                if key == item:
                    try:
                        query = "INSERT INTO Product + (Name)+  VALUES ('" + reformat_product + "')"
                        mycursor = db.cursor()
                        mycursor.execute(query)

                        print(key, " : ", product_dictionnary[key])

                    except Error as e:
                        print(f"The error '{e}' occurred")
                else:
                    detail = product_dictionnary[key]
                    try:
                        print(item, " : ", detail[item])
                    except Error as e:
                        print(f"The error '{e}' occurred")"""