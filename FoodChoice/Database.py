from data import *

from FoodChoice.API import *
from FoodChoice.Category import *
from FoodChoice.City import *
from FoodChoice.Store import *

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

                    #insert data
                    api = API()
                    products_imported, stores_imported, cities_imported, categories_imported = api.products
                    print("\n",
                          " /!\ WAITING: importation of the data, this may take a few minutes ".center(100, '-'),
                          "\n")

                    # insert categories in Category table
                    for category_imported in categories_imported:
                        category = Category(category_imported)
                        cat_mgr = CategoryManager(db)
                        cat_mgr.insert(category)
                    print("categories imported successfully")

                    # insert cities in City table
                    for city_imported in cities_imported:
                        city = City(city_imported)
                        city_mgr = CityManager(db)
                        city_mgr.insert(city)
                    print("cities imported successfully")

                    # insert stores in Store table
                    for store_imported in stores_imported:
                        store = Store(store_imported)
                        store_mgr = StoreManager(db)
                        store_mgr.insert(store)
                    print("stores imported successfully")

                    


            print("Database connected successfully \n")
        except Error as e:
            print(f"The error '{e}' occurred")
        mycursor.close()

        return db