"""
Исходники игры FIDO v. 1.8.
Автор - Юрий Нестеренко
URL: http://yun.complife.net
e-mail: comte@au.ru
При внесении любых модификаций указание моих копирайтов обязательно
"""
import sys
from random import random
from typing import Union

import fido_date
from params import *
from echo import *
from fido_random import random_, _rnd, lrandom
from person import *
from wnds import *


end1 = ("", "а", "ов")
end2 = ("день", "дня", "дней")


def upcase(c):
    return chr(ord(c) & ~0x20)


def setbit(x, n):
    return x | (1 << n)


def tstbit(x, n):
    return x & (1 << n)





# Define the question structure as a class
class Question:
    def __init__(self, qstn, ans, mark, correct):
        self.qstn = qstn
        self.ans = ans
        self.mark = mark
        self.correct = correct

# echoes = [Echo(you) for _ in range(LE+6)]





def delecho(n):
    i = 0
    if n > LE:
        from params import E
        E -= 1
        you.moder -= 1
        echoes[n].name = ''
    del echoes[n]
    for i in range(n, params.E):
        echoes[i] = echoes[i + 1]
        echoname[i] = echoname[i + 1]
        echoes[i].name = echoname[i]
        echodescr[i] = echodescr[i + 1]
    if n > LE:
        echoname[params.E] = None


def final(st):
    s = ' ' * 1024
    ar = [0] * (80 * 24)
    
    s = (f"{st}{D - SD} {end(D - SD, end2)}. За это время вы потратили\n"
         f"на почту {alltime // (24 * 60)} сут. {(alltime % (24 * 60)) // 60} ч. {alltime % (24 * 60) % 60} мин. чистого времени, получили {pluses} плюс{end(pluses)}\n"
         f"в конференциях, сменили {newm} модем{end(newm)} и {newc} компьютер{end(newc)}.")
    showstat(1, 22, 0x30)
    ar = [0] * (80 * 24)
    message(s, 0x1F, 0)
    prnc(24, 0, "Нажмите клавишу \"Anykey\"", 0x74)
    i = 80 * 24
    while i:
        j = random.randint(0, 80 * 24 - 1)
        if ar[j] == 0:
            i -= 1
            ar[j] = 1
            # scrw[j + 0x800 + 80] = scrw[j + 80]
            delay(20)
    anykey()
    page(0)
    quit(0)


def min(a, b):
    return b if a > b else a


def max(a, b):
    return a if a > b else b






def round(f: float) -> int:
    return int(f + (0.5 if f > 0 else -0.5))


def dstodate(days) -> int:
    d, j, i, k, y = 0, 0, 0, 0, 0
    dt = Date()
    y = int(days // 365.25)
    while (y * 365 + ((y + 3) >> 2)) >= days:
        y -= 1
    d = days - d
    if not (y & 0x0003):  # for leap-year
        if d == fido_date.mofs[2] + 1:  # 29 Feb
            dt.setmonth(2)
            dt.setday(29)
        elif d > fido_date.mofs[2]:
            d -= 1
    if d > fido_date.mofs[11]:
        k = 11
    else:
        i, j = 0, 11
        while j > i + 1:
            k = (i + j) >> 1
            if d > fido_date.mofs[k]:
                i = k
            else:
                j = k
        k = i
    dt.setmonth(k + 1)
    dt.setday(d - fido_date.mofs[k])
    dt.setyear(y + 1990)
    return dt.date


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




def anykey():
    prnc(24, 0, "Нажмите клавишу \"Anykey\"", 0x74)




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




def sttime(D):
    if not you.spay:
        return 0
    elif you.spay < 0:
        return 0 if studper(D) == 2 else 6 * 60.0 * you.intens / 100.0
    else:
        return 2 * 60


def showhelp():
    s = ''
    prn(0, 0, f"Game │ BBS Upgrade Job Learn Soft Echoes Points Friends Time Next day")
    prncc(24, 0, s, 0x70)
    # free(s)




def showstat(y=1, x=22, c=0x30, c2=0x3F):
    mood = ["==8~-(E (", "=8~-((", "8~-(", ":~-(", ":-(", ":-/", ":-I", ";-I", ";-)", ":-)", "Ж:-)", "Ж:-))", "Ж8-D",
            "Ж|-))", "Ж|-)))", "Ж|-)))"]
    s = ""
    i = 0
    import wnds
    wnds._box(y, x, y + 17 + you.sysop + you.moder, x + 55, c, SDB)
    prnc(y + 1, x + 2, you.name, c2)
    prn(y + 2, x + 2, f"Статус: {status[you.status]}")
    if you.status > 1:
        prn(0, 0, "(%d поинт%s)" + str(you.points) + ' ' + end(you.points))
        # prnc(y+2, x+17, s, c2)
    if you.sysop:
        y += 1
        prn(0,0,f"Сисоп %c%s BBS {bbsnames[11]}")
        if Down or you.modem == 0xFF:
            prn(0, 0, f'{s + str(i)} (в дауне)')
        else:
            prn(0, 0, f'{s + str(i)} требует {round(75 * (you.modem + 1) * .1 + 10)} мин.в день')
        # prncc(y+2,x+2,s,c)
    for i in range(you.moder):
        prn(y + 3 + i, x + 3, "Модератор ")
        prnc(y + 3 + i, x + 3 + 10, echoes[LE + 1 + i].name, c2)
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
    wtime = sttime(D)
    prn(0, 0, f"Время/сут.: {you.wtime / 60.0} Работа {wtime / 60.0} Учеба  Своб. {(you.ftime - wtime) / 60.0}")
    # prncc(y+6,x+2,s,c)
    mem = os[you.os]['memory'] >> 10
    prn(0, 0, f"ОC: {OSnames[you.os]} занимает {mem} МБ")
    if you.osreq:
        prn(0, 0, f'{s + str(i)} Надо {OSnames[you.osreq]}')
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
        import os
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
        import os
        os.lseek(self.f, -self.size, 1)
        os.write(self.f, self.buff)
        if closef:
            os.close(self.f)


M = Memfile()


def code(name):
    import os
    if M.open(name, os.O_RDWR) == -1:
        return 0
    s = bytearray(f"{M.tm ^ M.dt:04x}{~M.tm:04x}", 'utf-8')
    for i in range(len(M.buff)):
        M.buff[i] ^= s[i % 8]
    return 1


# def save(fname):
#     f = os.open(fname, os.O_CREAT | os.O_WRONLY)
#     os.write(f, D.Date)
#     os.write(f, E)
#     os.write(f, you.status)
#     os.write(f, bbs)
#     for i in range(E):
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
#     e1 = E
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



def OSinfo(n):
    n -= 1
    s = f"Install time {os[n]['memory']} min.\nSpace required {os[n]['memory'] >> 10}M"
    write(14, 2, s)






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
            # q = openbox(10, 11, 12, 45, 0x70)
            echoes[6].read = 0
            s = f"Предложения работы в {echoes[6].name}"
            prn(11, 12 + len(pref) // 2, s)
            n = int(6 * random() + 1)
            for k in range(n):
                vars[k][2] = int(3 * random() + 1)
                vars[k][1] = int(2 * 60 + (12 if Stable else 20) * random() * 30)
                vars[k][0] = int(
                    vars[k][1] / 60.0 * (30 + (you.skill[vars[k][2]] - 64) * random() / 64.0 * 5 + (you.comp - 3) * 5))
                # s = f"{profn[vars[k][2]]<-20}  ${vars[k][0]:<4.0f}        {vars[k][1] / 60.0:.1f} ч."
                # var[k] = s
            var[n] = None
            j = menu(13, 14, 0x70, 0x0F, var, " Профиль              З/п в месяц  Время в день", 1)
            # closebox(10, 11, 12, 45, q)
            if j:
                Down = 1
                newdayf = 1
                newday()
                if you.income + 80 * random() + you.skill[vars[j][2]] / 8 + (
                        you.skill[vars[j][2]] / 4) * random() + random() * (you.comp * 10) < vars[j][0]:
                    message("Вы не прошли собеседование", 0x4F)
                else:  # break  # goto no
                    newjob(vars[j][0], vars[j][1], vars[j][2])



# def test(tst, N, y, x):
#     j = random(N)
#     tst[j].mark = 1
#     clrbl(y + 1, x + 2, y + 6, x + 49, 0x0F)
#     write(y + 1, x + 2, tst[j].qstn)
#     for k in range(3):
#         s = f"{k + 1}) {tst[j].ans[k]}"
#         prn(y + 4 + k, x + 3, s)
#     c = 0
#     s = 'salloc(50)'
#     while not (c > '0' and c < '4'):
#         c = getch()
#     c -= 0x31
#     return tst[j].correct == c


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


def callBBS(n):
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
            # closebox(6, 18, 23, 70, q)
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
                u = min(u, you.hdspace - you.soft - os[you.os]['memory'])
                if u == bbs[n].soft or u == you.hdspace - you.soft - os[you.os]['memory']:
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
                # clrbl(7, 19, 22, 69, 0x0F)
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
            for i in range(2, LE):
                if bbs[n].ech[i - 2]:
                    prn(0, 0, f"{i - 1}) {echoes[i].name}")
                    # prn(10 + j, 22, s)
                    j += 1
            # getc:
            # c = input()
            c = '1'
            c = int(c)
            if c > 0 and c < 9 and bbs[n].ech[c - 1]:
                c -= 1
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
                    if random.randint(0, 100) < echoes[c].read:
                        echoes[c].event()
            elif c != 27:
                pass
                # goto(getc)
            # clrbl(7, 19, 22, 69, 0x0F)
            # break
        if c.upper() == 'G':
            # clrbl(7, 19, 22, 69, 0x0F)
            prn(22, 21, "NO CARRIER")
            BBSf = 0
            params.alltime += t0 - params.Time
            # closebox(6, 18, 23, 70, q)
            showstat(1, 22, 0x30)
            return

    # all:
    prn(22, 21, "NO CARRIER")
    # anykey()
    # all1:
    BBSf = 0
    params.alltime += t0 - params.Time
    # closebox(6, 18, 23, 70, q)
    showstat(1, 22, 0x30)


def setpref(list):
    s = None
    for i in range(len(list)):
        if list[i] is None: continue
        if list[i][0] == '*':
            s = pref + list[i][1:]
            list[i] = s




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


def check_traffic(traf):
    if traf * 1024 / (bps[you.modem] / 10) / 60 > 30:
        message("У вас слишком медленный модем для такого трафика", 0x4F)
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
    # q = openbox(y, x, y + 18, x + 40, 0x1E)
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
        if not check_traffic(traf):
            echn = 0
            # goto(select)
        if echn and not echoes[echn].stat:
            c = 0
        for i in range(LE + 1, params.E):
            if not echoes[i].stat:
                # delecho(i)
                chrep(-4 - random.randint(0, 3))
            else:
                i += 1
        # closebox(y, x, y + 18, x + 40, q)
        return c
    if c.upper() == 32:
        if echoes[sel].stat:
            echoes[sel].stat = 0
            traf -= echoes[sel].traf
            scrs(y + 2 + sel, x + 1, '-')
            if sel > LE:
                message("Учтите - ваша эха без вас не выживет!", 0x4F)
        else:
            if echoes[sel].plus < 3:
                if check_traffic(traf + echoes[sel].traf):
                    traf += echoes[sel].traf
                    echoes[sel].stat = 1 if sel <= LE else 2
                    echoes[sel].dl = D
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
    # closebox(y, x, y + 18, x + 40, q)
    return 0


def readres(k):
    if Style == 3:
        chrep((random.randint(0, 5) - 3) * k)
        chmood(random.randint(0, 6) - 1)
    if Style == 2:
        chrep(random.randint(0, k + you.moder * 2))
        chmood(_rnd(k >> 1))
    if Style == 1:
        if k:
            chrep(random.randint(0, you.moder + 2))
            chmood(_rnd(2))


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
    # q = openbox(y, x, y + LE + 7, x + 74, 0x1B)
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
        #     rd = (t + params.Time - 1.0) / t
        #     params.Time = 1
        #     alltime += params.Time - 1
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
    # closebox(y, x, y + LE + 7, x + 74, q)
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
            if os[you.os].mincomp > you.comp:
                you.os = 0
                if you.osreq:
                    you.wdate = D + 6
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
    s = ''
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
        if not check_traffic(traf):
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
        if you.hdspace < os[you.os].size:
            you.os = 0
            if you.osreq:
                you.wdate = D + 6
        if you.soft + os[you.os].size > you.hdspace:
            incsoft(you.hdspace - you.soft - os[you.os].size)
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
        if you.soft + os[you.os].size + vars[j - 1][1] * 1024 > you.hdspace:
            message("У вас не хватает места на винте", 0x4F)
            # goto(sel1)
        decmoney(vars[j - 1][0])
        you.soft += vars[j - 1][1] * 1024
        params.Time -= 3 + random.randint(0, 3)
        if i == 0:
            you.antiv = D
        elif i == 1:
            k = you.wprof if you.wprof else 1
            you.skill[k] += (vars[j - 1][1] >> 4) * random.randint(0, 3)
        elif i == 2:
            chmood((vars[j - 1][1] >> 5) * (random.randint(0, 3) + 4))
    showstat()
    showtime()
    # if params.Time > 5:
    #     goto(sel)


# all1:
#     puttext(4, 11, 25, 20, q)
#     free(q)
# all:
#     free(s)


import random
import datetime




# def initech():
#     echoes = []
#     for i in range(0, LE + 6):
#         echoes.append(Echo(you))
#
#     import echo
#     echoes[1] = Local()
#     echoes[2] = Point()
#     echoes[3] = Exch()
#     echoes[4] = Bllog()
#     echoes[5] = Ruanekdot()
#     echoes[6] = Job()
#     echoes[7] = Vcool()
#     echoes[8] = Hardw()
#     echoes[9] = Softw()
#     echoes[10] = Fecho()
#     return echoes




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
    import os
    if os.path.exists('fido.dat'):
        setpref(echoname)
        # echoes = initech()
        # if not load():
        #     prn(0,0, "Ошибка чтения! Видать, не судьба...\nerror code %d  coreleft()=%lu")
        #     message(s, 0x4F)
        # quit(10)
    else:
        SD = Date(1, 1, 1990)
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
        # echoes = initech()
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
            for k in range(0, LE - 2):
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
                # i = menuf(1, 0, 0x2F, 0x0F, bbsnames, "BBS", LastBBS + 1, BBSinfo)
                i = 2
                # puttext(1, 15, 21, 21, q)
                # free(q)
                if i:
                    callBBS(i - 1)

            if i == 2:
                k = you.modem + (you.soft >> 12)
                if k > 20:
                    k = 20
                if not you.sysop:
                    # q = openbox(10, 21, 14, 59, 0x70)
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
                # q = openbox(10, 23, 14, 55, 0x70)
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
                if D.month() != 6:
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
                # q = openbox(10, 20, 14, 60, 0x70)
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
                    # q = openbox(10, 23, 14, 55, 0x70)
                    prn(12, 25, "Сколько поинтов набрать:")
                    # nmbrscrl(&maxpnt, 12, 50, 64, you.points)
                    # closebox(10, 23, 14, 55, q)
                if i == 2:
                    # q = openbox(10, 23, 14, 57, 0x70)
                    prn(12, 25, "Сколько поинтов оставить:")
                    k = you.points
                    chrep(nmbrscrl(you.points, 12, 50, you.points) * (4 + 3 * random()))
                    if k:
                        echoes[1].traf *= you.points / k
                    maxpnt = 0
                    # closebox(10, 23, 14, 57, q)

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
                    # q = openbox(10, 13, 15, 68, 0x70)
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
                    # closebox(10, 13, 15, 68, q)
                    break
                if i == 4:
                    # i = menu(12, 25, 0x70, 0x0F, style, "Ваш стиль", Style + 1)
                    if i:
                        Style = i - 1
                    break
                if i == 5:
                    # q = openbox(4, 5, 22, 75, 0x70)
                    prn(4, 13, "Эха")
                    prn(4, 37, "Трафик,К")
                    prn(4, 46, "Время,мин")
                    prn(4, 60, "Награды")
                    for i in range(0, params.E):
                        if echoes[i].stat and echoes[i].mark < 2:
                            prn(0,0,  f"{echoes[i].name}  {echoes[i].traf}      {echo_time(i)}")
                            l += echoes[i].traf
                            m += echo_time(i)
                            prn(5 + k, 7, s)
                            for j in range(0, echoes[i].plus):
                                prn(5 + k, 60 + (j << 2), "[+]")
                            k += 1
                    prn(0, 0, f"Всего   {l}    {m/60}ч. {m%60} мин.")
                    prn(21, 6, s)
                    anykey()

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
                        prn(0, 0, f"Читайте эху {echoes[2].name}")
                        message(s, 0x4F)
                        break
                    if you.reput > 32:
                        # q = openbox(10, 14, 10 + 7, 14 + 50, 0x0F)
                        prn(10, 30, "Экзамен по полиси")
                        for i in range(0, 9):
                            qstns[i].mark = 0
                        for i in range(0, 3):
                            pass
                            # if not test(qstns, 9, 10, 14):
                            #     break
                        # closebox(10, 14, 10 + 7, 14 + 50, q)
                        if i < 3:
                            message("Учите полиси!", 0x4F)
                            # goto ref
                            break
                        message("Вы получили поинтовый адрес! Теперь вы фидошник. Вам больше не надо\n"
                                "читать почту с ББС, вы можете подписываться на эхи и даже создавать\n"
                                "свои собственные. Но чтобы стать полноправным членом ФИДО, вам надо\n"
                                "получить нодовый адрес.", 0x1F)
                        chmood(you.status * 2)
                        for i in range(2, LE):
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
                        # q = openbox(y, x, y + 22, x + 46, 0x1E)
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
                        # closebox(y, x, y + 22, x + 46, q)
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
                prncc(24, 0,"Enter | Swap │ Esc | Exit", 0x70)
                # q = openbox(10, 30, 15, 50, 0x70)
                for i in range(0, 4):
                    prn(11 + i, 32, occup[i].name)
                i = 1
                # tlbl:
                prnc(10 + i, 32, occup[i - 1].name, 0x0F)
                prnc(11 + i, 32, occup[i].name, 0x0F)
                # do
                c = getch()  # while not c
                # switch (c):
                if c == 13:
                    tmp = occup[i - 1]
                    occup[i - 1] = occup[i]
                    occup[i] = tmp
                    # break
                if c == 27:
                    # closebox(10, 30, 15, 50, q)
                    showhelp()
                    # goto all1
                if c == 72:
                    prnc(10 + i, 32, occup[i - 1].name, 0x70)
                    prnc(11 + i, 32, occup[i].name, 0x70)
                    i = 3 if i == 1 else i - 1
                    break
                if c == 80:
                    prnc(10 + i, 32, occup[i - 1].name, 0x70)
                    prnc(11 + i, 32, occup[i].name, 0x70)
                    i = 1 if i == 3 else i + 1
                    break
                # goto tlbl
            if i == 2:
                if you.money < 5:
                    message("С такими финансами не до развлечений...", 0x4F)
                else:
                    k = 5
                    # q = openbox(10, 24, 15, 56, 0x70)
                    prn(11, 26, "На какую сумму развлекаемся?")
                    scrs(13, 37, '$')
                    # i = nmbrscrl(&k, 13, 38, min(you.money, 999), 5)
                    # closebox(10, 24, 15, 56, q)
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
                # q = openbox(10, 28, 15, 52, 0x70)
                for i in range(0, 3):
                    prn(11 + i, 30, aut[i])
                    prn(11 + i, 30 + 14, autop[auto_[i]])
                prn(0, 0, f"Антивирус {auto_[3]} д.")
                prn(14, 30, s)
                i = 0
                # autl:
                # chatr(11 + i, 30 + 14, 7, 0x0F)
                # do
                c = getch()  # while not c
                # switch (c):
                if c == 13:
                    if i < 3:
                        # k = menu(10 + i, 30 + 13, 0x70, 0x0F, autop, NULL, 1)
                        if k:
                            k -= 1
                            auto_[i] = k
                            prn(11 + i, 30 + 14, autop[auto_[i]])
                    else:
                        prn(0, 0, f"{auto_[3]}")
                        # gotoxy(45, 15)
                        if input(s, 2):
                            # auto_[3] = atoi(s)
                            prn(0, 0, f"{auto_[3]}")
                            prn(14, 30 + 14, s)
                    # break
                if c == 27:
                    # closebox(10, 28, 15, 51, q)
                    showhelp()
                    # goto all1
                if c == 72:
                    # chatr(11 + i, 30 + 14, 7, 0x70)
                    i = 3 if i == 0 else i - 1
                    break
                if c == 80:
                    # chatr(11 + i, 30 + 14, 7, 0x70)
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

    # block(1, 24, 0xF)
    if not params.Time:
        newday()
    showstat(1, 22, 0x30)


if __name__ == '__main__':
    main()
