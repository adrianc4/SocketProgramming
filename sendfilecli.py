
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
	print ("USAGE python " + sys.argv[0] + " Connection" )
	
def put_file(socket):
	# The name of the file
	fileName = input('Enter filename:')

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

	# Send File name to server
	file_name = input("Enter file name: ")
	socket.sendall(file_name.encode())
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

# Password check
password = input("Enter Server password: ")
connSock.sendall(password.encode())

response = connSock.recv(1024).decode()
if response:
	print("Server says:", response)
	if "incorrect" in response.lower():
		connSock.close()
		sys.exit(1)

		
# The number of bytes sent
numSent = 0

# The file data
fileData = None

print(f"Commands: \n", "ftp> get <filename> \n ftp> put <filename> \n ftp> ls \n ftp> quit")
# Keep sending until all is sent
while True:
	
	user_input = input("ftp> ")

	if(user_input == 'ls'):
		connSock.sendall(user_input.encode())
		response = connSock.recv(4096).decode()
		print(response)
	
	elif(user_input == 'put'):
		connSock.sendall(user_input.encode())

		put_file(connSock)

	elif(user_input == 'get'):
		# Send get request to server
		connSock.sendall(user_input.encode())

		recieve_file(connSock)

	elif(user_input == 'quit'):
		connSock.sendall(user_input.encode())
		# Close the socket and the file
		connSock.close()
		break

	else:
		print("Unknown command \n")

	
	


