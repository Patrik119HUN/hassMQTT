from .mqtt_manager import MQTTManager
from .topic_builder import Topic
from src.config_manager import config_manager

mqtt_manager = MQTTManager(**config_manager["mqtt"])
