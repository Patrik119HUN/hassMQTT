from abc import ABC, abstractmethod
from core.device.hardware import Hardware
from class_registry import ClassRegistry

device_builder = ClassRegistry()


class DeviceBuilder(ABC):
    @abstractmethod
    def get(self, unique_id: str, name: str, hardware: Hardware, icon: str,**kwargs):
        raise NotImplementedError
