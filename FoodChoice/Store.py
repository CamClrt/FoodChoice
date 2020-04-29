from data import *

class StoreManager:

    def __init__(self, database):
        self.database = database

    def find(self, store_name):
        """search if store_name already exists in the store table and insert it"""
        mycursor = self.database.cursor()
        mycursor.execute(SQL_SELECT_STORE.replace("%s", store_name))
        res = mycursor.fetchone()
        store = Store(store_name)
        if res is None:
            return self.insert(store)
        else:
            store.id = res[0]
            return store

    def insert(self, store_object):
        mycursor = self.database.cursor()
        mycursor.execute(SQL_INSERT_STORES.replace("%s", store_object.name))
        self.database.commit()
        mycursor.execute(LAST_INSERT_ID)
        store_object.id = mycursor.fetchone()[0]
        return store_object


class Store:

    def __init__(self, name):
        self.id = ""
        self.name = name

    def __str__(self):
        return f"{self.id} {self.name}"