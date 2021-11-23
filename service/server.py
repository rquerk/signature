"""Implementing the logic of the service"""

import SocketServer as Soc
import EstablishConnection as EstC
from socket_wrapper import ClientSocketWrap
clients_dict = dict


def serve(clients_iterable):
    client_tuple: tuple = EstC.socket_accept(server_socket)

    if is_valid(client_tuple):
        fill_client_waiting_list(client_tuple)

    process_client()

    if client_tuple in clients_iterable:
        EstC.socket_close(client_tuple[0])


def is_valid(client_tuple: tuple) -> bool:
    if client_tuple == ():
        return False
    if client_tuple[0] == -1:
        return False

    return True


def fill_client_waiting_list(client_tuple: tuple):
    clients_dict["sockets"].append(client_tuple[0])
    clients_dict["addresses"].append(client_tuple[1])


def process_client():
    ready_client_socket = get_ready_client_socket()
    send_back_digested_msg_and_close_connection(ready_client_socket)
        

def get_ready_client_socket():
    # only checking for readability
    ready_client_socket = Soc.select_client_socket(clients_dict)
    wrapped_client = wrap_client_socket(ready_client_socket)
    return wrapped_client


def wrap_client_socket(socket):
    client = ClientSocketWrap()
    client.socket_obj = socket
    return client


def send_back_digested_msg_and_close_connection(client):
    if client.is_valid():
        Soc.digest_client_request_and_send_back(client)
        Soc.close_connection_and_del_client_elem(client, clients_dict)


if __name__ == "__main__":
    try:
        server_socket = EstC.socket_create_bind_and_listen()
        server_socket.set_blocking(False)

        clients_dict = {"sockets": [], "addresses": []}

        while True:
            serve(clients_dict)

    except KeyboardInterrupt:
        exit(0)
