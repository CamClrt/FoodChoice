from data import *
import getpass
import bcrypt
import pickle

from FoodChoice.Database import Database
from FoodChoice.Users import *
import sys


class App:

    def __init__(self):
        pass

    def start(self):
        """Launch the DB connection and/or initialization + invite user log in, sign in or quit"""

        with Database() as db:
            mycursor = db.cursor()
            sql = (SQL_SHOW_DB)
            mycursor.execute(sql)
            myresult = mycursor.fetchall()

            print("\n", " FoodChoice database ".center(100, '*').upper())
            print("\n", " Connexion ".center(100, '#'))
            user_cnx = False

            while user_cnx == False:
                authentification_request = "\nNow, what do you want ? \n1. Log in \n2. Sign up \n3. Exit\nAnswer : "
                start_choice = int(input(authentification_request))
                users_mng = UsersManager(db)

                if type(start_choice) is int and start_choice <= 3:

                    if int(start_choice) == 3:  # Exit ?
                        conf = input("\nDo you really want to quit the program ? Y/N")
                        if conf.lower() == "y":
                            print("\n>>> Thank you and see you soon !<<<")
                            sys.exit(0)
                        else:
                            user_cnx == False

                    elif int(start_choice) == 1:  # Login in
                        print("\nPlease login in...")
                        name = input("\nYour username : ")
                        name_res, user_object = users_mng.find_name(name)  #test name
                        if name_res:
                            pwd = getpass.getpass("Your password (hidden field) : ")
                            pwd_res, user_object = users_mng.ckeck_pwd(name, pwd)  #test pwd
                            if pwd_res:
                                print("\nLogin in successfully")
                                user_cnx = True
                            else:
                                print("\nWARNING : Wrong password !!!")
                        else:
                            print("\nWARNING : User unknown !")

                    else:  # Sign up
                        print("\nPlease sign up...")
                        name = input("\nYour username : ")
                        res, user_object = users_mng.find_name(name)  # test name

                        if res:
                            print(f"\nWARNING : '{name}' is already used by someone else !")
                        else:
                            pwd = getpass.getpass('Your password (hidden field) : ')
                            pwd_hashed = bcrypt.hashpw(bytes(pwd, 'utf-8'), bcrypt.gensalt())  # convert pwd in bytes
                            serial_pwd_hashed = pickle.dumps(pwd_hashed)  # serialize the serial_pwd_hashed object
                            users_mng.create(name, serial_pwd_hashed)
                            print(f"\nUser {name} created successfully")
                            user_cnx = True
                else:
                    user_cnx == False

            return user_object