from data import *
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
        self.user_name = USER_NAME
        self.user_password = USER_PASSWORD
        self.user_name_root = USER_NAME_ROOT
        self.user_password_root = USER_PASSWORD_ROOT


    def init_database(self):
        # TODO : writing docstring

        if os.path.isdir(self.DB_URL):
            db = self.connect_database()
        else:
            self.create_database()
            db = self.connect_database()
            self.create_user(db)
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

        # TODO : writing docstring
        database_query = "CREATE DATABASE " + self.database_name
        mycursor = db.cursor()
        try:
            mycursor.execute(database_query)
            print("Database created successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

        mycursor.close()
        db.close()


    def create_user(self, db):
        # TODO : writing docstring

        mycursor = db.cursor()

        user_query1 = "CREATE USER '" + self.user_name + "'@'" + self.host_name + "' IDENTIFIED BY '" + self.user_password +"'"
        time.sleep(3)
        try:
            mycursor.execute(user_query1)
            print("User created successfully")

            # TODO : writing docstring
            user_query2 = "GRANT ALL PRIVILEGES ON " + self.database_name + ".* TO '" + self.user_name + "'@'" + self.host_name + "'"
            try:
                mycursor.execute(user_query2)
                print("Privileges granted successfully")
            except Error as e:
                print(f"The error '{e}' occurred")

        except Error as e:
            print(f"The error '{e}' occurred")

        mycursor.close()
        db.close()


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


    def show_databases(self, db):
        # TODO : writing docstring

        mycursor = db.cursor()
        mycursor.execute("SHOW DATABASES")
        try:
            print("\n **** DATABASES ****")
            for x in mycursor:
                print(x)
        except Error as e:
            print(f"The error '{e}' occurred")

        mycursor.close()
        db.close()


    def show_users(self, db):
        # TODO : writing docstring

        mycursor = db.cursor()
        mycursor.execute("SELECT User FROM mysql.user")
        try:
            print("\n **** USERS ****")
            for x in mycursor:
                print(x)
        except Error as e:
            print(f"The error '{e}' occurred")

        mycursor.close()
        db.close()


    def show_tables(self, db):
        # TODO : writing docstring

        mycursor = db.cursor()
        mycursor.execute("SHOW TABLES")
        try:
            print("\n **** TABLES ****")
            for x in mycursor:
                print(x)
        except Error as e:
            print(f"The error '{e}' occurred")

        mycursor.close()
        db.close()


food_choice = DatabaseManager()
db = food_choice.init_database()
food_choice.show_databases(db)
food_choice.show_users(db)
food_choice.show_tables(db)