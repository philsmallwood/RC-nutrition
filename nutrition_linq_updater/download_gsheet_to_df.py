# Module to Download Information from a Google 
# Sheet to a Dictionary
def download_gsheet_to_df(google_auth_key, 
    google_sheet_id, sheet_name='Sheet1'):
    ###Import Modules Needed for Function###
    import pandas as pd
    import gspread
    from google.oauth2.service_account import Credentials
    #Google Variables
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    google_credentials = Credentials.from_service_account_file(google_auth_key, scopes=scope)
    ##Get Data
    gclient = gspread.authorize(google_credentials)
    workbook = gclient.open_by_key(google_sheet_id)
    worksheet = workbook.worksheet(sheet_name)
    records = worksheet.get_all_records()
    #Load Records into DataFrame
    df = pd.DataFrame.from_dict(records)
    ##Return DataFrame
    return df