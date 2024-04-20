from mqtt.mqtt_manager import MQTTManager
from modbus import ModbusManager
from home_assistant import device


def main():
    Manager = MQTTManager()
    Modbus = ModbusManager()
    Manager.subscribe("asd")
    print(device.generate_id())


if __name__ == "__main__":
    main()
