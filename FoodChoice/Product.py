from data import *

class ProductManager:

    def __init__(self, database):
        self.database = database

    def insert_all(self, products): #liste d'objets products
        for product in products:
            pass

class Product:

    id = 0
    def __init__(self, name, brand, nutrition_grade, energy_100g, url, code, stores, places, categories): #ici une liste d'objet
        Product.id += 1
        self.name = name
        self.brand = brand
        self.nutrition_grade = nutrition_grade
        self.energy_100g = energy_100g
        self.url = url
        self.code = code
        self.stores = stores
        self.places = places
        self.categories = categories
        self.sustitute = None

    def __str__(self):
        return f"{self.name}, {self.code}, {self.brand}, {self.nutrition_grade},{self.energy_100g}cal, {self.url}"



#produit = Product(x, x, x, x, x, x, x, x, x, x, x)
#produit.manager.insert_all()

"""liste = []
for x in range(3):
    produit = Product(x, x, x, x, x, x, x, x, x, x, x)
    liste.append(produit)
    print(produit.id)

for item in liste:
    print(item)"""