from datetime import datetime

########################### DATABASE CONFIG ###############################

# database
DATABASE_NAME = "FoodChoice"
HOST_NAME = "localhost"
USER_NAME = "FoodChoiceUser"
USER_PASSWORD = "my-secret-pw"

########################### API CONFIG ###############################

# headers
APP_NAME = 'FoodChoice/0.0.1'
date = datetime.now()
DATE = date.__str__()[:19]

# categories
CATEGORIES_URL = "https://fr.openfoodfacts.org/categories.json"
CATEGORIES_KEY = "tags"
CATEGORIES_NAME_FIELD = "name"
NB_CAT_SELECTED_AMONG_THE_LIST = 15
CATEGORIES_REGEX = "^[A-Z].+"

# products
PRODUCTS_URL = "https://fr.openfoodfacts.org/cgi/search.pl?"
PRODUCT_KEY = "products"
PRODUCTS_NAME_FIELD = "nutrition_grades"

PAYLOAD = {
    "action": "process",
    "tagtype_0": "categories",
    "tag_contains_0": "contains",
    "tag_0": "category",
    "sort_by": "last_modified_t",
    "page_size": "100",
    "json": "true"
}

############################# SQL QUERIES #################################

SQL_DB_DIRECTORY = 'select @@datadir;'

SQL_CREATE_DB = "CREATE DATABASE " + DATABASE_NAME + " DEFAULT CHARACTER SET 'utf8';"

SQL_USE_DB = "USE " + DATABASE_NAME + ";"

SQL_SHOW_TABLES = "SHOW TABLES;"


SQL_CREATE_CATEGORY_TABLE = "CREATE TABLE IF NOT EXISTS `Category` (" \
                            "`ID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT," \
                            "`Name` VARCHAR(50) UNIQUE," \
                            "PRIMARY KEY (`ID`)" \
                            ")" \
                            "ENGINE=INNODB;"

SQL_CREATE_PRODUCT_TABLE = "CREATE TABLE IF NOT EXISTS `Product` (" \
                           "`ID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT," \
                           "`Name` VARCHAR(150)," \
                           "`Code` BIGINT UNSIGNED UNIQUE," \
                           "`Brand` VARCHAR(100)," \
                           "`Nutrition_grade` CHAR(1)," \
                           "`Energy_100g` SMALLINT UNSIGNED," \
                           "`URL` TEXT," \
                           "PRIMARY KEY (`ID`)" \
                           ")" \
                           "ENGINE=INNODB;"

SQL_CREATE_STORE_TABLE = "CREATE TABLE IF NOT EXISTS `Store` (" \
                         "`ID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT," \
                         "`Name` VARCHAR(50) UNIQUE," \
                         "PRIMARY KEY (`ID`)" \
                         ")" \
                         "ENGINE=INNODB;"

SQL_CREATE_CITY_TABLE = "CREATE TABLE IF NOT EXISTS `City` (" \
                        "`ID` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT," \
                        "`Name` VARCHAR(50) UNIQUE," \
                        "`Zip_code` SMALLINT UNSIGNED," \
                        "PRIMARY KEY (`ID`)" \
                        ")" \
                        "ENGINE=INNODB;"

SQL_CREATE_SUBSTITUTE_TABLE = "CREATE TABLE IF NOT EXISTS `Substitute` (" \
                              "`ID` BIGINT UNSIGNED  NOT NULL AUTO_INCREMENT," \
                              "`Users_ID` TINYINT UNSIGNED," \
                              "`Product_ID` BIGINT UNSIGNED," \
                              "`Date` DATETIME," \
                              "`Note` VARCHAR(140)," \
                              "KEY `PK, FK` (`ID`)," \
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
                         "`Name` VARCHAR(15) UNIQUE," \
                         "`Password` BLOB NOT NULL," \
                         "PRIMARY KEY (`ID`)" \
                         ")" \
                         "ENGINE=INNODB;"

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


SQL_INSERT_PRODUCTS = "INSERT IGNORE INTO Product " \
                              "(Name, Brand, Nutrition_grade, Energy_100g, URL, Code) VALUES (%s, %s, %s, %s, %s ,%s);"

SQL_INSERT_STORES = "INSERT IGNORE INTO Store (Name) VALUES (%s);"

SQL_INSERT_CITIES = "INSERT IGNORE INTO City (Name) VALUES (%s);"

SQL_INSERT_PRODUCT_LOCATION = "INSERT INTO ProductLocation (Product_ID, Store_ID, City_ID) VALUES (%s, %s, %s);"

SQL_INSERT_CATEGORIES = "INSERT IGNORE INTO Category (Name) VALUES (%s);"

SQL_INSERT_CATEGORY_PRODUCT = "INSERT INTO CategoryProduct (Product_ID, Category_ID) VALUES (%s, %s);"

SQL_INSERT_USER = "INSERT IGNORE INTO Users (Name, Password) VALUES (%s, %s);"

SQL_INSERT_SUBSTITUTE = "INSERT INTO Substitute (Users_ID, Product_ID, Date, Note) VALUES (%s, %s, NOW(), %s);"

LAST_INSERT_ID = "SELECT LAST_INSERT_ID();"


SQL_UPDATE_SUBSTITUTE_NOTE = "UPDATE Substitute SET Note = %s WHERE Substitute.Product_ID = %s;"

SQL_DELETE_SUBSTITUTE = "DELETE From Substitute WHERE Substitute.ID = %s;"


SQL_SELECT_CATEGORY = "SELECT ID FROM Category WHERE Name = %s;"

SQL_SELECT_STORE = "SELECT ID FROM Store WHERE Name = %s;"

SQL_SELECT_CITY = "SELECT ID FROM City WHERE Name = %s;"

SQL_SELECT_USER_NAME = "SELECT * FROM Users WHERE Name = %s;"

SQL_SELECT_PRODUCT = "" \
                                         "SELECT Product.ID, Product.Name, Product.Brand, Product.Nutrition_grade, " \
                                         "Product.Energy_100g, Product.Code, Product.URL " \
                                         "FROM Product " \
                                         "LEFT JOIN ProductLocation ON Product.ID = ProductLocation.Product_ID " \
                                         "WHERE Product.ID = %s;"

SQL_SELECT_CATEGORIES = "SELECT Category.Name, COUNT(CategoryProduct.Category_ID) AS NB_Cat, Category.ID " \
                        "FROM CategoryProduct " \
                        "INNER JOIN Category ON CategoryProduct.Category_ID = Category.ID " \
                        "GROUP BY CategoryProduct.Category_ID " \
                        "ORDER BY NB_Cat DESC LIMIT 20;"

SQL_SELECT_PRODUCTS_BY_CATEGORY = "SELECT DISTINCT Product.ID, Product.Name, Product.Brand, " \
                                  "Product.Code, Product.Nutrition_grade, Product.Energy_100g " \
                                  "FROM Product " \
                                  "INNER JOIN CategoryProduct ON Product.ID = CategoryProduct.Product_ID " \
                                  "INNER JOIN Category ON CategoryProduct.Category_ID = Category.ID " \
                                  "WHERE Category.ID = %s;"

SQL_SELECT_PRODUCTS_BY_NAME = "" \
                            "SELECT DISTINCT Product.ID, Product.Name, Product.Brand, " \
                            "Product.Code, Product.Nutrition_grade, Product.Energy_100g " \
                            "FROM Product " \
                            "WHERE Product.Name LIKE %s " \
                            "ORDER BY Product.Name;"

SQL_SELECT_CATEGORY_PRODUCT = "SELECT DISTINCT Product.ID, Product.Name, Category.ID, Category.Name FROM Category " \
                              "INNER JOIN CategoryProduct ON CategoryProduct.Category_ID = Category.ID " \
                              "INNER JOIN Product ON CategoryProduct.Product_ID = Product.ID " \
                              "WHERE Product.ID = %s;"

SQL_SELECT_CITY_PRODUCT = "SELECT DISTINCT Product.ID, Product.Name, City.ID, City.Name FROM City " \
                          "INNER JOIN ProductLocation ON City.ID = ProductLocation.City_ID " \
                          "INNER JOIN Product ON ProductLocation.Product_ID = Product.ID " \
                          "WHERE Product.ID = %s;"

SQL_SELECT_STORE_PRODUCT = "SELECT DISTINCT Product.ID, Product.Name, Store.ID, Store.Name FROM Store " \
                          "INNER JOIN ProductLocation ON Store.ID = ProductLocation.Store_ID " \
                          "INNER JOIN Product ON ProductLocation.Product_ID = Product.ID " \
                          "WHERE Product.ID = %s;"

SQL_SELECT_SUBSTITUTE = "SELECT products_selection.ID, " \
                        "products_selection.Nutrition_grade, products_selection.Energy_100g " \
                        "FROM (%s) AS products_selection " \
                        "ORDER BY products_selection.Nutrition_grade, products_selection.Energy_100g;"

SQL_SELECT_SUBSTITUTES_BY_USER = "SELECT DISTINCT Product.ID, Product.Name, Product.Brand, " \
                                 "Product.Nutrition_grade, Product.Energy_100g, " \
                                 "DATE_FORMAT(Substitute.Date, '%d/%m/%Y'), " \
                                 "Substitute.Note, Substitute.ID "\
                                 "FROM Product " \
                                 "INNER JOIN Substitute ON Product.ID = Substitute.Product_ID " \
                                 "INNER JOIN Users ON Substitute.Users_ID = Users.ID " \
                                 "WHERE Users.ID = %s;"


