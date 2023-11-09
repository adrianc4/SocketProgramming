
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
	print ("USAGE python " + sys.argv[0] + "big.txt" )
	

# Server address
# this is my ip and the port number is the standard one or something
serverAddr = ('192.168.1.21', 21)

# Server port
# serverPort = 1234

# The name of the file
# fileName = "/home/adrian/Assignment1SampleCodes/Python/sendfile/big.txt"
fileName = "small.txt"

# Open the file in binary
fileObj = open(fileName, "rb")

# Create a TCP socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
connSock.connect(serverAddr)

# The number of bytes sent
numSent = 0

# The file data
fileData = None

# Keep sending until all is sent
while True:
	
	user_input = input()
	# this while loop loops teh ls cmd
	while(user_input != "exit"):
		if(user_input == 'ls'):
			lscmd();
		
	# get();

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
	
# Close the socket and the file
connSock.close()
fileObj.close()
	


