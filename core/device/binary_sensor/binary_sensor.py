from core.device.entity import Entity
from gpiozero import DigitalInputDevice


class BinarySensor(Entity):
    __input = DigitalInputDevice(4,True)
    __state:bool = False

    @property
    def state(self):
        return self.__input.is_active

    @state.setter
    def state(self, value: bool):
        self.__state = value
