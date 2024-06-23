from core.home_assistant.device_observer import EntityObserver
from core.mqtt.topic_builder import Topic, TopicType
from core.device.light import BrightnessLight


class BrightnessObserver(EntityObserver):
    def update(self, topic: Topic, payload: bytes):
        brightness_state_topic = Topic.from_str(
            TopicType.PUBLISHER, self._topics["brightness_state_topic"]
        )
        self._mqtt_manager.publish(brightness_state_topic, payload)
