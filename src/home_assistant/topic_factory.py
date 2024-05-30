from src.mqtt.topic_builder import Topic, TopicType
import copy


class HATopicFactory:
    __topic: Topic

    def __init__(self, base_topic: str, device_type: str, device_id: str):
        self.__topic = (
            Topic(TopicType.PUBLISHER).add(base_topic).add(device_type).add(device_id)
        )

    def create(self, *args) -> str:
        new_topic = copy.deepcopy(self.__topic)
        for arg in args:
            new_topic.add(arg)
        return new_topic.build()
