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
        """
        Initializes an `Entity` object with its name, device, device class, icon,
        and unique ID.

        Args:
            name (str): name of the entity being created, which is a string value
                used to identify the entity in the code and its associated data.
            device (None): device associated with the Entity, which is then saved
                in the `device_class` attribute of the Entity instance.
            device_class (None): class of the device being initialized, which is
                used to determine the appropriate visual representation and behavior
                in the user interface.
            icon (None): 16x16 pixel image to be used as the device's icon.
            unique_id (None): 16-bit Universally Unique Identifier (UUID) of the
                entity, which serves as a distinct identifier for the entity within
                its class and across different systems and platforms.

        """
        Entity.__init__(self, name, device, device_class, icon, unique_id)

    @property
    def state(self) -> bool:
        """
        Returns the current state object of the program.

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

    def accept(self, visitor):
        """
        Transforms binary light into a different type of light based on a given rule.

        Args:
            visitor (binary light value.): binary light data that is being processed
                by the function.
                
                		- `self`: A reference to the visitor instance itself.

        """
        visitor.binary_light(self)


@register_light(light_type="brightness")
class BrightnessLight(BinaryLight):
    __brightness: int = 0

    @property
    def brightness(self) -> int:
        """
        Returns the brightness level of a given light based on its energy consumption,
        which is represented by the variable `__brightness`.

        Returns:
            int: a value representing the brightness of the display.

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

    def accept(self, visitor):
        """
        Sets the brightness level of the device's display based on user input.

        Args:
            visitor (instance of class `Visitor`.): Brightness Light widget that
                is being updated by the function.
                
                	The `brightness_light` property is a float value that represents
                the brightness level of the light in percent. It can range from 0
                to 100, where 0 indicates complete darkness and 100 indicates
                maximum brightness.

        """
        visitor.brightness_light(self)


@register_light(light_type="rgb")
class RGBLight(BrightnessLight):
    __red: int = 0
    __green: int = 0
    __blue: int = 0

    @property
    def red(self) -> int:
        """
        Returns a reference to the current instance of its class.

        Returns:
            int: an instance of the `Red` class.

        """
        return self.__red

    @property
    def green(self) -> int:
        """
        Returns its own internal value.

        Returns:
            int: the value `self.green`.

        """
        return self.__green

    @property
    def blue(self) -> int:
        """
        Returns a reference to its own object.

        Returns:
            int: a blue color value.

        """
        return self.__blue

    @red.setter
    def red(self, value: int) -> None:
        """
        Clamps the input value to a range of 0 to `MAX_LIGHT_VALUE` and sends the
        result to the driver through the `send_data()` method.

        Args:
            value (int): 0-based red value of an LED to be adjusted.

        """
        self.__red = clamp(value, 0, MAX_LIGHT_VALUE)
        self.driver.send_data(0, self.__red)

    @green.setter
    def green(self, value: int) -> None:
        """
        Calculates and sends a value within a given range to a driver module using
        the `clamp()` function to limit the value to a specified range.

        Args:
            value (int): 8-bit analog value that is converted into a 0 to
                MAX_LIGHT_VALUE range.

        """
        self.__green = clamp(value, 0, MAX_LIGHT_VALUE)
        self.driver.send_data(1, self.__green)

    @blue.setter
    def blue(self, value: int) -> None:
        """
        Takes a value between 0 and `MAX_LIGHT_VALUE`, calculates its clamped
        value, and sends it to the `driver` via `send_data`.

        Args:
            value (int): 8-bit RGB value to be lightened or darkened within the
                range of 0 to MAX_LIGHT_VALUE.

        """
        self.__blue = clamp(value, 0, MAX_LIGHT_VALUE)
        self.driver.send_data(2, self.__blue)

    @property
    def color(self) -> tuple[int, int, int]:
        """
        Returns  the   values  of its private attributes `__red`, `__green`, and
        `__blue`.

        Returns:
            tuple[int, int, int]: a tuple of three values representing red, green,
            and blue colors.

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

    def accept(self, visitor):
        """
        Modifies the `visitor.RGB` object by assigning its current value to the
        `light` attribute.

        Args:
            visitor (`rgb_light` object.): 3D light source used to simulate the
                lighting of the scene.
                
                		- `self`: A reference to the `Visitor` object itself.

        """
        visitor.rgb_light(self)
