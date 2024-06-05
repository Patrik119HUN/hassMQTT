from pydantic import BaseModel
from src.device.light import BinaryLight, BrightnessLight, RGBLight
from src.home_assistant.mqtt_packet.discovery.light import *
from src.home_assistant.topic_factory import HATopicFactory, TopicType

BASE_TOPIC = "shos"


def json(thing: BaseModel) -> str:
    return thing.model_dump_json(exclude_unset=True, exclude_none=True, indent=2)


class MQTTVisitor:
    __base_topic: str
    __packet: MQTTDiscoveryPacket

    def __init__(self, base_topic: str = BASE_TOPIC):
        self.__base_topic = base_topic

    def binary_light(self, light: BinaryLight):
        base_topic = HATopicFactory(self.__base_topic, "light", light.unique_id)
        self.__packet = BinaryLightMQTTDiscoveryPacket(
            name=light.name,
            unique_id=light.unique_id,
            command_topic=base_topic.create("set"),
            availability_topic=HATopicFactory(self.__base_topic, "light", light.unique_id, TopicType.PUBLISHER).create(
                "availability"
            ),
            state_topic=HATopicFactory(self.__base_topic, "light", light.unique_id, TopicType.PUBLISHER).create(
                "state"
            ),
        )

    def brightness_light(self, light: BrightnessLight):
        base_topic = HATopicFactory(self.__base_topic, "light", light.unique_id)
        self.__packet = BrightnessLightMQTTDiscoveryPacket(
            name=light.name,
            unique_id=light.unique_id,
            state_topic=base_topic.create("state"),
            command_topic=base_topic.create("command"),
            availability_topic=base_topic.create("availability"),
            brightness_command_topic=base_topic.create("brightness", "set"),
            brightness_state_topic=base_topic.create("brightness", "state"),
        )

    def rgb_light(self, light: RGBLight):
        base_topic = HATopicFactory(self.__base_topic, "light", light.unique_id)
        self.__packet = RGBLightMQTTDiscoveryPacket(
            name=light.name,
            unique_id=light.unique_id,
            state_topic=base_topic.create("state"),
            command_topic=base_topic.create("command"),
            availability_topic=base_topic.create("availability"),
            brightness_command_topic=base_topic.create("brightness", "set"),
            brightness_state_topic=base_topic.create("brightness", "state"),
            rgb_state_topic=base_topic.create("rgb", "state"),
            rgb_command_topic=base_topic.create("rgb", "set"),
        )

    def get(self):
        return self.__packet
