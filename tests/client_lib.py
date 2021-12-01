import socket
import sys
import traceback

host: str = ""
port: int = 5421

connection_queue_size: int = 2
buffer_size: int = 512
message_length: int = 1024

encoding_type: str = "utf-8"
close_bytes: bytes = b"\r\n"


def socket_create() -> socket:
    """This function calls the socket() and setsockopt() methods;
    socket is set to be reusable."""
    socket_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return socket_fd


def send_bytes_to_socket(c_socket: socket, msg: bytes) -> int:
    """Utilizing send() in a while loop: send(msg[bytes_send:]).
    Also catching BrokenPipeError."""
    bytes_send = 0
    while bytes_send < len(msg):
        try:
            bytes_send += c_socket.send(msg[bytes_send:])
        except BrokenPipeError as bpe:
            handle_exception(bpe, "can't send, client disconnected")
        if not bytes_send:
            break
    return bytes_send


def receive_bytes_from_socket(c_socket: socket) -> bytes:
    """Calling recv() in a while loop using a bytearray to append
    the received buffer to a result value witch can be returned."""
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


def handle_exception_and_exit(e: Exception, exitcode: int = 420, error_message: str = ""):
    print(e)
    print(traceback.format_exc())
    if error_message != "":
        print(error_message)
    sys.exit(exitcode)


def handle_exception(e: Exception, error_message: str = "error 421"):
    print(e)
    print(traceback.format_exc())
    print(error_message)
