from src.home_assistant.device import Entity
from dataclasses import dataclass
from src.mqtt.topic_builder import Topic, TopicType
from src.home_assistant.light import BinaryLight
from src.home_assistant.binary_sensor import BinarySensor
from src.home_assistant.mqtt_packet.discovery.visitor import MQTTVisitor
from src.home_assistant.mqtt_packet.discovery.base_packet import MQTTDiscoveryPacket
from typing import Tuple

DISCOVERY_TOPIC = "homeassistant"


@dataclass
class MQTTEntitySettings:
    qos: int
    expire_after: int = None


class DeviceToMQTTAdatper:
    __device: Entity = None
    __type: str = None
    __class_to_str = {BinaryLight: "light", BinarySensor: "sensor"}

    def __init__(self, device: Entity) -> None:
        """
        Initializes class instance variables `device` and `type`.

        Args:
            device (Entity): 3D printer or other hardware component associated
                with the code being generated.

        """
        self.__device = device
        self.__type = self.get_component()

    def get_component(self):
        """
        Iterates through the class variables defined on a Python class, and for
        each variable returns its corresponding string value if the variable is
        an instance of a specified type.

        Returns:
            str: a string representing the fully qualified name of the component
            instance being evaluated.

        """
        for x, y in self.__class_to_str.items():
            if isinstance(self.__device, x):
                return y

    def generate_discrovery_config_message(self):
        """
        Creates a discovery configuration message for code that is passed as input.

        """
        pass

    def get_discovery(self) -> Tuple[Topic, MQTTDiscoveryPacket]:
        """
        Creates a Topic object representing a MQTT subscription to a discovery
        endpoint and returns it along with an MQTT packet containing the device configuration.

        Returns:
            Tuple[Topic, MQTTDiscoveryPacket]: a tuple containing the MQTT topic
            and a payload.

        """
        visitor = MQTTVisitor()
        self.__device.accept(visitor)
        packet = visitor.get()
        topic = (
            Topic(TopicType.PUBLISHER)
            .add(DISCOVERY_TOPIC)
            .add(self.__type)
            .add(self.__device.unique_id)
            .add("config")
        )
        return topic, packet
