from socket import *
import pickle

audit_client = socket(AF_INET, SOCK_STREAM)
audit_client.connect(('localhost', 44409))
msg = {'command': 'ADD', 'user': 'parmj', 'amount': 200.00}

audit_client.send(pickle.dumps(msg))

reply = audit_client.recv(1024)

print(reply.decode())

audit_client.close()