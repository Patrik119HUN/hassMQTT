from src.device.entity import Entity


class BinarySensor(Entity):
    __state: bool = False

    @property
    def state(self):
        """
        Returns the current state object of the code generator.

        Returns:
            str: a reference to the current state of the system.

        """
        return self.__state

    @state.setter
    def state(self, value: bool):
        """
        Updates `state` with the input value.

        Args:
            value (bool): state of the instance being modified.

        """
        self.__state = value
