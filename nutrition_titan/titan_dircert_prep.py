#!/usr/bin/env python3
###RC Titan DirectCert Script
###Script to process Direct Cert files and upload to Titan
###Requires time, pandas, keyring, and pysftp to be installed
###For keyring, need to set the username/password for sftp sites for downloads and uploads

###Import Modules###
import pandas as pd
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
todayStr = today.strftime("%m/%d/%Y")
#Server Info
titanHostname = "sftp.titank12.com"
titanUsername = "RCCSD"
nutritionServer = "10.222.2.70"
nutritionShare = './dircert/'
nutritionUserName = 'philip.smallwood'
#File Vars
localNutritionPath = '/uploads/nutrition/dircert/'
archivePath ='/archive/'
localUpFilePath = '/RC-scripts/nutrition_titan/dircertupload.csv'
remoteUpFilePath = '/dircertupload.csv'
archiveFile = '/archive/dircertupload-' + todayStr + '.csv'
df_dircerts = pd.DataFrame()
#Mail_send Vars
logToEmail = 'philip.smallwood@redclay.k12.de.us'
logSubject = 'Titan Direct Cert File Uploaded'
logFile = "/var/log/scripts/titan_dircert_prep.log"
#######

###Logging###
f = open(logFile, "a")
f.write("------------------\n")
f.write("The Titan Direct Cert script started on " + startTime + "\n")
f.write("------------------\n")
f.close()
#######

###Get Direct Cert Files###
#Download any file with .txt or .csv extentions in 
#Dircert folder on server
try:
    with pysftp.Connection(host=nutritionServer, username=nutritionUserName, password=keyring.get_password("AD", "philip.smallwood")) as sftp:
        with sftp.cd(nutritionShare):
            dircertFiles = sftp.listdir()
            for file in dircertFiles:
                if (file[-3:]=='txt'):
                    sftp.get(file, localNutritionPath + file)
                elif (file[-3:]=='csv'):
                    sftp.get(file, localNutritionPath + file)
    #Logging
    f = open(logFile, "a")
    f.write("------------------\n")
    f.write("Files Downloaded from PCS Server \n")
    f.write("------------------\n")
    f.close()
except:
    #Logging
    f = open(logFile, "a")
    f.write("------------------\n")
    f.write("Files Could Not Be Downloaded from PCS Server \n")
    f.write("------------------\n")
    f.close()
#######   
    
###Read Direct Cert Files into a Dataframe###
localNutritionFiles = os.listdir(localNutritionPath)
for certFile in localNutritionFiles:
    try:
        df_temp = pd.read_csv(localNutritionPath+certFile, sep='\t', skiprows=3, dtype=str, encoding='utf-16')
        df_dircerts = pd.concat([df_dircerts,df_temp])
    except UnicodeError:
        df_temp = pd.read_csv(localNutritionPath+certFile, skiprows=3, dtype=str)
        df_dircerts = pd.concat([df_dircerts,df_temp])
        continue
    except:
        #Logging
        f = open(logFile, "a")
        f.write("------------------\n")
        f.write("Files Could Not Be Processed \n")
        f.write("------------------\n")
        f.close()
        break
#######

###Final Dataframe###
#Create empty Final Dataframe
df_final = pd.DataFrame()
#Add pieces
df_final['StudentID'] = df_dircerts['StudentID'].str.zfill(6)
df_final['Type'] = df_dircerts['FoodStamps']
df_final['Entry_Date'] = df_dircerts['Entry_Date']
#Format Eligibility Type
df_final.loc[df_final['Type'] ==  'Y', ['Type']] = 'SNAP'
df_final.loc[df_final['Type'] ==  'N', ['Type']] = 'TANF'
#######

###Export File for Titan###
df_final.to_csv(localUpFilePath, index=False)
#######

###Upload file to Titan###
with pysftp.Connection(host=titanHostname, username=titanUsername, password=keyring.get_password("TITANK12", "RCCSD")) as sftp:
    sftp.put(localUpFilePath, remoteUpFilePath)
#######

###Logging###
f = open(logFile, "a")
f.write("------------------\n")
f.write("File sent to Titan \n")
f.write("------------------\n")
f.close()
#######

###Cleanup###
#Move Downloaded Files to Archive
for file in localNutritionFiles:
    os.rename(localNutritionPath+file,archivePath+file)
#Delete files on Server
with pysftp.Connection(host=nutritionServer, username=nutritionUserName, password=keyring.get_password("AD", "philip.smallwood")) as sftp:
    with sftp.cd(nutritionShare):
        for file in dircertFiles:
            sftp.remove(file)
#Move Final File to Archive with Timestamp
os.rename(localUpFilePath,archivePath+remoteUpFilePath)
#Email Log
mail_send(logToEmail,logSubject,logFile)
#######