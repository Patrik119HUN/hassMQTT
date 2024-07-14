from .dao_interface import DAOInterface
from core.device.hardware import Hardware
from core.device.entity import Entity
from core.utils.db_connect import connect
from typing import List


class HardwareDAO(DAOInterface[Hardware]):
    def __init__(self, path: str):
        super().__init__(path)

    def list(self) -> list[Hardware]:
        hw_list: List[Hardware] = []
        with connect(self._path) as cursor:
            cursor.execute("SELECT * from hardware")
            for elem in cursor.fetchall():
                elem.pop("unique_id", None)
                hw_list.append(Hardware(**elem))
        return hw_list

    def get(self, item_id: int) -> Hardware:
        with connect(self._path) as cursor:
            cursor.execute("SELECT * from hardware where unique_id== ?", [item_id])
            elem = cursor.fetchone()
            elem.pop("unique_id", None)
            return Hardware(**elem)

    def create(self, item: Entity) -> None:
        hardware: Hardware = Hardware("Raspberry")
        if item.hardware is not None:
            hardware = item.hardware

        with connect(self._path) as cursor:
            cursor.execute(
                "INSERT INTO hardware VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    hardware.name,
                    hardware.model,
                    hardware.manufacturer,
                    hardware.sw_version,
                    hardware.hw_version,
                    hardware.identifiers,
                    hardware.connections,
                    hardware.configuration_url,
                    hardware.via_device,
                    item.unique_id,
                ],
            )
        pass

    def update(self, unique_id: str, item: Hardware) -> int:
        with connect(self._path) as cursor:
            cursor.execute(
                "UPDATE hardware SET name = ?, model = ?, manufacturer = ?, sw_version = ?, hw_version = ?, "
                "identifiers = ?, connections = ?, configuration_url = ?, via_device = ? WHERE unique_id= ?",
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
                    unique_id,
                ],
            )
            return cursor.rowcount > 0

    def delete(self, unique_id: str) -> int:
        with connect(self._path) as cursor:
            cursor.execute("DELETE FROM hardware WHERE unique_id=?", [unique_id])
            return cursor.rowcount > 0
