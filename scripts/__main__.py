from src.device_manager import device_manager
from src.mqtt import mqtt_manager
from src.home_assistant.mqtt_adapter import get_discovery
from src.home_assistant.mqtt_adapter.binary_light_observer import *


def main():
    for device in device_manager.list():
        topic, discovery_packet = get_discovery(device)
        mqtt_manager.publish(topic, discovery_packet.model_dump_json(indent=2, exclude_none=True))
        mqtt_manager.add_subscriber(
            discovery_packet.command_topic,
            BinaryObserver(mqtt_manager, discovery_packet, device),
        )
        if hasattr(discovery_packet, "brightness_command_topic"):
            mqtt_manager.add_subscriber(
                discovery_packet.brightness_command_topic,
                BrightnessObserver(mqtt_manager, discovery_packet, device),
            )
        if hasattr(discovery_packet, "rgb_command_topic"):
            mqtt_manager.add_subscriber(
                discovery_packet.rgb_command_topic,
                RGBObserver(mqtt_manager, discovery_packet, device),
            )

    mqtt_manager.loop()


if __name__ == "__main__":
    main()
