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

from exception_handling import print_exception_str
from exception_handling import handle_exception_and_exit


class SocketConnection:

    socket_wrap: SocketWrap
    HOST: str
    PORT: int

    def set_host_port(self, host, port):
        self.HOST = host
        self.PORT = port

    def socket_create(self):
        """This function calls the socket() and setsockopt() methods;
            socket is set to be reusable.
            """
        self.socket_wrap.init(AF_INET, SOCK_STREAM)
        self.socket_wrap.set_socket_options(SOL_SOCKET, SO_REUSE_ADDRESS, 1)
        return self.socket_wrap

    def close(self):
        """only printing exception name if one happens"""
        try:
            self.socket_wrap.shutdown(SHUT_RD_WR)
            self.socket_wrap.close()
        except OSError as os:
            # trying to close a non existing fd;
            # client might have closed the connection already
            print_exception_str(os)
        except Exception as e:
            print_exception_str(e)


class ServerSocketConnection(SocketConnection):

    socket_wrap: ServerSocketWrap
    connection_queue_size: int = 2

    def socket_create_bind_and_listen(self) -> ServerSocketWrap:
        """Function to return a listening socket, called on Server side"""
        self.socket_wrap = ServerSocketWrap()
        self.socket_create()
        self.socket_bind()
        self.socket_listen()
        return self.socket_wrap

    def socket_bind(self):
        """Call of bind() and its OSError catching."""
        try:
            self.socket_wrap.bind(self.HOST, self.PORT)
        except OSError as ose:
            handle_exception_and_exit(ose, 2000)

    def socket_listen(self):
        """Calls listen method with a given queue size"""
        self.socket_wrap.listen(self.connection_queue_size)

    def socket_accept(self) -> tuple:
        """Calling the socket.accept() method and catching BlockingIOError"""
        try:
            client_soc = self.socket_wrap.accept()
        except BlockingIOError:
            return ()

        return client_soc


class ClientSocketConnection(SocketConnection):

    socket_wrap: ClientSocketWrap

    def socket_create_and_connect(self) -> ClientSocketWrap:
        """Function to return a connected socket, called on client side"""
        self.socket_wrap = self.create_client()
        self.connect(self.HOST, self.PORT)
        return self.socket_wrap

    def create_client(self):
        """This function calls the socket() and setsockopt() methods;
            socket is set to be reusable.
            """
        self.socket_wrap = ClientSocketWrap()
        self.socket_wrap.init(AF_INET, SOCK_STREAM)
        self.socket_wrap.set_socket_options(SOL_SOCKET, SO_REUSE_ADDRESS, 1)
        return self.socket_wrap

    def connect(self, host: str, port: int):
        """Function to connect to specific host and port"""
        remote_ip = get_host_by_name(host)
        self.socket_wrap.connect(remote_ip, port)
        return self.socket_wrap
