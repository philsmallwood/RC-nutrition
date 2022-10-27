#!/usr/bin/env python3
###RC Titan Staff File Script
###Script to generate a student file with the necesary info for nutrition
###Requires time, pandas, keyring, and pysftp to be installed
###For keyring, need to set the username/password for sftp sites for downloads and uploads


###Import Modules
import pandas as pd
from datetime import date
from dfcleanup import df_stripper #Self Created Module
#######


###Variables###
#Date
CurrentDate = date.today()
Date = CurrentDate.strftime('%m-%d-%Y')
#Files
localStaffFile = '/uploads/DSC/HR/RedClayStaff.csv'
localStaffEmailFile = '/uploads/RC/staffIDtoGoogle.csv'
localContractorFile = '/uploads/RC/Contractor_Phone.csv'
localUpFilePath = '/uploads/RC/rc_titan_staff.csv'
###Set Dictionaries to Rename Columns
colNamesStaff = { 0 : 'EmployeeID', 
            1 : 'LastName',
            2 : 'FirstName',
            3 : 'MiddleName',
            4 : 'Dob',
            7 : 'HR_Location',
            14 : 'HR_Gender'}
colNamesEmail = { 0 : 'EmployeeID',
            1 : 'EmailAddress'}
colNamesContractors = { 0 : 'EmployeeID', 
            1 : 'FirstName',
            2 : 'MiddleName',
            3 : 'LastName',
            9 : 'Dob',
            7 : 'EmailAddress',
            8 : 'HR_Location'}
#######

#####Read Files into Dataframes#####    
###Read Staff File into Dataframe
df_staff = pd.read_csv(localStaffFile, skiprows=1, header=None, dtype=str)
df_staff = df_stripper(df_staff)
df_staff.rename(columns=colNamesStaff, inplace=True)
###Read Email File into Dataframe
df_email = pd.read_csv(localStaffEmailFile, skiprows=1, header=None, dtype=str)
df_email = df_stripper(df_email)
df_email.rename(columns=colNamesEmail, inplace=True)
###Read Contractor File into Dataframe
df_contractors = pd.read_csv(localContractorFile, skiprows=1, header=None, dtype=str)
df_contractors = df_stripper(df_contractors)
df_contractors.rename(columns=colNamesContractors, inplace=True)
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
df_final = df_staff_all[['EmployeeID', 'FirstName', 'MiddleName', \
    'LastName', 'EmailAddress', 'EmployeeID', 'Dob', 'HR_Gender', 'HR_Location']]
###Add staff type to dataframe
#Can be set to 'General' for all non-Nutrition workers
df_final['StaffType'] = 'General'
###Add Staff Assignment Date (Current Date)
df_final['AssignmentStart'] = Date
###Export to data to csv file
df_final.to_csv(localUpFilePath, index=False)
#######