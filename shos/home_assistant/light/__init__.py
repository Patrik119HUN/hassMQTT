from ..device import EntityInfo, DeviceTypes, Device
from shos.utils.clamp import clamp
from driver import LightDriver
from json_encoders import *

MAX_LIGHT_VALUE: int = 255


class Light(EntityInfo):
    __driver: LightDriver

    def __init__(self, name: str):
        self.component = DeviceTypes.LIGHT
        self.device = Device(name=name)
        self.name = name
        self.unique_id = EntityInfo.generate_id()
        pass

    @property
    def driver(self):
        return self.__driver

    @driver.setter
    def driver(self, driver: LightDriver):
        self.__driver = driver


__lights: dict[str, Light] = {}


def register_light(light_type: str):
    def decorator(fn):
        __lights[light_type] = fn
        return fn

    return decorator


@register_light(light_type="binary")
class BinaryLight(Light):
    __state: bool = False

    @property
    def state(self) -> bool:
        return self.__state

    @state.setter
    def state(self, state: bool) -> None:
        self.__state = state


@register_light(light_type="brightness")
class BrightnessLight(BinaryLight):
    __brightness: int = 0

    @property
    def brightness(self) -> int:
        return self.__brightness

    @brightness.setter
    def brightness(self, brightness: int) -> None:
        self.__brightness = clamp(brightness, 0, MAX_LIGHT_VALUE)
        self.state = True if self.__brightness != 0 else False


@register_light(light_type="rgb")
class RGBLight(BrightnessLight):
    __red: int = 0
    __green: int = 0
    __blue: int = 0

    @property
    def red(self) -> int:
        return self.__red

    @property
    def green(self) -> int:
        return self.__green

    @property
    def blue(self) -> int:
        return self.__blue

    @red.setter
    def red(self, value: int) -> None:
        self.__red = value

    @green.setter
    def green(self, value: int) -> None:
        self.__green = value

    @blue.setter
    def blue(self, value: int) -> None:
        self.__blue = value

    @property
    def color(self) -> tuple[int, int, int]:
        return self.__red, self.__green, self.__blue

    @color.setter
    def color(self, colors) -> None:
        red, green, blue = colors
        self.__red = clamp(red, 0, MAX_LIGHT_VALUE)
        self.__green = clamp(green, 0, MAX_LIGHT_VALUE)
        self.__blue = clamp(blue, 0, MAX_LIGHT_VALUE)

    @staticmethod
    def get_encoder():
        return RGBEncoder


def get_light(light_type: str):
    if light_type not in __lights:
        raise RuntimeError("No such a light type")
    return __lights[light_type]
