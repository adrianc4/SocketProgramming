# *********************************************************************
# This file illustrates how to execute a command and get it's output
# *********************************************************************
# import commands
from ftplib import FTP
import subprocess



# ftp = FTP('192.168.1.21')

# Run ls command, get output, and print it
def lscmd():
	for line in subprocess.getstatusoutput('ls -l'):
		print (line)


