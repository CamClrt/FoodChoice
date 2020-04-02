from data import *
import requests
import random
import re
from mysql.connector import Error
from Cam_FoodChoice.DatabaseManager import DatabaseManager


class CategoryManager():
    """Import datas from the OpenFoodFact API and process them"""
    def __init__(self):
        self.__category_list = [] # an extract of the whole categories
        self.__categories_selected_list = []  # an extract and a selection of categories

    def import_data(self, categories_url, categories_key, categories_name_field, categories_reg_exp):
        """import categories"""

        response = ""  # the response at the http get request
        content = ""  # the content in json format at the http get request
        imported_categories = []  # an extract of the whole categories

        response = requests.get(categories_url, timeout=5)

        try:
            response.status_code == requests.codes.ok
            content = response.json()
            imported_categories = content.get(categories_key)

            self.__category_list = [
                imported_category[categories_name_field]
                for imported_category in imported_categories
                if re.fullmatch(categories_reg_exp, imported_category[categories_name_field]) is not None
            ]

        except:

            print(f"The error : '{response.status_code}' occurred")

    def select_data(self, nb_cat_selected_among_the_list):
        """select randomly some categories"""
        random.seed(SEED)
        self.__categories_selected_list = random.sample(self.__category_list, nb_cat_selected_among_the_list)

    @property
    def categories(self):
        """Return the categories selected"""
        self.import_data(CATEGORIES_URL, CATEGORIES_KEY, CATEGORIES_NAME_FIELD, CATEGORIES_REG_EXP)
        self.select_data(NB_CAT_SELECTED_AMONG_THE_LIST)
        return self.__categories_selected_list


# -------------- Execution ------------------

food_choice = DatabaseManager()
db = food_choice.init_database()

categorymanager = CategoryManager()
print(categorymanager.categories)