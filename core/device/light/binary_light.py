from core.device.entity import Entity
from core.device.hardware import Hardware
from .light_builder import light_registry


@light_registry.register("binary")
class BinaryLight(Entity):
    color_mode: str = "binary"
    __state: bool = False

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

    @classmethod
    def from_entity(cls, entity: Entity):
        return cls(entity.name, entity.hardware, entity.entity_type, entity.icon, entity.unique_id)
