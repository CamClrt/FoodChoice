from data import *

class CategoryProductManager:
    """TODO ecrire"""

    def __init__(self, database):
        self.database = database

    def insert(self, categoryproduct_objects):

        data = []

        for categoryproduct_object in categoryproduct_objects:

            data.append((categoryproduct_object.product_id,
                         categoryproduct_object.category_id,))

        mycursor = self.database.cursor()
        mycursor.executemany(SQL_INSERT_CATEGORY_PRODUCT, data)
        self.database.commit()
        mycursor.close()

class CategoryProduct:
    """TODO ecrire"""

    def __init__(self, product_id, category_id):
        self.product_id = product_id
        self.category_id = category_id

    def __str__(self):
        """TODO ecrire"""
        return f"Product_ID : {self.product_id}, Category_ID : {self.category_id}"