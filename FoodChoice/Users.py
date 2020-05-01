from data import *
import bcrypt
import pickle


class UsersManager:
    """Manage Users class and Users table"""

    def __init__(self, database):
        self.database = database

    def create(self, name, pwd_serialized):
        """insert user_object in DB"""
        mycursor = self.database.cursor()
        data = (name, pwd_serialized)
        mycursor.execute(SQL_INSERT_USER, data)
        self.database.commit()

        user_object = Users(name)
        mycursor.execute(LAST_INSERT_ID)
        user_object.id = mycursor.fetchone()[0]
        return user_object

    def find_name(self, user_name):
        """find user_name in DB, return True and user_object if it already exists or False if it not exists"""
        mycursor = self.database.cursor()
        mycursor.execute(SQL_SELECT_USER_NAME, (user_name,))
        res = mycursor.fetchone()

        if res is None:
            return False, None

        else:
            user_object = Users(user_name)
            user_object.id = int(res[0])
            return True, user_object

    def ckeck_pwd(self,user_name, pwd):
        """check if the password is right"""
        mycursor = self.database.cursor()
        mycursor.execute(SQL_SELECT_USER_NAME, (user_name,))
        query_res = mycursor.fetchone()
        received_pwd_hashed = pickle.loads((query_res[2]))
        res = bcrypt.checkpw(bytes(pwd, 'utf-8'), received_pwd_hashed)

        if res:
            user_object = Users(user_name)
            user_object.id = int(query_res[0])
            return True, user_object
        else:
            return False, None

    #def substitute(self, product_object):
        # TODO
        # find the substitute
        # return it

    #def record_substitute(self, substitute_object):
    # TODO
    # record it in DB

class Users:
    """Represent Users table"""

    def __init__(self, user_name, pwd=""):
        self.id = ""
        self.name = user_name
        self.pwd = pwd
        self.substitutes = None

    def __repr__(self):
        return f"{self.id}, {self.name}"