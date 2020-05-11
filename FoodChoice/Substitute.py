from data import *
from FoodChoice.Product import *
from mysql.connector import Error

class SubstituteManager:
    """TODO écrire"""

    def __init__(self, database):
        self.database = database

    def substitute_and_display(self, sql, user_object):
        """Substitute the product by a another product healthier"""
        mycursor = self.database.cursor()
        query = SQL_SELECT_SUBSTITUTE.replace("%s", sql) #TODO à revoir avec Aymen
        mycursor.execute(query)
        substitute_id = mycursor.fetchall()[0][0]
        mycursor.close()
        product_mng = ProductManager(self.database)
        product_mng.display_product(substitute_id)
        substitute_object = Substitute(user_object.id, substitute_id)
        return substitute_object

    def insert(self, substitute_object):
        """TODO : écrire"""
        mycursor = self.database.cursor()

        data = (substitute_object.user, substitute_object.product)
        mycursor.execute(SQL_INSERT_SUBSTITUTE, data)
        self.database.commit()
        print("L'enregistrement a été effectué avec succès\n")

class Substitute:
    """TODO ecrire"""

    def __init__(self, user_id, product_id):
        self.id = id
        self.user = user_id
        self.product = product_id

    def __str__(self):
        """TODO ecrire"""
        return f"{self.id}, {self.user}"