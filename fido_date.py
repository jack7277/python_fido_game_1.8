from datetime import date, datetime, timedelta
from calendar import monthrange


week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
month = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
         "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь", None]


class Date:
    def __init__(self, day=1, month=1, year=1990):
        self.date = date(year, month, day)

    def year(self):
        return self.date.year

    def month(self):
        return self.date.month

    def day(self):
        return self.date.day

    def setyear(self, year):
        self.date = self.date.replace(year=year)
        # self.date = Date(new_date.day, new_date.month, new_date.year)

    def setmonth(self, month):
        if month > 12:
            self.setyear(self.year() + month // 12)
            month = month % 12 + 1
        self.date = self.date.replace(month=month)
        # self.date = Date(new_date.day, new_date.month, new_date.year)

    def setday(self, day):
        self.date = self.date.replace(day=day)
        # self.date = Date(new_date.day, new_date.month, new_date.year)

    def setdate(self, day, month, year):
        self.setyear(year)
        self.setmonth(month)
        self.setday(day)

    def __sub__(self, d):
        new_date = self.date - timedelta(days=d)
        return Date(new_date.day, new_date.month, new_date.year)

    def __isub__(self, d):
        new_date = self.date - timedelta(days=d)
        return Date(new_date.day, new_date.month, new_date.year)

    def __add__(self, d):
        new_date = self.date + timedelta(days=d)
        return Date(new_date.day, new_date.month, new_date.year)

    def __iadd__(self, d):
        new_date = self.date + timedelta(days=d)
        return Date(new_date.day, new_date.month, new_date.year)

    def __eq__(self, d):
        return self.date == d

    # def __lt__(self, d):
    #     return self.days() < d

    def weekday(self):
        return week[self.date.weekday()]

    def daysinmonth(self):
        x = monthrange(self.year(), self.month())
        return x[1]


def getcurdate():
    now = datetime.now()
    d = now.day
    m = now.month
    y = now.year
    d = Date(d, m, y)
    return d


if __name__ == '__main__':
    # Example usage
    D = getcurdate()
    print(f"{D.day()}.{D.month()}.{D.year()}")
    print(D.weekday())
    print(D.daysinmonth())
    D += 4 * 365
    d = D.day()
    m = D.month()
    y = D.year()
    print(f"{D.day()}.{D.month()}.{D.year()}")
    # you = Person()
    # you.grad.setdate(D.day(), D.month()+3, D.year())
    # print(f"{you.grad.day()}.{you.grad.month()}.{you.grad.year()}")
