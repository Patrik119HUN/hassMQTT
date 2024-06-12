from core.device.entity import Entity
from core.mqtt.topic_builder import Topic, TopicType
from core.device.light import BinaryLight
from core.device.binary_sensor import BinarySensor
from core.device.alarm_control_panel import AlarmControlPanel
from core.home_assistant.mqtt_packet.visitor import MQTTVisitor
from typing import Tuple, Dict

DISCOVERY_TOPIC = "homeassistant"


def get_discovery(entity: Entity) -> Tuple[Topic, Dict[str, str]]:
    class_to_str = {
        BinaryLight: "light",
        BinarySensor: "sensor",
        AlarmControlPanel: "alarm_control_panel",
    }
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
