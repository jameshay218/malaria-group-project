#!/usr/bin/python

import sys
import os
import cgi
import cgitb; cgitb.enable()
import paramiko as pm
import Image
import ImageDraw
from PIL import ImageFont

print("Content-Type: text/plain\n\n")

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
image_source = '/home/guest/Desktop/tree.jpg'
image_dest = '/homes/ml3613/GroupProject/group-project/Matthew/venv/temp/images/image.jpeg'

results_source = '/homes/ml3613/GroupProject/group-project/Matthew/venv/temp/results/csvresults'
results_dest = '/home/guest/group-project/William/cgi-bin/query/results/'

#constants for the Grid function
lineFill = (43, 58, 66)
lineWidth = 2
fontSize = 25


class Paramiko():
    def runTestScript(self):
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
            t.connect(username=USER, password=PASSWORD)
            sftp = pm.SFTPClient.from_transport(t)
            sftp.put(filepath, image_dest)
        finally:
            t.close()

    def SCPFileFrom(self, resultPath): 
        try:
            t = pm.Transport((hostname, port))
            t.connect(username=USER, password=PASSWORD)
            sftp = pm.SFTPClient.from_transport(t)
            sftp.get(results_source, resultPath)
        finally:
            t.close()

    def Grid(self, imagePath, resultsPath):
        img = Image.open(imagePath)
        width, height = img.size

        numW = int(width/256)
        #print 'numW is ' + `numW`
        numH = int(height/256)
        #print 'numH is ' + `numH`
        offW = int((width%256)/2)
        offH = int((height%256)/2)
        
        draw = ImageDraw.Draw(img)
        # get font 
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",25)
        textOff = 80
    
        # draw grid on Image
        for x in range (0, numH + 1):
            draw.line((offW, offH + x*256, offW + numW*256, offH + 256*x), fill=lineFill, width=lineWidth)

        for x in range (0, numW + 1):
            draw.line((offW + x*256, offH, offW + x*256, offH + 256*numH), fill=lineFill, width=lineWidth)

        #open csv file to read results
            results = open(resultsPath, 'r')
        
        #discard first line
            line = results.readline()

        # draw Image labels
            for x in range (0, numH):
                for y in range(0, numW):
                    line = results.readline()
                    if 'pos' in line:
                        draw.text((offW + textOff + 256*y, offH + 120 + 256*x), "Positive", (231,76,60), font=font)
                    elif 'neg' in line:
                        draw.text((offW + textOff + 256*y, offH + 120 + 256*x), "Negative", (63,101,69), font=font)
        
        img.save(imagePath)
        
    def infected(self, resultsFile):
        results = open(resultsFile, 'r')
        isPos = False

        for line in results:
            if 'pos' in line:
                isPos = True
        return isPos
    


    def Query(self, filepath):
        #first check format of filename
        #split filename into name and extension
        name, ext = os.path.splitext(filepath)
        #print 'name is ' + `name`
        #print 'extension  is ' + `ext`


        im = Image.open(filepath)
        fileName = os.path.basename(name)
       
        directoryName = os.path.dirname(name)
        directoryName = directoryName + '/tmp/'

        d = os.path.dirname(directoryName)
        if not os.path.exists(d):
            os.makedirs(d)        
        
        filepath = directoryName + fileName + '.jpeg'
        im.save(filepath)
        #print 'new filepath is ' + `filepath`

        
        #scp the file
        print 'sending the image file'
        self.SCPFileTo(filepath)
 
        #run the query script
        print 'running the query script'
        self.runTestScript()

        #scp back the results file
        print 'receiving the results file'

        resultsFile = directoryName + fileName + '.csv'
        print 'the results file will be' + `resultsFile`
        self.SCPFileFrom(resultsFile)

        self.Grid(filepath, resultsFile)

        isPositive = self.infected(resultsFile)
        
        print 'is the image positive ' +  `isPositive`

        return(filepath, isPositive)
        
        
def main():
    test = Paramiko()
    filep, b = test.Query('images/1.jpg')
    print filep
    print b
if __name__ == "__main__":
    main()


