class ProductManager:

    def __init__(self, database):
        self.database = database

class Product:

    objects = ProductManager(db)

    def __init__(self, id, name, code, brand, nutrition_grade, energy_100g,\
                 url, sustitute, categories, cities, stores, **kwargs):
        self.id = id
        self.name = name
        self.code = code
        self.brand = brand
        self.nutrition_grade = nutrition_grade
        self.energy_100g = energy_100g
        self.url = url
        self.categories = categories
        self.cities = cities
        self.stores = stores
        self.sustitute = sustitute

    def __str__(self):
        return f"{self.name}, {self.code}, {self.brand}, {self.nutrition_grade},{self.energy_100g},\
                    {self.url}, {self.categories}, {self.cities}, {self.stores}, {self.sustitute}"

    def convert_as_tuple(self):
        return (self.name, self.code, self.brand, self.nutrition_grade, self.energy_100g,\
                self.url, self.categories, self.cities, self.stores, self.sustitute)