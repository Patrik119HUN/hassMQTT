import paho.mqtt.client as mqtt
from paho.mqtt.enums import MQTTProtocolVersion


class MQTTManager:
    __mqtt_instance: mqtt.Client = None

    def __init__(self, client_id: str, broker: str, port: int) -> None:
        self._mqtt_instance = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=client_id,
            protocol=MQTTProtocolVersion.MQTTv5,
        )
        self._mqtt_instance.connect(host=broker, port=port)
        self._mqtt_instance.on_connect = self.__on_connect

    @staticmethod
    def __on_connect(client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print(f"Failed to connect: {reason_code}. retrying")

    def subscribe(self, topic: str):
        return
