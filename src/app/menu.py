"""
    This module manage the menus
"""

import getpass
import sys
import pickle
import bcrypt

from colorama import Fore, Style

from models.product import ProductManager
from models.users import UsersManager
from models.substitute import SubstituteManager


class Menu:
    """Respresents all the app menus"""

    def __init__(self, database):
        self.database = database
        self.user_object = None

    def cnx_menu(self):  # pylint: disable=too-many-branches
        """Allow user to create an account and connect him"""
        cnx = True
        users_mng = UsersManager(self.database)

        while cnx:
            authentification_request = (
                "\n1. Accès rapide"
                "\n2. Se connecter"
                "\n3. Créer un compte"
                "\n4. Quitter"
                "\n\nVotre réponse: "
            )
            start_choice = input(authentification_request)

            if start_choice in ["1", "2", "3", "4"]:
                if start_choice == "4":  # Exit
                    sys.exit(0)

                elif start_choice == "2":  # Login in
                    print("\nVeuillez vous connecter...")
                    name = input("Nom d'utilisateur: ")
                    name_res, user_object = users_mng.find_name(
                        name
                    )  # test name
                    if name_res:
                        pwd = getpass.getpass("Mot de passe (champ caché): ")
                        pwd_res, user_object = users_mng.ckeck_pwd(
                            name, pwd
                        )  # test pwd
                        if pwd_res:
                            print("\nConnexion réussie\n")
                            cnx = False
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
                        pwd = getpass.getpass("Mot de passe (champ caché): ")
                        # convert pwd in bytes
                        pwd_hashed = bcrypt.hashpw(
                            bytes(pwd, "utf-8"), bcrypt.gensalt()
                        )
                        # serialize the serial_pwd_hashed object
                        serial_pwd_hashed = pickle.dumps(pwd_hashed)
                        user_object = users_mng.create(name, serial_pwd_hashed)
                        print(
                            f"L'utilisateur '{name}' a été créé avec succès\n"
                        )
                        cnx = False

                else:  # Connexion without personal access
                    res, user_object = users_mng.find_name(
                        users_mng.default_username
                    )
                    if res:
                        cnx = False

            else:
                print(
                    Fore.RED
                    + f"'{start_choice}': "
                      f"ce choix ne figure pas dans la liste\n"
                )
                print(Style.RESET_ALL)

        self.user_object = user_object

    def main_menu(self):
        """Display the main menu and interact with user"""
        cnx = True
        while cnx:
            print("\n", " Menu principal ".center(100, "*"))

            menu_request = (
                "\n1. Quel aliment souhaitez-vous remplacer?"
                "\n2. Retrouver mes aliments substitués"
                "\n3. Quitter l'application"
                "\n\nVotre réponse: "
            )
            menu_choice = input(menu_request)

            if menu_choice in ["1", "2", "3"]:
                if menu_choice == "1":  # Replace food
                    self.product_menu()

                elif menu_choice == "2":  # Display substitute
                    self.substitute_menu()

                else:
                    sys.exit(0)  # Exit

            else:
                print(
                    Fore.RED
                    + f"'{menu_choice}': "
                      f"ce choix ne figure pas dans la liste\n"
                )
                print(Style.RESET_ALL)

    def product_menu(self):
        """Display product menu"""
        product_mng = ProductManager(self.database)

        cnx = True
        while cnx:
            print("\n", " Recherche de produit ".center(100, "*"))
            menu_request = (
                "\nSélectionnez par..."
                "\n1. son nom"
                "\n2. sa catégorie"
                "\n\nVotre réponse: "
            )
            menu_choice = input(menu_request)

            if menu_choice in ["1", "2"]:
                if menu_choice == "1":  # Find by name
                    product_name = input("\nLe nom de votre produit: ")
                    products, sql = product_mng.find_and_display_by_name(
                        product_name
                    )
                else:
                    products, sql = product_mng.find_and_display_by_category()

                if len(products) != 0:

                    if len(products) != 1:
                        sub_cnx = True
                        while sub_cnx:
                            product_choice = input(
                                "\nSélectionnez l'aliment n°: "
                            )
                            if product_choice in products.keys():
                                product = products.get(product_choice)
                                sub_cnx = False
                            else:
                                print(
                                    Fore.RED + f"'{product_choice}':"
                                    f" ce choix ne figure pas dans la liste"
                                )
                                print(Style.RESET_ALL)

                        product_id = product[0]
                        product_mng.display_product(product_id)

                        sustitute_choice = input(
                            "\nTrouver une meilleure "
                            "alternative à ce produit? y/n: "
                        )
                        if str(sustitute_choice).lower() == "y":
                            print(
                                "\n",
                                " Votre produit de substitution ".center(
                                    100, "*"
                                ),
                                "\n",
                            )
                            sub_mng = SubstituteManager(self.database)
                            substitute_object = sub_mng.substitute_and_display(
                                sql, self.user_object
                            )
                            sustitute_record = input(
                                "\nEnregistrer ce substitut? y/n: "
                            )
                            if str(sustitute_record).lower() == "y":
                                sub_mng.insert(substitute_object)
                                cnx = False
                else:
                    product = products.get("1")
                    product_id = product[0]
                    product_mng.display_product(product_id)

            else:
                print(
                    Fore.RED
                    + f"'{menu_choice}': ce choix ne figure pas dans la liste"
                )
                print(Style.RESET_ALL)

    def substitute_menu(self):
        """Display substitute menu"""
        cnx = True
        while cnx:
            print("\n", " Substituts ".center(100, "*"), "\n")
            sub_mng = SubstituteManager(self.database)
            substitutes = sub_mng.display_list(self.user_object)
            if len(substitutes) != 0:
                subsitute_request = (
                    "\nQuelle action souhaitez-vous faire?"
                    "\n1. Consulter la fiche détaillée d'un substitut"
                    "\n2. Ajouter ou modifier la note d'un substitut"
                    "\n3. Supprimer un substitut"
                    "\n4. Rejoindre le menu principal"
                    "\n\nVotre réponse: "
                )
                subsitute_choice = input(subsitute_request)

                if subsitute_choice == "4":
                    cnx = False
                else:

                    if subsitute_choice in ["1", "2", "3"]:
                        subsitute_index_choice = input(
                            "\nSélectionnez l'aliment n°: "
                        )

                        if subsitute_index_choice in substitutes.keys():
                            subsitute = substitutes.get(subsitute_index_choice)
                            product_id = subsitute[0]
                            subsitute_id = subsitute[7]

                            # Display substitute details
                            if subsitute_choice == "1":
                                prod_mng = ProductManager(self.database)
                                prod_mng.display_product(product_id)

                            # Add personal note
                            elif subsitute_choice == "2":
                                subsitute_note = input(
                                    "Votre note en moins de 140 caractères: "
                                )
                                sub_mng = SubstituteManager(self.database)
                                sub_mng.add_note(product_id, subsitute_note)

                            # Drop a substitute
                            else:
                                sub_mng = SubstituteManager(self.database)
                                sub_mng.delete(subsitute_id)

                        else:
                            print(
                                Fore.RED + f"'{subsitute_index_choice}':"
                                f" ce choix ne figure pas dans la liste\n"
                            )
                            print(Style.RESET_ALL)
            else:
                cnx = False
