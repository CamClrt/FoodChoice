from data import *

import os.path

import mysql.connector
from mysql.connector import Error

class Database:
    """"Init or connect database"""

    def __init__(self, database_name=DATABASE_NAME,
                 host_name=HOST_NAME,
                 user_name_root=USER_NAME_ROOT,
                 user_password_root=USER_PASSWORD_ROOT
                 ):

        self.database_name = database_name
        self.host_name = host_name
        self.user_name_root = user_name_root
        self.user_password_root = user_password_root

    def connect(self):
        """Connect to the service"""
        db = None
        try:
            db = mysql.connector.connect(
                user=self.user_name_root,
                password=self.user_password_root,
                host=self.host_name,
            )

            mycursor = db.cursor()
            mycursor.execute('select @@datadir')
            path = mycursor.fetchone()

            if len(path) != 0:
                url_db = path[0] + self.database_name
                if os.path.exists(url_db):
                    mycursor.execute('USE ' + self.database_name)
                else:
                    mycursor.execute(SQL_CREATE_DB)
                    print(">>> Database created successfully")
                    mycursor.execute('USE ' + self.database_name)
                    for name, query in TABLES.items():
                        mycursor.execute(query)
                        print(f"> {name} table created successfully")
            print("Database connected successfully")
        except Error as e:
            print(f"The error '{e}' occurred")
        mycursor.close()

        return db

db = Database()
db.connect()