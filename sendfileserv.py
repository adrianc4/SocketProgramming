
# *****************************************************
# Server file, Project 1
# Adrian Charbonneau
# Pauleena Phan
# *****************************************************

import socket
import os
import subprocess


SERVER_PASSWORD = '1234'

def recvAll(sock, numBytes):
	# The buffer
	recvBuff = b""
	
	# The temporary buffer
	tmpBuff = b""
	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
	return recvBuff

def check_password(sock):
	print("Waiting for password...")
	password = sock.recv(1024).decode()
	if password != SERVER_PASSWORD:
		message = "Your password is incorrect, now closing."
		sock.sendall(message.encode())
		return False
	else:
		message = "Your password is correct, open to FTP."
		sock.sendall(message.encode())
	return True

def send_file(sock):
	file_name = clientSock.recv(1024).decode()

	try:
		with open(file_name, 'rb') as file:
			print("Opening file from server")
			file_data = file.read()
			# Send the size of the file first
			file_size_str = str(len(file_data)).zfill(10)  # 10-byte size header
			sock.sendall(file_size_str.encode() + file_data)
			print(f"Sent file {file_name}.")
	except FileNotFoundError:
		print(f"File {file_name} not found. Sending error message to client.")
		error_message = "File not found"
		# Sending error size and message
		sock.sendall(str(len(error_message)).zfill(10).encode() + error_message.encode())

# The port on which to listen
hostname= 'localhost'
listenPort = 1234

# Create a welcome socket. 
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = socket.gethostbyname(hostname)
# Bind the socket to the port
server_add = (server_ip, listenPort)
welcomeSock.bind(server_add)

# Start listening on the socket
welcomeSock.listen(1)

clientSock = 0
# Accept connections forever
while True:
	
	if clientSock == 0:
		print ("Waiting for connections...")
			
		# Accept connections
		clientSock, addr = welcomeSock.accept()
		
		print ("Accepted connection from client: ", addr)
		
		if not check_password(clientSock):
			print("Incorrect password. Closing connection")
			clientSock.close()
			clientSock = 0
			break
		
	print ("\n")


	print("Awaiting commands from client")
	# Receive commands from client
	command = clientSock.recv(1024).decode()

	# Check commands from client and respond accordingly
	if command.lower() == 'get':
		print("Get command received")
		send_file(clientSock)
	elif command.lower() == 'put':
		print("Put command received")
		# The buffer to all data received from the
		# the client.
		fileData = ""
	
		# The temporary buffer to store the received
		# data.
		recvBuff = ""
		
		# The size of the incoming file
		fileSize = 0	
		
		# The buffer containing the file size
		fileSizeBuff = ""
		
		# Receive the first 10 bytes indicating the
		# size of the file
		fileSizeBuff = recvAll(clientSock, 10)
			
		# Get the file size
		fileSize = int(fileSizeBuff)
		
		print ("The file size is ", fileSize)
		
		# Get the file data
		fileData = recvAll(clientSock, fileSize)
		
		print ("The file data is: ")
		print (fileData.decode())

	elif command.lower() == 'ls':
		print("ls command received: \n")
		output = subprocess.getoutput("ls -l")
		print(output)
		clientSock.sendall(output.encode())

	elif command.lower() == 'quit':
		# Close our side
		print("Client has quit")
		clientSock.close()
		clientSock = 0
		break;
	else:
		print("Invalid command received")

	
	
			


print("socket is closed")
	
