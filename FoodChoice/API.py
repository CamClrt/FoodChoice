from data import *
from progress.bar import Bar
import requests
import random
import re


class API:
    """Import products from OpenFoodFact's API"""

    def __init__(self, products_key= PRODUCT_KEY,
                 products_url= PRODUCTS_URL,
                 products_name_field= PRODUCTS_NAME_FIELD,
                 categories_url= CATEGORIES_URL,
                 categories_key= CATEGORIES_KEY,
                 categories_name_field= CATEGORIES_NAME_FIELD,
                 categories_regex= CATEGORIES_REGEX,
                 nb_cat_selected_among_the_list= NB_CAT_SELECTED_AMONG_THE_LIST,
                 ):

        self.products_key = products_key
        self.products_url = products_url
        self.products_name_field = products_name_field
        self.categories_url = categories_url
        self.categories_key = categories_key
        self.categories_name_field = categories_name_field
        self.categories_regex = categories_regex
        self.nb_cat_selected_among_the_list = nb_cat_selected_among_the_list

    @property
    def categories(self):
        """Import and return a selection of categories"""
        headers = {'date': DATE, 'user-agent': APP_NAME}
        response = requests.get(self.categories_url, headers=headers, timeout=10)
        log = f"API : Date: '{response.headers['Date']}', ' \
                        'Import categories '{self.nb_cat_selected_among_the_list}': ' \
                        'Content-Type: '{response.headers['Content-Type']}', ' \
                        'Connection: '{response.headers['Connection']}\n"

        with open('log.txt', 'a', encoding="utf-8") as file:
            file.write(log)

        try:
            response.status_code == requests.codes.ok
            content = response.json()
            imported_categories = content.get(self.categories_key)

            # keep only a selection of x categories capitalized
            category_list = [
                imported_category[self.categories_name_field]
                for imported_category in imported_categories
                if re.fullmatch(self.categories_regex, imported_category[self.categories_name_field]) is not None
            ]

        except:
            err = f"The error : '{response.status_code}' occurred"
            print(err)
            with open('log.txt', 'a', encoding="utf-8") as file:
                file.write(err)

        random.seed(SEED)

        return random.sample(category_list, self.nb_cat_selected_among_the_list)

    @property
    def products(self):
        """Import and return a selection of products by category"""
        products = []

        print("\n-----> Importing data from Open Food Facts API <-----")
        with Bar('Processing', max=len(self.categories)) as bar:
            for category in self.categories:
                PAYLOAD["tag_0"] = "'" + str(category) + "'"
                headers = {'date': DATE, 'user-agent': APP_NAME}
                response = requests.get(self.products_url, params=PAYLOAD, headers=headers, timeout=10)
                log = f"API : Date: '{response.headers['Date']}', ' \
                                'Import products in '{category}': ' \
                                'Content-Type: '{response.headers['Content-Type']}', ' \
                                'Connection: '{response.headers['Connection']}\n"

                with open('log.txt', 'a', encoding="utf-8") as file:
                    file.write(log)

                try:
                    response.status_code == requests.codes.ok
                    content = response.json()
                    products.extend(content.get(self.products_key))

                except:
                    err = f"The error : '{response.status_code}' occurred"
                    print(err)
                    with open('log.txt', 'a', encoding="utf-8") as file:
                        file.write(err)

                bar.next()

        print(f"--------------> {len(products)} products imported <--------------")

        return products