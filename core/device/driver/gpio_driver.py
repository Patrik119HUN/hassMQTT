from core.device.driver.abstract_driver import AbstractDriver
from enum import Enum, auto
from gpiozero import DigitalInputDevice, DigitalOutputDevice
from typing import Dict, Callable
from loguru import logger


class PinType(Enum):
    INPUT = auto()
    OUTPUT = auto()


class GPIODriver(AbstractDriver):
    _instance = None

    def __init__(self) -> None:
        super().__init__()
        self.__gpios: Dict[int, DigitalInputDevice | DigitalOutputDevice] = {}

    def __new__(cls) -> None:
        if cls._instance is None:
            cls._instance = super(GPIODriver, cls).__new__(cls)
        return cls._instance

    def __del__(self) -> None:
        for devices in self.__gpios.values():
            devices.close()

    def connect(self, *args, **kwargs):
        pin: int = kwargs["pin"]
        pin_type: PinType = kwargs["type"]
        if pin in self.__gpios:
            logger.info(f"{pin} is already created")
            return
        if pin_type == PinType.INPUT:
            self.__gpios[pin] = DigitalInputDevice(pin=pin, pull_up=True)
        if pin_type == PinType.OUTPUT:
            self.__gpios[pin] = DigitalOutputDevice(pin=pin)

    def add_active_callback(self, pin: int, callback: Callable[[None], None]):
        if pin in self.__gpios:
            self.__gpios[pin].when_activated = callback
        else:
            logger.error("No such a pin")

    def add_deactivated_callback(self, pin: int, callback: Callable[[None], None]):
        if pin in self.__gpios:
            self.__gpios[pin].when_deactivated = callback
        else:
            logger.error("No such a pin")

    def disconnect(self):
        pass

    def send_data(self, address: int, value: int | bool):
        if value:
            self.__gpios[address].on()
        else:
            self.__gpios[address].off()

    def get_data(self, address: int):
        return self.__gpios[address].is_active

    def __repr__(self) -> str:
        return "gpio"
