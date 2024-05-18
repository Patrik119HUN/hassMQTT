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
        if reason_code.is_failure:
            print(f"Failed to connect: {reason_code}. retrying")

    def subscribe(self, topic: str):
        return
