from .repository_interface import IRepository
from core.device.hardware import Hardware
from core.utils.db_connect import connect
from typing import List


class HardwareRepository(IRepository[Hardware]):

    def __init__(self, path: str):
        super().__init__(path)

    def list(self) -> list[Hardware]:
        hw_list: List[Hardware] = []
        with connect(self._path) as cursor:
            cursor.execute("SELECT * from hardware")
            for elem in cursor.fetchall():
                elem.pop("hardware_id", None)
                hw_list.append(Hardware(**elem))
        return hw_list

    def get(self, item_id: int) -> Hardware:
        with connect(self._path) as cursor:
            cursor.execute("SELECT * from hardware where hardware_id == ?", [item_id])
            elem = cursor.fetchone()
            elem.pop("hardware_id", None)
            return Hardware(**elem)

    def create(self, item: Hardware) -> None:
        with connect(self._path) as cursor:
            cursor.execute(
                "INSERT INTO hardware VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    item.name,
                    item.model,
                    item.manufacturer,
                    item.sw_version,
                    item.hw_version,
                    item.identifiers,
                    item.connections,
                    item.configuration_url,
                    item.via_device,
                ],
            )
        pass

    def update(self, item: int, *args, **kwargs) -> None:
        pass

    def delete(self, item_id: int) -> None:
        pass
