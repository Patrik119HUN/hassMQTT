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
        """
        Records information in a specified log topic based on a given message payload.

        Args:
            client (Client): MQTT client that sent the message.
            userdata (str): additional data that is provided to the `logger.debug()`
                function beyond the `msg.payload`.
            msg (MQTTMessage): message object that contains information about the
                topic and payload of the message received, which is passed to the
                `debug()` function for logging.

        """
        logger.debug(f"Received {msg.payload} from {msg.topic} topic")

    @staticmethod
    def __on_connect(
        client: Client,
        userdata,
        flags: ConnectFlags,
        reason_code: ReasonCode,
        property: Properties,
    ):
        """
        Checks whether it was unable to connect and, if so, retries the connection
        process. Otherwise, it logs a message indicating the reason for failure
        in debug mode.

        Args:
            client (Client): Amazon API Gateway client that is used to interact
                with the AWS Service.
            userdata (str): additional data that is provided to the connected
                client, as specified by the reason code returned by the connection
                attempt.
            flags (ConnectFlags): failure reason code of the API call, and it is
                used to log the error message accordingly.
            reason_code (ReasonCode): reason for the failure to connect to the
                server, and its value is passed to the `logger` function to provide
                additional error information.
            property (Properties): reason for the failure to connect, and it is
                used to log the name of the reason in debug mode when the connection
                fails.

        """
        if reason_code.is_failure:
            logger.error(f"Failed to connect: {reason_code}. retrying")
        else:
            logger.debug(reason_code.getName())

    def publish(self, topic: Topic, payload: str):
        """
        Allows an object to publish data on a given MQTT topic. The function takes
        the topic, payload, and Quality Of Service (QOS) as inputs, and based on
        the `topic.get_topic_type`, either publishes the data or raises an exception
        if the input is not valid.

        Args:
            topic (Topic): MQTT topic that the function will send a message to or
                publish on, with possible values including PUBLISHER and SUBSCRIBER
                topics.
            payload (str): data that is sent to the MQTT broker when publishing a
                message using the specified `topic`.

        """
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
        """
        Determines if the given topic is a publisher or subscribe one and takes
        the appropriate action to connect to an MQTT broker.

        Args:
            topic (Topic): MQTT topic for which subscription is to be performed.

        """
        if topic.get_topic_type is TopicType.SUBSCRIBER:
            self.__mqtt_instance.subscribe(topic=topic)
        else:
            logger.error("Could not use a PUBLISHER topic as a subscriber")
            raise MQTTException("Could not use a PUBLISHER topic as a subscriber")

    @property
    def client(self):
        """
        Generates high-quality documentation for code that is passed to it, using
        the provided MQTT client instance.

        Returns:
            MqttClient` object: a reference to an instance of the `mosq.Client` class.
            
            		- `mqtt_instance`: A reference to the MQTT instance object, which
            can be used to send and receive messages in the MQTT broker.

        """
        return self.__mqtt_instance
