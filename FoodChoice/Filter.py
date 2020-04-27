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