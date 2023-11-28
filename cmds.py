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

def checkLogin():
	login = False
	while(login == False):
		print(f"Please Enter Username:")
		username_input = input()
		print(f"Please Enter Password:")
		password_input = input()

		if(username_input != "student" or password_input != "1234"):
			print(f"Try Again")
		else:
			login = True
