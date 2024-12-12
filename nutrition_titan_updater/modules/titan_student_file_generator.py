### RC Titan Student File Generator Script
### Script to Generate a Student File for Titan/Linq
### Includes Red Clay and Charter students

def titan_student_file_generator(df_rc_students,
                                df_languages,
                                df_charter_students,
                                df_allergies,
                                df_urban_promise_students,
                                titan_student_final_file):
    
    ### Import Modules ###
    import csv
    import pandas as pd
    from hashlib import md5
    from datetime import date
    #######

    ##### Variables #####
    # Date
    current_date = date.today()
    earliest_student_date_object = date(2024,8,26)
    student_date = current_date.strftime('%m/%d/%Y')
    earliest_student_start_date = earliest_student_date_object.strftime('%m/%d/%Y')
    # Charter Necessary Columns
    charter_needed_columns = [0, 2, 3, 4, 5, 7, 8, 9, 
        12, 14, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 
        29, 'Street Addr Line & Apt - Physical']
    # Dictionaries for Column Name Changes
    ## Charter Dateframe
    col_names_charter = { 
                0 : 'Current Building',
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
    ## Allergies Dataframe
    col_names_allergies = {
        3 : 'Student Id',
        8 : 'Allergies', 
        9 : 'FoodIntolerance'
    }
    ## Language Dataframe
    col_names_language = {
        0 : 'Student Id', 
        1 : 'Student Language'
    }
    ############

    ### Format DataFrames for Combination ###
    # Allergies
    df_allergies.columns = range(df_allergies.shape[1])
    df_allergies.rename(columns=col_names_allergies, inplace=True)
    # Student Language
    df_languages.columns = range(df_languages.shape[1])
    df_languages.rename(columns=col_names_language, inplace=True)
    # Charter Students
    df_charter_students.columns = range(df_charter_students.shape[1])
    ## Combine Street Address Line 1 and Apartment to match other sources
    df_charter_students['Street Addr Line & Apt - Physical'] = \
        df_charter_students[[19, 20]].apply(lambda x: ', '.join(x.dropna()), axis=1)
    ## Keep the Columns with Necessary Data
    df_charter_students = df_charter_students[charter_needed_columns]
    ## Rename the columns to match other sources for later merging
    df_charter_students.rename(columns=col_names_charter, inplace=True)
    ## Change Charter Race Codes to match Federal Race codes
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
    ## Change Ethnicity to Y or N
    df_charter_students.loc[df_charter_students['Hispanic/Latino Ethnicity'] == \
        'Hispanic', ['Hispanic/Latino Ethnicity']] = 'Y' #Hispanic
    df_charter_students.loc[df_charter_students['Hispanic/Latino Ethnicity'] == \
        'Non-Hispanic', ['Hispanic/Latino Ethnicity']] = 'N' #Non-Hispanic
    # RC Students
    ## Drop Z calendar (320888) and First State School (320530) students
    df_rc_students = df_rc_students[ (df_rc_students['Current Building'] != '888') & \
        (df_rc_students['Current Building'] != '530') ]
    ## Add District Code to Building Number
    df_rc_students['Current Building'] = '320' + df_rc_students['Current Building']
    ############

    ### Combine All Dataframes ###
    # Add Allergies to RC Students
    df_rc_students = df_rc_students.merge(df_allergies[['Student Id', 'Allergies', 'FoodIntolerance']], \
        on = 'Student Id', how = 'left')
    # Add Languages to RC Students
    df_rc_students = df_rc_students.merge(df_languages[['Student Id', \
        'Student Language']], on = 'Student Id', how = 'left')
    # Add Charter Students to Main
    df_rc_and_charter_students = pd.concat([df_rc_students, df_charter_students])
    ############

    ### Final Prep and Upload ### 
    # Reorder to Final Data Frame
    df_final = df_rc_and_charter_students[['Student Id', 'Student First Name', \
        'Student Middle Name', 'Student Last Name', 'Student Generation', \
        'Allergies', 'FoodIntolerance', 'Birthdate', 'Student Gender', 'Federal Race Code', \
        'Hispanic/Latino Ethnicity', 'Alternate Building', 'Current School Year', \
        'Current Building', 'Student Grade', 'Student Homeroom Primary', \
        'Street Addr Line & Apt - Physical', 'City - Physical', \
        'State - Physical', 'Zip - Physical', 'Street Addr Line & Apt - Mailing', \
        'City - Mailing', 'State - Mailing', 'Zip - Mailing', 'First Name - Guardian', \
        'Middle Name - Guardian', 'Last Name - Guardian', 'Mobile Phone', \
        'Home Phone', 'Work Phone', 'Email - Guardian', 'Relation Name - Guardian', \
        'Student Language']].copy()
    # Make Student ID 6-digits
    df_final['Student Id'] = df_final['Student Id'].astype(str).str.zfill(6)
    # Format Current Year
    df_final['Current School Year'] = df_final['Current School Year'].astype(str).str.rstrip('.0')
    df_final['Current School Year'] = df_final['Current School Year'].str.replace("nan","")
    # Make Federal Race Code Single Digit
    df_final['Federal Race Code'] = df_final['Federal Race Code'].str.rstrip('.0')
    df_final['Federal Race Code'] = df_final['Federal Race Code'].fillna("")
    df_final['Federal Race Code'] = df_final['Federal Race Code'].str.replace("nan","")
    # Remove 'Nan'
    df_final['Alternate Building'] = df_final['Alternate Building'].str.replace("nan","")
    # Create Household ID Based on Street Address Using Hashlib.md5
    df_final['HHID'] = df_final['Street Addr Line & Apt - Physical'].\
        apply(lambda x: md5(x.encode()).hexdigest() if x else None)
    # Make HouseHold ID shorter
    df_final['HHID'] = df_final['HHID'].astype(str).str[1:16]
    # Copy Physical Address to Mailing Address if Blank
    df_final['Street Addr Line & Apt - Mailing'] = df_final['Street Addr Line & Apt - Mailing'].\
        fillna(df_final['Street Addr Line & Apt - Physical'])
    df_final['City - Mailing'] = df_final['City - Mailing'].fillna(df_final['City - Physical'])
    df_final['State - Mailing'] = df_final['State - Mailing'].fillna(df_final['State - Physical'])
    df_final['Zip - Mailing'] = df_final['Zip - Mailing'].fillna(df_final['Zip - Physical'])
    # Fill Guardian Relationship as Guardian if Blank
    df_final['Relation Name - Guardian'] = df_final['Relation Name - Guardian'].fillna('Guardian')
    # Add Entry Date
    ## Use the earliest Entry Date if it is before that date
    ## Otherwise, use the current date
    if earliest_student_date_object > current_date:
        df_final['Enrollment Date'] = earliest_student_start_date
    else:
        df_final['Enrollment Date'] = student_date
    ## Add Urban Promise
    df_final = pd.concat([df_final, df_urban_promise_students])
    # Reset Index
    df_final.reset_index(inplace = True, drop = True)
    # Drop Duplicates
    df_final['Student Id'] = df_final['Student Id'].drop_duplicates()
    # Export to data to csv file
    df_final.to_csv(titan_student_final_file, 
                    quoting=csv.QUOTE_ALL,
                    index=False)
    ############

    return df_final