import socket
import time
import re
import pickle

def userCommand(item):
    string = "    <userCommand>\n"
    string += "        <timestamp>" + str(item[3]) + "</timestamp>\n"
    string += "        <server>" + str(item[8]) + "</server>\n"
    string += "        <transactionNum>" + str(item[0]) + "<transactionNum>\n"
    string += "        <command>" + str(item[2]) + "</command>\n"
    string += "        <username>" + str(item[1]) + "</username>\n"
    string += "        <funds>" + str(item[6]) + "</funds>\n"
    string += "    </userCommand>\n"
    return string

def quoteServer(item):
    string = "    <quoteServer>\n"
    string += "        <timestamp>" + str(item[3]) + "</timestamp>\n"
    string += "        <server>" + str(item[8]) + "</server>\n"
    string += "        <transactionNum>" + str(item[0]) + "<transactionNum>\n"
    string += "        <quoteServerTime>" + str(item[11]) + "</quoteServerTime>\n"
    string += "        <username>" + str(item[1]) + "</username>\n"
    string += "        <stockSymbol>" + str(item[4]) + "</stockSymbol>\n"
    string += "        <price>" + str(item[10]) + "</price>\n"
    string += "        <cryptokey>" + str(item[7]) + "</cryptokey>\n"
    string += "    </quoteServer>\n"
    return string

def accountTransaction(item):
    string = "    <accountTransaction>\n"
    string += "        <timestamp>" + str(item[3]) + "</timestamp>\n"
    string += "        <server>" + str(item[8]) + "</server>\n"
    string += "        <transactionNum>" + str(item[0]) + "<transactionNum>\n"
    string += "        <action>" + str(item[2]) + "</action>\n"
    string += "        <username>" + str(item[1]) + "</username>\n"
    string += "        <funds>" + str(item[5]) + "</funds>\n"
    string += "    </accountTransaction>\n"
    return string

def systemEvent(item):
    string = "    <systemEvent>\n"
    string += "        <timestamp>" + str(item[3]) + "</timestamp>\n"
    string += "        <server>" + str(item[8]) + "</server>\n"
    string += "        <transactionNum>" + str(item[0]) + "<transactionNum>\n"
    string += "        <command>" + str(item[2]) + "</command>\n"
    string += "        <username>" + str(item[1]) + "</username>\n"
    string += "        <stockSymbol>" + str(item[4]) + "</stockSymbol>\n"
    string += "        <funds>" + str(item[6]) + "</funds>\n"
    string += "    </systemEvent>\n"
    return string

def errorEvent(item):
    string = "    <errorEvent>\n"
    string += "        <timestamp>" + str(item[3]) + "</timestamp>\n"
    string += "        <server>" + str(item[8]) + "</server>\n"
    string += "        <transactionNum>" + str(item[0]) + "<transactionNum>\n"
    string += "        <command>" + str(item[2]) + "</command>\n"
    string += "        <username>" + str(item[1]) + "</username>\n"
    string += "        <stockSymbol>" + str(item[4]) + "</stockSymbol>\n"
    string += "        <funds>" + str(item[6]) + "</funds>\n"
    string += "        <errorMessage>" + str(item[13]) + "</errorMessage>\n"
    string += "    </errorEvent>\n"
    return string

def debugEvent(item):
    string = "    <debugEvent>\n"
    string += "        <timestamp>" + str(item[3]) + "</timestamp>\n"
    string += "        <server>" + str(item[8]) + "</server>\n"
    string += "        <transactionNum>" + str(item[0]) + "<transactionNum>\n"
    string += "        <command>" + str(item[2]) + "</command>\n"
    string += "        <username>" + str(item[1]) + "</username>\n"
    string += "        <stockSymbol>" + str(item[4]) + "</stockSymbol>\n"
    string += "        <funds>" + str(item[6]) + "</funds>\n"
    string += "        <debugMessage>" + str(item[14]) + "</debugMessage>\n"
    string += "    </debugEvent>\n"
    return string


def main():
    auditServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    auditServerSocket.bind(('localhost', 44409))
    auditServerSocket.listen(5)
    print('Ready to audit...')

    while True:
        c, addr = auditServerSocket.accept()
        print('audit log accepted...')
        try:
            line = pickle.loads(c.recv(4096))
            print('line received is ', line)
			
            redirect(line)
            audit_print = redirect(line)
            #c.send(audit_print.encode())
			
            c.close()
        except IOError as err:
            print(err)
            c.close()

    #file = open("1userWorkLoad.txt", "r")
    #Creates a list of list which each line is broken into parameters
    #contents = [re.sub("\[[0-9]+] ", "", item.strip()).split(",") for item in file.readlines()]
    #file.close()
    #print(contents)
    #usr_funds = 0.00

    #buy_amount = 0.00
    #sell_amount = 0.00
def redirect(line):
    log = ""
    for item in line:
        if(item[2] == "ADD"):
            print("ADD")
            log += userCommand(line)
            log += accountTransaction(line)
        elif (item[2] == "QUOTE"):
            print("QUOTE")
            log += quoteServer(usr = line[1])
        elif (item[2] == "BUY"):
            print("BUY")
            #buy_amount += float(line[3])
            log += userCommand(item)
            if item[13] is not None:
                log += errorEvent(item)
            elif item[14] is not None:
                log += debugEvent(item)
            else:
                log += systemEvent(item)
                log += quoteServer(item)
                log += accountTransaction(item)
        elif (item[2] == "COMMIT_BUY"):
            print("COMMIT_BUY")
            #log += userCommand(item)
            #log += systemEvent(item)
        elif (item[2] == "CANCEL_BUY"):
            print("CANCEL_BUY")
            #log += userCommand(item)
            #log += systemEvent(item)
        elif (item[2] == "SELL"):
            print("SELL")
            #log += userCommand(item)
            #log += systemEvent(item)
            #log += quoteServer(item)
            #log += accountTransaction(item)
        elif (item[2] == "COMMIT_SELL"):
            print("COMMIT_SELL")
            #log += userCommand(item)
            #log += systemEvent(item)
        elif (item[2] == "CANCEL_SELL"):
            print("CANCEL_SELL")
            #log += userCommand(item)
            #log += systemEvent(item)
        elif (item[2] == "SET_BUY_AMOUNT"):
            print("SET_BUY_AMOUNT")
            #log += userCommand(item)
            #log += systemEvent(item)
        elif (item[2] == "CANCEL_SET_BUY"):
            print("CANCEL_SET_BUY")
            #log += userCommand(item)
            #log += systemEvent(item)
        elif (item[2] == "SET_BUY_TRIGGER"):
            print("SET_BUY_TRIGGER")
            #log += userCommand(item)
            #log += systemEvent(item)
        elif (item[2] == "SET_SELL_AMOUNT"):
            print("SET_SELL_AMOUNT")
            #log += userCommand(item)
            #log += systemEvent(item)
        elif (item[2] == "SET_SELL_TRIGGER"):
            print("SET_SELL_TRIGGER")
            #log += userCommand(item)
            #log += systemEvent(item)
        elif (item[2] == "CANCEL_SET_SELL"):
            print("CANCEL_SET_SELL")
            #log += userCommand(item)
            #log += systemEvent(item)
        elif (item[2] == "DISPLAY_SUMMARY"):
            print("DISPLAY_SUMMARY")
            #log += userCommand(item)
        elif (item[2] == "DUMPLOG"):
            print("DUMPLOG")
            log_string = '<?xml version="1.0"?>\n<log>\n\n' + log + '\n</log>'
            xml_file = open(line[1], "w")
            xml_file.write(log_string)

    log_string = '<?xml version="1.0"?>\n<log>\n\n' + log + '\n</log>'
    xml_file = open('log.xml', "w")
    xml_file.write(log_string)

    #print(log_string)
    print(log_string)
	



if __name__ == "__main__":
    main()