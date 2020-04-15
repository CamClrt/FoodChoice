from FoodChoice.data import *

from FoodChoice.CategoryManager import CategoryManager
from FoodChoice.ProductManager import ProductManager

import mysql.connector
from mysql.connector import Error

import os.path
from os import path

import time


class DatabaseManager:
    """"Init database or connect it"""

    def __init__(self):
        self.DB_URL = path.join(path.dirname(__file__), "mysql_folder/FoodChoice")
        self.database_name = DATABASE_NAME
        self.host_name = HOST_NAME
        self.user_name_root = USER_NAME_ROOT
        self.user_password_root = USER_PASSWORD_ROOT


    def init_database(self):
        """"Init database and import data or connect it"""
        if os.path.isdir(self.DB_URL):
            db = self.connect_database()
            self.insert_product_data(db, self.insert_category_data(db)) #TODO à retirer ensuite
        else:
            time.sleep(15)
            self.create_database()
            db = self.connect_database()
            self.create_tables(db)
            self.insert_product_data(db, self.insert_category_data(db))
        return db

    def create_database(self):
        """At the first start, create database"""
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
        """Connect the database"""
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
        """At the first connexion, create tables"""
        for query in CREATE_TABLES:
            try:
                mycursor = db.cursor()
                mycursor.execute(query)
                print(f"Table created successfully")
            except Error as e:
                print(f"The error '{e}' occurred")

    def insert_category_data(self, db):
        """At the first connexion, import categories from the OpenFoodFact API"""
        category_manager = CategoryManager()
        category_list = category_manager.categories

        for category in category_list:
            try:
                query = SQL_CREATE_CATEGORIES.replace("category", category)
                mycursor = db.cursor()
                mycursor.execute(query)
            except Error as e:
                print(f"The error '{e}' occurred")
        db.commit()
        return category_list

    def insert_product_data(self, db, categories):
        """At the first start, import products data from the OpenFoodFact API"""
        for category in categories:
            product_manager = ProductManager(category)
            product_list = product_manager.products

            product_details_list = []
            data = []

            for product in product_list:
                for key, item in PRODUCT_PARARMETERS.items():
                    if key == item:
                        product_details_list.append(product.get(key, ""))
                    else:
                        detail = product.get(key, "")
                        try:
                            detail[item] is int
                            product_details_list.append(detail.get(item, ""))
                        except:
                            product_details_list.append(0)

                data.append(tuple(product_details_list))
                product_details_list = []

            try:
                mycursor = db.cursor()
                mycursor.executemany(SQL_CREATE_PRODUCTS, data)
            except Error as e:
                print(f"The error '{e}' occurred")

            db.commit()