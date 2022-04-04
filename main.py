from socket import *
from py.add import add
import _thread

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 8080
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(("localhost", serverPort))
serverSocket.listen(10)
print('The server is running')


# Server should be up and running and listening to the incoming connections
# Extract the given header value from the HTTP request message
def getHeader(message, header):
    if message.find(header) > -1:
        value = message.split(header)[1].split()[0]
    else:
        value = None
    return value

# service function to fetch the requested file, and send the contents back to the client in a HTTP response.
def getFile(filename):
    try:
        f = open(filename, "rb")
        body = f.read()
        header = ("HTTP/1.1 200 OK\r\n\r\n").encode()
    except IOError:
        # Send HTTP response message for resource not found
        header = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
        body = "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode()
    return header, body

def file(filename, par):
    header = "HTTP/1.1 200 OK\r\n\r\n".encode()
    body = filename.application(par)
    return header, body

# service function to generate HTTP response with a simple welcome message
def welcome(message):
    header = "HTTP/1.1 200 OK\r\n\r\n".encode()
    body = ("<html><head></head><body><h1>Welcome to my homepage</h1></body></html>\r\n").encode()
    return header, body

def getFiles(filename, par):
    body = (
            "<html><head></head><body><h1></h1></body></html><script>window.location.replace('http://localhost:8080/portfolio.html');localStorage.setItem('token'," + "'" + par + "'" + ");</script>\r\n").encode()
    header = ("HTTP/1.1 200 OK\r\n\r\n").encode()
    return header, body

def auth():
    header = "HTTP/1.1 200 OK\r\n\r\n".encode()
    body = ("<html><head></head><body><h1>Please log in first</h1></body></html>\r\n").encode()
    return header, body

# default service function
def default(message):
    header, body = welcome(message)
    return header, body

# We process client request here. The requested resource in the URL is mapped to a service function which generates the HTTP reponse
# that is eventually returned to the client.
def process(connectionSocket):
    # Receives the request message from the client
    message = connectionSocket.recv(1024).decode()
    print(len(message.split()))
    resource = message.split()[1]
    path = resource.split("?")[0]
    print(message.find("MjIwMTE3ODg6MjIwMTE3ODg=") > 0)
    if path == "/portfolio.json":
        responseHeader, responseBody = getFile("py/portfolio.json")
        # Send the HTTP response header line to the connection socket
        connectionSocket.send(responseHeader)
        # Send the content of the HTTP body (e.g. requested file) to the connection socket
        connectionSocket.send(responseBody)
        # Close the client connection socket
        connectionSocket.close()
    if (message.find("MjIwMTE3ODg6MjIwMTE3ODg=") > 0):
        if path == "/add.py":
            qruey = resource.split("?")[1]
            header = "HTTP/1.1 200 OK\r\n\r\n".encode()
            responseBody = add(qruey)
            responseHeader, responseBody = getFile("portfolio.html")
            # Send the HTTP response header line to the connection socket
            connectionSocket.send(header)
            # Send the content of the HTTP body (e.g. requested file) to the connection socket
            connectionSocket.send(responseBody)
            # Close the client connection socket
            connectionSocket.close()
        if path == "/research.html":
            responseHeader, responseBody = getFile("research.html")
            # Send the HTTP response header line to the connection socket
            connectionSocket.send(responseHeader)
            # Send the content of the HTTP body (e.g. requested file) to the connection socket
            connectionSocket.send(responseBody)
            # Close the client connection socket
            connectionSocket.close()
        if path == "/portfolio.html":
            responseHeader, responseBody = getFile("portfolio.html")
            # Send the HTTP response header line to the connection socket
            connectionSocket.send(responseHeader)
            # Send the content of the HTTP body (e.g. requested file) to the connection socket
            connectionSocket.send(responseBody)
            # Close the client connection socket
            connectionSocket.close()
        if path == "/" or path == "/index.html":
            responseHeader, responseBody = getFile("index.html")
            # Send the HTTP response header line to the connection socket
            connectionSocket.send(responseHeader)
            # Send the content of the HTTP body (e.g. requested file) to the connection socket
            connectionSocket.send(responseBody)
            # Close the client connection socket
            connectionSocket.close()
    # map requested resource (contained in the URL) to specific function which generates HTTP response
    else:
        response_line = "HTTP/1.1 401 OK\r\n"
        response_header = "WWW-authenticate:Basic Realm='test'\r\n"
        response_data = (response_line + response_header + "\r\n").encode("utf-8")
        # Send the content of the HTTP body (e.g. requested file) to the connection socket
        connectionSocket.send(response_data)
        # Close the client connection socket
        connectionSocket.close()

while True:
    # Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()
    # Clients timeout after 60 seconds of inactivity and must reconnect.
    # start new thread to handle incoming request
    _thread.start_new_thread(process, (connectionSocket,))
