import socket
import sys
import threading

clients = dict()

def new_client(conn,address, username):
    
    def thread_function():
        print("Connection from: " + str(address))
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024).decode()
            if not data:
                # if data is not received break
                break
            if data == 'bye':
                conn.send('bye'.encode())
                break

            # @user
            u = data.split()[0]
            aux = 0
            for name, client in clients.items():
                if u == '@'+name:
                    msg = '@' + username + ': ' + data
                    client.send(msg.encode())
                        
                    aux = aux + 1

            # All
            if aux == 0:
                for client in clients.values():
                    if conn != client:
                        msg = '@' + username + ': ' + data
                        client.send(msg.encode())

        clients.pop(username, conn)
        conn.close()  # close the connection
        
    return threading.Thread(target=thread_function)
    
def server_program(num_clients):
    # get the hostname
    #host = socket.gethostname()
    
    port = 8090  # initiate port no above 1024

    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) #SOCK_DGRAM for UDP # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind(('localhost', port))  # bind host address and port together
    
    while num_clients > 0:
        # configure how many client the server can listen simultaneously
        print('Server escutando... Cliente N ' + str(num_clients))
        server_socket.listen(num_clients)
        conn, address = server_socket.accept()  # accept new connection

        conn.send('getUsername'.encode())
        username = conn.recv(1024).decode()

        clients[username] = conn

        #criar nova thread para cada nova conexao
        thread_client = new_client(conn,address, username)
        thread_client.start()
        num_clients = num_clients - 1

if __name__ == '__main__':\
    
    server_program(int(sys.argv[1]))
