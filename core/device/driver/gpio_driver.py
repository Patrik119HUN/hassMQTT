from core.device.driver.abstract_driver import AbstractDriver
from enum import Enum, auto
from gpiozero import DigitalInputDevice, DigitalOutputDevice
from typing import Dict, Callable


class PinType(Enum):
    INPUT = auto()
    OUTPUT = auto()


class GPIODriver(AbstractDriver):
    __gpios: Dict[int, DigitalInputDevice | DigitalOutputDevice] = {}

    def __init__(self) -> None:
        super().__init__()

    def connect(self, *args, **kwargs):
        pin: int = kwargs["pin"]
        pin_type: PinType = kwargs["type"]
        if pin_type == PinType.INPUT:
            self.__gpios[pin] = DigitalInputDevice(pin=pin, pull_up=True)
        if pin_type == PinType.OUTPUT:
            self.__gpios[pin] = DigitalOutputDevice(pin=pin)

    def add_active_callback(self, pin: int, callback: Callable[[None], None]):
        self.__gpios[pin].when_activated = callback

    def add_deactivated_callback(self, pin: int, callback: Callable[[None], None]):
        self.__gpios[pin].when_deactivated = callback

    def disconnect(self):
        pass

    def send_data(self, address: int, value: int | bool):
        if value:
            self.__gpios[address].on()
        else:
            self.__gpios[address].off()

    def get_data(self, address: int):
        return self.__gpios[address].is_active
