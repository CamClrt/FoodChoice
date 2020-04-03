import mysql.connector
from mysql.connector import Error

class Database():
    # TODO : writing docstring

    def display_databases(self, db):
        # TODO : writing docstring

        mycursor = db.cursor()
        mycursor.execute("SHOW DATABASES")
        try:
            print("\n **** DATABASES ****")
            for x in mycursor:
                print(x)
        except Error as e:
            print(f"The error '{e}' occurred")


    def display_users(self, db):
        # TODO : writing docstring

        mycursor = db.cursor()
        mycursor.execute("SELECT User FROM mysql.user")
        try:
            print("\n **** USERS ****")
            for x in mycursor:
                print(x)
        except Error as e:
            print(f"The error '{e}' occurred")


    def display_tables(self, db):
        # TODO : writing docstring

        mycursor = db.cursor()
        mycursor.execute("SHOW TABLES")
        try:
            print("\n **** TABLES ****")
            for x in mycursor:
                print(x)
        except Error as e:
            print(f"The error '{e}' occurred")


    def display_data_in_tables(self, db):
        # TODO : writing docstring

        mycursor = db.cursor()
        mycursor.execute("SELECT * FROM Category")
        try:
            print("\n **** TABLE Category ****")
            for x in mycursor:
                print(x)
        except Error as e:
            print(f"The error '{e}' occurred")