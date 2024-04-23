from shos.mqtt.mqtt_manager import MQTTManager
from shos.modbus import get_modbus
from shos.home_assistant import device


def main():
    Manager = MQTTManager()
    Modbus = get_modbus()
    Manager.subscribe("asd")


if __name__ == "__main__":
    main()
