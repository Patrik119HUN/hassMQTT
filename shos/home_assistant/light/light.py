from shos.home_assistant.device import EntityInfo, DeviceTypes, Device, generate_id
from shos.home_assistant.light.driver import LightDriver


class Light(EntityInfo):
    __driver: LightDriver

    def __init__(self, name: str):
        self.component = DeviceTypes.LIGHT
        self.device = Device(name=name)
        self.name = name
        self.unique_id = generate_id()
        pass

    @property
    def driver(self):
        return self.__driver

    @driver.setter
    def driver(self, driver_instance: LightDriver):
        self.__driver = driver_instance
        print(f"driver set to {driver_instance}")
