#! /usr/bin/env python
# coding: utf-8

from FoodChoice.App import App
from FoodChoice.API import API


if __name__ == "__main__":
    app = App()
    user_object = app.start()
    app.main_menu(user_object)

else:
    print("main module is imported")


