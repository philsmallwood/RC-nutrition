#!/usr/bin/env python3
### RC Titan Files Upload
### Script to upload files the newest to 
### Titan Nutrition Management System
### Requires time, pandas, keyring, datetime, 
###pysftp
###For keyring, need to set the username/password for sftp sites for downloads and uploads


###Import Modules
import re
import pysftp
import time
import keyring
from dotenv import load_dotenv
from datetime import date
import os
#######


###Variables
#Load .ENV File
load_dotenv()
#Date
CurrentDate = date.today()
Date = CurrentDate.strftime('%m-%d-%Y')
startTime = time.ctime()
logFile = os.getenv('logFilePath') + "Titan-" + Date + ".log"
#Titan SFTP Vars
titanHostname = os.getenv('titanHostname')
titanUsername = os.getenv('titanUsername')
titanServiceName = os.getenv('titanServiceName')
#Files
uploadFiles = [os.getenv('localUpStudentFilePath'),
    os.getenv('localUpDirCertFilePath'),
    os.getenv('localUpStaffFilePath')]
#######

###Upload Files to Classlink
with pysftp.Connection(host=titanHostname, username=titanUsername, \
    password=keyring.get_password(titanServiceName, titanUsername)) as sftp:
    for upFile in uploadFiles:
        sftp.put(upFile,upFile.split('/')[-1])
#######

###Logging
f = open(logFile, "a")
f.write("------------------\n")
f.write("The following files were uploaded to Titan on " + startTime + ": \n\n")
for upFile in uploadFiles:
    f.write(upFile.split('/')[-1] + "\n")
f.write("------------------\n")
f.close()
#######

