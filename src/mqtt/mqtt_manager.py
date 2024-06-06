from paho.mqtt.client import Client, MQTTv311, MQTTMessage, ConnectFlags
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.reasoncodes import ReasonCode
from paho.mqtt.properties import Properties, MQTTException
from loguru import logger
from src.mqtt.topic_builder import Topic, TopicType, StringToTopic
from typing import Callable, List, Dict
from abc import ABC, abstractmethod


class TopicObserver(ABC):
    @abstractmethod
    def update(self, topic: Topic, payload: bytes):
        pass


class MQTTManager:
    __mqtt_instance: Client = None
    __subscribers: Dict[str, List[TopicObserver]] = {}

    def __init__(
        self,
        client_id: str,
        broker: str,
        port: int,
        username: str = None,
        password: str = None,
    ) -> None:
        """
        Sets up an instance of a MQTT client using `Client()` and establishes
        communication with an MQTT broker by calling `connect()`.

        Args:
            client_id (str): 16-bit unique identifier of the MQTT client.
            broker (str): address of the MQTT broker server to which the client
                will connect.
            port (int): 16-bit unsigned integer that specifies the MQTT broker's
                port number where the client will connect.

        """
        self.__mqtt_instance = Client(
            callback_api_version=CallbackAPIVersion.VERSION2,
            client_id=client_id,
            protocol=MQTTv311,
        )

        self.__mqtt_instance.username_pw_set(username, password)
        self.__mqtt_instance.on_connect = MQTTManager.__on_connect
        self.__mqtt_instance.on_message = self.__on_message

        self.__mqtt_instance.connect(host=broker, port=port)
        logger.info(f"MQTT manager connected to:{broker}:{port} with username:{username}")

    def __on_message(self, client: Client, userdata, msg: MQTTMessage):
        message = msg.payload.decode("utf-8")
        topic = Topic.from_str(TopicType.SUBSCRIBER, msg.topic)
        self.__notify_subscriber(topic, msg.payload)
        logger.debug(f"Received {message} from {msg.topic} topic")

    @staticmethod
    def __on_connect(
        client: Client,
        userdata,
        flags: ConnectFlags,
        reason_code: ReasonCode,
        property: Properties,
    ):
        if reason_code.is_failure:
            logger.error(f"Failed to connect: {reason_code}. retrying")
        else:
            logger.debug(reason_code.getName())

    def publish(self, topic: Topic, payload: str | bytes | bytearray | float | None):
        if topic.get_topic_type is TopicType.PUBLISHER:
            self.__mqtt_instance.publish(
                topic=topic.build(),
                payload=payload,
                qos=0,
            )
        else:
            logger.error("Could not use a SUBSCRIBER topic as a publisher")
            raise MQTTException("Could not use a SUBSCRIBER topic as a publisher")

    def add_subscriber(self, topic: Topic, observer: TopicObserver):
        topic_str: str = topic.build()
        if topic.get_topic_type is TopicType.SUBSCRIBER:
            self.__mqtt_instance.subscribe(topic=topic_str)
            logger.info(f"Client subscribed to:{topic_str}")
        else:
            logger.error("Could not use a PUBLISHER topic as a subscriber")
            raise MQTTException("Could not use a PUBLISHER topic as a subscriber")
        if topic_str not in self.__subscribers:
            self.__subscribers[topic_str] = []
        self.__subscribers[topic_str].append(observer)

    def remove_subscriber(self, topic: Topic, observer: TopicObserver):
        if topic in self.__subscribers:
            self.__subscribers[topic.build()].remove(observer)
            if not self.__subscribers[topic.build()]:
                del self.__subscribers[topic.build()]

    def __notify_subscriber(self, topic: Topic, payload: bytes):
        if topic.build() in self.__subscribers:
            for observer in self.__subscribers[topic.build()]:
                logger.info(f"Notifying observer:{topic.build()}")
                observer.update(topic, payload)

    def loop(self):
        self.__mqtt_instance.loop_forever()
