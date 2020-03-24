#categories
CATEGORIES_URL = "https://fr.openfoodfacts.org/categories.json"
CATEGORIES_KEY = "tags"
CATEGORIES_NAME_FIELDS = "name"
NB_CAT_SELECTED_AMONG_THE_LIST = 20
CATEGORIES_REG_EXP = "..:.+"


#products

#the 6 parts of the search request to associate one category with products
REQUEST_URL = "https://fr.openfoodfacts.org/cgi/search.pl?"
ACTION = "action=process"
TAGTYPE_0 = "&tagtype_0=categories"
TAG_CONTAINS_0 =  "&tag_contains_0=contains"
TAG_0 = "&tag_0=" #in this part, add the name of the category
JSON_FORMAT = "&json=true"

PRODUCT_KEY = "products"
NB_PROD_SELECTED_AMONG_THE_LIST = 20