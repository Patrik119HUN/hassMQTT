from typing import Dict, TypeVar
from core.home_assistant.device_observer import *
from core.device.entity import Entity
from core.mqtt.mqtt_manager import MQTTManager
from core.mqtt.topic import Topic, TopicType
from core.home_assistant.device_observer.observer_data import ObserverData

B = TypeVar("B", bound=EntityObserver)


class ObserverFactory:
    def __init__(self, mqtt_manager: MQTTManager = None):
        self._mqtt_manager = mqtt_manager
        self.__observer_registry: Dict[Entity, ObserverData] = {}

    def set_mqtt_manager(self, mqtt_manager: MQTTManager):
        self._mqtt_manager = mqtt_manager

    def register(self, device_type: type, observer_data: ObserverData):
        self.__observer_registry[device_type] = observer_data

    def get_observers(self, entity: Entity, topics: Dict[str, str]):
        observers: Dict[Topic, B] = {}

        entity_observers = self.__observer_registry[type(entity)]
        if entity_observers.command_observer is not None:
            subscribe_topic = Topic.from_str(
                TopicType.SUBSCRIBER, topics["command_topic"]
            )
            observers[subscribe_topic] = entity_observers.command_observer(
                self._mqtt_manager, topics, entity
            )

        if entity_observers.state_observer is not None:
            subscribe_topic = Topic.from_str(
                TopicType.SUBSCRIBER, topics["state_topic"]
            )
            observers[subscribe_topic] = entity_observers.state_observer(
                self._mqtt_manager, topics, entity
            )
        if entity_observers.other_observers is not None:
            for topic, observer in entity_observers.other_observers.items():
                if topic in topics:
                    subscribe_topic = Topic.from_str(
                        TopicType.SUBSCRIBER, topics[topic]
                    )
                    observers[subscribe_topic] = observer(
                        self._mqtt_manager, topics, entity
                    )
        return observers
