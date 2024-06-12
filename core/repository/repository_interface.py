from abc import ABC, abstractmethod


class IRepository[T](ABC):
    _path: str

    def __init__(self, path: str):
        self._path = path

    @abstractmethod
    def list(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def get(self, item_id: int) -> T:
        raise NotImplementedError

    @abstractmethod
    def create(self, item) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, item: int, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, item_id: int) -> None:
        raise NotImplementedError
