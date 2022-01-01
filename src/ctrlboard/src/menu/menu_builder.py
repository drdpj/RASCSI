from abc import ABC, abstractmethod


class MenuBuilder(ABC):

    @abstractmethod
    def build(self, name: str) -> None:
        pass
