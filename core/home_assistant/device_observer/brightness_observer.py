from core.home_assistant.device_observer import BinaryObserver
from core.mqtt.topic_builder import Topic, TopicType
from core.device.light import BrightnessLight


class BrightnessObserver(BinaryObserver):
    def update(self, topic: Topic, payload: bytes):
        super().update(topic=topic, payload=payload)
        brightness_state_topic = Topic.from_str(
            TopicType.PUBLISHER, self._topics["brightness_state_topic"]
        )
        self._mqtt_manager.publish(brightness_state_topic, payload)
