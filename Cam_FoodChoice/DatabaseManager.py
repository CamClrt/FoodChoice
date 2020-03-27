import mysql.connector
from mysql.connector import Error



def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    mycursor = connection.cursor()

    mycursor.execute("CREATE DATABASE FoodChoice")

    mycursor.execute("SHOW DATABASES")

    for x in mycursor:
        print(x)

    return connection

connection = create_connection("localhost", "root", "my-secret-pw")