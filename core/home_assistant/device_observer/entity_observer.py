from core.mqtt.mqtt_manager import MQTTManager
from abc import ABC, abstractmethod
from core.device.entity import Entity
from core.mqtt.topic import Topic, TopicType
from typing import Dict
from core.utils.observer_interface import IObserver


class EntityObserver(IObserver, ABC):
    def __init__(
        self, mqtt_manager: MQTTManager, topics: Dict[str, str], entity: Entity
    ):
        self._mqtt_manager = mqtt_manager
        self._topics = topics
        self._entity = entity

    @abstractmethod
    def update(self, *args, **kwargs):
        pass
