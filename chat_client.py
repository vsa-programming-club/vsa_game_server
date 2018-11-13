import socket, threading, struct

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
    
def send():
    while True:
        msg = input('CHAT> ')
        send_one_message(client_sock, bytes(chattarget+":CHAT:"+msg, 'utf-8'))

def receive():
    while True:
        msg = recv_one_message(client_sock).decode("utf-8")
        print(msg)

host = input('Server address:')
port = 5023
username = input('Username:')
password = input('Password:')
chattarget = input('Who do you want to chat with? (username or "ALL")')

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((bytes(host, 'utf-8'), port))     
print('Connected to remote host...')
send_one_message(client_sock, bytes(username, 'utf-8'))
send_one_message(client_sock, bytes(password, 'utf-8'))
send_one_message(client_sock, bytes('SYS:REG:'+chattarget+':CHAT', 'utf-8'))

thread_send = threading.Thread(target = send)
thread_send.start()

thread_receive = threading.Thread(target = receive)
thread_receive.start()
