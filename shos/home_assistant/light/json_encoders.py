from json import JSONEncoder

from shos.home_assistant.light import BinaryLight, BrightnessLight, RGBLight


class BinaryEncoder(JSONEncoder):
    def default(self, obj):
        """
        Takes an instance of `BinaryLight` as input and returns a dictionary with
        information about the light's state.

        Args:
            obj (`BinaryLight`.): BinaryLight object to be converted into a
                dictionary for output.
                
                	1/ `color_mode`: This property indicates that the object is in
                binary mode.
                	2/ `state`: This property represents the state of the object,
                which is either "ON" if the object's state is True or "OFF" otherwise.

        Returns:
            instance of JSONEncoder with the specified object as its argument: a
            dictionary with keys `"color_mode"` and `"state"`, where each key has
            a value of "binary" or "ON" or "OFF", depending on the `BinaryLight`
            instance's state.
            
            		- "color_mode": This property represents the light mode of the
            BinaryLight object, which is set to "binary" in this case.
            		- "state": This property indicates whether the light is on or off,
            based on the `state` attribute of the BinaryLight object. If the `state`
            attribute is True, the light is on, and if it's False, the light is off.

        """
        if isinstance(obj, BinaryLight):
            return {
                "color_mode": "binary",
                "state": "ON" if obj.state is True else "OFF",
            }
        return JSONEncoder.default(self, obj)


class BrightnessEncoder(JSONEncoder):
    def default(self, obj):
        """
        Takes an object `obj`, checks its type using `isinstance()`, and if it is
        a `BrightnessLight`, returns a dictionary with the `brightness`, `color_mode`,
        and `state` attributes, respectively. If the object is not a `BrightnessLight`,
        the function defaults to the `JSONEncoder.default` method.

        Args:
            obj (`BrightnessLight`.): object for which the code generates documentation.
                
                		- `brightness`: A attribute representing the brightness value
                of the `BrightnessLight` object.
                		- `color_mode`: An attribute that denotes the color mode of the
                light, which can be either "brightness" or any other mode specific
                to the `BrightnessLight` class.
                		- `state`: An attribute that indicates whether the light is
                turned on (`ON`) or off (`OFF`).

        Returns:
            object with attributes `brightness`, `color_mode`, and `state: a
            dictionary containing `brightness`, `color_mode`, and `state` attributes,
            based on the given `obj`.
            
            		- "brightness": The brightness level of the light, represented as
            an integer between 0 and 100.
            		- "color_mode": A string indicating the color mode of the light,
            with possible values of "brightness". This attribute indicates that
            the light's color is adjusted based on its brightness level.
            		- "state": A boolean value representing whether the light is turned
            ON or OFF.

        """
        if isinstance(obj, BrightnessLight):
            return {
                "brightness": obj.brightness,
                "color_mode": "brightness",
                "state": "ON" if obj.state is True else "OFF",
            }
        return JSONEncoder.default(self, obj)


class RGBEncoder(JSONEncoder):
    def default(self, obj):
        """
        Generates a dictionary with properties related to an object of type
        `RGBLight`. It returns the object's brightness, color mode, red, green and
        blue values as well as its state, which is "ON" if the object is on or
        "OFF" otherwise.

        Args:
            obj (`RGBLight` object.): object to be encoded into a JSON format.
                
                		- `brightness`: The brightness level of the RGB light, represented
                as a value between 0 and 100.
                		- `color_mode`: The color mode of the RGB light, with "rgb"
                indicating that it is an RGB light.
                		- `color`: An object representing the red, green, and blue values
                of the light, each represented as a value between 0 and 255.
                		- `state`: The state of the RGB light, either "ON" if the light
                is turned on or "OFF" otherwise.

        Returns:
            dict: a dictionary representing the object's state and color properties.

        """
        if isinstance(obj, RGBLight):
            return {
                "brightness": obj.brightness,
                "color_mode": "rgb",
                "color": {
                    "r": obj.red,
                    "g": obj.green,
                    "b": obj.blue,
                },
                "state": "ON" if obj.state is True else "OFF",
            }
        return JSONEncoder.default(self, obj)
