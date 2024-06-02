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
        """
        Sets attributes for a `Topic` object based on given values, combining a
        `Topic` type, a base topic, and a device ID into a single instance.

        Args:
            base_topic (str): base topic for the device, which is combined with
                the device's ID to form the complete topic name.
            device_type (str): type of device associated with the topic, which is
                added to the Topic object in the function.
            device_id (str): unique identifier of the device to be updated.
            topic_type (TopicType.SUBSCRIBER): type of topic to which the device
                belongs.

        """
        self.__topic = Topic(topic_type).add(base_topic).add(device_type).add(device_id)

    def create(self, *args) -> Topic:
        """
        Deepcopies a `Topic` object and adds provided arguments to it, returning
        the modified `Topic`.

        Returns:
            Topic: a copy of the original topic with additional arguments added
            to it.

        """
        new_topic = copy.deepcopy(self.__topic)
        for arg in args:
            new_topic.add(arg)
        return new_topic
