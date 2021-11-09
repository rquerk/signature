import socket
import ExceptionHandling as Exc
from ExceptionHandling import handle_exception_and_exit


HOST: str = ""
PORT: int = 5421


connection_queue_size: int = 2


def socket_create() -> socket:
    """This function calls the socket() and setsockopt() methods;
    socket is set to be reusable.
    """
    socket_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return socket_fd


def socket_bind(s_socket: socket, host: str, port: int):
    """Call of bind() and its OSError catching."""
    try:
        s_socket.bind((host, port))
    except OSError as ose:
        handle_exception_and_exit(ose, 2000)


def socket_listen(s_socket: socket):
    """Just calls the listen() method."""
    s_socket.listen(connection_queue_size)


def socket_create_bind_and_listen() -> socket:
    """Function to return a listening socket, called on Server side"""
    server_socket = socket_create()
    socket_bind(server_socket, HOST, PORT)
    socket_listen(server_socket)
    return server_socket


def socket_connect(c_socket: socket, host: str, port: int):
    """Function to connect to specific host and port"""
    remote_ip = socket.gethostbyname(host)
    c_socket.connect((remote_ip, port))
    return c_socket


def socket_create_and_connect() -> socket:
    """Function to return a connected socket, called on client side"""
    c_socket = socket_create()
    socket_connect(c_socket, HOST, PORT)
    return c_socket


def socket_accept(s_socket: socket) -> tuple:
    """Calling the socket.accept() method and catching BlockingIOError"""
    try:
        client_soc = s_socket.accept()
    except BlockingIOError:
        return ()

    return client_soc


def socket_close(soc: socket):
    """only printing exception name if one happens"""
    try:
        soc.shutdown(socket.SHUT_RDWR)
        soc.close()
    except OSError as os:
        # trying to close a non existing fd;
        # client might have closed the connection already
        Exc.print_exception_str(os)
    except Exception as e:
        Exc.print_exception_str(e)
