def titan_urban_promise_data_download(google_auth_key, urban_promise_sheet_id):
    
    ### Import Modules ###
    import pandas as pd
    from rc_google_py import download_gsheet_to_df
    #######

    ###Get Urban Promise Student Data###
    try:
        # Download Urban Promise Data from Google Sheets
        df_urban_promise = download_gsheet_to_df(\
            google_auth_key, \
            urban_promise_sheet_id)
            ###Data Cleanup###
        # Format Student IDs to 6-digits
        df_urban_promise['Student Id'] = df_urban_promise['Student Id'].\
            astype(str).str.zfill(6)
        # Format Student Grade to 2-digits
        df_urban_promise['Student Grade'] = df_urban_promise['Student Grade'].\
            astype(str).str.zfill(2)
        # Fix Kindergarten Grade
        df_urban_promise['Student Grade'] = df_urban_promise['Student Grade'].\
            str.replace('0K','KN')
        # Format DoB to MM/DD/YYYY
        df_urban_promise['Birthdate'] = pd.to_datetime(df_urban_promise['Birthdate'], \
            format='mixed')
        df_urban_promise['Birthdate'] = df_urban_promise['Birthdate']\
            .dt.strftime('%m/%d/%Y')
    except:
        df_urban_promise = pd.DataFrame()
    #######

    return df_urban_promise
