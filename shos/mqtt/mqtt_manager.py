from paho.mqtt.client import Client, MQTTv311, MQTTMessage, ConnectFlags
from paho.mqtt.enums import CallbackAPIVersion
from paho.mqtt.reasoncodes import ReasonCode
from paho.mqtt.properties import Properties, MQTTException
from loguru import logger
from shos.mqtt.topic_builder import Topic, TopicType


class MQTTManager:
    __mqtt_instance: Client = None

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
        self.__mqtt_instance.on_message = MQTTManager.__on_message

        self.__mqtt_instance.connect(host=broker, port=port)

    @staticmethod
    def __on_message(client: Client, userdata, msg: MQTTMessage):
        logger.debug(f"Received {msg.payload} from {msg.topic} topic")

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

    def publish(self, topic: Topic, payload: str):
        if topic.get_topic_type is TopicType.PUBLISHER:
            self.__mqtt_instance.publish(
                topic=topic,
                payload=payload,
                qos=0,
            )
        else:
            logger.error("Could not use a SUBSCRIBER topic as a publisher")
            raise MQTTException("Could not use a SUBSCRIBER topic as a publisher")

    def subscribe(self, topic: Topic):
        if topic.get_topic_type is TopicType.SUBSCRIBER:
            self.__mqtt_instance.subscribe(topic=topic)
        else:
            logger.error("Could not use a PUBLISHER topic as a subscriber")
            raise MQTTException("Could not use a PUBLISHER topic as a subscriber")

    @property
    def client(self):
        return self.__mqtt_instance
