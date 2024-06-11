from pydantic import BaseModel
from src.device.light import BinaryLight, BrightnessLight, RGBLight
from src.device.alarm_control_panel import AlarmControlPanel
from typing import Dict
from src.device.entity import Entity
from src.mqtt.topic_builder import Topic, TopicType

BASE_TOPIC = "shos"


class MQTTVisitor:
    __base_topic: str
    __packet: Dict[str, str] = {}

    def __init__(self, base_topic: str = BASE_TOPIC):
        self.__base_topic = base_topic

    def __subscriber(self, entity: Entity) -> Topic:
        return Topic(TopicType.SUBSCRIBER).add(
            self.__base_topic, entity.entity_type, entity.unique_id
        )

    def __publisher(self, entity: Entity) -> Topic:
        return Topic(TopicType.PUBLISHER).add(
            self.__base_topic, entity.entity_type, entity.unique_id
        )

    def binary_light(self, light: BinaryLight):
        self.__packet = self.packet(light)

    def alarm_control_panel(self, alarm: AlarmControlPanel):
        self.__packet = self.packet(alarm)

    def brightness_light(self, light: BrightnessLight):
        packet = self.packet(light)
        packet.update(
            {
                "brightness_command_topic": self.__subscriber(light).add("brightness", "set").build(),
                "brightness_state_topic": self.__publisher(light).add("brightness", "state").build(),
            }
        )
        self.__packet = packet

    def rgb_light(self, light: RGBLight):
        self.brightness_light(light)
        packet = self.__packet
        packet.update(
            {
                "rgb_state_topic": self.__subscriber(light).add("rgb", "state").build(),
                "rgb_command_topic": self.__publisher(light).add("rgb", "set").build(),
            }
        )
        self.__packet = packet

    def packet(self, entity: Entity) -> Dict[str, str]:
        return {
            "name": entity.name,
            "unique_id": entity.unique_id,
            "command_topic": self.__subscriber(entity).add("set").build(),
            "availability_topic": self.__subscriber(entity).add("availability").build(),
            "state_topic": self.__publisher(entity).add("state").build(),
        }

    def get(self):
        return self.__packet
