#!/usr/bin/env python

import socket
import selectors
import types
import json
import _thread

from RobotCommunicator import RobotCommunicator
from service_connection import service_connection


class RobotCommunicatorServer(RobotCommunicator):
    def __init__(self):
        super().__init__('', 65530)

    def start(self):
        tid = _thread.start_new_thread(robot_server, (self.port,
                                                      self._send_queue,
                                                      self._connected_clients,
                                                      self._recv_messages.append,))

    def list_clients(self):
        return list(self._connected_clients)


def robot_server(port, message_queue: list, connected_clients, handle_response):
    recv_queue = []
    sel = selectors.DefaultSelector()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
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
