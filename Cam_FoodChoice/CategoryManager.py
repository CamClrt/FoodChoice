from data import *
import requests
import random
import re

class CategoryManager():
    """Import datas from the OpenFoodFact API and process them"""
    def __init__(self):
        def __init__(self):
            self.__response = ""  # the response at the http get request
            self.__content = ""  # the content in json format at the http get request
            self.__imported_categories_int = ""  # a complete extract of the whole categories
            self.__imported_categories = ""  # an extract of the whole categories
            self.__category_list = []  # an extract of the whole categories
            self.__categories_selected_list = []  # an extract and a selection of categories

    def import_data(self, categories_url, categories_key, categories_name_fields, categories_reg_exp):
        """import categories and drop the categories starting with the id's country"""
        self.__response = requests.get(categories_url)

        if self.__response.status_code != 200:
            print("error : trying to consume the API in order to obtain categories")
        else:
            self.__content = self.__response.json()
            self.__imported_categories = self.__content.get(categories_key)

            self.__category_list = [
                imported_category[categories_name_fields]
                for imported_category in self.__imported_categories
                if re.fullmatch(categories_reg_exp, imported_category[categories_name_fields]) is not None
            ]
        print(f"Categories selected :{len(self.__category_list)} on {len(self.__imported_categories)}")

    def select_data(self, nb_cat_selected_among_the_list):
        """select randomly some categories"""
        self.__categories_selected_list = random.sample(self.__category_list, nb_cat_selected_among_the_list)

    @property
    def categories(self):
        """Return the categories selected"""
        self.import_data(CATEGORIES_URL, CATEGORIES_KEY, CATEGORIES_NAME_FIELDS, CATEGORIES_REG_EXP)
        self.select_data(NB_CAT_SELECTED_AMONG_THE_LIST)
        return self.__categories_selected_list

category = CategoryManager()
print(category.categories)