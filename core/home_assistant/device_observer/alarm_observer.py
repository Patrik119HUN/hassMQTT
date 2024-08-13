from typing import Dict
from core.device.entity import Entity
from core.home_assistant.device_observer import EntityObserver
from core.mqtt.mqtt_manager import MQTTManager
from core.mqtt.topic import Topic, TopicType
from core.device.alarm_control_panel import *
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

    def update(self, *args, **kwargs):
        payload: bytes = kwargs["payload"]
        match payload:
            case b"DISARM":
                self._mqtt_manager.publish(self.state_topic, b"disarmed")
                self._entity.set_alarm(disarmed)
            case b"ARM_HOME":
                self._mqtt_manager.publish(self.state_topic, "armed_home")
                self._entity.set_alarm(arm_home)
            case b"ARM_AWAY":
                self._mqtt_manager.publish(self.state_topic, "armed_away")
                self._entity.set_alarm(arm_away)
            case b"ARM_NIGHT":
                self._mqtt_manager.publish(self.state_topic, "armed_night")
                self._entity.set_alarm(arm_night)
            case b"ARM_VACATION":
                self._mqtt_manager.publish(self.state_topic, "armed_vacation")
                self._entity.set_alarm(arm_vacation)
            case b"ARM_CUSTOM_BYPASS":
                self._mqtt_manager.publish(self.state_topic, "armed_custom_bypass")
