from .repository_interface import IRepository
from core.device.hardware import Hardware
from core.utils.db_connect import connect
from typing import List, Dict


class DeviceDriverRepository(IRepository[Hardware]):

    def __init__(self, path: str):
        super().__init__(path)

    def list(self) -> List[Dict[str, str]]:
        with connect(self._path) as cursor:
            cursor.execute("SELECT * from device_driver")
            return [elem for elem in cursor.fetchall()]

    def get(self, item_id: str) -> Dict[str, str | int]:
        with connect(self._path) as cursor:
            cursor.execute("SELECT * from device_driver where unique_id== ?", [item_id])
            return cursor.fetchone()

    def create(self, item) -> None:
        with connect(self._path) as cursor:
            cursor.execute(
                "INSERT INTO device_driver VALUES (?, ?, ?)",
                [
                    item["unique_id"],
                    item["driver"],
                    item["address"],
                ],
            )
        pass

    def update(self, item: int, *args, **kwargs) -> None:
        pass

    def delete(self, item_id: int) -> None:
        pass
