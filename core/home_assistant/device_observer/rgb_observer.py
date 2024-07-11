from core.home_assistant.device_observer import BrightnessObserver
from core.mqtt.topic_builder import Topic, TopicType
from core.device.light import RGBLight


class RGBObserver(BrightnessObserver):
    def update(self, topic: Topic, payload: bytes):
        super().update(topic=topic, payload=payload)
        rgb_state_topic = Topic.from_str(TopicType.PUBLISHER, self._topics["rgb_state_topic"])
        self._mqtt_manager.publish(rgb_state_topic, payload)
        string = payload.decode("utf-8")
        for x in string.split(","):
            print(x)
