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
        self.__device = device
        self.__type = self.get_component()

    def get_component(self):
        for x, y in self.__class_to_str.items():
            if isinstance(self.__device, x):
                return y

    def generate_discrovery_config_message(self):
        pass

    def get_discovery(self) -> Tuple[Topic, MQTTDiscoveryPacket]:
        visitor = MQTTVisitor()
        self.__device.accept(visitor)
        packet = visitor.get()
        topic = (
            Topic(TopicType.PUBLISHER).add(DISCOVERY_TOPIC).add(self.__type).add(self.__device.unique_id).add("config")
        )
        return topic, packet
