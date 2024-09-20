import socket
import threading
import time

HEADER = 64
PORT = 21621
SERVER = '192.168.1.17'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!disconnect'

print(SERVER)
print(PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print('new connection')
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(addr, msg)
            if msg == DISCONNECT_MESSAGE:
                 connected = False

    conn.close()


def start():
    server.listen()
    print()
    print(f"server is listening on {(SERVER, PORT)}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"active connections {threading.active_count()-1}")

print("starting server")
start()

