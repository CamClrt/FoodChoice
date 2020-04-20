class CategoryManager:

    def __init__(self, database):
        self.database = database

class Category:

    objects = ProductManager(db)

    def __init__(self, id, name, products, **kwargs):
        self.id = id
        self.name = name
        self.products = products

    def __str__(self):
        return f"{self.name}, {self.products}"

    def convert_as_tuple(self):
        return (self.name, self.products)