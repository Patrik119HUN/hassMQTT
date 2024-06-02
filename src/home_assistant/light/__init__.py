from src.utils.clamp import clamp
from src.home_assistant.device import Entity, Hardware
from src.home_assistant.light.light_factory import register_light

MAX_LIGHT_VALUE: int = 255


@register_light(light_type="binary")
class BinaryLight(Entity):
    __state: bool = False

    def __init__(
        self,
        name: str,
        device: Hardware = None,
        device_class: str = None,
        icon: str = None,
        unique_id: str = None,
    ):
        Entity.__init__(self, name, device, device_class, icon, unique_id)

    @property
    def state(self) -> bool:
        return self.__state

    @state.setter
    def state(self, state: bool) -> None:
        """
        Updates the value of an int variable based on a logical expression and
        sends it to a driver via a send_data call.

        Args:
            state (bool): binary value to be sent through the `driver.send_data()`
                method.

        """
        self.__state = state
        self.driver.send_data(0, state)

    def accept(self, visitor):
        visitor.binary_light(self)


@register_light(light_type="brightness")
class BrightnessLight(BinaryLight):
    __brightness: int = 0

    @property
    def brightness(self) -> int:
        return self.__brightness

    @brightness.setter
    def brightness(self, brightness: int) -> None:
        """
        Clamps the input `brightness` value to a range between 0 and `MAX_LIGHT_VALUE`,
        then sends the clamped value to the `driver` module using the `send_data()`
        method. The function also sets the state of the light to `True` if the
        clamped value is non-zero, or `False` otherwise.

        Args:
            brightness (int): 0-100% dimming level of the LED strip, which is
                clamped to the range [0, MAX_LIGHT_VALUE] and then sent as an
                argument to the `send_data` method of the `driver` object.

        """
        self.__brightness = clamp(brightness, 0, MAX_LIGHT_VALUE)
        self.driver.send_data(1, self.__brightness)
        self.state = True if self.__brightness != 0 else False

    def accept(self, visitor):
        visitor.brightness_light(self)


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
        """
        Sets attributes for a object, `self`, to assign values for `red`, `green`,
        and `blue` colors respectively.

        Args:
            colors (enumeration (or 'tag').): 3 RGB colors that will be used to
                define the color of the component.

                                - `red`: The `red` property has the value `'red'`.
                                - `green`: The `green` property has the value `'green'`.
                                - `blue`: The `blue` property has the value `'blue'`.

        """
        red, green, blue = colors
        self.red = red
        self.green = green
        self.blue = blue

    def accept(self, visitor):
        visitor.rgb_light(self)
