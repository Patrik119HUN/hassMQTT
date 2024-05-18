from paho.mqtt.client import Client, MQTTv5


class MQTTManager:
    __mqtt_instance: Client = None

    def __init__(self, client_id: str, broker: str, port: int) -> None:
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
        self.__mqtt_instance = Client(client_id=client_id, protocol=MQTTv5)
        self.__mqtt_instance.connect(host=broker, port=port)
        self.__mqtt_instance.on_connect = self.__on_connect

    @staticmethod
    def __on_connect(client, userdata, flags, reason_code, properties):
        """
        Prints a message and retries the connection process if there is an error
        connecting to the target device.

        Args:
            client (object/instance of class `Client`.): client that is being
                connected to.
                
                		- `is_failure`: a boolean value indicating whether the connection
                attempt failed or not
            userdata (str): data associated with the connection attempt that failed,
                which is used to determine the cause of failure and retry the
                connection if necessary.
            flags (enumeration or flag-value type, as specified in the given code
                snippet.): 3-bit flags that provide additional information about
                the failure, with each bit setting the corresponding flag:
                `reason_code` (bits 0-2), `error_message` (bit 3), and `retry`
                (bit 4).
                
                		- `is_failure`: Indicates whether the connection attempt was
                unsuccessful (`True`) or successful (`False`).
            reason_code (str): reason for failure to connect when it is set as `True`.
            properties (str): dictionary containing the credentials of the user
                that are needed to connect to the service.

        """
        if reason_code.is_failure:
            print(f"Failed to connect: {reason_code}. retrying")

    def subscribe(self, topic: str):
        """
        Takes a string `topic`, an optional `callback` function, and an `optionalContext`
        as input and subscribes the callback function to the given topic.

        Args:
            topic (str): topic or subject matter of the generated documentation.

        """
        return
