"""Implementing the logic of the service"""

import SocketServer
import selector
import EstablishConnection as EstC
from socket_wrapper import ClientSocketWrap
from time import sleep


class Server:

    server_socket: EstC.ServerSocketConnection
    clients: list = []

    def __init__(self):
        self.server_socket = EstC.ServerSocketConnection()
        self.server_socket.set_host_port("", 5421)

    def serve(self):
        client_tuple: tuple = self.server_socket.socket_accept()

        if self.is_valid(client_tuple):
            self.fill_client_waiting_list(client_tuple)

        self.process_client()

    def is_valid(self, client_tuple: tuple) -> bool:
        if client_tuple == ():
            return False
        if client_tuple[0] == -1:
            return False

        return True

    def fill_client_waiting_list(self, client_tuple: tuple):
        self.clients.append(client_tuple[0])

    def process_client(self):
        client = self.get_ready_client_socket()
        self.send_back_digested_msg_and_close_connection(client)

    def get_ready_client_socket(self):
        # only checking for readability
        ready_client_socket = selector.select_client_socket(self.clients)
        wrapped_client = self.wrap_client_socket(ready_client_socket)
        return wrapped_client

    def wrap_client_socket(self, socket):
        client_socket_wrap = ClientSocketWrap()
        client_socket_wrap.socket_obj = socket
        return client_socket_wrap

    def send_back_digested_msg_and_close_connection(self, client):
        if client.is_valid():
            SocketServer.digest_client_request_and_send_back(client)
            SocketServer.close_connection_and_del_client_elem(client, self.clients)


if __name__ == "__main__":
    try:
        server = Server()
        server.server_socket.socket_create_bind_and_listen()
        server.server_socket.socket_wrap.set_blocking(False)

        while True:
            server.serve()
            sleep(1)  # prevents the server from taking all the cpu resources

    except KeyboardInterrupt:
        exit(0)
