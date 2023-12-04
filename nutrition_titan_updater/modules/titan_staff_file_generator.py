#!/usr/bin/env python3
###RC Titan Staff File Script
###Script to generate a student file with the necesary info for nutrition

def titan_staff_file_generator():

    ###Import Modules
    import csv
    import pandas as pd
    from datetime import date
    from os import getenv
    from dotenv import load_dotenv
    from dfcleanup import df_stripper #Self Created Module
    #######

    ###Variables###
    #Load .ENV File
    load_dotenv()
    #Date
    current_date = date.today()
    staff_date = current_date.strftime('%m/%d/%Y')
    #Log Entry
    log_entry = ""
    #Files
    staff_file = getenv('staff_file')
    staff_email_file = getenv('staff_email_file')
    contractor_file = getenv('contractor_file')
    staff_final_file = getenv('staff_final_file')
    ###Set Dictionaries to Rename Columns
    col_names_staff = { 0 : 'EmployeeID', 
                1 : 'LastName',
                2 : 'FirstName',
                3 : 'MiddleName',
                4 : 'Dob',
                7 : 'HR_Location',
                14 : 'HR_Gender'}
    col_names_email = { 0 : 'EmployeeID',
                1 : 'EmailAddress'}
    col_names_contractors = { 0 : 'EmployeeID', 
                1 : 'FirstName',
                2 : 'MiddleName',
                3 : 'LastName',
                9 : 'Dob',
                7 : 'EmailAddress',
                8 : 'HR_Location'}
    #######

    #####Read Files into Dataframes#####    
    ###Read Staff File into Dataframe
    df_staff = pd.read_csv(staff_file, skiprows=1, \
        header=None, dtype=str)
    df_staff = df_stripper(df_staff)
    df_staff.rename(columns=col_names_staff, inplace=True)
    ###Read Email File into Dataframe
    df_email = pd.read_csv(staff_email_file, skiprows=1, \
        header=None, dtype=str)
    df_email = df_stripper(df_email)
    df_email.rename(columns=col_names_email, inplace=True)
    ###Read Contractor File into Dataframe
    df_contractors = pd.read_csv(contractor_file, skiprows=1, \
        header=None, dtype=str)
    df_contractors = df_stripper(df_contractors)
    df_contractors.rename(columns=col_names_contractors, inplace=True)
    #######

    #####Format the Data#####
    ###Add 'E' to EmployeeID to State Employee IDs
    df_staff['EmployeeID'] = 'E' + df_staff['EmployeeID'].astype(str)
    df_email['EmployeeID'] = 'E' + df_email['EmployeeID'].astype(str)
    ###Combine Employees with Emails
    df_staff_emails = df_staff.merge(df_email[['EmployeeID','EmailAddress']], \
        on='EmployeeID', how='left')
    ###Combine Contractors with FTE Employees
    df_staff_all = pd.concat([df_staff_emails, df_contractors])
    ###Add District Identifier to Building Code
    df_staff_all['HR_Location'] = '320' + df_staff_all['HR_Location'].astype(str)
    #######

    ###Final Datafram###
    df_final = df_staff_all[['EmployeeID', 'FirstName', \
        'MiddleName', 'LastName', 'EmailAddress', 'EmployeeID', \
        'Dob', 'HR_Gender', 'HR_Location']].copy()
    ###Add staff type to dataframe
    #Can be set to 'General' for all non-Nutrition workers
    df_final['StaffType'] = 'General'
    ###Add Staff Assignment Date (Staff Date)
    df_final['AssignmentStart'] = staff_date
    ###Drop Staff with No Location
    df_final = df_final[df_final['HR_Location'] != '320']
    ###Drop Duplicates
    df_final.drop_duplicates('EmployeeID', inplace=True)
    ###Export to data to csv file
    df_final.to_csv(staff_final_file, 
                    quoting=csv.QUOTE_ALL,
                    index=False)
    #######
    ###Log Entry###
    log_entry += "---------------------------------\n"
    log_entry += "Titan Staff File Script Completed\n"
    log_entry += "---------------------------------\n"
    #######
    return log_entry

if __name__ == '__main__':
    log_entry = titan_staff_file_generator()
    print(log_entry)