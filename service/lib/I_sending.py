from abc import ABCMeta, abstractmethod


class ABTransmitter(metaclass=ABCMeta):

    close_bytes: bytes = b"\r\n"
    client = None

    @abstractmethod
    def send_bytes_to_socket(self, msg):
        pass

    @abstractmethod
    def receive_bytes_from_socket(self):
        pass

    @abstractmethod
    def set_client(self, client):
        pass

    @abstractmethod
    def is_valid(self):
        pass
