from src.utils.queries import *


class CategoryManager:
    """Manage Category table"""

    def __init__(self, database):
        self.database = database

    def find(self, category_name):
        """search if category_name already exists and insert it"""
        mycursor = self.database.cursor()
        mycursor.execute(SQL_SELECT_CATEGORY, (category_name, ))
        res = mycursor.fetchone()
        mycursor.close()
        category_object = Category(category_name)
        if res is None:
            return self.insert(category_object)
        else:
            category_object.id = int(res[0])
            return category_object

    def most_used_categories(self):
        """search the 20 most used categories and order them"""
        mycursor = self.database.cursor()
        mycursor.execute(SQL_SELECT_CATEGORIES)
        categories = mycursor.fetchall()
        mycursor.close()
        return categories

    def insert(self, category_object):
        """insert category_object in DB"""
        mycursor = self.database.cursor()
        mycursor.execute(SQL_INSERT_CATEGORIES, (category_object.name, ))
        self.database.commit()
        mycursor.execute(LAST_INSERT_ID)
        category_object.id = mycursor.fetchone()[0]
        mycursor.close()
        return category_object


class Category:
    """Represent Category table"""

    def __init__(self, name):
        self.id = ""
        self.name = name

    def __str__(self):
        """Represent Category object"""
        return f"{self.id} {self.name}"
