from shos.utils.clamp import clamp
from shos.home_assistant.device import Entity
from shos.home_assistant.light.light_factory import register_light

MAX_LIGHT_VALUE: int = 255


@register_light(light_type="binary")
class BinaryLight(Entity):
    __state: bool = False

    def __init__(self, name: str):
        Device.__init__(self, name=name)

    @property
    def state(self) -> bool:
        return self.__state

    @state.setter
    def state(self, state: bool) -> None:
        """
        Sets the value of a driver's output to either 255 or 0 based on the state
        of the function.

        Args:
            state (bool): boolean state of an output signal, which is used to
                determine the value of the output data when the function is called.

        """
        self.__state = state
        __value: int = 255 if self.__state is True else 0
        self.driver.send_data(0, __value)


@register_light(light_type="brightness")
class BrightnessLight(BinaryLight):
    __brightness: int = 0

    @property
    def brightness(self) -> int:
        return self.__brightness

    @brightness.setter
    def brightness(self, brightness: int) -> None:
        """
        Sets the brightness level of a light device based on an input value within
        a predetermined range, and sends the updated brightness value to the
        device's driver via a communication channel.

        Args:
            brightness (int): 0-based brightness value that determines the level
                of light emission produced by the lamp, with a maximum value of `MAX_LIGHT_VALUE`.

        """
        self.__brightness = clamp(brightness, 0, MAX_LIGHT_VALUE)
        self.driver.send_data(1, self.__brightness)
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
        Sets `self.red`, `self.green`, and `self.blue` to the specified values,
        assigning them as properties of the function object.

        Args:
            colors (`array`.): 3 primary colors: red, green, and blue, which are
                assigned to instance variables `self.red`, `self.green`, and
                `self.blue`, respectively.
                
                		- `red`: A property with the value of red, which is a primary color.
                		- `green`: A property with the value of green, which is also a
                primary color.
                		- `blue`: A property with the value of blue, which is another
                primary color.

        """
        red, green, blue = colors
        self.red = red
        self.green = green
        self.blue = blue