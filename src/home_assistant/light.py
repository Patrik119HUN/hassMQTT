from device import EntityInfo, Device, DeviceTypes
from dataclasses import dataclass
from enum import Enum

MAX_LIGHT_VALUE: int = 255


class Light(EntityInfo):
    @dataclass
    class Color:
        red: int
        green: int
        blue: int
        white: int
        warm_white: int

    class Type(Enum):
        BINARY = "binary"
        RGB = "rgb"
        RGBW = "rgbw"
        RGBWW = "rgbww"
        WHITE = "white"

        def __str__(self) -> str:
            return str(self.value)

    _type: Type
    _state: bool
    _brightness: int
    _color: Color = None

    def __init__(self, name: str, light_type: Type):
        self.component = DeviceTypes.LIGHT
        self.device = Device(name=name)
        self._type = light_type
        self.name = name
        self.unique_id = EntityInfo.generate_id()
        self._color = Light.Color(0, 0, 0, 0, 0)
        self._brightness = 0
        self._state = False
        pass

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def set_brightness(self, brightness: int) -> None:
        if self._type == Light.Type.BINARY:
            return
        if brightness <= 0:
            self._brightness = 0
            self._state = False
            return
        if brightness > MAX_LIGHT_VALUE:
            self._brightness = MAX_LIGHT_VALUE
        else:
            self._brightness = brightness
        self._state = True

    @property
    def state(self):
        return self._state

    @state.setter
    def set_state(self, state: bool):
        self._state = state

    @property
    def color(self):
        return self._color

    @color.setter
    def set_color(
        self, red: int, green: int, blue: int, white: int, warm_white: int
    ) -> None:
        self._color.red = red
        self._color.green = green
        self._color.blue = blue
        self._color.white = white
        self._color.warm_white = warm_white
