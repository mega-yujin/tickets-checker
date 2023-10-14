import json
from asyncio import sleep
from datetime import datetime
from typing import Union

from aiohttp import FormData, hdrs
from bs4 import BeautifulSoup
from pydantic import BaseModel

from app.context.checker.abstact import TicketsChecker, TicketsInfo, CheckResult, Show

SLEEP_TIME_SECONDS = 3


def _convert_date(date: str) -> datetime:
    """Convert str dates like "18 Октября, Среда, 19:00" to datetime"""

    month_map = {
        'Января': '01',
        'Февраля': '02',
        'Марта': '03',
        'Апреля': '04',
        'Мая': '05',
        'Июня': '06',
        'Июля': '07',
        'Августа': '08',
        'Сентября': '09',
        'Октября': '10',
        'Ноября': '11',
        'Декабря': '12',
    }

    date_elements = [item.replace(',', '') for item in date.split(' ')]
    date_elements[1] = month_map.get(date_elements[1])
    date_elements.pop(2)
    formatted_date = ' '.join(date_elements)
    return datetime.strptime(formatted_date, '%d %m %H:%M').replace(year=datetime.now().year)


def _get_date_id_from_link(link: str) -> str:
    """Get date_id from link"""
    return link.split('=')[-1]


class TicketsData(BaseModel):
    id: int
    pzone_id: int
    x: int
    y: int


class AvailableTickets(BaseModel):
    attr: bool
    data: Union[str, list[TicketsData]]
    hash: str
    success: bool


class PuppetTheatreChecker(TicketsChecker):
    theater = 'Белорусский государственный театр кукол'
    theatre_id = 'RkZDMTE2MUQtMTNFNy00NUIyLTg0QzYtMURDMjRBNTc1ODA0'
    host = 'puppet-minsk.com'
    tickets_shop_url = 'https://tce.by/index.php'

    def parse_page(self, page: str) -> Show:
        soup = BeautifulSoup(page, 'html.parser')
        show_name = soup.find('p', {'class': 'performance-title'}).text

        show_data = Show(theater=self.theater, show_name=show_name)

        schedule = soup.find_all('div', {'class': 'date-item'})
        for show in schedule:
            date = show.find_next('div', {'class': 'date-time'}).find('p').text
            link = show.find_next('div', {'class': 'performance-buy-ticket'}).find('a')['href']
            show_data.schedule.append(
                TicketsInfo(
                    date=_convert_date(date),
                    date_id=_get_date_id_from_link(link),  # type: ignore
                )
            )
        return show_data

    async def get_available_ticket(self, schedule: list[TicketsInfo]):
        for show in schedule:
            resp = await self._make_request(
                method=hdrs.METH_POST,
                url=self.tickets_shop_url,
                params={'view': 'shows', 'action': 'ticket', 'kind': 'json'},
                data=FormData({'server_key': self.theatre_id, 'bk_id': show.date_id})  # type: ignore  # TODO: !!
            )
            show.tickets = AvailableTickets(**json.loads(await resp.text()))
            await sleep(SLEEP_TIME_SECONDS)

    def analyze_result(self, show_data: Show) -> CheckResult:
        check_result = CheckResult(show=show_data)
        check_result.tickets_available = next(
            (True for show in show_data.schedule if show.tickets.success is True),
            False
        )
        return check_result
