########################### DATABASE CONFIG ###############################

#categories
CATEGORIES_URL = "https://fr.openfoodfacts.org/categories.json"
CATEGORIES_KEY = "tags"
CATEGORIES_NAME_FIELD = "name"
NB_CAT_SELECTED_AMONG_THE_LIST = 20
CATEGORIES_REG_EXP = "^[A-Z].+"

#products
PRODUCTS_URL = "https://fr.openfoodfacts.org/cgi/search.pl?"
PRODUCT_KEY = "products"
PRODUCTS_NAME_FIELD = "nutrition_grades"

PAYLOAD = {
    "action": "process",
    "tagtype_0": "categories",
    "tag_contains_0": "contains",
    "tag_0": "category",
    "sort_by": "last_modified_t",
    "page_size": "250",
    "json": "true"
}

#random seed
SEED = 100

########################### DATABASE CONFIG ###############################

#database
DATABASE_NAME = "FoodChoice"
HOST_NAME = "localhost"
USER_NAME_ROOT = "root"
USER_PASSWORD_ROOT = "my-secret-pw"

############################# SQL QUERIES #################################

SQL_DB_DIRECTORY = 'select @@datadir;'

SQL_SHOW_DB = "SHOW DATABASES;"

SQL_CREATE_DB = "CREATE DATABASE DB DEFAULT CHARACTER SET 'utf8';"

SQL_USE_DB = "USE DB;"

SQL_SHOW_TABLES = "SHOW TABLES;"

SQL_SELECT_ALL = "SELECT * FROM %s;"


SQL_CREATE_CATEGORY_TABLE = "CREATE TABLE IF NOT EXISTS `Category` (" \
                            "`ID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT," \
                            "`Name` VARCHAR(50)," \
                            "PRIMARY KEY (`ID`)" \
                            ")" \
                            "ENGINE=INNODB;"

SQL_CREATE_PRODUCT_TABLE = "CREATE TABLE IF NOT EXISTS `Product` (" \
                           "`ID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT," \
                           "`Name` VARCHAR(150)," \
                           "`Code` BIGINT UNSIGNED," \
                           "`Brand` VARCHAR(100)," \
                           "`Nutrition_grade` CHAR(1)," \
                           "`Energy_100g` SMALLINT UNSIGNED," \
                           "`URL` VARCHAR(255)," \
                           "PRIMARY KEY (`ID`)" \
                           ")" \
                           "ENGINE=INNODB;"

SQL_CREATE_STORE_TABLE = "CREATE TABLE IF NOT EXISTS `Store` (" \
                         "`ID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT," \
                         "`Name` VARCHAR(50)," \
                         "PRIMARY KEY (`ID`)" \
                         ")" \
                         "ENGINE=INNODB;"

SQL_CREATE_CITY_TABLE = "CREATE TABLE IF NOT EXISTS `City` (" \
                        "`ID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT," \
                        "`Name` VARCHAR(50)," \
                        "`Zip_code` SMALLINT UNSIGNED," \
                        "PRIMARY KEY (`ID`)" \
                        ")" \
                        "ENGINE=INNODB;"

SQL_CREATE_SUBSTITUTE_TABLE = "CREATE TABLE IF NOT EXISTS `Substitute` (" \
                              "`Substitute_ID` BIGINT UNSIGNED  NOT NULL AUTO_INCREMENT," \
                              "`Users_ID` TINYINT UNSIGNED," \
                              "`Product_ID` BIGINT UNSIGNED," \
                              "`Date` DATETIME," \
                              "`Note` TEXT," \
                              "KEY `PK, FK` (`Substitute_ID`)," \
                              "KEY `FK` (`Users_ID`, `Product_ID`)" \
                              ")" \
                              "ENGINE=INNODB;"

SQL_CREATE_CATEGORY_PRODUCT_TABLE = "CREATE TABLE IF NOT EXISTS `CategoryProduct` (" \
                                    "`Product_ID` BIGINT UNSIGNED NOT NULL," \
                                    "`Category_ID` BIGINT UNSIGNED NOT NULL," \
                                    "KEY `PK, FK` (`Product_ID`, `Category_ID`)" \
                                    ")" \
                                    "ENGINE=INNODB;"

SQL_CREATE_PRODUCT_LOCATION_TABLE = "CREATE TABLE IF NOT EXISTS `ProductLocation` (" \
                                    "`Product_ID` BIGINT UNSIGNED NOT NULL," \
                                    "`City_ID` BIGINT UNSIGNED NOT NULL," \
                                    "`Store_ID` BIGINT UNSIGNED NOT NULL," \
                                    "KEY `PK, FK` (`Product_ID`, `City_ID`, `Store_ID`)" \
                                    ")" \
                                    "ENGINE=INNODB;"

SQL_CREATE_USERS_TABLE = "CREATE TABLE IF NOT EXISTS `Users` (" \
                         "`ID` TINYINT UNSIGNED NOT NULL AUTO_INCREMENT," \
                         "`Name` VARCHAR(15)," \
                         "`Password` VARCHAR(15)," \
                         "PRIMARY KEY (`ID`)" \
                         ")" \
                         "ENGINE=INNODB;"

#put name tables as key and sql queries as value in a dictionnary to ease creation
TABLES = {
    'Substitute': SQL_CREATE_SUBSTITUTE_TABLE,
    'Category': SQL_CREATE_CATEGORY_TABLE,
    'CategoryProduct': SQL_CREATE_CATEGORY_PRODUCT_TABLE,
    'Product': SQL_CREATE_PRODUCT_TABLE,
    'ProductLocation': SQL_CREATE_PRODUCT_LOCATION_TABLE,
    'Store': SQL_CREATE_STORE_TABLE,
    'City': SQL_CREATE_CITY_TABLE,
    'Users': SQL_CREATE_USERS_TABLE,
}

SQL_INSERT_PRODUCTS = "INSERT INTO Product " \
                              "(Name, Brand, Nutrition_grade, Energy_100g, URL, Code)" \
                              "VALUES %s;"

SQL_INSERT_STORES = "INSERT INTO Store (Name) VALUES ('%s');"

SQL_INSERT_CITIES = "INSERT INTO City (Name) VALUES ('%s');"

SQL_INSERT_PRODUCT_LOCATION = "INSERT INTO ProductLocation (Product_ID, Store_ID, City_ID) VALUES %s;"

SQL_INSERT_CATEGORIES = "INSERT INTO Category (Name) VALUES ('%s');"

SQL_INSERT_CATEGORY_PRODUCT = "INSERT INTO CategoryProduct (Product_ID, Category_ID) VALUES %s;"

SQL_INSERT_USERS = "INSERT INTO Users (Name, Password) VALUES ('%s', '%s');"

SQL_INSERT_SUBSTITUTES = "INSERT INTO Substitute (Users_ID, Product_ID, Date, Note) VALUES ('%s', '%s', '%s', '%s');"

LAST_INSERT_ID = "SELECT LAST_INSERT_ID();"