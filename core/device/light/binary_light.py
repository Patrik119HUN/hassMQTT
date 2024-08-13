from core.device.entity import Entity
from core.device.hardware import Hardware
from core.utils.id_generator import generate_id
from dataclasses import dataclass
from attrs import define

@define
class BinaryLight(Entity):
    entity_type:str = "light"
    color_mode:str = "binary"
    __state: bool = False

    @property
    def state(self) -> bool:
        return self.__state

    @state.setter
    def state(self, state: bool) -> None:
        self.driver.send_data(0, state)
        self.__state = state
