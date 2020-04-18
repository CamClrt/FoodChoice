from FoodChoice.data import *

import json
import requests


class API_Product:
    """Import data from OpenFoodFact's API and process them"""

    def __init__(self, category):
        self.__category = category
        self.__product_list = []
        self.__products_key = PRODUCT_KEY
        self.__products_url = PRODUCTS_URL
        self.__products_name_field = PRODUCTS_NAME_FIELD


    def import_data(self):
        """import products"""
        response = ""  # the response at the http get request
        content = {}  # the content in json format at the http get request
        imported_products = []  # an extract of the whole products
        product_list_int = []  # an extract of 1000 products
        product = ""

        insert_in_payload = "'" + str(self.__category) + "'"
        PAYLOAD["tag_0"] = insert_in_payload
        response = requests.get(self.__products_url, params=PAYLOAD, timeout=10)

        try:
            response.status_code == requests.codes.ok
            content = response.json()
            imported_products = content.get(self.__products_key)

            imported_product = [
                imported_product
                for imported_product in imported_products
            ]

            # select only the products with nutrition_grade
            self.__product_list = [
                product
                for product in imported_product
                if product.get(self.__products_name_field) is not None
            ]

        except:
            print(f"The error : '{response.status_code}' occurred")

    @property
    def products(self):
        """Return products"""
        self.import_data()
        return self.__product_list