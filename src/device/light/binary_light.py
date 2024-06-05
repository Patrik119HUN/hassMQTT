from src.device.entity import Entity
from src.device.hardware import Hardware


class BinaryLight(Entity):
    __state: bool = False

    def __init__(
        self,
        name: str,
        device: Hardware = None,
        device_class: str = None,
        icon: str = None,
        unique_id: str = None,
    ):
        """
        Initializes an Entity object with its name, a device, a device class, an
        icon, and a unique ID.

        Args:
            name (str): identifier of the entity being initialized, which is used
                to store and retrieve information about the entity in the framework's
                database.
            device (None): 3rd party device that the `Entity` instance will manage
                in the system.
            device_class (None): categorical type of device being created, such
                as "Visual" or "Auditory".
            icon (None): image file to be used as a symbolic representation of the
                device in the UI, and it is expected to be a string containing the
                path or URL of the icon file.
            unique_id (None): unique identifier for the entity being initialized,
                which can be used to distinguish it from other entities of the
                same class in the system.

        """
        Entity.__init__(self, name, device, device_class, icon, unique_id)

    @property
    def state(self) -> bool:
        """
        Retrieves the internal state of the class object.

        Returns:
            bool: a Python `object` instance representing the current state of the
            system.

        """
        return self.__state

    @state.setter
    def state(self, state: bool) -> None:
        """
        Updates the value of an int variable based on a logical expression and
        sends it to a driver via a send_data call.

        Args:
            state (bool): binary value to be sent through the `driver.send_data()`
                method.

        """
        self.__state = state
        self.driver.send_data(0, state)

    def accept(self, visitor):
        """
        Lights up binary-based light.

        Args:
            visitor (`object`.): light object that is being traversed and manipulated
                by the `visitor` function.
                
                		- `self`: This is the current object being passed through the
                visitor pattern, providing information about its state and methods
                for manipulating it.
                
                	Additionally, `visitor` is an instance of a class representing
                the visitor pattern, which can be destructured to access its various
                attributes and methods for further manipulation or processing.

        """
        visitor.binary_light(self)
