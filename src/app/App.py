from src.app.Menu import *
from src.models.Database import *


class App:
    """Launch app and display menus"""
    def __init__(self):
        pass

    def start(self):
        """Launch the DB connection + invite user to log in, sign in or quit"""
        with Database() as db:
            print(" Bienvenue dans l'application FoodChoice ".center(102, "*"), "\n")
            cnx = True
            while cnx:
                print(" Connection ".center(102, '#'))
                menu = Menu(db)
                menu.cnx_menu()
                menu.main_menu()
