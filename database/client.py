from socket import *
s = socket(AF_INET,SOCK_STREAM)
s.connect(("173.183.78.100",80)) # Connect
s.send("'ADD', 'jiosesdo', 100.00") # Send request
data = s.recv(10000) # Get response
s.close()