#!/usr/bin/env python

import socket
import selectors
import types

def main():
    sel = selectors.DefaultSelector()
    send_queue = []
    recv_queue = []

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        port = 65530
        s.bind(('', port))
        s.listen(5)
        s.setblocking(False)
        sel.register(s, selectors.EVENT_READ, data=None)

        while True:
            # Send and recv messages
            events = sel.select(timeout=10)
            for key, mask in events:
                if key.data is None:
                    accept_connection(key.fileobj, sel)
                else:
                    service_connection(
                        key, mask, sel, send_queue, recv_queue)


def accept_connection(sock, sel):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask, sel, send_queue, recv_queue):
    sock = key.fileobj
    data = key.data
    print(data)

    # Put messagges in the send buffer
    if len(send_queue) > 0:
        if data.addr == send_queue[0].receiver:
            data.outb += send_queue.pop(0)

    # Put messages in the read buffer
    if mask & selectors.EVENT_READ:
        print(key)
        recv_data = sock.recv(1024)
        if recv_data: 
            print("Received: ", recv_data, " from ", data.addr)
            data.inb += recv_data
            # TODO: Parse message
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()

    # Send messages in the send buffer
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


if __name__ == "__main__":
    main()
