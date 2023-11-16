
# *******************************************************************
# This file illustrates how to send a file using an
# application-level protocol where the first 10 bytes
# of the message from client to server contain the file
# size and the rest contain the file data.
# *******************************************************************
import socket
import os
import sys


from cmds import *

# Command line checks 
if len(sys.argv) < 2:
	print ("USAGE python " + sys.argv[0] + " Connection" )
	
	

# Server address
serverAddr = '0.0.0.0'

# Server port
serverPort = 1234

# server_ip = socket.gethostbyname(server_hostname)

# Create a TCP socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
connSock.connect((serverAddr, serverPort))
# print(f"Connected to {server_hostname} ({server_ip}) on port {serverPort}")

# The number of bytes sent
numSent = 0

# The file data
fileData = None

print(f"Commands: \n", "ftp> get <filename> \n ftp> put <filename> \n ftp> ls \n ftp> quit")
# Keep sending until all is sent
while True:
	
	print(f"ftp>")
	user_input = input()
	if(user_input == 'ls'):
		lscmd();
	elif(user_input == 'put'):
		print(f'Enter filename:')
		# The name of the file
		fileName = input()

		# Open the file in binary
		fileObj = open(fileName, "rb")
		# Read 65536 bytes of data
		fileData = fileObj.read(65536)
		
		# Make sure we did not hit EOF
		if fileData:
			
				
			# Get the size of the data read
			# and convert it to string
			dataSizeStr = str(len(fileData))
			
			# Prepend 0's to the size string
			# until the size is 10 bytes
			while len(dataSizeStr) < 10:
				dataSizeStr = "0" + dataSizeStr
		
			dataSizeBytes = dataSizeStr.encode()
			fileData = dataSizeBytes + fileData

			# Prepend the size of the data to the
			# file data.


			# The number of bytes sent
			numSent = 0
			# Send the data!
			while len(fileData) > numSent:
				numSent += connSock.send(fileData[numSent:])
	
		# The file has been read. We are done
		else:
			break
		print ("Sent ", numSent, " bytes.")
	elif(user_input == 'quit'):
		break


	
# Close the socket and the file
connSock.close()
fileObj.close()
	


