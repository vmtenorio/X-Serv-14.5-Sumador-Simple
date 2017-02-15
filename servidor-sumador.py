#!/usr/bin/python3

import socket

# Create a TCP objet socket and bind it to a port
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Let the port be reused if no process is actually using it
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to the address corresponding to the main name of the host
mySocket.bind((socket.gethostname(), 1234))

# Queue a maximum of 5 TCP connection requests

mySocket.listen(5)

def endErr(recvSocket, str):
    recvSocket.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n<html><body>" + str + "</body></html>\r\n", 'utf-8'))
    recvSocket.close()

# Accept connections, read incoming data, and answer back an HTML page
#  (in an almost-infinite loop; the loop can be stopped with Ctrl+C)

first = True

try:
    while True:
        print('Waiting for connections')
        (recvSocket, address) = mySocket.accept()
        petition = recvSocket.recv(2048).decode('utf-8', 'strict')
        operand = petition.split()[1][1:]
        if operand == "favicon.ico":
            endErr(recvSocket, "<h1>Not Found</h1>")
            continue
        try:
            op = int(operand)
        except ValueError:
            endErr(recvSocket, "<p>Me has dado un " + operand + ". Vete</p>")
            continue
        if first:
            op1 = op
            recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n" +
                            "<html><body>" +
                            "<p>Me has dado un " + str(op) + ". Dame mas</p>" +
                            "</body></html>" +
                            "\r\n", 'utf-8'))
            first = False
        else:
            op2 = op
            recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n" +
                            "<html><body>" +
                            "<p>Me habias dado un " + str(op1) + ". Ahora un " + str(op2) + ". Suman " + str(op1 + op2) + "</p>" +
                            "</body></html>" +
                            "\r\n", 'utf-8'))
            first = True
        recvSocket.close()
except KeyboardInterrupt:
    print("Closing binded socket")
    mySocket.close()
