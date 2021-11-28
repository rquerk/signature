
import service.lib.selector as selector
from service.lib.socket_wrapper import SocketWrap

from service.I_clients import ABClientList


class ClientList(ABClientList):

    def __init__(self):
        self.clients: list = []

    def fill_client_waiting_list(self, client_tuple: tuple):
        self.clients.append(client_tuple[0])

    def get_wrapped_client_from_waiting_list(self):
        ready_client_socket = selector.select_client_socket(self.clients)
        if ready_client_socket is not None:
            wrapped_client = wrap_client_socket(ready_client_socket)
            return wrapped_client

    def length(self):
        return len(self.clients)


# if this function returned a SocketConnection, SocketConnections close function could be used,
# witch hase some more, but maybe unneeded, error handling.
def wrap_client_socket(socket) -> SocketWrap:
    client_socket_wrap = SocketWrap()
    client_socket_wrap.socket_obj = socket
    return client_socket_wrap
