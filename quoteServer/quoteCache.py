import ast
import os
import socket
import string
import sys
import Queue
import time
import threading

# Logic:
# - Commands for BUY and SELL will get the quote from the quote server
#     - place it in cache
# - Calling the QUOTE command will check the cache
#     - if quote is None or expired (greater than 60s)
#     - then update the cache from the quote server
#     - send the new quote back to transaction server
# - Quote timestamp is based on local time***

# https://www.geeksforgeeks.org/queue-in-python/
arrival_queue = Queue.Queue()

def curr_time():
	return int(time.time() * 1000)

# Need to change this
def get_quote(message):
    quoteserverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # could possibly make this faster by splitting stock symbols up
    quoteserverSocket.connect(('quoteserve.seng.uvic.ca', 4442))
    print('connected to quote server')
    quoteserverSocket.send((str(message['stock_sym'] + ',' + message['user']) + '\n').encode())
    print('sent symbol and user to quote server')
    reply = quoteserverSocket.recv(1024).decode()
    reply = ast.literal_eval(str(reply.split(',')))
    quoteserverSocket.close()
    return reply

def check_cache(stock_sym):


def update_cache(quote):


def thread_controller():
    while True:
        # Fetch from the queue
        connection = arrival_queue.get()

        message = connection.recv(4096)
        message = ast.literal_eval(message)

        if message["command"] == "BUY" or message["command"] == "SELL":
            # scan the cache
        elif message["command"] == "QUOTE":

        elif message["command"] == "TRIGGER":

        else:
            print("Quote Cache server had an issue getting quote")

        connection.send(str(quote))
        connection.close()

        arrival_queue.task_done()
    return

# Set up the socket so it can receive data
def listen():
    try:
        # Prepare a server socket
        quoteCacheSocket.bind(('localhost', 44404))
    except socket.error
        print("Failed binding socket to IP and port")
        return 0

    # 10 is the amount it can allow in queue before it starts dropping packets
    quoteCacheSocket.listen(10)

    return 1

def main():
    # Make threads
    for i in range(1, 10):
        t = threading.Thread(target=thread_controller, args=())
        t.daemon = True
        t.start()

    quoteCacheSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if listen():
        while True:
            connection, addr = quoteCacheSocket.accept()
            arrival_queue.put(connection)

if __name__ == "__main__":
	main()