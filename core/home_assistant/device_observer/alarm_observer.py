from core.home_assistant.device_observer import EntityObserver
from core.mqtt.topic_builder import Topic, TopicType
from core.device.alarm_control_panel import AlarmControlPanel


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
