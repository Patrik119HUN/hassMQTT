from pydantic import BaseModel
from src.home_assistant.device import Hardware


class MQTTDiscoveryPacket(BaseModel):
    name: str
    unique_id: str
    state_topic: str
    command_topic: str
    availability_topic: str
    device: Hardware = None
