"""This is a helper module for sending and receiving bytes over sockets"""

import ExceptionHandling as Exc
from socket import socket

buffer_size: int = 512
message_length: int = 1024

close_bytes: bytes = b"\r\n"


def send_bytes_to_socket(c_socket: socket, msg: bytes) -> int:
    """Utilizing send() in a while loop: send(msg[bytes_send:]).
    Also catching BrokenPipeError.
    """
    bytes_send = 0
    while bytes_send < len(msg):
        try:
            bytes_send += c_socket.send(msg[bytes_send:])
        except BrokenPipeError as bpe:
            Exc.print_exception_str(bpe)
        if not bytes_send:
            break
    return bytes_send


def receive_bytes_from_socket(c_socket: socket) -> bytes:
    """Calling recv() in a while loop using a bytearray to append
    the received buffer to a result value witch can be returned.
    """
    bytes_received = 0
    request: bytearray = bytearray(b"")
    while bytes_received < message_length:
        client_data: bytes = c_socket.recv(buffer_size)
        if not client_data or client_data == b"":
            return b""  # or break?
        bytes_received += len(client_data)
        request.extend(client_data)
        if received_closing_bytes(client_data):
            request = request[:-len(close_bytes)]
            break
    return bytes(request)


def received_closing_bytes(received_bytes: bytes) -> bool:
    if received_bytes[-len(close_bytes):] == close_bytes:
        return True
