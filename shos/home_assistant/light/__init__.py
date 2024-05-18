from shos.utils.clamp import clamp
from shos.home_assistant.device import Entity, Hardware
from shos.home_assistant.light.light_factory import register_light

MAX_LIGHT_VALUE: int = 255


@register_light(light_type="binary")
class BinaryLight(Entity):
    __state: bool = False

    def __init__( self, name: str, device: Hardware = None, device_class: str = None, icon: str = None, ):
        """
        Initializes a `Entity` object by taking in `name`, `device`, `device_class`,
        and `icon` parameters and setting the respective attributes accordingly.

        Args:
            name (str): name of the entity being initialized, which is used to
                create the appropriate file or directory path for storing configuration
                and state information.
            device (None): 3rd party library that will be used to interact with
                the hardware device.
            device_class (None): class of the device being created, which determines
                the display icon and label shown in the entity list.
            icon (None): 2D image file that will be used to display the entity in
                its interface, such as a logo or icon, during the initialization
                of the `Entity` class.

        """
        Entity.__init__(self, name, device, device_class, icon)

    @property
    def state(self) -> bool:
        """
        Returns the internal state of its receiver, providing direct access to its
        implementation-specific data structure.

        Returns:
            bool: the current state of the system.

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
        self.driver.send_data(0, state)


@register_light(light_type="brightness")
class BrightnessLight(BinaryLight):
    __brightness: int = 0

    @property
    def brightness(self) -> int:
        """
        Returns the current brightness level of the device.

        Returns:
            int: a value representing the brightness level of a display device.

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
        Returns the `self__red` attribute value.

        Returns:
            int: a reference to the same `red` object.

        """
        return self.__red

    @property
    def green(self) -> int:
        """
        Returns its own object reference.

        Returns:
            int: a string representation of the color "Green".

        """
        return self.__green

    @property
    def blue(self) -> int:
        """
        Returns a reference to the same object that it was called on, maintaining
        its state and behavior.

        Returns:
            int: a reference to its own `self` attribute.

        """
        return self.__blue

    @red.setter
    def red(self, value: int) -> None:
        """
        Takes a value and clamps it between 0 and `MAX_LIGHT_VALUE`, then sends
        the clamped value to the `driver` module as data.

        Args:
            value (int): 0-100% range of red light intensity that is clamped to
                the maximum value of `MAX_LIGHT_VALUE` for output through the
                `driver.send_data()` method.

        """
        self.__red = clamp(value, 0, MAX_LIGHT_VALUE)
        self.driver.send_data(0, self.__red)

    @green.setter
    def green(self, value: int) -> None:
        """
        Clamps an input value between 0 and `MAX_LIGHT_VALUE`, then sends it to a
        driver as output data.

        Args:
            value (int): 0-based index of the green color component to be sent as
                a voltage value through the driver module.

        """
        self.__green = clamp(value, 0, MAX_LIGHT_VALUE)
        self.driver.send_data(1, self.__green)

    @blue.setter
    def blue(self, value: int) -> None:
        """
        Sets the value of `self.__blue` to the input value `value`, clamped to the
        range [0, MAX_LIGHT_VALUE]. The clamped value is then sent to the driver
        through the `send_data()` method.

        Args:
            value (int): 8-bit RGB value to be lightened or darkened within the
                specified range of 0 to MAX_LIGHT_VALUE.

        """
        self.__blue = clamp(value, 0, MAX_LIGHT_VALUE)
        self.driver.send_data(2, self.__blue)

    @property
    def color(self) -> tuple[int, int, int]:
        """
        Returns the red, green, and blue values of a given color in hexadecimal format.

        Returns:
            tuple[int, int, int]: a tuple of three colors: red, green, and blue.

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
