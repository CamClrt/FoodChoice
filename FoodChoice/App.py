from data import *
import getpass
import bcrypt
import pickle
from colorama import Fore, Style
import time

from FoodChoice.Database import Database
from FoodChoice.Product import *
from FoodChoice.Substitute import *
from FoodChoice.Filter import *
from FoodChoice.Users import *
import sys


class App:
    """Launch app and display menus"""

    def __init__(self):
        pass

    def start(self):
        """Launch the DB connection and/or initialization + invite user to log in, sign in or quit"""
        with Database() as db:
            print("\n", " Connection ".center(100, '#'))
            user_cnx = False
            users_mng = UsersManager(db)

            while user_cnx == False:
                authentification_request = "\n1. Se connecter" \
                                           "\n2. Créer un compte" \
                                           "\n3. Accès sans compte" \
                                           "\n4. Quitter" \
                                           "\nVotre réponse: "

                start_choice = input(authentification_request)

                if start_choice in ["1", "2", "3", "4"]:
                    if start_choice == "4":  # Exit ?
                        conf = input("\nSouhaitez-vous réellement quitter le programme? Y/N: ")
                        if conf.lower() == "y":
                            print("\n>>> Merci et à bientôt! <<<")
                            sys.exit(0)

                    elif start_choice == "1":  # Login in
                        print("\nVeuillez vous connecter...")
                        name = input("Nom d'utilisateur: ")
                        name_res, user_object = users_mng.find_name(name)  # test name
                        if name_res:
                            pwd = getpass.getpass("Mot de passe (ce champ est caché): ")
                            pwd_res, user_object = users_mng.ckeck_pwd(name, pwd)  # test pwd
                            if pwd_res:
                                print("\nConnection réussie")
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

                    else:                       # Connexion without personal access
                        res, user_object = users_mng.find_name(users_mng.default_username)
                        if res:
                            user_cnx = True

                else:
                    print(Fore.RED + f"ATTENTION: '{start_choice}' ne figure pas dans les choix possibles")
                    print(Style.RESET_ALL)

        return user_object

    def main_menu(self, user_object):
        """Display the main menu and interact with user"""
        print("\n", " FoodChoice database ".center(100, '*').upper())
        menu_cnx = False
        while menu_cnx == False:
            print("\n", " Menu principal ".center(100, '*'))
            menu_request = "\n1. Trouver un produit" \
                           "\n2. Trouver un substitut déjà enregistré" \
                           "\n3. Quitter" \
                           "\nVotre réponse: "
            menu_choice = input(menu_request)

            if int(menu_choice) in [1, 2, 3]:
                if int(menu_choice) == 3:  # Exit ?
                    conf = input("\nSouhaitez-vous réellement quitter le programme? Y/N: ")
                    if conf.lower() == "y":
                        print("\n>>> Merci et à bientôt! <<<")
                        sys.exit(0)

                elif int(menu_choice) == 1:  # Replace food
                    print("\n", " Categories ".center(100, '*'), "\n")

                    with open('categories.data', 'rb') as file:
                        imported_categories = pickle.load(file)
                        filter = Filter()
                        categories = {}

                        for tmp_index, tmp_category in enumerate(imported_categories):
                            index = tmp_index + 1
                            category = filter.cat_filter(tmp_category)
                            print(index, " : ", category)
                            categories[str(index)] = category

                    with Database() as db:
                        product_mng = ProductManager(db)

                        categories_cnx = False
                        while categories_cnx == False:
                            category_selected = input("\nSélectionnez l'index de votre catégorie... \nVotre réponse: ")
                            if category_selected in categories.keys():
                                print("\n", " Products ".center(100, '*'), "\n")
                                products = product_mng.display_by_category(categories.get(category_selected))
                                categories_cnx = True
                            else:
                                print(f"{category_selected}' ne figure pas dans les choix possibles. Veuillez ré essayer.\n")

                        product_cnx = False
                        while product_cnx == False:
                            product_selected = input("Sélectionnez l'index de votre produit... \nVotre réponse: ")
                            if int(product_selected) in products.keys():
                                print("\n", " Fiche produit ".center(100, '*'), "\n")
                                product = products.get(int(product_selected))
                                product_id = product[0]
                                product_grade = product[3]
                                product_energy = product[4]
                                product_mng.display_product(product_id)
                                print("\n", "".center(100, '*'))
                                product_cnx = True

                            else:
                                print(f"{product_selected}' ne figure pas dans les choix possibles. Veuillez ré essayer.\n")

                        substitute_cnx = False
                        while substitute_cnx == False:
                            substitute_request = "\n1. Trouver un remplaçant plus sain?" \
                                                 "\n2. Retourner au menu principal" \
                                                 "\n3. Quitter \nVotre réponse: "

                            substitute_choice = input(substitute_request)

                            if substitute_choice in ["1", "2", "3"]:
                                if substitute_choice == "3":  # Exit ?
                                    conf = input("\nSouhaitez-vous réellement quitter le programme? Y/N: ")
                                    if conf.lower() == "y":
                                        print("\n>>> Merci et à bientôt! <<<")
                                        sys.exit(0)

                                elif substitute_choice == "1":  # Substitute it
                                    substitute_mng = SubstituteManager(db)
                                    print("\n", " Proposition de substitut ".center(100, '*'), "\n")
                                    substitute = substitute_mng.substitute_and_display(
                                                                categories.get(category_selected),
                                                                product_grade,
                                                                product_energy)
                                    time.sleep(2)
                                    substitute_cnx = True

                                else:
                                    time.sleep(1)
                                    substitute_cnx = True     # Go to the main menu
                                    menu_cnx = False

                            else:
                                print(Fore.RED + f"ATTENTION: '{substitute_choice}' ne figure pas dans les choix possibles")
                                print(Style.RESET_ALL)

                else:
                    print("\n", " Your substitutes ", "".center(100, '*'))