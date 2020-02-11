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
    print("amount is seen as ", amount)


    if message['command'] == 'ADD':
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
                usr_funds = db.selectUsers(message['user'])[1]
                usr_funds = float(format_money(usr_funds)) + float(format_money(amount))
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
        if buy_queue is not None:
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
        # print(message['user'] + ', ' + message['stock_sym'] + ', ' + message['amount'])
        # Error checking the amount want to be sold is valid
        if amount > 0:
            # Check the user's records.
            if db.selectUsers(message['user'])[1] >= amount:
                current_quote = get_quote(message)
                curr_price = current_quote[0]

                # Calcualtes exactly how much I am able to sell
                amountOfStock = int(int(amount) / float(curr_price))
                sell_amt = amountOfStock * float(curr_price)
                remaining_amt = db.selectUsers(message['user'])[1] + sell_amt
                timestamp = int(current_quote[3])

                # Sell the amount by updating the DB
                db.addPending(message['user'], message['command'], message['stock_sym'], amountOfStock, remaining_amt, timestamp)
                response_msg = "Placed an order to Sell " + str(message['stock_sym']) + ":" + str(curr_price)
            else:
                response_msg = "Insufficent stock owned"
        else:
            response_msg = "Tried to sell less than 0 shares"

        return response_msg

    elif message['command'] == 'COMMIT_SELL':
        # print(message['user'])

        #Compare time with timestamp
        sell_queue = db.selectPending(message['user'], 'SELL')
        print(sell_queue)
        if sell_queue is not None:
            if curr_time() - 60000 <= int(sell_queue[5]):
                # update with the most recent amount and stock symbol
                amount = sell_queue[4]
                stock_sym = sell_queue[2]
                amountOfStock = sell_queue[3]

                # update the DB using the new amount from above
                db.changeUsers(message['user'], amount)

                # create or update the stock for the user
                db.changeAccount(message['user'], stock_sym, amountOfStock)

                # Delete the pending records
                db.removePending(message['user'], 'SELL')
                response_msg = "Commited most recent SELL order"

            else:
                response_msg = "Time is greater than 60s. Commit buy cancelled."

        else:
            response_msg = "No sell order pending. Cancelled COMMIT SELL."
        return response_msg

    elif message['command'] == 'CANCEL_SELL':
        # print(message['user'])
        db.removePending(message['user'], 'SELL')
        response_msg = "Cancelled Sell"
        return response_msg

    elif message['command'] == 'SET_BUY_AMOUNT':
        # print(message['user'] + ', ' + message['stock_sym'] + ', ' + message['amount'])
        # Need to check the user's balance'
        funds = db.selectUsers(message['user'])[1]
        if funds >= amount:
            # selectTrigger:  input (user, stock_sym) output(amount, trigger, buy, user, stock_sym).
            if db.selectTrigger(message['user'], message['command'], message['stock_sym']) is not None:
                response_msg = "Trigger is already set for stock: " + str(message['stock_sym'])
            else:
                # Update the user funds by subtracting the amount from funds
                new_funds = float(format_money(funds)) - float(format_money(amount))
                db.changeUsers(message['user'], new_funds)

                # ??? Set up the trigger by adding a record in the DB with its Trigger amount to add
                db.addTrigger(message['user'], message['command'], message['stock_sym'], amount, new_funds, curr_time())
                response_msg = "BUY TRIGGER amount is SET"
        else:
            response_msg = "Not enough funds in user account to SET TRIGGER"

        return response_msg

    elif message['command'] == 'SET_BUY_TRIGGER':
        #print(message['user'] + ', ' + message['stock_sym'] + ', ' + message['amount'])
        funds = db.selectUsers(message['user'])[1]
        # if SET_BUY_AMOUNT command was executed for this user and stock symbol
        if db.selectTrigger(message['user'], 'SET_BUY_AMOUNT', message['stock_sym']):
            # if trigger was already set, remove it and add updated trigger
            if db.selectTrigger(message['user'], message['command'], message['stock_sym']):
                db.removeTrigger(message['user'], message['command'], message['stock_sym'])
            # amount is the price that the stock price needs to be less than or equal to before executing a buy
            db.addTrigger(message['user'], message['command'], message['stock_sym'], message['amount'], funds, curr_time())
            response_msg = "Buy trigger is set"
        else:
            response_msg = "SET_BUY_AMOUNT has not been executed for this command to run"
        return response_msg


    elif message['command'] == 'CANCEL_SET_BUY':
        # print(message['user'] + ', ' + message['stock_sym'])
        triggerAmount = db.selectTrigger(message['user'], 'SET_BUY_AMOUNT', message['stock_sym']) # amount here is the Trigger amount. Not funds.
        funds = db.selectUsers(message['user'])[1]
        if triggerAmount is None:
            response_msg = "There are no Trigger for this stock"
        else:
            # Add money back to the user funds
            db.changeUsers(message['user'], float(format_money(funds)) + float(format_money(triggerAmount[3])))
            # Delete the Trigger record
            db.removeTrigger(message['user'], 'SET_BUY_AMOUNT', message['stock_sym'])
            db.removeTrigger(message['user'], 'SET_BUY_TRIGGER', message['stock_sym'])
            response_msg = "Cancelled BUY TRIGGER"
        return response_msg


    elif message['command'] == 'SET_SELL_AMOUNT':
#        print(message['user'] + ', ' + message['stock_sym'] + ', ' + message['amount'])
        funds = db.selectUsers(message['user'])[1]
        stock_fund = db.selectAccount(message['user'], message['stock_sym'])[2]
        if amount <= stock_fund:
            if db.selectTrigger(message['user'], message['command'], message['stock_sym']):
                db.removeTrigger(message['user'], message['command'], message['stock_sym'])
            db.addTrigger(message['user'], message['command'], message['stock_sym'], message['amount'], funds, curr_time())
        else:
            response_msg = "Insufficient stock funds to set sell amount"

        return response_msg

    elif message['command'] == 'SET_SELL_TRIGGER':
        print(message['user'] + ', ' + message['stock_sym'] + ', ' + message['amount'])
        funds = db.selectUsers(message['user'])[1]
        # if SET_SELL_AMOUNT command was executed for this user and stock symbol
        if db.selectTrigger(message['user'], 'SET_SELL_AMOUNT', message['stock_sym']):
            # if trigger was already set, remove it and add updated trigger
            if db.selectTrigger(message['user'], message['command'], message['stock_sym']):
                db.removeTrigger(message['user'], message['command'], message['stock_sym'])
            # amount is the price that the stock price needs to be less than or equal to before executing a buy
            new_funds = funds + message['amount']
            db.changeUsers(message['user'], new_funds)
            db.addTrigger(message['user'], message['command'], message['stock_sym'], message['amount'], funds, curr_time())
            response_msg = "Sell trigger is set."
        else:
            response_msg = "SET_SELL_AMOUNT has not been executed for this command to run"
        return response_msg

    elif message['command'] == 'CANCEL_SET_SELL':
        print(message['user'] + ', ' + message['stock_sym'])
        triggerAmount = db.selectTrigger(message['user'], 'SET_SELL_TRIGGER', message['stock_sym'])[3] # amount here is the Trigger amount. Not funds.
        funds = db.selectUsers(message['user'])[1]
        if not amount:
            response_msg = "There are no Trigger for this stock"
        else:
            # Add money back to the user funds
            db.changeUsers(message['user'], float(format_money(funds)) + float(format_money(triggerAmount[3])))
            # Delete the Trigger record
            db.removeTrigger(message['user'], message['command'], message['stock_sym'])
            response_msg = "Cancelled SELL TRIGGER"
        return response_msg

    elif message['command'] == 'DUMPLOG':
        if len(message) == 1:
            print('Error in usage: DUMPLOG [userid]')
        elif len(message) == 2:
            #security feature for users accessing other user logs
            print('user access denied')
        else:
            print(message['user'] + ', ' + message.get('filename', ''))
            audit_dump = db.dumpAudit(message['user'])
            #send audit_dump to audit.py, possibly via socket
    elif message['command'] == 'DISPLAY_SUMMARY':
        print('display summary for ' + message['user'])
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
