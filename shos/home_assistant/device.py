from dataclasses import dataclass
import random
import string
from typing import Optional
from enum import StrEnum


class DeviceTypes(StrEnum):
    SENSOR = "sensor"
    SWITCH = "switch"
    BINARY_SENSOR = "binary_sensor"
    LIGHT = "light"
    COVER = "cover"
    CLIMATE = "climate"
    FAN = "fan"
    ALARM_PANEL = "alarm_control_panel"


@dataclass
class Device:
    name: str
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    sw_version: Optional[str] = None
    hw_version: Optional[str] = None
    identifiers: Optional[list[str]] = None
    connections: Optional[list[tuple]] = None
    configuration_url: Optional[str] = None
    via_device: Optional[str] = None


@dataclass
class EntityInfo:
    component: DeviceTypes
    name: str
    device: Optional[Device] = None
    device_class: Optional[str] = None
    enabled_by_default: Optional[bool] = None
    entity_category: Optional[str] = None
    expire_after: Optional[int] = None
    force_update: Optional[bool] = None
    icon: Optional[str] = None
    object_id: Optional[str] = None
    qos: Optional[int] = None
    unique_id: Optional[str] = None


type Entity = EntityInfo


def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
