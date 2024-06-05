from .repository_interface import IRepository
from src.device.hardware import Hardware
from src.utils.db_connect import connect


class HardwareRepository(IRepository[Hardware]):

    def get_all(self) -> list[Hardware]:
        with connect(self._path) as cursor:
            cursor.execute("SELECT * from hardware")
            return cursor.fetchall()

    def get_by_id(self, item_id: int) -> Hardware:
        with connect(self._path) as cursor:
            cursor.execute("SELECT * from hardware where hardware_id == ?", [item_id])
            return cursor.fetchone()

    def create(self, item) -> None:
        pass

    def update(self, item: int, *args, **kwargs) -> None:
        pass

    def delete(self, item_id: int) -> None:
        pass
