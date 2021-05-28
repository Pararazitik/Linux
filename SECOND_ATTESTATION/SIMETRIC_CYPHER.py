import socket
import pickle

HOST = '127.0.0.1'
PORT = 9090

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(1)
conn, addr = sock.accept()

msg = conn.recv(1024)
print(pickle.loads(msg))
conn.send(msg)
conn.close()
import socket
import pickle

HOST = '127.0.0.1'
PORT = 9090

sock = socket.socket()
sock.connect((HOST, PORT))

p, g, a = 7, 5, 3
A = g ** a % p
sock.send(pickle.dumps((p, g, A)))
msg = sock.recv(1024)
print(pickle.loads(msg))
sock.close()


def encrypt(k, m):
    return ''.join(map(chr, (x + k for x in map(ord, m))))


def decrypt(k, m):
    return ''.join(map(chr, (x - k for x in map(ord, m))))


code = input("Введите текст: ")
key = int(input("Введите смещение: "))
codecs = encrypt(key, code)
decodecs = decrypt(key, codecs)

print(code)
print(codecs)
print(decodecs)