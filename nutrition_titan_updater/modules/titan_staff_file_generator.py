### RC Titan Staff File Script
### Script to Generate a Staff File 
### to Upload to Titan/LINQ

def titan_staff_file_generator():

    ###Import Modules
    import csv
    import pandas as pd
    from datetime import date
    from os import getenv
    from dotenv import load_dotenv
    from sqlalchemy import create_engine
    #######

    ###Variables###
    # Load .ENV File
    load_dotenv()
    # Date
    current_date = date.today()
    staff_date = current_date.strftime('%m/%d/%Y')
    # Log Entry
    log_entry = ""
    # Files
    staff_final_file = getenv('staff_final_file')
    # MySQL Vars
    sql_username = getenv('sql_username')
    sql_pass = getenv('sql_pass')
    sql_hostname = getenv('sql_hostname')
    db_name = getenv('db_name')
    staff_table_name = getenv('staff_table_name')
    #######

    ### Get Info from MySQL ###
    # Create SQL Connection Object
    engine = create_engine(f'mysql+pymysql://{sql_username}:{sql_pass}@{sql_hostname}/{db_name}')
    # Load Info into Temp Table
    df_employee_info = pd.read_sql(f'SELECT * FROM {staff_table_name}', con=engine)
    ########

    ### Create Final Dataframe ###
    df_final = pd.DataFrame()
    df_final['EmployeeID'] = 'E' + df_employee_info['employeeID']
    df_final['FirstName'] = df_employee_info['givenName']
    df_final['MiddleName'] = df_employee_info['middleName'].str[0]
    df_final['LastName'] = df_employee_info['sn']
    df_final['EmailAddress'] = df_employee_info['userPrincipalName'].str.lower()
    df_final['StaffStateID'] = 'E' + df_employee_info['employeeID']
    df_final['Dob'] = df_employee_info['extensionAttribute1']
    df_final['HR_Gender'] = df_employee_info['extensionAttribute9']
    df_final['HR_Location'] = '320' + df_employee_info['departmentNumber'].astype('Int64').astype('str')
    df_final['StaffType'] = 'General'
    df_final['AssignmentStart'] = staff_date
    ########

    ### Format Final DataFrame ###
    # Drop Duplicates
    df_final.drop_duplicates('EmployeeID', inplace=True)
    # Drop Staff with No Location
    df_final = df_final[df_final['HR_Location'] != '320<NA>']
    ########

    ### Export CSV File ###
    df_final.to_csv(staff_final_file, 
                    quoting=csv.QUOTE_ALL,
                    index=False)
    #######

    ### Log Entry ###
    log_entry += "---------------------------------\n"
    log_entry += "Titan Staff File Script Completed\n"
    log_entry += "---------------------------------\n"
    #######
    return log_entry

if __name__ == '__main__':
    log_entry = titan_staff_file_generator()
    print(log_entry)