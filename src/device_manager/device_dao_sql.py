from src.device_manager.device_dao_interface import DeviceDAOInterface
from src.config_manager import config_manager
import sqlite3


class DeviceDAOSQL(DeviceDAOInterface):
    __sqlite_con: sqlite3.Connection = None
    __sqlite_cur: sqlite3.Cursor = None

    def __init__(self):
        self.__sqlite_con = sqlite3.connect(config_manager["database"])
        self.__sqlite_cur = self.__sqlite_con.cursor()
        for x in self.get_all_devices():
            print(x)

    def get_device_by_id(self, unique_id: str):
        res = self.__sqlite_cur.execute(
            "SELECT * from device WHERE unique_id=?", [unique_id]
        )
        return res.fetchone()

    def get_all_devices(self):
        res = self.__sqlite_cur.execute("SELECT * from device")
        return res.fetchall()

    def add_device(
        self, unique_id: str, name: str, hardware_type: str, device_type: str
    ):
        self.__sqlite_cur.execute(
            "INSERT INTO device VALUES (?, ?, ?, ?)",
            [unique_id, name, hardware_type, device_type],
        )
        self.__sqlite_con.commit()

    def update_device(self, device):
        pass

    def delete_device(self, unique_id: str):
        pass
