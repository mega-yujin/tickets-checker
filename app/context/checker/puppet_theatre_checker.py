from bs4 import BeautifulSoup

from app.context.checker.abstact import TicketsChecker, Schedule, ScheduleWithTickets, CheckResult, PlayInfo

from datetime import datetime


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

    splitted_date = [item.replace(',', '') for item in date.split(' ')]
    splitted_date[1] = month_map.get(splitted_date[1])
    splitted_date.pop(2)
    formatted_date = ' '.join(splitted_date)
    return datetime.strptime(formatted_date, '%d %m %H:%M').replace(year=datetime.now().year)


def _get_date_id_from_link(link: str) -> str:
    """Get date_id from link"""
    return link.split('=')[-1]


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
