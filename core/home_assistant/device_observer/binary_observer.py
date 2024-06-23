from core.home_assistant.device_observer import EntityObserver
from core.mqtt.topic_builder import Topic, TopicType
from loguru import logger
from core.device.light import BinaryLight


class BinaryObserver(EntityObserver):
    def update(self, topic: Topic, payload: bytes):
        state_topic = Topic.from_str(TopicType.PUBLISHER, self._topics["state_topic"])
        if payload == b"ON":
            self._mqtt_manager.publish(state_topic, payload)
            logger.info("Light turned on")

        if payload == b"OFF":
            self._mqtt_manager.publish(state_topic, payload)
            logger.info("Light turned off")
