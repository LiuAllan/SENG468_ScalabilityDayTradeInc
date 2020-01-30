import socket
import time

def userCommand(cmd, usr, funds, server = 'CLT1', transnum = 1, t = time.time()):
    string = "<userCommand>\n"
    string += "    <timestamp>" + str(t) + "</timestamp>\n"
    string += "    <server>" + str(server) + "</server>\n"
    string += "    <transactionNum>" + str(transnum) + "<transactionNum>\n"
    string += "    <command>" + str(cmd) + "</command>\n"
    string += "    <username>" + str(usr) + "</username>\n"
    string += "    <funds>" + str(funds) + "</funds>\n"
    string += "</userCommand>\n"
    return string

def quoteServer(t, server, transnum, qtime, usr, symbol, price, key):
    string = "<quoteServer>\n"
    string += "    <timestamp>" + str(t) + "</timestamp>\n"
    string += "    <server>" + str(server) + "</server>\n"
    string += "    <transactionNum>" + str(transnum) + "<transactionNum>\n"
    string += "    <quoteServerTime>" + str(qtime) + "</quoteServerTime>\n"
    string += "    <username>" + str(usr) + "</username>\n"
    string += "    <stockSymbol>" + str(symbol) + "</stockSymbol>\n"
    string += "    <price>" + str(price) + "</price>\n"
    string += "    <cryptokey>" + str(key) + "</cryptokey>\n"
    string = "</quoteServer>"
    return string

def accountTransaction(t, server, transnum, action, usr, funds):
    string = "<accountTransaction>\n"
    string += "    <timestamp>" + str(t) + "</timestamp>\n"
    string += "    <server>" + str(server) + "</server>\n"
    string += "    <transactionNum>" + str(transnum) + "<transactionNum>\n"
    string += "    <action>" + str(action) + "</action>\n"
    string += "    <username>" + str(usr) + "</username>\n"
    string += "    <funds>" + str(funds) + "</funds>\n"
    string = "</accountTransaction>"
    return string

def systemEvent(t, server, transnum, cmd, usr, symbol, funds):
    string = "<systemEvent>\n"
    string += "    <timestamp>" + str(t) + "</timestamp>\n"
    string += "    <server>" + str(server) + "</server>\n"
    string += "    <transactionNum>" + str(transnum) + "<transactionNum>\n"
    string += "    <command>" + str(cmd) + "</command>\n"
    string += "    <username>" + str(usr) + "</username>\n"
    string += "    <stockSymbol>" + str(symbol) + "</stockSymbol>\n"
    string += "    <funds>" + str(funds) + "</funds>\n"
    string = "</systemEvent>"
    return string

def errorEvent(t, server, transnum, cmd, usr, symbol, funds, msg):
    string = "<errorEvent>\n"
    string += "    <timestamp>" + str(t) + "</timestamp>\n"
    string += "    <server>" + str(server) + "</server>\n"
    string += "    <transactionNum>" + str(transnum) + "<transactionNum>\n"
    string += "    <command>" + str(cmd) + "</command>\n"
    string += "    <username>" + str(usr) + "</username>\n"
    string += "    <stockSymbol>" + str(symbol) + "</stockSymbol>\n"
    string += "    <funds>" + str(funds) + "</funds>\n"
    string += "    <errorMessage>" + str(msg) + "</errorMessage>\n"
    string = "</errorEvent>"
    return string

def debugEvent(t, server, transnum, cmd, usr, symbol, funds, msg):
    string = "<debugEvent>\n"
    string += "    <timestamp>" + str(t) + "</timestamp>\n"
    string += "    <server>" + str(server) + "</server>\n"
    string += "    <transactionNum>" + str(transnum) + "<transactionNum>\n"
    string += "    <command>" + str(cmd) + "</command>\n"
    string += "    <username>" + str(usr) + "</username>\n"
    string += "    <stockSymbol>" + str(symbol) + "</stockSymbol>\n"
    string += "    <funds>" + str(funds) + "</funds>\n"
    string += "    <debugMessage>" + str(msg) + "</debugMessage>\n"
    string = "</debugEvent>"
    return string


def main():
    auditServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    auditServerSocket.bind(('localhost', 8000))
    auditServerSocket.listen(5)

    while True:
        print('audit log ready...')
        c, addr = auditServerSocket.accept()
        info = auditServerSocket.recv(2048).decode()

    client_cmd = ['ADD', 'jiosesdo', 100.00]
    log = userCommand(client_cmd[0], client_cmd[1], client_cmd[2])





    log_string = '<?xml version="1.0"?>\n<log>\n\n    ' + log + '\n</log>'
    print(log_string)
	



if __name__ == "__main__":
    main()
