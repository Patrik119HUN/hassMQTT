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
        Entity.__init__(self, name, device, device_class, icon, unique_id)

    @property
    def state(self) -> bool:
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
        visitor.binary_light(self)
