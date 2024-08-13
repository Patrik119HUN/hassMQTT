from core.device.light.binary_light import BinaryLight
from core.device.entity import Entity
from core.utils.clamp import clamp
from attrs import define

MAX_LIGHT_VALUE: int = 255


@define
class RGBLight(Entity):
    entity_type: str = "light"
    color_mode: str = "rgb"

    __red: int = 255
    __green: int = 255
    __blue: int = 255
    __brightness: float = 1
    __state: bool = False

    @property
    def brightness(self) -> int:
        return self.__brightness

    @brightness.setter
    def brightness(self, brightness: int) -> None:
        self.__brightness = clamp(brightness, 0, MAX_LIGHT_VALUE) / 255
        self.state = True if brightness != 0 else False

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state: bool) -> None:
        if state:
            self.color = (self.__red, self.__green, self.__blue)
        else:
            for x in range(3):
                self.driver.send_data(x, 0)
        self.__state = state

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
        self.__red = clamp(value, 0, MAX_LIGHT_VALUE)
        self.driver.send_data(0, int(self.__red * self.__brightness))

    @green.setter
    def green(self, value: int) -> None:
        self.__green = clamp(value, 0, MAX_LIGHT_VALUE)
        self.driver.send_data(1, int(self.__green * self.__brightness))

    @blue.setter
    def blue(self, value: int) -> None:
        self.__blue = clamp(value, 0, MAX_LIGHT_VALUE)
        self.driver.send_data(2, int(self.__blue * self.__brightness))

    @property
    def color(self) -> tuple[int, int, int]:
        return self.__red, self.__green, self.__blue

    @color.setter
    def color(self, colors) -> None:
        red, green, blue = colors
        self.red = red
        self.green = green
        self.blue = blue
