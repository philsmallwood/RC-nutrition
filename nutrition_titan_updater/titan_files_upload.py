### RC Titan Files Upload
### Script to upload files the newest to 
### Titan Nutrition Management System
### For keyring, need to set the username/password for sftp sites for downloads and uploads

def titan_files_upload():
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
    #Start Time
    start_time = time.ctime()
    #Log
    log_entry = str()
    #Titan SFTP Vars
    titan_hostname = getenv('titan_hostname')
    titan_username = getenv('titan_username')
    titan_service_name = getenv('titan_service_name')
    #Files
    upload_files = [getenv('titan_student_final_file'),
        getenv('direct_cert_file_path'),
        getenv('staff_final_file')]
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

    return log_entry