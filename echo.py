from fido_random import _rnd
from init import *
from mood import *
from reputation import chrep
from viruses import vircheck
from wnds import message, fidomess, prn, menu


def echo_time(i):
    k1 = 1 if echoes[i].stat > 2 else echoes[i].stat
    k2 = 1 if you.os > 0 else 1.3
    return round(echoes[i].traf * echoes[i].trafk * (params.Style + 1) * k1 * (11.0 - you.comp / 1.5) * k2 / 10.0)


def echtime1(i, n):
    t = round((n) * 2 * echoes[i].trafk * (params.Style + 1) * (1 if echoes[i].stat > 2 else echoes[i].stat) * (11.0 - you.comp / 1.5) * (1 if you.os > 0 else 1.3) / 10.0)
    if not t and n:
        t = 1
    return t


def check_traffic(traf):
    if traf * 1024 / (bps[you.modem] / 10) / 60 > 30:
        message("У вас слишком медленный модем для такого трафика", 0x4F)
        return 0
    return 1



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

    params.showtime()

    if params.D.month() == 1 and params.D.day() == 1:
        message("\n C Новым Годом! \n", 0x1F)
        for i in range(10):
            if bbs[i].mxtime == -1:
                bbs[i].mxtime = 0
        params.Down += 1
        chmood(random.randint(0, 10))
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
                # q = openbox(10, 29, 14, 52, 0x70)
                prn(12, 30, "Сколько дать? $    00")
                k = 0
                # i = nmbrscrl( & k, 12, 45, min(999, you.money // 100), 1, 1)
                # closebox(10, 29, 14, 52, q)
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
            # oblom: block(1, 24, 0x4F)
            message("Вас забрали в армию. Вот, собственно, и все...", 0x4F)
            quit(2)

    if params.D.weekday() == 6 and date.Date._month(params.D + 7) != params.D.month() and you.status:
        if params.yn("Пойдете на сисопку?"):
            t = min(params.Time - 1, 4 * 60 + random.randint(0, 8 * 60))
            params.Time -= t
            chmood(t // 90 + random.randint(0, you.friends))
            you.money -= random.randint(0, t // 60)
            you.friends += (random.randint(0, t // 180) > 0)
            message("Как ни странно, общаться можно не только по модему...", 0x1F)

    for i in range(4):
        (params.occup[i].func)()
        params.showtime()

    if not params.Down and params.auto_[3] and you.antiv.date and params.D.days() >= params.lstscn.days() + params.auto_[3]:
        vircheck(2, 4)

    if you.spay > 0 or you.spay < 0 and params.studper(params.D) != 2:
        you.sdays += 1

    if params.D.day() < 20 and random.randint(0, 10) < random.randint(0, you.friends) and you.money > 100:
        l = random.randint(0, you.money >> 3) + 5
        s = f"Друг просит ${l} в долг до конца месяца. Дадите?"
        if params.yn(s, params.auto_[1]):
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
                params.fire()
            elif random.randint(0, you.income) > 80 + (i := random.randint(0, 5) + 1) * 80 and not you.Date and (you.osreq == i) != you.os:
                s = f"Ваша работа требует перехода на {params.OSnames[you.osreq]}\nУ вас в запасе 6 дней."
                message(s, 0x4F)
                you.wdate = params.D + 6
                if params.auto_[2] == 1:
                    params.instOS(you.osreq)

    for i in range(10):
        if not random.randint(0, 20):
            bbs[i].down = not bbs[i].down
            if not bbs[i].down:
                bbs[i].modem = random.randint(6)

    if not params.Stable:
        if not random.randint(60) and you.money > 300:
            l = random.randint(0, you.money >> 1) + 50
            s = f"Из-за финансового кризиса вы потеряли ${l}"
            message(s, 0x4F)
            chmood(-l / you.money * 32.0)
            you.money -= l
        if you.wprof:
            if not random.randint(0, 50):
                message("Из-за экономического кризиса ваша фирма лопнула, и вы потеряли работу!", 0x4F)
                you.wdays = 0
                chmood(-10)
                params.newjob(0, 0, 0)
            elif not random.randint(0, 40):
                k = random.randint(0, 50) + 1
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
                # if you.hdspace < os[you.os].size or l > (you.soft >> 1):
                #     s = f"Порушилась операционная система...\nГрузим с дискетки {OSnames[0]}"
                # message(s, 0x4F)
                # chmood(-random.randint(you.os + 1))
                # you.os = 0
                # params.Time -= os[0]['itime']
                # if params.Time < 1:
                #     params.Time = 1
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



def proposal(i):
    from_ = ["Don Carleone", "Vasya Pupkin", "Sergey Mavrodi"]
    d = 0
    summ = 0
    pay = 0
    s = ''
    if i == 1:
        summ = random.randint(0, you.skill[1] * 5) + 100
        s = (f"Есть деловое предложение для крутого хакера.\n"
             f"Надо взломать кой-какую защиту. Плачу ${summ}.")
        d = random.randint(0, 5) + 2

    if i == 2:
        summ = random.randint(0, 4) * 10 + 20
        s = f"Я слышал, вы можете компьютер наладить. За ${summ} возьметесь?"
        d = 1

    if i == 3:
        pay = random.randint(0, you.skill[3]) * 5 + 50
        summ = pay * (2 + random.randint(0, 4))
        s = f"Предлагаю выгодный совместный бизнес.\nВложив всего ${pay}, вы получите ${summ}!"
        d = random.randint(0, 4) + 2

    fidomess(from_[i - 1], you.name, "Предложение", s)
    if not params.yn("Вы принимаете предложение?"):
        return 0

    params.Down += d
    you.money -= pay
    s = None
    prn(0, 0, f"Напряженный труд занял {d} {params.end(d, params.end2)}...")
    newdayf = 1
    while (d):
        newday()
        d -=1

    if i == 1:
        if random.randint(0, summ) > you.skill[1] * 2:
            message("Ничего не вышло. Защита оказалась слишком сложной для вас.\n"
                    "Это не пойдет на пользу вашей профессиональной репутации.", 0x4F)
            you.skill[1] -= random.randint(0, 5)
            # break
        elif not _rnd(you.skill[1] >> 7):
            s = (f"У вас крупные неприятности. Те, чью защиту вы ломали, пожелали\n"
                 f"узнать, кто это такой умный, и им это удалось. Придется вам\n"
                 f"заплатить им ${summ * 2}, и считайте, что дешево отделались!\n")
            summ -= 2 * summ
            you.skill[1] -= random.randint(0, 10)
            message(s, 0x4F)
        else:
            you.skill[1] += random.randint(0, 5)
            message("Нет такой защиты, которую нельзя было бы сломать!", 0x1F)
            you.money += summ

    if i == 2:
        if not _rnd(you.skill[2] >> 7):
            message("Вам не удалось совладать с железом заказчика\n"
                    "Это не пойдет на пользу вашей профессиональной репутации.", 0x4F)
            you.skill[2] -= random.randint(0, 5)
        else:
            you.skill[2] += random.randint(0, 5)
            message("Не так страшно кривое железо, как кривые руки...\n"
                    "К счастью, вы этим не страдаете!", 0x1F)
            you.money += summ

    if i == 3:
        if random.randint(0, pay) > you.skill[3] * 2:
            message("Плакали ваши денежки...", 0x4F)
            you.skill[3] -= random.randint(0, 5)
            # break
        elif not _rnd(you.skill[3] >> 7):
            s = (f"Пора бы знать, что честный бизнес таких прибылей не приносит.\n"
                 f"Те, кого вы пытались кинуть, оказались не лохами, и теперь \n"
                 f"вам придется заплатить им ${summ}!\n")
            message(s, 0x4F)
            summ -= summ
            you.skill[3] -= random.randint(0, 10)
        else:
            you.skill[3] += random.randint(0, 5)
            message("Дело было рискованным, но риск себя оправдал.", 0x1F)
            you.money += summ
    # free(s)
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

    return 0
