import socket

HOST = 'localhost'
PORT = 9090

while True:
    sock = socket.socket()
    sock.connect((HOST, PORT))

    request = input('my_ftp_server ')
    sock.send(request.encode())

    response = sock.recv(1024).decode()
    print(response)

    sock.close()

    if request == 'exit':
        break
