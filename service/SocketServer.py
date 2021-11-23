"""The module which implements the communication protocol"""

import cryptic
import select
import socket
import ExceptionHandling as Exc
from EstablishConnection import socket_close
from sending import send_bytes_to_socket
from sending import receive_bytes_from_socket
from sending import close_bytes

# TODO: separate select functions from


def select_client_socket(client_sockets: dict, mode: str = "rd"):
    """Head function for select() call, handling the case, that
    no exception was raised nor a value was returned"""
    try:
        return _select_client_socket(client_sockets, mode)
    except Exc.SelectException as se:
        Exc.print_exception_str(se)


def _select_client_socket(client_sockets: dict, mode: str) -> socket:
    """Handling select() exceptions"""
    try:
        readable_socket = _try_to_select_socket_and_pop_it(client_sockets, mode)
        return readable_socket
    except RuntimeError as RE:
        Exc.print_exception_str(RE)
    except AttributeError as AE:
        Exc.handle_exception_and_exit(AE, 4200)
    except ValueError as VE:
        Exc.print_exception_str(VE)
        Exc.print_error_code(500)
    except Exception as e:
        Exc.handle_exception_and_exit(e, 4201)
    # if we get here, something must be very wrong
    raise Exc.SelectException


def _try_to_select_socket_and_pop_it(cl_soc: dict, mode) -> socket:
    """Taking last client in the list"""
    selected_sockets: list = _select_read_or_write(cl_soc, mode)
    if len(selected_sockets) > 0:
        return selected_sockets.pop()


def _select_read_or_write(socs: dict, rd_wr: str) -> list:
    """Call of select() method. If mode is changed to 'wr',
    select looks for writable file descriptors"""
    if rd_wr == "rd":
        client_sockets_rd = select.select(socs["sockets"], [], [], 0)
        return client_sockets_rd[0]
    elif rd_wr == "wr":
        client_sockets_wr = select.select([], socs["sockets"], [], 0)
        return client_sockets_wr[1]


def digest_client_request_and_send_back(ready_client: socket):
    """receive some data, digest it and send it back"""
    client_request: bytes = receive_bytes_from_socket(ready_client)
    if client_request != b"":
        _send_digested(ready_client, client_request)


def _send_digested(soc: socket, msg: bytes):
    """first sending the message then sending the closing bytes"""
    send_bytes_to_socket(soc, cryptic.digest(msg))
    send_bytes_to_socket(soc, close_bytes)


def close_connection_and_del_client_elem(soc: socket, client_list: dict):
    """Closes socket connection and removes the socket from the ready clients list"""
    try:
        _del_client_elem(soc, client_list)
        if soc is not None:
            socket_close(soc)
    except Exception as e:
        Exc.handle_exception_and_exit(e, 700)


def _del_client_elem(soc: socket, client_list: dict):
    """Catching exceptions of the _del_all_info function"""
    try:
        _del_all_client_info(soc, client_list)
    except IndexError as ie:
        Exc.handle_exception_and_exit(ie, 6000)
    except ValueError as ve:
        Exc.handle_exception_and_exit(ve, 6001)


def _del_all_client_info(soc: socket, client_list: dict):
    """Calls the pop() method to delete elements in the lists of the client dict."""
    list_index = client_list["sockets"].index(soc)
    client_list["sockets"].pop(list_index)
    client_list["addresses"].pop(list_index)
