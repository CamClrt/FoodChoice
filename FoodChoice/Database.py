from FoodChoice.data import *

import mysql.connector
from mysql.connector import Error


class Database():
    """Display the different element of MySQL : databases, users, tables & the whole contain of the tables"""

    def display_databases(self, db):
        """Display databases"""
        mycursor = db.cursor()
        mycursor.execute("SHOW DATABASES")
        try:
            print("\n **** DATABASES ****")
            for x in mycursor:
                print(x)
        except Error as e:
            print(f"The error '{e}' occurred")

    def display_users(self, db):
        """Display users"""
        mycursor = db.cursor()
        mycursor.execute("SELECT User FROM mysql.user")
        try:
            print("\n **** USERS ****")
            for x in mycursor:
                print(x)
        except Error as e:
            print(f"The error '{e}' occurred")

    def display_tables(self, db):
        """Display tables"""
        mycursor = db.cursor()
        mycursor.execute("SHOW TABLES")
        try:
            print("\n **** TABLES ****")
            for x in mycursor:
                print(x)
        except Error as e:
            print(f"The error '{e}' occurred")

    def display_data_in_tables(self, db):
        """Display data in tables"""
        mycursor = db.cursor()
        for table in TABLES:
            mycursor.execute("SELECT * FROM " + table)
            try:
                print("\n **** " + table + " table ****")
                for x in mycursor:
                    print(x)
            except Error as e:
                print(f"The error '{e}' occurred")