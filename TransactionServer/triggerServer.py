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

def check_quote:

def check_trigger:

# Should handle checking every few seconds
def main():




if __name__ == "__main__":
    main()