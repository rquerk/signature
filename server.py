"""The module which implements the communication protocol"""

import SocketServer as Soc
import EstablishConnection as EstC

clients_dict = dict


def socket_is_valid(client_socket):
    if client_socket != -1 and client_socket is not None:
        return True


def send_back_digested_msg_and_close_connection(ready_client_socket) -> int:
    if socket_is_valid(ready_client_socket):
        Soc.digest_client_request_and_send_back(ready_client_socket)
        Soc.close_connection_and_del_client_elem(ready_client_socket, clients_dict)
        
        return 0
    else:
        # no client ready after select
        return 1

# only checks readability
def get_ready_client_socket(client_tuple: tuple):
    Soc.fill_client_waiting_list(client_tuple, clients_dict)
    # only checking for readability
    ready_client_socket = Soc.select_client_socket(clients_dict)
    
    return ready_client_socket
        

def tuple_is_valid_client_tuple(client_tuple: tuple) -> bool:
    if client_tuple == ():
        return False
    if client_tuple[0] == -1:
        return False
    
    return True


def check_client_validity_and_then_process_it(client_tuple: tuple):
    if tuple_is_valid_client_tuple(client_tuple):
        ready_client_socket = get_ready_client_socket(client_tuple)
        send_back_digested_msg_and_close_connection(ready_client_socket)


def handle_client(clients_dict: dict):
    """accepts a client, waits for data, digests that data
    and responds to the client with the digest.
    Then it closes the client connection again"""
    client_tuple: tuple = EstC.socket_accept(server_socket)
    check_client_validity_and_then_process_it(client_tuple)

    if client_tuple in clients_dict:
        EstC.socket_close(client_tuple[0])


if __name__ == "__main__":
    try:
        server_socket = EstC.socket_create_bind_and_listen()
        server_socket.setblocking(False)

        clients_dict = Soc.clients

        while True:
            handle_client(clients_dict)

        EstC.socket_close(server_socket)
    except KeyboardInterrupt:
        exit(0)
