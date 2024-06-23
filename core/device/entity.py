from core.device.driver.abstract_driver import AbstractDriver
from typing import Optional
from core.device.hardware import Hardware
from pydantic import BaseModel, ConfigDict, PlainSerializer
from typing_extensions import Annotated

CustomStr = Annotated[
    AbstractDriver, PlainSerializer(lambda x: x.__class__.__name__, return_type=str)
]


class Entity(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True,str_strip_whitespace=True)

    name: str
    unique_id: str = None
    entity_type: Optional[str] = None
    icon: Optional[str] = None
    driver: Optional[CustomStr] = None
    hardware: Optional[Hardware] = None

    def accept(self, visitor):
        pass

    def from_entity(self, entity):
        pass

    @classmethod
    def get_type(cls):
        return cls.entity_type
