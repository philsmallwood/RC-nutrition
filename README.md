# RC-nutrition

### Nutrition Titan Updater

#### Repo: RC-Nutrition
#### Languages: Python

The collection of scripts is related to the Titan Nutrition Management System and involves the creation, formatting, and uploading of files to the Titan SFTP server. The main script, "Titan Update Main Script," calls various sub-scripts to perform specific tasks. The sub-scripts included in this collection are:

The main script initializes variables, imports required modules, and defines functions for logging.  It then calls each subscript in sequence, capturing the log output for each script. Finally, it writes the complete log to Google Drive and sends an email alert if an error occurs.

Scripts need a configured .env file in the same path.  Envsample file available for settings.  
