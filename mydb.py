import mysql.connector

dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2413",
    database="elderco"  
)


# cursor object
currsorObject = dataBase.cursor()

# create databse
currsorObject.execute("CREATE DATABASE elderco")

print("All Done")