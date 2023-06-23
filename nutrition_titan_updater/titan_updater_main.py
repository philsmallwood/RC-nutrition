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
from datetime import date
from os import getenv
from dotenv import load_dotenv
from titan_files_upload import titan_files_upload
from titan_student_file_generator import titan_student_file_generator
from titan_staff_file_generator import titan_staff_file_generator
from titan_dircert_file_prep import titan_dircert_file_prep
from titan_files_download import titan_files_download
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
script_list = [titan_files_download, titan_student_file_generator,
    titan_dircert_file_prep, titan_staff_file_generator, titan_files_upload]
#Google Info
google_auth_key = getenv('google_auth_key')
network_team_drive_id = getenv('network_team_drive_id')
titan_log_folder_id = getenv('titan_log_folder_id')
#Log Vars
log_file = str()
log_file_name = 'TitanDailyUpdaterLog-'
#Email Alert Vars
alert_to_email = getenv('log_to_email')
alert_subject = "Titan Updater - ERROR ALERT"
###########

###Function Definitions###
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
        log_file += sub_script()
        log_file += log_script_var(sub_script)
    except:
        log_file += log_script_error_var(sub_script)
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