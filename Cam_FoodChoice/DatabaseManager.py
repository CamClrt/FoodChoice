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
            self.insert_data(db)
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

    def insert_data(self, db):
        # TODO : writing docstring

        #insert categories & products
        category_manager = CategoryManager()
        category_list = category_manager.categories

        for category in category_list:
            reformat_category = category.replace("'"," ")
            try:
                query = "INSERT INTO Category (Name) VALUES ('" + reformat_category + "')"
                mycursor = db.cursor()
                mycursor.execute(query)
            except Error as e:
                print(f"The error '{e}' occurred")

"""        for category in category_list:
            product_manager = ProductManager(category)
            product_dictionnary = product_manager.import_data()"""