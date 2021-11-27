"""The module which implements the communication protocol/functionality"""

from exception_handling import handle_exception_and_exit
import sending
import cryptic


class Service:

    def __init__(self, client):
        self.transmit = sending.Transmitter()
        self.transmit.set_client(client)

    def digest_client_request_and_send_back(self):
        """receive some data, digest it and send it back"""
        client_request: bytes = self.transmit.receive_bytes_from_socket()
        if client_request != b"":
            self._send_digested(client_request)

    def _send_digested(self, msg: bytes):
        """first sending the message then sending the closing bytes"""
        self.transmit.send_bytes_to_socket(cryptic.digest(msg))
        self.transmit.send_bytes_to_socket(self.transmit.close_bytes)

    def close_connection_and_del_client_elem(self, client_list):
        """Closes socket connection and removes the socket from the ready clients list"""
        try:
            self._del_client_elem(client_list)
            if self.transmit.client is not None:
                self.transmit.client.close()
        except Exception as e:
            handle_exception_and_exit(e, 700)

    def _del_client_elem(self, client_list):
        """Calls the pop() method to delete the element in the lists of the clients"""
        try:
            list_index = client_list.index(self.transmit.client.socket_obj)
            client_list.pop(list_index)
        except IndexError as ie:
            handle_exception_and_exit(ie, 6000)
        except ValueError as ve:
            handle_exception_and_exit(ve, 6001)
