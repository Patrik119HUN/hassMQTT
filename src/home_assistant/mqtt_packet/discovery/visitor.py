from pydantic import BaseModel
from src.device.light import BinaryLight, BrightnessLight, RGBLight
from src.home_assistant.mqtt_packet.discovery.light import *
from src.home_assistant.topic_factory import HATopicFactory, TopicType

BASE_TOPIC = "shos"


def json(thing: BaseModel) -> str:
    """
    "thing.model_dump_json(exclude_unset=True, exclude_none=True, indent=2)"
    generates high-quality documentation for given code by producing a JSON
    representation of the code's model without unset or none fields and with
    indentation level of 2.

    Args:
        thing (BaseModel): Python object that contains data to be serialized as JSON.

    Returns:
        str: a serialized representation of the `thing` object.

    """
    return thing.model_dump_json(exclude_unset=True, exclude_none=True, indent=2)


class MQTTVisitor:
    __base_topic: str
    __packet: MQTTDiscoveryPacket

    def __init__(self, base_topic: str = BASE_TOPIC):
        """
        Sets a code generator's topical variable `self._base_topic`.

        Args:
            base_topic (BASE_TOPIC): topic that the function will operate on.

        """
        self.__base_topic = base_topic

    def binary_light(self, light: BinaryLight):
        """
        Creates a Binary Light MQTT Discovery Packet, including command and state
        topics, based on input `light` data.

        Args:
            light (BinaryLight): device that the function is generating documentation
                for, providing its name and unique ID.

        """
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
        """
        Generates a BrightnessLightMQTTDiscoveryPacket with various MQTT topics
        for a light device based on its given information, such as name, unique
        ID, and brightness command and state topics.

        Args:
            light (BrightnessLight): instance of a `light` class and provides the
                unique ID of the light to be configured.

        """
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
        """
        Creates a packet for RGB light device based on its provided name and unique
        ID, specifying the topic names for its state, command, availability,
        brightness set and state, and RGB state and set topics.

        Args:
            light (RGBLight): object being discovered, providing its name and
                unique ID for use in generating the discovery packet.

        """
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
        """
        Retrieves the internal packet representation of the class instance provided
        as its argument.

        Returns:
            Packet: a packet object.
            
            		- `self`: This is the current object instance being worked on, which
            contains all the necessary information to generate high-quality documentation.
            		- `__packet`: The output of the `get` function, which is a packet
            of documentation that can be used to generate code documentation.

        """
        return self.__packet
