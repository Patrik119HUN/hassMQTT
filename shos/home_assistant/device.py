from dataclasses import dataclass, field
from shos.home_assistant.abstract_driver import AbstractDriver
from typing import Optional
from shos.utils.id_generator import generate_id


@dataclass
class Hardware:
    name: str
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    sw_version: Optional[str] = None
    hw_version: Optional[str] = None
    identifiers: Optional[list[str]] = None
    connections: Optional[list[tuple]] = None
    configuration_url: Optional[str] = None
    via_device: Optional[str] = None


class MQTTEntitySettings:
    qos: int
    expire_after: int = None


@dataclass(init=False)
class Entity:
    name: str
    device: Optional[Hardware] = field(default=None, repr=False)
    device_class: Optional[str] = None
    icon: Optional[str] = None
    unique_id: str = field(default_factory=generate_id)
    driver: AbstractDriver = None

    def __init__(self, name: str, device: Hardware = None, device_class: str = None, icon: str = None):
        self.name = name
        self.device = device
        self.device_class = device_class
        self.icon = icon
