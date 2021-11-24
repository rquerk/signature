"""The module which implements the communication protocol"""

import exception_handling as exc
from socket_wrapper import SocketWrap

from sending import receive_bytes_from_socket
from sending import send_bytes_to_socket
from sending import close_bytes
import cryptic


def digest_client_request_and_send_back(ready_client: SocketWrap):
    """receive some data, digest it and send it back"""
    client_request: bytes = receive_bytes_from_socket(ready_client)
    if client_request != b"":
        _send_digested(ready_client, client_request)


def _send_digested(soc: SocketWrap, msg: bytes):
    """first sending the message then sending the closing bytes"""
    send_bytes_to_socket(soc, cryptic.digest(msg))
    send_bytes_to_socket(soc, close_bytes)


def close_connection_and_del_client_elem(soc: SocketWrap, client_list):
    """Closes socket connection and removes the socket from the ready clients list"""
    try:
        _del_client_elem(soc, client_list)
        if soc is not None:
            soc.close()
    except Exception as e:
        exc.handle_exception_and_exit(e, 700)


def _del_client_elem(soc: SocketWrap, client_list):
    """Catching exceptions of the _del_all_info function"""
    try:
        _del_all_client_info(soc, client_list)
    except IndexError as ie:
        exc.handle_exception_and_exit(ie, 6000)
    except ValueError as ve:
        exc.handle_exception_and_exit(ve, 6001)


def _del_all_client_info(soc: SocketWrap, client_list):
    """Calls the pop() method to delete elements in the lists of the client dict."""
    list_index = client_list.index(soc.socket_obj)
    client_list.pop(list_index)



