from data import *
from FoodChoice.Database import Database
from FoodChoice.API import API

class App:

    def __init__(self):
        pass

    def start(self):

        with Database() as db:
            mycursor = db.cursor()
            sql = (SQL_SHOW_DB)
            mycursor.execute(sql)
            myresult = mycursor.fetchall()

            for x in myresult:
                print(x)

app = App()
app.start_app()