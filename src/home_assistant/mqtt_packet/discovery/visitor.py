from pydantic import BaseModel
from src.home_assistant.light import BinaryLight, BrightnessLight, RGBLight
from src.home_assistant.mqtt_packet.discovery.light import *
from src.home_assistant.topic_factory import HATopicFactory

BASE_TOPIC = "shos"


def json(thing: BaseModel) -> str:
    """
    Returns a JSON representation of the given object model in less than 50 words

    Args:
        thing (BaseModel): code to be documented, and the `model_dump_json()`
            function generates high-quality documentation for it.

    Returns:
        str: a JSON-formatted string containing the model dump of the provided input.

    """
    return thing.model_dump_json(exclude_unset=True, exclude_none=True, indent=2)


class MQTTVisitor:
    __base_topic: str
    __packet: MQTTDiscoveryPacket

    def __init__(self, base_topic: str = BASE_TOPIC):
        """
        Sets the `base_topic` attribute of a Python object, indicating the topic
        that serves as the base or starting point for the object's documentation.

        Args:
            base_topic (BASE_TOPIC): top-level topic or category for which
                high-quality documentation is to be generated.

        """
        self.__base_topic = base_topic

    def binary_light(self, light: BinaryLight):
        """
        Creates a Binary Light MQTT discovery packet with a name, unique ID, and
        three topic names: "state", "set", and "availability".

        Args:
            light (BinaryLight): Light object to create a packet for in the `BinaryLightMQTTDiscoveryPacket`.

        """
        base_topic = HATopicFactory(self.__base_topic, "light", light.unique_id)
        self.__packet = BinaryLightMQTTDiscoveryPacket(
            name=light.name,
            unique_id=light.unique_id,
            state_topic=base_topic.create("state"),
            command_topic=base_topic.create("set"),
            availability_topic=base_topic.create("availability"),
        )

    def brightness_light(self, light: BrightnessLight):
        """
        Creates a Brightness Light MQTT Discovery Packet based on a given light
        object, specifying topics for state, command, availability, and brightness
        control and state.

        Args:
            light (BrightnessLight): object to generate high-quality documentation
                for, providing its name and unique ID.

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
        Defines a MQTT discovery packet for an RGB light, defining various topics
        and commands for state, control, and availability.

        Args:
            light (RGBLight): `Light` object that provides the necessary information
                to generate high-quality documentation for the code.

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
        Returns a copy of its receiver (i.e., itself) as a `Packet` object.

        Returns:
            Packet: a packet object instance.
            
            		- `self`: A reference to the `Packet` object, indicating that the
            method returned a reference to the same object for further manipulation
            or methods call.
            		- `__packet`: The actual packet data as a bytestring, which can be
            further processed or analyzed.

        """
        return self.__packet
