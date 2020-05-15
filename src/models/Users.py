import pickle
import bcrypt
from src.utils.queries import *


class UsersManager:
    """Manage Users table"""
    default_username = "UserByDefault"
    default_pw = "PwdByDefault"

    def __init__(self, database):
        self.database = database

    def create(self, name, pwd_serialized):
        """insert user object in DB"""
        mycursor = self.database.cursor()
        data = (name, pwd_serialized)
        mycursor.execute(SQL_INSERT_USER, data)
        self.database.commit()

        user_object = Users(name)
        mycursor.execute(LAST_INSERT_ID)
        user_object.id = mycursor.fetchone()[0]
        mycursor.close()
        return user_object

    def find_name(self, user_name):
        """find if user_name is already in DB"""
        mycursor = self.database.cursor()
        mycursor.execute(SQL_SELECT_USER_NAME, (user_name, ))
        res = mycursor.fetchone()
        mycursor.close()

        if res is None:
            return False, None
        else:
            user_object = Users(user_name)
            user_object.id = int(res[0])
            return True, user_object

    def ckeck_pwd(self, user_name, pwd):
        """check if the password is right"""
        mycursor = self.database.cursor()
        mycursor.execute(SQL_SELECT_USER_NAME, (user_name, ))
        query_res = mycursor.fetchone()
        mycursor.close()
        received_pwd_hashed = pickle.loads((query_res[2]))
        res = bcrypt.checkpw(bytes(pwd, 'utf-8'), received_pwd_hashed)

        if res:
            user_object = Users(user_name)
            user_object.id = int(query_res[0])
            return True, user_object
        else:
            return False, None


class Users:
    """Represent Users table"""

    def __init__(self, user_name, pwd=""):
        self.id = ""
        self.name = user_name
        self.pwd = pwd
        self.substitutes = None

    def __repr__(self):
        """Represent Users object"""
        return f"{self.id}, {self.name}"
