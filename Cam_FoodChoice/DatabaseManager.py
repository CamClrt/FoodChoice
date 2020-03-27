from data import *
import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    #TODO : writing docstring

    def __init__(self):
        pass

    def create_database_and_user(self, database_name, user_name, host_name, user_password, user_name_root, user_password_root):
        # TODO docsting

        # TODO docsting
        db = None
        try:
            db = mysql.connector.connect(
                user=user_name_root,
                password=user_password_root,
                host=host_name,
            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        # TODO docsting
        database_query = "CREATE DATABASE " + database_name
        cursor = db.cursor()
        try:
            cursor.execute(database_query)
            print("Database created successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

        # TODO docsting
        user_query1 = "CREATE USER '" + user_name + "'@'" + host_name + "' IDENTIFIED BY '" + user_password +"'"
        try:
            cursor.execute(user_query1)
            print("User created successfully")

            # TODO docsting
            user_query2 = "GRANT ALL PRIVILEGES ON " + database_name + ". * TO '" + user_name + "'@'" + host_name + "'"
            try:
                cursor.execute(user_query2)
                print("Privileges granted successfully")
            except Error as e:
                print(f"The error '{e}' occurred")

        except Error as e:
            print(f"The error '{e}' occurred")


    def connect_database_and_user(self, database_name, user_name, host_name, user_password):
        # TODO docsting

        db = None
        try:
            db = mysql.connector.connect(
                user=user_name,
                password=user_password,
                host=host_name,
                database=database_name
            )
            print("Connection to " + database_name + " DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

        return db

    def show_databases(self, db):
        # TODO docsting

        mycursor = db.cursor()
        mycursor.execute("SHOW DATABASES")
        try:
            print("\n **** DATABASES ****")
            for x in mycursor:
                print(x)
        except Error as e:
            print(f"The error '{e}' occurred")

    def show_users(self, db):
        # TODO docsting

        mycursor = db.cursor()
        mycursor.execute("SELECT User FROM mysql.user")
        try:
            print("\n **** USERS ****")
            for x in mycursor:
                print(x)
        except Error as e:
            print(f"The error '{e}' occurred")

    def show_tables(self, db):
        # TODO docsting

        mycursor = db.cursor()
        mycursor.execute("SHOW TABLES")
        try:
            print("\n **** TABLES ****")
            for x in mycursor:
                print(x)
        except Error as e:
            print(f"The error '{e}' occurred")


FoodChoice = DatabaseManager()
#FoodChoice.create_database_and_user(DATABASE_NAME, USER_NAME, HOST_NAME, USER_PASSWORD, USER_NAME_ROOT, USER_PASSWORD_ROOT)
db = FoodChoice.connect_database_and_user(DATABASE_NAME, USER_NAME_ROOT, HOST_NAME, USER_PASSWORD_ROOT)
FoodChoice.show_databases(db)
FoodChoice.show_users(db)
FoodChoice.show_tables(db)