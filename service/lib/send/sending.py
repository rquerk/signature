"""This is a helper module for sending and receiving bytes over sockets"""

from service.lib.I_sending import ABTransmitter
from service.lib.exceptions.exception_handling import print_exception_str
from service.lib.socket_wrapper import SocketWrap


class Transmitter(ABTransmitter):

    client: SocketWrap

    buffer_size: int = 512
    message_length: int = 1024

    def set_client(self, client):
        self.client = client

    def send_bytes_to_socket(self, msg: bytes) -> int:
        """Utilizing send() in a while loop: send(msg[bytes_send:]).
        Also catching BrokenPipeError.
        """
        bytes_send = 0
        while bytes_send < len(msg):
            try:
                bytes_send += self.client.send(msg[bytes_send:])
            except BrokenPipeError as bpe:
                print_exception_str(bpe)
            if not bytes_send:
                break
        return bytes_send

    def receive_bytes_from_socket(self) -> bytes:
        """Calling recv() in a while loop using a bytearray to append
        the received buffer to a result value witch can be returned.
        """
        bytes_received = 0
        request: bytearray = bytearray(b"")
        while bytes_received < self.message_length:
            client_data: bytes = self.client.receive(self.buffer_size)
            if not client_data or client_data == b"":
                return b""  # or break?
            bytes_received += len(client_data)
            request.extend(client_data)
            if self.received_closing_bytes(client_data):
                request = request[:-len(self.close_bytes)]
                break
        return bytes(request)

    def received_closing_bytes(self, received_bytes: bytes) -> bool:
        if received_bytes[-len(self.close_bytes):] == self.close_bytes:
            return True

    def is_valid(self):
        if self.client is not None:
            return self.client.is_valid()
