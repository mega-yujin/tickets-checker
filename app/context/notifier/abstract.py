from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from pydantic import BaseModel

from app.api.check.models import NotificationChannelEnum
from app.context.checker.abstact import CheckResult

C = TypeVar("C", bound=BaseModel)


class Notifier(Generic[C], ABC):
    notification_channel_name: NotificationChannelEnum

    def __init__(self, config: C):
        self._config = config

    @abstractmethod
    def send_notifications(self, receivers: tuple[str, ...], check_result: CheckResult):
        """Implements a sending notifications method"""
