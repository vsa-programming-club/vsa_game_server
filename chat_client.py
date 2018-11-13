import socket, threading

def send():
    while True:
        msg = input('CHAT> ')
        client_sock.send(bytes(chattarget+":CHAT:"+msg, 'utf-8'))

def receive():
    while True:
        msg = client_sock.recv(1024).decode("utf-8")
        print(msg)

host = input('Server address:')
port = 5023
username = input('Username:')
password = input('Password:')
chattarget = input('Who do you want to chat with? (username or "ALL")')

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((bytes(host, 'utf-8'), port))     
print('Connected to remote host...')
client_sock.send(bytes(username, 'utf-8'))
client_sock.send(bytes(password, 'utf-8'))
client_sock.send(bytes('SYS:REG:'+chattarget+':CHAT', 'utf-8'))

thread_send = threading.Thread(target = send)
thread_send.start()

thread_receive = threading.Thread(target = receive)
thread_receive.start()
