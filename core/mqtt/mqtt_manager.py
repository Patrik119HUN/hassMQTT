from core.utils.observer_interface import IObserver
from core.mqtt.topic import Topic, TopicType
from paho.mqtt.enums import CallbackAPIVersion, MQTTErrorCode
from paho.mqtt.client import Client, MQTTv311, MQTTMessage
from paho.mqtt.properties import MQTTException
from typing import List, Dict
from loguru import logger


class MQTTManager:
    __mqtt_instance: Client

    def __init__(
        self,
        client_id: str,
        broker: str,
        port: int = 1883,
        username: str = None,
        password: str = None,
    ):
        MQTTManager.__mqtt_instance = Client(
            callback_api_version=CallbackAPIVersion.VERSION2,
            client_id=client_id,
            protocol=MQTTv311,
        )
        self.__subscribers: Dict[str, List[IObserver]] = {}
        MQTTManager.__mqtt_instance.username_pw_set(username, password)
        MQTTManager.__mqtt_instance.on_message = self.__on_message

        error_code: MQTTErrorCode = MQTTManager.__mqtt_instance.connect(
            host=broker, port=port
        )
        if error_code != MQTTErrorCode.MQTT_ERR_SUCCESS:
            logger.error(f"Failed to connect: {error_code}. retrying")
            raise RuntimeError("Could not connect to MQTT broker!")
        logger.info(
            f"MQTT manager connected to:{broker}:{port} with username:{username}"
        )

    def __on_message(self, client: Client, userdata, msg: MQTTMessage) -> None:
        logger.debug(f"Received {msg.payload.decode()} from {msg.topic} topic")
        if msg.topic not in self.__subscribers:
            return
        for observer in self.__subscribers[msg.topic]:
            logger.info(f"Notifying observer:{msg.topic}")
            observer.update(topic=msg.topic, payload=msg.payload)

    def publish(
        self, topic: Topic, payload: str | bytes | bytearray | float | None
    ) -> None:
        if topic.get_topic_type is TopicType.SUBSCRIBER:
            logger.error("Could not use a SUBSCRIBER topic as a publisher")
            raise MQTTException("Could not use a SUBSCRIBER topic as a publisher")
        MQTTManager.__mqtt_instance.publish(topic.build(), payload)

    def add_subscriber(self, topic: Topic, observer: IObserver) -> None:
        topic_str: str = topic.build()
        if topic.get_topic_type is TopicType.PUBLISHER:
            logger.error("Could not use a PUBLISHER topic as a subscriber")
            raise MQTTException("Could not use a PUBLISHER topic as a subscriber")

        MQTTManager.__mqtt_instance.subscribe(topic=topic_str)
        logger.info(f"Client subscribed to:{topic_str}")
        if topic_str not in self.__subscribers:
            self.__subscribers[topic_str] = []
        self.__subscribers[topic_str].append(observer)

    def remove_subscriber(self, topic: Topic, observer: IObserver) -> None:
        if topic in self.__subscribers:
            self.__subscribers[topic.build()].remove(observer)
            if not self.__subscribers[topic.build()]:
                del self.__subscribers[topic.build()]

    @classmethod
    def instance(self) -> Client:
        return MQTTManager.__mqtt_instance
