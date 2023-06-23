# RC-nutrition

### Nutrition Titan Updater

#### Repo: RC-Nutrition
#### Languages: Python

The collection of scripts is related to the Titan Nutrition Management System and involves the creation, formatting, and uploading of files to the Titan SFTP server. The main script, "Titan Update Main Script," calls various sub-scripts to perform specific tasks. The sub-scripts included in this collection are:

1. `titan_files_download.py`: This script downloads the newest copy of the student file for Urban Promise Charter and the Direct Certification Files from the Nutrition Server.
2. `titan_student_file_generator.py`: This script generates a student file with the necessary information for nutrition.  It includes Red Clay, Charter, and Urban Promise students.
3. `titan_dircert_file_prep.py`: This script prepares the Direct Certification Files for processing.
4. `titan_staff_file_generator.py`: This script generates a staff file for the Titan Nutrition Management System.
5. `titan_files_upload.py`: This script uploads the generated files to the Titan Nutrition Management System.

The main script initializes variables, imports required modules, and defines functions for logging.  It then calls each subscript in sequence, capturing the log output for each script. Finally, it writes the complete log to Google Drive and sends an email alert if an error occurs.

Scripts need a configured .env file in the same path.  Envsample file available for settings.  
