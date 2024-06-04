import smtplib
import ssl

from pydantic import BaseModel, ConfigDict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

from app.api.check.models import NotificationChannelEnum
from app.context.checker.abstact import CheckResult
from app.context.notifier.abstract import Notifier


class EmailNotifierConfig(BaseModel):
    host: str
    port: int
    login: str
    password: str

    model_config = ConfigDict(arbitrary_types_allowed=True)


class EmailNotifier(Notifier[EmailNotifierConfig]):
    notification_channel_name = NotificationChannelEnum.email

    def __init__(self, config):
        super().__init__(config)
        self._context = ssl.create_default_context()

    def send_notifications(self, receivers: tuple[str, ...], check_result: CheckResult):
        with smtplib.SMTP_SSL(
            host=self._config.host,
            port=self._config.port,
            context=self._context,
        ) as server:
            server.login(self._config.login, self._config.password)
            for receiver in receivers:
                server.sendmail(self._config.login, receiver, self._generate_message(check_result))

    def _generate_message(self, check_result: CheckResult) -> str:
        msg = MIMEMultipart('alternative')

        msg['From'] = ...
        msg['Date'] = formatdate()
        msg['Subject'] = ...

        text = ...

        msg.attach(MIMEText(..., 'plain'))

        return msg.as_string()
