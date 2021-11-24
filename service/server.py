"""Implementing the logic of the service"""

import SocketServer
import selector
import EstablishConnection as EstC
from socket_wrapper import ClientSocketWrap
from time import sleep

clients: list = []


def serve():
    client_tuple: tuple = EstC.socket_accept(server_socket)

    if is_valid(client_tuple):
        fill_client_waiting_list(client_tuple)

    process_client()


def is_valid(client_tuple: tuple) -> bool:
    if client_tuple == ():
        return False
    if client_tuple[0] == -1:
        return False

    return True


def fill_client_waiting_list(client_tuple: tuple):
    clients.append(client_tuple[0])


def process_client():
    ready_client_socket = get_ready_client_socket()
    send_back_digested_msg_and_close_connection(ready_client_socket)
        

def get_ready_client_socket():
    # only checking for readability
    ready_client_socket = selector.select_client_socket(clients)
    wrapped_client = wrap_client_socket(ready_client_socket)
    return wrapped_client


def wrap_client_socket(socket):
    client = ClientSocketWrap()
    client.socket_obj = socket
    return client


def send_back_digested_msg_and_close_connection(client):
    if client.is_valid():
        SocketServer.digest_client_request_and_send_back(client)
        SocketServer.close_connection_and_del_client_elem(client, clients)


if __name__ == "__main__":
    try:
        server_socket = EstC.socket_create_bind_and_listen()
        server_socket.set_blocking(False)

        while True:
            serve()
            sleep(1)  # prevents the server from taking all the cpu resources

    except KeyboardInterrupt:
        exit(0)
