from typing import List
from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, updated_object) -> None:
        pass


class Subject:
    _observers: List[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, updated_object):
        for observer in self._observers:
            observer.update(updated_object)
