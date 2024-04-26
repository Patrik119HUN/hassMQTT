from light import Light
from dataclasses import dataclass


class BinaryLight(Light):
    __state: bool = False

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state: bool):
        self.__state = state


class WhiteLight(BinaryLight):
    __brightness: int = 0

    @property
    def brightness(self):
        return self.__brightness

    @brightness.setter
    def state(self, brightness: int):
        self.__brightness = brightness


class RGBLight(WhiteLight):
    __red: int = 0
    __green: int = 0
    __blue: int = 0

    @property
    def red(self):
        return self.__red

    @property
    def green(self):
        return self.__green

    @property
    def blue(self):
        return self.__blue

    @red.setter
    def red(self, value: int):
        self.__red = value

    @green.setter
    def red(self, value: int):
        self.__green = value

    @blue.setter
    def red(self, value: int):
        self.__blue = value

    @property
    def color(self):
        return [self.__red, self.__green, self.__blue]

    @color.setter
    def color(self, red: int, green: int, blue: int):
        self.__red = red
        self.__green = green
        self.__blue = blue
