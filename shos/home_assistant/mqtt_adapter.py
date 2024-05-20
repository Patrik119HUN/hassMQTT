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
        """
        Sets a variable named `device` to the value passed as an argument, serving
        as a shorthand for initializing other attributes based on that value.

        Args:
            device (Entity): 3D graphics device to which the code should be generated.

        """
        self.__device = device
    
    def getJsonDiscovery(self):
       """
       Generates high-quality documentation for code.

       """
       topic = Topic(TopicType.PUBLISHER).add("homeassistant").add("asd")
    
