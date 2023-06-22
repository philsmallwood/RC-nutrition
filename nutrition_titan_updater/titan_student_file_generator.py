#!/usr/bin/env python3
###RC Titan Student File Generator Script
###Script to generate a student file with the necesary info for nturition
###Includes Red Clay and Charter students

def titan_student_file_generator():
    ###Import Modules###
    import pandas as pd
    import time
    from os import getenv,environ,execv
    import sys
    from datetime import date
    from dotenv import load_dotenv
    from dfcleanup import df_stripper #Self Created Module
    #######

    ###Turns off the hashseed randomization###
    ###Used to ensure that people with the same address get the same household ID
    ###everytime the script runs
    hashseed = getenv('PYTHONHASHSEED')
    if not hashseed:
        environ['PYTHONHASHSEED'] = '0'
        execv(sys.executable, [sys.executable] + sys.argv)
    #######

    #####Variables#####
    #Load .ENV File
    load_dotenv()
    #Date
    current_date = date.today()
    student_date = current_date.strftime('%m/%d/%Y')
    earliest_student_start_date = '08/29/2023'
    #File Locations
    student_file_path = getenv('localStudentFilePath')
    charter_student_file_path = getenv('localCharterStudentFilePath')
    urban_promise_file_path = getenv('localUrbanPromiseFilePath')
    allergy_file_path = getenv('localAllergyFilePath')
    student_language_file_path = getenv('localStudentLanguageFilePath')
    titan_student_final_file = getenv('localUpStudentFilePath')
    #Charter Necessary Columns
    charter_needed_columns = [0, 2, 3, 4, 5, 7, 8, 9, 
        12, 14, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 
        29, 'Street Addr Line & Apt - Physical']
    ##Set dictionary to rename columns
    #Charter Dateframe
    col_names_charter = { 
                0 : 'Student Building',
                2 : 'Student Id',
                3 : 'Student Last Name',
                4 : 'Student First Name', 
                5 : 'Student Middle Name', 
                7 : 'Student Gender',
                8 : 'Student Homeroom Primary',
                9 : 'Student Grade', 
                12 : 'Birthdate',
                14 : 'Email - Guardian',
                17 : 'Federal Race Code',
                18 : 'Hispanic/Latino Ethnicity',
                21 : 'City - Physical',
                22 : 'State - Physical', 
                23 : 'Zip - Physical', 
                24 : 'First Name - Guardian', 
                25 : 'Last Name - Guardian',
                26 : 'Middle Name - Guardian',
                27 : 'Home Phone', 
                28 : 'Mobile Phone',
                29 : 'Work Phone'}
    #Urban Promise Dateframe
    col_names_urban_promise = { 
                0 : 'Student Building',
                1 : 'Student Id',
                2 : 'Student First Name',
                3 : 'Student Last Name',
                4 : 'Student Grade',
                5 : 'Birthdate',
                6 : 'Allergies',
                7 : 'Street Addr Line & Apt - Physical',
                8 : 'City - Physical',
                9 : 'State - Physical',
                10 : 'Zip - Physical'}
    #Allergies Dataframe
    col_names_allergies = {
        'StudentID':'Student Id'
    }
    #Language Dataframe
    col_names_language = {
        0 : 'Student Id', 
        1 : 'Student Language'
    }
    ############

    ###Read Files into Dataframes###
    #Read RC Student File to Dataframe
    df_rc_students = pd.read_csv(student_file_path, dtype=str)
    df_rc_students = df_stripper(df_rc_students)
    #Read Charter School File to Dataframe
    df_charter_students = pd.read_csv(charter_student_file_path, \
        header=None, skiprows=1, dtype=str, on_bad_lines='skip')
    df_charter_students = df_stripper(df_charter_students)
    #Read Urban Promise File to Dataframe
    #Format Can Be Excel or CSV
    try:
        df_urban_promise_students = pd.read_excel(urban_promise_file_path, \
            skiprows=1, header=None, dtype=str)
        df_urban_promise_students = df_stripper(df_urban_promise_students)
    except:
        df_urban_promise_students = pd.read_csv(urban_promise_file_path, \
            skiprows=1, header=None, dtype=str)
        df_urban_promise_students = df_stripper(df_urban_promise_students)
    #Read Allergies File to Dataframe
    df_allergies = pd.read_csv(allergy_file_path, dtype=str)
    #Rename the StudentID Field in Allergies DataFrame
    df_allergies.rename(columns=col_names_allergies, inplace=True)
    #Read Language File to Dataframe
    df_languages = pd.read_csv(student_language_file_path, dtype=str, \
        header=None, skiprows=1 )
    #Rename the StudentID Field in Languages DataFrame
    df_languages.rename(columns=col_names_language, inplace=True)
    ############

    ###Format Charter schools dataframe###
    ###Combine Street Address Line 1 and Apartment to match other sources
    df_charter_students['Street Addr Line & Apt - Physical'] = \
        df_charter_students[[19, 20]].apply(lambda x: ', '.join(x.dropna()), axis=1)
    ###Keep the Columns with Necessary Data
    df_charter_students = df_charter_students[charter_needed_columns]
    ###Rename the columns to match other sources for later merging
    df_charter_students.rename(columns=col_names_charter, inplace=True)
    ###Change Charter Race codes to match Federal Race codes
    df_charter_students.loc[df_charter_students['Federal Race Code'] == 'Asian', \
        ['Federal Race Code']] = '3' #Asian
    df_charter_students.loc[df_charter_students['Federal Race Code'] == 'White', \
        ['Federal Race Code']] = '6' #Caucasian
    df_charter_students.loc[df_charter_students['Federal Race Code'] == 'Black', \
        ['Federal Race Code']] = '4' #Black/African
    df_charter_students.loc[df_charter_students['Federal Race Code'] == 'Native Am.', \
        ['Federal Race Code']] = '2' #American Indian/Alaskan
    df_charter_students.loc[df_charter_students['Federal Race Code'] == 'Hawaiian', \
        ['Federal Race Code']] = '5' #Native Hawaiian/Other Pacific Islander
    ###Change Ethnicity to Y or N
    df_charter_students.loc[df_charter_students['Hispanic/Latino Ethnicity'] == 'Hispanic', \
        ['Hispanic/Latino Ethnicity']] = 'Y' #Hispanic
    df_charter_students.loc[df_charter_students['Hispanic/Latino Ethnicity'] == 'Non-Hispanic', \
        ['Hispanic/Latino Ethnicity']] = 'N' #Non-Hispanic
    ############

    ###Format Urban Promise dataframe###
    df_urban_promise_students = df_urban_promise_students.loc[df_urban_promise_students[0] == '5544']
    ###Fix date format by making object a 'datetime' format and setting output
    df_urban_promise_students[5] = pd.to_datetime(df_urban_promise_students[5])
    df_urban_promise_students[5] = df_urban_promise_students[5].dt.strftime('%m/%d/%Y')
    ###Add leading zeros to studentID to ensure 6 digits exactly
    df_urban_promise_students[1] = df_urban_promise_students[1].str.zfill(6)
    ###Add leading zeros to Grade to ensure 2 digits exactly
    df_urban_promise_students[4] = df_urban_promise_students[4].str.zfill(2)
    ###Fix Kindergarten Grade
    df_urban_promise_students[4] = df_urban_promise_students[4].str.replace('0K','KN')
    ###Rename columns for final output
    df_urban_promise_students.rename(columns=col_names_urban_promise, inplace=True)
    ############

    ###Format Main Student dataframe###
    ###Drop Z calendar (320888) and First State School (320530) students
    df_rc_students = df_rc_students[ (df_rc_students['Current Building'] != '888') & \
        (df_rc_students['Current Building'] != '530') ]
    df_rc_students['Student Building'] = '320' + df_rc_students['Current Building']
    ############

    ###Combine all of the Dataframes###
    ##Add allergies for RC Students to Main
    df_rc_students = df_rc_students.merge(df_allergies[['Student Id', 'Allergies']], \
        on = 'Student Id', how = 'left')
    ##Add Languages for RC Students to Main
    df_rc_students = df_rc_students.merge(df_languages[['Student Id', 'Student Language']], \
        on = 'Student Id', how = 'left')
    ##Add Charter Students to Main
    df_rc_and_charter_students = df_rc_students.merge(df_charter_students, how = 'outer')
    ##Add Urban Promise Students to Main
    df_all_students = df_rc_and_charter_students.merge(df_urban_promise_students, how = 'outer')
    ############

    ###Final Prep and Upload### 
    ###Reorder to Final Data Frame
    df_final = df_all_students[['Student Id', 'Student First Name', 'Student Middle Name', \
        'Student Last Name', 'Student Generation', 'Allergies', 'Birthdate', 'Student Gender', \
        'Federal Race Code', 'Hispanic/Latino Ethnicity', 'Alternate Building', \
        'Current School Year', 'Student Building', 'Student Grade', 'Student Homeroom Primary', \
        'Street Addr Line & Apt - Physical', 'City - Physical', 'State - Physical', 'Zip - Physical', \
        'Street Addr Line & Apt - Mailing', 'City - Mailing', 'State - Mailing', 'Zip - Mailing', \
        'First Name - Guardian', 'Middle Name - Guardian', 'Last Name - Guardian', 'Mobile Phone', \
        'Home Phone', 'Work Phone', 'Email - Guardian', 'Relation Name - Guardian', 'Student Language']].copy()

    ###Create Household ID based on Street Address
    df_final['HHID'] = df_final['Street Addr Line & Apt - Physical'].map(hash)
    ###Make HouseHold ID shorter
    df_final['HHID'] = df_final['HHID'].astype(str).str[1:16]

    ###Copy Physical Address to Mailing Address if Blank
    df_final['Street Addr Line & Apt - Mailing'].fillna(\
        df_final['Street Addr Line & Apt - Physical'], inplace=True)
    df_final['City - Mailing'].fillna(df_final['City - Physical'], inplace=True)
    df_final['State - Mailing'].fillna(df_final['State - Physical'], inplace=True)
    df_final['Zip - Mailing'].fillna(df_final['Zip - Physical'], inplace=True)

    ###Fill Guardian Relationship as Guardian if Blank
    df_final['Relation Name - Guardian'].fillna('Guardian', inplace=True)

    ###Add Entry Date
    ##Use the earliest Entry Date if it is before that date
    ##Otherwise, use the current date
    if earliest_student_start_date > student_date:
        df_final['Enrollment Date'] = earliest_student_start_date
    else:
        df_final['Enrollment Date'] = student_date

    ###Export to data to csv file
    df_final.to_csv(titan_student_final_file, index=False)
    ############