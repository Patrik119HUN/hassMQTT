from pydantic import BaseModel
from src.home_assistant.device import Hardware
from src.mqtt.topic_builder import Topic


class MQTTDiscoveryPacket(BaseModel):
    name: str
    unique_id: str
    state_topic: Topic
    command_topic: Topic
    availability_topic: Topic
    device: Hardware = None
