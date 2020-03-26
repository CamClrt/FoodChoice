import json
import re
import requests
from data import *

class ProductManager:
    """Import datas from the OpenFoodFact API and process them"""
    def __init__(self, category):
        self.category = category
        self.payload = {}
        self.__response = ""
        self.__content = ""
        self.__imported_products = ""
        self.__product_list = []

    def import_data(self, products_key, products_url, products_name_fields, products__reg_exp):
        """import some products"""

        self.payload = {"action": "process",
                        "tagtype_0": "categories",
                        "tag_contains_0": "contains",
                        "tag_0": self.category,
                        "sort_by": "last_modified_t",
                        "page_size": "1000",
                        "json": "true"}

        self.__response = requests.get(products_url, params= self.payload)

        if self.__response.status_code == requests.codes.ok:
            self.__content = self.__response.json()
            self.__imported_products = self.__content.get(products_key)



        else:
            print("error : trying to consume the API in order to obtain products")

    def select_data(self, nb_cat_selected_among_the_list):
        """select some products"""
        pass



products = ProductManager("Boissons chaudes")
products.import_data(PRODUCT_KEY, PRODUCTS_URL, PRODUCTS_NAME_FIELDS, PRODUCTS_REG_EXP)