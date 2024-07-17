from typing import Dict, TypeVar
from core.home_assistant.device_observer import *
from core.device.entity import Entity
from core.device.light import *
from core.device.binary_sensor import BinarySensor
from core.device.alarm_control_panel import AlarmControlPanel
from core.mqtt.mqtt_manager import TopicObserver, MQTTManager

observer_registry: Dict[type, type] = {
    BinarySensor: SensorObserver,
    BinaryLight: BinaryObserver,
    BrightnessLight: BrightnessObserver,
    RGBLight: BinaryObserver,
    AlarmControlPanel: AlarmObserver,
}

observer_dict = {
    "brightness_command_topic": BrightnessObserver,
    "rgb_command_topic": RGBObserver,
}

B = TypeVar("B", bound=EntityObserver)


class ObserverFactory:
    _mqtt_manager: MQTTManager

    def __init__(self, mqtt_manager: MQTTManager):
        self._mqtt_manager = mqtt_manager

    def get_observers(self, entity: Entity, topics: Dict[str, str]):
        observers: Dict[str, B] = {}
        for topic, observer in observer_dict.items():
            if topic in topics:
                subscriber = topics[topic]
                observers[subscriber] = observer(self._mqtt_manager, topics, entity)
        if "command_topic" in topics:
            observers[topics["command_topic"]] = observer_registry[type(entity)](
                self._mqtt_manager, topics, entity
            )

        if entity.entity_type == "binary_sensor":
            observers[topics["state_topic"]] = observer_registry[BinarySensor](
                self._mqtt_manager, topics, entity
            )
        return observers
