from abc import ABC, abstractmethod


class LightDriver(ABC):
    @abstractmethod
    def connect(self, *args, **kwargs):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def send_data(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_data(self):
        pass


class ModbusDriver(LightDriver):
    def connect(self, *args, **kwargs):
        pass

    def disconnect(self):
        pass

    def send_data(self, *args, **kwargs):
        pass

    def get_data(self):
        pass
