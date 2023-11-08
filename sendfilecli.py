
# *******************************************************************
# This file illustrates how to send a file using an
# application-level protocol where the first 10 bytes
# of the message from client to server contain the file
# size and the rest contain the file data.
# *******************************************************************
import socket
import os
import sys

# Command line checks 
if len(sys.argv) < 2:
	print ("USAGE python " + sys.argv[0] + " /home/adrian/Assignment1SampleCodes/Python/sendfile/big.txt" )
	

# Server address
serverAddr = "localhost"

# Server port
serverPort = 1234

# The name of the file
fileName = "/home/adrian/Assignment1SampleCodes/Python/sendfile/big.txt"

# Open the file in binary
fileObj = open(fileName, "rb")

# Create a TCP socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
connSock.connect((serverAddr, serverPort))

# The number of bytes sent
numSent = 0

# The file data
fileData = None

# Keep sending until all is sent
while True:
	
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
	


