class ProductManager:

    def __init__(self, database):
        self.database = database

    def insert_all(self, products): #liste d'objets products
        for product in products:



class Product:

    id = 0
    def __init__(self, name, code, brand, nutrition_grade, energy_100g, url, categories, cities, stores): #ici une liste d'objet aussi
        Product.id += 1
        self.name = name
        self.code = code
        self.brand = brand
        self.nutrition_grade = nutrition_grade
        self.energy_100g = energy_100g
        self.url = url
        self.categories = categories
        self.cities = cities
        self.stores = stores
        self.sustitute = None #objet

    def __str__(self):
        return f"{self.name}, {self.code}, {self.brand}, {self.nutrition_grade},{self.energy_100g}, {self.url}, {self.sustitute}"



produit = Product(x, x, x, x, x, x, x, x, x, x, x)
produit.manager.insert_all()

"""liste = []
for x in range(3):
    produit = Product(x, x, x, x, x, x, x, x, x, x, x)
    liste.append(produit)
    print(produit.id)

for item in liste:
    print(item)"""