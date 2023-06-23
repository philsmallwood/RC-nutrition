### RC Titan Files Upload
### Script to upload files the newest to 
### Titan Nutrition Management System

def titan_files_upload():
    ###Import Modules
    import pysftp
    import time
    from dotenv import load_dotenv
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
    titan_pass = getenv('titan_pass')
    #Files
    upload_files = [getenv('titan_student_final_file'),
        getenv('direct_cert_file_path'),
        getenv('staff_final_file')]
    #######

    ###Upload Files to Classlink
    with pysftp.Connection(host=titan_hostname, \
        username=titan_username, \
        password=titan_pass) as sftp:
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