from light import Light
from dataclasses import dataclass
from enum import Enum


class RGBLight(Light):
    @dataclass
    class _Color:
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
    _state: bool = False
    _brightness: int = 0
    _color_temp: int = 0
    _color: _Color = _Color(0, 0, 0, 0, 0)

    def __init__(self, name: str, light_type: Type):
        self.component = DeviceTypes.LIGHT
        self.device = Device(name=name)
        self._type = light_type
        self.name = name
        self.unique_id = EntityInfo.generate_id()
        pass

    @property
    def type(self):
        return self._type

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def set_brightness(self, brightness: int) -> None:
        if self._type == Light.Type.BINARY:
            return
        self._brightness = clamp(brightness, 0, MAX_LIGHT_VALUE)
        self._state = True if self._brightness != 0 else False
        return

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state: bool):
        self._state = state

    @property
    def color(self):
        return self._color

    @color.setter
    def set_color(
        self, red: int, green: int, blue: int, white: int, warm_white: int
    ) -> None:
        self._color.red = clamp(red, 0, MAX_LIGHT_VALUE)
        self._color.green = clamp(green, 0, MAX_LIGHT_VALUE)
        self._color.blue = clamp(blue, 0, MAX_LIGHT_VALUE)
        self._color.white = clamp(white, 0, MAX_LIGHT_VALUE)
        self._color.warm_white = clamp(warm_white, 0, MAX_LIGHT_VALUE)
