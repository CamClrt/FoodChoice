from data import *

import requests
import random
import re


class API:
    """Import data from OpenFoodFact's API and process them"""

    def __init__(self):
        self.products_key = PRODUCT_KEY
        self.products_url = PRODUCTS_URL
        self.products_name_field = PRODUCTS_NAME_FIELD
        self.categories_url = CATEGORIES_URL
        self.categories_key = CATEGORIES_KEY
        self.categories_name_field = CATEGORIES_NAME_FIELD
        self.categories_reg_exp = CATEGORIES_REG_EXP
        self.nb_cat_selected_among_the_list = NB_CAT_SELECTED_AMONG_THE_LIST

    def import_categories(self):
        """Import categories"""
        response = requests.get(self.categories_url, timeout=10)

        try:
            response.status_code == requests.codes.ok
            content = response.json()
            imported_categories = content.get(self.categories_key)

            temporary_category_list = [
                imported_category[self.categories_name_field]
                for imported_category in imported_categories
                if re.fullmatch(self.categories_reg_exp, imported_category[self.categories_name_field]) is not None
            ]

            category_list = [
                category.replace("'", "")  # exclude the ' character in the field to avoid SQL error
                for category in temporary_category_list
            ]

        except:
            print(f"The error : '{response.status_code}' occurred")

        return category_list

    @property
    def categories(self):
        """Return a selection of categories"""
        categories = self.import_categories()
        random.seed(SEED)
        return random.sample(categories, self.nb_cat_selected_among_the_list)


    def import_products(self):
        """import products and store them in a dictionnary"""
        products_dictionnary = {} #key: category & value: a list of products in JSON format

        for category in self.categories:
            PAYLOAD["tag_0"] = "'" + str(category) + "'"
            response = requests.get(self.products_url, params=PAYLOAD, timeout=10)

            try:
                response.status_code == requests.codes.ok
                content = response.json()
                imported_products = content.get(self.products_key)

                imported_product = [
                    imported_product
                    for imported_product in imported_products
                ]

                # select only the products with nutrition_grade
                product_list = [
                    product
                    for product in imported_product
                    if product.get(self.products_name_field) is not None
                ]
            except:
                print(f"The error : '{response.status_code}' occurred")

            products_dictionnary[category] = product_list
        return products_dictionnary

    @property
    def products(self):
        """Return the whole products in a dictionnary"""
        return self.import_products()