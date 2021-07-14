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


###Set variables for script
startTime = time.ctime()
myHostname = "ftp.doe.k12.de.us"
myUsername = "colonialdata"
titanHostname = "sftp.titank12.com"
titanUsername = "RCCSD"
remoteFilePath = '/Cognos/Titan-en.xlsx'
localFilePath = './Titan-en.xlsx'
localUpFilePath = './rc_titan_student.csv'
remoteUpFilePath = '/rc_titan_student.csv'

###Get Titan Cognos Report from DOE SFTP
##NOTE: 7/7/2021 - need to change to RedClay instance when have correct access
with pysftp.Connection(host=myHostname, username=myUsername, password=keyring.get_password("COLDOE", "colonialdata")) as sftp:
    sftp.get(remoteFilePath, localFilePath)

###Read Cognos report 
df = pd.read_excel("Titan-en.xlsx", dtype=str)

###Re-order the report into the correct order, with an additional field at end to determine program
df_reorder = df[['Student Id', 'Student First Name', 'Student Middle Name', 'Student Last Name', 'Student Generation', 'Student Id', 'Birthdate', 'Student Gender', 'Federal Race Code', 'Hispanic/Latino Ethnicity', 'Alternate Building', 'Current School Year', 'Current Building', 'Student Grade', 'Student Homeroom Primary', 'Street Addr Line & Apt - Physical', 'City - Physical', 'State - Physical', 'Zip - Physical', 'Street Addr Line & Apt - Mailing', 'City - Mailing', 'State - Mailing', 'Zip - Mailing', 'First Name - Guardian', 'Middle Name - Guardian', 'Last Name - Guardian', 'Mobile Phone', 'Home Phone', 'Work Phone', 'Email - Guardian', 'Relation Name - Guardian', 'Alternate Building Name']]

###Swap Current and Alternate Building for special programs
###NOTE: 07/14/2021
###Programs Affected - Meadowood and Early Years
##Meadowood
df_reorder.loc[df_reorder['Alternate Building Name'] == 'Forest Oak Elementary School', ['Current Building', 'Alternate Building']] = '320240', '320516'
df_reorder.loc[df_reorder['Alternate Building Name'] == 'H.B. duPont Middle School', ['Current Building', 'Alternate Building']] = '320276', '320516'
df_reorder.loc[df_reorder['Alternate Building Name'] == 'McKean High School', ['Current Building', 'Alternate Building']] = '320294', '320516'
##Early Years
df_reorder.loc[df_reorder['Alternate Building Name'] == 'Meadowood Program', ['Current Building', 'Alternate Building']] = '320516', '320529'
df_reorder.loc[df_reorder['Alternate Building Name'] == 'Mote Elementary School', ['Current Building', 'Alternate Building']] = '320264', '320529'
df_reorder.loc[df_reorder['Alternate Building Name'] == 'Richardson Park Learning Center', ['Current Building', 'Alternate Building']] = '320254', '320529'
df_reorder.loc[df_reorder['Alternate Building Name'] == 'Warner Elementary School', ['Current Building', 'Alternate Building']] = '320266', '320529'
df_reorder.loc[df_reorder['Alternate Building Name'] == 'Wm. C. Lewis Dual Language Elem.', ['Current Building', 'Alternate Building']] = '320246', '320529'

###Drop Z calendar (320888) and First State School (320530) students
df_no888 = df_reorder[df_reorder['Current Building'] != '320888']
df_no530or888 = df_no888[df_no888['Current Building'] != '320530']

###Drop extra column at the end
###Holding on dropping this until 09/01/2021
df_no530or888.loc[df_no530or888['Alternate Building Name'] != 'a', ['Alternate Building Name']] = '8/31/2021'
df_final = df_no530or888
#df_final = df_no530or888.drop(columns = ['Alternate Building Name'])

###Export to csv
df_final.to_csv("rc_titan_student.csv", index=False)

###Upload file to Titan

#with pysftp.Connection(host=titanHostname, username=titanUsername, password=keyring.get_password("TITANFTP", "RCCSD")) as sftp:
#    sftp.put(localUpFilePath, remoteUpFilePath)


###Logging
f = open("titan_student_upload.log", "a")
f.write("------------------\n")
f.write("The Titan student upload script ran on " + startTime + "\n")
f.write("------------------\n")
f.close()

###Remove downloaded files
#os.remove("Titan-en.csv")
#os.remove("rc_titan_student.csv")
