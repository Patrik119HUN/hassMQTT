from src.device.entity import Entity
from dataclasses import dataclass
from src.mqtt.topic_builder import Topic, TopicType
from src.device.light import BinaryLight
from src.device.binary_sensor import BinarySensor
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
        Sets instance variables `device` and `type` based on input parameter `device`.

        Args:
            device (Entity): 3D graphics hardware on which the scene is to be
                rendered, and its value is used to determine the appropriate
                rendering settings for the scene.

        """
        self.__device = device
        self.__type = self.get_component()

    def get_component(self):
        """
        Maps each item in the dictionary `self.__class_to_str` to its corresponding
        string value, and then checks if the device object is of that type. If it
        is, the function returns the associated string value.

        Returns:
            instance of `type: the string representation of the component class
            associated with the provided device.
            
            	For each key-value pair in the `self.__class_to_str` dictionary, if
            the value is an instance of the specified class, the return value is
            that class.

        """
        for x, y in self.__class_to_str.items():
            if isinstance(self.__device, x):
                return y

    def generate_discrovery_config_message(self):
        """
        Generates high-quality documentation for code

        """
        pass

    def get_discovery(self) -> Tuple[Topic, MQTTDiscoveryPacket]:
        """
        Is called by an instance of `MQTTVisitor` and returns a tuple containing
        the MQTT topic and message after processing a device acceptance.

        Returns:
            Tuple[Topic, MQTTDiscoveryPacket]: a topic and a data packet containing
            information about a device.

        """
        visitor = MQTTVisitor()
        self.__device.accept(visitor)
        packet = visitor.get()
        topic = (
            Topic(TopicType.PUBLISHER).add(DISCOVERY_TOPIC).add(self.__type).add(self.__device.unique_id).add("config")
        )
        return topic, packet
