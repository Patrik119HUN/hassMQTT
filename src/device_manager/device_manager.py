from src.home_assistant.binary_sensor import BinarySensor
from src.home_assistant.light.driver import ModbusDriver
from src.home_assistant.light.light_factory import get_light
from pymodbus.client.base import ModbusBaseSyncClient
from loguru import logger
from src.home_assistant.device import Entity
from src.modbus_controller import modbus_controller
from src.device_manager.device_dao_interface import DeviceDAOInterface


class DeviceManager:
    __modbus_manager: ModbusBaseSyncClient = None
    __device_list: list[Entity] = []
    __device_dao: DeviceDAOInterface = None

    def __init__(
        self,
        modbus_driver=modbus_controller.instance,
        device_dao: DeviceDAOInterface = None,
    ):
        self.__modbus_manager = modbus_driver
        self.__device_dao = device_dao

    def create_device(
        self, unique_id: str, name: str, hardware_type: str, device_type: str, **kwargs
    ) -> Entity:
        dev = DeviceManager.device_factory(device_type, name, unique_id, **kwargs)
        driver = self.driver_factory(hardware_type, address=kwargs["device_id"])

        dev.driver = driver
        return dev

    @staticmethod
    def device_factory(device_type: str, name: str, unique_id: str, **kwargs) -> Entity:
        created_dev = None
        match device_type:
            case "light":
                created_dev = get_light(kwargs["color_mode"])(name, unique_id=unique_id)
            case "binary_sensor":
                created_dev = BinarySensor(name)
            case "alarm":
                raise NotImplemented("Alarm not implemented yet")
        logger.debug(f"created an {created_dev.__class__.__name__}")
        return created_dev

    def driver_factory(self, hardware_type: str, address: int):
        created_driver = None
        match hardware_type:
            case "modbus":
                created_driver = ModbusDriver(self.__modbus_manager)
                created_driver.connect(id=address)
            case "can":
                raise NotImplemented("CAN driver implemented yet")
            case "hat":
                raise NotImplemented("Built in driver implemented yet")
        return created_driver
