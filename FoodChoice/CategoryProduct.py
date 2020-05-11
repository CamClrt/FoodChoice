from data import *

class CategoryProductManager:
    """Manage CategoryProduct table"""

    def __init__(self, database):
        self.database = database

    def insert(self, categoryproduct_objects):
        """insert CategoryProduct objects in DB"""
        data = []

        for categoryproduct_object in categoryproduct_objects:
            data.append((categoryproduct_object.product_id,
                         categoryproduct_object.category_id,))

        mycursor = self.database.cursor()
        mycursor.executemany(SQL_INSERT_CATEGORY_PRODUCT, data)
        self.database.commit()
        mycursor.close()

class CategoryProduct:
    """Represent CategoryProduct table"""

    def __init__(self, product_id, category_id):
        self.product_id = product_id
        self.category_id = category_id

    def __str__(self):
        """Represent CategoryProduct object"""
        return f"Product_ID : {self.product_id}, Category_ID : {self.category_id}"