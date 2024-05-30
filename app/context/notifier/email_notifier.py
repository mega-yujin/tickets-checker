import smtplib
import ssl
from typing import Union

from dependency_injector.providers import ConfigurationOption
from pydantic import BaseModel, ConfigDict

from app.context.notifier.abstract import Notifier


class EmailNotifierConfig(BaseModel):
    host: Union[str, ConfigurationOption]
    port: Union[int, ConfigurationOption]
    login: Union[str, ConfigurationOption]
    password: Union[str, ConfigurationOption]

    model_config = ConfigDict(arbitrary_types_allowed=True)


class EmailNotifier(Notifier[EmailNotifierConfig]):
    def __init__(self, config):
        super().__init__(config)
        self._context = ssl.create_default_context()

    def send_notifications(self, receivers: tuple[str, ...]):
        with smtplib.SMTP_SSL(
                host=self._config.host,
                port=self._config.port,
                context=self._context,
        ) as server:
            server.login(self._config.login, self._config.password)
            for receiver in receivers:
                server.sendmail(self._config.login, receiver, ...)

    def _generate_template(self):
        pass
