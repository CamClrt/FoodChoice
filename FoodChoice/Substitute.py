from data import *
from FoodChoice.Product import *

class SubstituteManager:
    """TODO ecrire"""

    def __init__(self, database):
        self.database = database

    def substitute_and_display(self, category_selected, product_grade, product_energy):
        """Substitute the product by a another product healthier and display it"""
        data = (category_selected, product_grade, product_energy, )
        mycursor = self.database.cursor()
        mycursor.execute(SQL_SELECT_SUBSTITUTE, data)
        substitute = mycursor.fetchall()[0]
        mycursor.close()

        product_mng = ProductManager(self.database)
        product_mng.display_product(substitute[0])

        return substitute


class Substitute:
    """TODO ecrire"""

    def __init__(self, id, date, user):
        self.id = id
        self.date = date
        self.user = user
        self.product = None

    def __str__(self):
        """TODO ecrire"""
        return f"{self.id}, {self.date}, {self.user}"