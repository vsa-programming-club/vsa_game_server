# vsa game server

# started from https://stackoverflow.com/questions/36060346/creating-a-simple-chat-application-in-python-sockets

import socket, threading, struct

server_password = input("password:")

# list of person, socket, list of registered services
clientlist = []

def send_one_message(sock, data):
    length = len(data)
    sock.sendall(struct.pack('!I', length))
    sock.sendall(data)
    
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf
    
def recv_one_message(sock):
    lengthbuf = recvall(sock, 4)
    length, = struct.unpack('!I', lengthbuf)
    return recvall(sock, length)

def accept_client():
    while True:
        client_sock, client_address = server_socket.accept()
        person = recv_one_message(client_sock)
        password = recv_one_message(client_sock)
        if password.decode() != server_password:
            print("invalid password:",person.decode(),password.decode())
            client_sock.close()
        else:
            client = (person, client_sock, [])
            clientlist.append(client)
            print(person.decode(),client_address,'is now connected')
            thread_client = threading.Thread(target = process_client, args=[client])
            thread_client.start()

def process_client(client):
    person = client[0]
    client_sock = client[1]
    while True:
        try:
            # blocking call, hence one thread per client
            payload = recv_one_message(client_sock)
            if payload:
                msg = person.decode() + ":" + payload.decode()
                # log everything
                print(msg)
                broadcast_msg(client, msg)
        except Exception as x:
            print("Exception:",x)
            clientlist.remove(client)
            print("Dropping connection for",person.decode())
            break

def broadcast_msg(client, msg):
    person = client[0]
    client_sock = client[1]
    fromuser,touser,program,payload = msg.split(':',3)
    #print(fromuser,touser,program,payload)
    if touser == 'SYS':
        if program == 'REG':
            client[2].append(payload)
            print(client[2])
        elif program == 'UNREG':
            client[2].remove(payload)
    else:
        service = fromuser+':'+program
        allservice = 'ALL:'+program
        for c in clientlist:
            if service in c[2] or (client != c and allservice in c[2]):
                send_one_message(c[1], bytes(msg, 'utf-8'))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())
port = 5023
server_socket.bind((host, port))
server_socket.listen(1)
print('Chat server started on ',host,':',port, sep='')

accept_thread = threading.Thread(target = accept_client)
accept_thread.start()

