"""
    This module manage all operations with the Substitute table
"""

from utils import queries
from models.product import ProductManager


class SubstituteManager:
    """Manage Substitute table"""

    def __init__(self, database):
        self.database = database

    def substitute_and_display(self, sql, user_object):
        """Substitute the product by an other healthier"""
        mycursor = self.database.cursor()
        mycursor.execute(queries.SQL_SELECT_SUBSTITUTE.replace("%s", sql))
        product_id = mycursor.fetchall()[0][0]
        mycursor.close()
        product_mng = ProductManager(self.database)
        product_mng.display_product(product_id)
        substitute_object = Substitute(user_object.id, product_id)
        return substitute_object

    def insert(self, substitute_object):
        """insert substitute object in DB"""
        mycursor = self.database.cursor()
        data = (
            substitute_object.user,
            substitute_object.product,
            substitute_object.note,
        )
        mycursor.execute(queries.SQL_INSERT_SUBSTITUTE, data)
        self.database.commit()
        print("L'enregistrement a été effectué avec succès\n")

    def display_list(self, user_object):
        """display a list of substitute by user"""
        mycursor = self.database.cursor()
        mycursor.execute(
            queries.SQL_SELECT_SUBSTITUTES_BY_USER, (user_object.id,))
        substitutes = mycursor.fetchall()
        substitutes_dic = {}
        for tmp_index, substitute in enumerate(substitutes):
            index = tmp_index + 1
            substitutes_dic[str(index)] = substitute
            print(
                f"{substitute[5]}  {index}. {substitute[1]} "
                f"- {substitute[2]} (votre note: {substitute[6]})"
            )
        return substitutes_dic

    def add_note(self, product_id, note):
        """insert substitute note in DB"""
        mycursor = self.database.cursor()
        data = (note[:140], product_id)
        mycursor.execute(queries.SQL_UPDATE_SUBSTITUTE_NOTE, data)
        self.database.commit()
        print("L'enregistrement de votre note a été effectué avec succès\n")

    def delete(self, substitute_id):
        """delete substitute in DB"""
        mycursor = self.database.cursor()
        mycursor.execute(queries.SQL_DELETE_SUBSTITUTE, (substitute_id,))
        self.database.commit()
        print("Ce substitut a été supprimé avec succès\n")


class Substitute:
    """Represent Substitute table"""

    def __init__(self, user_id, product_id):
        self.id = id
        self.user = user_id
        self.product = product_id
        self.date = ""
        self.note = "aucune"

    def __str__(self):
        """Represent Substitute object"""
        return f"{self.id}, {self.user}, {self.product}"
