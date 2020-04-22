from data import *
from FoodChoice.Database import Database

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

            for x in myresult:
                print(x)

            print("\n", " TABLES ".center(100, '*'), "\n")

            sql = (SQL_SHOW_TABLES)
            mycursor.execute(sql)
            myresult = mycursor.fetchall()

            for x in myresult:
                print(x)

            print("\n", " USERS ".center(100, '*'), "\n")
            sql = (SQL_SELECT_ALL.replace("%s", "Users"))
            mycursor.execute(sql)
            myresult = mycursor.fetchall()

            for x in myresult:
                print(x)

            print("\n", " CATEGORY ".center(100, '*'), "\n")
            sql = (SQL_SELECT_ALL.replace("%s", "Category"))
            mycursor.execute(sql)
            myresult = mycursor.fetchall()

            for x in myresult:
                print(x)

            print("\n", " PRODUCT ".center(100, '*'), "\n")
            sql = (SQL_SELECT_ALL.replace("%s", "Product"))
            mycursor.execute(sql)
            myresult = mycursor.fetchall()

            for x in myresult:
                print(x)

            print("\n", " STORE ".center(100, '*'), "\n")
            sql = (SQL_SELECT_ALL.replace("%s", "Store"))
            mycursor.execute(sql)
            myresult = mycursor.fetchall()

            for x in myresult:
                print(x)

            print("\n", " CITY ".center(100, '*'), "\n")
            sql = (SQL_SELECT_ALL.replace("%s", "City"))
            mycursor.execute(sql)
            myresult = mycursor.fetchall()

            for x in myresult:
                print(x)