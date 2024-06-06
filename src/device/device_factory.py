from pymodbus.client.base import ModbusBaseSyncClient
from src.home_assistant.driver.modbus_driver import ModbusDriver
from src.device.light import BinaryLight, BrightnessLight, RGBLight
from src.device.binary_sensor import BinarySensor
from src.device.entity import Entity
from src.device.hardware import Hardware
from loguru import logger
from src.repository import EntityRepository, LightRepository, DeviceDriverRepository
from src.config_manager import config_manager


class DeviceFactory:
    __light_registry = {
        "binary": BinaryLight,
        "brightness": BrightnessLight,
        "rgb": RGBLight,
    }
    __sensor_registry = {
        "binary": BinarySensor,
    }
    __light_repository: LightRepository = None
    __entity_repository: EntityRepository = None
    __device_driver_repository: DeviceDriverRepository = None
    __modbus_manager: ModbusBaseSyncClient = None

    def __init__(self, modbus_driver):
        self.__light_repository = LightRepository(config_manager["database"])
        self.__entity_repository = EntityRepository(config_manager["database"])
        self.__device_driver_repository = DeviceDriverRepository(config_manager["database"])
        self.__modbus_manager = modbus_driver

    def get_device(
        self,
        device_type: str,
        name: str,
        unique_id: str,
        hardware: Hardware,
        icon: str,
        **kwargs,
    ) -> Entity:
        created_dev = None
        match device_type:
            case "light":
                params = self.__light_repository.get(unique_id)
                created_dev = DeviceFactory.get_light(
                    light_type=params["color_mode"],
                    name=name,
                    unique_id=unique_id,
                    hardware=hardware,
                    icon=icon,
                )
            case "binary_sensor":
                created_dev = DeviceFactory.get_sensor(kwargs["device_class"], **kwargs)
            case "alarm":
                raise NotImplemented("Alarm not implemented yet")
        logger.debug(f"created an {created_dev.__class__.__name__}")
        params = self.__device_driver_repository.get(unique_id)
        driver = self.driver_factory(params["driver"], params["address"])

        created_dev.driver = driver
        return created_dev

    @classmethod
    def get_light(
        cls, light_type: str, name: str, unique_id: str, hardware: Hardware, icon: str
    ) -> Entity:
        if light_type not in DeviceFactory.__light_registry:
            raise RuntimeError("No such a light type")
        return DeviceFactory.__light_registry[light_type](
            name=name, unique_id=unique_id, hardware=hardware, icon=icon
        )

    @classmethod
    def get_sensor(cls, sensor_type: str, *args, **kwargs) -> Entity:
        if sensor_type not in DeviceFactory.__sensor_registry:
            raise RuntimeError("No such a sensor type")
        return DeviceFactory.__sensor_registry[sensor_type](*args, **kwargs)

    def driver_factory(self, driver: str, address: int):
        created_driver = None
        match driver:
            case "modbus":
                created_driver = ModbusDriver(self.__modbus_manager)
                created_driver.connect(id=address)
            case "can":
                raise NotImplemented("CAN driver implemented yet")
            case "hat":
                raise NotImplemented("Built in driver implemented yet")
        return created_driver
