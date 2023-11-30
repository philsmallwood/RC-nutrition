def titan_urban_promise_data_download():
    ###Import Modules###
    import pandas as pd
    from os import getenv
    from dotenv import load_dotenv
    from rc_google_py import download_gsheet_to_df
    #######

    ###Variables###
    #Load .ENV File
    load_dotenv()
    #Google Vars
    google_auth_key = getenv('google_auth_key')
    urban_promise_sheet_id = getenv('urban_promise_sheet_id')
    #Empty Vars
    log_entry = str()
    #######

    ###Get Urban Promise Student Data###
    try:
        df_urban_promise = download_gsheet_to_df(\
            google_auth_key, \
            urban_promise_sheet_id)
        #Log Entry
        log_entry += "------------------\n"
        log_entry += "Urban Promise Data Downloaded \n"
        log_entry += "------------------\n"
    except:
        #Error Log Entry
        log_entry += "------------------\n"
        log_entry += "!! Error !! - Problem Downloading Urban Promise Data \n"
        log_entry += "------------------\n"
    #######
    ###Data Cleanup###
    #Format Student IDs to 6-digits
    df_urban_promise['Student Id'] = df_urban_promise['Student Id'].\
        astype(str).str.zfill(6)
    #Format Student Grade to 2-digits
    df_urban_promise['Student Grade'] = df_urban_promise['Student Grade'].\
        astype(str).str.zfill(2)
    #Fix Kindergarten Grade
    df_urban_promise['Student Grade'] = df_urban_promise['Student Grade'].\
        str.replace('0K','KN')
    #Format Date
    df_urban_promise['Birthdate'] = pd.to_datetime(df_urban_promise['Birthdate'], \
        format='mixed')
    df_urban_promise['Birthdate'] = df_urban_promise['Birthdate']\
        .dt.strftime('%m/%d/%Y')
    #######
    return df_urban_promise, log_entry
