"""Module to establish a TCP socket connection"""

from socket_wrapper import AF_INET
from socket_wrapper import SOCK_STREAM
from socket_wrapper import SOL_SOCKET
from socket_wrapper import SO_REUSE_ADDRESS
from socket_wrapper import SHUT_RD_WR
from socket_wrapper import SocketWrap
from socket_wrapper import ServerSocketWrap
from socket_wrapper import ClientSocketWrap
from socket_wrapper import get_host_by_name

import ExceptionHandling as Exc
from ExceptionHandling import handle_exception_and_exit


HOST: str = ""
PORT: int = 5421


connection_queue_size: int = 2


def socket_create_bind_and_listen() -> ServerSocketWrap:
    """Function to return a listening socket, called on Server side"""
    server_socket = socket_create()
    socket_bind(server_socket, HOST, PORT)
    socket_listen(server_socket)
    return server_socket


def socket_create():
    """This function calls the socket() and setsockopt() methods;
        socket is set to be reusable.
        """
    socket_fd = ServerSocketWrap()
    socket_fd.init(AF_INET, SOCK_STREAM)
    socket_fd.set_socket_options(SOL_SOCKET, SO_REUSE_ADDRESS, 1)
    return socket_fd


def socket_create_client():
    """This function calls the socket() and setsockopt() methods;
        socket is set to be reusable.
        """
    socket_fd = ClientSocketWrap()
    socket_fd.init(AF_INET, SOCK_STREAM)
    socket_fd.set_socket_options(SOL_SOCKET, SO_REUSE_ADDRESS, 1)
    return socket_fd


def socket_bind(s_socket: ServerSocketWrap, host: str, port: int):
    """Call of bind() and its OSError catching."""
    try:
        s_socket.bind(host, port)
    except OSError as ose:
        handle_exception_and_exit(ose, 2000)


def socket_listen(s_socket: ServerSocketWrap):
    """Calls listen method with a given queue size"""
    s_socket.listen(connection_queue_size)


def socket_accept(s_socket: ServerSocketWrap) -> tuple:
    """Calling the socket.accept() method and catching BlockingIOError"""
    try:
        client_soc = s_socket.accept()
    except BlockingIOError:
        return ()

    return client_soc


# Following two functions should only be available on client side
def socket_create_and_connect() -> ClientSocketWrap:
    """Function to return a connected socket, called on client side"""
    c_socket = socket_create_client()
    socket_connect(c_socket, HOST, PORT)
    return c_socket


def socket_connect(c_socket: ClientSocketWrap, host: str, port: int):
    """Function to connect to specific host and port"""
    remote_ip = get_host_by_name(host)
    c_socket.connect(remote_ip, port)
    return c_socket


def socket_close(soc: SocketWrap):
    """only printing exception name if one happens"""
    try:
        soc.shutdown(SHUT_RD_WR)
        soc.close()
    except OSError as os:
        # trying to close a non existing fd;
        # client might have closed the connection already
        Exc.print_exception_str(os)
    except Exception as e:
        Exc.print_exception_str(e)
