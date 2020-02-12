import socket
import time
import re
import pickle

def userCommand(line):
    string = "    <userCommand>\n"
    string += "        <timestamp>" + str(line['timestamp']) + "</timestamp>\n"
    string += "        <server>" + line['server'] + "</server>\n"
    string += "        <transactionNum>" + str(line['transaction_num']) + "<transactionNum>\n"
    string += "        <command>" + line['command'] + "</command>\n"
    string += "        <username>" + line['user'] + "</username>\n"
    string += "        <funds>" + str(line['amount']) + "</funds>\n"
    string += "    </userCommand>\n"
    return string

def quoteServer(line):
    string = "    <quoteServer>\n"
    string += "        <timestamp>" + str(line['timestamp']) + "</timestamp>\n"
    string += "        <server>" + line['server'] + "</server>\n"
    string += "        <transactionNum>" + str(line['transaction_num']) + "<transactionNum>\n"
    string += "        <quoteServerTime>" + str(line['q_time']) + "</quoteServerTime>\n"
    string += "        <username>" + line['user'] + "</username>\n"
    string += "        <stockSymbol>" + line['stock_sym'] + "</stockSymbol>\n"
    string += "        <price>" + line['quote_price'] + "</price>\n"
    string += "        <cryptokey>" + line['crypto_key'] + "</cryptokey>\n"
    string += "    </quoteServer>\n"
    return string

def accountTransaction(line):
    string = "    <accountTransaction>\n"
    string += "        <timestamp>" + str(line['timestamp']) + "</timestamp>\n"
    string += "        <server>" + line['server'] + "</server>\n"
    string += "        <transactionNum>" + str(line['transaction_num']) + "<transactionNum>\n"
    string += "        <action>" + line['command'] + "</action>\n"
    string += "        <username>" + line['user'] + "</username>\n"
    string += "        <funds>" + str(line['amount']) + "</funds>\n"
    string += "    </accountTransaction>\n"
    return string

def systemEvent(line):
    string = "    <systemEvent>\n"
    string += "        <timestamp>" + str(line['timestamp']) + "</timestamp>\n"
    string += "        <server>" + line['server'] + "</server>\n"
    string += "        <transactionNum>" + str(line['transaction_num']) + "<transactionNum>\n"
    string += "        <command>" + line['command'] + "</command>\n"
    string += "        <username>" + line['user'] + "</username>\n"
    string += "        <stockSymbol>" + line['stock_sym'] + "</stockSymbol>\n"
    string += "        <funds>" + str(line['funds']) + "</funds>\n"
    string += "    </systemEvent>\n"
    return string

def errorEvent(line):
    string = "    <errorEvent>\n"
    string += "        <timestamp>" + str(line['timestamp']) + "</timestamp>\n"
    string += "        <server>" + line['server'] + "</server>\n"
    string += "        <transactionNum>" + str(line['transaction_num']) + "<transactionNum>\n"
    string += "        <command>" + line['command'] + "</command>\n"
    string += "        <username>" + line['user'] + "</username>\n"
    string += "        <stockSymbol>" + line['stock_sym'] + "</stockSymbol>\n"
    string += "        <funds>" + str(line['funds']) + "</funds>\n"
    string += "        <errorMessage>" + line['error_msg'] + "</errorMessage>\n"
    string += "    </errorEvent>\n"
    return string

def debugEvent(line):
    string = "    <debugEvent>\n"
    string += "        <timestamp>" + str(line['timestamp']) + "</timestamp>\n"
    string += "        <server>" + line['server'] + "</server>\n"
    string += "        <transactionNum>" + str(line['transaction_num']) + "<transactionNum>\n"
    string += "        <command>" + line['command'] + "</command>\n"
    string += "        <username>" + line['user'] + "</username>\n"
    string += "        <stockSymbol>" + line['stock_sym'] + "</stockSymbol>\n"
    string += "        <funds>" + str(line['funds']) + "</funds>\n"
    string += "        <debugMessage>" + line['debug_msg'] + "</debugMessage>\n"
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
            c.send('info received as type {}'.format(type(line)).encode())
			
            redirect(line)
			
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
    if(line['command'] == "ADD"):
        print("ADD")
        log += userCommand(line)
        log += accountTransaction(line)
    elif (line['command'] == "QUOTE"):
        print("QUOTE")
        log += quoteServer(usr = line[1])
    elif (line['command'] == "BUY"):
        print("BUY")
        buy_amount += float(line[3])
        #log += userCommand(line[0], line[1], usr_funds)
        #log += systemEvent()
        #log += quoteServer()
        #log += accountTransaction()
    elif (line['command'] == "COMMIT_BUY"):
        print("COMMIT_BUY")
        #log += userCommand(line[0], line[1], line[2])
        #log += systemEvent()
    elif (line['command'] == "CANCEL_BUY"):
        print("CANCEL_BUY")
        #log += userCommand()
        #log += systemEvent()
    elif (line['command'] == "SELL"):
        print("SELL")
        #log += userCommand(line[0], line[1], usr_funds)
        #log += systemEvent()
        #log += quoteServer()
        #log += accountTransaction()
    elif (line['command'] == "COMMIT_SELL"):
        print("COMMIT_SELL")
        #log += userCommand(line[0], line[1], line[2])
        #log += systemEvent()
    elif (line['command'] == "CANCEL_SELL"):
        print("CANCEL_SELL")
        #log += userCommand(line[0], line[1], line[2])
        #log += systemEvent()
    elif (line['command'] == "SET_BUY_AMOUNT"):
        print("SET_BUY_AMOUNT")
        #log += userCommand(line[0], line[1], line[2])
        #log += systemEvent()
    elif (line['command'] == "CANCEL_SET_BUY"):
        print("CANCEL_SET_BUY")
        #log += userCommand(line[0], line[1], line[2])
        #log += systemEvent()
    elif (line['command'] == "SET_BUY_TRIGGER"):
        print("SET_BUY_TRIGGER")
        #log += userCommand(line[0], line[1], line[2])
        #log += systemEvent()
    elif (line['command'] == "SET_SELL_AMOUNT"):
        print("SET_SELL_AMOUNT")
        #log += userCommand(line[0], line[1], line[2])
        #log += systemEvent()
    elif (line['command'] == "SET_SELL_TRIGGER"):
        print("SET_SELL_TRIGGER")
        #log += userCommand(line[0], line[1], line[2])
        #log += systemEvent()
    elif (line['command'] == "CANCEL_SET_SELL"):
        print("CANCEL_SET_SELL")
        #log += userCommand(line[0], line[1], line[2])
        #log += systemEvent()
    elif (line['command'] == "DISPLAY_SUMMARY"):
        print("DISPLAY_SUMMARY")
        #log += userCommand(line[0], line[1], line[2])
    elif (line['command'] == "DUMPLOG"):
        print("DUMPLOG")
        log_string = '<?xml version="1.0"?>\n<log>\n\n' + log + '\n</log>'
        xml_file = open(line[1], "w")
        xml_file.write(log_string)

    #print(log_string)
    print(log)
	



if __name__ == "__main__":
    main()
