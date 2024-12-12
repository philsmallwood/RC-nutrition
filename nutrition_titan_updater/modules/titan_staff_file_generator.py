### RC Titan Staff File Script
### Script to Generate a Staff File 
### to Upload to Titan/LINQ

def titan_staff_file_generator(df_employee_info, titan_staff_final_file):

    ###Import Modules
    import csv
    import pandas as pd
    from datetime import date
    #######

    ### Variables ###
    current_date = date.today()
    staff_date = current_date.strftime('%m/%d/%Y')
    ########

    ### Create Final Dataframe ###
    df_final = pd.DataFrame()
    df_final['EmployeeID'] = 'E' + df_employee_info['employeeID']
    df_final['FirstName'] = df_employee_info['givenName']
    df_final['MiddleName'] = ""
    df_final['LastName'] = df_employee_info['sn']
    df_final['EmailAddress'] = df_employee_info['userPrincipalName'].str.lower()
    df_final['StaffStateID'] = 'E' + df_employee_info['employeeID']
    df_final['Dob'] = df_employee_info['extensionAttribute1']
    df_final['HR_Gender'] = df_employee_info['extensionAttribute9']
    df_final['HR_Location'] = '320' + df_employee_info['departmentNumber'].astype('Int64').astype('str')
    df_final['StaffType'] = 'General'
    df_final['AssignmentStart'] = staff_date
    ########

    ### Format Final DataFrame ###
    # Drop Duplicates
    df_final.drop_duplicates('EmployeeID', inplace=True)
    # Drop Staff with No Location
    df_final = df_final[df_final['HR_Location'] != '320<NA>']
    ########

    ### Export CSV File ###
    df_final.to_csv(titan_staff_final_file, 
                    quoting=csv.QUOTE_ALL,
                    index=False)
    #######

    return df_final