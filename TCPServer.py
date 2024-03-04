from socket import *
import threading
import random
import json

def handle_quit(json_data):
    return {"Message": "Goodbye closing the connection"}

def handle_random(json_data):
    tal1 = json_data.get('tal1')
    tal2 = json_data.get('tal2')
    if tal1 is None or tal2 is None:
        return {"Error": "Wrong input"}
    else:
        random_number = random.randint(tal1, tal2)
        return {"Random number": random_number}

def handle_add(json_data):
    tal1 = json_data.get('tal1')
    tal2 = json_data.get('tal2')
    if tal1 is None or tal2 is None:
        return {"Error": "Wrong input"}
    else:
        return {"Result": tal1 + tal2}

def handle_sub(json_data):
    tal1 = json_data.get('tal1')
    tal2 = json_data.get('tal2')
    if tal1 is None or tal2 is None:
        return {"Error": "Wrong input"}
    else:
        return {"Result": tal1 - tal2}

def handle_invalid(json_data):
    return {"Error": "Wrong Method"}

def handle_invalid_json(json_data):
    return {"Error": "Invalid JSON format"}

method_handlers = {
    "close": handle_quit,
    "Random": handle_random,
    "Add": handle_add,
    "Subtract": handle_sub,
}

def handleClient(connectionSocket, addr):
    print(addr[0])
    keep_communicating = True

    while keep_communicating:
        sentence = connectionSocket.recv(1024).decode()
        try:
            json_data = json.loads(sentence)
            Method = json_data.get('Method')
            handler = method_handlers.get(Method, handle_invalid)
            response = handler(json_data)
            connectionSocket.send(json.dumps(response).encode())
        except json.JSONDecodeError:
            response = handle_invalid_json({})
            connectionSocket.send(json.dumps(response).encode())

    connectionSocket.close()
    print('Connection closed')

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('Server is ready to listen')

while True:
    connectionSocket, addr = serverSocket.accept()
    threading.Thread(target=handleClient, args=(connectionSocket, addr)).start()
