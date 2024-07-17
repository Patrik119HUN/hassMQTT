from core.device.entity import Entity
from core.mqtt.topic_builder import Topic, TopicType
from typing import Tuple, Dict
from core.home_assistant.mqtt_packet.discovery import *

DISCOVERY_TOPIC = "homeassistant"

discovery_visitor = (
    DiscoveryCompositeVisitor()
    .add_visitor(RGBVisitor())
    .add_visitor(BrightnessVisitor())
    .add_visitor(AlarmVisitor())
    .add_visitor(BinaryVisitor())
    .add_visitor(SensorVisitor())
)


def get_discovery(entity: Entity) -> Tuple[Topic, Dict[str, str]]:
    discovery_visitor.visit(entity)
    topic = (
        Topic(TopicType.PUBLISHER)
        .add(DISCOVERY_TOPIC)
        .add(entity.entity_type)
        .add(entity.unique_id)
        .add("config")
    )
    return topic, discovery_visitor.get()
