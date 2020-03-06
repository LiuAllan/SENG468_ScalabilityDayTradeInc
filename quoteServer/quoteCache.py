import ast
import os
import socket
import string
import sys
import queue
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

quoteCacheSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Placeholder
cache = {
    "A":
    {
        'price': 0,
        'user': "",
        'timestamp': 0,
        'cryptokey': "",
        'expire': 0
    }
}


# https://www.geeksforgeeks.org/queue-in-python/
arrival_queue = queue.Queue()
lock_cache = threading.Semaphore(1)


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
    response = quoteserverSocket.recv(1024).decode()

    response = response.split(',')

    reply = {
        "price": response[0],
        "stock_sym": response[1],
        "user": response[2],
        "timestamp": response[3],
        "cryptokey": response[4],
        "expire": curr_time() + 60000
    }

    # reply = ast.literal_eval(str(reply.split(',')))
    quoteserverSocket.close()
    return reply


def check_cache(stock_sym):
    lock_cache.acquire()
    if stock_sym in cache:
        if cache[stock_sym]["expire"] >= curr_time():
            reply = {
                "result": "match",
                "price": cache[stock_sym]["price"],
                "stock_sym": stock_sym,
                "user": cache[stock_sym]["user"],
                "timestamp": cache[stock_sym]["timestamp"],
                "cryptokey": cache[stock_sym]["cryptokey"],
                "expire": cache[stock_sym]["expire"]
            }
        else:
            reply = {"result": "expired"}
    else:
        reply = {"result": "none"}
    lock_cache.release()
    return reply


def update_cache(quote):
    lock_cache.acquire()

    cache[quote["stock_sym"]] = {
        "price": quote["price"],
        "user": quote["user"],
        "timestamp": quote["timestamp"],
        "cryptokey": quote["cryptokey"],
        "expire": quote["expire"]  # curr_time() + 60 seconds
    }

    lock_cache.release()

    return


def thread_controller():
    while True:
        # Fetch from the queue
        connection = arrival_queue.get()

        # Receive and convert string back into a dictionary so we can use it
        message = connection.recv(4096).decode()
        message = ast.literal_eval(message)
        print(message)

        if message["command"] == "BUY" or message["command"] == "SELL":
            # check the cache
            quote = check_cache(message["stock_sym"])
            if quote["result"] != "match":
                quote = get_quote(message)
                update_cache(quote)
        elif message["command"] == "QUOTE":
            quote = check_cache(message["stock_sym"])
            if quote["result"] != "match":
                quote = get_quote(message)
                update_cache(quote)
        # trigger server will access this
        elif message["command"] == "TRIGGER":
            quote = check_cache(message["stock_sym"])
            if quote["result"] != "match":
                quote = get_quote(message)
                update_cache(quote)
        else:
            print("Quote Cache didn't detect any valid commands")
            quote = cache
        print(quote)
        connection.send(str(quote).encode())
        connection.close()

        arrival_queue.task_done()
    return


# Set up the socket so it can receive data
def listen():
    try:
        # Prepare a server socket
        quoteCacheSocket.bind(('localhost', 44407))
    except socket.error:
        print("Failed binding socket to IP and port")
        return 0

    # 10 is the amount it can allow in queue before it starts dropping packets
    quoteCacheSocket.listen(10)

    return 1


def main():
    # Make threads
    print("Cache is listening")
    for i in range(1, 10):
        t = threading.Thread(target=thread_controller, args=())
        t.daemon = True
        t.start()

    if listen():
        while True:
            connection, addr = quoteCacheSocket.accept()
            arrival_queue.put(connection)


if __name__ == "__main__":
    main()
