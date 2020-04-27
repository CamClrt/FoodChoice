from data import *

from FoodChoice.API import *
from FoodChoice.City import *
from FoodChoice.Store import *
from FoodChoice.Product import *
from FoodChoice.Category import *
from FoodChoice.CategoryProduct import *
from FoodChoice.ProductLocation import *

import re
import time
import os.path
from progress.bar import Bar

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

                    # import data from OpenFoodfacts API
                    api = API()
                    try:
                        imported_products = api.products
                    except Error as e:
                        print(f"The error '{e}' occurred")
                        time.sleep(5)
                        imported_products = api.products

                    # create database and tables
                    mycursor.execute(SQL_CREATE_DB.replace("DB", self.database_name))
                    print("\n> Database created successfully")

                    mycursor.execute(SQL_USE_DB.replace("DB", self.database_name))
                    for name, query in TABLES.items():
                        mycursor.execute(query)
                        print(f"> {name} table created successfully")

                    # insert data in DB
                    print("\n-------------> Inserting data in database <-------------")

                    with Bar('Processing', max=len(imported_products)) as bar:
                        for imported_product in imported_products:

                            # filter & insert categories
                            tmp_categories = imported_product.get("categories", "").split(',')
                            for tmp_categorie in tmp_categories:
                                categorie = tmp_categorie.replace("'", " ").strip().capitalize()

                                if re.search("..:", categorie):
                                    if categorie[:2] == "fr:":
                                        cat_mng = CategoryManager(db)
                                        cat_mng.insert(Category(((categorie[3:])[:50])))
                                else:
                                    cat_mng = CategoryManager(db)
                                    cat_mng.insert(Category(categorie[:50]))

                                # filter & insert cities
                                tmp_cities = imported_product.get("purchase_places", "").split(',')

                                if len(tmp_cities) != 0:
                                    for tmp_city in tmp_cities:
                                        city = (tmp_city.replace("'", " ")).strip().capitalize()
                                        city_mng = CityManager(db)
                                        city_mng.insert(City(city[:50]))

                                # filter & insert cities
                                tmp_stores = imported_product.get("stores", "").split(',')

                                if len(tmp_stores) != 0:
                                    for tmp_store in tmp_stores:
                                        store = (tmp_store.replace("'", " ")).strip().capitalize()
                                        store_mng = StoreManager(db)
                                        store_mng.insert(Store(store[:50]))

                        bar.next()


            print("Database connected successfully")

        except Error as e:
            print(f"The error '{e}' occurred")
        mycursor.close()

        return db