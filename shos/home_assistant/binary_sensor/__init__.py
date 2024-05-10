from shos.home_assistant.device import Entity
from shos.home_assistant.abstract_driver import AbstractDriver


class BinarySensor(Entity):
    __state: bool = False

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value: bool):
        self.__state = value
