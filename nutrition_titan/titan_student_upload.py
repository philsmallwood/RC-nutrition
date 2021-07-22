#!/usr/bin/env python3
###RC Titan Student File Script
###Script to generate a student file with the necesary info for nturition
###Requires time, pandas, keyring, and pysftp to be installed
###For keyring, need to set the username/password for sftp sites for downloads and uploads


###Import Modules
import pandas as pd
import keyring
import pysftp
import time
import os

###Change working directory in which script is located
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

###Set variables for script
startTime = time.ctime()
DOEHostname = "ftp.doe.k12.de.us"
DOEUsername = "colonialdata"
UMRAHostname = "rcit-umra.redclay.k12.de.us"
UMRAUsername = "Philip.Smallwood"
titanHostname = "sftp.titank12.com"
titanUsername = "RCCSD"
remoteStudentFilePath = '/Cognos/Titan-en.xlsx'
localStudentFilePath = './Titan-en.xlsx'
remoteAllergyFilePath = '/Allergies/StudentAllergies.csv'
localAllergyFilePath = './Allergies.csv'
localUpFilePath = './rc_titan_student.csv'
remoteUpFilePath = '/rc_titan_student.csv'
logFile = "/var/log/scripts/titan_student_upload.log"

###Get Titan Cognos Report from DOE SFTP
##NOTE: 7/7/2021 - need to change to RedClay instance when have correct access
with pysftp.Connection(host=DOEHostname, username=DOEUsername, password=keyring.get_password("COLDOE", "colonialdata")) as sftp:
    sftp.get(remoteStudentFilePath, localStudentFilePath)
    
###Get Allergies file from UMRA server
with pysftp.Connection(host=UMRAHostname, username=UMRAUsername, password=keyring.get_password("UMRA", "Philip.Smallwood")) as sftp:
    sftp.get(remoteAllergyFilePath, localAllergyFilePath)
    

###Read Cognos report with Student Data to dataframe
df_students = pd.read_excel(localStudentFilePath, dtype=str)

###Read Allergies file to dataframe
df_allergies = pd.read_csv(localAllergyFilePath, dtype=str)

###Rename the StudentID field in allergies dataframe
df_allergies.rename(columns={'StudentID':'Student Id'}, inplace=True)


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
###Holding on dropping this until 09/01/2021
df_studentsno530or888.loc[df_studentsno530or888['Alternate Building Name'] != 'a', ['Alternate Building Name']] = '8/31/2021'


#df_final = df_no530or888.drop(columns = ['Alternate Building Name'])

###Add Allergies into main file
df_studentallergies = df_studentsno530or888.merge(df_allergies[['Student Id', 'Allergies']], on = 'Student Id', how = 'left')

###Reorder to final form
df_final = df_studentallergies[['Student Id', 'Student First Name', 'Student Middle Name', 'Student Last Name', 'Student Generation', 'Allergies', 'Birthdate', 'Student Gender', 'Federal Race Code', 'Hispanic/Latino Ethnicity', 'Alternate Building', 'Current School Year', 'Current Building', 'Student Grade', 'Student Homeroom Primary', 'Street Addr Line & Apt - Physical', 'City - Physical', 'State - Physical', 'Zip - Physical', 'Street Addr Line & Apt - Mailing', 'City - Mailing', 'State - Mailing', 'Zip - Mailing', 'First Name - Guardian', 'Middle Name - Guardian', 'Last Name - Guardian', 'Mobile Phone', 'Home Phone', 'Work Phone', 'Email - Guardian', 'Relation Name - Guardian', 'Alternate Building Name']]


###Export to data to csv file
df_final.to_csv(localUpFilePath, index=False)

###Upload file to Titan
with pysftp.Connection(host=titanHostname, username=titanUsername, password=keyring.get_password("TITANK12", "RCCSD")) as sftp:
    sftp.put(localUpFilePath, remoteUpFilePath)


###Logging
f = open(logFile, "a")
f.write("------------------\n")
f.write("The Titan student upload script ran on " + startTime + "\n")
f.write("------------------\n")
f.close()

###Email Results
os.system("python mailsend.py 'technology@redclay.k12.de.us' 'philip.smallwood@redclay.k12.de.us' 'logFile'")

###Remove downloaded files
os.remove(localStudentFilePath)
os.remove(localAllergyFilePath)
#os.remove("rc_titan_student.csv")
