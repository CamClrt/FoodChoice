from data import *

class CityManager:
    """TODO ecrire"""

    def __init__(self, database):
        self.database = database

    def find(self, city_name):
        """search if city_name already exists in the city table and insert it"""
        mycursor = self.database.cursor()
        mycursor.execute(SQL_SELECT_CITY, (city_name, ))
        res = mycursor.fetchone()
        city = City(city_name)
        mycursor.close()
        if res is None:
            return self.insert(city)
        else:
            city.id = int(res[0])
            return city

    def insert(self, city_object):
        """TODO ecrire"""
        mycursor = self.database.cursor()
        mycursor.execute(SQL_INSERT_CITIES,(city_object.name, ))
        self.database.commit()
        mycursor.execute(LAST_INSERT_ID)
        city_object.id = mycursor.fetchone()[0]
        mycursor.close()
        return city_object


class City:
    """TODO ecrire"""

    def __init__(self, name, zipcode=00000):
        self.id = ""
        self.name = name
        self.zipcode = zipcode

    def __str__(self):
        """TODO ecrire"""
        return f"{self.id} {self.name} {self.zipcode}"