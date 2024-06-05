import smtplib
import ssl

from pydantic import BaseModel
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.api.check.models import NotificationChannelEnum
from app.context.checker.abstact import CheckResult, TicketsInfo
from app.context.notifier.abstract import Notifier


class EmailNotifierConfig(BaseModel):
    host: str
    port: int
    login: str
    password: str


class EmailNotifier(Notifier[EmailNotifierConfig]):
    notification_channel_name = NotificationChannelEnum.email
    POSITIVE_SUBJECT = 'Available tickets for the show "{show_name}"'
    NEGATIVE_SUBJECT = 'No available tickets for the show "{show_name}"'
    POSITIVE_TEXT = """
Congratulations! You can buy tickets for the show "{show_name}\"

Available dates:
{available_dates}
"""
    AVAILABLE_DATES = "* {date} - {tickets_num}\n"
    NEGATIVE_TEXT = "Unfortunately, you can't visit this show yet"

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

        if check_result.tickets_available:
            msg['Subject'] = self.POSITIVE_SUBJECT.format(
                show_name=check_result.show.show_name,
            )
            text = self.POSITIVE_TEXT.format(
                show_name=check_result.show.show_name,
                available_dates=self._generate_list_of_available_tickets(check_result.show.schedule),
            )
        else:
            msg['Subject'] = self.NEGATIVE_SUBJECT.format(
                show_name=check_result.show.show_name,
            )
            text = self.NEGATIVE_TEXT

        msg.attach(MIMEText(text, 'plain'))

        return msg.as_string()

    def _generate_list_of_available_tickets(self, schedule: list[TicketsInfo]) -> str:
        result_str = ''
        for show_date in schedule:
            result_str += self.AVAILABLE_DATES.format(
                date=str(show_date.date),
                tickets_num=show_date.tickets,
            )
        return result_str
