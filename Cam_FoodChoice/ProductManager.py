import json
import re
import requests
from data import *

class Product():
    """Create Product table in the database and import data"""
    pass

class ProductManager:
    """Import datas from the OpenFoodFact API and process them"""
    def __init__(self, category):
        self.category = category
        self.product_list = []

    def import_data(self, products_key, products_url, products_reg_exp, products_name_fields):
        """import some products"""

        response = ""  # the response at the http get request
        content = {}  # the content in json format at the http get request
        imported_products = []  # an extract of the whole categories

        payload = {"action": "process",
                    "tagtype_0": "categories",
                    "tag_contains_0": "contains",
                    "tag_0": self.category,
                    "sort_by": "last_modified_t",
                    "page_size": "1000",
                    "json": "true"}

        response = requests.get(products_url, params = payload)

        if response.status_code == requests.codes.ok:
            content = response.json()
            imported_products = content.get(products_key)

            self.product_list = [
                imported_product
                for imported_product in imported_products
                #if re.fullmatch(products_reg_exp, imported_product[products_name_fields]) is not None
            ]

        else:
            print("error : trying to consume the API in order to obtain products")
        return self.product_list



products = ProductManager("Boissons chaudes")
print(type(products.import_data(PRODUCT_KEY, PRODUCTS_URL, PRODUCTS_REG_EXP, PRODUCTS_NAME_FIELDS)))
print(len(products.import_data(PRODUCT_KEY, PRODUCTS_URL, PRODUCTS_REG_EXP, PRODUCTS_NAME_FIELDS)))