#!/usr/bin/env python3
### Titan Update Main Script
### Script to call the various sub-scripts that 
### create create, fix, and upload files for 
### Titan Nutrition Managment System
### Scripts: 
# titan_files_download.py
# titan_student_file_generator.py
# titan_dircert_file_prep.py
# titan_staff_file_generator.py
# titan_files_upload.py

###Import Modules###
import time
import subprocess
from pathlib import Path
from datetime import date
from os import getenv
from dotenv import load_dotenv
from rc_google_py import write_log_to_google,login_google_service_account
from rcmailsend import mail_send #Self Created Module
#######

###Variables###
#Load .ENV File
load_dotenv()
#Date
current_date = date.today()
date_str = current_date.strftime('%m-%d-%Y')
start_time = time.ctime()
#Scripts
script_path = getenv('scriptPath')
source_files_script = 'titan_files_download.py'
student_files_script = 'titan_student_file_generator.py'
direct_cert_script = 'titan_dircert_file_prep.py'
staff_file_script = 'titan_staff_file_generator.py'
titan_file_upload_script = 'titan_files_upload.py'
script_list = [source_files_script, student_files_script,
    direct_cert_script, staff_file_script, titan_file_upload_script]
#Google Info
google_auth_key = getenv('GoogleAuthKey')
network_team_drive_id = getenv('NetworkTeamDriveID')
titan_log_folder_id = getenv('ClasslinkLogFolderID')
#Log Vars
log_file = str()
log_file_name = 'TitanDailyUpdaterLog-'
#Email Alert Vars
alert_to_email = getenv('alertToEmail')
alert_subject = "Titan Updater - ERROR ALERT"
###########

###Function Definitions###
#Call Python Script
def pyscript_call(script_path,script_name):
    #Call a python script
    subprocess.run(["python3", script_path + script_name])
#Log Successful Transfer
def log_script_var(script_name):
    log_entry = str()
    log_entry += "---\n"
    log_entry += f"Script {script_name} ran successfully \n"
    log_entry += "---\n"
    return log_entry
#Log Transfer Error
def log_script_error_var(script_name):
    log_entry = str()
    log_entry += "---\n"
    log_entry += f"!! Error !! Script {script_name} failed! \n"
    log_entry += "---\n"
    return log_entry
###########

###Log Begin###
log_file += "------------------\n"
log_file += f"The Classlink Updater Script was started on {start_time} \n"
log_file += "---\n"
###########


###Call the Scripts###
for sub_script in script_list:
    try:
        pyscript_call(script_path, sub_script)
        log_file += log_script_var(sub_script)
    except:
        log_script_error_var(sub_script)
###########

###Write Log to Google###
try: 
    write_log_to_google(google_auth_key, network_team_drive_id,
        titan_log_folder_id, log_file,
        log_file_name, date_str)
except:
    #Email if Error Logging
    mail_send(alert_to_email,alert_subject)
########

###Alert if Error###
if "error" in log_file.lower():
    mail_send(alert_to_email,alert_subject)
########