import socket

AF_INET = socket.AF_INET
SOCK_STREAM = socket.SOCK_STREAM
SOL_SOCKET = socket.SOL_SOCKET
SO_REUSE_ADDRESS = socket.SO_REUSEADDR
SHUT_RD_WR = socket.SHUT_RDWR


def get_host_by_name(self, host):
    socket.gethostbyname(host)


class SocketWrap:
    socket_obj: socket.socket

    def __init__(self, family: int, socket_type: int):
        self.socket_obj = socket.socket(family, socket_type)

    def shutdown(self, how: int):
        self.socket_obj.shutdown(how)

    def close(self):
        self.socket_obj.close()


class ServerSocketWrap(SocketWrap):

    def set_socket_options(self, level: int, opt_name: int):
        self.socket_obj.setsockopt(level, opt_name)

    def bind(self, host, port):
        self.socket_obj.bind((host, port))

    def listen(self, backlog):
        self.socket_obj.listen(backlog)

    def accept(self):
        self.socket_obj.accept()


class ClientSocketWrap(SocketWrap):

    def connect(self, ip, port):
        self.socket_obj.connect((ip, port))
