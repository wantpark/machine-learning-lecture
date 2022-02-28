import json
import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 8000  # The port used by the server

j = {
    "rain": 0.0,
    "temp": 10.0
}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(bytes(json.dumps(j), encoding="utf-8"))
    data = s.recv(1024)

    print(data.decode('utf-8'))
