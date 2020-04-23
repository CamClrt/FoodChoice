from data import *

class ProductLocationManager:

    def __init__(self, database):
        self.database = database

    def insert(self, productlocation_objects):
        data = []
        for productlocation_object in productlocation_objects:
            data.append((productlocation_object.Product_ID,
                         productlocation_object.Store_ID,
                         productlocation_object.City_ID,))
            mycursor = self.database.cursor()
            mycursor.executemany(SQL_INSERT_PRODUCT_LOCATION, data)
            self.database.commit()


class ProductLocation:

    def __init__(self, Product_ID, Store_ID, City_ID):
        self.Product_ID = Product_ID
        self.Store_ID = Store_ID
        self.City_ID = City_ID

    def __str__(self):
        return f"Product_ID : {self.Product_ID}, Store_ID : {self.Store_ID}, City_ID : {self.City_ID}"