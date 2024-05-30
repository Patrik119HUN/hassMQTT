from src.config_manager.config_manager import ConfigManager
from pathlib import Path

CONFIG_FILE = (Path(__file__).parent / "../../config/config.json").resolve()

config_manager = ConfigManager(CONFIG_FILE)
