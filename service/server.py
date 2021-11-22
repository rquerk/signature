"""Implementing the logic of the service"""

import SocketServer as Soc
import EstablishConnection as EstC

clients_dict = dict


def serve(clients_iterable):
    client_tuple: tuple = EstC.socket_accept(server_socket)

    if is_valid(client_tuple):
        fill_client_waiting_list(client_tuple, clients_dict)

    process_client()

    if client_tuple in clients_iterable:
        EstC.socket_close(client_tuple[0])


def is_valid(client_tuple: tuple) -> bool:
    if client_tuple == ():
        return False
    if client_tuple[0] == -1:
        return False

    return True


def fill_client_waiting_list(client_tuple: tuple, client_connections: dict):
    client_connections["sockets"].append(client_tuple[0])
    client_connections["addresses"].append(client_tuple[1])


def process_client():
    ready_client_socket = get_ready_client_socket()
    send_back_digested_msg_and_close_connection(ready_client_socket)
        

def get_ready_client_socket():
    # only checking for readability
    ready_client_socket = Soc.select_client_socket(clients_dict)

    return ready_client_socket


def send_back_digested_msg_and_close_connection(client_socket):
    if socket_is_valid(client_socket):
        Soc.digest_client_request_and_send_back(client_socket)
        Soc.close_connection_and_del_client_elem(client_socket, clients_dict)


def socket_is_valid(client_socket):
    if client_socket != -1 and client_socket is not None:
        return True


if __name__ == "__main__":
    try:
        server_socket = EstC.socket_create_bind_and_listen()
        server_socket.setblocking(False)

        clients_dict = {"sockets": [], "addresses": []}

        while True:
            serve(clients_dict)

    except KeyboardInterrupt:
        exit(0)
