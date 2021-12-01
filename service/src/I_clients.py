from abc import ABCMeta, abstractmethod


class ABClientList(metaclass=ABCMeta):

    @abstractmethod
    def fill_client_waiting_list(self, client):
        pass

    @abstractmethod
    def get_wrapped_client_from_waiting_list(self):
        pass

    @abstractmethod
    def length(self):
        pass
