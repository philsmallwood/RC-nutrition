def titan_dircert_file_generator():
    ###Import Modules###
    import pandas as pd
    from io import StringIO
    from os import getenv
    from dotenv import load_dotenv
    from pydrive2.drive import GoogleDrive
    from rc_google_py import login_google_service_account
    #######
    ###Variables###
    #Load .ENV File
    load_dotenv()
    #File Vars
    direct_cert_file_path = getenv('direct_cert_file_path')
    #Google Vars
    google_auth_key = getenv('google_auth_key')
    nutrition_shared_drive_id = getenv('nutrition_shared_drive_id')
    direct_cert_shared_folder_id = getenv('direct_cert_shared_folder_id')
    google_drive_query = f"{direct_cert_shared_folder_id} in parents and trashed=false"
    #Empty Vars
    log_entry = str()
    dircert_file_ids = []
    df_dircerts = pd.DataFrame()
    df_final = pd.DataFrame()
    #######
    ###Authenticate to Google###
    gauth = login_google_service_account(google_auth_key)
    drive = GoogleDrive(gauth)
    #######
    ###Get Direct Cert File Info###
    try:
        #List Files in Direct Cert Shared Folder
        dircert_file_list = drive.ListFile(
            {'q':google_drive_query, 
            'corpora': 'teamDrive', 
            'teamDriveId': nutrition_shared_drive_id, 
            'includeTeamDriveItems': True, 
            'supportsTeamDrives': True}).GetList()
        if len(dircert_file_list) > 0:
            #Get Direct Cert File IDs
            for file in dircert_file_list:
                #Only Grab Files, Not Folders
                if file['mimeType'] != 'application/vnd.google-apps.folder':
                    dircert_file_ids.append(file['id'])
            #Extract Direct Cert Data to DataFrame
            for id in dircert_file_ids:
                file_instance = drive.CreateFile({'id':id})
                file_info = file_instance.GetContentString()
                df_temp = pd.read_csv(StringIO(file_info), skiprows=3)
                df_dircerts = pd.concat([df_temp,df_dircerts])
            #Log Entry
            log_entry += "------------------\n"
            log_entry += "Direct Cert Data Downloaded \n"
            log_entry += "------------------\n"
        else:
            #Log Entry
            log_entry += "------------------\n"
            log_entry += "No Direct Cert Files to Process \n"
            log_entry += "------------------\n"
    except:
        #Error Log Entry
        log_entry += "------------------\n"
        log_entry += "!! Error !! - Problem Downloading Direct Cert Data \n"
        log_entry += "------------------\n"
    #######
    ###Determine Benefit Type###
    df_dircerts.loc[df_dircerts['MedicaidReduced'] == 'Y', 'Type'] = 'Medicaid Reduced'
    df_dircerts.loc[df_dircerts['MedicaidFree'] == 'Y', 'Type'] = 'Medicaid'
    df_dircerts.loc[df_dircerts['PublicAssistance'] == 'Y', 'Type'] = 'TANF'
    df_dircerts.loc[df_dircerts['FoodStamps'] == 'Y', 'Type'] = 'SNAP'
    #######
    ###Final DataFrame###
    #Format Final DataFrame
    df_final['StudentID'] = df_dircerts['StudentID1'].astype(str).str.zfill(6)
    df_final['Type'] = df_dircerts['Type']
    df_final['Entry_Date'] = df_dircerts['Entry_Date']
    #Export Final DataFrame to File
    df_final.to_csv(direct_cert_file_path, index=False)
    #Return Message
    return log_entry

if __name__ == '__main__':
    log_entry = titan_dircert_file_generator()
    print('log_entry')