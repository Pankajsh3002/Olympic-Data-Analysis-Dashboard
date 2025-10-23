import mysql.connector
import pandas as pd
import numpy as np

mydb = mysql.connector.connect(
    host="Localhost",
    user="root",
    password="9811052565"
)
if mydb.is_connected():
    print("Connected to the database successfully!")

cursor=mydb.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS Olympic_Games_History")
print("Created Database 'Olympic_Games_History' Successfully")
cursor.execute("USE Olympic_Games_History")

#Getting Data from csv file
data_path=r"D:\Projects\Web-Application\Dataset\Olympic History.csv"
df=pd.read_csv(data_path,sep=",")

#Data Cleaning
#dropping where Age, Height, Weight is null
df.dropna(subset=['Age','Height', 'Weight'], inplace=True)
df['Sex']=df['Sex'].replace({'M':'Male','F':'Female'})

table_name="olympic_history"
create_table_query =f"""CREATE TABLE IF NOT EXISTS {table_name} (
    ID INT,
    Name VARCHAR(255),
    Sex CHAR(10),
    Age INT,
    Height INT,
    Weight INT,
    Team VARCHAR(100),
    NOC CHAR(3),
    Games VARCHAR(100),
    Year INT,
    Season VARCHAR(20),
    City VARCHAR(100),
    Sport VARCHAR(100),
    Event VARCHAR(100),
    Medal VARCHAR(20)
)"""
cursor.execute(create_table_query)
print(f"Table '{table_name}' is ready.")

#cursor.execute(f"TRUNCATE TABLE {table_name}")
#inserting data form csv to sql table
data_to_insert = [tuple(row) for row in df.itertuples(index=False)]

sql = f"""
INSERT INTO {table_name} (ID,Name,Sex,Age,Height,Weight,Team,NOC,Games,Year,Season,City,Sport,Event,Medal) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Execute the insert in one go
cursor.executemany(sql, data_to_insert)
# Commit the Changes
mydb.commit()
print(f"{cursor.rowcount} records were inserted into the '{table_name}' table.")
