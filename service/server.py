"""Implementing the logic of the service"""

from I_service import ABService
from lib.service import Service
from lib.send.sending import Transmitter
import lib.selector as selector
from lib.establish_connection import ServerSocketConnection
from lib.socket_wrapper import ClientSocketWrap
from time import sleep


class Server:
    server_socket: ServerSocketConnection
    clients: list = []

    def __init__(self):
        self.server_socket = ServerSocketConnection()
        self.server_socket.set_host_port("", 5421)

    def start(self):
        self.server_socket.socket_create_bind_and_listen()
        self.server_socket.socket_wrap.set_blocking(False)

    def new_client(self):
        self.accept_new_client_and_push_to_waiting_list()
        return self.get_wrapped_client_from_waiting_list()

    def accept_new_client_and_push_to_waiting_list(self):
        client_tuple: tuple = self.server_socket.socket_accept()
        if is_valid(client_tuple):
            self.fill_client_waiting_list(client_tuple)

    def fill_client_waiting_list(self, client_tuple: tuple):
        self.clients.append(client_tuple[0])

    def get_wrapped_client_from_waiting_list(self):
        ready_client_socket = selector.select_client_socket(self.clients)
        if ready_client_socket is not None:
            wrapped_client = wrap_client_socket(ready_client_socket)
            return wrapped_client

    def process_client(self, service: ABService):
        if service.is_valid() and len(self.clients) > 0:
            service.serve(self.clients)


def is_valid(client_tuple: tuple) -> bool:
    if client_tuple == ():
        return False
    if client_tuple[0] == -1:
        return False

    return True


# if this function returned a SocketConnection, SocketConnections close function could be used,
# witch hase some more, but maybe unneeded, error handling.
def wrap_client_socket(socket) -> ClientSocketWrap:
    client_socket_wrap = ClientSocketWrap()
    client_socket_wrap.socket_obj = socket
    return client_socket_wrap


if __name__ == "__main__":
    try:
        server = Server()
        server.start()

        while True:
            client_wrap = server.new_client()
            transmitter = Transmitter()
            signature = Service(client_wrap, transmitter)
            server.process_client(signature)
            sleep(1)  # prevents the server from taking all the cpu resources

    except KeyboardInterrupt:
        exit(0)
