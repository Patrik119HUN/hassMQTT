from core.device.entity import Entity
from core.device.hardware import Hardware
from loguru import logger
from core.device.driver.driver_factory import DriverFactory
from core.device.light import LightBuilder
from core.device.alarm_control_panel import AlarmBuilder

device_builder = {"light": LightBuilder, "alarm": AlarmBuilder}


class DeviceFactory:
    def __init__(self):
        logger.trace("DeviceFactory initialized")
        self.__driver_factory = DriverFactory()

    def get_device(
        self, device_type: str, name: str, unique_id: str, hardware: Hardware, icon: str, **kwargs
    ) -> Entity:
        created_dev = None
        for builder_type, builder in device_builder.items():
            if builder_type == device_type:
                created_dev = builder().get(unique_id, name, hardware, icon, **kwargs)
        logger.debug(f"created an {created_dev.__class__.__name__}")
        created_dev.driver = self.__driver_factory.get(unique_id, **kwargs)
        return created_dev
