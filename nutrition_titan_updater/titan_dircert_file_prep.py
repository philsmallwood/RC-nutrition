#!/usr/bin/env python3
###RC Titan DirectCert Script
###Script to process Direct Cert files and upload to Titan

def titan_dircert_file_prep():

    ###Import Modules###
    import pandas as pd
    from os import getenv,rename,listdir
    from dotenv import load_dotenv
    from datetime import date
    #######

    #####Variables#####
    #Load .ENV File
    load_dotenv()
    #Date
    current_date = date.today()
    date_str = current_date.strftime('%m-%d-%Y')
    #File Vars
    nutrition_direct_cert_path = getenv('nutrition_direct_cert_path')
    archive_path = getenv('archive_path')
    direct_cert_file_path = getenv('direct_cert_file_path')
    archive_dircect_cert_file = f"{archive_path}dircertupload-{date_str}.csv"
    #Empty Dataframe to Start
    df_dircerts = pd.DataFrame()
    #Log
    log_entry = str()
    #######

    ###Read Direct Cert Files into a Dataframe###
    localNutritionDirCertFiles = listdir(nutrition_direct_cert_path)
    if not localNutritionDirCertFiles:
        #Logging No New Files
        log_entry += "------------------\n"
        log_entry += "No New Direct Cert Files to Process \n"
        log_entry +="------------------\n"
    else:
        for certFile in localNutritionDirCertFiles:
            try:
                df_temp = pd.read_csv(nutrition_direct_cert_path+certFile, sep='\t', skiprows=3, dtype=str, encoding='utf-16')
                df_dircerts = pd.concat([df_dircerts,df_temp])
                rename(nutrition_direct_cert_path+certFile,archive_path+certFile)
            except UnicodeError:
                df_temp = pd.read_csv(nutrition_direct_cert_path+certFile, skiprows=3, dtype=str)
                df_dircerts = pd.concat([df_dircerts,df_temp])
                continue
            except:
               #Logging
                log_entry += "------------------\n"
                log_entry += "Files Could Not Be Processed \n"
                log_entry += "------------------\n"
                break
    #######

    ###Final Dataframe###
    if not df_dircerts.empty:
        #Archive Old Direct Cert Titan File
        rename(direct_cert_file_path,archive_dircect_cert_file)
        #Create Empty Final Dataframe
        df_final = pd.DataFrame()
        #Add Necessary Data
        df_final['StudentID'] = df_dircerts['StudentID'].str.zfill(6)
        df_final['Type'] = df_dircerts['FoodStamps']
        df_final['Entry_Date'] = df_dircerts['Entry_Date']
        #Format Eligibility Type
        df_final.loc[df_final['Type'] ==  'Y', ['Type']] = 'SNAP'
        df_final.loc[df_final['Type'] ==  'N', ['Type']] = 'TANF'
        #Export File for Titan###
        df_final.to_csv(direct_cert_file_path, index=False)
    #######

    return log_entry