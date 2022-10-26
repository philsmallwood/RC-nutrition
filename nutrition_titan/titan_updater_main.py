#!/usr/bin/env python3
### Titan Update Main Script
### Script to call the various sub-scripts that 
### create create, fix, and upload files for 
### Titan Nutrition Managment System
### Scripts: 
# titan_urbanpromise_file_download.py
# titan_student_all_upload.py
# classlink_dsc_file_fix.py
# classlink_upload.py

###Import Modules###
import time
import datetime
import os
from rcmailsend import mail_send #Self Created Module
#######

###Variables###
#Date
CurrentDate = datetime.date.today()
Date = CurrentDate.strftime('%m-%d-%Y')
startTime = time.ctime()
#Scripts
scriptPath = '/RC-scripts/classlink/classlink_updater/'
urbanPromiseFileScript = 'titan_urbanpromise_file_download.py'
studentFileScript = 'titan_student_all_upload.py'
directCertScript = 'classlink_dsc_file_fix.py'
uploadscript = 'classlink_upload.py'
#Email Vars
logToEmail = 'philip.smallwood@redclay.k12.de.us'
logSubject = 'Classlink Updates Log'
logFile = "/var/log/scripts/Classlink-" + Date +".log"
##Function Definitions
#Function to call a python script and append info to a log file
def pyscript_call(scriptPath,scriptName,logFile):
    #Call a python script
    os.system("python3 %s" % scriptPath + scriptName)
    #Write entry to log
    f = open(logFile, "a")
    f.write("---\n")
    f.write("The " + scriptName + " script ran successfully \n")
    f.write("---\n")
    f.close()
###########

###Log Begin
f = open(logFile, "a")
f.write("------------------\n")
f.write("The Titan Updater Script was started on " + startTime + "\n")
f.write("---\n")
f.close()

###Admin File Generator###
try:
    pyscript_call(scriptPath,adminScript,logFile)
except:
    ###Log Error
    f = open(logFile, "a")
    f.write("---\n")
    f.write("The " + adminScript + " failed! \n")
    f.write("---\n")
    f.close()


#Call Urban Promise Downloader

#Call Student Updater

## call Direct Cert 

##Call Staff

