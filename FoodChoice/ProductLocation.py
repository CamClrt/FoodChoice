from data import *

class ProductLocationManager:

    def __init__(self, database):
        self.database = database

    def insert(self, productlocation_objects):

        data = []

        for productlocation_object in productlocation_objects:

            data.append((productlocation_object.product_id,
                        productlocation_object.store_id,
                        productlocation_object.city_id,))

        mycursor = self.database.cursor()
        mycursor.executemany(SQL_INSERT_PRODUCT_LOCATION, data)
        self.database.commit()
        mycursor.close()


class ProductLocation:

    def __init__(self, product_id, store_id, city_id):
        self.product_id = product_id
        self.store_id = store_id
        self.city_id = city_id

    def __str__(self):
        return f"Product_ID : {self.product_id}, Store_ID : {self.store_id}, City_ID : {self.city_id}"