#!/usr/bin/env python

import socket
import selectors
import types
import json
import _thread

from service_connection import service_connection

class RobotCommunicatorServer:
    def __init__(self):
        self._recv_messages = []
        self._send_queue = []
        self._connnected_clients = {}

    def start(self):
        tid = _thread.start_new_thread(robot_server, (self._send_queue,
                                                       self._connnected_clients,
                                                       self._recv_messages.append,))
    def list_clients(self):
        return list(self._connnected_clients)

    def send_message(self, msg: dict, client_id: int):
        if client_id in self._connnected_clients:
            body = msg.copy()
            body['addr'] = self._connnected_clients[client_id]
            self._send_queue.append(body)

    def pop_message(self):
        return self._recv_messages.pop(0)


def robot_server(message_queue: list, connected_clients, handle_response):
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
                    accept_connection(key.fileobj, sel, connected_clients)
                else:
                    service_connection(
                        key, mask, sel, message_queue, recv_queue, connected_clients)

            if len(recv_queue) > 0:
                handle_response(recv_queue.pop(0))


def accept_connection(sock, sel, connected_clients):
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    connected_clients[len(connected_clients)] = addr
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
