"""from Cam_FoodChoice.data import *
from Cam_FoodChoice.CategoryManager import CategoryManager
from Cam_FoodChoice.ProductManager import ProductManager"""
from Cam_FoodChoice.DatabaseManager import DatabaseManager
from Cam_FoodChoice.Database import Database

#launch the programm
init_db = DatabaseManager()
db = init_db.init_database()

#display the different elements in the database
display = Database()
display.display_databases(db)
display.display_users(db)
display.display_tables(db)
display.display_data_in_tables(db)