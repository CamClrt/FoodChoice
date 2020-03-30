from data import *
import json
import requests


class ProductManager:
    """Import datas from the OpenFoodFact API and process them"""
    def __init__(self, category):
        self.category = category
        self.product_list = [] # an extract of products with "nutrition_grade_fr_producer"
        self.products_selected_list = []  # an extract and a selection of products

    def import_data(self, products_key, products_url, products_name_field):
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

        response = requests.get(products_url, params = payload, timeout=10)

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
                if product.get(products_name_field) is not None
            ]

        else:
            print("error")

        "Create Product table in the database and import data"""

        for i in range(len(products.products_selected_list) - 1):
            product = self.products_selected_list[i]

            liste = []
            #iste.append(product.get("product_name_fr"))
            #liste.append(product.get("brands"))
            #liste.append(product.get("nutrition_grades"))
            #liste.append(product.get("ingredients_text"))
            #liste.append(product.get("nutriments")) # TODO aller chercher energy_100g dans le dico nutriments
            #liste.append(product.get("url"))
            #liste.append(product.get("code"))
            #liste.append(product.get("stores"))
            # TODO trouver le champs catégorie pour faire le lien avec product
            #liste.append("FIN")

        return self.products_selected_list


class Product():
    pass


products = ProductManager("Biscuit")
products.import_data(PRODUCT_KEY, PRODUCTS_URL, PRODUCTS_NAME_FIELD)