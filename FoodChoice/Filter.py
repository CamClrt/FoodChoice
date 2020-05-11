import re


class Filter:
    """Allow to filter API data before DB insertion"""

    def __init__(self):
        pass

    def cat_filter(self, tmp_category):
        """Filter categories data"""
        category = tmp_category.strip().capitalize()
        if re.search("..:", category):
            if category[:2] == "fr:":  # exclude foreign categories
                return (category[3:])[:50]
        else:
            return category[:50]

    def city_filter(self, tmp_city):
        """Filter cities data"""
        city = tmp_city.strip().capitalize()
        return city[:50]

    def store_filter(self, tmp_store):
        """Filter stores data"""
        store = tmp_store.strip().capitalize()
        return store[:50]

    def prod_filters(self, tmp_name, tmp_brand, tmp_nutrition_grade, tmp_energy_100g, tmp_url, tmp_code):
        """Filter products data"""
        name = tmp_name[:150]
        brand = tmp_brand[:100]
        nutrition_grade = tmp_nutrition_grade[:1]
        energy_100g = str(tmp_energy_100g)
        url = tmp_url
        code = str(tmp_code)
        return name, brand, nutrition_grade, energy_100g, url, code