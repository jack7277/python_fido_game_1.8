"""
Модуль проведения времени
- обучение/исключени
- развлечение
- работа
- почта
"""

import random
import params
from echo import check_traffic
from fido_random import _rnd
from mood import chmood
from params import studper
from person import you, incsoft
from toccup import occup
from wnds import message, prn


def expel():  # Исключение из института
    you.skill[you.sprof] -= 10
    if you.skill[you.sprof] < 0:
        you.skill[you.sprof] = 0
    chmood(-10 - random.randint(0, 8))
    you.spay = 0
    you.sdays = 0
    you.grad = 0
    you.sprof = 0
    if you.army == 1:
        you.army = 3


def studtime(you, D, Time):
    t = 0
    d = 1.0
    if not you.sprof or you.sdays < 0:
        return
    if D.weekday() == 6 and (you.spay > 0 or (you.spay < 0 and studper(D))):
        return
    if you.spay < 0:
        if D == 25.01 or D == 25.06:
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
        if studper(D) == 2:
            return
        if (D == 2.01 or D == 1.06) and you.mark < 2.5:
            message("Вы даже не смогли сдать зачеты! Вы отчислены из института.", 0x4F)
            expel()
            return
        d = you.intens / 100.0
        t = 6 * 60.0 * d
    else:
        t = 2 * 60
    if Time < t:
        d *= Time / t
        t = Time - 1
        message("Вы уделяете недостаточно внимания учебе!", 0x4F)
    Time -= t
    d /= (1 + _rnd(you.tired >> 2) / 8.0)
    you.skill[you.sprof] += d * (random.randint(0, 4))
    you.mark = (you.mark * you.sdays + 4.75 * d) / (you.sdays + 1)
    you.sdays += 1
    if you.mark > 5.0:
        you.mark = 5.0
    elif you.mark < 2.0:
        you.mark = 2.0
    you.tired += _rnd(t / 30) + (t / 30 - 6 * 2) if t > 6 * 60 else 0
    chmood(-_rnd(you.tired >> 2) / 2)


def worktime():
    if not you.wprof:
        return
    s = ''
    d, i, t = 0, 0, 0
    if you.wtime > 0:
        you.wdays += 1
    if params.D.weekday() < 5:
        d = _rnd(you.wtime / 120)
        if params.Time > you.wtime and _rnd(you.wtime / 90) and d - _rnd(you.tired >> 2) / 2:
            you.skill[you.wprof] += d
            if not random.randint(0, 20):
                if d > 0:
                    d = _rnd(you.income / 20) + 5
                    s = f"Рост вашей квалификации не прошел незамеченным - вам подняли зарплату на ${d}!"
                else:
                    s = f"Усталость плохо сказывается на вашей работе. Ваша зарплата уменьшена на ${d}!"
                message(s, 0x1F)
                you.income += d
        t = min(you.wtime, params.Time - 1)
        you.tired += _rnd(t / 30) + (t > 8 * 60) * (t / 30 - 6 * 2)
        params.Time -= you.wtime
        if params.Time < 0:
            prn(0, 0, s + " Вы уделяете недостаточно внимания работе!")
            if _rnd(-params.Time) > 30:
                d = (float(params.Time) / 2 / you.wtime * you.income)  # d < 0
                d = (d / 5) * 5
                if d < -50 or you.income + d < 50:
                    prn(0,0, s + str(i) + " Вы уволены!")
                    params.fire()
                else:
                    prn(0,0, s + str(i) + f" Ваша зарплата уменьшена на ${-d}")
                    you.income += d
            message(s, 0x4F)
            Time = 1


def joytime():
    i = 0
    t = 0
    r = 0.0
    you.expens = -150

    for i in range(4):
        if occup[i].ord == 4:
            break

    if i == 3:
        return

    i += 1
    you.expens -= 150 / i
    t = (_rnd(8) + 1) / (i + 1) * 60

    if t > params.Time:
        r = params.Time / t
    else:
        r = 1.0

    chmood(_rnd(8 - i) * r)
    params.Time -= min(params.Time - 1, t)





def mailtime(bbs, echoes, echodescr, Down, Style, you, auto_, E, D, SD):
    lost = 0
    traf = 0
    for i in range(10):
        bbs[i]['time'] = bbs[i]['mxtime']
        bbs[i]['soft'] += random.randint(0, 150 * (bbs[i]['modem'] + 1))

    for i in range(E):
        if D.day() == SD.day() and echoes[i]['stat'] != 2 and echoes[i]['izverg'] and not random.randint(0, 3):
            echoes[i]['plus'] = 0
            echoes[i]['read'] -= 25
            if echoes[i]['read'] < 0:
                echoes[i]['read'] = 0

        if echoes[i]['stat']:
            k = 0
            if not Down:
                k += 1
                if echoes[i]['stat'] == 2:
                    if not echoes[i]['read']:
                        echoes[i]['traf'] *= (5.0 - Style + random.randint(0, 5)) / 10
                    if echoes[i]['traf'] <= 2:
                        echoes[i]['traf'] = random.randint(0, 5) + 5
                        echoes[i]['traf'] = max(echoes[i]['traf'], 0)
                        lim = (echoes[i]['traf'] // 200 + 1) * 100
                        if echoes[i]['msg'] > lim:
                            echoes[i]['msg'] = lim
                        if echoes[i]['newm'] > lim:
                            if echoes[i]['mark'] < 2:
                                lost += echoes[i]['newm'] - lim
                            echoes[i]['newm'] = lim
                        echoes[i]['new1'] = echoes[i]['newm']
                else:
                    if i and (echoes[i]['traf'] + random.randint(0, 6) - 3) <= 2:
                        echoes[i]['traf'] = random.randint(0, 5) + 5
                    if (echoes[i]['mark'] < 2 or you['points']) and random.randint(1, echoes[i]['new1'] + 1) > echoes[i]['newm']:
                        echoes[i]['moderatorial']()
                    if i and random.randint(1, echoes[i]['new1'] + 1) > echoes[i]['newm'] and random.randint(0, Style):
                        echoes[0]['msg'] += 1
                        echoes[0]['newm'] += 1
                        echoes[0]['new1'] += 1
                    if echodescr[i] is not None and echoes[i]['traf'] / 2 >= 1000:
                        echoes[i]['traf'] = 1800
                    echoes[i]['newm'] += echoes[i]['traf'] / 2
                    echoes[i]['msg'] += echoes[i]['traf'] / 2
                    lim = (echoes[i]['traf'] / 200 + 1) * 100
                    if echoes[i]['msg'] > lim:
                        echoes[i]['msg'] = lim
                    if echoes[i]['newm'] > lim:
                        if echoes[i]['mark'] < 2:
                            lost += echoes[i]['newm'] - lim
                        echoes[i]['newm'] = lim
                    echoes[i]['new1'] = echoes[i]['newm']
        else:
            if echoes[i]['dl'] == D:
                echoes[i]['plus'] = 0
            if random.randint(0, you['points']) > random.randint(0, 16) and echoes[i]['plus'] < 3 and not Down and i > 1:
                d = you['points']
                you['points'] *= (8 - random.randint(0, 7)) / 10.0
                echoes[1]['traf'] *= you['points'] / d
                d -= you['points']

    if Down:
        if params.Time < 6 * 60:
            you['tired'] += (6 * 60 - params.Time) / 60
        return
    if lost:
        message("Вы не успеваете читать всю почту, и это портит вам настроение", 0x4F)
        chmood(-((_rnd(lost) >> 1) % 30))
    if not check_traffic(traf):
        pass
    if you['status'] and not Down:
        pass
    if you['sysop']:
        l = random.randint(0, 150 * (you['modem'] + 1))
        l = incsoft(l)
        you['virus'] += random.randint(0, l) < (l >> 3)
        params.Time -= l * 0.1 + random.randint(0, 20)
        if params.Time < 0:
            message("Вы не успеваете следить за своей ББС, и это портит вам настроение", 0x4F)
            chmood(-(_rnd(-params.Time) >> 1) % 30)
            params.Time = 1
    if params.Time < 6 * 60:
        you['tired'] += (6 * 60 - params.Time) / 60
