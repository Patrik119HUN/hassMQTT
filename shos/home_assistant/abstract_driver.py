from abc import ABC, abstractmethod


class AbstractDriver(ABC):
    @abstractmethod
    def connect(self, *args, **kwargs):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def send_data(self, address: int, value: int | bool):
        pass

    @abstractmethod
    def get_data(self):
        pass
