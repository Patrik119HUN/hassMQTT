from loguru import logger
from src.mqtt.topic_builder import Topic
from src.home_assistant.mqtt_adapter.entity_observer import EntityObserver


class BinaryObserver(EntityObserver):
    def update(self, topic: Topic, payload: bytes):
        if payload == b"ON":
            self._mqtt_manager.publish(self._topics.state_topic, payload)
            logger.info("Light turned on")
        if payload == b"OFF":
            self._mqtt_manager.publish(self._topics.state_topic, payload)
            logger.info("Light turned off")


class BrightnessObserver(EntityObserver):
    def update(self, topic: Topic, payload: bytes):
        self._mqtt_manager.publish(self._topics.brightness_state_topic, payload)


class RGBObserver(EntityObserver):
    def update(self, topic: Topic, payload: bytes):
        self._mqtt_manager.publish(self._topics.rgb_state_topic, payload)
