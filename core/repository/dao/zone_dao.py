from .dao_interface import DAOInterface
from core.device.hardware import Hardware
from core.utils.db_connect import connect
from typing import List, Dict


class ZoneDAO(DAOInterface[Hardware]):
    def __init__(self, path: str):
        super().__init__(path)

    def list(self) -> List[Dict[str, str]]:
        with connect(self._path) as cursor:
            cursor.execute("SELECT * from zones")
            return [elem for elem in cursor.fetchall()]

    def get(self, item_id: str) -> Dict[str, str]:
        with connect(self._path) as cursor:
            cursor.execute("SELECT * from zones where unique_id== ?", [item_id])
            return cursor.fetchone()

    def create(self, item) -> None:
        with connect(self._path) as cursor:
            cursor.execute(
                "INSERT INTO zones VALUES (?, ?)",
                [
                    item.unique_id,
                    item.zone_id,
                ],
            )

    def update(self, unique_id: str, item) -> int:
        with connect(self._path) as cursor:
            cursor.execute(
                "UPDATE zones SET zone_id=? WHERE unique_id=?",
                [item.zone_id, unique_id],
            )
            return cursor.rowcount > 0

    def delete(self, unique_id: str) -> int:
        with connect(self._path) as cursor:
            cursor.execute("DELETE FROM zones WHERE unique_id=?", [unique_id])
            return cursor.rowcount > 0
