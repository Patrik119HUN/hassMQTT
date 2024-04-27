from json import JSONEncoder

from shos.home_assistant.light import BinaryLight, BrightnessLight, RGBLight


class BinaryEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BinaryLight):
            return {
                "color_mode": "binary",
                "state": "ON" if obj.state is True else "OFF",
            }
        return JSONEncoder.default(self, obj)


class BrightnessEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BrightnessLight):
            return {
                "brightness": obj.brightness,
                "color_mode": "brightness",
                "state": "ON" if obj.state is True else "OFF",
            }
        return JSONEncoder.default(self, obj)


class RGBEncoder(JSONEncoder):
    def default(self, obj):
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
