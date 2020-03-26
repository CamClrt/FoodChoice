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
        self.product_list = [] # an extract of products with "nutrition_grade_fr_producer"
        self.products_selected_list = []  # an extract and a selection of products

    def import_data(self, products_key, products_url):
        """import some products"""

        response = ""  # the response at the http get request
        content = {}  # the content in json format at the http get request
        imported_products = []  # an extract of the whole products
        product_list_int = []  # an extract of 1000 products
        product = ""

        payload = {"action": "process",
                    "tagtype_0": "categories",
                    "tag_contains_0": "contains",
                    "tag_0": self.category,
                    "sort_by": "last_modified_t",
                    "page_size": "500",
                    "json": "true"}

        response = requests.get(products_url, params = payload)

        if response.status_code == requests.codes.ok:
            content = response.json()
            imported_products = content.get(products_key)

            imported_product = [
                imported_product
                for imported_product in imported_products
            ]

            # keep just the products with a nutrition_grade
            self.products_selected_list = [
                product
                for product in imported_product
                if product.get("nutrition_grades") is not None
            ]

            with open("data_file.json", "w") as write_file:
                json.dump(self.products_selected_list, write_file, indent=4)

        else:
            print("error : trying to consume the API in order to obtain products")

        return self.products_selected_list

products = ProductManager("Thés verts à la menthe")
print(len(products.import_data(PRODUCT_KEY, PRODUCTS_URL)))