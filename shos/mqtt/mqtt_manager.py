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
        Prints a message when it fails to establish a connection, providing the
        reason code as additional information.

        Args:
            client (object.): Twython client instance used for API requests.
                
                	1/ `is_failure`: A boolean value indicating whether the connection
                attempt failed.
            userdata (str): additional data that can be provided to the `connect()`
                function to further customize its behavior.
            flags (int): 3-bit status flag returned by the operating system when
                a connection attempt fails, providing additional information about
                the failure reason.
            reason_code (str): error or failure cause of connecting to a remote system.
            properties (str): configuration properties of the connection, which
                are used to determine the error message when the connection fails.

        """
        if reason_code.is_failure:
            print(f"Failed to connect: {reason_code}. retrying")

    def subscribe(self, topic: str):
        """
        Is used to subscribe to a Firebase Realtime Database notification when a
        specific event occurs.

        Args:
            topic (str): topic or theme for which the generated documentation will
                be tailored.

        """
        return
