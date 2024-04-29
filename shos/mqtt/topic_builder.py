from enum import Enum, auto


class TopicType(Enum):
    SUBSCRIBER = auto()
    PUBLISHER = auto()


class Topic:
    __list: list[str] = []
    __topic_type: TopicType = None

    def __init__(self, topic_type: TopicType) -> None:
        self.__topic_type = topic_type
        self.__list = list()
        pass

    def add(self, value: str):
        self.__list.append(value)
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
        return temp

    def __str__(self) -> str:
        return self.build()
