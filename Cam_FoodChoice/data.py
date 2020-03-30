#categories
CATEGORIES_URL = "https://fr.openfoodfacts.org/categories.json"
#CATEGORIES_URL = "https://httpbin.org/status/404"
CATEGORIES_KEY = "tags"
CATEGORIES_NAME_FIELD = "name"
NB_CAT_SELECTED_AMONG_THE_LIST = 20
CATEGORIES_REG_EXP = "^[A-Z].+"

#products
PRODUCTS_URL = "https://fr.openfoodfacts.org/cgi/search.pl?"
PRODUCT_KEY = "products"
PRODUCTS_NAME_FIELD = "nutrition_grades"
NB_PROD_SELECTED_AMONG_THE_LIST = 250

#random seed
SEED = 100

#database
DATABASE_NAME = "FoodChoice"
HOST_NAME = "localhost"
USER_NAME_ROOT = "root"
USER_PASSWORD_ROOT = "my-secret-pw"


#TODO : à supprimer
#docker run -d -p 3306:3306 -v /Users/cam/Documents/Dev/OC/Projet/P5/Cam_FoodChoice/mysql_folder:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw mysql:8.0.19