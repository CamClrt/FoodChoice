from data import *
import json
import requests


class ProductManager:
    """Import datas from the OpenFoodFact API and process them"""
    def __init__(self, category):
        self.category = category
        self.product_list = [] # an extract and a selection of products
        self.products_key = PRODUCT_KEY
        self.products_url = PRODUCTS_URL
        self.products_name_field = PRODUCTS_NAME_FIELD

    def import_data(self):
        """import some products"""

        response = ""  # the response at the http get request
        content = {}  # the content in json format at the http get request
        imported_products = []  # an extract of the whole products
        product_list_int = []  # an extract of 1000 products
        product = ""

        #payload = {"action": "process", TODO à supprimer si ok
        # "tagtype_0": "categories",
        # "tag_contains_0": "contains",
        # "tag_0": self.category,
        # "sort_by": "last_modified_t",
        # "page_size": "500",
        # "json": "true"}

        insert_in_payload = "'" + self.category + "'"

        PAYLOAD["tag_0"] = insert_in_payload

        response = requests.get(self.products_url, params=PAYLOAD, timeout=10)

        try:
            response.status_code == requests.codes.ok
            content = response.json()
            imported_products = content.get(self.products_key)

            imported_product = [
                imported_product
                for imported_product in imported_products
            ]

            # keep just the products with a nutrition_grade
            self.product_list = [
                product
                for product in imported_product
                if product.get(self.products_name_field) is not None
            ]

        except:
            print(f"The error : '{response.status_code}' occurred")

        return self.product_list