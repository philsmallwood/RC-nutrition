###Python mini script to send emails in other scripts

import sys
import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "scriptmaster@redclay.k12.de.us"
smtp_server = smtplib.SMTP('doverksmtp001.k12.de.us')
receiver_email = sys.argv[1]                           #Needs to be changed per script
subject = sys.argv[2]                                  #Needs to be changed per script
logfile = sys.argv[3]                                    #Needs to be changed per script

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

body = "The script has completed."
message.attach(MIMEText(body, "plain"))

with open(logfile, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

encoders.encode_base64(part)

part.add_header(
    "Content-Disposition",
    f"attachment; filename= {logfile}",
)

message.attach(part)
text = message.as_string()

smtp_server.sendmail(sender_email, receiver_email, text)
