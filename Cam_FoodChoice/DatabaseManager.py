from Cam_FoodChoice.data import *
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
            time.sleep(30)
            try:
                self.create_database()
            except:
                print("Waiting, second and last try to connect...")
                time.sleep(30)
                self.create_database()
            try:
                db = self.connect_database()
                self.create_tables(db)
            except:
                print(f"FATAL ERROR : The database can be create")
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

"""    def insert_data(self, db, category_list):
        # TODO : writing docstring

        #insert categories
        for category in category_list:
            query = "INSERT INTO Category (Name) VALUES ('" + category + "')"
            mycursor = db.cursor()
            mycursor.execute(query)"""

"""        mycursor = db.cursor()
        mycursor.execute("SELECT * FROM Products")
        try:
            print("\n **** TABLE Products ****")
            for x in mycursor:
                print(x)
        except Error as e:
            print(f"The error '{e}' occurred")"""


# -------------- Execution ------------------

"""food_choice = DatabaseManager()"""
