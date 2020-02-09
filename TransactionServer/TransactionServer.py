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
import time
from database import Database

# app = Flask(__name__)

# Make a socket for the transaction server
transactionserverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Initialize Database
db = Database()

# command, user=None, stock_sym=None, amount=None, filename=None
def logic(message):
    # this fixes the bug when comparing "amount < 0"
    amount = message.get('amount')

    # remove the decimals and convert to an int
    if amount:
        amount = int(float(amount) * 100)
    print(amount)


    if message['command'] == 'ADD':
#         response_msg = "hi"
#         return response_msg
        if message['amount'] is None:
            response_msg = "No input for Amount"
            # need to audit the error here
        elif amount < 0:
            response_msg = "Attempted to add negative currency"
            # need to audit the error here
        else:
            # select the user
            check_user = db.selectUsers(message['user'])
            print(check_user)

            # if user doesnt exist create the user
            if check_user == None:
                usr_funds = db.changeUsers(message['user'], amount)[1]
            else:
                # get the current funds of the user
                usr_funds = db.selectUsers(message['users'])[1]

                usr_funds += float(format_money(amount))
                print('user funds is:', usr_funds)

            # update the Database with the newly added funds
            db.changeUsers(message['user'], usr_funds)
            response_msg = "Added $%s to %s's account." % (format_money(amount), message['user'])
            # need to audit the transaction here
        return response_msg

    elif message['command'] == 'QUOTE':
        current_quote = get_quote(message)
        print('got current quote')
        print(current_quote)
        response_msg = "Quote for " + str(message['stock_sym']) + ':' + str(current_quote[0])
        print(response_msg)
        return response_msg

    elif message['command'] == 'BUY':
        # print(message['user'] + ', ' + message['stock_sym'] + ', ' + message['amount'])
        #First, check the user balance if they have enough money
        if db.selectUsers(message['user'])[1] >= amount:
            current_quote = get_quote(message)
            curr_price = current_quote[0]

            # calculate the amount user can buy with their funds.
            amountOfStock = int(int(amount) / float(curr_price))
            buy_amt = amountOfStock * float(curr_price)

            remaining_amt = db.selectUsers(message['user'])[1] - buy_amt

            # We need to include the timestamp to know if it is still valid after 60 seconds
            timestamp = int(current_quote[3])

            # set pending buy to latest values of buy and update with timestamp
            db.addPending(message['user'], message['command'], message['stock_sym'], amountOfStock, remaining_amt, timestamp)

            response_msg = "Placed an order to Buy " + str(message['stock_sym']) + ":" + str(curr_price)

        else:
            response_msg = "Not enough funds in user account to purchase stock"

        return response_msg

    elif message['command'] == 'COMMIT_BUY':
        # print(message['user'])
        #Compare time with timestamp
        buy_queue = db.selectPending(message['user'], 'BUY')
        print(buy_queue)
        if buy_queue[5]:
            if curr_time() - 60000 <= int(buy_queue[5]):
                # update with the most recent amount and stock symbol
                amount = buy_queue[4]
                stock_sym = buy_queue[2]
                amountOfStock = buy_queue[3]

                # update the DB using the new amount from above
                db.changeUsers(message['user'], amount)

                # create or update the stock for the user
                db.changeAccount(message['user'], stock_sym, amountOfStock)

                # Delete the pending records
                db.removePending(message['user'], 'BUY')
                response_msg = "Commited most recent BUY order"

            else:
                response_msg = "Time is greater than 60s. Commit buy cancelled."

        else:
            response_msg = "No buy order pending. Cancelled COMMIT BUY."
        return response_msg

    elif message['command'] == 'CANCEL_BUY':
        # print(message['user'])
        db.removePending(message['user'], 'BUY')
        response_msg = "Cancelled Buy"
        return response_msg

    elif message['command'] == 'SELL':
        print(message['user'] + ', ' + message['stock_sym'] + ', ' + message['amount'])
        # # Error checking the amount want to be sold is valid
        # if amount > 0:
        #     # Check the user's records.
        #     if database.select_query(''):
        #         # Sell the amount by updating the DB
        #         database.update('')
        #     else:
        #         response_msg = "Insufficent stock owned"
        # else:
        #     response_msg = "Tried to sell less than 0 shares"
        #
        # return response_msg

    elif message['command'] == 'COMMIT_SELL':
        print(message['user'])
        # Pretty much the same as COMMIT_BUY

    elif message['command'] == 'CANCEL_SELL':
        # print(message['user'])
        db.removePending(message['user'], 'SELL')
        response_msg = "Cancelled Sell"
        return response_msg

    elif message['command'] == 'SET_BUY_AMOUNT':
        print(message['user'] + ', ' + message['stock_sym'] + ', ' + message['amount'])
        # Need to check the user's balance'

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

def curr_time():
    return int(time.time() * 1000)

def format_money(money):
    # return str(int(money)) + '.' + "{:02d}".format(int(money % 10000))
    return str(int(float(money) / 100)) + '.' + "{:02d}".format(int(money % 100))

def get_quote(message):
    quoteserverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # could possibly make this faster by splitting stock symbols up
    quoteserverSocket.connect(('quoteserve.seng.uvic.ca', 4442))
    print('connected to quote server')

    test = str(message['stock_sym'] + ',' + message['user']) + '\n'
    print(test)
    quoteserverSocket.send((str(message['stock_sym'] + ',' + message['user']) + '\n').encode())
    print('sent symbol and user to quote server')
    reply = quoteserverSocket.recv(1024).decode()
    # reply_dict = {'quote': None, 'sym': None, 'userid': None, 'timestamp': None, 'cryptokey': None}
    # split_reply = reply.split(',')
    # reply[0]
    print(type(reply))
    reply = ast.literal_eval(str(reply.split(',')))
    quoteserverSocket.close()
    return reply


# Prepare a server socket
transactionserverSocket.bind(('localhost', 44406))
transactionserverSocket.listen(5)

# Keep sending if there are more commands
while True:
    print('Ready to serve...')
    # Make a socket for the database
    databaseSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # accept returns a pair of client socket and address
    connectionSocket, addr = transactionserverSocket.accept()

    # message from web server
    # ast.literal_eval converts string to dictionary
    message = ast.literal_eval(connectionSocket.recv(4096).decode())
    print(message)

    message = logic(message)

    response = 'returned ' + str(message)
    connectionSocket.sendall(response.encode())
    # close the socket
    connectionSocket.close()

# if __name__ == "__main__":
#     app.run(host='localhost', port=6000)
