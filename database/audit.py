import socket
import time
import re

def userCommand(cmd, usr, funds, server = 'CLT1', transnum = 1, t = time.time()):
    string = "    <userCommand>\n"
    string += "        <timestamp>" + str(t) + "</timestamp>\n"
    string += "        <server>" + str(server) + "</server>\n"
    string += "        <transactionNum>" + str(transnum) + "<transactionNum>\n"
    string += "        <command>" + str(cmd) + "</command>\n"
    string += "        <username>" + str(usr) + "</username>\n"
    string += "        <funds>" + str(funds) + "</funds>\n"
    string += "    </userCommand>\n"
    return string

def quoteServer(usr, t = time.time(), server = 'CLT1', transnum = 1, qtime = time.time(), symbol = 'ABC', price = 1.00, key = '4rn94ng'):
    string = "    <quoteServer>\n"
    string += "        <timestamp>" + str(t) + "</timestamp>\n"
    string += "        <server>" + str(server) + "</server>\n"
    string += "        <transactionNum>" + str(transnum) + "<transactionNum>\n"
    string += "        <quoteServerTime>" + str(qtime) + "</quoteServerTime>\n"
    string += "        <username>" + str(usr) + "</username>\n"
    string += "        <stockSymbol>" + str(symbol) + "</stockSymbol>\n"
    string += "        <price>" + str(price) + "</price>\n"
    string += "        <cryptokey>" + str(key) + "</cryptokey>\n"
    string = "    </quoteServer>\n"
    return string

def accountTransaction(action, usr, funds, t = time.time(), server = 'CLT1', transnum = 1):
    string = "    <accountTransaction>\n"
    string += "        <timestamp>" + str(t) + "</timestamp>\n"
    string += "        <server>" + str(server) + "</server>\n"
    string += "        <transactionNum>" + str(transnum) + "<transactionNum>\n"
    string += "        <action>" + str(action) + "</action>\n"
    string += "        <username>" + str(usr) + "</username>\n"
    string += "        <funds>" + str(funds) + "</funds>\n"
    string = "    </accountTransaction>\n"
    return string

def systemEvent(t, server, transnum, cmd, usr, symbol, funds):
    string = "    <systemEvent>\n"
    string += "        <timestamp>" + str(t) + "</timestamp>\n"
    string += "        <server>" + str(server) + "</server>\n"
    string += "        <transactionNum>" + str(transnum) + "<transactionNum>\n"
    string += "        <command>" + str(cmd) + "</command>\n"
    string += "        <username>" + str(usr) + "</username>\n"
    string += "        <stockSymbol>" + str(symbol) + "</stockSymbol>\n"
    string += "        <funds>" + str(funds) + "</funds>\n"
    string = "    </systemEvent>\n"
    return string

def errorEvent(t, server, transnum, cmd, usr, symbol, funds, msg):
    string = "    <errorEvent>\n"
    string += "        <timestamp>" + str(t) + "</timestamp>\n"
    string += "        <server>" + str(server) + "</server>\n"
    string += "        <transactionNum>" + str(transnum) + "<transactionNum>\n"
    string += "        <command>" + str(cmd) + "</command>\n"
    string += "        <username>" + str(usr) + "</username>\n"
    string += "        <stockSymbol>" + str(symbol) + "</stockSymbol>\n"
    string += "        <funds>" + str(funds) + "</funds>\n"
    string += "        <errorMessage>" + str(msg) + "</errorMessage>\n"
    string = "    </errorEvent>\n"
    return string

def debugEvent(t, server, transnum, cmd, usr, symbol, funds, msg):
    string = "    <debugEvent>\n"
    string += "        <timestamp>" + str(t) + "</timestamp>\n"
    string += "        <server>" + str(server) + "</server>\n"
    string += "        <transactionNum>" + str(transnum) + "<transactionNum>\n"
    string += "        <command>" + str(cmd) + "</command>\n"
    string += "        <username>" + str(usr) + "</username>\n"
    string += "        <stockSymbol>" + str(symbol) + "</stockSymbol>\n"
    string += "        <funds>" + str(funds) + "</funds>\n"
    string += "        <debugMessage>" + str(msg) + "</debugMessage>\n"
    string = "    </debugEvent>\n"
    return string


def main():
    #auditServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #auditServerSocket.bind(('localhost', 8000))
    #auditServerSocket.listen(5)

    #while True:
    #    c, addr = auditServerSocket.accept()
    #    print('audit log accepted...')
    #    info = auditServerSocket.recv(2048).decode()

    file = open("1userWorkLoad.txt", "r")
    # Creates a list of list which each line is broken into parameters
    contents = [re.sub("\[[0-9]+] ", "", item.strip()).split(",") for item in file.readlines()]
    file.close()
    
    log = ""

    for line in contents:
        if(line[0] == "ADD"):
            print("ADD")
            log += userCommand(line[0], line[1], line[2])
            log += accountTransaction(action = 'add', usr = line[1], funds = line[2])
        elif (line[0] == "QUOTE"):
            print("QUOTE")
            log += quoteServer(usr = line[1])
        elif (line[0] == "BUY"):
            print("BUY")
            #log += userCommand(line[0], line[1], line[2])
            #log += systemEvent()
            #log += quoteServer()
            #log += accountTransaction()
        elif (line[0] == "COMMIT_BUY"):
            print("COMMIT_BUY")
            #log += userCommand(line[0], line[1], line[2])
            #log += systemEvent()
        elif (line[0] == "CANCEL_BUY"):
            print("CANCEL_BUY")
        elif (line[0] == "SELL"):
            print("SELL")
        elif (line[0] == "COMMIT_SELL"):
            print("COMMIT_SELL")
        elif (line[0] == "CANCEL_SELL"):
            print("CANCEL_SELL")
        elif (line[0] == "SET_BUY_AMOUNT"):
            print("SET_BUY_AMOUNT")
        elif (line[0] == "CANCEL_SET_BUY"):
            print("CANCEL_SET_BUY")
        elif (line[0] == "SET_BUY_TRIGGER"):
            print("SET_BUY_TRIGGER")
        elif (line[0] == "SET_SELL_AMOUNT"):
            print("SET_SELL_AMOUNT")
        elif (line[0] == "SET_SELL_TRIGGER"):
            print("SET_SELL_TRIGGER")
        elif (line[0] == "CANCEL_SET_SELL"):
            print("CANCEL_SET_SELL")
        elif (line[0] == "DUMPLOG"):
            print("DUMPLOG")
        elif (line[0] == "DISPLAY_SUMMARY"):
            print("DISPLAY_SUMMARY")

    log_string = '<?xml version="1.0"?>\n<log>\n\n' + log + '\n</log>'
    xml_file = open("log.xml", "w")
    xml_file.write(log_string)
    print(log_string)
	



if __name__ == "__main__":
    main()
