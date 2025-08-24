### Linq Nutrition Student File Generator ###
# This Script Generates a File with Student Information
# to Upload to LINQ Nutrition Management System


### Import Modules ###
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
from os import getenv
from dotenv import load_dotenv
#####################

### Variables ###
# Load .ENV File
load_dotenv('./.env')
# MySQL Vars
sql_username = getenv('sql_username')
sql_pass = getenv('sql_pass')
sql_hostname = getenv('sql_hostname')
dsc_db_name = getenv('dsc_db_name')
# IC Vars
mssql_driver = 'ODBC Driver 18 for SQL Server'
ic_db_hostname = getenv('ic_db_hostname')
ic_db_username = getenv('ic_db_username')
ic_db_pass = getenv('ic_db_pass')
ic_db_name = getenv('ic_db_name')
# Query Vars from files
with open('./linq_ic_rc_student_query.sql', 'r') as file:
    linq_ic_rc_student_query = file.read()
with open('./linq_ic_charter_student_query.sql', 'r') as file:
    linq_charter_student_query = file.read()
with open('./linq_student_allergy_query.sql', 'r') as file:
    linq_student_allergy_query = file.read()
#####################


### Fetch Student Data from IC ###
# Create DB Connection
engine = create_engine(
    f"mssql+pyodbc://{ic_db_username}:{ic_db_pass}@{ic_db_hostname}/{ic_db_name}?driver={mssql_driver}&TrustServerCertificate=yes")
# Store RC Student Data in DataFrame
df_ic_rc_students = pd.read_sql_query(linq_ic_rc_student_query, engine)
# Close Connection
engine.dispose()
##################################

### Fetch Data from DSC ###
# Create DB Connection
engine = create_engine(f'mysql+pymysql://{sql_username}:{sql_pass}@{sql_hostname}/{dsc_db_name}')
# Store Charter Student Data in DataFrame
df_ic_charter_students = pd.read_sql_query(linq_charter_student_query, engine)
# Store Student Allergy Data in DataFrame
df_student_allergies = pd.read_sql_query(linq_student_allergy_query, engine)
# Close Connection
engine.dispose()
##################################

### Merge DataFrames ###
# Format Student IDs for Merging
df_student_allergies['Student Id'] = df_student_allergies['Student Id'].astype(str)
df_ic_charter_students['Student Id'] = df_ic_charter_students['Student Id'].astype(str)
# Merge DataFrames
df_ic_rc_students = pd.merge(df_ic_rc_students, df_student_allergies, how='left', on='Student Id')
df_students_all = pd.concat([df_ic_rc_students, df_ic_charter_students], ignore_index=True)
# Drop Duplicates Students
df_students_all = df_students_all.drop_duplicates(subset='Student Id')
# Set Student ID to 6 Digits
df_students_all['Student Id'] = df_students_all['Student Id'].str.zfill(6)
# Convert Year to Integer
df_students_all['Current School Year'] = df_students_all['Current School Year'].astype(int)
#########

### Export Final File ###
df_students_all.to_csv('linq_student_file.csv', index=False)
#########################