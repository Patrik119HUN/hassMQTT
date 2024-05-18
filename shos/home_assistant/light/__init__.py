from shos.utils.clamp import clamp
from shos.home_assistant.device import Entity
from shos.home_assistant.light.light_factory import register_light

MAX_LIGHT_VALUE: int = 255


@register_light(light_type="binary")
class BinaryLight(Entity):
    __state: bool = False

    def __init__(self, name: str):
        """
        Initializes instance attributes with user-provided values and performs
        required actions for the Device class.

        Args:
            name (str): device's name during initialization.

        """
        Device.__init__(self, name=name)

    @property
    def state(self) -> bool:
        """
        Retrieves the internal state of the object from which it was called.

        Returns:
            bool: a copy of its internal state.

        """
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
        __value: int = 255 if self.__state is True else 0
        self.driver.send_data(0, __value)


@register_light(light_type="brightness")
class BrightnessLight(BinaryLight):
    __brightness: int = 0

    @property
    def brightness(self) -> int:
        """
        Returns the current brightness level of the system.

        Returns:
            int: a value representing the brightness level of a display, ranging
            from 0 (completely dark) to 1 (brightly lit).

        """
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


@register_light(light_type="rgb")
class RGBLight(BrightnessLight):
    __red: int = 0
    __green: int = 0
    __blue: int = 0

    @property
    def red(self) -> int:
        """
        Returns the value of the `self._red` attribute.

        Returns:
            int: a red color.

        """
        return self.__red

    @property
    def green(self) -> int:
        """
        Returns `self`.

        Returns:
            int: a green object instance.

        """
        return self.__green

    @property
    def blue(self) -> int:
        """
        Returns its own attribute value `self._blue`.

        Returns:
            int: a reference to the `blue` attribute of its owner object.

        """
        return self.__blue

    @red.setter
    def red(self, value: int) -> None:
        """
        Clamps a value between 0 and a maximum light value before sending it to
        the driver through the `send_data` method.

        Args:
            value (int): 8-bit value to be scaled and returned as the red component
                of an RGB value.

        """
        self.__red = clamp(value, 0, MAX_LIGHT_VALUE)
        self.driver.send_data(0, self.__red)

    @green.setter
    def green(self, value: int) -> None:
        """
        Clamps an input value to a range between 0 and `MAX_LIGHT_VALUE` and sends
        the result via the `driver` module.

        Args:
            value (int): 8-bit RGB value that determines the green color channel
                of the LED array, and its range is clamped to 0 to MAX_LIGHT_VALUE
                to ensure valid LED output.

        """
        self.__green = clamp(value, 0, MAX_LIGHT_VALUE)
        self.driver.send_data(1, self.__green)

    @blue.setter
    def blue(self, value: int) -> None:
        """
        Sets the blue value of an unknown device to a value within the range of 0
        to MAX_LIGHT_VALUE through the `send_data()` method of a driver object.

        Args:
            value (int): 8-bit blue component of an RGB color value to be clamped
                within the range of 0 to MAX_LIGHT_VALUE before being sent through
                the `driver.send_data()` method.

        """
        self.__blue = clamp(value, 0, MAX_LIGHT_VALUE)
        self.driver.send_data(2, self.__blue)

    @property
    def color(self) -> tuple[int, int, int]:
        """
        Returns a tuple of three integers representing red, green, and blue values
        for the given code.

        Returns:
            tuple[int, int, int]: a tuple of three values representing red, green,
            and blue components of a color.

        """
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
