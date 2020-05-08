from data import *


class ProductManager:
    """TODO ecrire"""

    last_id = 0  # Store the last attributed id by MySQL

    def __init__(self, database):
        self.database = database

    def insert(self, product_object):
        """TODO ecrire"""
        mycursor = self.database.cursor()

        data = (product_object.name,
                product_object.brand,
                product_object.nutrition_grade,
                product_object.energy_100g,
                product_object.url,
                product_object.code,
                )

        mycursor = self.database.cursor()
        mycursor.execute(SQL_INSERT_PRODUCTS, data)
        self.database.commit()

        mycursor.execute(LAST_INSERT_ID)
        id = mycursor.fetchone()[0]
        if id != ProductManager.last_id:
            product_object.id = id
        else :
            product_object = None

        ProductManager.last_id = id
        mycursor.close()
        return product_object

    def display_by_category(self, category):
        """Display products by category"""
        mycursor = self.database.cursor()
        mycursor.execute(SQL_SELECT_PRODUCT_BY_CATEGORY, (category,))
        products_by_category = mycursor.fetchall()
        print(f"Catégorie selectionnée: {category.upper()}\n")

        print(" N° ".center(6, "#"), "  Nom ".center(75, "#"), " Marque ".center(50, "#"))

        products = {}

        for tmp_index, product_by_category in enumerate(products_by_category):
            index = tmp_index +1
            products[index] = product_by_category
            print(f'{str(index).center(6)}|'
                  f'{str(product_by_category[1])[:75].center(75)}|'
                  f'{str(product_by_category[2])[:50].center(50)}')

        return products

    def display_product(self, product_id):
        """Display products"""
        mycursor = self.database.cursor(buffered=True)
        mycursor.execute(SQL_SELECT_PRODUCT, (product_id,))
        product = mycursor.fetchone()

        mycursor.execute(SQL_SELECT_CATEGORY_PRODUCT, (product_id,))
        categories_res = mycursor.fetchall()
        categories = []
        for category_res in categories_res:
            categories.append(category_res[3])

        mycursor.execute(SQL_SELECT_CITY_PRODUCT, (product_id,))
        cities_res = mycursor.fetchall()
        cities = []
        for city_res in cities_res:
            cities.append(city_res[3])

        mycursor.execute(SQL_SELECT_STORE_PRODUCT, (product_id,))
        stores_res = mycursor.fetchall()
        stores = []
        for store_res in stores_res:
            stores.append(store_res[3])

        print(" Nom: ", product[1], "\n",
              "Marque: ", product[2], "\n",
              "Nutri-Score: ", product[3], "\n",
              "Repères nutritionnels pour 100g: ", product[4], "Kcal", "\n",
              "EAN-13: ", product[5], "\n",
              "URL: ", product[8], "\n",
              "\n", "Catégories: ", ", ".join(categories), "\n",
              "\n", "Points de vente: ", ", ".join(stores), "\n",
              "\n", "Villes: ", ", ".join(cities), "\n")


class Product:
    """TODO ecrire"""

    def __init__(self, name, brand, nutrition_grade, energy_100g, url, code, stores, cities, categories):
        self.id = ""
        self.name = name
        self.brand = brand
        self.nutrition_grade = nutrition_grade
        self.energy_100g = energy_100g
        self.url = url
        self.code = code
        self.stores = stores
        self.cities = cities
        self.categories = categories
        self.sustitute = None

    def __str__(self):
        """TODO ecrire"""
        return f"{self.id}, {self.name}, {self.code}, {self.brand}, {self.nutrition_grade}, {self.energy_100g}cal, {self.url}"