from datetime import datetime
from bs4 import BeautifulSoup, Tag

from app.context.checker.abstact import TicketsChecker, Schedule, ScheduleWithTickets, CheckResult, PlayInfo


def _convert_date(date: str) -> datetime:
    """Convert str dates like "18 Октября, Среда, 19:00" to datetime"""

    month_list = (
        'Января',
        'Февраля',
        'Марта',
        'Апреля',
        'Мая',
        'Июня',
        'Июля',
        'Августа',
        'Сентября',
        'Октября',
        'Ноября',
        'Декабря',
    )



    datetime.strptime(date, '%d %B, %A, %H:%M')
    pass


def _get_date_id_from_link(link: str) -> str:
    """Get date_id from link"""

    pass


class PuppetTheatreChecker(TicketsChecker):
    host = 'puppet-minsk.com'
    tickets_shop = 'https://tce.by/shows.html'
    theatre_id = 'RkZDMTE2MUQtMTNFNy00NUIyLTg0QzYtMURDMjRBNTc1ODA0'

    def parse_page(self, page: str) -> Schedule:
        result = Schedule()
        soup = BeautifulSoup(page, 'html.parser')
        table = soup.find_all('div', {'class': 'date-item'})
        for item in table:
            date = item.find_next('div', {'class': 'date-time'}).find('p').text
            link = item.find_next('div', {'class': 'performance-buy-ticket'}).find('a')['href']
            result.plays.append(
                PlayInfo(
                    date=_convert_date(date),
                    date_id=_get_date_id_from_link(link)
                )
            )
        return result

    def get_available_ticket(self, schedule: Schedule) -> ScheduleWithTickets:
        pass

    def analyze_result(self, schedule: ScheduleWithTickets) -> CheckResult:
        pass
