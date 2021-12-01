"""Implementing the logic of the service"""

from service.I_connection import ABConnection
from service.I_clients import ABClientList
from service.I_service import ABService


class Server:
    server_socket: ABConnection
    clients: ABClientList

    def __init__(self, server_socket, clients):
        self.server_socket = server_socket
        self.server_socket.set_host_port("", 5421)
        self.clients = clients

    def start(self):
        self.server_socket.create()
        self.server_socket.set_blocking(False)

    def new_client(self):
        self.accept_new_client_and_push_to_waiting_list()
        return self.clients.get_wrapped_client_from_waiting_list()

    def accept_new_client_and_push_to_waiting_list(self):
        client_tuple: tuple = self.server_socket.socket_accept()
        if is_valid(client_tuple):
            self.clients.fill_client_waiting_list(client_tuple)

    def process_client(self, service: ABService):
        if service.is_valid() and self.clients.length() > 0:
            service.serve(self.clients)


def is_valid(client_tuple: tuple) -> bool:
    if client_tuple == ():
        return False
    if client_tuple[0] == -1:
        return False

    return True

