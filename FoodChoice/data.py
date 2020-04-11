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

PARARMETERS_PRODUCT = {
    "product_name_fr": "product_name_fr",
    "brands": "brands",
    "nutrition_grades": "nutrition_grades",
    "ingredients_text": "ingredients_text",
    "nutriments": "energy_100g",
    "url": "url",
    "code": "code",
    "stores": "stores"
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
                            "`ID` SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT," \
                            "`Name` VARCHAR(100)," \
                            "PRIMARY KEY (`ID`)" \
                            ")" \
                            "ENGINE=INNODB"

SQL_CREATE_PRODUCT_TABLE = "CREATE TABLE `Product` (" \
                            "`ID` INT UNSIGNED NOT NULL AUTO_INCREMENT," \
                            "`Category_ID` INT UNSIGNED," \
                            "`product_name_fr` VARCHAR(150)," \
                            "`code` BIGINT UNSIGNED," \
                            "`brands` VARCHAR(100)," \
                            "`nutrition_grades` CHAR(1)," \
                            "`ingredients_text` TEXT," \
                            "`energy_100g` SMALLINT UNSIGNED," \
                            "`url` VARCHAR(255)," \
                            "`stores` VARCHAR(100)," \
                            "PRIMARY KEY (`ID`)," \
                            "KEY FK (`Category_ID`)" \
                            ")" \
                            "ENGINE=INNODB"

SQL_CREATE_SUBSTITUTE_TABLE = "CREATE TABLE `Substitute` (" \
                              "`ID` INT UNSIGNED NOT NULL AUTO_INCREMENT," \
                              "`Product_ID` INT UNSIGNED," \
                              "`Date` DATETIME," \
                              "PRIMARY KEY (`ID`)," \
                              "KEY FK (`Product_ID`)" \
                              ")" \
                              "ENGINE=INNODB"

CREATE_TABLES = [
    SQL_CREATE_PRODUCT_TABLE,
    SQL_CREATE_SUBSTITUTE_TABLE,
    SQL_CREATE_CATEGORY_TABLE,
]

TABLES = [
    'Category',
    'Product',
    'Substitute',
]

SQL_CREATE_CATEGORY = "INSERT INTO Category (Name) VALUES ('category')"

SQL_CREATE_PRODUCT = "INSERT INTO Product \
            (Category_ID, product_name_fr, brands, nutrition_grades, ingredients_text, energy_100g, url, code, stores)\
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
