from src.device.entity import Entity
from src.device.hardware import Hardware
from loguru import logger
from src.device.driver_factory import DriverFactory
from src.device.device_builder import device_builder


class DeviceFactory:
    __driver_factory: DriverFactory = None

    def __init__(self):
        logger.trace("DeviceFactory initialized")
        self.__driver_factory = DriverFactory()

    def get_device(
        self, device_type: str, name: str, unique_id: str, hardware: Hardware, icon: str
    ) -> Entity:
        created_dev = None
        for builder_type, builder in device_builder.items():
            if builder_type == device_type:
                created_dev = builder().get(unique_id, name, hardware, icon)
        logger.debug(f"created an {created_dev.__class__.__name__}")

        created_dev.driver = self.__driver_factory.get(unique_id)
        return created_dev
