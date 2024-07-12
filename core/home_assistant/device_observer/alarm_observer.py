from typing import Dict
from core.device.entity import Entity
from core.home_assistant.device_observer import EntityObserver
from core.mqtt.mqtt_manager import MQTTManager
from core.mqtt.topic_builder import Topic, TopicType
from core.device.alarm_control_panel import AlarmControlPanel
from threading import Thread
import time

class AlarmObserver(EntityObserver):
    def __init__(
        self, mqtt_manager: MQTTManager, topics: Dict[str, str], entity: Entity
    ):
        super().__init__(mqtt_manager, topics, entity)
        self.state_topic = Topic.from_str(
            TopicType.PUBLISHER, self._topics["state_topic"]
        )
        thread = Thread(target=self.triggered)
        thread.start()

    def triggered(self):
        while True:
            if self._entity.state():
                self._mqtt_manager.publish(self.state_topic, "triggered")
            time.sleep(1)

    def update(self, topic: Topic, payload: bytes):
        if payload == b"DISARM":
            self._mqtt_manager.publish(self.state_topic, b"disarmed")
        if payload == b"ARM_HOME":
            self._mqtt_manager.publish(self.state_topic, "armed_home")
        if payload == b"ARM_AWAY":
            self._mqtt_manager.publish(self.state_topic, "armed_away")
        if payload == b"ARM_NIGHT":
            self._mqtt_manager.publish(self.state_topic, "armed_night")
        if payload == b"ARM_VACATION":
            self._mqtt_manager.publish(self.state_topic, "armed_vacation")
        if payload == b"ARM_CUSTOM_BYPASS":
            self._mqtt_manager.publish(self.state_topic, "armed_custom_bypass")
