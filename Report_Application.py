import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#----------------------------Connecting to the Database----------------------------#
mydb= mysql.connector.connect(
    host="Localhost",
    user="root",
    password="9811052565",
    database="Olympic_Games_History"
)

if mydb.is_connected():
    print("Connected to the database 'Olympic_Games_History' successfully!")
cursor=mydb.cursor()

cursor.execute("select * from olympic_history")
results=cursor.fetchall()


#-------------------------Creating Streamlit Application-------------------------#
#Streamlit Page Configuration
st.set_page_config(layout="wide")

#Getting Columns Names
column_names = [i[0] for i in cursor.description]

#Streamlit Application title
st.title("Olympic Games History Data Overview")

#Showing Dataframe in Streamlit
st.dataframe(pd.DataFrame(results,columns=column_names))