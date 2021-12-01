from abc import ABCMeta, abstractmethod


class ABConnection(metaclass=ABCMeta):

    @abstractmethod
    def set_host_port(self, host, port):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def set_blocking(self, boolean):
        pass

    @abstractmethod
    def socket_accept(self):
        pass

    @abstractmethod
    def close(self):
        pass
