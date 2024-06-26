from core.mqtt.mqtt_manager import TopicObserver, MQTTManager
from abc import ABC
from core.device.entity import Entity
from core.mqtt.topic_builder import Topic, TopicType
from typing import Dict
import time


class EntityObserver(TopicObserver, ABC):
    _mqtt_manager: MQTTManager
    _topics: Dict[str, str]
    _entity: Entity

    def __init__(self, mqtt_manager: MQTTManager, topics: Dict[str, str], entity: Entity):
        self._mqtt_manager = mqtt_manager
        self._mqtt_manager.publish(
            Topic.from_str(TopicType.PUBLISHER, topics["availability_topic"]), "online"
        )
        self._topics = topics
        self._entity = entity
