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

        if response.status_code == requests.codes.ok:
            content = response.json()
            imported_categories = content.get(categories_key)

            self.__category_list = [
                imported_category[categories_name_field]
                for imported_category in imported_categories
                if re.fullmatch(categories_reg_exp, imported_category[categories_name_field]) is not None
            ]

        else:
            print("error")

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


class Category():
    """Create Category table in the database and import data"""

    def __init__(self):
        pass

    def create_category_table(self, db):
    #TODO : writing docstring

        mycursor = db.cursor()

        query = "CREATE TABLE `Category` (`ID` SMALLINT UNSIGNED,`Name` VARCHAR(75),PRIMARY KEY (`ID`))"

        try:
            mycursor.execute(query)
            print("Category table creation to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

food_choice = DatabaseManager()
db = food_choice.init_database()

category = Category()
category.create_category_table(db)