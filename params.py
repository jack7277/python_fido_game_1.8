from datetime import datetime
import fido_date

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


qstns = [
    {"qstn": "Каково время ZMH зоны 2?",
     "ans": ["2:30 - 3:30 UTC", "3:30 - 4:30 UTC", "5:30-6:30 московского времени"],
     "mark": 0,
     "correct": 0},
    {"qstn": "Что обязан делать нод?",
     "ans": ["Набирать поинтов", "Поддерживать ZMH", "Раздавать файлэхи"],
     "mark": 0,
     "correct": 1},
    {"qstn": "Что означают цифры 5020 в адресе 2:5020/1402?",
     "ans": ["Номер зоны", "Номер статьи УК", "Номер сети"],
     "mark": 0,
     "correct": 2},
    {"qstn": "Вправе ли нод просматривать нетмэйл, идущий через его узел?",
     "ans": ["Да", "Нет", "Не только просматривать, но и изменять"],
     "mark": 0,
     "correct": 0},
    {"qstn": "Для чего предназначен ZMH?",
     "ans": ["Для работы ББС", "Для пересылки нетмэйла", "Для отдыха сисопа"],
     "mark": 0,
     "correct": 1},
    {"qstn": "Какова плата за подключение к ФИДО?",
     "ans": ["$50", "3 бутылки пива", "Подключение бесплатное"],
     "mark": 0,
     "correct": 2},
    {"qstn": "Кто осуществляет управление сетью?",
     "ans": ["Координатор", "Администратор", "Модератор"],
     "mark": 0,
     "correct": 0},
    {"qstn": "Каким образом получает должность Координатор Зоны?",
     "ans": ["Жеребьевкой", "Голосованием", "По наследству"],
     "mark": 0,
     "correct": 1},
    {"qstn": "При возникновении конфликта с другим сисопом первым делом надо:",
     "ans": ["Подать жалобу сетевому координатору", "Подать в суд", "Попытаться решить конфликт нетмэйлом"],
     "mark": 0,
     "correct": 2}
]

ndreq = [
    {"str": "Ваше имя", "mark": 0, "correct": 1},
    {"str": "Возраст", "mark": 0, "correct": 0},
    {"str": "Пол", "mark": 0, "correct": 0},
    {"str": "Семейное положение", "mark": 0, "correct": 0},
    {"str": "Город и страна, где расположена стация", "mark": 0, "correct": 1},
    {"str": "Домашний адрес", "mark": 0, "correct": 0},
    {"str": "Номер голосового телефона", "mark": 0, "correct": 1},
    {"str": "Место работы", "mark": 0, "correct": 0},
    {"str": "Годовой доход", "mark": 0, "correct": 0},
    {"str": "Образование", "mark": 0, "correct": 0},
    {"str": "Номер модемного телефона", "mark": 0, "correct": 1},
    {"str": "Название вашей станции", "mark": 0, "correct": 1},
    {"str": "Ваш компьютер", "mark": 0, "correct": 0},
    {"str": "Ваш модем", "mark": 0, "correct": 1},
    {"str": "Стаж работы с компьютером", "mark": 0, "correct": 0},
    {"str": "Время работы вашей станции", "mark": 0, "correct": 1},
    {"str": "Национальность", "mark": 0, "correct": 0},
    {"str": "Партийная принадлежность", "mark": 0, "correct": 0},
    {"str": "BPS вашего модема", "mark": 0, "correct": 1},
    {"str": "Каким мэйлером пользуетесь", "mark": 0, "correct": 1},
    {"str": "Привлекались ли к уголовной ответственности", "mark": 0, "correct": 0}
]

status = ["Юзер", "Поинт", "Нод", "NC"]
profn = ["---", "Программирование", "Железо", "Торговля/менеджмент", None]
stper = ["СЕССИЯ!", "Семестр", "Каникулы"]
bps = [2400, 9600, 14400, 21600, 28800, 33600]
comp = ["286", "386DX40", "486DX2/66", "486DX100", "Pentium-133", "Pentium-166", "Pentium Pro 200"]
hd = [20, 40, 120, 540, 850, 1200, 2500]  # Объемы жесткого диска в МБ
mprice = [5, 50, 100, 180, 240, 350]  # Цены на модем в $
cprice = [45, 140, 350, 550, 800, 1000, 2300]  # Цены на компьютеры в $
hprice = [5, 10, 40, 80, 120, 200, 300]  # Цены на HDD, в $
pref = "MO."
echoname = ["NETMAIL", "LOCAL.PVT", "*POINT", "PVT.EXCH.COMPUTER", "PVT.EXCH.BLACK.LOG",
            "RU.ANEKDOT", "*JOB", "VERY.COOL", "SU.HARDW", "SU.SOFTW", "файлэхи",
            None, None, None, None, None, None]
echodescr = ["Личная почта", "Локалка", "Поинтовые дела", "Покупка/продажа железа", "Что у кого стоит покупать",
             "Анекдоты", "Устройство на работу", "Весьма полезная эха", "Тонкости железа", "Программирование",
             None, "Моя крутая эха #1            ", "Моя крутая эха #2            ", "Моя крутая эха #3            ",
             "Моя крутая эха #4            ", "Моя крутая эха #5            "]
bbsnames = ["Format complete", "Ctrl-Alt-Del", "Fatal error", "Exception 13", "NO CARRIER", "Lamer Hunter",
            "Windows Must Die", "Beer Club", "Mailoman's", "Crazy Gamers", None, "                  "]
cityname = [None] * 23
cities = [
    {"name": "Москва", "pref": "MO.", "frnds": 0, "fr": 0},
    {"name": "Санкт-Петербург", "pref": "SPB.", "frnds": 0, "fr": 0},
    {"name": "Владивосток", "pref": "VL.", "frnds": 0, "fr": 0},
    {"name": "Днепропетровск", "pref": "DN.", "frnds": 0, "fr": 0},
    {"name": "Донецк", "pref": "DONBASS.", "frnds": 0, "fr": 0},
    {"name": "Екатеринбург", "pref": "MU.", "frnds": 0, "fr": 0},
    {"name": "Иркутск", "pref": "ESIB.", "frnds": 0, "fr": 0},
    {"name": "Калуга", "pref": "KLG.", "frnds": 0, "fr": 0},
    {"name": "Киев", "pref": "KIEV.", "frnds": 0, "fr": 0},
    {"name": "Краснодар", "pref": "KR.", "frnds": 0, "fr": 0},
    {"name": "Красноярск", "pref": "KRS.", "frnds": 0, "fr": 0},
    {"name": "Луганск", "pref": "LUG.", "frnds": 0, "fr": 0},
    {"name": "Нижний Тагил", "pref": "NT.", "frnds": 0, "fr": 0},
    {"name": "Новокузнецк", "pref": "NKZ.", "frnds": 0, "fr": 0},
    {"name": "Новосибирск", "pref": "NSK.", "frnds": 0, "fr": 0},
    {"name": "Пермь", "pref": "PERM.", "frnds": 0, "fr": 0},
    {"name": "Псков", "pref": "PSKOV.", "frnds": 0, "fr": 0},
    {"name": "Рязань", "pref": "RZ.", "frnds": 0, "fr": 0},
    {"name": "Томск", "pref": "TSK.", "frnds": 0, "fr": 0},
    {"name": "Уфа", "pref": "UFA.", "frnds": 0, "fr": 0},
    {"name": "Харьков", "pref": "KHARKOV.", "frnds": 0, "fr": 0},
    {"name": "Челябинск", "pref": "CHEL.", "frnds": 0, "fr": 0}
]


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
    {"memory": 3 * (2 ** 10), "itime": 8, "mincomp": 0},
    {"memory": 15 * (2 ** 10), "itime": 20, "mincomp": 1},
    {"memory": 70 * (2 ** 10), "itime": 30, "mincomp": 2},
    {"memory": 100 * (2 ** 10), "itime": 60, "mincomp": 3},
    {"memory": 150 * (2 ** 10), "itime": 50, "mincomp": 3},
    {"memory": 200 * (2 ** 10), "itime": 90, "mincomp": 3}
]

