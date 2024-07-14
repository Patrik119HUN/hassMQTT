from core.device.light.brightness_light import BrightnessLight
from core.device.entity import Entity
from core.device.hardware import Hardware
from core.utils.clamp import clamp
from core.utils.id_generator import generate_id

MAX_LIGHT_VALUE: int = 255


class RGBLight(BrightnessLight):
    color_mode: str = "rgb"
    __red: int = 0
    __green: int = 0
    __blue: int = 0

    def __init__(
        self,
        name: str,
        unique_id: str = generate_id(),
        hardware: Hardware = None,
        icon: str = None,
        entity_type: str = "light",
    ):
        Entity.__init__(
            self,
            name=name,
            unique_id=unique_id,
            hardware=hardware,
            icon=icon,
            entity_type=entity_type,
        )

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
        self.driver.send_data(0, self.__red)

    @green.setter
    def green(self, value: int) -> None:
        self.__green = clamp(value, 0, MAX_LIGHT_VALUE)
        self.driver.send_data(1, self.__green)

    @blue.setter
    def blue(self, value: int) -> None:
        self.__blue = clamp(value, 0, MAX_LIGHT_VALUE)
        self.driver.send_data(2, self.__blue)

    @property
    def color(self) -> tuple[int, int, int]:
        return self.__red, self.__green, self.__blue

    @color.setter
    def color(self, colors) -> None:
        red, green, blue = colors
        self.red = red
        self.green = green
        self.blue = blue
