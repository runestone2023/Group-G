import socket
import selectors
import types
import json
import _thread
from service_connection import service_connection


class RobotCommunicatorClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._recv_messages = []
        self._send_queue = []
        self._connected_clients = {}

    def start(self):
        tid = _thread.start_new_thread(robot_client, (self.host,
                                                      self.port,
                                                      self._send_queue,
                                                      self._connected_clients,
                                                      self._recv_messages.append,))

    def send_message(self, msg: dict):
        try:
            body = msg.copy()
            body['addr'] = self._connected_clients[0]
            self._send_queue.append(body)
        except:
            print("Error: could not send message to server")


    def pop_message(self):
            return self._recv_messages.pop(0)


def robot_client(host, port, message_queue, connected_clients, handle_message):
    recv_queue = []
    sel = selectors.DefaultSelector()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Connecting to", host, port)
        connected_clients[0] = s.getsockname()

        s.connect((host, port))
        s.setblocking(False)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE

        data = types.SimpleNamespace(addr=s.getsockname(), inb=b"", outb=b"")
        sel.register(s, events, data=data)

        while True:
            events = sel.select(timeout=10)
            for key, mask in events:
                if key.data is not None:
                    service_connection(
                        key, mask, sel, message_queue, recv_queue, connected_clients)

            if len(recv_queue) > 0:
                handle_message(recv_queue.pop(0), message_queue)
