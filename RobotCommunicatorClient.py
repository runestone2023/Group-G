import socket
import selectors
import types
import json
import _thread

from RobotCommunicator import RobotCommunicator
from service_connection import service_connection


class RobotCommunicatorClient(RobotCommunicator):
    def __init__(self, host, port):
        super().__init__(host,port)

    def start(self):
        tid = _thread.start_new_thread(robot_client, (self.host,
                                                      self.port,
                                                      self._send_queue,
                                                      self._connected_clients,
                                                      self._recv_messages.append,))
    def send_message(self, msg: dict):
        super().send_message(msg, 0)


def robot_client(host, port, message_queue, connected_clients, handle_message):
    recv_queue = []
    sel = selectors.DefaultSelector()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Connecting to", host, port)

        s.connect((host, port))
        s.setblocking(False)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE

        data = types.SimpleNamespace(addr=s.getsockname(), inb=b"", outb=b"")
        sel.register(s, events, data=data)

        connected_clients[0] = s.getsockname()
        while True:
            events = sel.select(timeout=10)
            for key, mask in events:
                if key.data is not None:
                    service_connection(
                        key, mask, sel, message_queue, recv_queue, connected_clients)

            if len(recv_queue) > 0:
                handle_message(recv_queue.pop(0), message_queue)
