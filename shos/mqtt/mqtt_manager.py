from paho.mqtt.client import Client, MQTTv5


class MQTTManager:
    __mqtt_instance: Client = None

    def __init__(self, client_id: str, broker: str, port: int) -> None:
        self.__mqtt_instance = Client(client_id=client_id, protocol=MQTTv5)
        self.__mqtt_instance.connect(host=broker, port=port)
        self.__mqtt_instance.on_connect = self.__on_connect

    @staticmethod
    def __on_connect(client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print(f"Failed to connect: {reason_code}. retrying")

    def subscribe(self, topic: str):
        return
