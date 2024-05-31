import socket
import os
import shutil

PORT = 9090  # Порт для соединений

WORKING_DIR = 'server_dir'  # Рабочая директория сервера

if not os.path.exists(WORKING_DIR): # Создание рабочей директории, если она не существует
    os.makedirs(WORKING_DIR)


def process(req):
    # Разбиение запроса на отдельные команды
    commands = req.split(' ')
    command = commands[0]

    # Обработки запроса
    if command == 'ls':
        # Вывод списка файлов в рабочей директории
        return '; '.join(os.listdir(WORKING_DIR))

    elif command == 'mkdir':
        # Создание новой папки
        if len(commands) != 2:
            return 'bad request'
        dirname = os.path.join(WORKING_DIR, commands[1])
        try:
            os.makedirs(dirname)
            return f'directory {commands[1]} created'
        except Exception as e:
            return str(e)

    elif command == 'rmdir':
        # Удаление папки
        if len(commands) != 2:
            return 'bad request'
        dirname = os.path.join(WORKING_DIR, commands[1])
        try:
            os.rmdir(dirname)
            return f'directory {commands[1]} removed'
        except Exception as e:
            return str(e)

    elif command == 'rm':
        # Удаление файла
        if len(commands) != 2:
            return 'bad request'
        filename = os.path.join(WORKING_DIR, commands[1])
        try:
            os.remove(filename)
            return f'file {commands[1]} removed'
        except Exception as e:
            return str(e)

    elif command == 'mv':
        # Переименование файла
        if len(commands) != 3:
            return 'bad request'
        oldname = os.path.join(WORKING_DIR, commands[1])
        newname = os.path.join(WORKING_DIR, commands[2])
        try:
            os.rename(oldname, newname)
            return f'{commands[1]} renamed to {commands[2]}'
        except Exception as e:
            return str(e)

    elif command == 'put':
        # Загрузка файла на сервер
        if len(commands) < 3:
            return 'bad request'
        filename = os.path.join(WORKING_DIR, commands[1])
        data = ' '.join(commands[2:])
        try:
            with open(filename, 'w') as f: # Cоздать файл и записать в него данные
                f.write(data)
            return f'file {commands[1]} created'
        except Exception as e:
            return str(e)

    elif command == 'get':
        # Загрузка файла с сервера
        if len(commands) != 2:
            return 'bad request'
        filename = os.path.join(WORKING_DIR, commands[1])
        try:
            with open(filename, 'r') as f: # Открыть файл и прочитать содержимое
                return f.read()
        except Exception as e:
            return str(e)

    elif command == 'exit':
        # Завершение соединения с клиентом
        return 'exit'

    else:
        # Некорректная команда
        return 'bad request'


def start_server():
    sock = socket.socket()  # Создание TCP-сокета
    sock.bind(('', PORT))   # Привязка сокета к указанному порту
    sock.listen()  # Начало прослушивания входящих соединений

    print("Слушаем порт", PORT)
    while True:  # Принимает и обрабатывает входящие соединения
        conn, addr = sock.accept()  # Принятие соединения от клиента
        print(f'Connected by {addr}')

        # Получение запроса от клиента
        request = conn.recv(1024).decode() # из байтов строчку
        print(f'Received request: {request}')

        # Обработка запроса и получение ответа
        response = process(request)

        # Отправка ответа клиенту
        if response == 'exit':
            conn.send(response.encode())
            conn.close()
            break

        conn.send(response.encode()) # ответ клиенту
        conn.close()

    # Закрытие сокета после завершения работы сервера
    sock.close()


if __name__ == '__main__':
    start_server()
