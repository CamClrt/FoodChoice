class Product:

    id = 0

    def __init__(self, name, code, brand, nutrition_grade, energy_100g, url,\
                 sustitute, database, categories, cities, stores, **kwargs):
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
        self._database = database
        self.sustitute = sustitute

    def __str__(self):
        return f"{self.name}, {self.code}, {self.brand}, {self.nutrition_grade},{self.energy_100g}, {self.url}"

    def create(self):
        pass

liste = []
for x in range(3):
    produit = Product(x, x, x, x, x, x, x, x, x, x, x)
    liste.append(produit)
    print(produit.id)

for item in liste:
    print(item)