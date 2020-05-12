Pur Beurre x OpenFoodFacts: FoodChoice
=================

This is a student project made for the project 5 from [OpenClassrooms](https://openclassrooms.com/ )'s Python course.

This project aims to help the Pur Beurre compagny's customer to eat healthier thanks to the [Open Food facts](https://world.openfoodfacts.org/) data.

1. Before starting
2. To use the program
3. Functions
4. Made with
5. Contributing
6. Versions
7. Authors

## 1. Before starting

> You need to install MySQL

* MySQL 8 -> please follow [the official documentation](https://dev.mysql.com/doc/mysql-installation-excerpt/8.0/en/)

After MySQL installation, in your terminal use theses commands:

> Configure MySQL

Create a user with all privileges:

`CREATE USER 'FoodChoiceUser'@'localhost' IDENTIFIED BY 'FoodChoiceUser'`  
`GRANT ALL ON *.* TO 'FoodChoiceUser'@'localhost';`

*If you want to use a different host, it will be necessary to update HOST_NAME in data.py*

> Clone the repository from Github

`git clone git@github.com:CamClrt/FoodChoice.git` or `git clone https://github.com/CamClrt/FoodChoice.git`

> Install the package

TODO

`pip install .`

## 2. To use the program

The application is built for being used in a terminal's interface.
The user can interact with it with keyboard.

**Important**: for the moment the program is only available in French.

## 3. Functions

* Connect without account to the application
* Create and log in to his personal account (an user name and password is required)
* Find a product by his category or his name
* Display the product's details (Name, Brand, Code, Nutrition_grade, Energy_100g, URL, Categories, Stores and Cities)
* Substitute the current product by an other healthier (compare to the 'Nutrition_grade' and the 'Energy_100g' fields)
* Record the substitute in a list linked to the account (personal or not)
* Display the substitute list and consult the details of one substitute, add it some personal short note or delete it
* Quit the program

## 4. Made with

* PyCharm: https://www.jetbrains.com/fr-fr/pycharm/, text editor
* OpenFoodFacts: https://fr.openfoodfacts.org/, API
* MySQL 8, RDBMS
* Love 💙

## 5. Contributing

Feel free to contribute to this project

## 6. Versions

Created in:   May 2020  
Developed:  March/May 2020  
Last version: https://github.com/CamClrt/FoodChoice

## 7. Authors

**Camille Clarret** aka **Camoulty** or **CamClrt** : https://github.com/CamClrt/labyrinth/  
Baby dev 🐣 I'm learning 🐍 #Python with [OpenClassrooms](https://openclassrooms.com/ )

**Aymen Mouelhi** (as supervisor): https://github.com/aymen-mouelhi
