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
        """
        Updates the latest data for a user based on their ID and other inputs.

        Args:
            topic (Topic): topic that is being passed through the transformation
                function for analysis or processing.
            payload (bytes): data to be sent with the request.

        """
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
        logger.info(
            f"MQTT manager connected to:{broker}:{port} with username:{username}"
        )

    def __on_message(self, client: Client, userdata, msg: MQTTMessage):
        """
        Processes a message received from a message queue and sends it to an output
        topic, logs the message to debug for later analysis, decodes the message
        payload from a binary message format, converts the `TopicType` into a
        `StringToTopic` object, builds and subscribes to a topic, and notifies the
        topic of the received message.

        Args:
            client (Client): MQTT client that sent the message.
            userdata (str): payload of the message, which is a JSON-formatted
                string that contains the data to be processed by the function.
            msg (MQTTMessage): message being processed in the function, containing
                the encoded payload in UTF-8 format and the topic name for subscribers.

        """
        message = msg.payload.decode("utf-8")
        topic = StringToTopic(TopicType.SUBSCRIBER, msg.topic).build()
        self.notify(topic, msg.payload)
        logger.debug(f"Received {message} from {msg.topic} topic")

    @staticmethod
    def __on_connect(
        client: Client,
        userdata,
        flags: ConnectFlags,
        reason_code: ReasonCode,
        property: Properties,
    ):
        """
        Retries the connection if there is an error, otherwise it logs the reason
        for the failure with a corresponding debug message.

        Args:
            client (Client): object that will be used to connect to the server and
                execute the given operation.
            userdata (object/instance of the `Any` type.): additional data that
                accompanies the API request and is available to the API endpoint
                being called.
                
                	1/ `reason_code`: This is a property that represents an object
                with different attributes representing the reason for connection
                failure. The value of this property can be a string or an integer.
            flags (ConnectFlags): error reason code, which is used to determine
                whether the connection was successful or failed and what additional
                information to log when retrying the connection.
            reason_code (ReasonCode): error reason code received from the API,
                which is debugged or error-reported in the function depending on
                its value.
            property (Properties): reason for the failure to connect, which is
                used to determine whether to retry or log the reason for the failure.

        """
        if reason_code.is_failure:
            logger.error(f"Failed to connect: {reason_code}. retrying")
        else:
            logger.debug(reason_code.getName())

    def publish(self, topic: Topic, payload: str | bytes | bytearray | float | None):
        """
        Takes a `topic` and `payload`, sets `qos` to zero, and publishes the message
        to the MQTT broker based on the specified `topic.get_topic_type()` value.

        Args:
            topic (Topic): topic object to which the payload will be published.
            payload (str | bytes | bytearray | float | None): message to be published
                to the MQTT topic.

        """
        if topic.get_topic_type is TopicType.PUBLISHER:
            self.__mqtt_instance.publish(
                topic=topic.build(),
                payload=payload,
                qos=0,
            )
        else:
            logger.error("Could not use a SUBSCRIBER topic as a publisher")
            raise MQTTException("Could not use a SUBSCRIBER topic as a publisher")

    def subscribe(self, topic: Topic):
        """
        Checks the topic type and subscribe to the appropriate MQTT topic if it
        is a subscriber, or raise an exception otherwise.

        Args:
            topic (Topic): MQTT topic for which the client will subscribe or publish
                data, and is used to construct the corresponding MQTT message.

        """
        if topic.get_topic_type is TopicType.SUBSCRIBER:
            self.__mqtt_instance.subscribe(topic=topic.build())
            logger.info(f"Client subscribed to:{topic.build()}")
        else:
            logger.error("Could not use a PUBLISHER topic as a subscriber")
            raise MQTTException("Could not use a PUBLISHER topic as a subscriber")

    def add_subscriber(self, topic: Topic, observer: TopicObserver):
        """
        Adds an observer to a list of subscribers for a specific topic, storing
        the new observer in the topic's subscription list if it is not already
        present and increasing its length by one.

        Args:
            topic (Topic): Topic object that is being subscribed to and is used
                to add or update the subscription details in the internal cache
                of the ObserverManager instance.
            observer (TopicObserver): observer object that is being added to the
                subscription list for the given topic.

        """
        logger.info(f"Client subscribed to:{topic.build()}")
        if topic.build() not in self.__subscribers:
            self.__subscribers[topic.build()] = []
        self.__subscribers[topic.build()].append(observer)

    def remove_observ(self, topic: Topic, observer: TopicObserver):
        """
        Removes observer from specific topics' list of subscribers.

        Args:
            topic (Topic): topic for which the observer is to be removed or deleted,
                allowing the function to properly manage the subscribers for each
                topic.
            observer (TopicObserver): observer to be removed from the subscription
                list, which is then removed from the associated topic's subscription
                list and deleted if there are no remaining subscribers for that topic.

        """
        if topic in self.__subscribers:
            self.__subscribers[topic.build()].remove(observer)
            if not self.__subscribers[topic.build()]:
                del self.__subscribers[topic.build()]

    def notify(self, topic: Topic, payload: bytes):
        """
        Is a centralized mechanism for sending notifications to observers in a
        Reactive framework. It takes a topic and a payload as input and loops over
        the observers registered for that topic, calling the `update` method on
        each one with the updated topic and payload.

        Args:
            topic (Topic): topic being notified, which is used to determine the
                observers to notify.
            payload (bytes): data that will be passed to the observers when notified.

        """
        if topic.build() in self.__subscribers:
            for observer in self.__subscribers[topic.build()]:
                logger.info(f"Notifying observer:{topic.build()}")
                observer.update(topic, payload)

    def loop(self):
        """
        Loops endlessly

        """
        self.__mqtt_instance.loop_forever()

    @property
    def client(self):
        """
        Generates high-quality documentation for given code by providing a reference
        to its instance of an MQTT client.

        Returns:
            instance of `paho.mqtt.client.Client: a reference to the instance of
            the MQTT client.
            
            		- `self`: This is an instance of the `MqttClient` class, which
            represents the MQTT client used to communicate with the MQTT broker.
            		- `__mqtt_instance`: This is a property that contains the actual
            MQTT client object, which can be accessed and manipulated as needed.

        """
        return self.__mqtt_instance
