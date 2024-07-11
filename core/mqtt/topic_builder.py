from enum import Enum, auto, StrEnum
from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, List

import json


class TopicType(StrEnum):
    SUBSCRIBER = "SUBSCRIBER"
    PUBLISHER = "PUBLISHER"


class Topic:
    __list: list[str] = []
    __topic_type: TopicType = None

    def __init__(self, topic_type: TopicType) -> None:
        """
        Initializes a `Topic` class object by setting its `__topic_type` attribute
        to a given value and creating an empty list called `__list`.

        Args:
            topic_type (TopicType): type of documentation to be generated by the
                function, such as code or concept, and influences the output
                structure and content.

        """
        self.__topic_type = topic_type
        self.__list = list()
        pass

    def add(self, *args: str):
        for i in args:
            self.__list.append(i)
        return self

    def pop(self):
        self.__list.pop()
        return self

    def add_single_level(self):
        """
        Updates a list with a new string by concatenating it with the previous
        content using the plus operator, and then raises an error if the topic
        type is publisher.

        Returns:
            str: a list with a concatenated string and a plus sign at the end.

        """
        if self.__topic_type == TopicType.PUBLISHER:
            raise RuntimeError("Wildcards are not allowed in publisher topic")
        self.__list += "+"
        return self

    def add_multi_level(self):
        """
        Allows the addition of multiple level wildcard topics to a list, with the
        exception of publisher topics. The function appends a `#` symbol to the
        list and raises a runtime error for publisher topics.

        Returns:
            str: a new list with a # character appended, indicating that wildcards
            are not allowed in publisher topics.

        """
        if self.__topic_type == TopicType.PUBLISHER:
            raise RuntimeError("Wildcards are not allowed in publisher topic")
        self.__list += "#"
        return self

    def build(self) -> str:
        """
        Concatenates the elements of an iterable list `self.__list` separated by
        a `/`. It returns the resulting string.

        Returns:
            str: a concatenation of the elements of the `self._list` list, separated
            by slashes.

        """
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
            serialization=core_schema.plain_serializer_function_ser_schema(lambda c: c.build()),
        )