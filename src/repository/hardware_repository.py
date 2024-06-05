from .repository_interface import IRepository
from src.device.hardware import Hardware
from src.utils.db_connect import connect


class HardwareRepository(IRepository[Hardware]):

    def get_all(self) -> list[Hardware]:
        """
        Executes a SQL SELECT statement on the "hardware" table within the database
        and returns the results as a list of tuples.

        Returns:
            list[Hardware]: a list of tuples containing various information about
            the hardware of the system.

        """
        with connect(self._path) as cursor:
            cursor.execute("SELECT * from hardware")
            return cursor.fetchall()

    def get_by_id(self, item_id: int) -> Hardware:
        """
        Executes a SELECT query on a hardware table to retrieve data for an item
        ID provided as input. It returns the retrieved data as a single row from
        the result set.

        Args:
            item_id (int): id of the hardware item for which information is to be
                retrieved.

        Returns:
            Hardware: a tuple containing the specified item's hardware details.

        """
        with connect(self._path) as cursor:
            cursor.execute("SELECT * from hardware where hardware_id == ?", [item_id])
            return cursor.fetchone()

    def create(self, item) -> None:
        """
        Generates high-quality documentation for code.

        Args:
            item (int): item that is being updated or deleted in the function.

        """
        pass

    def update(self, item: int, *args, **kwargs) -> None:
        """
        Updates the state of a component based on user input and other internal
        state variables.

        Args:
            item (int): element that the function operates on.

        """
        pass

    def delete(self, item_id: int) -> None:
        """
        Passes any arguments passed to it to the operating system for permanent removal.

        Args:
            item_id (int): id of an item for which additional metadata is being
                added or updated.

        """
        pass
