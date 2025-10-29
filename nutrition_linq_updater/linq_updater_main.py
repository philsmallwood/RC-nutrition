### Linq Nutrition Updater ###

### Import Modules ###
import logging
import datetime
import pandas as pd
from pathlib import Path
from os import getenv
from dotenv import load_dotenv
from linq_student_file_generator import linq_student_file_generator
from sftp_utils import sftp_upload
from rc_smtp_send import google_smtp_send
###########

### Variables ###
env_file = '/config_files/env_file/.env'
load_dotenv(env_file)
# File Vars
today_str = datetime.datetime.now().strftime('%Y-%m-%d')
final_file_path = Path(getenv('final_file_path'))
log_path = getenv('log_path')
log_file = f"{log_path}/linq_updater_{today_str}.log"
# SFTP Vars
sftp_hostname = getenv('sftp_hostname')
sftp_username = getenv('sftp_username')
sftp_password = getenv('sftp_password')
upload_path = '/'
local_path = getenv('final_file_path')
# Email Vars
alert_email = getenv('alert_email')
subject = f"!! Linq Nutrition Updater Error {today_str} !!"
smtp_pass = getenv('smtp_pass')
###################

### Logging Setup ###
logger = logging.getLogger("nutrition_linq_updater")
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(message)s'))
    logger.addHandler(handler)
logger.propagate = False    
#####################

### Student File Generation ###
try:
    linq_student_file_generator(env_file)
    logger.info("Student file generated successfully.")
except Exception as e:
    logger.error(f"Error generating student file: {e}")
###############################

###  Upload Files to Remind ###
# Get List of Files to Upload
upload_files = [f for f in final_file_path.iterdir() if f.is_file()]
# Upload Files
try:
    for upfile in upload_files:
        sftp_upload(sftp_hostname,
                    sftp_username,
                    sftp_password,
                    f"{local_path}{upfile.name}",
                    f"{upload_path}{upfile.name}")
        logger.info(f"Uploaded {upfile.name} to {upload_path}")
    # Logging for SFTP Upload
    logger.info("Files Uploaded to Linq")
except Exception as e:
    # Logging for Error
    logger.error(f"Files Not Uploaded to Linq: {e}")
###########

### Email if Error Occurs ###
with open(log_file, "r") as f:
    if "Error" in f.read():
        google_smtp_send(alert_email,
            subject,
            smtp_pass,
            message_body=f.read())
##############################




