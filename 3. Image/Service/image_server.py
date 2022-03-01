#!/usr/bin/env python3

# https://github.com/realpython/materials/blob/master/python-sockets-tutorial/multiconn-server.py

from ast import While
from PIL import Image

import socket
import selectors
# import threading
import types
import numpy as np

import image_class


sel = selectors.DefaultSelector()

HOST = "0.0.0.0"
PORT = 8000

IMG_DATA = 76800  # 160 * 160 * 3
IMG_SIZE = 160


def classify(data, recv_data):
    np_array = np.frombuffer(recv_data, dtype=np.uint8)
    np_array = np_array.reshape((IMG_SIZE, IMG_SIZE, 3))
    img = Image.fromarray(np_array)

    result = image_class.run(img)
    data.outb += result.encode("utf-8")


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")

    # conn.setblocking(False)

    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE

    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = bytearray()

        while True:
            recv = sock.recv(1024 * 100)

            if not recv:
                break
            else:
                recv_data.extend(recv)

            if IMG_DATA == len(recv_data):
                classify(data, recv_data)
                return

        if 0 == len(recv_data):
            print(f"Closing connection to {data.addr}")

            sel.unregister(sock)
            sock.close()
        else:
            data.outb += "error".encode("utf-8")

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
