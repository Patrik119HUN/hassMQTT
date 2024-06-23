from loguru import logger
from .abstract_driver import AbstractDriver
from gpiozero import DigitalInputDevice, DigitalOutputDevice


class GPIODriver(AbstractDriver):
    def __init__(self):
        pass

    def connect(self, *args, **kwargs):
        pass

    def disconnect(self):
        pass

    def send_data(self, address: int, value: bool):
        output = DigitalOutputDevice(pin=address)
        output.value = value

    def get_data(self, address: int):
        return DigitalInputDevice(pin=address, pull_up=True, active_state=True).is_active
