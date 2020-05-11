from data import *

class StoreManager:
    """Manage Store table"""

    def __init__(self, database):
        self.database = database

    def find(self, store_name):
        """search if store_name already exists in the store table and insert it"""
        mycursor = self.database.cursor()
        mycursor.execute(SQL_SELECT_STORE, (store_name, ))
        res = mycursor.fetchone()
        mycursor.close()
        store = Store(store_name)
        if res is None:
            return self.insert(store)
        else:
            store.id = int(res[0])
            return store

    def insert(self, store_object):
        """insert """
        mycursor = self.database.cursor()
        mycursor.execute(SQL_INSERT_STORES, (store_object.name, ))
        self.database.commit()
        mycursor.execute(LAST_INSERT_ID)
        store_object.id = mycursor.fetchone()[0]
        mycursor.close()
        return store_object


class Store:
    """Represent Store table"""

    def __init__(self, name):
        self.id = ""
        self.name = name

    def __str__(self):
        """Represent Store object"""
        return f"{self.id} {self.name}"