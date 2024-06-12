from core.home_assistant.driver.abstract_driver import AbstractDriver
from typing import Optional
from core.utils.id_generator import generate_id
from core.device.hardware import Hardware
from pydantic import BaseModel, GetCoreSchemaHandler, ConfigDict, Field, PlainSerializer
from typing import Any
from typing_extensions import Annotated

CustomStr = Annotated[
    AbstractDriver, PlainSerializer(lambda x: x.__class__.__name__, return_type=str)
]


class Entity(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True,str_strip_whitespace=True)

    name: str
    unique_id: str = None
    hardware: Optional[Hardware] = None
    entity_type: Optional[str] = None
    icon: Optional[str] = None
    driver: Optional[CustomStr] = None

    def accept(self, visitor):
        pass

    def from_entity(self, entity):
        pass

    @classmethod
    def get_type(cls):
        return cls.entity_type
