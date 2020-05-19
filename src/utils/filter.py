"""
    This module store all the useful filters to process API data
"""

import re


def cat_filter(tmp_category):
    """Filter categories data"""
    res = None
    category = tmp_category.strip().capitalize()
    if re.search("..:", category):
        if category[:2] == "fr:":  # exclude foreign categories
            res = (category[3:])[:50]
    else:
        res = category[:50]
    return res


def city_filter(tmp_city):
    """Filter cities data"""
    city = tmp_city.strip().capitalize()
    return city[:50]


def store_filter(tmp_store):
    """Filter stores data"""
    store = tmp_store.strip().capitalize()
    return store[:50]


def prod_filters(tmp_name, tmp_brand, tmp_nutrition_grade,
                 tmp_energy_100g, tmp_url, tmp_code):
    """Filter products data"""
    name = tmp_name[:150]
    brand = tmp_brand[:100]
    nutrition_grade = tmp_nutrition_grade[:1]
    energy_100g = str(tmp_energy_100g)
    url = tmp_url
    code = str(tmp_code)
    return name, brand, nutrition_grade, energy_100g, url, code
