from config_manager import ConfigManager
from mqtt.mqtt_manager import MQTTManager


def main():
    Manager = MQTTManager()
    Manager.subscribe("asd")
    


if __name__ == "__main__":
    main()
