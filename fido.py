"""
Исходники игры FIDO v. 1.8.
Автор - Юрий Нестеренко
URL: http://yun.complife.net
e-mail: comte@au.ru
При внесении любых модификаций указание моих копирайтов обязательно
"""
import sys
import time
from random import random
from typing import Union

import params
from date import *
from wnds import *
from wnds import _box

import random

def lrandom(x):
    return x if x == 0 else (random.randint(0, 0xFFFF) * random.randint(0, 0xFFFF)) % x

def random_(x):
    return -random.randint(0, -x) if x < 0 else random.randint(0, x)

def upcase(c):
    return chr(ord(c) & ~0x20)

def setbit(x, n):
    return x | (1 << n)

def tstbit(x, n):
    return x & (1 << n)

class toccup:
    def __init__(self, name, ord, func):
        self.name = name
        self.ord = ord
        self.func = func


def mailtime():
    pass


def worktime():
    pass


def studtime():
    pass


def joytime():
    pass


occup = [
    toccup("Почта      ", 1, mailtime),
    toccup("Работа     ", 2, worktime),
    toccup("Учеба      ", 3, studtime),
    toccup("Развлечения", 4, joytime)
]

word = Union[int, None]
byte = Union[int, None]


# Define the question structure as a class
class Question:
    def __init__(self, qstn, ans, mark, correct):
        self.qstn = qstn
        self.ans = ans
        self.mark = mark
        self.correct = correct


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

import os

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

class Person:
    def __init__(self):
        self.name = ""  # salloc(31) длина 31 символ
        self.status = 0
        self.sysop = 0
        self.modem = 0
        self.comp = 0
        self.hd = 0
        self.mreli = 32767
        self.creli = 32767
        self.hreli = 32767
        self.income = 0
        self.expens = -150
        self.spay = 0
        self.money = 300
        self.debt = 0
        self.soft = 0
        self.os = 0
        self.osreq = 0
        self.hdspace = 20 * 1024
        self.virus = 0
        self.ftime = 20 * 60
        self.wtime = 0
        self.wdays = 0
        self.sdays = -1
        self.wprof = 0
        self.sprof = 0
        self.mood = 0
        self.tired = 0
        self.reput = 0
        self.moder = 0
        self.points = 0
        self.friends = 0
        self.antiv = params.Date()
        self.wdate = params.Date()
        self.grad = params.Date()
        self.tries = 0
        self.army = 0
        self.intens = 0
        self.mark = 0.0
        self.echo = [0] * 5
        self.skill = [0, 100, 0, 0]  # 0,prg,hrd,trd

    def reput_(self):
        return self.reput + self.skill[1] + self.skill[2] + self.skill[3]


you = Person()

class Echo:
    def __init__(self, you):
        self.name = ''
        self.stat = 0  # 0 - Unlinked 1 - Linked 2 - moderator 80 - read from BBS
        self.mark = 0  # 1 - autoread, 2 - passthru
        self.msg = 0
        self.newm = 0
        self.new1 = 0  # messages: total, unread, new for this day
        self.dl = params.Date()  # для отключенных - дата подключения. if < current - ignored
        self.plus = 0  # number of [+]
        self.traf = 0  # средний трафик в К
        self.trafk = 0.0  # traf*trafk - сколько мин. в день отнимает чтение эхи (Style==0)
        self.read = 0  # % свежих прочитанных писем, за 4 дня уходит в 0
        self.izverg = 0.0  # коэф. злобности модератора
        self.you = you

    def event(self):
        if random.randint(0, 4) != 0:
            return 0
        l = random.randint(32, 1055)
        l = self.incsoft(l)
        you.virus += random.randint(0, l) < (l >> 5)
        if random.randint(0, 4) == 0:
            you.antiv = params.D
            message("A fresh antivirus came through the file echo! Useful thing...", 0x1F)
            chmood(1)
        return 1

    def incsoft(self, ds, chrp=1):
        if you.soft + os[self.you.os].size + ds > self.you.hdspace:
            ds = self.you.hdspace - you.soft - os[self.you.os].size
        if not ds:
            return 0
        chrep(random.randint(0, ds * int(you.status / 512)) / 2, chrp)
        you.soft += ds
        return ds

    def moderatorial(self, y, x):
        nn = [" ", " второй ", " третий "]
        if 100 * random() < params.prob[params.Style] * self.izverg * (1 + float(random() * (self.you.points)) / 32):
            s = f"За нарушение правил вы получили {nn[1]} ПЛЮС"
            self.plus += 1
            # self.pluses += 1
            d = -2
            if self.plus == 3:
                stat = 0
                dl = params.D + 92
                s += f"\nи отключены от конференции до {dl.day()}.{dl.month()}.{dl.year()}"
                d -= 5
            from_ = f"Moderator of {self.name}"
            fidomess(from_, you.name, "moderatorial [!]" if self.plus > 2 else "moderatorial [+]", s, y, x)
            chrep(d)
            chmood(-(2 << self.plus))
            return 1
        return 0

echoes = [Echo(you) for _ in range(params.LE+6)]

class fecho(Echo):
    def __init__(self):
        super().__init__(10)
        self.izverg = 0
        self.traf = 1024
        self.trafk = 0.01


def final(st):
    s = ' ' * 1024
    ar = [0] * (80 * 24)
    s = (f"{st}{params.D - params.SD} {end(params.D - params.SD, end2)}. За это время вы потратили\n"
         f"на почту {params.alltime // (24 * 60)} сут. {(params.alltime % (24 * 60)) // 60} ч. {params.alltime % (24 * 60) % 60} мин. чистого времени, получили {params.pluses} плюс{end(params.pluses)}\n"
         f"в конференциях, сменили {params.newm} модем{end(params.newm)} и {params.newc} компьютер{end(params.newc)}.")
    block(1, 23, 0xF)
    showstat(1, 22, 0x30)
    scrw[0x1000:0x1000 + 4000] = scrw[:4000]
    page(1)
    ar = [0] * (80 * 24)
    block(1, 24, 0x1F)
    message(s, 0x1F, 0)
    prnc(24, 0, "                              Нажмите клавишу \"Anykey\"                         ", 0x74)
    i = 80 * 24
    while i:
        j = random.randint(0, 80 * 24 - 1)
        if ar[j] == 0:
            i -= 1
            ar[j] = 1
            scrw[j + 0x800 + 80] = scrw[j + 80]
            delay(20)
    anykey()
    page(0)
    quit(0)


def min(a, b):
    return b if a > b else a


def max(a, b):
    return a if a > b else b


def getch():
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


def _year(Date: word) -> word:
    return ((Date & 0xFE00) >> 9) + 1980


def _month(Date: word) -> byte:
    return (Date & 0x01E0) >> 5


def _day(Date: word) -> byte:
    return Date & 0x001F


def round(f: float) -> int:
    return int(f + (0.5 if f > 0 else -0.5))




def dstodate(days: word) -> word:
    d, j, i, k, y = 0, 0, 0, 0, 0
    dt = params.Date()
    y = int(days // 365.25)
    while (y * 365 + ((y + 3) >> 2)) >= days:
        y -= 1
    d = days - d
    if not (y & 0x0003):  # for leap-year
        if d == mofs[2] + 1:  # 29 Feb
            dt.setmonth(2)
            dt.setday(29)
        elif d > mofs[2]:
            d -= 1
    if d > mofs[11]:
        k = 11
    else:
        i, j = 0, 11
        while j > i + 1:
            k = (i + j) >> 1
            if d > mofs[k]:
                i = k
            else:
                j = k
        k = i
    dt.setmonth(k + 1)
    dt.setday(d - mofs[k])
    dt.setyear(y + 1990)
    return dt.date


class BBS:
    def __init__(self):
        self.name = None
        self.mxtime = 0  # -1 means twit, 0 - 1st time
        self.time = 0  # current time
        self.U = 0  # upload
        self.D = 0  # download
        self.soft = 0  # total not-your soft
        self.modem = 0
        self.down = 0
        LE = 10
        self.ech = [0] * (LE - 2)


bbs = [BBS() for _ in range(10)]




# class echo:
#     def __init__(self,n):
#         self.name=echoname[n]
#         self.stat=0
#         self.plus=0
#         self.traf=20
#         self.trafk=0.4
#         self.read=0
#         self.izverg=1
#         self.moderatorial()
#     def moderatorial(self,y=5,x=8):
#         return 0
#     def event(self):
#         return 0
#
# class netmail(echo):
#     def __init__(self):
#         super().__init__(0)
#         self.izverg=0
#         self.traf=0
#         self.trafk=0.7
#
# class local(echo):
#     def __init__(self):
#         super().__init__(1)
#         self.izverg=0
#         self.traf=10
#         self.trafk=0.5
#
# class point(echo):
#     def __init__(self):
#         super().__init__(2)
#         self.traf=15
#
# class exch(echo):
#     def __init__(self):
#         super().__init__(3)
#
# class bllog(echo):
#     def __init__(self):
#         super().__init__(4)
#
# class ruanekdot(echo):
#     def __init__(self):
#         super().__init__(5)
#         self.izverg=4
#         self.traf=70
#         self.trafk=0.5
#
# class job(echo):
#     def __init__(self):
#         super().__init__(6)
#         self.izverg=2.0
#         self.traf=35
#         self.trafk=0.2
#
# class vcool(echo):
#     def __init__(self):
#         super().__init__(7)
#         self.izverg=2.0
#         self.traf=45
#         self.trafk=0.45
#
# class hardw(echo):
#     def __init__(self):
#         super().__init__(8)
#         self.traf=100
#         self.trafk=0.4
#
# class softw(echo):
#     def __init__(self):
#         super().__init__(9)
#         self.traf=100
#         self.trafk=0.4
#
# class fecho(echo):
#     def __init__(self):
#         super().__init__(10)
#         self.izverg=0
#         self.traf=1024
#         self.trafk=0.01

Cursor = 0


def min_(x, y):
    if x < y:
        y = x
        x = 0
        return y
    x -= y
    return y


def quit(i):
    # fclose(log)
    # curson()
    # clrscr()
    sys.exit()


def ESC():
    pass
    # return (kbhit() and getch()==27)


def scrs(y, x, c):
    scr[(y) * 160 + ((x) << 1)] = (c)


def scra(y, x, c):
    scr[(y) * 160 + ((x) << 1) + 1] = (c)


def scrsa(y, x, w):
    scrw[(y) * 80 + (x)] = (w)


def anykey():
    q = ''
    # gettext(1,25,80,25,q)
    prnc(24, 0, "                              Нажмите клавишу \"Anykey\"                         ", 0x74)
    # if not getch():
    #     getch()
    # puttext(1,25,80,25,q)
    # free(q)


# def viewstr(s,t=2,l=5,h=20,w=70, col=0x70):
#     p=0
#     p1=0
#     i=0
#     q=openbox(t,l,t+h,l+w,col)
#     show:
#     clrbl(t+1,l+2,t+h-1,l+w-1,col)
#     p1=writen(t+1,l+2,s+p,h-1)
#     while True:
#         c=getch()
#         if c==27:
#             break
#         elif c==0:
#             c=getch()
#             if c==73:
#                 for i in range(h-1):
#                     if not p:
#                         break
#                     p-=1
#                     while p:
#                         p-=1
#                         if s[p-1]=='\n':
#                             break
#                 goto show
#             elif c==72:
#                 if not p:
#                     break
#                 p-=1
#                 while p:
#                     p-=1
#                     if s[p-1]=='\n':
#                         break
#                 goto show
#             elif c==81:
#                 for i in range(h-1):
#                     while s[p]:
#                         p+=1
#                         if s[p-1]=='\n':
#                             break
#                 goto show
#             elif c==80:
#                 while s[p]:
#                     p+=1
#                     if s[p-1]=='\n':
#                         break
#                 goto show
#         elif c==13:
#             d=r-*n
#             *n=r
#             return d
#     closebox(t,l,t+h,l+w,q)

def message(s, c, wait=1, y=0xFF, x=0):
    prn(0, 0, s)
    # i=0
    # k=0
    # l=0
    # n=1
    # q=None
    # while s[i]:
    #     if s[i]=='\n':
    #         if k>l:
    #             l=k
    #         k=0
    #         n+=1
    #     else:
    #         k+=1
    #     s += 1
    # if k>l:
    #     l=k
    # if y==0xFF:
    #     y=(25-n) >> 1
    #     x=(76-l) >> 1
    # q=openbox(y,x,y+n+1,x+l+3,c)
    # write(y+1,x+2,s)
    # if Log:
    #     prn(0,0, "%d.%d.%d\n%s\n",D.day(),D.month(),D.year(),s)
    # if wait==1:
    #     anykey()
    #     closebox(y,x,y+n+1,x+l+3,q)
    # elif wait==0:
    #     pass  # free(q)
    # else:
    #     delay(1000)
    #     closebox(y,x,y+n+1,x+l+3,q)


def nmbrscrl(n, y, x, mx=99, mn=0, dn=1):
    c = 0
    s = [8] * 8
    r = n
    d = 0
    if r < mn:
        r = mn
    elif r > mx:
        r = mx
    prn(0, 0, f"%3d {r}")
    prn(y, x + 1, s)
    scrs(y - 1, x, 30)
    scrs(y + 1, x, 31)
    scrs(y, x, '■')
    while c != 27:
        c = getch()
        if c == 0:
            continue
        elif c == 80:
            if r >= mn + dn:
                r -= dn
        elif c == 72:
            if r <= mx - dn:
                r += dn
        elif c == 13:
            pass
            # d=r-*n
            # *n=r
            return d
        prn(0, 0, f"%3d {r}")
        prn(y, x + 1, s)
    return 0


def studper(D):
    if D < datetime.date(D.year, 1, 25) or (datetime.date(D.year, 6, 1) <= D < datetime.date(D.year, 6, 25)):
        return 0  # session
    elif datetime.date(D.year, 9, 1) <= D or (datetime.date(D.year, 2, 6) <= D < datetime.date(D.year, 6, 1)):
        return 1  # semester
    else:
        return 2  # vacations


def echtime(i, echoes, Style, you):
    return round(echoes[i].traf * echoes[i].trafk * (Style + 1) * (1 if echoes[i].stat > 2 else echoes[i].stat) * (
                11.0 - you.comp / 1.5) * (1 if you.os > 0 else 1.3) / 10.0)


def sttime(D, you):
    if not you.spay:
        return 0
    elif you.spay < 0:
        return 0 if studper(D) == 2 else 6 * 60.0 * you.intens / 100.0
    else:
        return 2 * 60


week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
month = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь",
         "Декабрь", None]
situat = ["Нестабильная", "Стабильная", None]

dtm = ""


def showtime():
    prn(0, 0,
        f"{week[params.D.weekday()]}, {params.D.day()}.{params.D.month()}.{params.D.year()}  Осталось {params.Time / 60} ч. {params.Time % 60} мин. ")
    prn(0, 32, dtm)


def showhelp():
    s = ''
    prn(0, 0, f"Game │ BBS Upgrade Job Learn Soft Echoes Points Friends Time Next day")
    prncc(24, 0, s, 0x70)
    # free(s)


end1 = ("", "а", "ов")
end2 = ("день", "дня", "дней")


def end(x, ending=end1):
    if 10 < x <= 20:
        # if x<=20 and x>10:
        return ending[2]
    x = x % 10 - 1
    return ending[1] if x < 4 else ending[2]


mtok = lambda x: (x) << 10

BB = lambda: you.hdspace < mtok(hd[you.hd])


def showstat(y=1, x=22, c=0x30, c2=0x3F):
    mood = ["==8~-(E (", "=8~-((", "8~-(", ":~-(", ":-(", ":-/", ":-I", ";-I", ";-)", ":-)", "Ж:-)", "Ж:-))", "Ж8-D",
            "Ж|-))", "Ж|-)))", "Ж|-)))"]
    s = ""
    i = 0
    _box(y, x, y + 17 + you.sysop + you.moder, x + 55, c, SDB)
    prnc(y + 1, x + 2, you.name, c2)
    prn(y + 2, x + 2, f"Статус: {status[you.status]}")
    if you.status > 1:
        prn(0, 0, "(%d поинт%s)" + str(you.points) + ' ' + end(you.points))
        # prnc(y+2, x+17, s, c2)
    if you.sysop:
        y += 1
        prn(0,0,f"Сисоп %c%s BBS {bbsnames[11]}")
        if params.Down or you.modem == 0xFF:
            prn(0, 0, f'{s + str(i)} (в дауне)')
        else:
            prn(0, 0, f'{s + str(i)} требует {round(75 * (you.modem + 1) * .1 + 10)} мин.в день')
        # prncc(y+2,x+2,s,c)
    for i in range(you.moder):
        prn(y + 3 + i, x + 3, "Модератор ")
        prnc(y + 3 + i, x + 3 + 10, echoes[params.LE + 1 + i].name, c2)
    y += you.moder
    prn(0, 0, f"Репутация: {you.reput}")
    # prncc(y+3,x+2,s,c)
    if (you.comp | you.modem) == 0xFF:
        prnc(y + 4, x + 2, "Проблемы с hardware!", c2)
    else:
        prn(0, 0, f"Компьютер {comp[you.comp]} Модем на {bps[you.modem]}")
        # prncc(y+4,x+2,s,c)
    for i in range(1, 4):
        prn(0, 0, f"{profn[i]} {you.skill[i]}")
        # prncc(y+5+i,x+2,s,c)
    prn(0, 0, f"Работа: {profn[you.wprof]} З/п {you.income} Стаж {you.wdays} д.")
    # prncc(y+9,x+2,s,c)
    y += 4
    prn(0, 0, f"Учеба: {profn[you.sprof]}")
    if you.spay < 0:
        # p = stper[studper(D)]
        p = 3
        prn(0, 0, f" {p} Ср.балл {you.mark}")
    # prncc(y+9,x+2,s,c)
    y += 4
    wtime = sttime(params.D, you)
    prn(0, 0, f"Время/сут.: {you.wtime / 60.0} Работа {wtime / 60.0} Учеба  Своб. {(you.ftime - wtime) / 60.0}")
    # prncc(y+6,x+2,s,c)
    mem = params.os[you.os]['memory'] >> 10
    prn(0, 0, f"ОC: {params.OSnames[you.os]} занимает {mem} МБ")
    if you.osreq:
        prn(0, 0, f'{s + str(i)} Надо {params.OSnames[you.osreq]}')
    # prncc(y+7,x+2,s,c)
    prn(0, 0, f"{you.soft}К КРУТОГО СОФТА")
    if you.antiv:
        prn(0, 0, f'Антивирус от {you.antiv.day()}.{you.antiv.month()}.{you.antiv.year()}')
    # prncc(y+8,x+2,s,c2)
    d = you.spay if you.spay < 0 else 0
    d2 = you.spay if you.spay > 0 else 0
    prn(0, 0, f"Месячный доход/расход {you.income - d}$/~${-you.expens + d2}  Долги {you.debt}")
    # prncc(y+9,x+2,s,c)
    prn(0, 0, f"Всего денег {you.money}    Друзей: {you.friends}")
    # prncc(y+10,x+2,s,c)
    prn(0, 0, f"Настроение: {you.mood} хорошего {mood[int(you.mood / 10)]}  Усталость {you.tired}")
    # prncc(y+11,x+2,s,c)
    showtime()
    # free(s)


class Memfile:
    def __init__(self):
        self.buff = None
        self.ptr = None
        self.f = None
        self.size = None
        self.dt = None
        self.tm = None

    def open(self, name, atr):
        self.f = os.open(name, atr)
        if self.f == -1:
            return -1
        self.size = os.lseek(self.f, 0, 2)
        if self.buff is None:
            self.buff = bytearray(self.size)
        os.lseek(self.f, 0, 0)
        os.read(self.f, self.buff)
        self.ptr = memoryview(self.buff)
        return self.f

    def read(self, adr, l):
        noteof = 1
        if self.ptr + l > len(self.buff):
            l = len(self.buff) - self.ptr
            noteof = 0
        adr[:] = self.ptr[:l]
        self.ptr = self.ptr[l:]
        return noteof

    def write(self, adr, l):
        noteof = 1
        if self.ptr + l > len(self.buff):
            l = len(self.buff) - self.ptr
            noteof = 0
        self.ptr[:l] = adr
        self.ptr = self.ptr[l:]
        return noteof

    def flush(self, closef=1):
        os.lseek(self.f, -self.size, 1)
        os.write(self.f, self.buff)
        if closef:
            os.close(self.f)


M = Memfile()


def code(name):
    if M.open(name, os.O_RDWR) == -1:
        return 0
    s = bytearray(f"{M.tm ^ M.dt:04x}{~M.tm:04x}", 'utf-8')
    for i in range(len(M.buff)):
        M.buff[i] ^= s[i % 8]
    return 1


# def save(fname):
#     f = os.open(fname, os.O_CREAT | os.O_WRONLY)
#     os.write(f, params.D.Date)
#     os.write(f, params.E)
#     os.write(f, you.status)
#     os.write(f, bbs)
#     for i in range(params.E):
#         os.write(f, echoes[i].stat)
#         os.write(f, echoes[i].name)
#         if echodescr[i] is not None:
#             os.write(f, echodescr[i])
#         else:
#             os.write(f, b'\x00' * 30)
#     os.write(f, you.name)
#     for i in range(4):
#         os.write(f, occup[i].ord)
#     if you.sysop:
#         os.write(f, bbsnames[11])
#     os.close(f)
#     code(fname)
#     M.flush()


# def load():
#     e1 = params.E
#     if not code("fido.dat"):
#         return 0
#     s = bytearray(30)
#     M.read(D.Date, len(D.Date))
#     M.read(E, len(E))
#     M.read(you.status, len(you) - len(you.name))
#     M.read(bbs, len(bbs))
#     for i in range(10):
#         bbs[i].name = bbsnames[i]
#     for i in range(LE + 1, e1):
#         del echoes[i]
#     for i in range(LE + 1, E):
#         echoes[i] = Echo(i)
#     for i in range(E):
#         M.read(echoes[i].stat, len(echoes[i].izverg) - len(echoes[i].stat) + sizeof(float))
#         M.read(echoes[i].name, 30)
#         s = echoes[i].name.decode('utf-8')
#         if echodescr[i] is not None:
#             echodescr[i] = s
#     M.read(you.name, 30)
#     for i in range(4):
#         M.read(occup[i].ord, len(occup[0].ord))
#         tmpocp = occup[occup[i].ord - 1]
#     occup = tmpocp
#     if you.sysop:
#         M.read(bbsnames[11], 20)
#     os.close(M.f)
#     return 1

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
    q = openbox(t, l, t + 5 + n, l + ll, c1)
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
    closebox(t, l, t + 5 + n, l + ll, q)
    return s == 1


def chmood(dm):
    you.mood += dm
    if you.mood < 0:
        block(1, 24, 0x4F)
        message("                      Это конец!\n"
                "В приступе тяжелой депрессии вы  разбили молотком модем,\n"
                "выкинули из окна компьютер и повесились на сетевом шнуре.\n"
                "                       RIP.", 0x4F)
        quit(2)
    if you.mood <= 10:
        message(" Депрессия до добра не доводит!\n"
                "Нужно срочно поднять настроение!", 0x4F)
    elif you.mood > 150:
        if you.mood - dm < 150:
            message("Компьютер и модем - что еще человеку для счастья надо?", 0x1F)
        you.mood = 150


def chrep(dr, chrp=1):
    you.reput += dr
    if you.reput > 1024:
        if you.reput - dr < 1024:
            message("И слух о вас гремит по всей Сети великой...", 0x1F)
        you.reput = 1024
    elif dr < 0:
        if you.status == 2:
            if you.reput < 128:
                if chrp:
                    message("За особо раздражающее поведение вы лишены нодового адреса", 0x4F)
                    you.status = 1
                    maxpnt = you.points = 0
                else:
                    you.reput = 128
        elif you.status == 1:
            if you.reput < 32:
                if chrp:
                    message("За плохое поведение босс погнал вас из поинтов", 0x4F)
                    you.status = 0
                    # for i in range(params.LE + 1, E):
                    #     del echoes[params.E - 1]
                else:
                    you.reput = 32
        elif you.status == 0:
            if you.reput < -8:
                if chrp:
                    # block(1, 24, 0x4F)
                    message("Это ж кем надо быть, чтоб ни один сисоп не хотел иметь с вами дела!\n"
                            "         Вообще таким, как вы, надо винт форматировать... \n"
                            "                    Идите-ка отсюда, пока целы!", 0x4F)
                    quit(1)
                else:
                    you.reput = -8


def incsoft(ds, chrp=1):
    mem1 = you.soft + params.os[you.os]['memory'] + ds
    if mem1 > you.hdspace:
        ds = you.hdspace - you.soft - params.os[you.os]['memory']
    if not ds:
        return 0
    chrep(random_(ds * you.status / 512) / 2, chrp)
    you.soft += ds
    return ds


def newday():
    pass


def OSinfo(n):
    n -= 1
    s = f"Install time {params.os[n]['memory']} min.\nSpace required {params.os[n]['memory'] >> 10}M"
    write(14, 2, s)


def instOS(n=0):
    o = None
    i = None
    y = 10
    x = 0
    res = 0
    Time = 30  # ?????? тут этого не должно быть
    if not n:
        q = openbox(13, 0, 16, 22, 0x30)
        o = menuf(12, 25, 0x70, 0x0F, params.OSnames, "Install", 1, OSinfo)
        closebox(13, 0, 16, 22, q)
    else:
        o = n + 1
    while (1):
        if o:
            o -= 1
            if params.os[o]['memory'] > Time:
                message("Сегодня не успеем...", 0x4F)
                break
            if params.os[o]['mincomp'] > you.comp:
                message("У вас слишком хилый компьютер!", 0x4F)
                break
            if you.soft + params.os[o]['memory'] > you.hdspace:
                message("Не хватает места на винте!", 0x4F)
                break
            q = openbox(y, x, y + 6, x + 40, 0x0F)
            prn(0, 0, "Installing %s...", params.OSnames[o])
            # prn(y + 1, x + 1, s)
            for i in range(1, params.os[o]['itime'] + 1):
                prn(0, 0, "%d%% complete", 100 if i == params.os[o]['itime'] else i * 100 / params.os[o]['itime'])
                s = ''
                prn(y + 3, x + 2, s)
                Time -= 1
                showtime()
                if o > 0 and random() * (400 / (you.skill[1] + 1)) and not 10 * random():
                    message("Глюки!!! Придется переинсталлировать заново...", 0x4F)
                    break
                delay(400)
            closebox(y, x, y + 6, x + 40, q)
            you.os = o
            res = 1
            if you.osreq:
                you.wdate = params.D + 6
    return res


def fire():
    chrep(-random(10) - 5)
    you.skill[you.wprof] -= 15
    if you.skill[you.wprof] < 0:
        you.skill[you.wprof] = 0
    chmood(-15 - random() * (you.income) / (you.wtime / 60.0) / 8)
    you.ftime += you.wtime
    you.wtime = 0
    you.wdays = 0
    you.income = 0
    you.wprof = 0
    you.osreq = 0


def expel():
    you.skill[you.sprof] -= 10
    if you.skill[you.sprof] < 0:
        you.skill[you.sprof] = 0
    chmood(-10 - 8 * random())
    you.spay = 0
    you.sdays = 0
    you.grad = 0
    you.sprof = 0
    if you.army == 1:
        you.army = 3


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


def newinfo(i):
    return echoes[i].read > 100 * random()


def joffer(wait=1):
    while (1):
        if newinfo(6):
            var = [None] * 6
            vars = [[0] * 6] * 3
            n, k, j = None, None, None  # Uninitialized variables
            if wait:
                newdayf = 1
                # if tstbit(newday(), 14):
                #     break
            if max(you.skill[1], you.skill[3]) >= 4096:  # and not random(5):
                if you.skill[1] > you.skill[3] or (you.skill[1] > 4096 and you.money < 1000):
                    message("        Специальное предложение!      \n"
                            "Вы можете получить постоянную работу в США.\n"
                            "  Начальная зарплата - $5000 в месяц. ", 0x1F)
                    if yn("Согласны?"):
                        final("Ваш программистский уровень был оценен по достоинству. Вы уехали в Штаты.\n"
                              "Передавайте привет Пажитнову и остальным нашим! Теперь вам не до ФИДО...\n \n"
                              "Ваша фидошная карьера продолжалась ")
                elif you.money > 1000:
                    message("             Специальное предложение!          \n"
                            "Вы можете открыть свою собственную торговую фирму.", 0x1F)
                    if yn("Согласны?"):
                        final("Ну вот вы и новый русский. Или не русский? Впрочем, какая разница...\n"
                              "    Теперь вам не до ФИДО. Ваша дальнейшая биография может быть\n"
                              "       не менее интересной, но это уже совсем другая история...\n \n"
                              "Ваша фидошная карьера продолжалась ")
            q = openbox(10, 11, 12, 45, 0x70)
            echoes[6].read = 0
            s = f"Предложения работы в {echoes[6].name}"
            prn(11, 12 + len(pref) // 2, s)
            n = int(6 * random() + 1)
            for k in range(n):
                vars[k][2] = int(3 * random() + 1)
                vars[k][1] = int(2 * 60 + (12 if params.Stable else 20) * random() * 30)
                vars[k][0] = int(
                    vars[k][1] / 60.0 * (30 + (you.skill[vars[k][2]] - 64) * random() / 64.0 * 5 + (you.comp - 3) * 5))
                # s = f"{profn[vars[k][2]]<-20}  ${vars[k][0]:<4.0f}        {vars[k][1] / 60.0:.1f} ч."
                # var[k] = s
            var[n] = None
            j = menu(13, 14, 0x70, 0x0F, var, " Профиль              З/п в месяц  Время в день", 1)
            closebox(10, 11, 12, 45, q)
            if j:
                Down = 1
                newdayf = 1
                newday()
                if you.income + 80 * random() + you.skill[vars[j][2]] / 8 + (
                        you.skill[vars[j][2]] / 4) * random() + random() * (you.comp * 10) < vars[j][0]:
                    message("Вы не прошли собеседование", 0x4F)
                else:  # break  # goto no
                    newjob(vars[j][0], vars[j][1], vars[j][2])


def fidomess(from_, to, subj, text, y=5, x=8):
    q = openbox(y, x, y + 16, x + 60, 0x1E)
    prnc(y + 1, x + 1, "From : ", 0x13)
    prnc(y + 1, x + 8, from_, 0x13)
    prnc(y + 2, x + 1, "To   : ", 0x13)
    prnc(y + 2, x + 8, to, 0x13)
    prnc(y + 3, x + 1, "Subj : ", 0x13)
    prnc(y + 3, x + 8, subj, 0x13)
    for i in range(x + 1, x + 60):
        scrs(y + 4, i, '─')
    scrs(y + 4, i, 195)
    scrs(y + 4, 60 + x, 180)
    prn(y + 5, x + 1, "Hi ")
    i = wrtword(y + 5, x + 4, to)
    scrs(y + 5, x + 4 + i, '!')
    i = write(y + 7, x + 1, text)
    wrtword(y + 8 + i, x + 1, from_)
    anykey()
    closebox(y, x, y + 16, x + 60, q)


def proposal(i):
    from_ = ["Don Carleone", "Vasya Pupkin", "Sergey Mavrodi"]
    d = 0
    summ = 0
    pay = 0
    s = ''
    if i == 1:
        s = (f"Есть деловое предложение для крутого хакера.\n"
             f"Надо взломать кой-какую защиту. Плачу ${(you.skill[1] * 5) * random() + 100}.")
        d = 5 * random() + 2
    elif i == 2:
        s = f"Я слышал, вы можете компьютер наладить. За ${4 * random() * 10 + 20} возьметесь?"
        d = 1
    elif i == 3:
        pay = random(you.skill[3]) * 5 + 50
        s = (f"Предлагаю выгодный совместный бизнес.\n"
             f"Вложив всего ${pay}, вы получите ${pay * (2 + 4 * random())}!")
        d = 4 * random() + 2
    fidomess(from_[i - 1], you.name, "Предложение", s)
    if not yn("Вы принимаете предложение?"):
        return 0
    params.Down += d
    you.money -= pay
    s = None
    if i == 1:
        if summ * random() > you.skill[1] * 2:
            message("Ничего не вышло. Защита оказалась слишком сложной для вас.\n"
                    "Это не пойдет на пользу вашей профессиональной репутации.", 0x4F)
            you.skill[1] -= 5 * random()
            # break
        elif not random() * (you.skill[1] >> 7):
            s = (f"У вас крупные неприятности. Те, чью защиту вы ломали, пожелали\n"
                 f"узнать, кто это такой умный, и им это удалось. Придется вам\n"
                 f"заплатить им ${summ * 2}, и считайте, что дешево отделались!\n")
            summ -= 2 * summ
            you.skill[1] -= 10 * random()
            message(s, 0x4F)
        else:
            you.skill[1] += 5 * random()
            message("Нет такой защиты, которую нельзя было бы сломать!", 0x1F)
        you.money += summ
    elif i == 2:
        if not random() * (you.skill[2] >> 7):
            message("Вам не удалось совладать с железом заказчика\n"
                    "Это не пойдет на пользу вашей профессиональной репутации.", 0x4F)
            you.skill[2] -= 5 * random()
        else:
            you.skill[2] += 5 * random()
            message("Не так страшно кривое железо, как кривые руки...\n"
                    "К счастью, вы этим не страдаете!", 0x1F)
        you.money += summ
    elif i == 3:
        if pay * random() > you.skill[3] * 2:
            message("Плакали ваши денежки...", 0x4F)
            you.skill[3] -= random(5)
            # break
        elif not random() * (you.skill[3] >> 7):
            s = (f"Пора бы знать, что честный бизнес таких прибылей не приносит.\n"
                 f"Те, кого вы пытались кинуть, оказались не лохами, и теперь \n"
                 f"вам придется заплатить им ${summ}!\n")
            message(s, 0x4F)
            summ -= summ
            you.skill[3] -= 10 * random()
        else:
            you.skill[3] += 5 * random()
            message("Дело было рискованным, но риск себя оправдал.", 0x1F)
        you.money += summ
    # free(s)
    return 1


class Netmail(Echo):
    def __init__(self):
        super().__init__(0)
        self.izverg = 0
        self.traf = 0
        self.trafk = 0.7

    def event(self):
        return 0


class Local(Echo):
    def __init__(self):
        super().__init__(you)
        self.izverg = 0
        self.traf = 10
        self.trafk = 0.5

    def event(self):
        return 0


class Point(Echo):
    def __init__(self):
        super().__init__(you)
        self.traf = 15

    def event(self):
        return 0


class Exch(Echo):
    def __init__(self):
        super().__init__(you)

    def event(self):
        return 0


class Bllog(Echo):
    def __init__(self):
        super().__init__(you)

    def event(self):
        return 0


class Ruanekdot(Echo):
    def __init__(self):
        super().__init__(you)
        self.izverg = 4
        self.traf = 70
        self.trafk = 0.5

    def event(self):
        return 0


class Job(Echo):
    def __init__(self):
        super().__init__(you)
        self.izverg = 2.0
        self.traf = 35
        self.trafk = 0.2

    def event(self):
        return 0


class Vcool(Echo):
    def __init__(self):
        super().__init__(you)
        self.izverg = 2.0
        self.traf = 45
        self.trafk = 0.45

    def event(self):
        return 0


class Hardw(Echo):
    def __init__(self):
        super().__init__(you)
        self.traf = 100
        self.trafk = 0.4

    def event(self):
        return 0


class Softw(Echo):
    def __init__(self):
        super().__init__(you)
        self.traf = 100
        self.trafk = 0.4

    def event(self):
        return 0


class Fecho(Echo):
    def __init__(self):
        super().__init__(you)
        self.izverg = 0
        self.traf = 1024
        self.trafk = 0.01

    def event(self):
        return 0


def netmail_event():
    traf = 1
    traf += random() * (params.Style * 3) - 2
    if traf < 0:
        traf = 0
    traf *= params.Style / (1.5 + random() * (params.Style * 2) / 4.0)
    while echtime(0) > 24 * 60:
        traf /= 2
    chmood(int(random() * (traf)) >> 2)
    if params.Style == 3:
        if you.friends != 0:
            you.friends -= int(20 * random())
            if you.friends < 0:
                you.friends = 0
    else:
        you.friends += random.randint(0, params.Style + 1) and not random.randint(0, 16)
    for i in range(1, 4):
        if random() * (you.skill[i] >> 6) and not random.randint(0, 10):
            if proposal(i):
                break
    return traf


def local_event():
    traf = 11111111111111
    traf += random() * (params.Style * 2) + random() * (5) - 2
    if you.status > 1:
        if params.Style == 3 or not params.Style:
            traf *= (5.0 - params.Style + random.randint(0, 5)) / 10
    if traf < 0:
        traf = 0
    while echtime(0) > 24 * 60:
        traf /= 2
    chmood(int(random() * (traf)) >> 3)
    return traf


def point_event():
    maxpnt = 555555
    if you.points < maxpnt and not 3 * random():
        d = you.points
        you.points += 4 * random()
        if you.points >= maxpnt:
            you.points = maxpnt
            maxpnt = 0
        chrep((you.points - d) * (4 + 2 * random()))
        if d:
            echoes[1].traf *= float(you.points) / d
        else:
            echoes[1].traf += 5 * random() * you.points
        return 1
    return 0


def ruanekdot_event():
    i = 3 * random()
    chmood(int(i))
    return int(i)


def job_event():
    if not 20 * random() or params.BBSf:
        return 0
    return 1


def vcool_event():
    k = None
    if not 20 * random() or you.reput < 0:
        return 0
    s = 'salloc(80)'
    if random(5) == 0:
        if not you.wprof:
            pass
        k = (random() * (you.reput >> 2) / 10) * 10
        if not k:
            k = 5
        you.income += k
        s = f"Информация из эхи VERY.COOL позволила вам зарабатывать на ${k} больше!"
        message(s, 0x1F)
    elif random(5) == 1:
        if you.ftime < 5 * 60:
            if (k := (random(3) + 1) * 10) < you.wtime - 60:
                you.ftime += k
                you.wtime -= k
                s = f"Информация из эхи VERY.COOL позволила вам освободить {k} минут в день!"
                message(s, 0x1F)
    else:
        k = random() * (you.reput_() >> 3) + 1
        you.money += k
        s = f"Информация из эхи VERY.COOL позволила вам заработать ${k}!"
        message(s, 0x1F)
    # free(s)
    return 1


def fecho_event():
    if not random(5):
        l = random(1024) + 32
        l = incsoft(l)
        you.virus += random(l) < (l >> 5)
        if not random(5):
            you.antiv = params.D
            message("По файлэхе пришел свежий антивирус! Полезная вещь...", 0x1F)
            chmood(1)
        return 1
    return 0


def exch_event():
    if not random(8):
        you.skill[3] += 1


def bllog_event():
    if not random(8):
        you.skill[3] += 1


def hardw_event():
    if not random(3):
        you.skill[2] += 1


def softw_event():
    if not random(3):
        you.skill[1] += 1


def test(tst, N, y, x):
    j = random(N)
    tst[j].mark = 1
    clrbl(y + 1, x + 2, y + 6, x + 49, 0x0F)
    write(y + 1, x + 2, tst[j].qstn)
    for k in range(3):
        s = f"{k + 1}) {tst[j].ans[k]}"
        prn(y + 4 + k, x + 3, s)
    c = 0
    s = 'salloc(50)'
    while not (c > '0' and c < '4'):
        c = getch()
    c -= 0x31
    return tst[j].correct == c


def BBSinfo(n):
    n -= 1
    s = f"Модем на {bps[bbs[n].modem]}\nUploaded {bbs[n].U}\nDownloaded {bbs[n].D}\n"
    if bbs[n].down:
        s += "       DOWN       "
    elif bbs[n].mxtime == -1:
        s += "       TWIT       "
    elif bbs[n].mxtime:
        s += f"Time left {bbs[n].time} min"
    write(14, 2, s)


def session(k1, cps, con, y, x, s):
    p = 100
    bad = 0
    for i in range(1, k1 + 1):
        p = i * 100 // k1
        cps_tmp = int(cps * (.9 + random.randint(0, 21) / 100.0))
        prn(0, 0, f"{p}%  {cps_tmp} cps    ")
        prnc(y, x, s, 0x07)
        params.Time -= 1
        # showtime()
        try:
            cps >>= bad
        except:
            pass
        i -= bad
        if cps <= con / 100:
            prn(0, 0, "Cancelled")
            delay(1500)
            break
        if not random.randint(0, 50 + you.modem * 10):
            bad = 1
        delay(4) # todo 400
    k1 = i - 1
    return p


def loadfile(name, where):
    f = open(name, 'r', encoding='cp866')
    data = f.read()
    result = data.encode('utf8')
    f.close()
    # where.extend(data)
    return data


def callBBS(n, you):
    q = 0
    PicSize = 16 * 50 * 2
    s = [0] * 60
    title = [0] * PicSize
    i = 0
    j = 0
    p = 0
    k1 = 0
    k = random.randint(0, 50)
    con = 0
    cps = 0
    t0 = params.Time
    u = 0
    u1 = 0
    LastBBS = n
    # q = openbox(6, 18, 23, 70, 0x0F)
    if bbs[n].down:
        prn(8, 22, "BBS temporary down... Sorry")
        # goto(all)
    prn(22, 21, "Dialing... Press <ESC> to abort")
    prn(7, 22, "BUSY")
    # while k:
    #     if not params.Time:
    #         break
    #         goto(all1)
    # prn(7, 22, "BUSY")
    # delay(500)
    # if ESC:
    #     goto(all)
    # prn(7, 22, "    ")
    # delay(200)
    # showtime()
    # k -= 1
    # prn(22, 21, "                               ")
    con = min(bps[you.modem], bps[bbs[n].modem])
    s = "CONNECT " + str(con)
    prn(7, 22, s)
    prn(8, 22, "Press <ESC>-<ESC> to enter BBS")
    # while getch() != 27:
    #     pass
    # while getch() != 27:
    #     pass
    # clrbl(7, 19, 22, 69, 0x0F)
    s = str(n + 1) + ".BBS"
    data = loadfile(s, title)
    if len(data) > 0:
        # if i > PicSize:
        #     message("Недопустимый размер картинки! Срочно выходите в ДОС!", 0xCF)
        # title[i] = 0
        # for j in range(16):
        #     scr[(7+j)*160+19*2:7+j*160+19*2+50*2] = title[j*50*2:j*50*2+50*2]
        # anykey()
        prn(0, 0, data)

    if bbs[n].mxtime == -1:
        prn(7, 22, "Пошел ВОН!!!")
        delay(300)
        # all:
        prn(22, 21, " NO CARRIER                     ")
        # anykey()
        # all1:
        BBSf = 0
        params.alltime += t0 - params.Time
        showstat(1, 22, 0x30)
        return
    elif not bbs[n].mxtime:
        prn(7, 22, "Sysop рад приветствовать нового юзера!")
        bbs[n].time = bbs[n].mxtime = 20 + random.randint(0, 5) * 5
    k = min(params.Time, bbs[n].time)
    BBSf = 1
    while True:
    # nxt:
        s = "У вас " + str(k) + " мин."
        prn(22, 21, s)
        # showtime()
        if not k:
            prn(22, 21, "NO CARRIER")
            BBSf = 0
            params.alltime += t0 - params.Time
            closebox(6, 18, 23, 70, q)
            showstat(1, 22, 0x30)
            return

        prn(9, 22, "F - File areas  M - Message areas  G - GoodBye")
        cps = con / (10 + random.randint(0, 10))
        # c = getch()
        # switch(upcase(c)):
        c = 'M'  # todo дебаг выбор
        if c.upper() == 'F':
            prn(9, 22, "File areas")
            prn(11, 23, "U-Upload to us  D-Download to you")
            # c = getch()
            c = 'D'   # todo дебаг выбор
            if c.upper() == 'U':
                try:
                    cmp1 = (int(cps) * k * 60) >> 10
                except Exception as err:
                    cmp1 = 0
                cmp2 = you.soft - bbs[n].D - bbs[n].U
                u = min(cmp1, cmp2)
                if u <= 0:
                    prn(13, 23, "0K send")
                    continue
                if u == u1:
                    k1 = (u << 10) / (cps * 60)
                else:
                    k1 = k
                p = session(k1, cps, con, 13, 23, s)
                if p == 100:
                    k -= k1
                else:
                    k = 0
                    u *= p / 100.0
                bbs[n].time -= k1
                bbs[n].U += u
                s = "   " + str(u) + "K send, CPS " + str(cps)
                prnc(13, 23, s, 0x0F)
                if random.randint(0, you.virus + 1):
                    bbs[n].mxtime = -1
                    message(
                        "Вы закачали на BBS вирус, и сисоп поставил вам twit!\n"
                        "Теперь даже и не пытайтесь звонить сюда!",
                        0x4F)
                    chmood(-(9 - (you.status << 1)))
                    chrep(-5)
                    # goto(all)
                chrep(u >> (9 + (you.reput >> 5)))
                # break
            if c.upper() == 'D':
                u = min((int(cps) * k * 60) >> 10, bbs[n].soft)
                u = min(u, you.hdspace - you.soft - params.os[you.os]['memory'])
                if u == bbs[n].soft or u == you.hdspace - you.soft - params.os[you.os]['memory']:
                    k1 = (u << 10) / (cps * 60)
                else:
                    k1 = k
                p = session(k1, cps, con, 13, 23, s)
                if p == 100:
                    k -= k1
                else:
                    k = 0
                    u *= p / 100.0
                bbs[n].time -= k1
                bbs[n].soft -= u
                bbs[n].D += u
                u = incsoft(u)
                prn(0, 0, f"{u}K received")
                if u:
                    prn(0, 0, s + ", CPS " + str(cps) + "          ")
                prnc(13, 23, s, 0x0F)
                if not u:
                    pass
                    # break
                chmood(u >> 11)
                if not random.randint(0, 10):
                    you.antiv = params.D
                    message("Вы скачали свежий антивирус! Полезная вещь...", 0x1F)
                    chmood(1)
                you.virus += ((lrandom(u) < (u >> 5)))
                # break
            if c.upper() == 27:
                clrbl(7, 19, 22, 69, 0x0F)
                # goto(nxt)
                b1 = (int)(bbs[n].U - (bbs[n].D)) >> 2
                bbs[n].mxtime += 5 * int(random() * b1) >> 8
                if bbs[n].mxtime < 5:
                    bbs[n].mxtime = 5
                elif bbs[n].mxtime > 180:
                    bbs[n].mxtime = 180
                # goto(nxt)
        if c.upper() == 'M':
            prn(9, 22, "Message areas")
            for i in range(2, params.LE):
                if bbs[n].ech[i - 2]:
                    prn(0, 0, f"{i - 1}) {echoes[i].name}")
                    # prn(10 + j, 22, s)
                    j += 1
            # getc:
            c = getch()
            if c > '0' and c < '9' and bbs[n].ech[c - '0' - 1]:
                c -= 0x30 - 1
                if not echoes[c].stat:
                    if k < (echoes[c].traf * echoes[c].trafk):
                        echoes[c].read = k / j * 100.0
                        k1 = k
                    else:
                        k1 = j
                        echoes[c].read = 100
                    k -= k1
                    params.Time -= k1
                    bbs[n].time -= k1
                    if random(100) < echoes[c].read:
                        echoes[c].event()
            elif c != 27:
                pass
                # goto(getc)
            clrbl(7, 19, 22, 69, 0x0F)
            # break
        if c.upper() == 'G':
            clrbl(7, 19, 22, 69, 0x0F)
            prn(22, 21, "NO CARRIER")
            BBSf = 0
            params.alltime += t0 - params.Time
            closebox(6, 18, 23, 70, q)
            showstat(1, 22, 0x30)
            return

    # all:
    prn(22, 21, "NO CARRIER")
    # anykey()
    # all1:
    BBSf = 0
    params.alltime += t0 - params.Time
    closebox(6, 18, 23, 70, q)
    showstat(1, 22, 0x30)


def setpref(list):
    s = None
    for i in range(len(list)):
        if list[i] is None: continue
        if list[i][0] == '*':
            s = pref + list[i][1:]
            list[i] = s


def vircheck(y, x):
    q = None
    i = 0
    t = 0
    if not you.antiv.date:
        message("Дык нету у вас антивируса!", 0x4F)
        return 0
    t = you.soft / (1024 + you.comp * 2048)
    if t >= params.Time:
        message("Сегодня не успеем провериться...", 0x4F)
        return 0
    q = openbox(y, x, y + 6, x + 40, 0x0F)
    prn(y + 1, x + 1, "Antivirus starts...")
    s = 'salloc(15)'
    for i in range(t + 1):
        prn(0, 0, "%lu%% complete", 100 if i == t else i * 100 / t)
        prn(y + 3, x + 2, s)
        params.Time -= 1
        showtime()
        delay(400)
    lstscn = params.D
    i = you.virus / (random() * ((params.D - you.antiv) >> 3) + 1)
    if i:
        prn(0, 0, "%d virus(es) found & cured!", i)
        you.virus -= i
        prnc(y + 4, x + 1, s, 0x0C)
    else:
        prn(y + 4, x + 1, "No viruses found")
    if params.D - you.antiv > 16:
        prn(y + 5, x + 1, "Warning: you antivirus is too old!")
    anykey()
    closebox(y, x, y + 6, x + 40, q)
    # free(s)
    return i


def wear(reli):
    reli *= 0.9992
    i = random()
    return i > reli and not random() * (4 + (echoes[8].read != 0) + (you.skill[2] >> 4))


def decmoney(x):
    if (you.money - x) < 0:
        message("Вы залезли в долги! Это может плохо кончиться!", 0x4F)
        return 1
    else:
        return 0


def chktrf(traf):
    if traf * 1024 / (bps[you.modem] / 10) / 60 > 30:
        message("У вас слишком медленный модем для так��го трафика", 0x4F)
        return 0
    return 1


def echlink(echn=0, y=4, x=10):
    q = None
    i = 0
    j = 0
    traf = 0
    sel = 0
    c = 0
    marks = [' ', '√', 'p']
    if echn:
        sel = echn
        if echoes[sel].stat:
            return 1
    else:
        sel = 2
    q = openbox(y, x, y + 18, x + 40, 0x1E)
    prnc(y + 1, x + 1, "From : ", 0x13)
    prnc(y + 1, x + 8, you.name, 0x1F)
    prnc(y + 2, x + 1, "To   : AreaFix", 0x13)
    for i in range(x + 1, x + 40):
        scrs(y + 3, i, '─')
    scrs(y + 3, x, 195)
    scrs(y + 3, 40 + x, 180)
    for i in range(2, params.E):
        prn(y + 2 + i, x + 2, echoes[i].name)
        if echoes[i].stat:
            scrs(y + 2 + i, x + 1, '+')
            traf += echoes[i].traf
    # select:
    for i in range(x + 2, x + 30):
        scra(y + 2 + sel, i, 0x0F)
    c = getch()
    # switch(upcase(c)):
    if c.upper() == 27:
        c = 0
        # goto(all)
    if c.upper() == 13:
        # selected:
        c = 1
        # all:
        if not chktrf(traf):
            echn = 0
            # goto(select)
        if echn and not echoes[echn].stat:
            c = 0
        for i in range(params.LE + 1, params.E):
            if not echoes[i].stat:
                # delecho(i)
                chrep(-4 - random(3))
            else:
                i += 1
        closebox(y, x, y + 18, x + 40, q)
        return c
    if c.upper() == 32:
        if echoes[sel].stat:
            echoes[sel].stat = 0
            traf -= echoes[sel].traf
            scrs(y + 2 + sel, x + 1, '-')
            if sel > params.LE:
                message("Учтите - ваша эха без ��ас не выж��вет!", 0x4F)
        else:
            if echoes[sel].plus < 3:
                if chktrf(traf + echoes[sel].traf):
                    traf += echoes[sel].traf
                    echoes[sel].stat = 1 if sel <= params.LE else 2
                    echoes[sel].dl = params.D
                    echoes[sel].msg = echoes[sel].newm = echoes[sel].new1 = 0
        if echn:
            # goto(selected)
            pass
        # break
    if c.upper() == 73:  # PgUp
        if sel > 2:
            for i in range(x + 2, x + 30):
                scra(y + 2 + sel, i, 0x1E)
            sel = 2
        # break
    if c.upper() == 81:  # PgDn
        if sel < params.E - 1:
            for i in range(x + 2, x + 30):
                scra(y + 2 + sel, i, 0x1E)
            sel = params.E - 1
        # break
    if c.upper() == 72:
        for i in range(x + 2, x + 30):
            scra(y + 2 + sel, i, 0x1E)
        sel = params.E - 1 if sel == 2 else sel - 1
        # break
    if c.upper() == 80:
        for i in range(x + 2, x + 30):
            scra(y + 2 + sel, i, 0x1E)
        sel = 2 if sel == params.E - 1 else sel + 1
        # break
    # goto(select)
    # all:
    closebox(y, x, y + 18, x + 40, q)
    return 0


def readres(k):
    if params.Style == 3:
        chrep((random(5) - 3) * k)
        chmood(random(6) - 1)
    elif params.Style == 2:
        chrep(random(k + you.moder * 2))
        chmood(random() * (k >> 1))
    elif params.Style == 1:
        if k:
            chrep(random(you.moder + 2))
            chmood(random() * (2))


def echread(au=1, y=6, x=2):
    q = None
    i = 0
    j = 0
    k = 0
    l = 0
    t = 0
    lost = 0
    lim = 0
    sel = 0
    traf = 0
    c = 0
    marks = [' ', '√', 'p']
    echn = 33333
    if echn:
        sel = echn
        if echoes[sel].stat:
            return 1
    else:
        sel = 2
    q = openbox(y, x, y + params.LE + 7, x + 74, 0x1B)
    prnc(y + 1, x + 1, "From : ", 0x13)
    prnc(y + 1, x + 8, you.name, 0x1F)
    prnc(y + 2, x + 1, "To   : AreaFix", 0x13)
    for i in range(x + 1, x + 74):
        scrs(y + 3, i, '─')
    scrs(y + 3, x, 195)
    scrs(y + 3, x + 74, 180)
    for i in range(2, params.E):
        prn(y + 2 + i, x + 2, echoes[i].name)
        if echoes[i].stat:
            scrs(y + 2 + i, x + 1, '+')
            traf += echoes[i].traf
    # select:
    for i in range(x + 2, x + 73):
        scra(y + 1 + sel, i, 0x0F)
    c = getch()
    # switch(upcase(c)):

    if c.upper() == 27:
        pass
        # goto(all)
    if c.upper() == 13:
        # if echoes[area[sel]].mark & 2:
        # goto(rd3)
        # params.Time -= (t = echtime1(area[sel], echoes[area[sel]].newm))
        # if not t:
        #     goto(rd3)
        rd = 1.0
        # if params.Time <= 0:
        #     rd = (t + Time - 1.0) / t
        #     Time = 1
        #     alltime += Time - 1
        # else:
        #     alltime += t
        # if not (j = echoes[area[sel]].newm * rd):
        #     goto(rd3)
        # goto(mesread)
        # rd3:
        #         if autor == 1:
        #             goto(rd0)
        # elif autor == 2:
        # goto(rd4)
        # break
        # if c.upper() == 32:
        #     if echoes[area[sel]].mark & 2:
        #         break
        #     if echoes[area[sel]].newm:
        #         t = echtime1(area[sel], 1)
        #     else:
        # break
        if t >= params.Time:
            t = 0
            # break
        params.Time -= t
        params.alltime += t
        j = 1
        # rd = 1.0 / echoes[area[sel]].new1
        # goto(mesread)
    if c.upper() == 73:  # PgUp
        if sel > 2:
            for i in range(x + 2, x + 73):
                scra(y + 1 + sel, i, 0x1B)
            sel = 2
        # break
    if c.upper() == 81:  # PgDn
        if sel < l - 1:
            for i in range(x + 2, x + 73):
                scra(y + 1 + sel, i, 0x1B)
            sel = l - 1
        # break
    if c.upper() == 72:
        for i in range(x + 2, x + 73):
            scra(y + 1 + sel, i, 0x1B)
        sel = l - 1 if sel == 2 else sel - 1
        # break
    if c.upper() == 80:
        for i in range(x + 2, x + 73):
            scra(y + 1 + sel, i, 0x1B)
        sel = 2 if sel == l - 1 else sel + 1
        # break
    # goto(select)
    # all:
    closebox(y, x, y + params.LE + 7, x + 74, q)
    return 0


def tstbit(x, n):
    return (x & (1 << n)) != 0


def buycomp(wait=0):
    ar = [None] * 8
    var = [None] * 6
    vars = [[0] * 2 for _ in range(5)]  # цена, надежность
    warn = "Не можете же вы жить совсем без компьютера!"
    s = [None] * 12 * 5
    q = None
    i = 0
    n = 0
    k = 0
    j = 0
    cpr = 0
    if not wait:
        j = random.randint(0, 2) + 2
        s = "На поиск предложений ушли " + str(j) + " " + end(j, end2) + "..."
        message(s, 0x71)
    else:
        j = wait
    for _ in range(j):
        pass
        # if tstbit(newday(), 1):
        #     goto(all)
    cpr = 0 if you.comp == 0xFF else cprice[you.comp] * 0.9
    while cprice[i] <= you.money and i < 7:
        ar[i] = comp[i]
        i += 1
    ar[i] = None
    q = 'malloc(22*10*2)'
    # gettext(4, 11, 25, 20, q)
    # sel:
    i = menuncl(10, 3, 0x2F, 0x0F, ar, "Компьютеры", 1)
    if i:
        i -= 1
        n = 1 + random.randint(0, echoes[3].read // 25)
        for k in range(n):
            vars[k][1] = 24576 + random.randint(0, 8192)
            vars[k][0] = cprice[i] * (0.8 if you.skill[3] > 640 else (1.2 - you.skill[3] / 1600.0)) * vars[k][1] / (
                        24576 + random.randint(0, 8192))
            s = "$%-4d  " % vars[k][0]
            if echoes[4].read:
                s += "  %2d%%" % (vars[k][1] * 100 // 32768)
            var[k] = s
        var[n] = None
        # sel1:
        j = menu(10, 14, 0x70, 0x0F, var, " Цена  ��адежн." if echoes[4].read else "Цена", 1)
        if not j and you.comp == 0xFF:
            message(warn, 0x4F)
            # goto(sel1)
        if j:
            decmoney(vars[j - 1][0] - cpr)
            if you.comp != 0xFF:
                chmood((i - you.comp) * (random.randint(0, 3) + 1))
            you.comp = i
            you.creli = vars[j - 1][1]
            if params.os[you.os].mincomp > you.comp:
                you.os = 0
                if you.osreq:
                    you.wdate = params.D + 6
            # newc += 1
            if cpr:
                s = "Ваш старый компьютер продан за $" + str(cpr)
                message(s, 0x71)
    else:
        if you.comp == 0xFF:
            message(warn, 0x4F)
            # goto(sel)
    # puttext(4, 11, 25, 20, q)
    # free(q)


# all:
#     free(s)

def buymodem(wait=0):
    ar = [None] * 7
    var = [None] * 6
    vars = [[0] * 2 for _ in range(5)]  # цена, надежность
    s = [None] * 70 + 12 * 5
    q = None
    i = 0
    n = 0
    k = 0
    j = 0
    mpr = 0
    traf = 0
    if not wait:
        j = random.randint(0, 2) + 2
        s = "На поиск предложений ушли " + str(j) + " " + end(j, end2) + "..."
        message(s, 0x71)
    else:
        j = wait
    for _ in range(j):
        pass
        # if tstbit(newday(), 0):
        #     goto(all)
    mpr = 0 if you.modem == 0xFF else mprice[you.modem] * 0.9
    while mprice[i] <= you.money and i < 6:
        ar[i] = str(bps[i])
        i += 1
    ar[i] = None
    q = 'malloc(14*14*2)'
    # gettext(4, 11, 15, 24, q)
    # sel:
    i = menuncl(10, 3, 0x2F, 0x0F, ar, "Модемы", 1)
    if i:
        i -= 1
        n = 1 + random.randint(0, echoes[3].read // 25)
        for k in range(n):
            vars[k][1] = 24576 + random.randint(0, 8192)
            vars[k][0] = mprice[i] * (0.8 if you.skill[3] > 640 else (1.2 - you.skill[3] / 1600.0)) * vars[k][1] / (
                        24576 + random.randint(0, 8192))
            s = "$%-4d  " % vars[k][0]
            if echoes[4].read:
                s += "  %2d%%" % (vars[k][1] * 100 // 32768)
            var[k] = s
        var[n] = None
        # sel1:
        j = menu(10, 14, 0x70, 0x0F, var, " Цена  Надежн." if echoes[4].read else "Цена", 1)
        # if not j and you.modem == 0xFF:
        #     message(warn, 0x4F)
        #     goto(sel1)
        if j:
            decmoney(vars[j - 1][0] - mpr)
            if you.modem != 0xFF:
                chmood((i - you.modem) * (random.randint(0, 3) + 1))
            if mpr:
                s = "Ваш старый модем ��родан за $" + str(mpr)
                message(s, 0x71)
            you.modem = i
            you.mreli = vars[j - 1][1]
            # newm += 1
    else:
        if you.modem == 0xFF:
            pass
            # message(warn, 0x4F)
            # goto(sel)
    # puttext(4, 11, 15, 24, q)
    # free(q)
    # all:
    #     free(s)
    if you.status:
        for i in range(2, params.E):
            if echoes[i].stat:
                traf += echoes[i].traf
        if not chktrf(traf):
            echlink()


def buyhd(wait=0):
    ar = [None] * 8
    var = [None] * 6
    vars = [[0] * 2 for _ in range(5)]  # цена, надежность
    s = [None] * 70 + 12 * 5
    q = None
    i = 0
    n = 0
    k = 0
    j = 0
    hpr = 0
    if not wait:
        j = random.randint(0, 2) + 2
        s = "На поиск предложений ушли " + str(j) + " " + end(j, end2) + "..."
        message(s, 0x71)
    else:
        j = wait
    for _ in range(j):
        newday()  # if tstbit(,0) goto all;
    hpr = (hprice[you.hd] >> 1) * float(you.hdspace) / (hd[you.hd] << 10) if BB() else hprice[you.hd] * 0.9
    while hprice[i] <= you.money and i < 7:
        ar[i] = str(hd[i])
        i += 1
    ar[i] = None
    q = 'malloc(14*14*2)'
    # gettext(4, 11, 15, 24, q)
    # sel:
    i = menuncl(10, 3, 0x2F, 0x0F, ar, "Винты", 1)
    if i:
        i -= 1
        n = 1 + random.randint(0, echoes[3].read // 25)
        for k in range(n):
            vars[k][1] = 24576 + random.randint(0, 8192)
            vars[k][0] = hprice[i] * (0.8 if you.skill[3] > 640 else (1.2 - you.skill[3] / 1600.0)) * vars[k][1] / (
                        24576 + random.randint(0, 8192))
            s = "$%-4d  " % vars[k][0]
            if echoes[4].read:
                s += "  %2d%%" % (vars[k][1] * 100 // 32768)
            var[k] = s
        var[n] = None
        j = menu(10, 14, 0x70, 0x0F, var, " Цена  Надежн." if echoes[4].read else "Цена", 1)
        # if not j:
        #     goto(all1)
        decmoney(vars[j - 1][0] - hpr)
        chmood((i - you.hd) * (random.randint(0, 3) + 1))
        if hpr:
            s = "Ваш старый винт продан за $" + str(hpr)
            message(s, 0x71)
        you.hd = i
        you.hreli = vars[j - 1][1]
        you.hdspace = hd[you.hd] << 10
        if you.hdspace < params.os[you.os].size:
            you.os = 0
            if you.osreq:
                you.wdate = params.D + 6
        if you.soft + params.os[you.os].size > you.hdspace:
            incsoft(you.hdspace - you.soft - params.os[you.os].size)
        # newh += 1


# all1:
#     puttext(4, 11, 15, 24, q)
#     free(q)
# all:
#     free(s)

def buysoft():
    ar = ["Антивирус", "Софт для работы", "Игрушки", None]
    var = [None] * 5
    vars = [[0] * 2 for _ in range(5)]  # цена, объем
    s = [None] * 15 * 5
    q = None
    i = 0
    n = 0
    k = 0
    j = 0
    cpr = 0
    if params.Time < 2 * 60 + 5:
        message("Сегодня не успеем...", 0x4F)
        # goto(all)
    params.Time -= 2 * 60
    q = 'malloc(22*10*2)'
    # gettext(4, 11, 25, 20, q)
    # sel:
    i = menuncl(10, 3, 0x2F, 0x0F, ar, "Виды софта", 1)
    if i:
        i -= 1
        if i == 0:
            n = 1
            vars[0][0] = 10
            vars[0][1] = 0
        else:
            n = random.randint(0, 5) + 1
        for k in range(n):
            if i:
                vars[k][1] = 5 + random.randint(0, 200 // i)
                vars[k][0] = (vars[k][1] * (5 - i * 2 + random.randint(0, 3))) // (i * 2) + random.randint(0, 5) + 1
            s = "$%-4d  " % vars[k][0]
            if i:
                s += "  %3dM" % vars[k][1]
            var[k] = s
        var[n] = None
        # sel1:
        j = menu(10, 14, 0x70, 0x0F, var, " Цена  Объем" if i else "Цена", 1)
        # if not j:
        #     goto(all1)
        if vars[j - 1][0] > you.money:
            message("У вас не хватает денег", 0x4F)
            # goto(sel1)
        if you.soft + params.os[you.os].size + vars[j - 1][1] * 1024 > you.hdspace:
            message("У вас не хватает места на винте", 0x4F)
            # goto(sel1)
        decmoney(vars[j - 1][0])
        you.soft += vars[j - 1][1] * 1024
        params.Time -= 3 + random.randint(0, 3)
        if i == 0:
            you.antiv = params.D
        elif i == 1:
            k = you.wprof if you.wprof else 1
            you.skill[k] += (vars[j - 1][1] >> 4) * random.randint(0, 3)
        elif i == 2:
            chmood((vars[j - 1][1] >> 5) * (random.randint(0, 3) + 4))
    showstat()
    showtime()
    # if Time > 5:
    #     goto(sel)


# all1:
#     puttext(4, 11, 25, 20, q)
#     free(q)
# all:
#     free(s)

def worktime():
    d = 0
    i = 0
    t = 0
    s = 'salloc(2048)'
    if not you.wprof:
        return
    if you.wtime > 0:
        you.wdays += 1
    if params.D.weekday() < 5:
        d = random() * (you.wtime // 120)
        if params.Time > you.wtime and random() * (you.wtime // 90) and d - random() * (you.tired >> 2) // 2:
            you.skill[you.wprof] += d
            if not random(20):
                if d > 0:
                    d = random() * (you.income // 20) + 5
                    s = ("Рост вашей квалиф��кации не прошел незамеченным -\n"
                         "        вам подняли зарплату на $") + str(d)
                else:
                    d = random() * (you.income // 20) + 5
                    s = "Усталость плохо сказывается на вашей работе.\nВаша зарплата уменьшена на $" + str(d)
                message(s, 0x1F)
                you.income += d
        t = min(you.wtime, params.Time - 1)
        you.tired += random() * (t // 30) + (t // 30 - 6 * 2) if t > 8 * 60 else 0
        params.Time -= you.wtime
        if params.Time < 0:
            prn(0, 0, "Вы уделяете недостаточно внимания работе!")
            if random() * (-params.Time) > 30:
                d = params.Time / 2 / you.wtime * you.income
                d = (d / 5) * 5
                if d < -50 or you.income + d < 50:
                    prn(0, 0, s + i, " Вы уволены!")
                    fire()
                else:
                    prn(0, 0, s + i, "\nВаша зарплата уменьшена на $%d" % -d)
                    you.income += d
            message(s, 0x4F)
            params.Time = 1
    # free(s)


def studtime():
    t = 0
    d = 1.0
    if not you.sprof or you.sdays < 0:
        return
    if params.D.weekday() == 6 and (you.spay > 0 or you.spay < 0 and studper(params.D)):
        return
    if you.spay < 0:
        if params.D == 25.01 or params.D == 25.06:
            if you.mark < 3.0:
                message("Вы завалили сессию и отчислены из института!", 0x4F)
                expel()
                return
            elif you.mark < 4.5:
                message("Вы таки сдали сессию...", 0x1F)
                you.spay = -30
                chmood(5)
            elif you.mark < 5.0:
                message("Вы сдали сессию хорошо и заработали повышенную стипендию!", 0x1F)
                you.spay = -40
                chmood(10)
            else:
                message("Вы сдали сессию отлично и заработали максимальную стипендию!", 0x1F)
                you.spay = -50
                chmood(15)
        if studper(params.D) == 2:
            return
        if (params.D == 2.01 or params.D == 1.06) and you.mark < 2.5:
            message("Вы даже не смогли сдать зачеты!\n Вы отчислены из института.", 0x4F)
            expel()
            return
        d = you.intens / 100.0
        t = 6 * 60.0 * d
    else:
        t = 2 * 60
    if params.Time < t:
        d *= params.Time / t
        t = params.Time - 1
        message("Вы уделяете недостаточно внимания учебе!", 0x4F)
    params.Time -= t
    d /= (1 + random() * (you.tired >> 2) / 8.0)
    you.skill[you.sprof] += d * (random(4))
    you.mark = (you.mark * you.sdays + 4.75 * d) / (you.sdays + 1)
    you.sdays += 1
    if you.mark > 5.0:
        you.mark = 5.0
    elif you.mark < 2.0:
        you.mark = 2.0
    you.tired += random() * (t / 30) + (t > 6 * 60 and (t / 30 - 6 * 2) or 0)
    chmood(-random() * (you.tired >> 2) / 2)


def joytime():
    i = 0
    t = 0
    r = 0.0
    you.expens = -150
    for i in range(4):
        if params.occup[i].ord == 4:
            break
    if i == 3:
        return
    i += 1
    you.expens -= 150 / i
    t = (random() * (8) + 1) / (i + 1) * 60
    if t > params.Time:
        r = params.Time / t
    else:
        r = 1.0
    chmood(random() * (8 - i) * r)
    params.Time -= min(params.Time - 1, t)


def mailtime():
    l = 0
    i = 0
    d = 0
    k = 0
    lim = 0
    lost = 0
    traf = 0
    s = 'salloc(2048)'
    for i in range(10):
        bbs[i].time = bbs[i].mxtime
        bbs[i].soft += random(150 * (bbs[i].modem + 1))
    for i in range(params.E):
        if params.D.day() == params.SD.day() and echoes[i].stat != 2 and echoes[i].izverg and not random(4):
            prn(0, 0, "Moderator of %s", echoes[i].name)
            fidomess(s, "All", "АМНИСТИЯ", "В эхе проводится subj! Все плюсы аннулированы.")
            echoes[i].plus = 0
        if echoes[i].read - 25 < 0:
            echoes[i].read = 0
        if echoes[i].stat:
            if not params.Down:
                k += 1
                if echoes[i].stat == 2:
                    if not echoes[i].read:
                        echoes[i].traf *= (5.0 - params.Style + random(5)) / 10
                    if echoes[i].traf <= 2:
                        prn(0, 0, "Модерируемая вами эха %s загнулась! Трафик упал до 0.", echoes[i].name)
                        message(s, 0x4F)
                        # delecho(i)
                        chmood(-10)
                        chrep(-4 - params.Style)
                        block(1, 24, 0xF)
                        showstat(1, 22, 0x30)
                        break
                else:
                    if i and (echoes[i].traf + 6 * random() - 3) <= 2:
                        echoes[i].traf = 5 * random() + 5
                    if (echoes[i].mark < 2 or you.points) and random() * (echoes[i].new1) + 1 > echoes[i].newm:
                        echoes[i].moderatorial()
                if i and random() * (echoes[i].new1) + 1 > echoes[i].newm and random() * (params.Style):
                    echoes[0].msg += 1
                    echoes[0].newm += 1
                    echoes[0].new1 += 1
                if echodescr[i] != None and echoes[i].traf / 2 >= 1000:
                    echoes[i].traf = 1800
                echoes[i].newm += echoes[i].traf / 2
                echoes[i].msg += echoes[i].traf / 2
                lim = (echoes[i].traf / 200 + 1) * 100
                if echoes[i].msg > lim:
                    echoes[i].msg = lim
                if echoes[i].newm > lim:
                    if echoes[i].mark < 2:
                        lost += echoes[i].newm - lim
                    echoes[i].newm = lim
                echoes[i].new1 = echoes[i].newm
        else:
            if echoes[i].dl == params.D:
                echoes[i].plus = 0
            if random() * (you.points) > random() * (16) and echoes[i].plus < 3 and not params.Down and i > 1:
                prn(0, 0, "Поинты просят подписаться на %s", echoes[i].name)
                message(s, 0x71, 1 + params.auto_[0])
                if not echoes[i].stat:
                    d = you.points
                    you.points *= (8 - random() * (7)) / 10.0
                    echoes[1].traf *= you.points / d
                    d -= you.points
                    chrep(-d * (5 + random(2)))
    # if Down:
    #     goto all
    if lost:
        message("Вы не успеваете читать всю почту, и это портит вам настроение", 0x4F)
        chmood(-(int(random() * (lost)) >> 1) % 30)
    if not chktrf(traf):
        echlink()
    if you.status and not params.Down:
        echread(0)
    chmood(random() * (you.points >> 3))
    if you.sysop:
        l = random(150 * (you.modem + 1))
        l = incsoft(l)
        you.virus += random(l) < (l >> 3)
        params.Time -= l * 0.1 + random(20)
        if params.Time < 0:
            message("Вы не успеваете следить за своей ББС, и это портит вам настроение", 0x4F)
            chmood(-int(random() * (-params.Time) >> 1) % 30)
            Time = 1
    # all:
    # free(s)
    if params.Time < 6 * 60:
        you.tired += (6 * 60 - Time) / 60


import random
import datetime


def newday():
    i = k = t = mpr = cpr = 0
    res = 0
    q = None
    l = b = 0
    arm = ["Откупиться", "Прятаться у друзей", "Идти служить", None]
    s = ""

    if you.tired - (params.Time < 6 * 60) / 30 >= 0:
        you.tired -= (params.Time < 6 * 60) / 30
    else:
        you.tired = 0
    if (you.tired - params.Time / 30.0 * 4) <= 0:
        you.tired = 0
    else:
        chmood(-you.tired % 50)
    params.D += 1
    params.Time = 20 * 60

    if you.tired > 32:
        t = (8 + random.randint(0, 4)) * 60 + 10 + random.randint(0, 10) * 5
        s = f"Вы проспали {t // 60} часов {t % 60} минут!"
        params.Time -= t
        if (you.tired - t / 30.0 * 4) <= 0:
            you.tired = 0
        message(s, 0x4F)

    you.money += round(you.expens / 30.0)

    if not random.randint(20):  # dequalification
        while (i := random.randint(1, 3)) == you.sprof or i == you.wprof:
            pass
        if you.skill[i] > 0:
            you.skill[i] -= 1

    if not random.randint(40):  # устаревание софта
        incsoft(-random.randint(max(you.soft >> 7, min(you.soft, 500))), 0)

    showtime()

    if params.D.month() == 1 and params.D.day() == 1:
        message("\n C Новым Годом! \n", 0x1F)
        for i in range(10):
            if bbs[i].mxtime == -1:
                bbs[i].mxtime = 0
        params.Down += 1
        chmood(random.randint(10))
        you.tries = 0

    if (params.D.month() == 6 or params.D.month() == 1) and you.army == 2 and params.D - params.SD > 2 * 30:
        you.army = 3

    if you.sdays == -1 and params.D.month() == 9 and params.D.day() == 1:
        you.spay = -30
        you.sdays = 1
        message(
            "Вот и началась ваша учеба в институте.\nТеперь вы будете получать $30 стипендии.\nОгромные деньги, не правда ли?",
            0x1F)

    if params.D == you.grad:
        if you.spay < 0:
            s = "Вас есть с чем поздравить - вы окончили институт" + (
                " с красным дипломом" if you.mark >= 4.75 else "") + "!"
            you.skill[you.sprof] += you.mark * 10
            you.army = 0
            message(s, 0x1F)
        else:
            message("Вы окончили платные курсы.", 0x1F)
            you.skill[you.sprof] += 10
        you.sprof = 0
        you.spay = 0

    if you.army == 3 and (params.D.month() == 4 or params.D.month() == 10) and not random.randint(7):
        message("         Пришла повестка на бумажке!!!\nГоворила вам мама - надо в институт поступать...", 0x4F)
        if not params.Stable:
            i = menu(12, 25, 0x70, 0x0F, arm, "Варианты", 1)
            while i == 0:
                pass
            # match i:
            if i == 1:
                q = openbox(10, 29, 14, 52, 0x70)
                prn(12, 30, "Сколько дать? $    00")
                k = 0
                # i = nmbrscrl( & k, 12, 45, min(999, you.money // 100), 1, 1)
                closebox(10, 29, 14, 52, q)
                you.money -= k * 100
                if random.randint(k) >= 20:
                    message("Считайте, что военкомат забыл о вас навсегда!", 0x1F)
                    you.army = 0
                elif random.randint(k) > 5:
                    message("Вам дали отсрочку до следующего призыва.", 0x1F)
                    you.army = 2
                else:
                    message("Взятка не помогла! То ли честный попался, то ли мало дали...", 0x4F)
                    # goto oblom
            if i == 2:
                if random.randint(you.friends):
                    message("На сей раз вы отсиделись, но друзья не могут прятать вас вечно...", 0x1F)
                else:
                    message("Увы, никто не смог вам помочь...", 0x4F)
            # case _:
            #     goto
            #     oblom
        else:
            oblom: block(1, 24, 0x4F)
            message("Вас забрали в армию. Вот, собственно, и все...", 0x4F)
            quit(2)

    if params.D.weekday() == 6 and _month(params.D + 7) != params.D.month() and you.status:
        if yn("Пойдете на сисопку?"):
            t = min(params.Time - 1, 4 * 60 + random.randint(8 * 60))
            params.Time -= t
            chmood(t // 90 + random.randint(you.friends))
            you.money -= random.randint(t // 60)
            you.friends += (random.randint(t // 180) > 0)
            message("Как ни странно, общаться можно не только по модему...", 0x1F)

    for i in range(4):
        (params.occup[i].func)()
        showtime()

    if not params.Down and params.auto_[3] and you.antiv.date and params.D.days() >= params.lstscn.days() + params.auto_[3]:
        vircheck(2, 4)

    if you.spay > 0 or you.spay < 0 and studper(params.D) != 2:
        you.sdays += 1

    if params.D.day() < 20 and random.randint(10) < random.randint(you.friends) and you.money > 100:
        l = random.randint(you.money >> 3) + 5
        s = f"Друг просит ${l} в долг до конца месяца. Дадите?"
        if yn(s, params.auto_[1]):
            you.money -= l
            you.debt -= l
            chrep(random.randint(3) + 1)
        else:
            message("Жадность не способствует дружбе...", 0x4F, 1 + params.auto_[1])
            if random.randint(you.money / l) > 8:
                you.friends -= 1

    if you.wtime > 0 and params.D.weekday() < 5:
        if params.D >= you.wdate:
            you.wdate = 0
            if you.osreq and you.os != you.osreq:
                message("Вы и ваш софт не подходите для этой работы. Вы уволены!", 0x4F)
                fire()
            elif random.randint(you.income) > 80 + (i := random.randint(5) + 1) * 80 and not you.wdate.Date and (
                    you.osreq == i) != you.os:
                s = f"Ваша работа требует перехода на {params.OSnames[you.osreq]}\nУ вас в запасе 6 дней."
                message(s, 0x4F)
                you.wdate = params.D + 6
                if params.auto_[2] == 1:
                    instOS(you.osreq)

    for i in range(10):
        if not random.randint(20):
            bbs[i].down = not bbs[i].down
            if not bbs[i].down:
                bbs[i].modem = random.randint(6)

    if not params.Stable:
        if not random.randint(60) and you.money > 300:
            l = random.randint(you.money >> 1) + 50
            s = f"Из-за финансового кризиса вы потеряли ${l}"
            message(s, 0x4F)
            chmood(-l / you.money * 32.0)
            you.money -= l
        if you.wprof:
            if not random.randint(50):
                message("Из-за экономического кризиса ваша фирма лопнула,\n      и вы потеряли работу!", 0x4F)
                you.wdays = 0
                chmood(-10)
                newjob(0, 0, 0)
            elif not random.randint(40):
                k = random.randint(50) + 1
                s = f"Из-за экономического кризиса ваша зарплата уменьшена на {k}%"
                message(s, 0x4F)
                chmood(-(k >> 2))
                you.income *= 1 - k / 100.0

    if not params.Down:
        if you.comp != 0xFF:
            you.virus += random.randint(you.virus + 1)
            if random.randint(you.virus >> 3) and (l := random.randint(you.soft >> 1)):
                s = f"Злобные вирусы погрызли {l}K вашего КРУТОГО СОФТА!"
                message(s, 0x4F)
                # chmood(-(float(l) / (you.soft + 1) * 50 * (2 - (1.0 + random.randint(you.soft >> 9) / (1 + (you.soft >> 8))))))
                incsoft(-l)

                # if wear( & you.hreli):
                # if random.randint(3):
                #     if
                # l := random.randint(you.soft):
                # s = "                        У вас покрылся винт!\nК счастью, не насмерть, но {l}K КРУТОГО СОФТА погибли безвозвратно"
                # message(s, 0x4F)
                # chmood(-(float(l) / (you.soft + 1) * 50 * (
                #             2 - (1.0 + random.randint(you.soft >> 9) / (1 + (you.soft >> 8)))))
                # incsoft(-l)
                # else:
                # b = random.randint((long(hd[you.hd]) << 6))
                # if b > you.hdspace - (3 << 10):
                #     b = you.hdspace - (3 << 10)
                # b = (b >> 2) << 2  # block=4K
                # if b:
                #     l = you.soft * float(b) / you.hdspace
                # i = sprintf(s, "У вас посыпался винт! {b}K ушло в бэд блоки.")
                # if l:
                #     sprintf(s + i, "\n{l}K КРУТОГО СОФТА погибли безвозвратно.")
                # message(s, 0x4F)
                # you.hdspace -= b
                # chmood(-(float(l) / (you.soft + 1) * 50 * (
                #             2 - (1.0 + random.randint(you.soft >> 9) / (1 + (you.soft >> 8)))))
                # incsoft(-l)
                #
                # if you.hdspace < params.os[you.os].size or l > (you.soft >> 1):
                #     s = f"Порушилась операционная система...\nГрузим с дискетки {params.OSnames[0]}"
                # message(s, 0x4F)
                # chmood(-random.randint(you.os + 1))
                # you.os = 0
                # Time -= params.os[0].itime
                # if Time < 1:
                #     Time = 1
                # chmood(-2)
                # if you.osreq:
                #     you.wdate = D + 6
                #
                # elif wear( & you.creli):
                #     match
                # random.randint(5):
                # case
                # 0:
                # k = random.randint(7) + 1
                # s = (f"Сегодня черный день в вашей жизни! Скончался ваш компьютер...\n"
                #      f"      Вы в трауре, станция в дауне на {k} {end(k, end2)}...")
                # message(s, 0x4F)
                # chmood(-8 * (you.comp + 1))
                # Down += k
                # you.comp = 0xFF
                # setbit(res, 1)
                # buycomp(k)
                # case
                # 1 | 2 | 3:
                # i = random.randint(cprice[you.comp]) + 1
                # k = random.randint(3) + 2
                # s = f"  Вашему компьютеру потребовался ремонт.\nЭто обошлось вам в ${i} и {k} дня дауна..."
                # message(s, 0x4F)
                # Down += k
                # if decmoney(i):
                #     chmood(-10)
                # else:
                #     chmood(-i * 50 / (you.money + i))
                #
                # elif wear( & you.mreli):
                # k = random.randint(4) + 1
                # s = f"Горе-то какое... Модем у вас сгорел, однако!\nВаша станция в дауне на {k} {end(k, end2)}..."
                # message(s, 0x4F)
                # Down += k
                # chmood(-4 * (you.modem + 1))
                # you.modem = 0xFF
                # setbit(res, 0)
                # buymodem(k)
                #
                # if D.day() == SD.day():
                #     if
                # you.wdays < 30:
                # if you.wdays >= 7:
                #     you.money += you.income * (float(you.wdays % 30) / 30)
                # else:
                #     you.money += you.income
                # you.money -= you.spay
                #
                # if you.debt < 0:  # должны тебе
                #     if
                # random.randint(you.reput / 8) > you.friends:
                # l = you.debt


def initech():
    echoes = []
    for i in range(0, params.LE + 6):
        echoes.append(Echo(you))

    echoes[1] = Local()
    echoes[2] = Point()
    echoes[3] = Exch()
    echoes[4] = Bllog()
    echoes[5] = Ruanekdot()
    echoes[6] = Job()
    echoes[7] = Vcool()
    echoes[8] = Hardw()
    echoes[9] = Softw()
    echoes[10] = Fecho()
    return echoes


def delay(ms):
    time.sleep(ms / 1000)


def setbmpal(addr, palsz):
    pass


def getfdt(f, dt, tm):
    pass


def setfdt(f, dt, tm):
    pass


def page(p):
    pass


def main():
    q = None
    s = ''
    help = ''
    i = 0
    j = 0
    k = 0
    m = 0
    y = 0
    x = 0
    sel = 0
    l = 0
    c = ''
    tl = []
    tmp = None
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

    # show logo
    # buf = None
    # if setvesa640x480x256():
    #     if loadbmp("fidologo.bmp", buf):
    #         free(buf)
    #         getch()

    # textmode()
    # textattr(0x0F)
    # clrscr()
    lstscn = 0
    # log = fopen("log", "a+t")
    # srand(loww(0x46C))
    prnc(0, 0, " FIDO v.1.8 (C) YuN 1997-99", 0x1F)
    # block(1, 24, 0xF)
    # cursoff()
    # if i = loadfile("readme.fid", help):
    #     help[i] = 0
    # else:
    #     message("Не найден Readme.fid! Так дело не пойдет!", 0x4F)
    #     quit(10)
    if os.path.exists('fido.dat'):
        setpref(echoname)
        echoes = initech()
        # if not load():
        #     prn(0,0, "Ошибка чтения! Видать, не судьба...\nerror code %d  coreleft()=%lu")
        #     message(s, 0x4F)
        # quit(10)
    else:
        SD = params.Date(1, 1, 1990)
        SD.setday(1)
        # memset(you.name, ' ', 30)
        # you.name[0] = 0
        # q = openbox(10, 15, 14, 65, 0x71)
        prn(11, 17, "Введите ваше настоящее имя (латинскими буквами)")
        # prnc(12, 25, you.name, 0x0F)

        # you.name = input()
        you.name = 'John Doe'
        for i in range(0, 22):
            cityname[i] = cities[i]['name']
        # cityname[i] = None
        City = 22
        # if i = menu(0, 50, 0x70, 0x0F, cityname, "Ваш город", 1):
        #     pref = cities[City = --i].pref
        # else:
        #     prn(13, 17, "Префикс вашего города:")
        #     prnc(13, 42, pref, 0x0F)
        #     gotoyx(13, 42)
        # _input(pref, 8)
        citiname = 'Москва'
        pref = 'MO.'
        setpref(echoname)
        month = 1
        # if i = menu(1, 0, 0x70, 0x0F, month, "Месяц", 1):
        #     SD.setmonth(i)
        SD.setmonth(month)
        D = SD
        Stable = 1
        # Stable = menu(6, 20, 0x70, 0x0F, situat, "Обстановка в стране", 1)
        # if Stable:
        #     Stable--
        # i = menu(14, 20, 0x70, 0x0F, profn + 1, "Специализация", 1)
        # i = 1 программирование, i=2 железо, i=3 торговля/менеджмент
        i = 1
        you.skill[i] = 10
        if i == 1:
            you.soft = 2048
        elif i == 2:
            you.comp = 1
        elif i == 3:
            you.money = 400
        # closebox(10, 15, 14, 65, q)
        echoes = initech()
        # q = openbox(10, 10, 15, 70, 0x71)
        write(11, 12, "Вы, наверное, думаете, что вот так сразу и попали в ФИДО?\n"
                      "Как бы не так! Вас пустишь, а вы начнете флеймить и ламер-\n"
                      "ствовать! А это право надо еще заслужить!\n"
                      "Итак, вы начинаете в качестве юзера BBS...")
        anykey()
        # closebox(10, 10, 15, 70, q)
        for i in range(0, 10):
            bbs[i].time = bbs[i].U = bbs[i].D = 0
            bbs[i].soft = int(random.randint(0, 20000))
            bbs[i].name = bbsnames[i]
            bbs[i].modem = random.randint(0, 6)
            bbs[i].down = 1 if random.randint(0, 7) else 0
            for k in range(0, params.LE - 2):
                if random.randint(0, 3):
                    bbs[i].ech[k] = 1
        params.Time = you.ftime

    showstat(1, 22, 0x30)
    # game[1] = logst[Log]

    while True:
        while params.Down:
            newday()
        showhelp()
        # l0:
        # c = getch()
        # if not c:
        #     goto l0
        # c = input()
        c = 'B'
        # switch(c):
        if c.upper() == 'B':  # Главное меню BBS
            bbsmenu[1] = "Прибить" if you.sysop else "Создать"
            # i = menu(12, 25, 0x70, 0x0F, bbsmenu, "BBS", 1)
            i = 1
            # switch (i):
            if i == 1:
                # gettext(1, 15, 21, 21, q = malloc(7 * 22 * 2))
                # i = menuf(1, 0, 0x2F, 0x0F, bbsnames, "BBS", LastBBS + 1, &BBSinfo)
                i = 1
                # puttext(1, 15, 21, 21, q)
                # free(q)
                if i:
                    callBBS(i - 1, you)

            if i == 2:
                k = you.modem + (you.soft >> 12)
                if k > 20:
                    k = 20
                if not you.sysop:
                    q = openbox(10, 21, 14, 59, 0x70)
                    prn(12, 24, "Название BBS")
                    prnc(12, 39, bbsnames[11], 0x0F)
                    # gotoyx(12, 39)
                    bbsnames[11] = 'MyBBS'
                    you.sysop = 1
                    chrep(k)
                    # if _input(bbsnames[11], 18):
                    #     you.sysop = 1
                    #     chrep(k)
                    # closebox(10, 21, 14, 59, q)
                else:
                    you.sysop = 0
                    chrep(-k)
                    prn(0, 0, f"{bbsnames[11]} BBS ликвидирована.\n"
                              f"Но вас еще долго будут доставать модемными\n"
                              f"звонками, и это портит вам настроение.")
                    # message(s, 0x4F)
                    chmood(-((k >> 1) * random()) - 3)

        if c.upper() == 'S':
            # i = menu(12, 25, 0x70, 0x0F, smenu, "Soft", 1)
            i = 1
            # switch (i):
            if i == 1:
                vircheck(2, 4)
            if i == 2:
                instOS()
            if i == 3:
                buysoft()
            if i == 4:
                q = openbox(10, 23, 14, 55, 0x70)
                prn(12, 25, "Сколько % софта оставить:")
                k = 100
                # nmbrscrl(&k, 12, 50, 100)
                you.soft *= k / 100.0
                # closebox(10, 23, 14, 55, q)

        if c.upper() == 'J':
            # i = menu(12, 25, 0x70, 0x0F, jmenu, "Работа", 1)
            i = 1
            # switch (i):
            if i == 1:
                joffer()

            if i == 2:
                newjob(0, 0, 0)

        if c.upper() == 'L':
            # i = menu(12, 25, 0x70, 0x0F, lmenu, "Учеба", 1)
            i = 1
            if not i:
                break
            k = menu(12, 25, 0x70, 0x0F, profn + 1, "Профиль", 1)
            if i < 3 and not k:
                break

            if i == 1:
                if params.D.month() != 6:
                    message("Вступительные экзамены будут в июне!", 0x4F)
                else:
                    if you.tries > 3:
                        message("Попытайте счастья через год!", 0x4F)
                    else:
                        if you.skill[k] * random() < 30:
                            message("Вы не набрали проходной балл", 0x4F)
                            you.tries += 1
                        else:
                            you.sdays = -1
                            you.sprof = k
                            if you.army:
                                you.army = 1
                            you.grad.setdate(20, 5, D.year() + 4)
                            prn(0, 0, "Ну вот вы и студент! Учеба начнется 1 сентября и закончится в мае %d.\n         "
                                      "Если вас не выгонят раньше, разумеется.", you.grad.year())
                            message(s, 0x1F)
                        newday()

            if i == 2:
                if you.money < 100:
                    message("У вас нет даже $100 на первый взнос", 0x4F)
                you.money -= 100
                you.spay = 100
                you.sdays = 1
                if you.army == 1:
                    you.army = 3
                you.grad.setdate(D.day(), D.month() + 3, D.year())
                message("Окончание учебы через 3 месяца", 0x1F)
                you.sprof = k

            if i == 3:
                q = openbox(10, 20, 14, 60, 0x70)
                prn(12, 21, "Интенсивность учебы в ВУЗе      %")
                # nmbrscrl(&you.intens, 12, 49, 200, 10, 10)
                # closebox(10, 20, 14, 60, q)

            if i == 4:
                you.spay = 0
                you.sdays = 0
                you.grad = 0
                you.sprof = 0
                if you.army == 1:
                    you.army = 3

        if c.upper() == 'P':
            if you.status > 1:
                i = menu(12, 25, 0x70, 0x0F, points, "Поинты", 1)
                # switch (i):
                i = 1 # todo дебаг
                if i == 1:
                    if not echoes[2].stat:
                        prn(0, 0, "Подпишитесь на эху %s", echoes[2].name)
                        message(s, 0x4F)
                        break
                    q = openbox(10, 23, 14, 55, 0x70)
                    prn(12, 25, "Сколько поинтов набрать:")
                    # nmbrscrl(&maxpnt, 12, 50, 64, you.points)
                    closebox(10, 23, 14, 55, q)
                if i == 2:
                    q = openbox(10, 23, 14, 57, 0x70)
                    prn(12, 25, "Сколько поинтов оставить:")
                    k = you.points
                    chrep(nmbrscrl(you.points, 12, 50, you.points) * (4 + 3 * random()))
                    if k:
                        echoes[1].traf *= you.points / k
                    maxpnt = 0
                    closebox(10, 23, 14, 57, q)

        if c.upper() == 'F':
            if not you.friends:
                break
            i = menu(12, 25, 0x70, 0x0F, fmenu, "Друзья", 1)
            # switch (i):
            if i == 1:
                if params.Time <= 30:
                    message("Увы, у вас нет на это времени...", 0x4F)
                    break
                j = random() * (params.Time - 30) + 30
                params.Time -= j
                chmood(j / 90 + you.friends * random())
                message("Как ни странно, общаться можно не только по модему...", 0x1F)
            if i == 2:
                l = (you.money - you.debt * 3 + (you.reput >> 3)) / 4 * you.friends
                if l > 0:
                    l = l / 2 + random() * (l / 2)
                if l <= 5:
                    message("Увы, сейчас друзья не могут вам помочь...", 0x4F)
                else:
                    prn(0, 0, "Вы взяли взаймы $%ld до конца месяца", l)
                    message(s, 0x1F)
                    you.money += l
                    you.debt += l

        if c.upper() == 'E':
            if you.status:
                i = menu(12, 25, 0x70, 0x0F, emenu, "Эхоконференции", 1)
                # switch (i):
                if i == 1:
                    echread(1)
                    break
                if i == 2:
                    echlink()
                    break
                if i == 3:
                    if you.moder > 3:
                        message("Вы хотите модерировать слишком много конференций!", 0x4F)
                        break
                    q = openbox(10, 13, 15, 68, 0x70)
                    # echoes[E] = Echo(E)
                    prn(12, 14, "Название конференции")
                    # prnc(12, 36, echoes[E].name, 0x0F)
                    # gotoyx(12, 36)
                    # if not input(echoes[E].name, 29) or not echoes[E].name[0]:
                    #     free(echoes[E].name)
                    #     echoname[E] = None
                    #     delete echoes[E]
                    # else:
                    #     prn(13, 14, "Описание конференции")
                    #     prnc(13, 37, echodescr[E], 0x0F)
                    #     gotoyx(13, 37)
                    #     input(echodescr[E], 29)
                    #     for i in range(0, len(echoname[E])):
                    #         echoname[E][i] = upcase(echoname[E][i])
                    #     echoes[E].stat = 2
                    #     you.moder += 1
                    #     E += 1
                    #     chrep(4)
                    closebox(10, 13, 15, 68, q)
                    break
                if i == 4:
                    # i = menu(12, 25, 0x70, 0x0F, style, "Ваш стиль", Style + 1)
                    if i:
                        Style = i - 1
                    break
                if i == 5:
                    q = openbox(4, 5, 22, 75, 0x70)
                    prn(4, 13, "Эха")
                    prn(4, 37, "Трафик,К")
                    prn(4, 46, "Время,мин")
                    prn(4, 60, "Награды")
                    for i in range(0, params.E):
                        if echoes[i].stat and echoes[i].mark < 2:
                            # prn(0,0,  "%-30s  %4d      %3d", echoes[i].name, echoes[i].traf, echtime(i))
                            l += echoes[i].traf
                            m += echtime(i)
                            prn(5 + k, 7, s)
                            for j in range(0, echoes[i].plus):
                                prn(5 + k, 60 + (j << 2), "[+]")
                            k += 1
                    prn(0, 0, "             Всего              %4ld    %d ч.%02d мин.", l, m / 60, m % 60)
                    prn(21, 6, s)
                    anykey()
                    closebox(4, 5, 22, 75, q)

        if c.upper() == 'U':
            # i = menu(12, 25, 0x70, 0x0F, upgrm, "Что апгрейдим?", 1):
            if i == 1:
                buycomp()
                break
            if i == 2:
                buymodem()
                break
            if i == 3:
                buyhd()
                break
            if i == 4:
                status = you.status
                if status == 0:
                    if not newinfo(2):
                        prn(0, 0, "Читайте эху %s", echoes[2].name)
                        message(s, 0x4F)
                        break
                    if you.reput > 32:
                        q = openbox(10, 14, 10 + 7, 14 + 50, 0x0F)
                        prn(10, 30, "Экзамен по полиси")
                        for i in range(0, 9):
                            qstns[i].mark = 0
                        for i in range(0, 3):
                            pass
                            # if not test(qstns, 9, 10, 14):
                            #     break
                        closebox(10, 14, 10 + 7, 14 + 50, q)
                        if i < 3:
                            message("Учите полиси!", 0x4F)
                            # goto ref
                            break
                        message("Вы получили поинтовый адрес! Теперь вы фидошник. Вам больше не надо\n"
                                "читать почту с ББС, вы можете подписываться на эхи и даже создавать\n"
                                "свои собственные. Но чтобы стать полноправным членом ФИДО, вам надо\n"
                                "получить нодовый адрес.", 0x1F)
                        chmood(you.status * 2)
                        for i in range(2, params.LE):
                            echoes[i].stat = 0
                        echoes[0].stat = echoes[1].stat = 1
                    else:
                        pass
                        # ref:
                        message("Никто не хочет брать вас поинтом", 0x4F)
                    break
                if status == 1:
                    if you.reput > 128:
                        y = 1
                        x = 1
                        q = openbox(y, x, y + 22, x + 46, 0x1E)
                        prn(y, x + 12, "Укажите пункты заявки")
                        for k in range(0, 30):
                            i = int(21 * random())
                            j = int(21 * random())
                            tl = ndreq[i]
                            ndreq[i] = ndreq[j]
                            ndreq[j] = tl
                        for i in range(0, 21):
                            ndreq[i].mark = 0
                            prn(y + 1 + i, x + 2, ndreq[i].str)
                        sel = 0
                        # select:
                        for i in range(x + 2, x + 44):
                            scra(y + 1 + sel, i, 0x0F)
                        # do
                        c = getch()  # while not c
                        # switch (c):
                        if c == 27:
                            c = 0
                            # goto all
                        if c == 13:
                            c = 1
                            # goto all
                        if c == 32:
                            ndreq[sel].mark ^= 1
                            scrs(y + 1 + sel, x + 1, '√' if ndreq[sel].mark else ' ')
                            break
                        if c == 73:
                            if sel > 0:
                                for i in range(x + 2, x + 44):
                                    scra(y + 1 + sel, i, 0x1E)
                                sel = 0
                            break
                        if c == 81:
                            if sel < 20:
                                for i in range(x + 2, x + 44):
                                    scra(y + 1 + sel, i, 0x1E)
                                sel = 20
                            break
                        if c == 72:
                            for i in range(x + 2, x + 44):
                                scra(y + 1 + sel, i, 0x1E)
                            sel = 0 if sel == 0 else 3
                            break
                        if c == 80:
                            for i in range(x + 2, x + 44):
                                scra(y + 1 + sel, i, 0x1E)
                            sel = 20 if sel == 20 else 0
                            break
                        # goto select
                        # all:
                        closebox(y, x, y + 22, x + 46, q)
                        if not c:
                            break
                        for i in range(0, 21):
                            if ndreq[i].mark ^ ndreq[i].correct:
                                message("Неправильно составлена заявка", 0x4F)
                                # goto ref1
                        message("Вы получили нодовый адрес! Теперь вы полноправный член ФИДО.\n"
                                "Можете набирать поинтов, только помните, что вы отвечаете за\n"
                                "их письма с вашего узла.", 0x1F)
                        chmood(you.status * 2)
                        echoes[1].traf = 0
                        echoes[1].stat = 1
                    else:
                        # ref1:
                        message("Вам отказано в получении нодового адреса", 0x4F)
                    break

                if status == 2:
                    if D.month() != 5:
                        message("Выборы NC будут в мае", 0x4F)
                        break
                    if you.reput > 1000:
                        chmood(you.status * 2)
                        showstat(1, 22, 0x30)
                        final(
                            "          Вы избраны сетевым координатором! Поздравляю!\nПуть от юзера до NC занял у вас ")
                    else:
                        message("Ваша кандидатура не прошла на выборах NC", 0x4F)

        if c.upper() == 'T':
            # i = menu(12, 25, 0x70, 0x0F, tmenu, "Времяпровождение", 1)
            # switch (i):
            if i == 1:
                prncc(24, 0,
                      "\x04 Enter\xFF\ Swap │ \x04 Esc\xFF\ Exit                                                         ",
                      0x70)
                q = openbox(10, 30, 15, 50, 0x70)
                for i in range(0, 4):
                    prn(11 + i, 32, params.occup[i].name)
                i = 1
                # tlbl:
                prnc(10 + i, 32, params.occup[i - 1].name, 0x0F)
                prnc(11 + i, 32, params.occup[i].name, 0x0F)
                # do
                c = getch()  # while not c
                # switch (c):
                if c == 13:
                    tmp = params.occup[i - 1]
                    params.occup[i - 1] = params.occup[i]
                    params.occup[i] = tmp
                    # break
                if c == 27:
                    closebox(10, 30, 15, 50, q)
                    showhelp()
                    # goto all1
                if c == 72:
                    prnc(10 + i, 32, params.occup[i - 1].name, 0x70)
                    prnc(11 + i, 32, params.occup[i].name, 0x70)
                    i = 3 if i == 1 else i - 1
                    break
                if c == 80:
                    prnc(10 + i, 32, params.occup[i - 1].name, 0x70)
                    prnc(11 + i, 32, params.occup[i].name, 0x70)
                    i = 1 if i == 3 else i + 1
                    break
                # goto tlbl
            if i == 2:
                if you.money < 5:
                    message("С такими финансами не до развлечений...", 0x4F)
                else:
                    k = 5
                    q = openbox(10, 24, 15, 56, 0x70)
                    prn(11, 26, "На какую сумму развлекаемся?")
                    scrs(13, 37, '$')
                    # i = nmbrscrl(&k, 13, 38, min(you.money, 999), 5)
                    closebox(10, 24, 15, 56, q)
                    if i:
                        you.money -= k
                        if k > 64:
                            i = (k >> 6) + random() * (k >> 5)
                        else:
                            i = 1
                        params.Down += i
                        prn(0, 0, f"Станция в дауне на {i} {end(i, end2)}")
                        message(s, 0x71)
                        while params.Down:
                            newday()
                        chmood((k >> 3) + random() * (k >> 2) + 1)
                        if i > 4 and you.wtime > 0:
                            message("Развлекаясь, вы совсем забросили работу... и потеряли ее!", 0x4F)
                            fire()
                # break
            if i == 3:
                q = openbox(10, 28, 15, 52, 0x70)
                for i in range(0, 3):
                    prn(11 + i, 30, aut[i])
                    prn(11 + i, 30 + 14, autop[params.auto_[i]])
                prn(0, 0, f"Антивирус {params.auto_[3]} д.")
                prn(14, 30, s)
                i = 0
                # autl:
                chatr(11 + i, 30 + 14, 7, 0x0F)
                # do
                c = getch()  # while not c
                # switch (c):
                if c == 13:
                    if i < 3:
                        # k = menu(10 + i, 30 + 13, 0x70, 0x0F, autop, NULL, 1)
                        if k:
                            k -= 1
                            params.auto_[i] = k
                            prn(11 + i, 30 + 14, autop[params.auto_[i]])
                    else:
                        prn(0, 0, f"{params.auto_[3]}")
                        # gotoxy(45, 15)
                        if input(s, 2):
                            # auto_[3] = atoi(s)
                            prn(0, 0, f"{params.auto_[3]}")
                            prn(14, 30 + 14, s)
                    # break
                if c == 27:
                    closebox(10, 28, 15, 51, q)
                    showhelp()
                    # goto all1
                if c == 72:
                    chatr(11 + i, 30 + 14, 7, 0x70)
                    i = 3 if i == 0 else i - 1
                    break
                if c == 80:
                    chatr(11 + i, 30 + 14, 7, 0x70)
                    i = 0 if i == 3 else i + 1
                    # break
                # goto autl

        if c.upper() == 'N':
            newday()
            # break

        if c.upper() == 'Y':
            if you.name == "Yuri Nesterenko":
                break
            i = 0
            # do:
            #     s[i] = c = getch()
            #     i += 1
            # while c != 13 and i < 10
            # s[i - 1] = 0
            # if not strcmp(s, "rulez"):
            #     you.money += 1000
            # elif not strcmp(s, "cool"):
            #     you.reput += 100
            # elif not strcmp(s, "monster"):
            #     for i in range(1, 4):
            #         you.skill[i] += 100
            # break

        if c.upper() == 'G':
            i = menu(12, 25, 0x70, 0x0F, game, "", 1)
            # switch (i):
            if i == 1:
                if D.weekday() != 6:
                    prn(0, 0, f"Сегодня не воскресенье!\n"
                              f"Вы можете записаться, но ваша репутация уменьшится на {(6 - D.weekday()) * 10}")
                    if not yn(s):
                        break
                    chrep(-k)
                # if not save("fido.dat"):
                    # prn(0,0, f"Ошибка записи! Видать, не судьба...\nerror code {errno}, coreleft()={coreleft()}")
                    # message(s, 0x4F)
                    # if save("reserve.dat"):
                    #     message("Игра успешно сохранена в reserve.dat", 0x1F)
                    # else:
                        # prn(0,0,  "Записаться в reserve.dat тоже не удалось...\nerror code %d  coreleft()=%lu\nСообщите эти цифры автору!\n", errno, coreleft())
                        # message(s, 0x4F)
                break
            if i == 2:
                # Log = not Log
                game[1] = logst[params.Log]
                break
            if i == 3:
                # viewstr(help)
                break
            if i == 4:
                quit(0)

        if c.upper() == 'W':
            chrep((D.weekday() - 6) * 10)
            # save("fido.dat")

        if c.upper() == 'Q':
            quit(0)

    block(1, 24, 0xF)
    if not params.Time:
        newday()
    showstat(1, 22, 0x30)


if __name__ == '__main__':
    main()
