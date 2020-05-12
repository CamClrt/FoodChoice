from FoodChoice.Menu import *
from FoodChoice.Database import *


class App:
    """Launch app and display menus"""

    def start(self):
        """Launch the DB connection and/or initialization + invite user to log in, sign in or quit"""
        with Database() as db:
            print(" Bienvenue dans l'application FoodChoice ".center(102, "*"), "\n")
            cnx = True
            while cnx:
                print(" Connection ".center(102, '#'))
                menu = Menu(db)
                menu.cnx_menu()
                menu.main_menu()