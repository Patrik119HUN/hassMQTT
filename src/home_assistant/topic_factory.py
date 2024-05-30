from src.mqtt.topic_builder import Topic, TopicType
import copy


class HATopicFactory:
    __topic: Topic

    def __init__(self, base_topic: str, device_type: str, device_id: str):
        """
        Generates high-quality documentation for code given to it.

        Args:
            base_topic (str): base topic that the generated documentation will be
                organized around.
            device_type (str): device type to which the generated documentation
                will apply.
            device_id (str): 10-digit unique identifier of a specific device within
                a publisher's fleet, as specified by the user.

        """
        self.__topic = (
            Topic(TopicType.PUBLISHER).add(base_topic).add(device_type).add(device_id)
        )

    def create(self, *args) -> str:
        """
        Takes a deep copy of the current topic and appends any argument passed to
        it, then returns a newly created topic instance with the updated content.

        Returns:
            str: a new topic object containing all the added arguments.

        """
        new_topic = copy.deepcopy(self.__topic)
        for arg in args:
            new_topic.add(arg)
        return new_topic.build()
