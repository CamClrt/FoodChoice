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
        return (id, category_object)


class Category:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name}"