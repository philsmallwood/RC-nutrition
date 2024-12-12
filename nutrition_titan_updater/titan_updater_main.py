### Titan Update Main Script
### Script to call the various sub-scripts that 
### create create, fix, and upload files for 
### Titan Nutrition Managment System


### Import Modules ###
import pandas as pd
import time
import logging
import pysftp
from datetime import date
from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from pathlib import Path
from modules.titan_student_file_generator import titan_student_file_generator
from modules.titan_staff_file_generator import titan_staff_file_generator
from modules.titan_dircert_file_generator import titan_dircert_file_generator
from modules.titan_urban_promise_data_download import titan_urban_promise_data_download
#from rc_smtp_send import google_smtp_send 
#######

### Configure Logging ###
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
#########

logger.info("Titan Updater Script Started")

###Variables###
# Load .ENV File
load_dotenv()
# Date
current_date = date.today()
date_str = current_date.strftime('%m-%d-%Y')
start_time = time.ctime()
# Google Info
google_auth_key = getenv('google_auth_key')
network_team_drive_id = getenv('network_team_drive_id')
nutrition_shared_drive_id = getenv('nutrition_shared_drive_id')
direct_cert_shared_folder_id = getenv('direct_cert_shared_folder_id')
titan_log_folder_id = getenv('titan_log_folder_id')
urban_promise_sheet_id = getenv('urban_promise_sheet_id')
# MySQL Vars
sql_username = getenv('sql_username')
sql_pass = getenv('sql_pass')
sql_hostname = getenv('sql_hostname')
doe_db_name = getenv('doe_db_name')
dsc_db_name = getenv('dsc_db_name')
ad_db_name = getenv('ad_db_name')
student_info_table = getenv('student_info_table')
student_lang_table = getenv('student_lang_table')
allergy_table = getenv('allergy_table')
charter_student_info_table = getenv('charter_student_info_table')
staff_table_name = getenv('staff_table_name')
# File Paths
direct_cert_file_path = getenv('direct_cert_file_path')
titan_staff_final_file = getenv('titan_staff_final_file')
titan_student_final_file = getenv('titan_student_final_file')
# SFTP Vars
final_file_path = Path(getenv('final_file_path'))
titan_hostname = getenv('titan_hostname')
titan_username = getenv('titan_username')
titan_pass = getenv('titan_pass')
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
# Email Alert Vars
alert_to_email = getenv('log_to_email')
alert_subject = "Titan Updater - ERROR ALERT"
smtp_pass = getenv('smtp_pass')
###########

logger.info("Variables Loaded")

# region DB Data Download
### DB Data Download ###
# Create SQL Connection Object - DOE Data
engine = create_engine(f'mysql+pymysql://{sql_username}:{sql_pass}@{sql_hostname}/{doe_db_name}')
# RC Student Info
df_rc_students = pd.read_sql(f'SELECT * FROM {student_info_table}', con=engine)
# RC Student Home Language
df_languages = pd.read_sql(f'SELECT * FROM {student_lang_table}', con=engine)
# Close DOE Data Connection
engine.dispose()
# Create SQL Connection Object - DSC Data
engine = create_engine(f'mysql+pymysql://{sql_username}:{sql_pass}@{sql_hostname}/{dsc_db_name}')
# Charter Student Info
df_charter_students = pd.read_sql(f'SELECT * FROM {charter_student_info_table}', con=engine)
# Allergy Info
df_allergies = pd.read_sql(f'SELECT * FROM {allergy_table}', con=engine)
# Close DSC Data Connection
engine.dispose()
# Create SQL Connection Object - AD Data
engine = create_engine(f'mysql+pymysql://{sql_username}:{sql_pass}@{sql_hostname}/{ad_db_name}')
# Staff Info
df_staff = pd.read_sql(f'SELECT * FROM {staff_table_name}', con=engine)
# Close AD Data Connection
engine.dispose()
################
# endregion 

### Download Urban Promise Data ###
try:
    df_urban_promise = titan_urban_promise_data_download(\
        google_auth_key, \
        urban_promise_sheet_id)
    # Log Entry
    logger.info("Urban Promise Data Downloaded")
except:
    logger.error("!! Error !! - Problem Downloading Urban Promise Data")
################

### Directory Cert File Generator ###
try:
    df_dircerts_final = titan_dircert_file_generator(google_auth_key, 
                                                    nutrition_shared_drive_id,
                                                    direct_cert_shared_folder_id,
                                                    direct_cert_file_path)
    # Log Entry
    logger.info("Direct Cert File Generated")
except:
    logger.error("!! Error !! - Problem Generating Direct Cert File")
################

### Titan Student File Generator ###
try:
    df_student_final = titan_student_file_generator(df_rc_students, 
                                                    df_languages, 
                                                    df_charter_students, 
                                                    df_allergies, 
                                                    df_urban_promise, 
                                                    titan_staff_final_file)
    # Log Entry
    logger.info("Student File Generated")
except:
    logger.error("!! Error !! - Problem Generating Student File")
################

### Titan Staff File Generator ###
try:
    df_staff_final = titan_staff_file_generator(df_staff, 
                                                titan_staff_final_file)
    # Log Entry
    logger.info("Staff File Generated")
except:
    logger.error("!! Error !! - Problem Generating Staff File")
################

### Titan Files Upload ###
upload_files = [f for f in final_file_path.iterdir() if f.is_file()]
try:
    ### Upload Files to Classlink
    with pysftp.Connection(host=titan_hostname,
        username=titan_username,
        password=titan_pass,
        cnopts=cnopts) as sftp:
        for upfile in upload_files:
            sftp.put(str(upfile), upfile.name)
except:
    logger.error("!! Error !! - Problem Uploading Files to Titan")
################

###Alert if Error###
# Add Later
########