"""The module which implements the communication protocol/functionality"""

import exception_handling as exc
from socket_wrapper import SocketWrap

from sending import receive_bytes_from_socket
from sending import send_bytes_to_socket
from sending import close_bytes
import cryptic


class Service:

    client: SocketWrap

    def __init__(self, client):
        self.client = client

    def digest_client_request_and_send_back(self):
        """receive some data, digest it and send it back"""
        client_request: bytes = receive_bytes_from_socket(self.client)
        if client_request != b"":
            self._send_digested(client_request)

    def _send_digested(self, msg: bytes):
        """first sending the message then sending the closing bytes"""
        send_bytes_to_socket(self.client, cryptic.digest(msg))
        send_bytes_to_socket(self.client, close_bytes)

    def close_connection_and_del_client_elem(self, client_list):
        """Closes socket connection and removes the socket from the ready clients list"""
        try:
            self._del_client_elem(client_list)
            if self.client is not None:
                self.client.close()
        except Exception as e:
            exc.handle_exception_and_exit(e, 700)

    def _del_client_elem(self, client_list):
        """Calls the pop() method to delete the element in the lists of the clients"""
        try:
            list_index = client_list.index(self.client.socket_obj)
            client_list.pop(list_index)
        except IndexError as ie:
            exc.handle_exception_and_exit(ie, 6000)
        except ValueError as ve:
            exc.handle_exception_and_exit(ve, 6001)
