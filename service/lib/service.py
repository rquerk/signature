"""The module which implements the communication protocol/functionality"""

from src.I_service import ABService
from lib.I_sending import ABTransmitter
from lib.exceptions.exception_handling import handle_exception_and_exit
import lib.sign.cryptic as cryptic
import os


class Service(ABService):

    transmit: ABTransmitter = None

    def __init__(self, client, transmitter):
        if client is not None:
            self.transmit = transmitter
            self.transmit.set_client(client)

    def serve(self, clients):
        self.sign_client_request_and_send_back()
        self.close_connection_and_del_client_elem(clients)

    def sign_client_request_and_send_back(self):
        """receive some data, sign it and send it back"""
        client_request: bytes = self.transmit.receive_bytes_from_socket()
        if client_request != b"":
            self.do_and_send_signature(client_request)

    def do_and_send_signature(self, msg: bytes):
        key = os.environ['PRIVATE_KEY']
        private_key_file = fr"{key}"
        pri = cryptic.read_key_from_file(private_key_file)
        signature = cryptic.sign(msg, pri)
        self.transmit.send_bytes_to_socket(signature)
        self.transmit.send_bytes_to_socket(self.transmit.close_bytes)

    # feels like this should be in SocketConnection Class
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
            list_index = client_list.clients.index(self.transmit.client.socket_obj)
            client_list.clients.pop(list_index)
        except IndexError as ie:
            handle_exception_and_exit(ie, 6000)
        except ValueError as ve:
            handle_exception_and_exit(ve, 6001)

    def is_valid(self):
        if self.transmit is not None:
            return self.transmit.is_valid()
