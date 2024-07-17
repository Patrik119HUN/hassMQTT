from core.device.entity import Entity
from core.home_assistant.device_observer import EntityObserver
from core.mqtt.mqtt_manager import MQTTManager
from core.mqtt.topic_builder import Topic, TopicType
from typing import Dict


class RGBObserver(EntityObserver):
    def __init__(
        self, mqtt_manager: MQTTManager, topics: Dict[str, str], entity: Entity
    ):
        super().__init__(mqtt_manager, topics, entity)
        self.__rgb_state_topic = Topic.from_str(
            TopicType.PUBLISHER, self._topics["rgb_state_topic"]
        )

    def update(self, topic: Topic, payload: bytes):
        self._mqtt_manager.publish(self.__rgb_state_topic, payload)
        self._entity.color = tuple(map(int, payload.decode("utf-8").split(",")))
