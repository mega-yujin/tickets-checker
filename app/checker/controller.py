from app.checker.models import CheckRequest


class Controller:

    def check_tickets(self, req: CheckRequest):
        print(f'request: {req}')
