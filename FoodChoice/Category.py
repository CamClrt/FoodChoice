from data import *


class CategoryManager:

    def __init__(self, database):
        self.database = database

    def find(self, category_name):
        """search if category_name already exists in the category table and insert it"""
        mycursor = self.database.cursor()
        mycursor.execute(SQL_SELECT_CATEGORY.replace("%s", category_name))
        res = mycursor.fetchone()
        mycursor.close()
        category = Category(category_name)
        if res is None:
            return self.insert(category)
        else:
            category.id = int(res[0])
            return category

    def insert(self, category_object):
        """insert category_object in DB"""
        mycursor = self.database.cursor()
        mycursor.execute(SQL_INSERT_CATEGORIES.replace("%s", category_object.name))
        self.database.commit()
        mycursor.execute(LAST_INSERT_ID)
        category_object.id = mycursor.fetchone()[0]
        mycursor.close()
        return category_object


class Category:

    def __init__(self, name):
        self.id = ""
        self.name = name

    def __str__(self):
        return f"{self.id} {self.name}"