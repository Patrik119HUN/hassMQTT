from src.home_assistant.driver.modbus_driver import ModbusDriver
from src.device.device_factory import DeviceFactory
from pymodbus.client.base import ModbusBaseSyncClient
from src.device.entity import Entity
from src.modbus_controller import modbus_controller
from src.repository import EntityRepository, HardwareRepository


class DeviceManager:
    __modbus_manager: ModbusBaseSyncClient = None
    __device_list: list[Entity] = []
    __device_dao: DeviceDAOInterface = None
    __device_factory: DeviceFactory

    def __init__(
        self,
        modbus_driver=modbus_controller.instance,
        device_dao: DeviceDAOInterface = None,
    ):
        self.__modbus_manager = modbus_driver
        self.__device_dao = device_dao
        self.__device_factory = DeviceFactory()

    def create_device(
        self, unique_id: str, name: str, hardware_type: str, device_type: str, **kwargs
    ) -> Entity:
        dev = self.__device_factory.get_device(device_type, name, unique_id, **kwargs)
        driver = self.driver_factory(hardware_type, address=kwargs["device_id"])

        dev.driver = driver
        return dev

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
