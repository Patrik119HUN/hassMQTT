from dataclasses import dataclass, field
from src.home_assistant.driver.abstract_driver import AbstractDriver
from typing import Optional
from src.utils.id_generator import generate_id
from src.device.hardware import Hardware


@dataclass(init=False)
class Entity:
    name: str
    hardware: Optional[Hardware] = field(default=None, repr=False)
    entity_type: Optional[str] = None
    icon: Optional[str] = None
    unique_id: str = None
    driver: AbstractDriver = None

    def __init__(
        self,
        name: str,
        hardware: Hardware = None,
        entity_type: str = None,
        icon: str = None,
        unique_id: str = None,
    ):
        """
        Initializes an instance variable `self.name`, `self.device`, `self.device_class`,
        and `self.icon`.

        Args:
            name (str): device's name.
            hardware (None): device to which the documentation will be generated for.
            entity_type (None): categorical type of device being processed by the
                function, with values including `Desktop`, `Laptop`, and `Tablet`.
            icon (None): 2D icon to be displayed next to the device in the list,
                as specified by its value.

        """
        self.name = name
        self.hardware = hardware
        self.entity_type = entity_type
        self.icon = icon
        self.unique_id = generate_id() if unique_id is None else unique_id

    def __getstate__(self):
        return {
            "name": self.name,
            "hardware": self.hardware,
            "entity_type": self.entity_type,
            "icon": self.icon,
            "id": self.unique_id,
            "driver": self.driver.__class__.__name__,
        }

    def __setstate__(self, state):
        self.name = state["name"]
        self.hardware = state["hardware"]
        self.entity_type = state["entity_type"]
        self.icon = state["icon"]
        self.unique_id = state["id"]
        driver_name = state["driver"]

    def accept(self, visitor):
        pass

    def from_entity(self, entity):
        pass

    @classmethod
    def get_type(cls):
        return cls.entity_type
