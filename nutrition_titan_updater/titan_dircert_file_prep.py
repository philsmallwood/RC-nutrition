#!/usr/bin/env python3
###RC Titan DirectCert Script
###Script to process Direct Cert files and upload to Titan
###Requires time, pandas, keyring, and pysftp to be installed
###For keyring, need to set the username/password for sftp sites for downloads and uploads

###Import Modules###
import pandas as pd
import time
import os
import sys
from dotenv import load_dotenv
from datetime import date
#######

#####Variables#####
#Load .ENV File
load_dotenv()
#Date
startTime = time.ctime()
CurrentDate = date.today()
Date = CurrentDate.strftime('%m-%d-%Y')
#File Vars
localNutritionDirCertPath = os.getenv('localNutritionDirCertPath')
archivePath = os.getenv('localArchivePath')
localUpFilePath = os.getenv('localUpDirCertFilePath')
archiveDirCertFile = archivePath + 'dircertupload-' + Date + '.csv'
df_dircerts = pd.DataFrame()
#Log
logFile = os.getenv('logFilePath') + "Titan-" + Date + ".log"
#######

###Read Direct Cert Files into a Dataframe###
localNutritionDirCertFiles = os.listdir(localNutritionDirCertPath)
if not localNutritionDirCertFiles:
    #Logging No New Files
    f = open(logFile, "a")
    f.write("------------------\n")
    f.write("No New Direct Cert Files to Process \n")
    f.write("------------------\n")
    f.close()
else:
    for certFile in localNutritionDirCertFiles:
        try:
            df_temp = pd.read_csv(localNutritionDirCertPath+certFile, sep='\t', skiprows=3, dtype=str, encoding='utf-16')
            df_dircerts = pd.concat([df_dircerts,df_temp])
            os.rename(localNutritionDirCertPath+certFile,archivePath+certFile)
        except UnicodeError:
            df_temp = pd.read_csv(localNutritionDirCertPath+certFile, skiprows=3, dtype=str)
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
if not df_dircerts.empty:
    #Archive Old Direct Cert Titan File
    os.rename(localUpFilePath,archiveDirCertFile)
    #Create Empty Final Dataframe
    df_final = pd.DataFrame()
    #Add Necessary Data
    df_final['StudentID'] = df_dircerts['StudentID'].str.zfill(6)
    df_final['Type'] = df_dircerts['FoodStamps']
    df_final['Entry_Date'] = df_dircerts['Entry_Date']
    #Format Eligibility Type
    df_final.loc[df_final['Type'] ==  'Y', ['Type']] = 'SNAP'
    df_final.loc[df_final['Type'] ==  'N', ['Type']] = 'TANF'
    #Export File for Titan###
    df_final.to_csv(localUpFilePath, index=False)
#######