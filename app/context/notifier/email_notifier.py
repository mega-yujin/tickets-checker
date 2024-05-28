import smtplib
import ssl

from pydantic import BaseModel

from app.context.notifier.abstract import Notifier


class EmailNotifierConfig(BaseModel):
    host: str
    port: int
    login: str
    password: str


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
