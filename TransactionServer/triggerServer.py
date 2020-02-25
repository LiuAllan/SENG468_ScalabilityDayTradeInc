import ast
import os
import socket
import string
import sys
import time
import threading
from database import Database
#  - We set the and store the triggers in a Database from Transaction server
#  - Get quotes of each trigger about to expire
#  - Compare quotes with trigger amount
#  - Go through with the transaction if the price matches
#
# Check every couple seconds:
# 1. Connect to database
# 2. select user records
# 3. Connect to the quoteServer
# 4. Get the current quotes
# 5. Compare trigger amount with quote amount
# 6. If the trigger is BUY_TRIGGER
#     quote amount less than or equal to trigger_amount
#     update user account in DB with the new stock
#     Delete the trigger record
#     update time stamp
#    If the trigger is SELL_TRIGGER
#     if quote amount is greater than or equal to trigger amount
#         update user funds in DB with funds + quote amount
#         Delete the trigger record
#         update timestamp

# Initialize Database
db = Database()

def curr_time():
    return int(time.time() * 1000)

def get_quote(message):
    quoteserverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    quoteserverSocket.connect(('quoteserve.seng.uvic.ca', 4442))
    print('connected to quote server')
    quoteserverSocket.send((str(message['stock_sym'] + ',' + message['user']) + '\n').encode())
    print('sent symbol and user to quote server')
    reply = quoteserverSocket.recv(1024).decode()
    reply = ast.literal_eval(str(reply.split(',')))
    quoteserverSocket.close()
    return reply

def check_quote():


def check_trigger():
    # Somehow get the user records
    has_buy_trigger = selectTrigger(user, command, stock_sym)
    has_sell_trigger = selectTrigger(user, command, stock_sym)

    if has_buy_trigger is None:
        print('Trigger was not set in Transaction server')
    else:
        current_quote = get_quote(has_buy_trigger)
        if command == 'SET_BUY_TRIGGER':
            if current_quote[0] <= has_buy_trigger[3]:
                # update the DB
                db.changeUsers(message['user'], amount - current_quote[0])
                # create or update the stock for the user
                db.changeAccount(message['user'], stock_sym, amountOfStock)
                db.removeTrigger(user, command, stock_sym)
            else:
                print('Nothing done to Trigger')

        if command == 'SET_SELL_TRIGGER':
            if current_quote[0] <= has_sell_trigger[3]:
                # update the DB
                db.changeUsers(message['user'], amount + current_quote[0])
                # create or update the stock for the user
                db.changeAccount(message['user'], stock_sym, amountOfStock)
                db.removeTrigger(user, command, stock_sym)
            else:
                print('Nothing done to Trigger')


# Should handle checking every few seconds
def main():
    timer = threading.Timer(5.0, check_trigger)
    timer.start()


if __name__ == "__main__":
    main()