from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from pydantic import BaseModel

C = TypeVar("C", bound=BaseModel)


class Notifier(Generic[C], ABC):
    def __init__(self, config: C):
        self._config = config

    @abstractmethod
    def send_notifications(self, receivers: tuple[str, ...]):
        """Implements a sending notifications method"""
