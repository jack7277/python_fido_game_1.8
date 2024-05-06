from OS import OSnames
from fido_date import Date
from init import echoes
from person import you
from wnds import prn, SDB, _box, prnc
from params import week, Time, D, dtm, status, end, bbsnames, Down, LE, comp, bps, profn, os


def studper(D):
    if D < Date(D.year, 1, 25) or (Date(D.year, 6, 1) <= D < Date(D.year, 6, 25)):
        return 0  # session
    elif Date(D.year, 9, 1) <= D or (Date(D.year, 2, 6) <= D < Date(D.year, 6, 1)):
        return 1  # semester
    else:
        return 2  # vacations

def sttime(D):
    if not you.spay:
        return 0
    elif you.spay < 0:
        return 0 if studper(D) == 2 else 6 * 60.0 * you.intens / 100.0
    else:
        return 2 * 60


def showtime():
    prn(0, 0,
        f"{week[D.weekday()]}, {D.day()}.{D.month()}.{D.year()}  Осталось {Time / 60} ч. {Time % 60} мин. ")
    prn(0, 32, dtm)


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
