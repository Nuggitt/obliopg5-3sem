from socket import *
import json

serverName = "localhost"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

keep_communacating = True

while keep_communacating:
    Method = input('\nWelcome here is your options \nMenu: Random, Add, Subtract, close: ')
    if Method == "close":
        request = json.dumps({"Method": Method})
        keep_communacating = False
    else:
        number1 = int(input('Enter tal1: '))
        number2 = int(input('Enter tal2: '))
        request = json.dumps({"Method": Method, "tal1": number1, "tal2": number2})

    clientSocket.send(request.encode())
    response = clientSocket.recv(1024).decode()
    print('From server: ', response)
clientSocket.close()