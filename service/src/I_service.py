from abc import ABCMeta, abstractmethod


class ABService(metaclass=ABCMeta):

    @abstractmethod
    def serve(self, clients):
        pass

    @abstractmethod
    def is_valid(self):
        pass
