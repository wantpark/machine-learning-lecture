#!/usr/bin/env python3

# https://github.com/realpython/materials/blob/master/python-sockets-tutorial/multiconn-server.py

import json
import socket
import selectors
import threading
import types

import bike_forecast

sel = selectors.DefaultSelector()

HOST = "0.0.0.0"
PORT = 8000


def forecast(data, recv_data):
    j = json.loads(recv_data.decode("utf-8"))

    result = bike_forecast.run(j["rain"], j["temp"])

    data.outb += result.encode("utf-8")


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")

    conn.setblocking(False)

    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE

    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read

        if recv_data:
            t = threading.Thread(target=forecast, args=(data, recv_data))
            t.start()
        else:
            print(f"Closing connection to {data.addr}")

            sel.unregister(sock)
            sock.close()

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Response {data.outb} to {data.addr}")

            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((HOST, PORT))
lsock.listen()

print(f"Listening on {PORT}")

lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)

        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
