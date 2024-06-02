from abc import ABC, abstractmethod


class DeviceDAOInterface(ABC):

    @abstractmethod
    def get_device_by_id(self, unique_id: str):
        pass

    @abstractmethod
    def get_all_devices(self):
        pass

    @abstractmethod
    def add_device(
        self, unique_id: str, name: str, hardware_type: str, device_type: str
    ):
        pass

    @abstractmethod
    def update_device(self, device):
        pass

    @abstractmethod
    def delete_device(self, unique_id: str):
        pass
