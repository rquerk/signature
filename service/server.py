"""Implementing the logic of the service"""

import service
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

    def serve(self):
        self.accept_new_client_and_push_to_waiting_list()
        client = self.get_ready_client_from_waiting_list()
        self.process_client(client)

    def accept_new_client_and_push_to_waiting_list(self):
        client_tuple: tuple = self.server_socket.socket_accept()
        if is_valid(client_tuple):
            self.fill_client_waiting_list(client_tuple)

    def fill_client_waiting_list(self, client_tuple: tuple):
        self.clients.append(client_tuple[0])

    def get_ready_client_from_waiting_list(self):
        # only checking for readability
        ready_client_socket = selector.select_client_socket(self.clients)
        wrapped_client = wrap_client_socket(ready_client_socket)
        return wrapped_client

    def process_client(self, client):
        if client.is_valid():
            s = service.Service(client)
            s.digest_client_request_and_send_back()
            s.close_connection_and_del_client_elem(self.clients)


def is_valid(client_tuple: tuple) -> bool:
    if client_tuple == ():
        return False
    if client_tuple[0] == -1:
        return False

    return True


def wrap_client_socket(socket) -> ClientSocketWrap:
    client_socket_wrap = ClientSocketWrap()
    client_socket_wrap.socket_obj = socket
    return client_socket_wrap


if __name__ == "__main__":
    try:
        server = Server()
        server.start()

        while True:
            server.serve()
            sleep(1)  # prevents the server from taking all the cpu resources

    except KeyboardInterrupt:
        exit(0)
