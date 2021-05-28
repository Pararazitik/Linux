import socket

HOST = 'localhost'
PORT = 9090

while True:
    try:
        request = input('ftp>')
    except:
        break
    sock = socket.socket()
    try:
        sock.connect((HOST, PORT))
    except:
        break
    if request == '':
        continue
    sock.send(request.encode())
    try:
        response = sock.recv(1024).decode()
    except:
        break
    if response == 'exit' or response == 'cstop':
        break
    print(response)

sock.close()