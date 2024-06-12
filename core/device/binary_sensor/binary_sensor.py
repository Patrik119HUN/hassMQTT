from core.device.entity import Entity


class BinarySensor(Entity):
    __state: bool = False

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value: bool):
        self.__state = value
