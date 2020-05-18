# pylint:  disable=no-self-use, too-few-public-methods

"""
    This module manage the application start
"""

from app.menu import Menu
from models.database import Database


class App:
    """Launch app and display menus"""

    def start(self):
        """Launch the DB connection + invite user to log in, sign in or quit"""
        with Database() as database:
            print(
                " Bienvenue dans l'application FoodChoice ".center(102, "*"),
                "\n",
            )
            cnx = True
            while cnx:
                print(" Connection ".center(102, "#"))
                menu = Menu(database)
                menu.cnx_menu()
                menu.main_menu()
