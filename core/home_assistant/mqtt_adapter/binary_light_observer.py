from loguru import logger
from core.mqtt.topic_builder import Topic, TopicType
from core.home_assistant.mqtt_adapter.entity_observer import EntityObserver


class BinaryObserver(EntityObserver):
    def update(self, topic: Topic, payload: bytes):
        state_topic = Topic.from_str(TopicType.PUBLISHER, self._topics["state_topic"])
        if payload == b"ON":
            self._mqtt_manager.publish(state_topic, payload)
            logger.info("Light turned on")

        if payload == b"OFF":
            self._mqtt_manager.publish(state_topic, payload)
            logger.info("Light turned off")


class BrightnessObserver(EntityObserver):
    def update(self, topic: Topic, payload: bytes):
        brightness_state_topic = Topic.from_str(
            TopicType.PUBLISHER, self._topics["brightness_state_topic"]
        )
        self._mqtt_manager.publish(brightness_state_topic, payload)


class RGBObserver(EntityObserver):
    def update(self, topic: Topic, payload: bytes):
        rgb_state_topic = Topic.from_str(TopicType.PUBLISHER, self._topics["rgb_state_topic"])
        self._mqtt_manager.publish(rgb_state_topic, payload)
        string = payload.decode("utf-8")
        for x in string.split(","):
            print(x)


class AlarmObserver(EntityObserver):
    def update(self, topic: Topic, payload: bytes):
        state_topic = Topic.from_str(TopicType.PUBLISHER, self._topics["state_topic"])
        if payload == b"DISARM":
            self._mqtt_manager.publish(state_topic, b"disarmed")

        if payload == b"ARM_HOME":
            self._mqtt_manager.publish(state_topic, "armed_home")
        if payload == b"ARM_AWAY":
            self._mqtt_manager.publish(state_topic, "armed_away")
        if payload == b"ARM_NIGHT":
            self._mqtt_manager.publish(state_topic, "armed_night")
        if payload == b"ARM_VACATION":
            self._mqtt_manager.publish(state_topic, "armed_vacation")
        if payload == b"ARM_CUSTOM_BYPASS":
            self._mqtt_manager.publish(state_topic, "armed_custom_bypass")
