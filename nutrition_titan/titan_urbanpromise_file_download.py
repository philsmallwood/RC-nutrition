#!/usr/bin/env python3
### RC Titan Urban Promise File Download
### Script to download the newest copy of the 
### the student file for Urban Promise Charter
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

#####Variables#####
#Date
startTime = time.ctime()
today = date.today()
todayStr = today.strftime("%m-%d-%Y")
#Server Info
nutritionServer = "10.222.2.70"
nutritionShare = './dailyenrollment/'
nutritionUserName = 'philip.smallwood'
#File Vars
localNutritionPath = '/uploads/nutrition/urbanpromise/'
currentUrbanPromiseFile = 'urbanpromisecurrent'
archivePath ='/archive/'
localUpFilePath = '/RC-scripts/nutrition_titan/dircertupload.csv'
archiveFile = '/archive/urbanpromise-' + todayStr + '.xls'
#Mail_send Vars
logToEmail = 'philip.smallwood@redclay.k12.de.us'
logSubjectNewFile = 'New Urban Promise File Downloaded'
logSubjectNoFile = 'No New Urban Promise File'
logSubjectProblem = 'Urban Promise File - PROBLEM'
#######

###Get Urban Promise File###
#Download any file with .xls, .xlsx, or .csv extentions
#in Dailyenrollment folder on server
try:
    with pysftp.Connection(host=nutritionServer, username=nutritionUserName, password=keyring.get_password("AD", "philip.smallwood")) as sftp:
        with sftp.cd(nutritionShare):
            dailyFiles = sftp.listdir()
            for file in dailyFiles:
                if (file[-3:]=='xls'):
                    sftp.get(file, localNutritionPath + file)
                    sftp.remove(file)
                elif (file[-4:]=='xlsx'):
                    sftp.get(file, localNutritionPath + file)
                    sftp.remove(file)
                elif (file[-3:]=='csv'):
                    sftp.get(file, localNutritionPath + file)
                    sftp.remove(file)
except:
    pass
#######

###Make New file Current and backup old one###
urbanPromiseFiles = os.listdir(localNutritionPath)
if len(urbanPromiseFiles) == 2:
    #Move current file to archive
    os.rename(localNutritionPath+currentUrbanPromiseFile,archiveFile)
    urbanPromiseFilesNew = os.listdir(localNutritionPath)
    os.rename(localNutritionPath+urbanPromiseFilesNew[0],localNutritionPath+currentUrbanPromiseFile)
    #email new file alert
    mail_send(logToEmail,logSubjectNewFile)
elif len(urbanPromiseFiles) == 1:
    #email no new file alert
    mail_send(logToEmail,logSubjectNoFile)
else:
    #email alert to problem
    mail_send(logToEmail,logSubjectProblem)



