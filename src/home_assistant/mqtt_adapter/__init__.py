from src.device.entity import Entity
from dataclasses import dataclass
from src.mqtt.topic_builder import Topic, TopicType
from src.device.light import BinaryLight
from src.device.binary_sensor import BinarySensor
from src.home_assistant.mqtt_packet.discovery.visitor import MQTTVisitor
from src.home_assistant.mqtt_packet.discovery.base_packet import MQTTDiscoveryPacket
from typing import Tuple

DISCOVERY_TOPIC = "homeassistant"


def get_discovery(entity: Entity) -> Tuple[Topic, MQTTDiscoveryPacket]:
    class_to_str = {BinaryLight: "light", BinarySensor: "sensor"}
    device_type: str = ""
    visitor = MQTTVisitor()

    for x, y in class_to_str.items():
        if isinstance(entity, x):
            device_type = y

    entity.accept(visitor)
    topic = (
        Topic(TopicType.PUBLISHER)
        .add(DISCOVERY_TOPIC)
        .add(device_type)
        .add(entity.unique_id)
        .add("config")
    )
    return topic, visitor.get()
