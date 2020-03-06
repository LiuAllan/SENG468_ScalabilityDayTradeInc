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
    quoteserverSocket.connect(('localhost', 44407))
    print('connected to quote server')
    quoteserverSocket.send(str(message).encode())
    print('sent symbol and user to quote server')
    reply = quoteserverSocket.recv(1024).decode()
    print(reply)
    quoteserverSocket.close()
    return reply

# def check_quote():


def check_trigger():
    allTriggers = db.selectAllTrigger()
    print(allTriggers)
    # Somehow get the user records
    # has_buy_trigger = selectTrigger(user, command, stock_sym)
    # has_sell_trigger = selectTrigger(user, command, stock_sym)

    for trigger in allTriggers:
        current_quote = get_quote(trigger)
        if trigger['command'] == 'SET_BUY_TRIGGER':
            # Compare quote with trigger amount
            if current_quote[0] <= trigger['triggerAmount']:
                # update the DB
                funds = selectUsers(trigger['user'])
                db.changeUsers(trigger['user'], trigger['funds'] - current_quote[0])
                # create or update the stock for the user
                db.changeAccount(trigger['user'], trigger['stock_sym'], trigger['amountOfStock'])
                db.removeTrigger(trigger['user'], trigger['command'], trigger['stock_sym'])
            else:
                print('Nothing done to Trigger')

        if command == 'SET_SELL_TRIGGER':
            if current_quote[0] >= trigger['triggerAmount']:
                # update the DB
                db.changeUsers(trigger['user'], trigger['funds'] + current_quote[0])
                # create or update the stock for the user
                db.changeAccount(trigger['user'], trigger['stock_sym'], trigger['amountOfStock'])
                db.removeTrigger(trigger['user'], trigger['command'], trigger['stock_sym'])
            else:
                print('Nothing done to Trigger')


# Should handle checking every few seconds
def main():
    while True:
        check_trigger()
        time.sleep(5)

if __name__ == "__main__":
    main()
