from data import *
import getpass
from FoodChoice.Database import Database
from FoodChoice.Users import *
import sys


class App:

    def __init__(self):
        pass

    def start(self):

        with Database() as db:
            mycursor = db.cursor()
            sql = (SQL_SHOW_DB)
            mycursor.execute(sql)
            myresult = mycursor.fetchall()

            print("\n", " FoodChoice database ".center(100, '*'), "\n")

            user_cnx = False

            while user_cnx == False:

                authentification_request = "\nWhat do you want ? \n1. Login in \n2. Sign up \n3. Exit \n"
                start_choice = int(input(authentification_request))

                if type(start_choice) is int and start_choice <= 3:

                    if int(start_choice) == 3:  # Exit ?
                        conf = input("Do you really want to quit the program ? Y/N\n")
                        if conf.lower() == "y":
                            print("\n>>> Thank you and see you soon !<<<")
                            sys.exit(0)
                        else:
                            user_cnx == False

                    elif int(start_choice) == 1:  # Login in
                        print("Please login in...\n")
                        name = input("Your username : ")
                        pwd = getpass.getpass("Your password (hidden fied) : ")
                        users_mng = UsersManager(db)
                        name_res, user_object = users_mng.find_name(name, pwd)

                        if name_res:
                            pwd_res, user_object = users_mng.ckeck_pwd(name, pwd)
                            if pwd_res:
                                print("\nLogin in successfully ICI")
                                user_cnx = True
                            else:
                                print("\nWARNING : Wrong password !!!")
                                pwd = getpass.getpass("\nPlease, try again ! Your password (hidden fied) : ")
                                pwd_res, user_object = users_mng.ckeck_pwd(name, pwd)
                                if pwd_res:
                                    print("\nLogin in successfully")
                                    user_cnx = True
                                else:
                                    print("\nWARNING : Wrong password !!!")
                                    user_cnx == False
                        else:
                            print("\nWARNING : User unknown !")
                            user_cnx == False

                    else:  # Sign up
                        print("Please sign up...\n")
                        name = input("Your username : ")
                        pwd = getpass.getpass("Your password (hidden fied) : ")
                        users_mng = UsersManager(db)
                        res, user_object = users_mng.find_name(name, pwd)

                        if res:
                            print(f"WARNING : '{name}' as username is already use by someone else !")
                            user_cnx == False
                        else:
                            users_mng.create(name, pwd)
                            print("User created successfully")
                            user_cnx = True

                else:
                    user_cnx == False

            print("Yolo sortie du While")
            return user_object