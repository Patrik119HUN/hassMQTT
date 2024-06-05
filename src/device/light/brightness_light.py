from src.device.light.binary_light import BinaryLight
from src.utils.clamp import clamp


MAX_LIGHT_VALUE: int = 255


class BrightnessLight(BinaryLight):
    __brightness: int = 0

    @property
    def brightness(self) -> int:
        """
        Returns the object's brightness level based on the `value` parameter
        provided in the function call.

        Returns:
            int: a floating-point value representing the brightness of the screen,
            ranging from 0.0 to 1.0.

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
        Sets the brightness of a light according to the visitor's input.

        Args:
            visitor (int): brightness level of the lighting environment that the
                code is operating within.

        """
        visitor.brightness_light(self)
