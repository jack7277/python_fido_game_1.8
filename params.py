import random
import time

from fido_date import *
from fido_random import _rnd
from mood import *
from person import you
from reputation import chrep
from wnds import prn, menuf, write, message, prnc, scr, scrw


def getch():
    import os
    if os.name == 'nt':
        import msvcrt
        return msvcrt.getch().decode()
    else:
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


def round(f):
    return int(f + (0.5 if f > 0 else -0.5))


end1 = ("", "а", "ов")
end2 = ("день", "дня", "дней")

# Define the OS names

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

upgrm = ["Компьютер", "Модем", "Винт", "Себя", None]
emenu = ["GoldEd", "Подписка", "Создание", "Поведение в эхах", "Статистика", None]
points = ["Набрать", "Разогнать", None]
game = ["Save", "Log on", "View ReadMe", "Quit to DOS", None]
logst = ["Log on", "Log off"]
bbsmenu = ["Звонить", None, None]
tmenu = ["Приоритеты", "Развлечься", "Автопилот", None]
smenu = ["Антивирус", "Операционная система", "Купить", "Расчистить", None]
jmenu = ["Устроиться", "Уволиться", None]
lmenu = ["Поступить в институт", "Поступить на курсы", "Интенсивность занятий", "Бросить учебу", None]
fmenu = ["Пообщаться", "Попросить взаймы", None]
aut = ["Подписываться ", "Давать в долг ", "Ставить ОС    ", None]
autop = ["Вручную", "Да     ", "Нет    ", None]

style = ["Read-only", "Неактивный", "Активный", "Flame", None]
week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
month = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
         "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь", None]
situat = ["Нестабильная", "Стабильная", None]
dtm = ""

prob = [0, 1, 4, 8]  # вероятность [+] в % как f(Style) при izverg==1
lstscn = fido_date.Date()
newdayf = 0
LE = 10
BBSf = 0
D = fido_date.Date()
SD = fido_date.Date()
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


def scrs(y, x, c):
    scr[(y) * 160 + ((x) << 1)] = (c)


def scra(y, x, c):
    scr[(y) * 160 + ((x) << 1) + 1] = (c)


def scrsa(y, x, w):
    scrw[(y) * 80 + (x)] = (w)


def end(x, ending=end1):
    if 10 < x <= 20:
        # if x<=20 and x>10:
        return ending[2]
    x = x % 10 - 1
    return ending[1] if x < 4 else ending[2]


mtok = lambda x: (x) << 10
BB = lambda: you.hdspace < mtok(hd[you.hd])


def newjob(pay, time, prof):
    if you.wdays > 7:
        you.money += you.income * (float(you.wdays % 30) / 30)
    you.ftime += you.wtime
    you.wtime = time
    you.ftime -= you.wtime
    you.wprof = prof
    you.income = pay
    you.wdays = 0
    you.osreq = 0
    you.wdate = 0


def yn(qst, ans=0, c1=0x70, c2=0xF):
    ls = 0
    k = 0
    i = 0
    s = 1
    n = 1
    while qst[i]:
        if qst[i] == '\n':
            if k > ls:
                ls = k
            k = 0
            n += 1
        else:
            k += 1
        i += 1
    if k > ls:
        ls = k
    ll = max(ls + 4, 28)
    t = 10
    l = (78 - ll) >> 1
    # q = openbox(t, l, t + 5 + n, l + ll, c1)
    write(t + 2, l + 2, qst)
    if ans:
        s = ans
    while (True):
        prnc(t + 3 + n, l + 2, " А как же! ", c2 if s == 1 else c1)
        prnc(t + 3 + n, l + ll - 12, " Вот еще!  ", c1 if s == 1 else c2)
        if ans:
            delay(1000)
            break
        c = getch()
        if c == 13:
            break
        elif c == 75:
            if s == 1:
                s = 2
            else:
                s -= 1
        elif c == 77:
            if s == 2:
                s = 1
            else:
                s += 1
    # closebox(t, l, t + 5 + n, l + ll, q)
    return s == 1




def studper(D):
    if D < Date(D.year, 1, 25) or (Date(D.year, 6, 1) <= D < Date(D.year, 6, 25)):
        return 0  # session
    elif Date(D.year, 9, 1) <= D or (Date(D.year, 2, 6) <= D < Date(D.year, 6, 1)):
        return 1  # semester
    else:
        return 2  # vacations


def delay(ms):
    time.sleep(ms / 1000)


def fire():
    chrep(-random.randint(0, 10) - 5)
    you.skill[you.wprof] -= 15
    if you.skill[you.wprof] < 0:
        you.skill[you.wprof] = 0
    chmood(-15 - _rnd((you.income) / (you.wtime / 60.0) / 8))
    you.ftime += you.wtime
    you.wtime = 0
    you.wdays = 0
    you.income = 0
    you.wprof = 0
    you.osreq = 0


def showtime():
    prn(0, 0,
        f"{week[D.weekday()]}, {D.day()}.{D.month()}.{D.year()}  Осталось {Time / 60} ч. {Time % 60} мин. ")
    prn(0, 32, dtm)


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

# Define the OS information
os = [
    {"memory": 3 * (2 ** 10), "itime": 8, "mincomp": 0},
    {"memory": 15 * (2 ** 10), "itime": 20, "mincomp": 1},
    {"memory": 70 * (2 ** 10), "itime": 30, "mincomp": 2},
    {"memory": 100 * (2 ** 10), "itime": 60, "mincomp": 3},
    {"memory": 150 * (2 ** 10), "itime": 50, "mincomp": 3},
    {"memory": 200 * (2 ** 10), "itime": 90, "mincomp": 3}
]
