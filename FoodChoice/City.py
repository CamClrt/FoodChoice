from data import *

class CityManager:

    def __init__(self, database):
        self.database = database

    def insert(self, city_object):
        mycursor = self.database.cursor()
        mycursor.execute(SQL_INSERT_CITIES.replace("%s", city_object.name))
        self.database.commit()
        mycursor.execute(LAST_INSERT_ID)
        city_object.id = mycursor.fetchone()[0]
        return city_object


class City:

    def __init__(self, name, zipcode=00000):
        self.id = ""
        self.name = name
        self.zipcode = zipcode

    def __str__(self):
        return f"{self.id} {self.name} {self.zipcode}"