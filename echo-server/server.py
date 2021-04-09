import socket
import logging
import datetime
import sqlite3

db = sqlite3.connect("echoServer.db")
cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS clients("
               "ip VARCHAR PRIMARY KEY,"
               "name VARCHAR NOT NULL,"
               "pwd_hash VARCHAR)")

logging.basicConfig(filename='Change.log', level=logging.INFO)

sock = socket.socket()
port = 9090
endPort = 10000


def exitServer():
    db.close()
    exit()


def ChangeName(ip, name):
    cursor.execute("UPDATE clients SET name =? WHERE ip = ?", (name, ip))
    db.commit()

    return f"Имя успешно измененно на {name}!"


def toWrite(log, message):
    print(message)
    log(f'--{datetime.now()}--\n{message}\n')


def getDate():
    data = None
    try:
        data = conn.recv(1024).decode()
    except (ConnectionResetError, KeyboardInterrupt) as e:
        toWrite(logging.error, f"Потерняо соединение({e})")

    return data


def identification(ip):

    sql = "SELECT name " \
          "FROM clients " \
          "WHERE ip = ?"

    client = cursor.execute(sql, (ip,)).fetchone()

    if not client:
        conn.send("Введите имя: ".encode())
        name = getDate()
        conn.send(f"Введите пароль: : ".encode())
        password = getDate()

        if name is not None and password is not None:
            cursor.execute("INSERT INTO clients VALUES(?,?,?)", (add[0], name, password))
            db.commit()
        else:
            conn.send("Некорректное имя!".encode())
            toWrite(logging.warning, "Некорректное имя!")

            return None
    else:
        name = client[0]

    conn.send(f"Идентификация прошла успешно".encode())

    return name

while True:
    if port > endPort:
        toWrite(logging.error, "Не свободных портов")
    try:
        sock.bind(('', port))
        toWrite(logging.info, f"Порт: {port}")
        break
    except OSError:
        port += 1

while True:
    toWrite(logging.info, f"Ждём на порте: {port}")
    sock.listen(1)

    try:
        conn, add = sock.accept()
        ip = add[0]
        number = add[1]
    except KeyboardInterrupt as k:
        toWrite(logging.error, f"Остановка программы: \n{k}")
        exitServer()

    try:
        client_name = identification(add[0])
    except Exception as e:
        print(f"{e}")

    if client_name is None:
        continue

    toWrite(logging.info, f'Пользователь подключился: ({ip}, {number}, {client_name})')

    while True:
        data = getDate()

        print(data)

        if data == "/changename":
            conn.send("Ввведите имя: ".encode())
            newName = getDate()

            messageText = f"({ip}, {number}, {client_name}): {ChangeName(ip, newName)}"

            client_name = newName
            conn.send(messageText.encode())
            toWrite(logging.info, messageText)

            continue

        if data == '':
            break

        conn.send(data.encode())