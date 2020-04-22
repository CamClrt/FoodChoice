from data import *

class CityManager:

    def __init__(self, database):
        self.database = database

    def insert(self, products): #liste d'objets products
        pass

class City:

    id = 0
    def __init__(self, name, products):
        City.id += 1
        self.name = name
        self.products = products