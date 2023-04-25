"""
This module provides classes for creating a RobotCommunicator that can send and receive messages
between a RobotCommunicatorServer and RobotCommunicatorClient.

Classes:
    - RobotCommunicator: The base class for handling communication between server and client.
    - RobotCommunicatorServer: Inherits from RobotCommunicator; represents the server-side implementation.
    - RobotCommunicatorClient: Inherits from RobotCommunicator; represents the client-side implementation.
"""

import socket
import selectors
import types
import json
import _thread


class RobotCommunicator:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._recv_messages = []
        self._send_queue = []
        self._connected_clients = {}

    def send_message(self, msg: dict, client_id) -> bool:
        """
        Sends a message to the specified client.
        Blocks untill the message is sent to the send buffer

        :param msg: The message to be sent as a dictionary.
        :param client_id: The ID of the client to send the message to.
        :return: True if the message was sent, False otherwise.
        """
        if client_id in self._connected_clients:
            body = msg.copy()
            body['addr'] = self._connected_clients[client_id]
            self._send_queue.append(body)
            while len(self._send_queue) > 0:
                pass
            return True
        else:
            print("Error: could not send message to server")
            return False

    def pop_message(self) -> dict:
        """
        Retrieves the next message from the received messages queue.
        :return: The next message in the queue as a dictionary or an empty
        dictionary if the queue is empty.
        """
        if len(self._recv_messages) > 0:
            return self._recv_messages.pop(0)
        else:
            return {}


class RobotCommunicatorServer(RobotCommunicator):
    def __init__(self, ip, port):
        super().__init__(ip, port)

    def start(self):
        tid = _thread.start_new_thread(robot_tcp_server, (self.port,
                                                          self._send_queue,
                                                          self._connected_clients,
                                                          self._recv_messages.append,))

    def list_clients(self):
        return list(self._connected_clients)


class RobotCommunicatorClient(RobotCommunicator):
    def __init__(self, host, port):
        super().__init__(host, port)

    def start(self):
        tid = _thread.start_new_thread(robot_tcp_client, (self.host,
                                                          self.port,
                                                          self._send_queue,
                                                          self._connected_clients,
                                                          self._recv_messages.append,))
        while len(self._connected_clients) < 1:
            pass

    def send_message(self, msg: dict):
        super().send_message(msg, 0)

    def is_connected(self) -> bool:
        return len(self._connected_clients) > 0


def robot_tcp_client(host, port, message_queue, connected_clients, handle_message):
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
                handle_message(recv_queue.pop(0))


def robot_tcp_server(port, message_queue: list, connected_clients, handle_response):
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
    """
    Accepts a connection from a client
    """
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    connected_clients[len(connected_clients)] = addr
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask, sel, send_queue: list, recv_queue: list, connected_clients: dict):
    """
    Sends messages from send_queue and inserts messages in the recv_queue
    """
    sock = key.fileobj
    data = key.data
    data.message_length = 0

    # Put messagges in the send buffer
    if len(send_queue) > 0:
        if data.addr == tuple(send_queue[0]['addr']):
            message = send_queue.pop(0)
            body = json.dumps(message).encode('utf-8')
            data.outb += len(body).to_bytes(2, 'big')
            data.outb += body

    # Put messages in the read buffer
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            print("Received: ", recv_data, "from", data.addr)
            data.inb += recv_data

            if len(data.inb) >= 2 and data.message_length == 0:
                data.message_length = int.from_bytes(data.inb[:2])
                data.inb = data.inb[2:]

            if len(data.inb) >= data.message_length:
                message = json.loads(data.inb[:data.message_length])
                data.inb = data.inb[data.message_length:]
                recv_queue.append(message)

        else:
            print(f"Closing connection to {data.addr}")

            for client_id, addr in list(connected_clients.items()):
                if addr == data.addr:
                    del connected_clients[client_id]

            sel.unregister(sock)
            sock.close()

    # Send messages in the send buffer
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Sending {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]
