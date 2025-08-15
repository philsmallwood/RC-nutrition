###


### Import Modules ###
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
from os import getenv
from dotenv import load_dotenv
###

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
with open('./linq_ic_student_query.sql', 'r') as file:
    linq_ic_student_query = file.read()
with open('./linq_student_allergy_query.sql', 'r') as file:
    linq_student_allergy_query = file.read()
##


### Fetch Student Data from IC ###
engine = create_engine(f"mssql+pyodbc://{ic_db_username}:{ic_db_pass}@{ic_db_hostname}/{ic_db_name}?driver={mssql_driver}&TrustServerCertificate=yes")
df_ic_students = pd.read_sql_query(linq_ic_student_query, engine)
engine.dispose()
##################################

### Fetch Allergy Data from DSC ###
engine = create_engine(f'mysql+pymysql://{sql_username}:{sql_pass}@{sql_hostname}/{dsc_db_name}')
df_student_allergies = pd.read_sql_query(linq_student_allergy_query, engine)
engine.dispose()
##################################

### Merge DataFrames ###
# Format Student Ids
df_student_allergies['Student Id'] = df_student_allergies['Student Id'].astype(str)
# Merge
df_students = pd.merge(df_ic_students, df_student_allergies, how='left', on='Student Id')
# Drop Duplicates
df_students = df_students.drop_duplicates(subset='Student Id')
######

### Export Final File ###
df_students.to_csv('linq_student_file.csv', index=False)
