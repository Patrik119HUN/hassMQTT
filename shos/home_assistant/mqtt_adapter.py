from shos.home_assistant.device import Entity
from dataclasses import dataclass
from shos.mqtt.topic_builder import Topic,TopicType

@dataclass
class MQTTEntitySettings:
    qos: int
    expire_after: int = None


class MQTTAdapter:
    __device: Entity = None

    def __init__(self, device: Entity) -> None:
        self.__device = device
    
    def getJsonDiscovery(self):
       topic = Topic(TopicType.PUBLISHER).add("homeassistant").add("asd")
    
