from core.config_manager.config_manager import ConfigManager
from pathlib import Path

CONFIG_FILE = (Path(__file__).parent / "../../config/config.json").resolve()
MQTTDOTENV_FILE = (Path(__file__).parent / "../../config/.env.mqtt").resolve()

config_manager = ConfigManager(CONFIG_FILE)
config_manager.load_env("mqtt", MQTTDOTENV_FILE)
