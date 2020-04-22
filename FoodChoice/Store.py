from data import *

class StoreManager:

    def __init__(self, database):
        self.database = database

    def insert(self, store_object):
        name = store_object.name
        mycursor = self.database.cursor()
        mycursor.execute(SQL_INSERT_STORES.replace("%s", name))
        self.database.commit()
        mycursor.execute(LAST_INSERT_ID)
        id = mycursor.fetchone()
        return id, store_object


class Store:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"{self.name}"