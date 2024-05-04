from typing import Union

import fido_date


word = Union[int, None]
byte = Union[int, None]

def _year(Date: word) -> word:
    return ((Date & 0xFE00) >> 9) + 1980


def _month(Date: word) -> byte:
    return (Date & 0x01E0) >> 5


def _day(Date: word) -> byte:
    return Date & 0x001F


class Date:
    def __init__(self, day=1, month=1, year=1990):
        self.date = 0
        self.date = self.setdate(day, month, year)
        # print()

    @staticmethod
    def _year(date):
        return ((date & 0xFE00) >> 9) + 1990

    @staticmethod
    def _month(date):
        return (date & 0x01E0) >> 5

    @staticmethod
    def _day(Date):
        return Date & 0x001F

    def year(self):
        return self._year(self.date)

    def month(self):
        return self._month(self.date)

    def day(self):
        return self._day(self.date)

    def setyear(self, year):
        self.date &= ~0xFE00
        self.date ^= int((year - 1990)) << 9
        return self.date

    def year_(self):
        return int((self.date & 0xFE00) >> 9)

    def setmonth(self, month):
        if month > 12:
            self.setyear(self._year(self.date) + month // 12)
            month = month % 12 + 1
        self.date &= ~0x01E0
        self.date ^= month << 5
        return self.date

    def setday(self, day):
        self.date &= ~0x001F
        self.date ^= int(day)
        return self.date

    def setdate(self, day, month, year):
        self.setyear(year)
        self.setmonth(month)
        self.setday(day)
        return self.date

    def days(self):
        y = self.year_()
        return self.day() + fido_date.mofs[self.month() - 1] + y * 365 + (y + 3) // 4 + (
            0 if y % 4 != 0 else (1 if self.month() > 2 else 0))

    def __sub__(self, d):
        return self.days() - d.days()

    def __iadd__(self, d):
        self.date = self.dstodate(self.days() + d)
        return self.date

    def __isub__(self, d):
        self.date = self.dstodate(self.days() - d)
        return self.date

    def __eq__(self, other):
        return self.date == other.date

    def __ne__(self, other):
        return self.date != other.date

    def __lt__(self, other):
        return self.days() < other.days()

    def __le__(self, other):
        return self.days() <= other.days()

    def __gt__(self, other):
        return self.days() > other.days()

    def __ge__(self, other):
        return self.days() >= other.days()

    def weekday(self):
        return (self.days() + 7) % 7

    def daysinmonth(self):
        x = self.month()
        return 31 if x == 12 else (fido_date.mofs[x] - fido_date.mofs[x - 1])

    @staticmethod
    def dstodate(days):
        d = j = i = k = y = 0
        dt = Date()
        y = days // 365.25
        while (d := y * 365 + ((y + 3) // 4)) >= days:
            y -= 1
        d = days - d
        if y % 4 == 0:
            if d == fido_date.mofs[2] + 1:
                dt.setmonth(2)
                dt.setday(29)
                return dt.date
            elif d > fido_date.mofs[2]:
                d -= 1
        if d > fido_date.mofs[11]:
            k = 11
        else:
            i = 0
            j = 11
            while j > i + 1:
                k = (i + j) // 2
                if d > fido_date.mofs[k]:
                    i = k
                else:
                    j = k
            k = i
        dt.setmonth(k + 1)
        dt.setday(d - fido_date.mofs[k])
        dt.setyear(y + 1990)
        return dt.date

