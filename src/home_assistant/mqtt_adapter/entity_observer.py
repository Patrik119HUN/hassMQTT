from src.mqtt.mqtt_manager import TopicObserver, MQTTManager
from abc import ABC
from src.device.entity import Entity
from src.mqtt.topic_builder import Topic, TopicType
from typing import Dict


class EntityObserver(TopicObserver, ABC):
    _mqtt_manager: MQTTManager
    _topics: Dict[str,str]
    _entity: Entity

    def __init__(self, mqtt_manager: MQTTManager, topics: Dict[str,str], entity: Entity):
        self._mqtt_manager = mqtt_manager
        self._mqtt_manager.publish(
            Topic.from_str(TopicType.PUBLISHER, topics["availability_topic"]), "online"
        )
        self._topics = topics
        self._entity = entity
