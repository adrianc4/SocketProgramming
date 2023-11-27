
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
	
def put_file(socket):
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
	print ("Sent ", numSent, " bytes.")
	fileObj.close()

def recieve_file(socket):
	print("Enter file name: ")
	file_name = input()
	file_size_str = socket.recv(10).decode()
	if not file_size_str:
		print("No response")
		return
	
	file_size = int(file_size_str)

	with open(file_name, 'wb') as file:
		remaining = file_size
		while remaining:
			chunk_size = 4096 if remaining >= 4096 else remaining
			chunk = socket.recv(chunk_size)
			if not chunk:
				break
			file.write(chunk)
			remaining -= len(chunk)
		print(f"File {file_name} recieved successfully.")

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

username = "chicken"
password = "feet"

# client login attempts
login_tries = 0
while(login_tries < 3):
	print(f"Please Enter Username:")
	username_input = input()
	print(f"Please Enter Password:")
	password_input = input()

	# checking the client input login
	if(username_input != username or password_input != password):
		print(f"Login is incorrect. Please try again")
		login_tries += 1
		print(login_tries)
	else:
		login_tries = 4

# After 3 failed attempts the client's connection will break
if(login_tries == 3):
	print(f"Too many failed attempts. Please try again later")

# If the client failed less than 3 times they will be able to connect
elif(login_tries == 4):
	print(f"Commands: \n", "ftp> get <filename> \n ftp> put <filename> \n ftp> ls \n ftp> quit")
	# Keep sending until all is sent
	while True:
		
		print(f"ftp>")
		user_input = input()
		if(user_input == 'ls'):
			lscmd();
		elif(user_input == 'put'):
			put_file(connSock)
		elif(user_input == 'get'):
			recieve_file(connSock)
		elif(user_input == 'quit'):
			break
		else:
			print("Unknown command")

	
# Close the socket and the file
connSock.close()
	


