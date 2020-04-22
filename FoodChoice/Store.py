from data import *

class StoreManager:

    def __init__(self, database):
        self.database = database

    def insert(self, products): #liste d'objets products
        pass

class Store:

    id = 0
    def __init__(self, name, products):
        store.id += 1
        self.name = name
        self.products = products