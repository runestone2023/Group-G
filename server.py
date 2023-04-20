#!/usr/bin/env python

import socket
import selectors
import types
import json

from service_connection import service_connection


def robot_server(message_queue: list, handle_response):
    recv_queue = []
    sel = selectors.DefaultSelector()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', 65530))
        s.listen(5)
        s.setblocking(False)
        sel.register(s, selectors.EVENT_READ, data=None)

        while True:
            events = sel.select(timeout=10)
            for key, mask in events:
                if key.data is None:
                    accept_connection(key.fileobj, sel)
                else:
                    service_connection(
                        key, mask, sel, message_queue, recv_queue)

            if len(recv_queue) > 0:
                handle_response(recv_queue.pop(0), message_queue)


def connected_clients(sel) -> list:
    result = []
    for elem in sel.get_map():
        key = sel.get_key(elem)
        if key.data is not None:
            result.append(key.data.addr)
    return result


def accept_connection(sock, sel):
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


if __name__ == "__main__":
    send_queue = []

    robot_server(send_queue, print)
