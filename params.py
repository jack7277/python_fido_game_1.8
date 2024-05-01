from datetime import datetime

mofs = [
    0,
    31,
    31 + 28,
    31 + 28 + 31,
    31 + 28 + 31 + 30,
    31 + 28 + 31 + 30 + 31,
    31 + 28 + 31 + 30 + 31 + 30,
    31 + 28 + 31 + 30 + 31 + 30 + 31,
    31 + 28 + 31 + 30 + 31 + 30 + 31 + 31,
    31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30,
    31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31,
    31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30,
]

class Date:
    def __init__(self, day=1, month=1, year=1990):
        self.date = 0
        self.date = self.setdate(day, month, year)
        # print()

    def _year(self, date):
        return ((date & 0xFE00) >> 9) + 1990

    def _month(self, date):
        return (date & 0x01E0) >> 5

    def _day(self, Date):
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
        return self.day() + mofs[self.month() - 1] + y * 365 + (y + 3) // 4 + (
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
        return 31 if x == 12 else (mofs[x] - mofs[x - 1])

    @staticmethod
    def dstodate(days):
        d=j=i=k=y= 0
        dt = Date()
        y = days // 365.25
        while (d := y * 365 + ((y + 3) // 4)) >= days:
            y -= 1
        d = days - d
        if y % 4 == 0:
            if d == mofs[2] + 1:
                dt.setmonth(2)
                dt.setday(29)
                return dt.date
            elif d > mofs[2]:
                d -= 1
        if d > mofs[11]:
            k = 11
        else:
            i = 0
            j = 11
            while j > i + 1:
                k = (i + j) // 2
                if d > mofs[k]:
                    i = k
                else:
                    j = k
            k = i
        dt.setmonth(k + 1)
        dt.setday(d - mofs[k])
        dt.setyear(y + 1990)
        return dt.date


def getcurdate():
    now = datetime.now()
    d = now.day
    m = now.month
    y = now.year
    d = Date(d, m, y)
    return d

style = ["Read-only", "Неактивный", "Активный", "Flame", None]
prob = [0, 1, 4, 8]  # вероятность [+] в % как f(Style) при izverg==1
lstscn = Date()
newdayf = 0
LE = 10
BBSf = 0
D = Date()
SD = Date()
E = LE + 1
Stable = 0
Log = 0
Style = 0
LastBBS = 0
pluses = 0
newm = 0
newc = 0
newh = 0
alltime = 0
Down = 0
City = 0
maxpnt = 0
auto_ = [0, 0, 0, 0]  # link, debt, OS, antivirus
Time = 0


# Define the toccup structure as a class
class Toccup:
    def __init__(self, name, ord, func):
        self.name = name
        self.ord = ord
        self.func = func


# Define the occupations
occup = [
    Toccup("Почта       ", 1, 'mailtime'),
    Toccup("Работа      ", 2, 'worktime'),
    Toccup("Учеба       ", 3, 'studtime'),
    Toccup("Развлечения", 4, 'joytime')
]

# Define the OS names
OSnames = [
    "MSDOS 5.0",
    "MSDOS+Win'3.11",
    "Windows 95",
    "Windows NT",
    "OS/2",
    "Linux",
    None
]

# Define the OS information
os = [
    {"memory": 3 * (2 ** 10), "disk": 8, "index": 0},
    {"memory": 15 * (2 ** 10), "disk": 20, "index": 1},
    {"memory": 70 * (2 ** 10), "disk": 30, "index": 2},
    {"memory": 100 * (2 ** 10), "disk": 60, "index": 3},
    {"memory": 150 * (2 ** 10), "disk": 50, "index": 3},
    {"memory": 200 * (2 ** 10), "disk": 90, "index": 3}
]

