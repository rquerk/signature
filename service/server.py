"""Implementing the logic of the service"""

from I_service import ABService
from I_connection import ABConnection

import lib.selector as selector
from lib.socket_wrapper import SocketWrap


class Server:
    server_socket: ABConnection
    clients: list = []

    def __init__(self, server_socket):
        self.server_socket = server_socket
        self.server_socket.set_host_port("", 5421)

    def start(self):
        self.server_socket.create()
        self.server_socket.set_blocking(False)

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
def wrap_client_socket(socket) -> SocketWrap:
    client_socket_wrap = SocketWrap()
    client_socket_wrap.socket_obj = socket
    return client_socket_wrap

