from data import *
import bcrypt


class UsersManager:
    """Manage Users class and Users table"""

    def __init__(self, database):
        self.database = database

    def create(self, name, pwd):
        """insert user_object in DB"""
        user_object = Users(name, pwd)
        mycursor = self.database.cursor()
        SQL_INSERT_USER = "INSERT IGNORE INTO Users (Name, Password) VALUES %s;"
        data = "('" + user_object.name + "', '" + user_object.pwd + "')"
        mycursor.execute(SQL_INSERT_USER.replace("%s", data))
        self.database.commit()

        mycursor.execute(LAST_INSERT_ID)
        user_object.id = mycursor.fetchone()[0]

        return user_object

    def find_name(self, user_name, pwd):
        """find user_name in DB, return True and user_object if it already exists or False if it not exists"""
        mycursor = self.database.cursor()
        mycursor.execute(SQL_SELECT_USER_NAME.replace("%s", user_name))
        res = mycursor.fetchone()

        if res is None:
            return False, None

        else:
            user_object = Users(user_name, pwd)
            user_object.id = int(res[0])
            return True, user_object

    def ckeck_pwd(self,user_name, pwd):
        """check if the password is right"""
        mycursor = self.database.cursor()
        mycursor.execute(SQL_SELECT_USER_NAME_AND_PWD.replace("%s/name", user_name).replace("%s/pwd", pwd))
        res = mycursor.fetchone()

        if res is None:
            return False, None

        else:
            user_object = Users(user_name, pwd)
            user_object.id = int(res[0])
            return True, user_object

    def connect(self, name, pwd):
        # TODO vérifie l'info & connecte l'utilisateur ou non

        pass

    #def substitute(self, product_object):
        # TODO
        # find the substitute
        # return it

    #def record_substitute(self, substitute_object):
    # TODO
    # record it in DB

class Users:
    """Represent Users table"""

    def __init__(self, user_name, pwd):
        self.id = ""
        self.name = user_name
        self.pwd = pwd
        self.substitutes = None

    def __repr__(self):
        return f"{self.id}, {self.name}"

