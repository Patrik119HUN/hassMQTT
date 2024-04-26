from shos.home_assistant.device import EntityInfo, Device, DeviceTypes
from dataclasses import dataclass
from enum import Enum
import json
from shos.utils.clamp import clamp

MAX_LIGHT_VALUE: int = 255


class Light(EntityInfo):
    class Type(Enum):
        BINARY = "binary"
        RGB = "rgb"
        RGBW = "rgbw"
        RGBWW = "rgbww"
        WHITE = "white"

        def __str__(self) -> str:
            return str(self.value)

    _type: Type

    def __init__(self, name: str, light_type: Type):
        self.component = DeviceTypes.LIGHT
        self.device = Device(name=name)
        self._type = light_type
        self.name = name
        self.unique_id = EntityInfo.generate_id()
        pass

    @property
    def type(self):
        return self._type



class LightEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Light):
            return {
                "brightness": obj.brightness,
                "color_mode": str(obj.type),
                "color": {
                    "r": obj.color.red,
                    "g": obj.color.green,
                    "b": obj.color.blue,
                    "w": obj.color.white,
                },
                "state": "ON" if obj.state is True else "OFF",
            }
        return json.JSONEncoder.default(self, obj)
