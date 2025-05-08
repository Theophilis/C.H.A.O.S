import socket

HEADER = 64
PORT = 21621
SERVER = '192.168.1.17'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!disconnect'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

