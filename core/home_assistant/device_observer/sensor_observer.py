from core.home_assistant.device_observer import EntityObserver
from core.mqtt.topic_builder import Topic, TopicType
from loguru import logger
from core.device.light import BinaryLight
import time
from threading import Thread
from core.device.entity import Entity
from typing import Dict
from core.mqtt.mqtt_manager import MQTTManager


class SensorObserver(EntityObserver):
    def __init__(
        self, mqtt_manager: MQTTManager, topics: Dict[str, str], entity: Entity
    ):
        super().__init__(mqtt_manager, topics, entity)
        self.__state_topic = Topic.from_str(
            TopicType.PUBLISHER, self._topics["state_topic"]
        )
        self._entity.set_callback(self.on, self.off)
        self._mqtt_manager.publish(self.__state_topic, "OFF")

    def on(self):
        self._mqtt_manager.publish(self.__state_topic, "ON")

    def off(self):
        self._mqtt_manager.publish(self.__state_topic, "OFF")

    def update(self, topic: Topic, payload: bytes):
        pass
