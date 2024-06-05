from src.device.light.brightness_light import BrightnessLight
from src.utils.clamp import clamp


MAX_LIGHT_VALUE: int = 255


class RGBLight(BrightnessLight):
    __red: int = 0
    __green: int = 0
    __blue: int = 0

    @property
    def red(self) -> int:
        """
        Returns a copy of its argument, unchanged.

        Returns:
            int: an instance of the `red` class.

        """
        return self.__red

    @property
    def green(self) -> int:
        """
        Returns `self.__green`. It does not provide any further details or
        functionality beyond this simple return statement.

        Returns:
            int: a `self` instance.

        """
        return self.__green

    @property
    def blue(self) -> int:
        """
        Returns the internal variable `__blue`.

        Returns:
            int: a reference to the object of type `self`.

        """
        return self.__blue

    @red.setter
    def red(self, value: int) -> None:
        """
        Takes a value `value` and maps it to a color value within the range of
        `[0, MAX_LIGHT_VALUE]`. It then sends the resulting color value to the
        `driver` via the `send_data()` method.

        Args:
            value (int): 8-bit red value that will be clamped to the range of 0
                to MAX_LIGHT_VALUE and then sent to the LED driver through the
                `send_data()` method.

        """
        self.__red = clamp(value, 0, MAX_LIGHT_VALUE)
        self.driver.send_data(0, self.__red)

    @green.setter
    def green(self, value: int) -> None:
        """
        Clamps an input value between 0 and a maximum value (`MAX_LIGHT_VALUE`)
        and sends the resulting value to the driver via a data send request (`.send_data()`).

        Args:
            value (int): 8-bit input value that determines the green light intensity
                output by the function.

        """
        self.__green = clamp(value, 0, MAX_LIGHT_VALUE)
        self.driver.send_data(1, self.__green)

    @blue.setter
    def blue(self, value: int) -> None:
        """
        Takes an integer value `value`, clamps it to a range of 0 to `MAX_LIGHT_VALUE`,
        and sends the result as a binary signal to the `driver`.

        Args:
            value (int): 8-bit input value that will be clamped to the range of 0
                to MAX_LIGHT_VALUE before being sent through the driver module as
                output data.

        """
        self.__blue = clamp(value, 0, MAX_LIGHT_VALUE)
        self.driver.send_data(2, self.__blue)

    @property
    def color(self) -> tuple[int, int, int]:
        """
        Returns a tuple of three values representing red, green, and blue components
        of a color.

        Returns:
            tuple[int, int, int]: a tuple of three integers representing red,
            green, and blue values.

        """
        return self.__red, self.__green, self.__blue

    @color.setter
    def color(self, colors) -> None:
        """
        Sets instance variables for red, green, and blue to the values `red`,
        `green`, and `blue`, respectively.

        Args:
            colors (array.): 3 RGB colors, red, green, and blue, which are assigned
                to instance variables `self.red`, `self.green`, and `self.blue`.
                
                		- `red`: The red color property has been assigned the value `red`.
                		- `green`: The green color property has been assigned the value
                `green`.
                		- `blue`: The blue color property has been assigned the value `blue`.

        """
        red, green, blue = colors
        self.red = red
        self.green = green
        self.blue = blue

    def accept(self, visitor):
        """
        Updates the `visitor` object's `rgb_light` property by passing a reference
        to the current RGB light state as an argument.

        Args:
            visitor (RGB light.): 3D light visitor object that controls the rendering
                of the light within the scene.
                
                		- `self`: The instance of the visitor class itself, which serves
                as the context for the deserialization process.

        """
        visitor.rgb_light(self)
