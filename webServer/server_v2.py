from flask import Flask, render_template, request
import socket
app = Flask(__name__)

def request_info(command, user=None, stock_sym=None, amount=None, filename=None):
    data = {
        # ADD, BUY, COMMIT, CANCEL, etc.
        'command': command
    }
    if user:
        data['user'] = user
    if stock_sym:
        data['stock_sym'] = stock_sym
    if amount:
        data['amount'] = amount
    if filename:
        data['filename'] = filename

    # Make a socket for the webserver to be accessed through
    webserverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    trans_server_address = ('localhost', 44406)

    #Prepare a server socket
    webserverSocket.bind(("localhost", 44405))
    webserverSocket.listen(5)

    # keep sending if there are more commands
    while True:
        # Establish the connection
        print('Ready to serve...')

        # Make a socket for the transaction server to be accessed through
        transerverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # message from web client
            message = str(data)
            print(message)

            # send message to transaction server
            transerverSocket.connect(trans_server_address)
            print('made a connection to transaction server')
            transerverSocket.send(message.encode())

            # receive message back from transaction server
            strbuffer = ''
            data = transerverSocket.recv(4096).decode()
            # print(data)
            while data:
                strbuffer += data
                data = transerverSocket.recv(4096).decode()

            # close the sockets
            transerverSocket.close()
            print(data)
            # Send data back to web client
            return strbuffer

        except IOError as err:
            # Send response message for file not found
            # connectionSocket.send('HTTP/ 1.1 404 NOT FOUND'.encode())
            print(err)

            # Close sockets
            transerverSocket.close()

    webserverSocket.close()

# looks for forward slash to indicate index
@app.route('/',  methods=['GET','POST'])
def index():
    # Get request for data from server
    if request.method == 'GET':
        # render_template looks for the directory 'template' then 'index.html'. Flask is smart.
        return render_template('index.html')
    # Sends data to a server
    elif request.method == 'POST':

        # received some data from web client
        # (https://stackoverflow.com/questions/40610644/python-3-flask-how-to-send-data-to-server)
        print(request.form)

        # request_info gets parameters from workload generator (or user from browser)
        response_message = request_info(
            command=request.form.get('request_type', None),
            user=request.form.get('username', None),
            stock_sym=request.form.get('stock_sym', None),
            amount=request.form.get('amount', None),
            filename=request.form.get('filename', None)
        )

        # look in "template" directory
        return render_template('index.html', response_message=response_message)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

# run the web server on IP address and port
if __name__ == "__main__":
    app.run(host='localhost', port=5000)