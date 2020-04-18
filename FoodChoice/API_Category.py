from data import *

import requests
import random
import re


class API_Category():
    """Import data from OpenFoodFact's API and process them"""

    def __init__(self):
        self.__category_list = []  # an extract of the whole categories
        self.__categories_selected_list = []  # a selection of categories


    def import_data(self, categories_url, categories_key, categories_name_field, categories_reg_exp):
        """Import categories"""
        response = ""  # the response at the http get request
        content = ""  # the content in json format at the http get request
        imported_categories = []  # an extract of the whole categories

        response = requests.get(categories_url, timeout=10)

        try:
            response.status_code == requests.codes.ok
            content = response.json()
            imported_categories = content.get(categories_key)

            temporary_category_list = [
                imported_category[categories_name_field]
                for imported_category in imported_categories
                if re.fullmatch(categories_reg_exp, imported_category[categories_name_field]) is not None
            ]

            self.__category_list = [
                category.replace("'", "")  # exclude the ' character in the field to avoid SQL error
                for category in temporary_category_list
            ]

        except:
            print(f"The error : '{response.status_code}' occurred")

    def select_data(self, nb_cat_selected_among_the_list):
        """Select categories randomly"""
        random.seed(SEED)
        self.__categories_selected_list = random.sample(self.__category_list, nb_cat_selected_among_the_list)

    @property
    def categories(self):
        """Return categories"""
        self.import_data(CATEGORIES_URL, CATEGORIES_KEY, CATEGORIES_NAME_FIELD, CATEGORIES_REG_EXP)
        self.select_data(NB_CAT_SELECTED_AMONG_THE_LIST)
        return self.__categories_selected_list