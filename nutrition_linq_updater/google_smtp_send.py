def google_smtp_send(receipient_email,
            subject,
            smtp_pass,
            message_attachment='',
            sender_email='scriptmaster@redclayschools.com',
            smtp_server='smtp.gmail.com',
            message_body='The operation has completed.'):

    ### Import Modules ###
    import smtplib
    import ssl
    import os
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    ########

    ### Variables ###
    # Message Vars
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receipient_email
    message["Subject"] = subject
    message.attach(MIMEText(message_body, "plain"))
    # Connection Vars
    smtp_port = 465
    smtp_context = ssl.create_default_context()
        
    ###Add Attachement to Message if Present###
    if message_attachment != '':
        #Open Attachment for Processing
        with open(message_attachment, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        #Encode Attachment for Message
        encoders.encode_base64(part)
        #Add Attachment, Displaying Only the File Name (not full path)
        part.add_header("Content-Disposition",
                    "attachment", 
                    filename=os.path.basename(message_attachment))
        message.attach(part)
    ########

    ###Convert Message for Transit###
    text = message.as_string()
    ########
    
    ### Send Message ###
    with smtplib.SMTP_SSL(smtp_server, 
                        smtp_port, 
                        context=smtp_context) as server:
        server.login(sender_email, smtp_pass)
        server.sendmail(sender_email, receipient_email, text)
    ########
