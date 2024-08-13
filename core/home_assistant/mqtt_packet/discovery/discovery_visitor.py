from core.mqtt.topic import Topic, TopicType
from core.device.entity import Entity
from typing import Dict

BASE_TOPIC = "shos"


class Discovery:
    _base_topic: str

    def __init__(self, base_topic: str = BASE_TOPIC):
        self._base_topic = base_topic

    def _subscriber(self, entity: Entity) -> Topic:
        return Topic(TopicType.SUBSCRIBER).add(
            self._base_topic, entity.entity_type, entity.unique_id
        )

    def _publisher(self, entity: Entity) -> Topic:
        return Topic(TopicType.PUBLISHER).add(
            self._base_topic, entity.entity_type, entity.unique_id
        )

    def packet(self, entity: Entity) -> Dict[str, str]:
        return {
            "name": entity.name,
            "unique_id": entity.unique_id,
            "command_topic": self._subscriber(entity).add("set").build(),
            "availability_topic": self._subscriber(entity).add("availability").build(),
            "state_topic": self._publisher(entity).add("state").build(),
        }
