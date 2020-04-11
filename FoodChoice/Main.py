from FoodChoice.DatabaseManager import DatabaseManager
from FoodChoice.Database import Database

import time


#launch the programm
init_db = DatabaseManager()
db = init_db.init_database()
categories = init_db.insert_category_data(db)
for category in categories:
    init_db.insert_product_data(db, category)


#display the different elements in the database
time.sleep(2)
display = Database()
display.display_databases(db)
display.display_users(db)
display.display_tables(db)
display.display_data_in_tables(db)
