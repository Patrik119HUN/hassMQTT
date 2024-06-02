from src.home_assistant.mqtt_packet.discovery.base_packet import MQTTDiscoveryPacket
from src.mqtt.topic_builder import Topic


class BinaryLightMQTTDiscoveryPacket(MQTTDiscoveryPacket):
    payload_on: str = "ON"
    payload_off: str = "OFF"


class BrightnessLightMQTTDiscoveryPacket(BinaryLightMQTTDiscoveryPacket):
    brightness_command_topic: Topic
    brightness_state_topic: Topic


class RGBLightMQTTDiscoveryPacket(BrightnessLightMQTTDiscoveryPacket):
    rgb_command_topic: Topic
    rgb_state_topic: Topic
