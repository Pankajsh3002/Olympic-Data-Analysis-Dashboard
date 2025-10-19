import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host="Localhost",
    user="root",
    password="9811052565",
)
if mydb.is_connected():
    print("Connected to the database successfully!")

cursor=mydb.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS check_db")
cursor.execute("use check_db")


df=pd.read_csv(r"C:\Users\jiten\Desktop\Stream.csv")
df.columns = df.columns.str.replace(' ', '_')

table_name = 'stream_data'
create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Date INT,
        doctype VARCHAR(255),
        county VARCHAR(255),
        field VARCHAR(255),
        Total INT,
        filled INT,
        auto_filled INT,
        manual_filled INT
    )
    """
cursor.execute(create_table_query)
print(f"Table '{table_name}' is ready.")
cursor.execute(f"TRUNCATE TABLE {table_name}")

data_to_insert = [tuple(row) for row in df.itertuples(index=False)]

# The SQL query now matches the cleaned column names
sql = f"""
INSERT INTO {table_name} (Date, doctype, county, field, Total, filled, auto_filled, manual_filled) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

# Execute the insert in one go
cursor.executemany(sql, data_to_insert)

# --- 5. Commit the Changes ---
# This saves all the inserted data to your database
mydb.commit()
print(f"{cursor.rowcount} records were inserted into the '{table_name}' table.")