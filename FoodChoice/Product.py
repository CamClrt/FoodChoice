from data import *


class ProductManager:

    def __init__(self, database):
        self.database = database

    def insert(self, product_object):
        mycursor = self.database.cursor()

        data = "('" + product_object.name + "','" \
               + product_object.brand + "','" \
               + product_object.nutrition_grade + "'," \
               + str(product_object.energy_100g) + ",'" \
               + product_object.url + "'," \
               + str(product_object.code) + ")"

        mycursor = self.database.cursor()
        mycursor.execute(SQL_INSERT_PRODUCTS.replace("%s", data))
        self.database.commit()
        mycursor.execute(LAST_INSERT_ID)
        product_object.id = mycursor.fetchone()[0]
        return product_object


class Product:

    def __init__(self, name, brand, nutrition_grade, energy_100g, url, code, stores, cities, categories):
        self.id = ""
        self.name = name
        self.brand = brand
        self.nutrition_grade = nutrition_grade
        self.energy_100g = energy_100g
        self.url = url
        self.code = code
        self.stores = stores
        self.cities = cities
        self.categories = categories
        self.sustitute = None

    def __str__(self):
        return f"{self.name}, {self.code}, {self.brand}, {self.nutrition_grade},{self.energy_100g}cal, {self.url}"