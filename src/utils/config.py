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
NB_CAT_SELECTED_AMONG_THE_LIST = 10
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
    "page_size": "50",
    "json": "true"
}
