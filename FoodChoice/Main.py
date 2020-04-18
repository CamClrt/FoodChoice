from FoodChoice.DatabaseManager import DatabaseManager
from FoodChoice.Database import Database


#launch the programm
init_db = DatabaseManager()
db = init_db.init_database()

#display the different elements in the database
display = Database()
display.display_databases(db)
display.display_users(db)
display.display_tables(db)
display.display_data_in_tables(db)