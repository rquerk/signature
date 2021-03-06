"""Module to handle the select call"""

import select
import lib.exceptions.exception_handling as exc


def select_client_socket(client_sockets, mode: str = "rd"):
    """Head function for select() call, handling the case, that
    no exception was raised nor a value was returned"""
    try:
        return _select_client_socket(client_sockets, mode)
    except exc.SelectException as se:
        exc.print_exception_str(se)


def _select_client_socket(client_sockets, mode: str):
    """Handling select() exceptions"""
    try:
        readable_socket = _try_to_select_socket_and_pop_it(client_sockets, mode)
        return readable_socket
    except RuntimeError as RE:
        exc.print_exception_str(RE)
    except AttributeError as AE:
        exc.handle_exception_and_exit(AE, 4200)
    except ValueError as VE:
        exc.print_exception_str(VE)
    except Exception as e:
        exc.handle_exception_and_exit(e, 4201)
    # if we get here, something must be very wrong
    raise exc.SelectException


def _try_to_select_socket_and_pop_it(cl_soc, mode: str):
    """Taking last client in the list"""
    selected_sockets: list = _select_read_or_write(cl_soc, mode)
    if len(selected_sockets) > 0:
        return selected_sockets.pop()


def _select_read_or_write(socs: list, rd_wr: str) -> list:
    """Call of select() method. If mode is changed to 'wr',
    select looks for writable file descriptors"""
    if rd_wr == "rd":
        client_sockets_rd = select.select(socs, [], [], 0)
        return client_sockets_rd[0]
    elif rd_wr == "wr":
        client_sockets_wr = select.select([], socs, [], 0)
        return client_sockets_wr[1]
