from core.mqtt import mqtt_manager
from core.home_assistant.mqtt_adapter import get_discovery
from core.home_assistant.mqtt_adapter.binary_light_observer import *
from core.mqtt.topic_builder import Topic, TopicType
from core.device_manager import device_manager


def main():
    for device in device_manager.list():
        topic, discovery_packet = get_discovery(device)
        # mqtt_manager.publish(topic, json.dumps(discovery_packet, indent=2))
        mqtt_manager.add_subscriber(
            Topic.from_str(TopicType.SUBSCRIBER, discovery_packet["command_topic"]),
            BinaryObserver(mqtt_manager, discovery_packet, device),
        )
        mqtt_manager.add_subscriber(
            Topic.from_str(TopicType.SUBSCRIBER, discovery_packet["command_topic"]),
            AlarmObserver(mqtt_manager, discovery_packet, device),
        )
        if "brightness_command_topic" in discovery_packet:
            mqtt_manager.add_subscriber(
                Topic.from_str(TopicType.SUBSCRIBER, discovery_packet["brightness_command_topic"]),
                BrightnessObserver(mqtt_manager, discovery_packet, device),
            )
        if "rgb_command_topic" in discovery_packet:
            mqtt_manager.add_subscriber(
                Topic.from_str(TopicType.SUBSCRIBER, discovery_packet["rgb_command_topic"]),
                RGBObserver(mqtt_manager, discovery_packet, device),
            )

    mqtt_manager.loop()


if __name__ == "__main__":
    main()
