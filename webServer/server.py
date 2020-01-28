# To run: python3 server.py
# requires install of "flask": pip install flask
# Go to in browser: localhost:5000/

# from http.server import HTTPServer, BaseHTTPRequestHandler

from flask import Flask, render_template, request
import socket
app = Flask(__name__)

# class Serv(BaseHTTPRequestHandler):
#     def do_GET(self):
#         #read the index page
#         if self.path == '/':
#             self.path = '/index.html'
#         try:
#             file_to_open = open(self.path[1:]).read()
#             self.send_response(200)
#             print("connection successful")
#         except:
#             file_to_open = "File not found"
#             self.send_response(404)
#         self.end_headers()
#         self.wfile.write(bytes(file_to_open, 'utf-8'))

# gets transaction info from user/generator
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

    # make a TCP/IP socket to transaction server
    TransServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # address (ip and port) of where the transaction server is listening
    server_address = ('transaction.serv', 44405)

    TransServerSocket.connect(server_address)
    try:
        # Send data
        message = str(data)
        TransServerSocket.sendall(message)
        response = TransServerSocket.recv(1024)
        print(response)

    except IOError:
        # Send response message for file not found
        TransServerSocket.send('HTTP/ 1.1 404 NOT FOUND\r\n\r\n')
        # close the socket
        TransServerSocket.close()

    return response

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
            # transaction_number=0,
            command=request.form.get('command', None),
            user=request.form.get('username', None),
            stock_sym=request.form.get('stock_sym', None),
            amount=request.form.get('amount', None),
            filename=request.form.get('filename', None)
        )

        # look in "template" directory
        return render_template('index.html', response_message=response_message)

# run the web server on IP address and port
if __name__ == "__main__":
    app.run(host='localhost', port=5000)

# httpd = HTTPServer(('localhost', 8080), Serv)
# httpd.serve_forever()
