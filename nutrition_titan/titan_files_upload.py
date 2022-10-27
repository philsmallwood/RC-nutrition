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
from datetime import date
import os
#######


###Variables
#Date
CurrentDate = date.today()
Date = CurrentDate.strftime('%m-%d-%Y')
startTime = time.ctime()
logFile = "/var/log/scripts/Titan-" + Date + ".log"
#Titan SFTP Vars
titanHostname = "sftp.titank12.com"
titanUsername = "RCCSD"
#Files
uploadFiles = ['/uploads/RC/rc_titan_student.csv',
    '/uploads/RC/rc_titan_staff.csv',
    '/uploads/RC/dircertupload.csv']
#######

###Upload Files to Classlink
with pysftp.Connection(host=titanHostname, username=titanUsername, \
    password=keyring.get_password("TITANK12", "RCCSD")) as sftp:
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

