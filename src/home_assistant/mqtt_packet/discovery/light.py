from src.home_assistant.mqtt_packet.discovery.base_packet import MQTTDiscoveryPacket


class BinaryLightMQTTDiscoveryPacket(MQTTDiscoveryPacket):
    payload_on: str = "ON"
    payload_off: str = "OFF"


class BrightnessLightMQTTDiscoveryPacket(BinaryLightMQTTDiscoveryPacket):
    brightness_command_topic: str
    brightness_state_topic: str


class RGBLightMQTTDiscoveryPacket(BrightnessLightMQTTDiscoveryPacket):
    rgb_command_topic: str
    rgb_state_topic: str
