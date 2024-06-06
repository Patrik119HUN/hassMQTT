from src.mqtt.mqtt_manager import TopicObserver, MQTTManager
from src.home_assistant.mqtt_packet.discovery.base_packet import MQTTDiscoveryPacket
from abc import ABC
from src.device.light import BinaryLight
from src.device.entity import Entity


class EntityObserver(TopicObserver, ABC):
    _mqtt_manager: MQTTManager
    _topics: [MQTTDiscoveryPacket]
    _entity: BinaryLight

    def __init__(self, mqtt_manager: MQTTManager, topics: [MQTTDiscoveryPacket], entity: [Entity]):
        self._mqtt_manager = mqtt_manager
        self._mqtt_manager.publish(topics.availability_topic, b"online")
        self._topics = topics
        self._entity = entity
