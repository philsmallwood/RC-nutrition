#!/usr/bin/env python3
### RC Titan Source Files Download
### Script to download the newest copy of the 
### the student file for Urban Promise Charter
### and the Direct Certification Files from the 
### Nutrition Server
###Requires time, pandas, keyring, datetime, 
###pysftp, and rcmailsend(self-created package) to be installed
###For keyring, need to set the username/password for sftp sites for downloads and uploads

###Import Modules###
import keyring
import pysftp
import time
import os
import sys
from datetime import date
from rcmailsend import mail_send #Self Created Module
#######

#region Variable and Function Defs
#####Variables#####
#Date
CurrentDate = date.today()
Date = CurrentDate.strftime('%m-%d-%Y')
startTime = time.ctime()
#Server Info
nutritionServer = "10.222.2.70"
nutritionDailyShare = './dailyenrollment/'
nutritionDirCertShare = './dircert/'
nutritionUserName = 'philip.smallwood'
#File Vars
localNutritionUrbanPromisePath = '/uploads/nutrition/urbanpromise/'
localNutritionDirCertPath = '/uploads/nutrition/dircert'
currentUrbanPromiseFile = 'urbanpromisecurrent'
archivePath ='/archive/'
localUpFilePath = '/RC-scripts/nutrition_titan/dircertupload.csv'
archiveFile = '/archive/urbanpromise-' + Date + '.xls'
#Mail_send Vars
logFile = "/var/log/scripts/Titan-" + Date + ".log"
logToEmail = 'philip.smallwood@redclay.k12.de.us'
logNewFile = 'New Urban Promise File Downloaded'
logNoFile = 'No New Urban Promise File'
logProblem = 'Urban Promise File - PROBLEM!!'
logSubjectProblem = 'Urban Promise File - PROBLEM!!'
#######
#endregion Variable and Function Defs


#region Download Urban Promise File
###Get Urban Promise File###
#Download Files with .xls, .xlsx, or .csv Extentions
#in Dailyenrollment Folder on Server
try:
    with pysftp.Connection(host=nutritionServer, username=nutritionUserName, \
        password=keyring.get_password("AD", "philip.smallwood")) as sftp:
        with sftp.cd(nutritionDailyShare):
            dailyFiles = sftp.listdir()
            for file in dailyFiles:
                if (file[-3:]=='xls'):
                    sftp.get(file, localNutritionUrbanPromisePath + file)
                    sftp.remove(file)
                elif (file[-4:]=='xlsx'):
                    sftp.get(file, localNutritionUrbanPromisePath + file)
                    sftp.remove(file)
                elif (file[-3:]=='csv'):
                    sftp.get(file, localNutritionUrbanPromisePath + file)
                    sftp.remove(file)
    #Logging
    f = open(logFile, "a")
    f.write("------------------\n")
    f.write("Urban Promise File Downloaded or No File from PCS Server \n")
    f.write("------------------\n")
    f.close()
except:
    #Logging Error
    f = open(logFile, "a")
    f.write("------------------\n")
    f.write("Problem Connecting to Server to Download Urban Promise File \n")
    f.write("------------------\n")
    f.close()
#######
#endregion Download Urban Promise File

#region Download Direct Certification Files
###Get Direct Cert Files###
#Download Files with .txt or .csv Extentions in 
#Dircert Folder on Server
try:
    with pysftp.Connection(host=nutritionServer, username=nutritionUserName, \
        password=keyring.get_password("AD", "philip.smallwood")) as sftp:
        with sftp.cd(nutritionDirCertShare):
            dircertFiles = sftp.listdir()
            for file in dircertFiles:
                if (file[-3:]=='txt'):
                    sftp.get(file, localNutritionDirCertPath + file)
                elif (file[-3:]=='csv'):
                    sftp.get(file, localNutritionDirCertPath + file)
    #Logging
    f = open(logFile, "a")
    f.write("------------------\n")
    f.write("Direct Cert Files Downloaded from PCS Server or No New File \n")
    f.write("------------------\n")
    f.close()
except:
    #Logging
    f = open(logFile, "a")
    f.write("------------------\n")
    f.write("Problem Connecting to Server to Download Direct Cert Files \n")
    f.write("------------------\n")
    f.close()
####### 
#endregion Download Direct Certification Files

#region Process Urban Promise File
###Make New File Current and Backup Old File###
urbanPromiseFiles = os.listdir(localNutritionUrbanPromisePath)
if len(urbanPromiseFiles) == 2:
    #Move current file to archive
    os.rename(localNutritionUrbanPromisePath+currentUrbanPromiseFile,archiveFile)
    urbanPromiseFilesNew = os.listdir(localNutritionUrbanPromisePath)
    os.rename(localNutritionUrbanPromisePath+urbanPromiseFilesNew[0],localNutritionUrbanPromisePath+currentUrbanPromiseFile)
    #Write entry to log
    f = open(logFile, "a")
    f.write("---\n")
    f.write(logNewFile + " \n")
    f.write("---\n")
    f.close()
elif len(urbanPromiseFiles) == 1:
    #Write Entry to Log
    f = open(logFile, "a")
    f.write("---\n")
    f.write(logNoFile + " \n")
    f.write("---\n")
    f.close()
else:
    #Write Entry to Log
    f = open(logFile, "a")
    f.write("---\n")
    f.write(logProblem + " \n")
    f.write("---\n")
    f.close()
    #Email Alert of Problem
    mail_send(logToEmail,logSubjectProblem)
#endregion Process Urban Promise File



