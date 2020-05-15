import time
from src.utils.queries import *
from src.models.Category import *


class ProductManager:
    """Manage Product table"""
    last_id = 0  # Store the last attributed id by MySQL

    def __init__(self, database):
        self.database = database

    def insert(self, product_object):
        """insert product_object in DB"""
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
        else:
            product_object = None

        ProductManager.last_id = id
        mycursor.close()
        return product_object

    def find_and_display_by_category(self):
        """Display products by category_name"""
        cat_mng = CategoryManager(self.database)
        tmp_most_used_categories = cat_mng.most_used_categories()
        most_used_categories = sorted(tmp_most_used_categories, key=lambda x: x[0])

        categories = {}
        print("\n", " Catégories ".center(50, "*"), "\n")
        for tmp_index, category_by_name in enumerate(most_used_categories):
            index = tmp_index + 1
            categories[str(index)] = category_by_name
            print(f'{str(index)}. {str(category_by_name[0])}')

        cnx = True
        while cnx:
            category_choice = input("\nQuelle categorie souhaitez-vous sélectionner: ")

            if category_choice in categories.keys():
                category = categories.get(category_choice)
                category_id = category[2]
                mycursor = self.database.cursor()
                mycursor.execute(SQL_SELECT_PRODUCTS_BY_CATEGORY, (category_id,))
                sql = mycursor.statement
                products_by_category = mycursor.fetchall()

                products = {}

                print("\n")
                print(" N° ".center(10, "#"), "  Nom ".center(50, "#"),
                      " Marque ".center(50, "#"), " Code ".center(15, "#"))
                for tmp_index, product_by_category in enumerate(products_by_category):
                    index = tmp_index + 1
                    products[str(index)] = product_by_category
                    print(f'{str(index)[:10].center(10)}|'
                          f'{str(product_by_category[1])[:48].center(50)}|'
                          f'{str(product_by_category[2])[:48].center(50)}|'
                          f'{str(product_by_category[3])[:13].center(15)}|')
                cnx = False
            else:
                print(f"\n '{category_choice}': cette catégorie ne figure pas dans la liste\n")
        return products, sql[:-1]

    def find_and_display_by_name(self, tmp_product_name):
        """Find by product name and display a list"""
        mycursor = self.database.cursor()
        product_name = "%" + tmp_product_name + "%"
        mycursor.execute(SQL_SELECT_PRODUCTS_BY_NAME, (product_name, ))
        sql = mycursor.statement
        products_by_name = mycursor.fetchall()

        products = {}

        if len(products_by_name) == 0:
            print("\nAucun produit ne correspond à la recherche!")
        else:
            print("\n")
            print(" N° ".center(10, "#"), "  Nom ".center(50, "#"),
                  " Marque ".center(50, "#"), " Code ".center(15, "#"))
            for tmp_index, product_by_name in enumerate(products_by_name):
                index = tmp_index + 1
                products[str(index)] = product_by_name
                print(f'{str(index)[:10].center(10)}|'
                      f'{str(product_by_name[1])[:48].center(50)}|'
                      f'{str(product_by_name[2])[:48].center(50)}|'
                      f'{str(product_by_name[3])[:13].center(15)}|')
        return products, sql[:-1]

    def display_product(self, product_id):
        """Display product details"""
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

        print("\n", " Fiche produit ".center(100, "*"), "\n")
        print(" Nom: ", product[1], "\n",
              "Marque: ", product[2], "\n",
              "Nutri-Score: ", product[3], "\n",
              "Repères nutritionnels pour 100g: ", product[4], "Kcal", "\n",
              "EAN-13: ", product[5], "\n",
              "URL: ", product[6], "\n\n",
              "Catégories: ", ", ".join(categories), "\n\n",
              "Points de vente: ", ", ".join(stores), "\n\n",
              "Villes: ", ", ".join(cities), "\n")
        time.sleep(1)


class Product:
    """Represent Product table"""

    def __init__(self, name, brand, nutrition_grade, energy_100g,
                 url, code, stores, cities, categories):
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

    def __str__(self):
        """Represent Product object"""
        return f"{self.id}, {self.name}, {self.code}, {self.brand}, " \
               f"{self.nutrition_grade}, {self.energy_100g}cal, {self.url}" \
               f"{self.code}, {self.stores}, {self.cities}, {self.categories}"
