#categories
CATEGORIES_URL = "https://fr.openfoodfacts.org/categories.json"
CATEGORIES_KEY = "tags"
CATEGORIES_NAME_FIELD = "name"
NB_CAT_SELECTED_AMONG_THE_LIST = 50
CATEGORIES_REG_EXP = "^[A-Z].+"

#products
PRODUCTS_URL = "https://fr.openfoodfacts.org/cgi/search.pl?"
PRODUCT_KEY = "products"
PRODUCTS_NAME_FIELD = "nutrition_grades"
NB_PROD_SELECTED_AMONG_THE_LIST = 250

PAYLOAD = {
    "action": "process",
    "tagtype_0": "categories",
    "tag_contains_0": "contains",
    "tag_0": "category",
    "sort_by": "last_modified_t",
    "page_size": "500",
    "json": "true"
}

PRODUCT_PARARMETERS = {
    "product_name_fr": ["product_name_fr", 150],
    "brands": ["brands", 100],
    "nutrition_grades": ["nutrition_grades", 1],
    "nutriments": ["energy_100g", int],
    "url": ["url", 255],
    "code": ["code", 19],
}

PRODUCT_STORE_PARARMETERS = {
    "stores_tags": ["stores_tags", 50],
}

PRODUCT_CITY_PARARMETERS = {
    "purchase_places_tags": ["purchase_places_tags", 50],
}

#random seed
SEED = 100

#database
DATABASE_NAME = "FoodChoice"
HOST_NAME = "localhost"
USER_NAME_ROOT = "root"
USER_PASSWORD_ROOT = "my-secret-pw"

#SQL requests
SQL_CREATE_DB = "CREATE DATABASE " + DATABASE_NAME + " DEFAULT CHARACTER SET 'utf8'"

SQL_CREATE_CATEGORY_TABLE = "CREATE TABLE `Category` (" \
                            "`ID` INT UNSIGNED NOT NULL AUTO_INCREMENT," \
                            "`Name` VARCHAR(50)," \
                            "PRIMARY KEY (`ID`)" \
                            ")" \
                            "ENGINE=INNODB"

SQL_CREATE_PRODUCT_TABLE = "CREATE TABLE `Product` (" \
                           "`ID` INT UNSIGNED NOT NULL AUTO_INCREMENT," \
                           "`Name` VARCHAR(150)," \
                           "`Code` BIGINT UNSIGNED," \
                           "`Brand` VARCHAR(100)," \
                           "`Nutrition_grade` CHAR(1)," \
                           "`Energy_100g` SMALLINT UNSIGNED," \
                           "`URL` VARCHAR(255)," \
                           "PRIMARY KEY (`ID`)" \
                           ")" \
                           "ENGINE=INNODB"

SQL_CREATE_STORE_TABLE = "CREATE TABLE `Store` (" \
                         "`ID` INT UNSIGNED NOT NULL AUTO_INCREMENT," \
                         "`Name` VARCHAR(50)," \
                         "PRIMARY KEY (`ID`)" \
                         ")" \
                         "ENGINE=INNODB"

SQL_CREATE_CITY_TABLE = "CREATE TABLE `City` (" \
                        "`ID` INT UNSIGNED," \
                        "`Name` VARCHAR(50)," \
                        "`ZipCode` SMALLINT UNSIGNED," \
                        "PRIMARY KEY (`ID`)" \
                        ")" \
                        "ENGINE=INNODB"

CREATE_TABLES = [
    SQL_CREATE_CATEGORY_TABLE,
    SQL_CREATE_PRODUCT_TABLE,
    SQL_CREATE_STORE_TABLE,
    SQL_CREATE_CITY_TABLE,
]

TABLES = [
    'Category',
    'Product',
    'Store',
    'City',
]

SQL_CREATE_CATEGORIES = "INSERT INTO Category (Name) VALUES ('category')"

SQL_CREATE_PRODUCTS = "INSERT INTO Product \
            (Name, Brand, Nutrition_grade, Energy_100g, URL, Code)\
             VALUES (%s, %s, %s, %s, %s, %s)"

SQL_CREATE_STORES = "INSERT INTO Store (Name) VALUES ('store');" #TODO ici à revoir

SQL_CREATE_CITIES = "INSERT INTO City (Name) VALUES ('city');" #TODO ici à revoir

PRODUCTS_DATA = {
    SQL_CREATE_PRODUCTS: PRODUCT_PARARMETERS,
    SQL_CREATE_STORES: PRODUCT_STORE_PARARMETERS,
    SQL_CREATE_CITIES: PRODUCT_CITY_PARARMETERS,
}