from .dao_interface import DAOInterface
from core.device.hardware import Hardware
from core.utils.db_connect import connect
from typing import List, Dict
from core.device.entity import Entity


class DeviceDriverDAO(DAOInterface[Hardware]):

    def __init__(self, path: str):
        super().__init__(path)

    def list(self) -> List[Dict[str, str]]:
        with connect(self._path) as cursor:
            cursor.execute("SELECT * from device_driver")
            return [elem for elem in cursor.fetchall()]

    def get(self, unique_id: str) -> Dict[str, str | int]:
        with connect(self._path) as cursor:
            cursor.execute("SELECT * from device_driver where unique_id== ?", [unique_id])
            return cursor.fetchone()

    def create(self, item: Entity) -> None:
        with connect(self._path) as cursor:
            cursor.execute(
                "INSERT INTO device_driver VALUES (?, ?, ?)",
                [
                    item.unique_id,
                    item.driver.__class__.__name__,
                    item.driver.get_address(),
                ],
            )

    def update(self, unique_id: str, item) -> int:
        with connect(self._path) as cursor:
            cursor.execute(
                "UPDATE device_driver SET driver=?, address=? WHERE unique_id=?",
                [item.driver, item.address, unique_id],
            )
            return cursor.rowcount > 0

    def delete(self, unique_id: str) -> int:
        with connect(self._path) as cursor:
            cursor.execute("DELETE FROM device_driver WHERE unique_id=?", [unique_id])
            return cursor.rowcount > 0
