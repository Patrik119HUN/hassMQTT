from src.mqtt.topic_builder import Topic, TopicType
import copy


class HATopicFactory:
    __topic: Topic

    def __init__(
        self,
        base_topic: str,
        device_type: str,
        device_id: str,
        topic_type: TopicType = TopicType.SUBSCRIBER,
    ):
        self.__topic = Topic(topic_type).add(base_topic).add(device_type).add(device_id)

    def create(self, *args) -> Topic:
        new_topic = copy.deepcopy(self.__topic)
        for arg in args:
            new_topic.add(arg)
        return new_topic
