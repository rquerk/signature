import socket

AF_INET = socket.AF_INET
SOCK_STREAM = socket.SOCK_STREAM
SOL_SOCKET = socket.SOL_SOCKET
SO_REUSE_ADDRESS = socket.SO_REUSEADDR
SHUT_RD_WR = socket.SHUT_RDWR


def get_host_by_name(host):
    return socket.gethostbyname(host)


class SocketWrap:
    socket_obj: socket.socket

    def init(self, family: int, socket_type: int):
        self.socket_obj = socket.socket(family, socket_type)

    def send(self, data: bytes):
        return self.socket_obj.send(data)

    def receive(self, buffer_size: int):
        return self.socket_obj.recv(buffer_size)

    def shutdown(self, how: int):
        self.socket_obj.shutdown(how)

    def close(self):
        self.socket_obj.close()

    def set_socket_options(self, level: int, opt_name: int, value):
        self.socket_obj.setsockopt(level, opt_name, value)

    def set_blocking(self, block: bool):
        self.socket_obj.setblocking(block)


class ServerSocketWrap(SocketWrap):

    def bind(self, host, port):
        self.socket_obj.bind((host, port))

    def listen(self, backlog):
        self.socket_obj.listen(backlog)

    def accept(self):
        return self.socket_obj.accept()


class ClientSocketWrap(SocketWrap):

    def connect(self, ip, port):
        return self.socket_obj.connect((ip, port))

    def is_valid(self):
        if self.socket_obj != -1 and self.socket_obj is not None:
            return True
