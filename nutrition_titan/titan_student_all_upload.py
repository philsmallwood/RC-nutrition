#!/usr/bin/env python3
###RC Titan Student File Script
###Script to generate a student file with the necesary info for nturition
###Requires time, pandas, keyring, and pysftp to be installed
###For keyring, need to set the username/password for sftp sites for downloads and uploads
###Includes Red Clay and Charter students

###Import Modules###
import pandas as pd
import keyring
import pysftp
import time
import os
import sys
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

###Set variables for script###
startTime = time.ctime()
DOEHostname = "ftp.doe.k12.de.us"
DOEUsername = "RedClayData"
UMRAHostname = "rcit-umra.redclay.k12.de.us"
UMRAUsername = "Philip.Smallwood"
titanHostname = "sftp.titank12.com"
titanUsername = "RCCSD"
nutritionHostname ="10.222.2.70"
nutritionUsername = "philip.smallwood"
remoteStudentFilePath = '/Cognos/Titan-en.xlsx'
localStudentFilePath = './Titan-en.xlsx'
remoteSecondaryStudentFilePath = '/Cognos/SecondaryNutrition-en.csv'
localSecondaryStudentFilePath = './SecondaryNutrition-en.csv'
remoteAllergyFilePath = '/Allergies/StudentAllergies.csv'
localAllergyFilePath = './Allergies.csv'
localUpFilePath = './rc_titan_student.csv'
remoteUpFilePath = '/rc_titan_student.csv'
logFile = "/var/log/scripts/titan_student_upload.log"
dropColumnsCharter = {4, 7, 9, 10, 11, 12, 15, 16, 17, 26, 27, 28, 29, 30, 31, 32}

###Set dictionary to rename columns
###Secondary Dataframe
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

###Charter Dateframe
colNamesCharter = { 0 : 'Student Id', 
            2 : 'Student First Name', 
            1 : 'Student Last Name', 
            3 : 'Student Middle Name', 
            5 : 'Current Building',
            6 : 'Student Grade', 
            14 : 'Federal Race Code', 
            13 : 'Student Gender', 
            18 : 'City - Physical',
            19 : 'State - Physical', 
            20 : 'Zip - Physical', 
            8 : 'Student Homeroom Primary', 
            23 : 'First Name - Guardian', 
            22 : 'Last Name - Guardian',
            24 : 'Middle Name - Guardian',
            21 : 'Home Phone', 
            25 : 'Work Phone'}
#######

###Download Files###
###Get Titan Cognos Report from DOE SFTP
with pysftp.Connection(host=DOEHostname, username=DOEUsername, password=keyring.get_password("RCDOE", "RedClayData")) as sftp:
    sftp.get(remoteStudentFilePath, localStudentFilePath)

###Get Secondary Cognos Report from DOE SFTP
with pysftp.Connection(host=DOEHostname, username=DOEUsername, password=keyring.get_password("RCDOE", "RedClayData")) as sftp:
    sftp.get(remoteSecondaryStudentFilePath, localSecondaryStudentFilePath) 

###Get Allergies file from UMRA server
with pysftp.Connection(host=UMRAHostname, username=UMRAUsername, password=keyring.get_password("UMRA", "Philip.Smallwood")) as sftp:
    sftp.get(remoteAllergyFilePath, localAllergyFilePath)
###Get Charter School Files
###NOTE: need to get these streamlined into COGNOS
with pysftp.Connection(host=nutritionHostname, username=nutritionUsername, password=keyring.get_password('NUTRITIONSERVER', nutritionUsername)) as sftp:
    sftp.cwd('dailyenrollment')
    files = sftp.listdir()
    for file in files: 
        if (file[-3:]=='txt'):
            sftp.get(file)
            sftp.remove(file)
######

###Read Files into Dataframes###
##Read Titan Cognos report with Student Data to dataframe
df_students = pd.read_excel(localStudentFilePath, dtype=str)

##Read Secondary Cognos report with Student Data to dataframe
df_students_other = pd.read_csv(localSecondaryStudentFilePath, encoding='cp1252', dtype=str)

##Combine Charter school files into one file
os.system("cat *.txt >> chartercombined.csv")
df_students_charters = pd.read_csv('chartercombined.csv', header=None, dtype=str)

###Read Allergies file to dataframe
df_allergies = pd.read_csv(localAllergyFilePath, dtype=str)
###Rename the StudentID field in allergies dataframe
df_allergies.rename(columns={'StudentID':'Student Id'}, inplace=True)
#######

###Format Charter schools dataframe###
###Create Birthdate column from month, day, year columns
df_students_charters['Birthdate'] = df_students_charters[9].astype(str) + '/' + df_students_charters[10].astype(str) + '/20' + df_students_charters[11].astype(str)
###Combine Street Address Line 1 and Apartment to match other sources
df_students_charters['Street Addr Line & Apt - Physical'] = df_students_charters[[16, 17]].apply(lambda x: ', '.join(x.dropna()), axis=1)
###Rename the columns to match other sources for later merging
df_students_charters.rename(columns=colNamesCharter, inplace=True)
###Drop columns that are not needed
df_students_charters.drop(columns = dropColumnsCharter, inplace=True)
###Change Charter Race codes to match Federal Race codes
df_students_charters.loc[df_students_charters['Federal Race Code'] == '6', ['Federal Race Code']] = '3' #Asian
df_students_charters.loc[df_students_charters['Federal Race Code'] == '5', ['Federal Race Code']] = '6' #Caucasian
df_students_charters.loc[df_students_charters['Federal Race Code'] == '2', ['Federal Race Code']] = '4' #Black/African
df_students_charters.loc[df_students_charters['Federal Race Code'] == '1', ['Federal Race Code']] = '2' #American Indian/Alaskan


###Format Secondary file###
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
########

###Format Main Student dataframe###
###Swap Current and Alternate Building for special programs
###NOTE: 07/14/2021
###Programs Affected - Meadowood and Early Years
##Meadowood
df_students.loc[df_students['Alternate Building Name'] == 'Forest Oak Elementary School', ['Current Building', 'Alternate Building']] = '320240', '320516'
df_students.loc[df_students['Alternate Building Name'] == 'H.B. duPont Middle School', ['Current Building', 'Alternate Building']] = '320276', '320516'
df_students.loc[df_students['Alternate Building Name'] == 'McKean High School', ['Current Building', 'Alternate Building']] = '320294', '320516'
##Early Years
df_students.loc[df_students['Alternate Building Name'] == 'Meadowood Program', ['Current Building', 'Alternate Building']] = '320516', '320529'
df_students.loc[df_students['Alternate Building Name'] == 'Mote Elementary School', ['Current Building', 'Alternate Building']] = '320264', '320529'
df_students.loc[df_students['Alternate Building Name'] == 'Richardson Park Learning Center', ['Current Building', 'Alternate Building']] = '320254', '320529'
df_students.loc[df_students['Alternate Building Name'] == 'Warner Elementary School', ['Current Building', 'Alternate Building']] = '320266', '320529'
df_students.loc[df_students['Alternate Building Name'] == 'Wm. C. Lewis Dual Language Elem.', ['Current Building', 'Alternate Building']] = '320246', '320529'
###Drop Z calendar (320888) and First State School (320530) students
df_studentsno888 = df_students[df_students['Current Building'] != '320888']
df_studentsno530or888 = df_studentsno888[df_studentsno888['Current Building'] != '320530']
###Drop extra column at the end
#df_final = df_no530or888.drop(columns = ['Alternate Building Name'])
###Holding on dropping this until 09/01/2021
df_studentsno530or888.loc[df_studentsno530or888['Alternate Building Name'] != 'a', ['Alternate Building Name']] = '8/31/2021'
#########

###Add students from Secondary Student and Charter dataframes that are not in the Titan file###
df_students_combined = df_studentsno530or888.merge(df_students_noguard, how = 'outer')
df_students_combined_charters = df_students_combined.merge(df_students_charters, how = 'outer')
######

###Final Prep and Upload### 
###Add Allergies into main file
df_studentallergies = df_students_combined_charters.merge(df_allergies[['Student Id', 'Allergies']], on = 'Student Id', how = 'left')

###Reorder to final form
df_final = df_studentallergies[['Student Id', 'Student First Name', 'Student Middle Name', 'Student Last Name', 'Student Generation', 'Allergies', 'Birthdate', 'Student Gender', 'Federal Race Code', 'Hispanic/Latino Ethnicity', 'Alternate Building', 'Current School Year', 'Current Building', 'Student Grade', 'Student Homeroom Primary', 'Street Addr Line & Apt - Physical', 'City - Physical', 'State - Physical', 'Zip - Physical', 'Street Addr Line & Apt - Mailing', 'City - Mailing', 'State - Mailing', 'Zip - Mailing', 'First Name - Guardian', 'Middle Name - Guardian', 'Last Name - Guardian', 'Mobile Phone', 'Home Phone', 'Work Phone', 'Email - Guardian', 'Relation Name - Guardian', 'Alternate Building Name']]

###Create Household ID based on Street Address
df_final['HHID'] = df_final['Street Addr Line & Apt - Physical'].map(hash)
###Make HouseHold ID shorter
df_final['HHID'] = df_final['HHID'].astype(str).str[1:9]

###Section for Urban Promise
###We sporadically get files from Urban Promise
###Adding logic to check before adding and exporting
if os.path.exists('urbanpromise'):
    df_urbanpromise = pd.read_csv('urbanpromise', dtype=str)
    df_allstudents = df_final.merge(df_urbanpromise, how = 'outer')
    df_allstudents.to_csv(localUpFilePath, index=False)
else:    
###Export to data to csv file if no urban promise file
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
#os.system("python3 mailsend.py 'philip.smallwood@redclay.k12.de.us' 'File Successfully Uploaded to Titan' '/var/log/scripts/titan_student_upload.log' ")

###Move Uploaded File to archive
os.rename(localUpFilePath,time.strftime("/archive/%Y%m%d%H%M%S-TitanStudentFile.csv"))

###Remove downloaded files
fileToDelete = os.listdir()
for file in fileToDelete: 
    if (file[-3:]=='txt') or (file[-3:]=='csv') or (file[-4:]=='xlsx'):
        os.remove(file)
########
