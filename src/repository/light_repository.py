from .repository_interface import IRepository
from src.device.hardware import Hardware
from src.utils.db_connect import connect
from typing import List, Dict


class LightRepository(IRepository[Hardware]):

    def __init__(self, path: str):
        super().__init__(path)

    def list(self) -> List[Dict[str, str]]:
        with connect(self._path) as cursor:
            cursor.execute("SELECT * from light")
            return [elem for elem in cursor.fetchall()]

    def get(self, item_id: str) -> Dict[str, str]:
        with connect(self._path) as cursor:
            cursor.execute("SELECT * from light where device_id== ?", [item_id])
            return cursor.fetchone()

    def create(self, item) -> None:
        with connect(self._path) as cursor:
            cursor.execute(
                "INSERT INTO light VALUES (?, ?)",
                [
                    item["unique_id"],
                    item["color_mode"],
                ],
            )
        pass

    def update(self, item: int, *args, **kwargs) -> None:
        pass

    def delete(self, item_id: int) -> None:
        pass
