from shos.mqtt.mqtt_manager import MQTTManager
from shos.modbus import get_modbus
from shos.home_assistant import device
from shos.home_assistant import light
import json


def SimpleEncoder(obj):
    return obj.__dict__


def main():
    Manager = MQTTManager()
    Modbus = get_modbus()
    Manager.subscribe("asd")
    asztali = light.Light("Asztali lampa", light.Light.Type.RGBWW)
    asztali.state = False
    # asztali.set_color(255, 255, 123, 12, 222)
    valami = json.dumps(asztali, cls=light.LightEncoder, indent=4)
    # print(valami)


if __name__ == "__main__":
    main()
