from src.repository.repository_interface import IRepository
import sqlite3
from typing import List
from src.device.entity import Entity
from src.utils.db_connect import connect
from .hardware_repository import HardwareRepository


class EntityRepository(IRepository[Entity]):

    def __init__(self, path: str, harware_repo: HardwareRepository):
        """
        Sets up the necessary variables and instances for a class, including the
        `hardware_repo` instance variable, which holds a reference to an external
        hardware repository.

        Args:
            path (str): directory where the hardware repository will be initialized
                and stored, which is then passed to the superclass `__init__`
                method for further initialization.
            harware_repo (HardwareRepository): repository containing the hardware
                files that are being initialized and used by the class.

        """
        super().__init__(path)
        self.__hardware_repo = harware_repo

    def get_all(self) -> list[Entity]:
        """
        Retrieves a list of entities from a database using a SQL query, then creates
        an Entity object for each entity in the result set and adds it to a list.
        The resulting list of Entities is returned.

        Returns:
            list[Entity]: a list of `Entity` objects containing information about
            entities in the database.

        """
        entity_list: List[Entity] = []
        with connect(self._path) as cursor:
            cursor.row_factory = sqlite3.Row
            cursor.execute("SELECT * from entity")
            for entity in cursor.fetchall():
                hardware = self.__hardware_repo.get_by_id(entity["hardware_id"])
                entity_list.append(
                    Entity(
                        name=entity["name"],
                        device=hardware,
                        device_class=entity["entity_type"],
                        icon=entity["icon"],
                        unique_id=entity["unique_id"],
                    )
                )
            return entity_list

    def get_by_id(self, item_id: int) -> Entity:
        """
        Retrieves a single entity from a SQLite database based on its unique ID,
        and returns an Entity object containing its name, device, device class,
        icon, and unique ID.

        Args:
            item_id (int): 3D entity ID in the database for which the function
                retrieves information from the entity table.

        Returns:
            Entity: an `Entity` object containing information from the database.

        """
        with connect(self._path) as cursor:
            cursor.row_factory = sqlite3.Row
            cursor.execute("SELECT * from entity")
            entity = cursor.fetchone()
            hardware = self.__hardware_repo.get_by_id(entity["hardware_id"])
            return Entity(
                name=entity["name"],
                device=hardware,
                device_class=entity["entity_type"],
                icon=entity["icon"],
                unique_id=entity["unique_id"],
            )

    def create(self, item: Entity) -> None:
        """
        Inserts data into an entity table using a parameterized query with positional
        arguments and keyword arguments for more efficient and secure database operations.

        Args:
            item (Entity): data to be inserted into the database table.

        """
        with connect(self._path) as cursor:
            cursor.execute(
                "INSERT INTO entity VALUES (?, ?, ?, ?, ?,?)",
                [
                    item.unique_id,
                    item.name,
                    item.driver.__class__.__name__,
                    item.device_class,
                    1,
                    item.icon,
                ],
            )

    def update(self, item: int, *args, **kwargs) -> None:
        """
        Updates a given model's data by passing it through a transformation function,
        which modifies the original data based on the input provided.

        Args:
            item (int): item that is being manipulated or operated on by the function.

        """
        pass

    def delete(self, item_id: int) -> None:
        """
        Deletes a specific node from a linked list.

        Args:
            item_id (int): unique identifier of an item that is being passed through
                the function for processing.

        """
        pass
