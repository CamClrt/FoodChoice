"""
    This module manage all operations with the API
"""

import re
from progress.bar import Bar
import requests
from colorama import Fore, Style
from utils import config


class API:
    """Import products from OpenFoodFact's API"""

    def __init__(self, products_key=config.PRODUCT_KEY,
                 products_url=config.PRODUCTS_URL,
                 products_name_field=config.PRODUCTS_NAME_FIELD,
                 categories_url=config.CATEGORIES_URL,
                 categories_key=config.CATEGORIES_KEY,
                 categories_name_field=config.CATEGORIES_NAME_FIELD,
                 categories_regex=config.CATEGORIES_REGEX,
                 nb_cat_selected=config.NB_CAT_SELECTED_AMONG_THE_LIST):

        self.products_key = products_key
        self.products_url = products_url
        self.products_name_field = products_name_field
        self.categories_url = categories_url
        self.categories_key = categories_key
        self.categories_name_field = categories_name_field
        self.categories_regex = categories_regex
        self.nb_cat_selected = nb_cat_selected

    @property
    def categories(self):
        """Import and return a selection of categories"""
        headers = {'date': config.DATE, 'user-agent': config.APP_NAME}
        response = requests.get(self.categories_url,
                                headers=headers,
                                timeout=10)
        log = f"{response.headers['Date']}', '" \
              f"{self.nb_cat_selected}', '" \
              f"{response.headers['Content-Type']}', '" \
              f"{response.headers['Connection']}\n"

        with open('log.txt', 'a', encoding="utf-8") as file:
            file.write(log)

        if response.status_code == 200:
            content = response.json()
            imported_categories = content.get(self.categories_key)

            # keep only a selection of x categories capitalized
            category_list = [
                imported_category[self.categories_name_field]
                for imported_category in imported_categories
                if re.fullmatch(
                    self.categories_regex,
                    imported_category[self.categories_name_field]) is not None]
        else:
            err = f"The error : '{response.status_code}' occurred"
            print(err)
            with open('log.txt', 'a', encoding="utf-8") as file:
                file.write(err)

        return category_list[:self.nb_cat_selected]

    @property
    def products(self):
        """Import and return a selection of products by category"""
        products = []

        print(Fore.GREEN)
        print("\n-----> Importation des données depuis"
              " l'API d'Open Food Facts <-----\n")
        with Bar('Progression', max=len(self.categories)) as progress_bar:
            for category in self.categories:
                config.PAYLOAD["tag_0"] = "'" + str(category) + "'"
                headers = {'date': config.DATE, 'user-agent': config.APP_NAME}
                response = requests.get(self.products_url,
                                        params=config.PAYLOAD,
                                        headers=headers,
                                        timeout=10)
                log = f"{response.headers['Date']}', '" \
                      f"{category}', '" \
                      f"{response.headers['Content-Type']}', '" \
                      f"{response.headers['Connection']}\n"

                with open('log.txt', 'a', encoding="utf-8") as file:
                    file.write(log)

                if response.status_code == 200:
                    content = response.json()
                    products.extend(content.get(self.products_key))
                else:
                    err = f"L'erreur : '{response.status_code}' est survenue"
                    print(err)
                    with open('log.txt', 'a', encoding="utf-8") as file:
                        file.write(err)

                progress_bar.next()

        print(f"\n----> {len(products)} produits importés <----")
        print(Style.RESET_ALL)

        return products
