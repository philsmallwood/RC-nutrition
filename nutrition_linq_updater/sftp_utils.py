### SFTP Utils ###
### Simple Module for Download and Upload via SFTP ###

def sftp_download(hostname, username, password, remote_path, local_path, port=22):
    ### Import Module ###
    import paramiko
    ### Download File ###
    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(remote_path, local_path)
    sftp.close()
    transport.close()

def sftp_upload(hostname, username, password, local_path, remote_path, port=22):
    ### Import Module ###
    import paramiko
    ### Upload File ###
    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_path, remote_path)
    sftp.close()
    transport.close()
