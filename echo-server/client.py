import socket


def input_check(message=''):
    message_text = input(message)
    if message_text in ['/stop', '/exit']:
        exit()
    return message_text


while True:
    while True:
        try:
            port = int(input_check(f"Введите порт: "))
        except ValueError:
            print("Неправильный порт")
            continue

        try:
            sock = socket.socket()
            sock.setblocking(True)
            sock.connect(("localhost", port))
            print(f"Подключение к localhost:{port} успешно!\n")
            break
        except (socket.gaierror, ConnectionRefusedError) as e:
            print(f"Не удается подключиться к localhost:{port} ({e})!")

    while True:
        try:
            data = sock.recv(1024)
            print(data.decode())

            messageText = input_check(">>")
            if messageText == '':
                messageText = 'None'
            elif messageText == '/close':
                print(f"Отключение от localhost:{port}\n")
                sock.shutdown(0)
                break
            sock.send(messageText.encode())
        except (ConnectionRefusedError, ConnectionAbortedError, ConnectionResetError) as exeption:
            print(exeption)
            break

    sock.close()
