from data import *


class CategoryManager:

    def __init__(self, database):
        self.database = database

    def insert(self, category_object):
        mycursor = self.database.cursor()
        mycursor.execute(SQL_INSERT_CATEGORIES.replace("%s", category_object.name))
        self.database.commit()
        mycursor.execute(LAST_INSERT_ID)
        category_object.id = mycursor.fetchone()[0]
        return category_object


class Category:

    def __init__(self, name):
        self.id = ""
        self.name = name

    def __str__(self):
        return f"{self.id} {self.name}"