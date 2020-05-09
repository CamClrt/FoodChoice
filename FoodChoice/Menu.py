import sys
import bcrypt
import pickle
import getpass
from colorama import Fore, Style

from FoodChoice.Users import *
from FoodChoice.Product import *


class Menu():
    """Respresents all the app menus"""

    def __init__(self, database):
        self.database = database

    def cnx_menu(self):
        """Allow user to create an account and connect him with or without account"""

        user_cnx = False
        users_mng = UsersManager(self.database)

        while user_cnx == False:
            authentification_request = "\n1. Accès rapide" \
                                       "\n2. Se connecter" \
                                       "\n3. Créer un compte" \
                                       "\n4. Quitter" \
                                       "\n\nVotre réponse: "

            start_choice = input(authentification_request)

            if start_choice in ["1", "2", "3", "4"]:
                if start_choice == "4":  # Exit
                    self.quit()

                elif start_choice == "2":  # Login in
                    print("\nVeuillez vous connecter...")
                    name = input("Nom d'utilisateur: ")
                    name_res, user_object = users_mng.find_name(name)  # test name
                    if name_res:
                        pwd = getpass.getpass("Mot de passe (champ caché): ")
                        pwd_res, user_object = users_mng.ckeck_pwd(name, pwd)  # test pwd
                        if pwd_res:
                            print("\nConnection réussie\n")
                            user_cnx = True
                        else:
                            print(Fore.RED + "Mot de passe eronné\n")
                            print(Style.RESET_ALL)
                    else:
                        print(Fore.RED + "Utilisateur inconnu\n")
                        print(Style.RESET_ALL)

                elif start_choice == "3":  # Sign up
                    print("\nVeuillez vous inscrire...")
                    name = input("Nom d'utilisateur: ")
                    res, user_object = users_mng.find_name(name)  # test name

                    if res:
                        print(Fore.RED + f"'{name}': est déjà utilisé\n")
                        print(Style.RESET_ALL)
                    else:
                        pwd = getpass.getpass('Mot de passe (champ caché): ')
                        pwd_hashed = bcrypt.hashpw(bytes(pwd, 'utf-8'), bcrypt.gensalt())  # convert pwd in bytes
                        serial_pwd_hashed = pickle.dumps(pwd_hashed)  # serialize the serial_pwd_hashed object
                        user_object = users_mng.create(name, serial_pwd_hashed)
                        print(f"L'utilisateur '{name}' a été créé avec succès\n")
                        user_cnx = True

                else:  # Connexion without personal access
                    res, user_object = users_mng.find_name(users_mng.default_username)
                    if res:
                        user_cnx = True

            else:
                print(Fore.RED + f"'{start_choice}': ce choix ne figure pas dans la liste\n")
                print(Style.RESET_ALL)

        return user_object

    def main_menu(self, user_object):
        """Display the main menu and interact with user"""

        menu_cnx = False
        while menu_cnx == False:

            print("\n", " Menu principal ".center(100, '*'))

            menu_request = "\n1. Trouver un produit" \
                           "\n2. Trouver les substituts enregistrés" \
                           "\n3. Quitter cette session" \
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
                print(Fore.RED + f"'{menu_choice}': ce choix ne figure pas dans la liste\n")
                print(Style.RESET_ALL)

    def find_product_menu(self):
        """Display product menu"""
        print(" Recherche de produit ".center(100, '*'))

        menu_request = "\nChercher un produit par..." \
                       "\n1. Son nom" \
                       "\n2. Sa catégorie" \
                       "\n\nVotre réponse: "
        menu_choice = input(menu_request)

        product_mng = ProductManager(self.database)

        if menu_choice in ["1", "2"]:
            if menu_choice == "1":  # Find by name
                product_name = input("\nLe nom de votre produit: ")
                products = product_mng.find_and_display_by_name(product_name)

            else:
                products = product_mng.find_and_display_by_category()

            if len(products) != 0:
                cnx = True
                while cnx:
                    product_choice = input("\nQuel produit souhaitez-vous sélectionner: ")

                    if product_choice in products.keys():
                        product = products.get(product_choice)
                        product_id = product[0]
                        product_mng.display_product(product_id)
                        cnx = False

                    else:
                        print(f"\n '{product_choice}': ce produit ne figure pas dans la liste\n")

                # TODO : substituer ? Y/N
                # TODO : si oui, enregistrer le substitut

        else:
            print(Fore.RED + f"'{menu_choice}': ce choix ne figure pas dans la liste")
            print(Style.RESET_ALL)

    def quit(self):
        """Allow user to quit app"""
        conf = input("Souhaitez-vous réellement quitter le programme? Y/N: ")
        if conf.lower() == "y":
            print("\n>>> Merci et à bientôt! <<<")
            sys.exit(0)