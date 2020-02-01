#!/usr/bin/python           # This is server.py file

# import socket               # Import socket module
# import _thread
#
# def on_new_client(clientsocket,addr):
#     while True:
#         msg = clientsocket.recv(1024)
#         #do some checks and if msg == someWeirdSignal: break:
#         print (addr, ' >> ', msg)
#         msg = raw_input('SERVER >> ')
#         #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
#         clientsocket.send(msg)
#     clientsocket.close()
#
# s = socket.socket()         # Create a socket object
# host = socket.gethostname() # Get local machine name
# port = 50000                # Reserve a port for your service.
#
# print ('Server started!')
# print ('Waiting for clients...')
#
# s.bind((host, port))        # Bind to the port
# s.listen(5)                 # Now wait for client connection.
#
# while True:
#    c, addr = s.accept()     # Establish connection with client.
#    print ('Got connection from', addr)
#    _thread.start_new_thread(on_new_client,(c,addr))
#    #that's how you pass arguments to functions when creating new threads using thread module.
# s.close()


# from flask import Flask
import socket
import ast
import pickle
# app = Flask(__name__)

# Make a socket for the transaction server
transactionserverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#command, user=None, stock_sym=None, amount=None, filename=None
def logic(message):
    if message['command'] == 'ADD':
        print(message['user'] + ', ' + message['amount'])
        # if message['amount'] is None:
        #     response_msg = "No input for Amount"
        #     # need to audit the error here
        # elif message['amount'] < 0:
        #     response_msg = "Attempted to add negative currency"
        #     # need to audit the error here
        # else:
        #     # need to update the user's bank balance in DB by adding the amount
        #     response_msg = "Added $%s to %s's account." % (format_money(message['amount']), message['user'])
        #     # need to audit the transaction here
        # return response_msg

    elif message['command'] == 'QUOTE':
        # print(message['user'] + ', ' + message['stock_sym'])
        current_quote = get_quote(message)
        response_msg = "Quote for " + str(message['stock_sym']) + ':' + str(current_quote[0])
        print(response_msg)
        return response_msg

    elif message['command'] == 'BUY':
        print(message['user'] + ', ' + message['stock_sym'] + ', ' + message['amount'])
    elif message['command'] == 'COMMIT_BUY':
        print(message['user'])
    elif message['command'] == 'CANCEL_BUY':
        print(message['user'])
    elif message['command'] == 'SELL':
        print(message['user'] + ', ' + message['stock_sym'] + ', ' + message['amount'])
    elif message['command'] == 'COMMIT_SELL':
        print(message['user'])
    elif message['command'] == 'CANCEL_SELL':
        print(message['user'])
    elif message['command'] == 'SET_BUY_AMOUNT':
        print(message['user'] + ', ' + message['stock_sym'] + ', ' + message['amount'])
    elif message['command'] == 'SET_BUY_TRIGGER':
        print(message['user'] + ', ' + message['stock_sym'] + ', ' + message['amount'])
    elif message['command'] == 'CANCEL_SET_BUY':
        print(message['user'] + ', ' + message['stock_sym'])
    elif message['command'] == 'SET_SELL_AMOUNT':
        print(message['user'] + ', ' + message['stock_sym'] + ', ' + message['amount'])
    elif message['command'] == 'SET_SELL_TRIGGER':
        print(message['user'] + ', ' + message['stock_sym'] + ', ' + message['amount'])
    elif message['command'] == 'CANCEL_SET_SELL':
        print(message['user'] + ', ' + message['stock_sym'])
    elif message['command'] == 'DUMPLOG':
        print(message['user'] + ', ' + message.get('filename', ''))
    elif message['command'] == 'CANCEL_SET_SELL':
        print(message['user'] + ', ' + message['stock_sym'])
    else:
        print('problem')

def format_money(money):
    return str(int(float(money)/100)) + '.' + "{:02d}".format(int(money%100))

def get_quote(message):
    quoteserverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # could possibly make this faster by splitting stock symbols up
    quoteserverSocket.connect(('quoteserve.seng.uvic.ca', 4442))
    print('connected to quote server')
    quoteserverSocket.send(str(message['stock_sym'] + ',' + message['user']) + '\n')
    print('sent symbol and user to quote server')
    reply = quoteserverSocket.recv(1024)
    # reply_dict = {'quote': None, 'sym': None, 'userid': None, 'timestamp': None, 'cryptokey': None}
    # split_reply = reply.split(',')
    # reply[0]
    reply = ast.literal_eval(str(reply.split(',')))
    quoteserverSocket.close()
    return reply

# Prepare a server socket
transactionserverSocket.bind(('localhost', 44406))
transactionserverSocket.listen(5)

# Keep sending if there are more commands
while True:
    print('Ready to serve...')

    # Make a socket for the quoteserver
    #quoteserverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Make a socket for the database
    databaseSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # accept returns a pair of client socket and address
    connectionSocket, addr = transactionserverSocket.accept()


    # message from web server
    # ast.literal_eval converts string to dictionary
    message = ast.literal_eval(connectionSocket.recv(4096).decode())

    message = logic(message)

    response = 'returned ' + str(message)
    connectionSocket.sendall(response.encode())
    # close the socket
    connectionSocket.close()
