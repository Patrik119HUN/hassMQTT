from abc import ABC, abstractmethod
from typing import List
from core.utils.observer_interface import IObserver


class ISubject(ABC):
    def __init__(self):
        self._observers: List[IObserver] = []

    def attach(self, observer: IObserver) -> None:
        self._observers.append(observer)

    def notify_observers(self, *args, **kwargs) -> None:
        for observer in self._observers:
            observer.update(self, *args, **kwargs)
