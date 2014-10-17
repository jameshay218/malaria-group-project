#!/usr/bin/python

import sys
import os
import cgi
import cgitb; cgitb.enable()
import paramiko as pm

#print("Content-Type: text/plain\n\n")

class AllowAllKeys(pm.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        return

HOST = 'shell4.doc.ic.ac.uk'
USER = 'ml3613'
PASSWORD = 'Kadir200'

hostname = 'shell4.doc.ic.ac.uk'
password = 'Parasight1'
username = "ksm113"
port = 22
image_source = '/homes/ksm113/Desktop/logotrans.png'
image_dest = '/homes/ksm113/testspace/logotrans.jpeg'

class Paramiko():
    def testSSH():
        client = pm.SSHClient()
        client.load_system_host_keys()
        #client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        client.set_missing_host_key_policy(AllowAllKeys())
        client.connect(HOST, username=USER, password=PASSWORD)

        channel = client.invoke_shell()
        stdin = channel.makefile('wb')
        stdout = channel.makefile('rb')

        #ENTER COMMANDS HERE
        stdin.write('''
        hostname
        cd ~/GroupProject/group-project/Matthew/venv/
        sh webbatcher.sh
        exit
        ''')

        result = stdout.readlines()
        for line in result: 
            print line
        #print stdout.read()

        stdout.close()
        stdin.close()
        client.close()

#Scp script to get a file from the source to the webserver
#Change to sftp.put if sending a file from web server to source
    def SCPFileTo(self, filepath):
        try:
            t = pm.Transport((hostname, port))
            t.connect(username=username, password=password)
            sftp = pm.SFTPClient.from_transport(t)
            sftp.put(filepath, image_dest)

        finally:
            t.close()

    def SCPFileFrom(self): 
        try:
            t = pm.Transport((hostname, port))
            t.connect(username=USER, password=PASSWORD)
            sftp = pm.SFTPClient.from_transport(t)
            sftp.get(dest, source)

        finally:
            t.close()

def main():
    #check if the image file exists
    #if not (os.path.isfile('query/test.jpg') or os.path.isfile('query/test.png')):
    #    print('The file does not exist')
    #    return;

    #If the file is a .png, convert to jpeg
    #if (os.path.isfile())
    
    filepath = '/homes/ksm113/testspace/logotrans.png'

    print("starting")
    test = Paramiko()
    test.SCPFileTo(filepath)
    #test.testSSH()
    print("done")

if __name__ == "__main__":
    main()


