from data import *

class CityManager:

    def __init__(self, database):
        self.database = database

    def insert(self, city_object):
        name = city_object.name
        mycursor = self.database.cursor()
        mycursor.execute(SQL_INSERT_CITIES.replace("%s", name))
        self.database.commit()
        mycursor.execute(LAST_INSERT_ID)
        id = mycursor.fetchone()
        return id, city_object.name


class City:

    def __init__(self, name, zipcode=00000):
        self.name = name
        self.zipcode = zipcode

    def __str__(self):
        return f"{self.name}"