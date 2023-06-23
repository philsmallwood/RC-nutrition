#!/usr/bin/env python3
### RC Titan Source Files Download
### Script to download the newest copy of the 
### the student file for Urban Promise Charter
### and the Direct Certification Files from the 
### Nutrition Server
### For keyring, need to set the username/password for sftp sites for downloads and uploads

def titan_files_download():
    ###Import Modules###
    import keyring
    import pysftp
    import time
    from os import getenv,listdir,rename
    from datetime import date
    from dotenv import load_dotenv
    from rcmailsend import mail_send #Self Created Module
    #######

    #region Variable and Function Defs
    #####Variables#####
    #Load .ENV File
    load_dotenv()
    #Date
    current_date = date.today()
    date_str = current_date.strftime('%m-%d-%Y')
    #Server Info
    nutrition_server = getenv('nutrition_server')
    nutrition_daily_share = getenv('nutrition_daily_share')
    nutrition_direct_cert_share = getenv('nutritionDirCertShare')
    nutrition_user_name = getenv('nutrition_user_name')
    nutrition_service_name = getenv('nutrition_service_name')
    #File Vars
    nutrition_urban_promise_path = getenv('nutrition_urban_promise_path')
    nutrition_direct_cert_path = getenv('nutrition_direct_cert_path')
    current_urban_promise_file = getenv('current_urban_promise_file')
    archive_file = getenv('archive_path') + 'urbanpromise-' + date_str + '.xls'
    #Mail_send Vars
    log_entry = str()
    log_to_email = getenv('log_to_email')
    log_new_file = 'New Urban Promise File Downloaded'
    log_no_file = 'No New Urban Promise File'
    log_problem = 'Urban Promise File - PROBLEM!!'
    subject_problem = 'Urban Promise File - PROBLEM!!'
    ###Functions
    #Log Successful File Download
    def log_file_download(log_entry,fileName):
        #Write the Error to the Log
        log_entry += "------------------\n"
        log_entry += f"{fileName} File Downloaded from PCS Server \n"
        log_entry += "------------------\n"
    #Log Cannot Remove File
    def log_script_error_cannot_remove(log_entry):
        #Write the Error to the Log
        log_entry += "------------------\n"
        log_entry += "Cannot Remove File \n"
        log_entry += "------------------\n"
    #######
    #endregion Variable and Function Defs


    #region Download Urban Promise File
    ###Get Urban Promise File###
    #Download Files with .xls, .xlsx, or .csv Extentions
    #in Dailyenrollment Folder on Server
    try:
        with pysftp.Connection(host=nutrition_server, username=nutrition_user_name, \
            password=keyring.get_password(nutrition_service_name, nutrition_user_name)) as sftp:
            with sftp.cd(nutrition_daily_share):
                dailyFiles = sftp.listdir()
                if dailyFiles:
                    for file in dailyFiles:
                        if (file[-3:]=='xls'):
                            sftp.get(file, nutrition_urban_promise_path + file)
                            log_file_download(log_entry,"Urban Promise")
                            try:
                                sftp.remove(file)
                            except:
                                log_script_error_cannot_remove(log_entry)
                        elif (file[-4:]=='xlsx'):
                            sftp.get(file, nutrition_urban_promise_path + file)
                            log_file_download(log_entry,"Urban Promise")
                            try:
                                sftp.remove(file)
                            except:
                                log_script_error_cannot_remove(log_entry)
                        elif (file[-3:]=='csv'):
                            sftp.get(file, nutrition_urban_promise_path + file)
                            log_file_download(log_entry,"Urban Promise")
                            try:
                                sftp.remove(file)
                            except:
                                log_script_error_cannot_remove(log_entry)
                else:
                    #Logging
                    log_entry += "------------------\n"
                    log_entry += "No New Urban Promise File on PCS Server \n"
                    log_entry += "------------------\n"
    except:
        #Logging Error
        log_entry += "------------------\n"
        log_entry += "Problem Connecting to Server to Download Urban Promise File \n"
        log_entry += "------------------\n"
    #######
    #endregion Download Urban Promise File

    #region Download Direct Certification Files
    ###Get Direct Cert Files###
    #Download Files with .txt or .csv Extentions in 
    #Dircert Folder on Server
    try:
        with pysftp.Connection(host=nutrition_server, username=nutrition_user_name, \
            password=keyring.get_password(nutrition_service_name, nutrition_user_name)) \
            as sftp:
            with sftp.cd(nutrition_direct_cert_share):
                dircertFiles = sftp.listdir()
                if dircertFiles:
                    for file in dircertFiles:
                        if (file[-3:]=='txt'):
                            sftp.get(file, nutrition_direct_cert_path + file)
                            log_file_download(log_entry,"DirCert")
                            try:
                                sftp.remove(file)
                            except:
                                log_script_error_cannot_remove(log_entry)
                        elif (file[-3:]=='csv'):
                            sftp.get(file, nutrition_direct_cert_path + file)
                            log_file_download(log_entry,"DirCert")
                            try:
                                sftp.remove(file)
                            except:
                                log_script_error_cannot_remove(log_entry)
                else:
                    #Logging
                    log_entry +="------------------\n"
                    log_entry +="No New Direct Cert Files on PCS Server \n"
                    log_entry +="------------------\n"
    except:
        #Logging
        log_entry +="------------------\n"
        log_entry +="Problem Connecting to Server to Download Direct Cert Files \n"
        log_entry +="------------------\n"
    ####### 
    #endregion Download Direct Certification Files

    #region Process Urban Promise File
    ###Make New File Current and Backup Old File###
    urbanPromiseFiles = listdir(nutrition_urban_promise_path)
    if len(urbanPromiseFiles) == 2:
        #Move current file to archive
        rename(nutrition_urban_promise_path+current_urban_promise_file,archive_file)
        urbanPromiseFilesNew = listdir(nutrition_urban_promise_path)
        rename(nutrition_urban_promise_path+urbanPromiseFilesNew[0],\
            nutrition_urban_promise_path+current_urban_promise_file)
        #Write entry to log
        log_entry += "---\n"
        log_entry += f"{log_new_file}\n"
        log_entry += "---\n"
    elif len(urbanPromiseFiles) == 1:
        #Write Entry to Log
        log_entry += "---\n"
        log_entry += f"{log_no_file}\n"
        log_entry += "---\n"
    else:
        #Write Entry to Log
        log_entry += "---\n"
        log_entry += f"{log_problem}\n"
        log_entry += "---\n"
        #Email Alert of Problem
        mail_send(log_to_email,subject_problem)
    #endregion Process Urban Promise File

    return log_entry
