from data import *

class CategoryManager:

    def __init__(self, database):
        self.database = database

    def insert(self, category_object):
        name = category_object.name
        mycursor = self.database.cursor()
        mycursor.execute(SQL_INSERT_CATEGORIES.replace("%s", name))
        self.database.commit()

        mycursor.execute(LAST_INSERT_ID)
        id = mycursor.fetchone()

        return id, category_object.products


class Category:

    id = 0
    def __init__(self, name, products):
        Category.id += 1
        self.name = name
        self.products = products # a list of product object

    def __str__(self):
        return f"{self.name}"