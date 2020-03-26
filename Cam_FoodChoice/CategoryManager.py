from data import *
import requests
import random
import re

class Category():
    """Create Category table in the database and import data"""
    pass

class CategoryManager():
    """Import datas from the OpenFoodFact API and process them"""
    def __init__(self):
        self.__category_list = [] # an extract of the whole categories
        self.__categories_selected_list = []  # an extract and a selection of categories

    def import_data(self, categories_url, categories_key, categories_name_fields, categories_reg_exp):
        """import categories"""

        response = ""  # the response at the http get request
        content = ""  # the content in json format at the http get request
        imported_categories = []  # an extract of the whole categories

        response = requests.get(categories_url)

        if response.status_code != requests.codes.ok:
            print("error : trying to consume the API in order to obtain categories")
        else:
            content = response.json()
            imported_categories = content.get(categories_key)

            self.__category_list = [
                imported_category[categories_name_fields]
                for imported_category in imported_categories
                if re.fullmatch(categories_reg_exp, imported_category[categories_name_fields]) is not None
            ]

    def select_data(self, nb_cat_selected_among_the_list):
        """select randomly some categories"""
        random.seed(SEED)
        self.__categories_selected_list = random.sample(self.__category_list, nb_cat_selected_among_the_list)

    @property
    def categories(self):
        """Return the categories selected"""
        self.import_data(CATEGORIES_URL, CATEGORIES_KEY, CATEGORIES_NAME_FIELDS, CATEGORIES_REG_EXP)
        self.select_data(NB_CAT_SELECTED_AMONG_THE_LIST)
        return self.__categories_selected_list

category = CategoryManager()
print(category.categories)