from enum import Enum, auto
from core.device.binary_sensor import BinarySensor


class ZoneType(Enum):
    BinarySensor = auto()
    MotionSensor = auto()


class Zone:
    __sensor: BinarySensor = None
    __zone_type: ZoneType = None

    def __init__(self, zone_type: ZoneType):
        self.__zone_type = zone_type

    def add_sensor(self, sensor: BinarySensor):
        self.__sensor = sensor

    @property
    def state(self):
        return self.__sensor.state

    @property
    def zone_type(self):
        return self.__zone_type
