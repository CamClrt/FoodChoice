from data import *
from FoodChoice.Product import *

class SubstituteManager:
    """TODO ecrire"""

    def __init__(self, database):
        self.database = database

    def substitute_and_display(self, product_id):
        """Substitute the product by a another product healthier"""
        mycursor = self.database.cursor()
        mycursor.execute(SQL_SELECT_SUBSTITUTE, product_id)
        substitute_id = mycursor.fetchone()[0]
        mycursor.close()

        product_mng = ProductManager(self.database)
        product_mng.display_product(substitute[0])

        return substitute_id

    def insert(self, substitute_object):
        pass


class Substitute:
    """TODO ecrire"""

    def __init__(self, id, date, user, product):
        self.id = id
        self.date = date
        self.user = user
        self.product = product

    def __str__(self):
        """TODO ecrire"""
        return f"{self.id}, {self.date}, {self.user}"