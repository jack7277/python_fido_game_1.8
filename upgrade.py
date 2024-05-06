"""
UPGRADE MENU:
- Купить компьютер
- Купить модем
- Купить жесткий диск
- Купить ПО/Софт
"""
import random

from echo import check_traffic, echlink, newday
from fido_random import random_
from init import echoes
from money import decmoney
from mood import chmood
from params import end, end2, cprice, comp, os, D, mprice, bps, E, hprice, hd, BB
from person import you
from reputation import chrep
from stat import showstat
from wnds import message, menuncl, menu


# Скачивание софта?
def incsoft(ds, chrp=1):
    mem1 = you.soft + os[you.os]['memory'] + ds
    if mem1 > you.hdspace:
        ds = you.hdspace - you.soft - os[you.os]['memory']
    if not ds:
        return 0
    chrep(random_(ds * you.status / 512) / 2, chrp)
    you.soft += ds
    return ds


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
        for i in range(2, E):
            if echoes[i].stat:
                traf += echoes[i].traf
        if not check_traffic(traf):
            echlink()


def buyhd(wait=0):
    ar = [None] * 8
    var = [None] * 6
    vars = [[0] * 2 for _ in range(5)]  # цена, надежность
    s = [None] * 700
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
    from params import Time
    if Time < 2 * 60 + 5:
        message("Сегодня не успеем...", 0x4F)
        # goto(all)
    Time -= 2 * 60
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
        Time -= 3 + random.randint(0, 3)
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

