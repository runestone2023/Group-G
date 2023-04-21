class RobotCommunicator:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self._recv_messages = []
        self._send_queue = []
        self._connected_clients = {}

    def send_message(self, msg: dict, client_id):
        try:
            body = msg.copy()
            body['addr'] = self._connected_clients[client_id]
            self._send_queue.append(body)
        except:
            print("Error: could not send message to server")

    def pop_message(self):
        if len(self._recv_messages) > 0:
            return self._recv_messages.pop(0)
        else:
            return None
