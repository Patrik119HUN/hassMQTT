from enum import Enum, auto, StrEnum
from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, List

import json


class TopicType(StrEnum):
    SUBSCRIBER = "SUBSCRIBER"
    PUBLISHER = "PUBLISHER"


class Topic:
    def __init__(self, topic_type: TopicType) -> None:
        self.__topic_type: TopicType = topic_type
        self.__list: List[str] = []

    def add(self, *args: str):
        for i in args:
            self.__list.append(i)
        return self

    def pop(self):
        self.__list.pop()
        return self

    def add_single_level(self):
        if self.__topic_type == TopicType.PUBLISHER:
            raise RuntimeError("Wildcards are not allowed in publisher topic")
        self.__list += "+"
        return self

    def add_multi_level(self):
        if self.__topic_type == TopicType.PUBLISHER:
            raise RuntimeError("Wildcards are not allowed in publisher topic")
        self.__list += "#"
        return self

    def build(self) -> str:
        temp: str = ""
        for x in self.__list:
            temp += x + "/"
        temp = temp[:-1]
        return temp

    def to_json(self):
        return json.dumps(self.build())

    @property
    def get_topic_type(self):
        return self.__topic_type

    def __str__(self) -> str:
        return self.build()

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(self.build)

    @classmethod
    def from_str(cls, topic_type: TopicType, value: str):
        topic = cls(topic_type)
        for x in value.split("/"):
            topic.add(x)
        return topic

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.is_instance_schema(Topic),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda c: c.build()
            ),
        )
