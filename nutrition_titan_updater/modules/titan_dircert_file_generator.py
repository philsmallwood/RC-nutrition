def titan_dircert_file_generator(google_auth_key, 
                                nutrition_shared_drive_id,
                                direct_cert_shared_folder_id,
                                direct_cert_file_path):
    
    ### Import Modules ###
    import pandas as pd
    from io import StringIO
    from pydrive2.drive import GoogleDrive
    from rc_google_py import login_google_service_account
    #######

    ### Variables ###
    google_drive_query = f"'{direct_cert_shared_folder_id}' in parents and trashed=false"
    # Empty Vars
    dircert_file_ids = []
    df_dircerts = pd.DataFrame()
    df_final = pd.DataFrame()
    #######

    ### Authenticate to Google ###
    gauth = login_google_service_account(google_auth_key)
    drive = GoogleDrive(gauth)
    #######

    ### Get Direct Cert File Info ###
    try:
        # List Files in Direct Cert Shared Folder
        dircert_file_list = drive.ListFile(
            {'q':google_drive_query, 
            'corpora': 'teamDrive', 
            'teamDriveId': nutrition_shared_drive_id, 
            'includeTeamDriveItems': True, 
            'supportsTeamDrives': True}).GetList()
        if len(dircert_file_list) > 0:
            # Get Direct Cert File IDs
            for file in dircert_file_list:
                # Only Grab Files, Not Folders
                if file['mimeType'] != 'application/vnd.google-apps.folder':
                    dircert_file_ids.append(file['id'])
            # Extract Direct Cert Data to DataFrame
            for id in dircert_file_ids:
                file_instance = drive.CreateFile({'id':id})
                file_info = file_instance.GetContentString()
                df_temp = pd.read_csv(StringIO(file_info), skiprows=3, dtype=str)
                df_dircerts = pd.concat([df_temp,df_dircerts])
    except:
        pass
    #######

    ### Determine Benefit Type ###
    df_dircerts.loc[df_dircerts['MedicaidReduced'] == 'Y', 'Type'] = 'Medicaid Reduced'
    df_dircerts.loc[df_dircerts['MedicaidFree'] == 'Y', 'Type'] = 'Medicaid'
    df_dircerts.loc[df_dircerts['PublicAssistance'] == 'Y', 'Type'] = 'TANF'
    df_dircerts.loc[df_dircerts['FoodStamps'] == 'Y', 'Type'] = 'SNAP'
    #######

    ### Final DataFrame ###
    # Format Final DataFrame
    df_final['StudentID'] = df_dircerts['StudentID1'].astype(str).str.zfill(6)
    df_final['Type'] = df_dircerts['Type']
    df_final['Entry_Date'] = pd.to_datetime(df_dircerts['Entry_Date'])
    df_final['Entry_Date'] = df_final['Entry_Date'].dt.strftime('%m/%d/%Y')
    # Drop Duplicates
    df_final.drop_duplicates(inplace=True)
    # Export Final DataFrame to File
    df_final.to_csv(direct_cert_file_path, index=False)
    # Return Message

    return df_final
    #return f"Direct Cert File Generated: {direct_cert_file_path}"