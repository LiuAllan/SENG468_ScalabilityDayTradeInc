# To run: change filename to desired 1userWorkLoad
# File needs to be in the same directory as the program
# python3 generator.py
import re
import io
import socket
import sys
import string
import os

from threading import Thread, current_thread

# Global variables
webserver_ip = 'localhost'
webserver_port = 5000

def request_info(command, user=None, stock_sym=None, amount=None, filename=None):
    data = {
        # 'transaction_number': transaction_number,
        # ADD, BUY, COMMIT, CANCEL, etc.
        'command': command,
    }

    if user:
        data['user'] = user

    if stock_sym:
        data['stock_sym'] = stock_sym

    if amount:
        data['amount'] = amount

    if filename:
        data['filename'] = filename

    # make a TCP/IP socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # address (ip and port) of where the web server is listening
    server_address = (webserver_ip, webserver_port)

    clientSocket.connect(server_address)

    # Send data
    print(data)

    # something wrong here***************
    message = str(data).encode('utf-8')
    clientSocket.sendall(message)
    response = clientSocket.recv(1024)

    strbuffer = ""

    while response:
        strbuffer += response
        response = clientSocket.recv(4096)

    clientSocket.close()
    print(strbuffer)

    return response


# -----------------------------------
def ADD(params):
    request_info(listItems[0][0], listItems[0][1], amount=listItems[0][2])
    # print("ADD {}".format(params))
def QUOTE(params):
    request_info(listItems[0][0], listItems[0][1], listItems[0][2])
    # print("QUOTE {}".format(params))
def BUY(params):
    request_info(listItems[0][0], listItems[0][1], listItems[0][2], listItems[0][3])
    # print("BUY {}".format(params))
def COMMIT_BUY(params):
    request_info(listItems[0][0], listItems[0][1])
    # print("COMMIT_BUY {}".format(params))
def CANCEL_BUY(params):
    request_info(listItems[0][0], listItems[0][1])
    # print("CANCEL_BUY {}".format(params))
def SELL(params):
    print("SELL {}".format(params))
def COMMIT_SELL(params):
    print("COMMIT_SELL {}".format(params))
def CANCEL_SELL(params):
    print("CANCEL_SELL {}".format(params))
def SET_BUY_AMOUNT(params):
    print("SET_BUY_AMOUNT {}".format(params))
def SET_BUY_TRIGGER(params):
    print("SET_BUY_TRIGGER {}".format(params))
def CANCEL_SET_BUY(params):
    print("CANCEL_SET_BUY {}".format(params))
def SET_SELL_AMOUNT(params):
    print("SET_SELL_AMOUNT {}".format(params))
def SET_SELL_TRIGGER(params):
    print("SET_SELL_TRIGGER {}".format(params))
def CANCEL_SET_SELL(params):
    print("CANCEL_SET_SELL {}".format(params))
def DUMPLOG(params):
    print("DUMPLOG {}".format(params))
def DISPLAY_SUMMARY(params):
    print("DISPLAY_SUMMARY {}".format(params))
def PROBLEM(params):
    print("PROBLEM {}".format(params))


# read in the workload file, split the commands into list so we can process them
filename = "1userWorkLoad"
switcher = {
    "ADD": ADD,
    "QUOTE": QUOTE,
    "BUY": BUY,
    "COMMIT_BUY": COMMIT_BUY,
    "CANCEL_BUY": CANCEL_BUY,
    "SELL": SELL,
    "COMMIT_SELL": COMMIT_SELL,
    "CANCEL_SELL": CANCEL_SELL,
    "SET_BUY_AMOUNT": SET_BUY_AMOUNT,
    "SET_BUY_TRIGGER": SET_BUY_TRIGGER,
    "CANCEL_SET_BUY": CANCEL_SET_BUY,
    "SET_SELL_AMOUNT": SET_SELL_AMOUNT,
    "SET_SELL_TRIGGER": SET_SELL_TRIGGER,
    "CANCEL_SET_SELL": CANCEL_SET_SELL,
    "DUMPLOG": DUMPLOG,
    "DISPLAY_SUMMARY": DISPLAY_SUMMARY

}
file = open(filename, "r")
# Creates a list of list which each line is broken into parameters
listItems = [re.sub("\[[0-9]+] ", "", item.strip()).split(",") for item in file.readlines()]

for item in listItems:
    switcher.get(item[0], PROBLEM)(item[1:])