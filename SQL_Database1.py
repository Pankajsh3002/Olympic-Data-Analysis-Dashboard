import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host="localhost",      
    user="root",           
    password="9811052565", 
)

if mydb.is_connected():
    print("Connection to the database was successful!")

cursor=mydb.cursor()


#Creating Database 
cursor.execute("CREATE DATABASE IF NOT EXISTS company_db")
print("Database 'company_db' Created Successfully")

# Listing all databases
# cursor.execute("SHOW DATABASES")
# for db in cursor:
#     print(db)

cursor.execute("USE company_db")

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department VARCHAR(50),
    salary DECIMAL(10,2),
    hire_date DATE
)
""")

print(" Table 'employees' ready to use!")

query = """
INSERT INTO employees (first_name, last_name, department, salary, hire_date)
VALUES (%s, %s, %s, %s, %s)
"""

values = [
    ("Pankaj", "Sharma", "Finance", 50000.00, "2023-03-12"),
    ("Amit", "Verma", "IT", 60000.00, "2022-10-01"),
    ("Neha", "Singh", "HR", 45000.00, "2024-01-18"),
    ("Rohit", "Kumar", "Sales", 55000.00, "2021-07-25"),
    ("Riya", "Mehta", "HR", 47000.00, "2024-07-10"),
    ("Deepak", "Yadav", "Operations", 52000.00, "2020-12-05"),
    ("Karan", "Patel", "IT", 65000.00, "2022-05-14"),
    ("Sneha", "Goyal", "Finance", 48000.00, "2023-08-22"),
    ("Vikram", "Nair", "Sales", 57000.00, "2021-11-09"),
    ("Priya", "Raj", "Marketing", 53000.00, "2022-02-17")
]

cursor.executemany(query, values)
mydb.commit()

print(f"{cursor.rowcount} records inserted successfully!")


cursor.execute("SELECT * FROM employees")
row=cursor.fetchall()
df=pd.DataFrame(row,columns=[desc[0] for desc in cursor.description])
df.to_excel("employeee_data.xlsx",index=False)