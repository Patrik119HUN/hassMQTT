from dataclasses import dataclass, field
from src.home_assistant.driver.abstract_driver import AbstractDriver
from typing import Optional
from src.utils.id_generator import generate_id
from src.modbus_controller import modbus_controller


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


@dataclass(init=False)
class Entity:
    name: str
    device: Optional[Hardware] = field(default=None, repr=False)
    device_class: Optional[str] = None
    icon: Optional[str] = None
    unique_id: str = None
    driver: AbstractDriver = None

    def __init__(
        self,
        name: str,
        device: Hardware = None,
        device_class: str = None,
        icon: str = None,
        unique_id: str = None,
    ):
        """
        Initializes an instance variable `self.name`, `self.device`, `self.device_class`,
        and `self.icon`.

        Args:
            name (str): device's name.
            device (None): device to which the documentation will be generated for.
            device_class (None): categorical type of device being processed by the
                function, with values including `Desktop`, `Laptop`, and `Tablet`.
            icon (None): 2D icon to be displayed next to the device in the list,
                as specified by its value.

        """
        self.name = name
        self.device = device
        self.device_class = device_class
        self.icon = icon
        self.unique_id = generate_id() if unique_id is None else unique_id

    def __getstate__(self):
        """
        Generates a Python tuple representing the state of an object instance. The
        function returns a dictionary with the object's attributes, including name,
        device, device_class, icon, unique_id, and driver.

        Returns:
            dict: a dictionary containing key-value pairs of object properties.

        """
        return {
            "name": self.name,
            "device": self.device,
            "device_class": self.device_class,
            "icon": self.icon,
            "id": self.unique_id,
            "driver": self.driver.__class__.__name__,
        }

    def __setstate__(self, state):
        """
        Sets instance variables from a dictionary of class state.

        Args:
            state (dict): configuration details of the device being created,
                providing values for `name`, `device`, `device_class`, `icon`, and
                `unique_id`.

        """
        self.name = state["name"]
        self.device = state["device"]
        self.device_class = state["device_class"]
        self.icon = state["icon"]
        self.unique_id = state["id"]
        driver_name = state["driver"]

    def accept(self, visitor):
        """
        Is intended to accept an incoming message from a user or system and perform
        the desired action.

        Args:
            visitor (int): 2D rectangle that is being updated or drawn in the
                corresponding graphical element.

        """
        pass
