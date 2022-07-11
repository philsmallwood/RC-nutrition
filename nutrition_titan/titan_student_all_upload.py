#!/usr/bin/env python3
###RC Titan Student File Script
###Script to generate a student file with the necesary info for nturition
###Requires time, pandas, keyring, datetime, glob, and pysftp to be installed
###For keyring, need to set the username/password for sftp sites for downloads and uploads
###Includes Red Clay and Charter students

###Import Modules###
import pandas as pd
import keyring
import pysftp
import time
import os
import sys
from datetime import date
#######

###Turns off the hashseed randomization###
###Used to ensure that people with the same address get the same household ID
###everytime the script runs
hashseed = os.getenv('PYTHONHASHSEED')
if not hashseed:
    os.environ['PYTHONHASHSEED'] = '0'
    os.execv(sys.executable, [sys.executable] + sys.argv)
#######

###Change location###
###Change to the working directory in which script is located
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
#######

#####Variables#####
startTime = time.ctime()
titanHostname = "sftp.titank12.com"
titanUsername = "RCCSD"
localStudentFilePath = '/uploads/DOE/student_master_primary-en.csv'
localSecondaryStudentFilePath = '/uploads/DOE/student_master_secondary-en.csv'
localCharterStudentFilePath = '/uploads/DSC/Follet/destinystudentsCharter.csv'
localUrbanPromiseFilePath = '/RC-scripts/nutrition_titan/urbanpromisecurrent'
localAllergyFilePath = '/uploads/DSC/Allergies/StudentAllergies.csv'
localUpFilePath = '/RC-scripts/nutrition_titan/rc_titan_student.csv'
remoteUpFilePath = '/rc_titan_student.csv'
logFile = "/var/log/scripts/titan_student_upload.log"
dropColumnsCharter = {1, 6, 10, 11, 13, 15, 16, 19, 20, 30, 31, 32, 33, 34, 35}
earliestEnrollmentDate = '08/31/2022'
today = date.today()
todayStr = today.strftime("%m/%d/%Y")
###Set dictionary to rename columns
##Secondary Dataframe
colNames = {'Student ID': 'Student Id', 
            'First Name': 'Student First Name', 
            'Last Name': 'Student Last Name', 
            'Middle Name': 'Student Middle Name', 
            'Birth Date': 'Birthdate',
            'School Code': 'Current Building',
            'Grade': 'Student Grade', 
            'Ethnicity': 'Hispanic/Latino Ethnicity', 
            'Race': 'Federal Race Code', 
            'Gender': 'Student Gender', 
            'City': 'City - Physical',
            'State': 'State - Physical', 
            'Zip': 'Zip - Physical', 
            'Homeroom': 'Student Homeroom Primary', 
            'Guardian First Name': 'First Name - Guardian', 
            'Guardian Last Name': 'Last Name - Guardian',
            'Home Phone Number': 'Home Phone', 
            'Guardian Work Phone Number': 'Work Phone', 
            'Email': 'Email - Guardian' }
##Charter Dateframe
colNamesCharter = { 0 : 'Current Building', 
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
colNamesUrbanPromise = { 0 : 'Current Building', 
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
############

#####Read Files into Dataframes#####
##Read Main Cognos report with Student Data to dataframe
df_students = pd.read_csv(localStudentFilePath, encoding='cp1252', dtype=str)
##Read Secondary Cognos report with Student Data to dataframe
df_students_other = pd.read_csv(localSecondaryStudentFilePath, encoding='cp1252', dtype=str)
##Read Charter School file into dataframe
df_students_charters = pd.read_csv(localCharterStudentFilePath, header=None, skiprows=1, dtype=str)
##Read Urban Promise file into dataframe
df_urbanpromise = pd.read_excel('urbanpromisecurrent', skiprows=1, header=None, dtype=str)
###Read Allergies file to dataframe
df_allergies = pd.read_csv(localAllergyFilePath, dtype=str)
###Rename the StudentID field in allergies dataframe
df_allergies.rename(columns={'StudentID':'Student Id'}, inplace=True)
############

###Format Charter schools dataframe###
###Combine Street Address Line 1 and Apartment to match other sources
df_students_charters['Street Addr Line & Apt - Physical'] = df_students_charters[[19, 20]].apply(lambda x: ', '.join(x.dropna()), axis=1)
###Rename the columns to match other sources for later merging
df_students_charters.rename(columns=colNamesCharter, inplace=True)
###Drop columns that are not needed
df_students_charters.drop(columns = dropColumnsCharter, inplace=True)
###Change Charter Race codes to match Federal Race codes
df_students_charters.loc[df_students_charters['Federal Race Code'] == 'Asian', \
    ['Federal Race Code']] = '3' #Asian
df_students_charters.loc[df_students_charters['Federal Race Code'] == 'White', \
    ['Federal Race Code']] = '6' #Caucasian
df_students_charters.loc[df_students_charters['Federal Race Code'] == 'Black', \
    ['Federal Race Code']] = '4' #Black/African
df_students_charters.loc[df_students_charters['Federal Race Code'] == 'Native Am.', \
    ['Federal Race Code']] = '2' #American Indian/Alaskan
df_students_charters.loc[df_students_charters['Federal Race Code'] == 'Hawaiian', ['Federal Race Code']] = '5' #Native Hawaiian/Other Pacific Islander
###Change Ethnicity to Y or N
df_students_charters.loc[df_students_charters['Hispanic/Latino Ethnicity'] == 'Hispanic', ['Hispanic/Latino Ethnicity']] = 'Y' #Hispanic
df_students_charters.loc[df_students_charters['Hispanic/Latino Ethnicity'] == 'Non-Hispanic', ['Hispanic/Latino Ethnicity']] = 'N' #Hispanic
############

###Format Urban Promise dataframe###
df_urbanpromise[1].fillna('5544-' + df_urbanpromise[2] + df_urbanpromise[3], inplace=True)
###Add leading zeros to teacherid to ensure 6 digits exactly
df_urbanpromise[1] = df_urbanpromise[1].apply(lambda x: '{0:0>6}'.format(x))
###Fix date format by making object a 'datetime' format and setting output
df_urbanpromise[5] = pd.to_datetime(df_urbanpromise[5])
df_urbanpromise[5] = df_urbanpromise[5].dt.strftime('%m/%d/%Y')
###Rename columns for final output
df_urbanpromise.rename(columns=colNamesUrbanPromise, inplace=True)
############

###Format Secondary file dataframe###
###Rename the columns to match other sources for later merging
df_students_other.rename(columns=colNames, inplace=True)
###Add '320' to the building code to match other sources
df_students_other['Current Building'] = '320' + df_students_other['Current Building'].astype(str)
###Combine Street Address Line 1 and Apartment to match other sources
df_students_other['Street Addr Line & Apt - Physical'] = df_students_other[['Street Address Line 1', 'Apartment']].apply(lambda x: ', '.join(x.dropna()), axis=1)
###Drop Address Line 1, Address Line2, and Apartment
df_students_other.drop(columns = ['Street Address Line 1', 'Street Address Line 1', 'Apartment'], inplace=True)
###Remove Students from Secondary file that are in the Main file
df_students_noguard = (df_students_other[~df_students_other['Student Id'].isin(df_students['Student Id'])])
############

###Format Main Student dataframe###
###Swap Current and Alternate Building for special programs
###Programs Affected - Meadowood and Early Years
##Meadowood
df_students.loc[(df_students['Alternate Building'] == '320240') & \
    (df_students['Current Building'] == '320516'), ['Current Building', 'Alternate Building']] = '320240', '320516'
df_students.loc[(df_students['Alternate Building'] == '320276') & \
    (df_students['Current Building'] == '320516'), ['Current Building', 'Alternate Building']] = '320276', '320516'
df_students.loc[(df_students['Alternate Building'] == '320294') & \
    (df_students['Current Building'] == '320516'), ['Current Building', 'Alternate Building']] = '320294', '320516'
##Early Years
df_students.loc[(df_students['Alternate Building'] == '320516') & \
    (df_students['Current Building'] == '320529'), ['Current Building', 'Alternate Building']] = '320516', '320529'
df_students.loc[(df_students['Alternate Building'] == '320264') & \
    (df_students['Current Building'] == '320529'), ['Current Building', 'Alternate Building']] = '320264', '320529'
df_students.loc[(df_students['Alternate Building'] == '320254') & \
    (df_students['Current Building'] == '320529'), ['Current Building', 'Alternate Building']] = '320254', '320529'
df_students.loc[(df_students['Alternate Building'] == '320266') & \
    (df_students['Current Building'] == '320529'), ['Current Building', 'Alternate Building']] = '320266', '320529'
df_students.loc[(df_students['Alternate Building'] == '320246') & \
    (df_students['Current Building'] == '320529'), ['Current Building', 'Alternate Building']] = '320246', '320529'
###Drop Z calendar (320888) and First State School (320530) students
df_studentsno888 = df_students[df_students['Current Building'] != '320888']
df_studentsno530or888 = df_studentsno888[df_studentsno888['Current Building'] != '320530']
############

###Combine all of the Dataframes###
df_students_combined = df_studentsno530or888.merge(df_students_noguard, how = 'outer')
df_students_combined_charters = df_students_combined.merge(df_students_charters, how = 'outer')
df_allstudents = df_students_combined_charters.merge(df_urbanpromise, how = 'outer')
############

###Final Prep and Upload### 
###Add Allergies into main file
df_allstudents_allergies = df_allstudents.merge(df_allergies[['Student Id', 'Allergies']], on = 'Student Id', how = 'left')

###Reorder to Final Data Frame
df_final = df_allstudents_allergies[['Student Id', 'Student First Name', 'Student Middle Name', \
    'Student Last Name', 'Student Generation', 'Allergies', 'Birthdate', 'Student Gender', \
    'Federal Race Code', 'Hispanic/Latino Ethnicity', 'Alternate Building', \
    'Current School Year', 'Current Building', 'Student Grade', 'Student Homeroom Primary', \
    'Street Addr Line & Apt - Physical', 'City - Physical', 'State - Physical', 'Zip - Physical', \
    'Street Addr Line & Apt - Mailing', 'City - Mailing', 'State - Mailing', 'Zip - Mailing', \
    'First Name - Guardian', 'Middle Name - Guardian', 'Last Name - Guardian', 'Mobile Phone', \
    'Home Phone', 'Work Phone', 'Email - Guardian', 'Relation Name - Guardian']]

###Create Household ID based on Street Address
df_final['HHID'] = df_final['Street Addr Line & Apt - Physical'].map(hash)
###Make HouseHold ID shorter
df_final['HHID'] = df_final['HHID'].astype(str).str[1:9]

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
if earliestEnrollmentDate > todayStr:
    df_final['Enrollment Date'] = earliestEnrollmentDate
else:
    df_final['Enrollment Date'] = todayStr

###Export to data to csv file
    df_final.to_csv(localUpFilePath, index=False)

###Upload file to Titan
#with pysftp.Connection(host=titanHostname, username=titanUsername, password=keyring.get_password("TITANK12", "RCCSD")) as sftp:
#    sftp.put(localUpFilePath, remoteUpFilePath)


###Logging
f = open(logFile, "a")
f.write("------------------\n")
f.write("The Titan student upload script ran on " + startTime + "\n")
f.write("------------------\n")
f.close()

###Email Results
os.system("python3 /usr/local/bin/mailsend.py 'philip.smallwood@redclay.k12.de.us' 'File Successfully Uploaded to Titan' '/var/log/scripts/titan_student_upload.log' ")

###Move Uploaded File to archive
#os.rename(localUpFilePath,time.strftime("/archive/%Y%m%d%H%M%S-TitanStudentFile.csv"))


########
