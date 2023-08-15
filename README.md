# RC-nutrition

### Nutrition Titan Updater

#### Repo: RC-Nutrition
#### Languages: Python

The collection of scripts is related to the Titan Nutrition Management System and involves the creation, formatting, and uploading of files to the Titan SFTP server. The main script, "Titan Update Main Script," calls various sub-scripts to perform specific tasks. The sub-scripts included in this collection are:

1. `titan_dircet_file_generator.py`: This script generates a direct certification file by fetching data raw csv files in Google Drive.
2. `titan_student_file_generator.py`: This script generates a student file with the necessary information for nutrition.  It includes Red Clay, Charter, and Urban Promise students.  Urban Promise data is downloaded from Google Drive using the titan_urban_promise_data_download script.
3. `titan_staff_file_generator.py`: This script generates a staff file for the Titan Nutrition Management System.
4. `titan_files_upload.py`: This script uploads the generated files to the Titan Nutrition Management System.

The main script initializes variables, imports required modules, and defines functions for logging.  It then calls each subscript in sequence, capturing the log output for each script. Finally, it writes the complete log to Google Drive and sends an email alert if an error occurs.

Scripts need a configured .env file in the same path.  Envsample file available for settings.  
