import socket
import threading


def sendMessage(client_socket):
    message = input()  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message

        message = input()  # again take input

    client_socket.send(message.encode())  # send message
    client_socket.close()  # close the connection


def receiveResponse(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()  # receive response
        except:
            client_socket.close()
            break
        
        if data == 'bye':
            client_socket.close()
            break
        print(data)  # show in terminal



def client_program():
    #host = socket.gethostname()  # as both code is running on same pc
    port = 8090  # socket server port number

    username = input('Enter a username: ')

    client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)  # instantiate
    client_socket.connect(('localhost', port))  # connect to the server

    data = client_socket.recv(1024).decode()
    if data == 'getUsername':
        client_socket.send(username.encode())

    threadSendMessage = threading.Thread(target=sendMessage, args=(client_socket,))
    threadSendMessage.start()

    threadReceiveResponse = threading.Thread(target=receiveResponse, args=(client_socket,))
    threadReceiveResponse.start()


if __name__ == '__main__':
    client_program()
