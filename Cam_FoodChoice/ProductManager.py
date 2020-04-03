from data import *
import json
import requests


class ProductManager:
    """Import datas from the OpenFoodFact API and process them"""
    def __init__(self, category):
        self.category = category
        self.product_list = [] # an extract and a selection of products

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

        response = requests.get(products_url, params=payload, timeout=10)

        try:
            response.status_code == requests.codes.ok
            content = response.json()
            imported_products = content.get(products_key)

            imported_product = [
                imported_product
                for imported_product in imported_products
            ]

            # keep just the products with a nutrition_grade
            self.product_list = [
                product
                for product in imported_product
                if product.get(products_name_field) is not None
            ]

        except:
            print(f"The error : '{response.status_code}' occurred")

        return self.product_list


"""class Product():
    # TODO : writing docstring

    for product in ??? :

        try:
            print("product_name_fr : ", product["product_name_fr"])
        except KeyError:
            print("product_name_fr : pas de clé")

        try:
            print("brands : ", product["brands"])
        except KeyError:
            print("brands : pas de clé")

        try:
            print("nutrition_grades : ", product["nutrition_grades"])
        except KeyError:
            print("nutrition_grades : pas de clé")

        try:
            print("ingredients_text : ", product["ingredients_text"])
        except KeyError:
            print("ingredients_text : pas de clé")

        try:
            dico = product["nutriments"]
            try:
                print("energy_100g", dico["energy_100g"])
            except KeyError:
                print("energy_100g : pas de clé")
        except KeyError:
            print("nutriments : pas de clé")

        try:
            print("url : ", product["url"])
        except KeyError:
            print("url : pas de clé")

        try:
            print("code : ", product["code"])
        except KeyError:
            print("code : pas de clé")

        try:
            print("stores : ", product["stores"])
        except KeyError:
            print("stores : pas de clé")"""

# -------------- Execution ------------------

"""products = ProductManager("Biscuit")
print(products.import_data(PRODUCT_KEY, PRODUCTS_URL, PRODUCTS_NAME_FIELD))"""