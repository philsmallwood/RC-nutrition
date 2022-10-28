#!/usr/bin/env python3
###RC Titan Student File Generator Script
###Script to generate a student file with the necesary info for nturition
###Requires time, pandas, datetime, 
###and rcmailsend(self-created package) to be installed
###Includes Red Clay and Charter students

###Import Modules###
import pandas as pd
import time
import os
import sys
from datetime import date
from dotenv import load_dotenv
from dfcleanup import df_stripper #Self Created Module
#######

###Turns off the hashseed randomization###
###Used to ensure that people with the same address get the same household ID
###everytime the script runs
hashseed = os.getenv('PYTHONHASHSEED')
if not hashseed:
    os.environ['PYTHONHASHSEED'] = '0'
    os.execv(sys.executable, [sys.executable] + sys.argv)
#######

#####Variables#####
#Load .ENV File
load_dotenv()
#Date
CurrentDate = date.today()
Date = CurrentDate.strftime('%m-%d-%Y')
StudentDate = CurrentDate.strftime('%m/%d/%Y')
startTime = time.ctime()
earliestEnrollmentDate = '08/29/2022'
#File Locations
localStudentFilePath = os.getenv('localStudentFilePath')
localCharterStudentFilePath = os.getenv('localCharterStudentFilePath')
localUrbanPromiseFilePath = os.getenv('localUrbanPromiseFilePath')
localAllergyFilePath = os.getenv('localAllergyFilePath')
localStudentLanguageFilePath = os.getenv('localStudentLanguageFilePath')
localUpFilePath = os.getenv('localUpStudentFilePath')
logFile = os.getenv('logFilePath') + "Titan-" + Date + ".log"
dropColumnsCharter = {1, 6, 10, 11, 13, 15, 16, 19, 20, 30, 31, 32, 33, 34, 35}
###Set dictionary to rename columns
##Charter Dateframe
colNamesCharter = { 
            0 : 'Student Building',
            2 : 'Student Id',
            3 : 'Student Last Name',
            4 : 'Student First Name', 
            5 : 'Student Middle Name', 
            7 : 'Student Gender',
            8 : 'Student Homeroom Primary',
            9 : 'Student Grade', 
            12 : 'Birthdate',
            14 : 'Email - Guardian',
            17 : 'Federal Race Code',
            18 : 'Hispanic/Latino Ethnicity',
            21 : 'City - Physical',
            22 : 'State - Physical', 
            23 : 'Zip - Physical', 
            24 : 'First Name - Guardian', 
            25 : 'Last Name - Guardian',
            26 : 'Middle Name - Guardian',
            27 : 'Home Phone', 
            28 : 'Mobile Phone',
            29 : 'Work Phone'}
##Urban Promise Dateframe
colNamesUrbanPromise = { 
            0 : 'Student Building',
            1 : 'Student Id',
            2 : 'Student First Name',
            3 : 'Student Last Name',
            4 : 'Student Grade',
            5 : 'Birthdate',
            6 : 'Allergies',
            7 : 'Street Addr Line & Apt - Physical',
            8 : 'City - Physical',
            9 : 'State - Physical',
            10 : 'Zip - Physical'}
##Allergies Dataframe
colNamesAllergies = {
    'StudentID':'Student Id'
}
##Language Dataframe
colNamesLanguage = {
    0 : 'Student Id', 
    1 : 'Student Language'
}
############

#####Read Files into Dataframes#####
##Read RC Student File to Dataframe
df_RCstudents = pd.read_csv(localStudentFilePath, dtype=str)
df_RCstudents = df_stripper(df_RCstudents)
##Read Charter School File to Dataframe
df_CharterStudents = pd.read_csv(localCharterStudentFilePath, header=None, skiprows=1, dtype=str, on_bad_lines='skip')
df_CharterStudents = df_stripper(df_CharterStudents)
##Read Urban Promise File to Dataframe
#Format Can Be Excel or CSV
try:
    df_UrbanPromise = pd.read_excel(localUrbanPromiseFilePath, skiprows=1, header=None, dtype=str)
    df_UrbanPromise = df_stripper(df_UrbanPromise)
except:
    df_UrbanPromise = pd.read_csv(localUrbanPromiseFilePath, skiprows=1, header=None, dtype=str)
    df_UrbanPromise = df_stripper(df_UrbanPromise)
###Read Allergies File to Dataframe
df_Allergies = pd.read_csv(localAllergyFilePath, dtype=str)
#Rename the StudentID Field in Allergies DataFrame
df_Allergies.rename(columns=colNamesAllergies, inplace=True)
###Read Language File to Dataframe
df_Languages = pd.read_csv(localStudentLanguageFilePath, dtype=str, header=None, skiprows=1 )
#Rename the StudentID Field in Languages DataFrame
df_Languages.rename(columns=colNamesLanguage, inplace=True)
############

###Format Charter schools dataframe###
###Combine Street Address Line 1 and Apartment to match other sources
df_CharterStudents['Street Addr Line & Apt - Physical'] = df_CharterStudents[[19, 20]].apply(lambda x: ', '.join(x.dropna()), axis=1)
###Rename the columns to match other sources for later merging
df_CharterStudents.rename(columns=colNamesCharter, inplace=True)
###Drop columns that are not needed
df_CharterStudents.drop(columns = dropColumnsCharter, inplace=True)
###Change Charter Race codes to match Federal Race codes
df_CharterStudents.loc[df_CharterStudents['Federal Race Code'] == 'Asian', \
    ['Federal Race Code']] = '3' #Asian
df_CharterStudents.loc[df_CharterStudents['Federal Race Code'] == 'White', \
    ['Federal Race Code']] = '6' #Caucasian
df_CharterStudents.loc[df_CharterStudents['Federal Race Code'] == 'Black', \
    ['Federal Race Code']] = '4' #Black/African
df_CharterStudents.loc[df_CharterStudents['Federal Race Code'] == 'Native Am.', \
    ['Federal Race Code']] = '2' #American Indian/Alaskan
df_CharterStudents.loc[df_CharterStudents['Federal Race Code'] == 'Hawaiian', \
    ['Federal Race Code']] = '5' #Native Hawaiian/Other Pacific Islander
###Change Ethnicity to Y or N
df_CharterStudents.loc[df_CharterStudents['Hispanic/Latino Ethnicity'] == 'Hispanic', \
    ['Hispanic/Latino Ethnicity']] = 'Y' #Hispanic
df_CharterStudents.loc[df_CharterStudents['Hispanic/Latino Ethnicity'] == 'Non-Hispanic', \
    ['Hispanic/Latino Ethnicity']] = 'N' #Hispanic
############

###Format Urban Promise dataframe###
df_UrbanPromise = df_UrbanPromise.loc[df_UrbanPromise[0] == '5544']
###Fix date format by making object a 'datetime' format and setting output
df_UrbanPromise[5] = pd.to_datetime(df_UrbanPromise[5])
df_UrbanPromise[5] = df_UrbanPromise[5].dt.strftime('%m/%d/%Y')
###Add leading zeros to studentID to ensure 6 digits exactly
df_UrbanPromise[1] = df_UrbanPromise[1].str.zfill(6)
###Add leading zeros to Grade to ensure 2 digits exactly
df_UrbanPromise[4] = df_UrbanPromise[4].str.zfill(2)
###Fix Kindergarten Grade
df_UrbanPromise[4] = df_UrbanPromise[4].str.replace('0K','KN')
###Rename columns for final output
df_UrbanPromise.rename(columns=colNamesUrbanPromise, inplace=True)
############

###Format Main Student dataframe###
###Drop Z calendar (320888) and First State School (320530) students
df_RCstudentsno530or888 = df_RCstudents[ (df_RCstudents['Current Building'] != '888') & \
    (df_RCstudents['Current Building'] != '530') ]
df_RCstudentsno530or888['Student Building'] = '320' + df_RCstudentsno530or888['Current Building']
############

###Combine all of the Dataframes###
##Add allergies for RC Students to Main
df_RCStudents_Allergies = df_RCstudentsno530or888.merge(df_Allergies[['Student Id', 'Allergies']], \
    on = 'Student Id', how = 'left')
##Add Languages for RC Students to Main
df_RCStudents_Allergies_Lang = df_RCStudents_Allergies.merge(df_Languages[['Student Id', 'Student Language']], \
    on = 'Student Id', how = 'left')
##Add Charter Students to Main
df_RCstudents_Charters = df_RCStudents_Allergies_Lang.merge(df_CharterStudents, how = 'outer')
##Add Urban Promise Students to Main
df_AllStudents = df_RCstudents_Charters.merge(df_UrbanPromise, how = 'outer')
############

###Final Prep and Upload### 
###Reorder to Final Data Frame
df_final = df_AllStudents[['Student Id', 'Student First Name', 'Student Middle Name', \
    'Student Last Name', 'Student Generation', 'Allergies', 'Birthdate', 'Student Gender', \
    'Federal Race Code', 'Hispanic/Latino Ethnicity', 'Alternate Building', \
    'Current School Year', 'Student Building', 'Student Grade', 'Student Homeroom Primary', \
    'Street Addr Line & Apt - Physical', 'City - Physical', 'State - Physical', 'Zip - Physical', \
    'Street Addr Line & Apt - Mailing', 'City - Mailing', 'State - Mailing', 'Zip - Mailing', \
    'First Name - Guardian', 'Middle Name - Guardian', 'Last Name - Guardian', 'Mobile Phone', \
    'Home Phone', 'Work Phone', 'Email - Guardian', 'Relation Name - Guardian', 'Student Language']]

###Create Household ID based on Street Address
df_final['HHID'] = df_final['Street Addr Line & Apt - Physical'].map(hash)
###Make HouseHold ID shorter
df_final['HHID'] = df_final['HHID'].astype(str).str[1:16]

###Copy Physical Address to Mailing Address if Blank
df_final['Street Addr Line & Apt - Mailing'].fillna(df_final['Street Addr Line & Apt - Physical'], inplace=True)
df_final['City - Mailing'].fillna(df_final['City - Physical'], inplace=True)
df_final['State - Mailing'].fillna(df_final['State - Physical'], inplace=True)
df_final['Zip - Mailing'].fillna(df_final['Zip - Physical'], inplace=True)

###Fill Guardian Relationship as Guardian if Blank
df_final['Relation Name - Guardian'].fillna('Guardian', inplace=True)

###Add Entry Date
##Use the earliest Entry Date if it is before that date
##Otherwise, use the current date
if earliestEnrollmentDate > StudentDate:
    df_final['Enrollment Date'] = earliestEnrollmentDate
else:
    df_final['Enrollment Date'] = StudentDate

###Export to data to csv file
df_final.to_csv(localUpFilePath, index=False)
############


