from random import randint

import params
from fido import bbs, echoes, fidomess, message, chmood, chrep, showstat, you, echodescr, check_traffic, echlink, \
    echread, incsoft, fire, studper, expel
from wnds import prn, block


class Toccup:
    def __init__(self, name, ord, func):
        self.name = name
        self.ord = ord
        self.func = func


def mailtime():
    l = 0
    i = 0
    d = 0
    k = 0
    lim = 0
    lost = 0
    traf = 0
    s = ''
    for i in range(10):
        bbs[i].time = bbs[i].mxtime
        bbs[i].soft += randint(0, 150 * (bbs[i].modem + 1))
    for i in range(params.E):
        if params.D.day() == params.SD.day() and echoes[i].stat != 2 and echoes[i].izverg and not randint(0, 4):
            prn(0, 0, f"Moderator of {echoes[i].name}")
            fidomess(s, "All", "АМНИСТИЯ", "В эхе проводится subj! Все плюсы аннулированы.")
            echoes[i].plus = 0
        if echoes[i].read - 25 < 0:
            echoes[i].read = 0
        if echoes[i].stat:
            if not params.Down:
                k += 1
                if echoes[i].stat == 2:
                    if not echoes[i].read:
                        echoes[i].traf *= (5.0 - params.Style + randint(0, 5)) / 10
                    if echoes[i].traf <= 2:
                        prn(0, 0, f"Модерируемая вами эха {echoes[i].name} загнулась! Трафик упал до 0.")
                        message(s, 0x4F)
                        # delecho(i)
                        chmood(-10)
                        chrep(-4 - params.Style)
                        block(1, 24, 0xF)
                        showstat(1, 22, 0x30)
                        break
                else:
                    if i and (echoes[i].traf + 6 * randint(0, 1) - 3) <= 2:
                        echoes[i].traf = 5 * randint(0, 1) + 5
                    if (echoes[i].mark < 2 or you.points) and randint(0, 1) * (echoes[i].new1) + 1 > echoes[i].newm:
                        echoes[i].moderatorial()
                if i and randint(0, 1) * (echoes[i].new1) + 1 > echoes[i].newm and randint(0, 1) * (params.Style):
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
            if randint(0, 1) * (you.points) > randint(0, 1) * (16) and echoes[i].plus < 3 and not params.Down and i > 1:
                prn(0, 0, f"Поинты просят подписаться на {echoes[i].name}")
                message(s, 0x71, 1 + params.auto_[0])
                if not echoes[i].stat:
                    d = you.points
                    you.points *= (8 - randint(0, 1) * (7)) / 10.0
                    echoes[1].traf *= you.points / d
                    d -= you.points
                    chrep(-d * (5 + randint(0, 2)))
    # if Down:
    #     goto all
    if lost:
        message("Вы не успеваете читать всю почту, и это портит вам настроение", 0x4F)
        chmood(-(int(randint(0, 1) * (lost)) >> 1) % 30)
    if not check_traffic(traf):
        echlink()
    if you.status and not params.Down:
        echread(0)
    chmood(randint(0, 1) * (you.points >> 3))
    if you.sysop:
        l = randint(0, 150 * (you.modem + 1))
        l = incsoft(l)
        ttt = randint(0, l) < (l >> 3)
        you.virus += ttt
        params.Time -= l * 0.1 + randint(0, 20)
        if params.Time < 0:
            message("Вы не успеваете следить за своей ББС, и это портит вам настроение", 0x4F)
            chmood(-int(randint(0, 1) * (-params.Time) >> 1) % 30)
            Time = 1
    # all:
    # free(s)
    if params.Time < 6 * 60:
        you.tired += (6 * 60 - params.Time) / 60


def worktime():
    d = 0
    i = 0
    t = 0
    s = ''
    if not you.wprof:
        return
    if you.wtime > 0:
        you.wdays += 1
    if params.D.weekday() < 5:
        d = randint(0, 1) * (you.wtime // 120)
        if params.Time > you.wtime and randint(0, 1) * (you.wtime // 90) and d - randint(0, 1) * (you.tired >> 2) // 2:
            you.skill[you.wprof] += d
            if not randint(0, 20):
                if d > 0:
                    d = randint(0, 1) * (you.income // 20) + 5
                    s = f"Рост вашей квалиффикации не прошел незамеченным - вам подняли зарплату на ${str(d)}"
                else:
                    d = randint(0, 1) * (you.income // 20) + 5
                    s = f"Усталость плохо сказывается на вашей работе.\nВаша зарплата уменьшена на ${str(d)}"
                message(s, 0x1F)
                you.income += d
        t = min(you.wtime, params.Time - 1)
        add = randint(0, 1) * (t // 30) + (t // 30 - 6 * 2) if t > 8 * 60 else 0
        you.tired += add
        params.Time -= you.wtime
        if params.Time < 0:
            prn(0, 0, "Вы уделяете недостаточно внимания работе!")
            if randint(0, 1) * (-params.Time) > 30:
                d = params.Time / 2 / you.wtime * you.income
                d = (d / 5) * 5
                if d < -50 or you.income + d < 50:
                    prn(0, 0, " Вы уволены!")
                    fire()
                else:
                    prn(0, 0, f"Ваша зарплата уменьшена на ${-d}")
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
    d /= (1 + randint(0, 1) * (you.tired >> 2) / 8.0)
    you.skill[you.sprof] += d * (randint(0, 4))
    you.mark = (you.mark * you.sdays + 4.75 * d) / (you.sdays + 1)
    you.sdays += 1
    if you.mark > 5.0:
        you.mark = 5.0
    elif you.mark < 2.0:
        you.mark = 2.0
    you.tired += randint(0, 1) * (t / 30) + (t > 6 * 60 and (t / 30 - 6 * 2) or 0)
    chmood(-randint(0, 1) * (you.tired >> 2) / 2)


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
    t = (randint(0, 1) * (8) + 1) / (i + 1) * 60
    if t > params.Time:
        r = params.Time / t
    else:
        r = 1.0
    chmood(randint(0, 1) * (8 - i) * r)
    params.Time -= min(params.Time - 1, t)


occup = [
    Toccup("Почта      ", 1, mailtime),
    Toccup("Работа     ", 2, worktime),
    Toccup("Учеба      ", 3, studtime),
    Toccup("Развлечения", 4, joytime)
]
