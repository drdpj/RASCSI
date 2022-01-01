from abc import ABC, abstractmethod
from menu.menu import Menu
from rascsi_client import RaScsiClient


class MenuBuilder(ABC):

    def __init__(self, rascsi_client: RaScsiClient):
        self._rascsi_client = rascsi_client

    @abstractmethod
    def build(self, name: str) -> Menu:
        pass

    def get_rascsi_client(self):
        return self._rascsi_client

