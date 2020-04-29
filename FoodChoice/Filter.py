import re


class Filter:

    def __init__(self):
        pass

    def cat_filter(self, tmp_category):
        #TODO docstring
        category = tmp_category.replace("'", " ").strip().capitalize()

        if re.search("..:", category):
            if category[:2] == "fr:":
                return (category[3:])[:50]
        else:
            return category[:50]

    def city_filter(self, tmp_city):
        #TODO docstring
        city = tmp_city.replace("'", " ").strip().capitalize()
        return city[:50]


    def store_filter(self, tmp_store):
        # TODO docstring
        store = tmp_store.replace("'", " ").strip().capitalize()
        return store[:50]

    def prod_filters(self, tmp_name, tmp_brand, tmp_nutrition_grade, tmp_energy_100g, tmp_url, tmp_code):
        name = (tmp_name[:150]).replace("'", "")
        brand = (tmp_brand[:100]).replace("'", "")
        nutrition_grade = tmp_nutrition_grade[:1]
        energy_100g = str(tmp_energy_100g)
        url = tmp_url.replace("'", "")
        code = str(tmp_code)
        return name, brand, nutrition_grade, energy_100g, url, code