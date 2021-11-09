import socket
import ExceptionHandling as Exc

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
        if not client_data:
            break
        bytes_received += len(client_data)
        request.extend(client_data)
        if client_data[-len(close_bytes):] == close_bytes:
            request = request[:-len(close_bytes)]
            break
    return bytes(request)
