from core.device.driver.abstract_driver import AbstractDriver
from typing import Optional
from core.device.hardware import Hardware
from core.utils.id_generator import generate_id
from attrs import define, field, setters


@define
class Entity:
    name: str = field(on_setattr=setters.frozen)
    unique_id: str = field(default=generate_id, on_setattr=setters.frozen)
    entity_type: Optional[str] = None
    icon: Optional[str] = None
    driver: Optional[AbstractDriver] = None
    hardware: Optional[Hardware] = None
