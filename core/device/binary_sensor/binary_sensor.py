from core.device.entity import Entity
from gpiozero import DigitalInputDevice
from core.device.hardware import Hardware
from core.device.driver.gpio_driver import GPIODriver, PinType
from typing import Callable, ClassVar
from attrs import define


@define
class BinarySensor(Entity):
    entity_type: str = ("binary_sensor",)
    __state: bool = False

    def set_callback(
        self, active: Callable[[None], None], deactivated: Callable[[None], None]
    ):
        self.driver.add_active_callback(pin=4, callback=active)
        self.driver.add_deactivated_callback(pin=4, callback=deactivated)

    @property
    def state(self):
        return self.driver.get_data(4)

    @state.setter
    def state(self, value: bool):
        self.__state = value
