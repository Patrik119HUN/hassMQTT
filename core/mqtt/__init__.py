from .mqtt_manager import MQTTManager
from .topic import Topic
from core.config_manager import config_manager

mqtt_manager = MQTTManager(**config_manager["mqtt"])
