#!/usr/bin/env python3
### Titan Update Main Script
### Script to call the various sub-scripts that 
### create create, fix, and upload files for 
### Titan Nutrition Managment System
### Scripts: 
# titan_files_download.py
# titan_student_file_generator.py
# titan_dircert_file_prep.py
# titan_staff_upload.py

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
scriptPath = '/RC-scripts/nutrition_titan/'
sourceFilesScript = 'titan_files_download.py'
studentFileScript = 'titan_student_file_generator.py'
directCertScript = 'titan_dircert_file_prep.py'
staffFileScript = 'titan_staff_upload.py'
uploadscript = 'classlink_upload.py'
#Email Vars
logToEmail = 'philip.smallwood@redclay.k12.de.us'
logSubject = 'Titan Updates Log'
logFile = "/var/log/scripts/Titan-" + Date + ".log"
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
def log_script_error(scriptName,logFile):
    #Write the Error to the Log
        ###Log Error
    f = open(logFile, "a")
    f.write("---\n")
    f.write("The " + scriptName + " failed! \n")
    f.write("---\n")
    f.close()
###########

###Log Begin
f = open(logFile, "a")
f.write("------------------\n")
f.write("The Titan Updater Script was started on " + startTime + "\n")
f.write("---\n")
f.close()

###Source Files Downloader###
try:
    pyscript_call(scriptPath,sourceFilesScript,logFile)
except:
    log_script_error(sourceFilesScript,logFile)
###########

###Student Updater File Generator###
try:
    pyscript_call(scriptPath,studentFileScript,logFile)
except:
    log_script_error(studentFileScript,logFile)
###########

###Direct Certification File Generator###
try:
    pyscript_call(scriptPath,directCertScript,logFile)
except:
    log_script_error(directCertScript,logFile)
###########

###Staff Updater File Generator###
try:
    pyscript_call(scriptPath,staffFileScript,logFile)
except:
    log_script_error(staffFileScript,logFile)
###########

###Titan File Uploader###
try:
    pyscript_call(scriptPath,titanFileUploadScript,logFile)
except:
    log_script_error(titanFileUploadScript,logFile)
###########


#
titanHostname = "sftp.titank12.com"
titanUsername = "RCCSD"
###Upload file to Titan
with pysftp.Connection(host=titanHostname, username=titanUsername, \
    password=keyring.get_password("TITANK12", "RCCSD")) as sftp:
    sftp.put(localUpFilePath, remoteUpFilePath)