import paho.mqtt.client as mqtt
from paho.mqtt.enums import MQTTProtocolVersion
from config_manager import ConfigManager


class MQTTManager:
    _instance = None
    _mqtt_instance: mqtt.Client = None
    _cm = ConfigManager("../config.json")

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(MQTTManager, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        _client_id = self._cm["MQTT"]["client_id"]
        _broker = self._cm["MQTT"]["broker"]
        _port = self._cm["MQTT"]["port"]

        self._mqtt_instance = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=_client_id,
            protocol=MQTTProtocolVersion.MQTTv5,
        )
        self._mqtt_instance.connect(host=_broker, port=_port)
        self._mqtt_instance.on_connect = self._on_connect

    def _on_connect(client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print(f"Failed to connect: {reason_code}. retrying")

    def subscribe(self, topic: str):
        return
