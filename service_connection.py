
import selectors
import types
import json

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
