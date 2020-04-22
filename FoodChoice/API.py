from data import *

import requests
import random
import re


class API:
    """Import data from OpenFoodFact's API and process them"""

    def __init__(self, products_key= PRODUCT_KEY,
                 products_url= PRODUCTS_URL,
                 products_name_field= PRODUCTS_NAME_FIELD,
                 categories_url= CATEGORIES_URL,
                 categories_key= CATEGORIES_KEY,
                 categories_name_field= CATEGORIES_NAME_FIELD,
                 categories_reg_exp= CATEGORIES_REG_EXP,
                 nb_cat_selected_among_the_list= NB_CAT_SELECTED_AMONG_THE_LIST,
                 ):

        self.products_key = products_key
        self.products_url = products_url
        self.products_name_field = products_name_field
        self.categories_url = categories_url
        self.categories_key = categories_key
        self.categories_name_field = categories_name_field
        self.categories_reg_exp = categories_reg_exp
        self.nb_cat_selected_among_the_list = nb_cat_selected_among_the_list

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
        """import products by category"""
        list_by_catgories = []

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
                temporary_product_list = [
                    product
                    for product in imported_product
                    if product.get(self.products_name_field) is not None
                ]
            except:
                print(f"The error : '{response.status_code}' occurred")
            list_by_catgories.append(temporary_product_list)

        products = [item for sublist in list_by_catgories for item in sublist]

        return products

    @property
    def products(self):
        """Return 4 objects :
        - a list witch contains all the products, one product = one tuple with this characteristics :
        (name, brand, nutrition_grade, energy_100g, url, code, stores, places, categories) ;
        - a set of stores depending on theses products ;
        - a set of places depending on theses products ;
        - a set of categories depending on theses products.
        """

        products = []
        product_stores = set()
        product_places = set()
        product_categories = set()

        for imported_product in self.import_products():
            #extract data and filter it to prepare the insertion in tables

            name = (imported_product.get("product_name_fr", "")[:150]).replace("'", "")

            brand = (imported_product.get("brands", "")[:100]).replace("'", "")

            nutrition_grade = imported_product.get("nutrition_grades", "")[:1]
            if imported_product.get("nutriments", "").get("energy_100g", "") is int:
                energy_100g = imported_product.get("nutriments", "").get("energy_100g", "")
            else:
                energy_100g = 0

            url = (imported_product.get("url", "")[:255]).replace("'", "")

            if imported_product.get("code", "") is int:
                code = imported_product.get("code", "") is int
            else:
                code = 0000000000000

            stores = imported_product.get("stores", "").split(',')
            for tmp_store in stores:
                store = (tmp_store.replace("'", " ")).strip()
                product_stores.add(store[:50])

            places = imported_product.get("purchase_places", "").split(',')
            for tmp_place in places:
                place = (tmp_place.replace("'", " ")).strip()
                product_places.add(place[:50])

            categories = imported_product.get("categories", "").split(',')
            for tmp_categorie in categories:
                categorie = (tmp_categorie.replace("'", " ")).strip()

                if re.search("..:", categorie):
                    if (categorie[:2]).lower() == "fr:":
                        product_categories.add(((categorie[3:]).capitalize())[:50])
                else:
                    product_categories.add(((categorie.capitalize()))[:50])

            products.append((name, brand, nutrition_grade, energy_100g, url, code, stores, places, categories))

        product_stores.discard("")
        product_places.discard("")
        product_categories.discard("")

        return products, product_stores, product_places, product_categories
