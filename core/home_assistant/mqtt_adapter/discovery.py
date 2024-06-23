from core.device.entity import Entity
from core.mqtt.topic_builder import Topic, TopicType
from core.device.light import BinaryLight
from core.device.binary_sensor import BinarySensor
from core.device.alarm_control_panel import AlarmControlPanel
from core.home_assistant.mqtt_packet.discovery import (
    DiscoveryCompositeVisitor,
    RGBVisitor,
    BrightnessVisitor,
    BinaryVisitor,
    AlarmVisitor,
)
from typing import Tuple, Dict

DISCOVERY_TOPIC = "homeassistant"

discovery_visitor = (
    DiscoveryCompositeVisitor()
    .add_visitor(RGBVisitor())
    .add_visitor(BrightnessVisitor())
    .add_visitor(AlarmVisitor())
    .add_visitor(BinaryVisitor())
)


def get_discovery(entity: Entity) -> Tuple[Topic, Dict[str, str]]:
    class_to_str = {
        BinaryLight: "light",
        BinarySensor: "sensor",
        AlarmControlPanel: "alarm_control_panel",
    }
    device_type: str = ""

    for x, y in class_to_str.items():
        if isinstance(entity, x):
            device_type = y

    discovery_visitor.visit(entity)
    topic = (
        Topic(TopicType.PUBLISHER)
        .add(DISCOVERY_TOPIC)
        .add(device_type)
        .add(entity.unique_id)
        .add("config")
    )
    return topic, discovery_visitor.get()
