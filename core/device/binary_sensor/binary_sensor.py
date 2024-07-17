from core.device.entity import Entity
from gpiozero import DigitalInputDevice
from core.device.hardware import Hardware
from core.device.driver.gpio_driver import GPIODriver, PinType
from typing import Callable


class BinarySensor(Entity):
    __state: bool = False

    def __init__(
        self,
        name: str,
        hardware: Hardware = None,
        icon: str = None,
        unique_id: str = None,
        entity_type: str = "binary_sensor",
    ):
        Entity.__init__(
            self,
            name=name,
            unique_id=unique_id,
            hardware=hardware,
            entity_type=entity_type,
            icon=icon,
        )

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
