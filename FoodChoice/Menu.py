import sys
import time
import bcrypt
import pickle
import getpass
from colorama import Fore, Style

from data import *
from FoodChoice.Users import *
from FoodChoice.Filter import *
from FoodChoice.Product import *
from FoodChoice.Substitute import *
from FoodChoice.Database import Database


class Menu():
    """Respresents all the app menus"""

    def __init__(self, database):
        self.database = database

    def cnx_menu(self):
        """Allow user to create an account and connect him with or without account"""

        user_cnx = False
        users_mng = UsersManager(self.database)

        while user_cnx == False:
            authentification_request = "\n1. Se connecter" \
                                       "\n2. Créer un compte" \
                                       "\n3. Accès sans compte" \
                                       "\n4. Quitter" \
                                       "\n\nVotre réponse: "

            start_choice = input(authentification_request)

            if start_choice in ["1", "2", "3", "4"]:
                if start_choice == "4":  # Exit
                    self.quit()

                elif start_choice == "1":  # Login in
                    print("\nVeuillez vous connecter...")
                    name = input("Nom d'utilisateur: ")
                    name_res, user_object = users_mng.find_name(name)  # test name
                    if name_res:
                        pwd = getpass.getpass("Mot de passe (ce champ est caché): ")
                        pwd_res, user_object = users_mng.ckeck_pwd(name, pwd)  # test pwd
                        if pwd_res:
                            print("\nConnection réussie\n")
                            user_cnx = True
                        else:
                            print(Fore.RED + "ATTENTION: Mot de passe eronné")
                            print(Style.RESET_ALL)
                    else:
                        print(Fore.RED + "ATTENTION: Utilisateur inconnu")
                        print(Style.RESET_ALL)

                elif start_choice == "2":  # Sign up
                    print("\nVeuillez vous inscrire...")
                    name = input("Nom d'utilisateur: ")
                    res, user_object = users_mng.find_name(name)  # test name

                    if res:
                        print(Fore.RED + f"ATTENTION: '{name}' est déjà utilisé")
                        print(Style.RESET_ALL)
                    else:
                        pwd = getpass.getpass('Mot de passe (ce champ est caché): ')
                        pwd_hashed = bcrypt.hashpw(bytes(pwd, 'utf-8'), bcrypt.gensalt())  # convert pwd in bytes
                        serial_pwd_hashed = pickle.dumps(pwd_hashed)  # serialize the serial_pwd_hashed object
                        user_object = users_mng.create(name, serial_pwd_hashed)
                        print(f"L'utilisateur '{name}' a été créé avec succès")
                        user_cnx = True

                else:  # Connexion without personal access
                    res, user_object = users_mng.find_name(users_mng.default_username)
                    if res:
                        user_cnx = True

            else:
                print(Fore.RED + f"ATTENTION: '{start_choice}' ne figure pas dans les choix possibles\n")
                print(Style.RESET_ALL)

        return user_object

    def main_menu(self, user_object):
        """Display the main menu and interact with user"""

        menu_cnx = False
        while menu_cnx == False:

            print(" Menu principal ".center(100, '*'))

            menu_request = "\n1. Trouver un produit" \
                           "\n2. Trouver vos substituts enregistrés" \
                           "\n3. Se déconnecter" \
                           "\n4. Quitter l'application" \
                           "\n\nVotre réponse: "
            menu_choice = input(menu_request)

            if menu_choice in ["1", "2", "3", "4"]:
                if menu_choice == "1":    # Replace food
                    self.find_product_menu()

                elif menu_choice == "2":    # Display substitute
                    pass
                    # TODO : afficher la liste de substitut
                    # TODO : demander à en selection un ou repartir au menu général
                    # TODO : Si selection > affichage de sa fiche

                elif menu_choice == "3":  # Disconnect ?
                    menu_cnx = True

                else:
                    self.quit()           # Exit ?

            else:
                print(Fore.RED + f"ATTENTION: '{start_choice}' ne figure pas dans les choix possibles\n")
                print(Style.RESET_ALL)

    def find_product_menu(self):
        """Display product menu"""
        print(" Recherche de produit ".center(100, '*'))

        menu_request = "\nChercher un produit par..." \
                       "\n1. Son nom" \
                       "\n2. Sa catégorie" \
                       "\n\nVotre réponse: "
        menu_choice = input(menu_request)

        if menu_choice in ["1", "2"]:
            if menu_choice == "1":  # Find by name
                #TODO : méthode de recherche par nom
                print("Menu 1")

            if menu_choice == "2":  # Find by category
                # TODO : méthode d'affichage des catégories
                # TODO : effectuer la sélection de la catégorie
                # TODO : méthode de recherche des produits
                # TODO : effectuer la sélection du produit
                # TODO : substituer ? Y/N
                # TODO : enregistrer le substitut
                print("Menu 2")

        else:
            print(Fore.RED + f"ICI ATTENTION: '{menu_choice}' ne figure pas dans les choix possibles")
            print(Style.RESET_ALL)

    def quit(self):
        """Allow user to quit app"""
        conf = input("Souhaitez-vous réellement quitter le programme? Y/N: ")
        if conf.lower() == "y":
            print("\n>>> Merci et à bientôt! <<<")
            sys.exit(0)