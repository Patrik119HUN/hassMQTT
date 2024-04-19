from config_manager import ConfigManager
from mqtt.mqtt_manager import MQTTManager
from modbus import ModbusManager


def main():
    Manager = MQTTManager()
    Modbus = ModbusManager()
    Manager.subscribe("asd")
    


if __name__ == "__main__":
    main()
