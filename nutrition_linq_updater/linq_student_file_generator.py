### Linq Nutrition Student File Generator ###
# This Script Generates a File with Student Information
# to Upload to LINQ Nutrition Management System

def linq_student_file_generator(env_file):

    ### Import Modules ###
    import pandas as pd
    import logging
    import pyodbc
    from datetime import datetime
    from sqlalchemy import create_engine
    from os import getenv
    from dotenv import load_dotenv
    from linq_postive_outcomes_data_download import linq_positive_outcomes_data_download
    from linq_urban_promise_data_download import linq_urban_promise_data_download
    #####################

    ### Variables ###
    # Load .ENV File
    load_dotenv(env_file)
    # File Vars
    today_str = datetime.today().strftime('%Y-%m-%d')
    final_student_file = getenv('final_student_file')
    log_path = getenv('log_path')
    log_file = f"{log_path}/linq_student_file_generator_{today_str}.log"
    # MySQL Vars
    sql_username = getenv('sql_username')
    sql_pass = getenv('sql_pass')
    sql_hostname = getenv('sql_hostname')
    dsc_db_name = getenv('dsc_db_name')
    # IC Vars
    mssql_driver = 'FreeTDS'
    ic_db_hostname = getenv('ic_db_hostname')
    ic_db_username = getenv('ic_db_username')
    ic_db_pass = getenv('ic_db_pass')
    ic_db_name = getenv('ic_db_name')
    # Google Vars
    google_auth_key = getenv('google_auth_key')
    positive_outcomes_sheet_id = getenv('positive_outcomes_sheet_id')
    urban_promise_sheet_id = getenv('urban_promise_sheet_id')
    # Query Vars from files
    with open('./linq_ic_rc_student_query.sql', 'r') as file:
        linq_ic_rc_student_query = file.read()
    with open('./linq_ic_charter_student_query.sql', 'r') as file:
        linq_charter_student_query = file.read()
    with open('./linq_student_allergy_query.sql', 'r') as file:
        linq_student_allergy_query = file.read()
    #####################

    ### Logging Setup ###
    logger = logging.getLogger("nutrition_linq_student")
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(message)s'))
        logger.addHandler(handler)
    logger.propagate = False    
    #####################

    ### Fetch Student Data from IC ###
    try:
        # Create DB Connection
        engine = create_engine(
            f"mssql+pyodbc://{ic_db_username}:{ic_db_pass}@{ic_db_hostname}/{ic_db_name}?driver={mssql_driver}&TrustServerCertificate=yes")
        # Store RC Student Data in DataFrame
        df_ic_rc_students = pd.read_sql_query(linq_ic_rc_student_query, engine)
        # Log Success
        logger.info("Successfully fetched IC RC student data.")
    except Exception as e:
        logger.error(f"Error fetching IC RC student data: {e}")
    # Close Connection
    engine.dispose()
    ##################################

    ### Fetch Data from DSC ###
    try:
        # Create DB Connection
        engine = create_engine(f'mysql+pymysql://{sql_username}:{sql_pass}@{sql_hostname}/{dsc_db_name}')
        # Store Charter Student Data in DataFrame
        df_ic_charter_students = pd.read_sql_query(linq_charter_student_query, engine)
        # Store Student Allergy Data in DataFrame
        df_student_allergies = pd.DataFrame()
        # Close Connection
        engine.dispose()
        # Log Success
        logger.info("Successfully fetched DSC student data.")
    except Exception as e:
        logger.error(f"Error fetching DSC student data: {e}")
    # Close Connection
    engine.dispose()
    ##################################

    ### Fetch Data from Google Sheets ###
    try:
        # Positive Outcomes Academy
        df_poa_students = linq_positive_outcomes_data_download(google_auth_key, positive_outcomes_sheet_id)
        # Log Success
        logger.info("Successfully fetched Positive Outcomes Academy student data.")
        # Urban Promise
        df_urban_promise = linq_urban_promise_data_download(google_auth_key, urban_promise_sheet_id)
        # Log Success
        logger.info("Successfully fetched Urban Promise student data.")
    except Exception as e:
        logger.error(f"Error fetching data from Google Sheets: {e}")
        df_poa_students = pd.DataFrame()
        df_urban_promise = pd.DataFrame()
    #####################################

    ### Merge DataFrames ###
    try:
        # Format Student IDs for Merging
        #df_student_allergies['Student Id'] = df_student_allergies['Student Id'].astype(str)
        df_ic_charter_students['Student Id'] = df_ic_charter_students['Student Id'].astype(str)
        df_urban_promise['Student Id'] = df_urban_promise['Student Id'].astype(str)
        df_poa_students['Student Id'] = df_poa_students['Student Id'].astype(str)
        # Merge DataFrames
        #df_ic_rc_students = pd.merge(df_ic_rc_students, df_student_allergies, how='left', on='Student Id')
        df_students_all = pd.concat([df_ic_rc_students, df_ic_charter_students, df_poa_students, df_urban_promise], ignore_index=True)
        # Drop Duplicates Students
        df_students_all = df_students_all.drop_duplicates(subset='Student Id').copy()
        # Set Student ID to 6 Digits
        df_students_all['Student Id'] = df_students_all['Student Id'].str.zfill(6)
        # Fix Year
        df_students_all['Current School Year'] = df_students_all['Current School Year'].fillna(0).astype(int)
        # Log Success
        logger.info("Successfully created final student dataframe.")
    except Exception as e:
        logger.error(f"Error creating final student dataframe: {e}")
    ###################################

    ### Export Final File ###
    df_students_all.to_csv(final_student_file, index=False)
    #########################

if __name__ == "__main__":
    import sys
    env_file = sys.argv[1] if len(sys.argv) > 1 else './.env'
    # Call the function with override
    linq_student_file_generator(env_file)
