from abc import ABC, abstractmethod


class DAOInterface[T](ABC):
    _path: str

    def __init__(self, path: str):
        self._path = path

    @abstractmethod
    def list(self) -> list[T]:
        raise NotImplementedError

    @abstractmethod
    def get(self, unique_id: str) -> T:
        raise NotImplementedError

    @abstractmethod
    def create(self, item) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, unique_id: str | int, item) -> int:
        raise NotImplementedError

    @abstractmethod
    def delete(self, unique_id: str | int) -> int:
        raise NotImplementedError
