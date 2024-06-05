from abc import ABC, abstractmethod


class IRepository[T](ABC):
    _path: str

    def __init(self, path: str):
        """
        Sets the value of the attribute `_path`.

        Args:
            path (str): full file path of the documentation that the function is
                supposed to generate, and it is used to determine the contents of
                the documentation output.

        """
        self._path = path

    @abstractmethod
    def get_all(self) -> list[T]:
        """
        Raises a `NotImplementedError` when it is called, indicating that the
        implementation for this function is not available or has not been provided.

        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, item_id: int) -> T:
        """
        Generates high-quality documentation for code that is given to it.

        Args:
            item_id (int): item ID of the instance being checked for compatibility
                with the provided configuration.

        """
        raise NotImplementedError

    @abstractmethod
    def create(self, item) -> None:
        """
        Is a generic method that does not have any implemented functionality and
        raises a `NotImplementedError`.

        Args:
            item (object reference of class `Item`.): item for which additional
                documentation is being generated.
                
                		- `id`: a unique identifier for the item (str)
                		- `name`: the name of the item (str)
                		- `description`: a brief description of the item (str)
                		- `type`: the type of the item (str)
                		- `tags`: a list of tags associated with the item (list[str])

        """
        raise NotImplementedError

    @abstractmethod
    def update(self, item: int, *args, **kwargs) -> None:
        """
        Updates the attributes of a class instance.

        Args:
            item (int): item being evaluated for the presence of the specified method.

        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, item_id: int) -> None:
        """
        Does not have any specified functionality, as it raises a `NotImplementedError`.

        Args:
            item_id (int): ID of the item being searched for in the database.

        """
        raise NotImplementedError
