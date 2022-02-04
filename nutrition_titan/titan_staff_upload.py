#!/usr/bin/env python3
###RC Titan Staff File Script
###Script to generate a student file with the necesary info for nutrition
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
titanHostname = "sftp.titank12.com"
titanUsername = "RCCSD"
localStaffFilePath = '/uploads/DSC/Google/Google_Staff_Dump.csv'
localUpFilePath = './rc_titan_staff.csv'
remoteUpFilePath = '/rc_titan_staff.csv'
logFile = "/var/log/scripts/titan_staff_upload.log"
    
###Read Staff file to dataframe
df_staff = pd.read_csv(localStaffFilePath, dtype=str, error_bad_lines=False)

###Designate StateID as belonging to employee
###Append 'E' to each EmployeeID
df_staff['EmployeeID'] = 'E' + df_staff['EmployeeID'].astype(str)

###Add District identifier to each building's code
df_staff['HR_Location'] = '320' + df_staff['HR_Location'].astype(str)


###Reorder to final form
df_final = df_staff[['EmployeeID', 'FirstName', 'MiddleName', 'LastName', 'Google_Custom_Email', 'EmployeeID', 'Dob', 'HR_Gender', 'HR_Location']]

###Add staff type to dataframe
###Can be set to 'General' for all non-Nutrition workers
df_final['StaffType'] = 'General'

###Add Staff Assignment Data
###For the Summer, all will start on 08/15/2021
df_final['AssignmentStart'] = '08/15/2021'

###Export to data to csv file
df_final.to_csv(localUpFilePath, index=False)

###Upload file to Titan
with pysftp.Connection(host=titanHostname, username=titanUsername, password=keyring.get_password("TITANK12", "RCCSD")) as sftp:
    sftp.put(localUpFilePath, remoteUpFilePath)


###Logging
f = open(logFile, "a")
f.write("------------------\n")
f.write("The Titan staff upload script ran on " + startTime + "\n")
f.write("------------------\n")
f.close()

###Email Results
os.system("python3 /usr/local/bin/mailsend.py 'philip.smallwood@redclay.k12.de.us' 'Staff File Successfully Uploaded to Titan' '/var/log/scripts/titan_staff_upload.log' ")

###Remove downloaded files
os.remove(localStaffFilePath)

###Move Uploaded file to archive
os.rename(localUpFilePath,time.strftime("/archive/%Y%m%d%H%M%S-TitanStaffFile.csv"))
