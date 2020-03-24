import json
import requests
from data import *

class ProductManager:
    """Import datas from the OpenFoodFact API and process them"""
    def __init__(self, category):
        self.response = "" #the response at the http get request
        self.request = REQUEST_URL + ACTION + TAGTYPE_0 + TAG_CONTAINS_0 + TAG_0 + category + JSON_FORMAT #the concatenation of the request
        self.content = "" #the content in json format at the http get request
        self.imported_products = "" #an extract of the whole products


    def import_data(self):
        """import products according to the category selected"""
        self.response = requests.get(self.request)
        if self.response.status_code != 200:
            print("error : trying to consume the API in order to obtain products")
        else:
            self.content = self.response.json()
            self.imported_products = self.content.get(PRODUCT_KEY)
        return self.imported_products #A SUPPRIMER

products = ProductManager("mortadelle-italienne")
print(products.import_data())