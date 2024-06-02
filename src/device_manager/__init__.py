from src.device_manager.device_manager import DeviceManager
from src.device_manager.device_dao_sql import DeviceDAOSQL

device_dao_sql: DeviceDAOSQL = DeviceDAOSQL()
device_manager: DeviceManager = DeviceManager(device_dao=device_dao_sql)
