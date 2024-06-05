from dataclasses import dataclass, field
from src.home_assistant.driver.abstract_driver import AbstractDriver
from typing import Optional
from src.utils.id_generator import generate_id
from src.device.hardware import Hardware


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
        Generates a dictionary representing an instance of a class.

        Returns:
            dict: a dictionary containing various attributes of the `self` object.

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
        Sets instance attributes from a dictionary representation, maintaining
        object state during serialization or pickling.

        Args:
            state (dict): object containing information about a device, including
                its name, class, icon, and unique ID, as well as the name of the
                driver responsible for managing it.

        """
        self.name = state["name"]
        self.device = state["device"]
        self.device_class = state["device_class"]
        self.icon = state["icon"]
        self.unique_id = state["id"]
        driver_name = state["driver"]

    def accept(self, visitor):
        """
        Accepts a passed string argument and returns it without modification.

        Args:
            visitor (� visitors.): 3D object to be rendered in the scene, which
                is passed to the render method for rendering.
                
                		- The `visitor` instance has a `content` property that contains
                the deserialized content as an object or array.
                		- The `content` property can be accessed directly without any
                wrapping or container objects.
                		- The `visitor` instance also has a `position` property that
                tracks the position of the deserialized content in the input stream.
                		- The `position` property is an integer value that indicates the
                current position of the deserialized content in the input stream,
                relative to the start of the input stream.

        """
        pass
