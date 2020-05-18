"""
    Application using Pur Beurre Substitute
    This application is made for the project 5 on OpenClassrooms during the
    Python courses
    The aim of this project is to use:
        - an API Rest,
        - a database like MySQL,
        - and of course Python.
"""

# ! /usr/bin/env python
# coding: utf-8

from app.app import App


if __name__ == "__main__":
    app = App()
    app.start()
