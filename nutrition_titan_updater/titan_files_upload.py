### RC Titan Files Upload
### Script to upload files the newest to 
### Titan Nutrition Management System
### For keyring, need to set the username/password for sftp sites for downloads and uploads


###Import Modules
import pysftp
import time
import keyring
from dotenv import load_dotenv
from datetime import date
from os import getenv
#######

###Variables
#Load .ENV File
load_dotenv()
#Date
current_date = date.today()
date_str = current_date.strftime('%m-%d-%Y')
start_time = time.ctime()
log_entry = str()
#Titan SFTP Vars
titan_hostname = getenv('titanHostname')
titan_username = getenv('titanUsername')
titan_service_name = getenv('titanServiceName')
#Files
upload_files = [getenv('localUpStudentFilePath'),
    getenv('localUpDirCertFilePath'),
    getenv('localUpStaffFilePath')]
#######

###Upload Files to Classlink
with pysftp.Connection(host=titan_hostname, username=titan_username, \
    password=keyring.get_password(titan_service_name, titan_username)) as sftp:
    for up_file in upload_files:
        sftp.put(up_file,up_file.split('/')[-1])
#######

###Logging
log_entry += "------------------\n"
log_entry += f"The following files were uploaded to Titan on {start_time}: \n\n"
for up_file in upload_files:
    log_entry += up_file.split('/')[-1] + "\n"
log_entry += "------------------\n"
#######

