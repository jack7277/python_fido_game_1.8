import random
import params
import person
from fido_random import _rnd
from init import *
from mood import chmood
from reputation import chrep
from wnds import message, fidomess


def echo_time(i):
    k1 = 1 if echoes[i].stat > 2 else echoes[i].stat
    k2 = 1 if you.os > 0 else 1.3
    return round(echoes[i].traf * echoes[i].trafk * (params.Style + 1) * k1 * (11.0 - you.comp / 1.5) * k2 / 10.0)


def echtime1(i, n):
    t = round((n) * 2 * echoes[i].trafk * (params.Style + 1) * (1 if echoes[i].stat > 2 else echoes[i].stat) * (11.0 - you.comp / 1.5) * (1 if you.os > 0 else 1.3) / 10.0)
    if not t and n:
        t = 1
    return t


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
        person.you.virus += random.randint(0, l) < (l >> 5)
        if random.randint(0, 4) == 0:
            person.you.antiv = params.D
            message("A fresh antivirus came through the file echo! Useful thing...", 0x1F)
            chmood(1)
        return 1

    def incsoft(self, ds, chrp=1):
        if person.you.soft + params.os[self.you.os].size + ds > self.you.hdspace:
            ds = self.you.hdspace - person.you.soft - params.os[self.you.os].size
        if not ds:
            return 0
        chrep(random.randint(0, ds * int(person.you.status / 512)) / 2, chrp)
        person.you.soft += ds
        return ds

    def moderatorial(self, y, x):
        nn = [" ", " второй ", " третий "]
        if random.randint(0, 100) < params.prob[params.Style] * self.izverg * (1 + random.randint((self.you.points)) / 32):
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
            fidomess(from_, person.you.name, "moderatorial [!]" if self.plus > 2 else "moderatorial [+]", s, y, x)
            chrep(d)
            chmood(-(2 << self.plus))
            return 1
        return 0


class Netmail(Echo):
    def __init__(self):
        super().__init__(0)
        self.izverg = 0
        self.traf = 0
        self.trafk = 0.7

    # todo тут всё неправильно, переделать
    def event(self):
        i = 0
        self.traf += _rnd(params.Style * 3) - 2
        if self.traf < 0:
            traf = 0
        self.traf *= params.Style / float(1.5 + _rnd(params.Style * 2) / 4.0)
        while int(echo_time(0)) > 24 * 60:
            self.traf /= 2
        chmood(_rnd(self.traf) >> 2)
        if params.Style == 3:
            if (person.you.friends - random.randint(0, 20)) < 0:
                person.you.friends = 0
        else:
            person.you.friends += (random.randint(0, params.Style + 1))
        for i in range(1, 4):
            if _rnd(person.you.skill[i] >> 6):
                if proposal(i):
                    break
        return self.traf


class Local(Echo):
    def __init__(self):
        super().__init__(1)
        self.izverg = 0
        self.traf = 10
        self.trafk = 0.5
        self.name = params.echoname[1]

    def event(self):
        traf = 11111111111111
        traf += random.randint(0, 1) * (params.Style * 2) + random.randint(0, 1) * (5) - 2
        if person.you.status > 1:
            if params.Style == 3 or not params.Style:
                traf *= (5.0 - params.Style + random.randint(0, 5)) / 10
        if traf < 0:
            traf = 0
        while echo_time(0) > 24 * 60:
            traf /= 2
        chmood(random.randint(0, 1) * (traf) >> 3)
        return traf


class Point(Echo):
    def __init__(self):
        super().__init__(2)
        self.traf = 15
        self.name = params.echoname[2]

    def event(self):
        maxpnt = 555555
        if person.you.points < maxpnt and not 3 * random.randint(0, 1):
            d = person.you.points
            person.you.points += 4 * random.randint(0, 1)
            if person.you.points >= maxpnt:
                person.you.points = maxpnt
                maxpnt = 0
            chrep((person.you.points - d) * (4 + 2 * random.randint(0, 1)))
            if d:
                echoes[1].traf *= float(person.you.points) / d
            else:
                echoes[1].traf += random.randint(0, 5) * person.you.points
            return 1
        return 0


class Exch(Echo):
    def __init__(self):
        super().__init__(3)
        self.name = params.echoname[3]

    def event(self):
        return 0


class Bllog(Echo):
    def __init__(self):
        super().__init__(4)
        self.name = params.echoname[4]

    def event(self):
        return 0


class Ruanekdot(Echo):
    def __init__(self):
        super().__init__(5)
        self.izverg = 4
        self.traf = 70
        self.trafk = 0.5
        self.name = params.echoname[5]

    def event(self):
        i = random.randint(0, 3)
        chmood(int(i))
        return int(i)


class Job(Echo):
    def __init__(self):
        super().__init__(6)
        self.izverg = 2.0
        self.traf = 35
        self.trafk = 0.2
        self.name = params.echoname[6]

    def event(self):
        if not random.randint(0, 20) or params.BBSf:
            return 0
        return 1


class Vcool(Echo):
    def __init__(self):
        super().__init__(7)
        self.izverg = 2.0
        self.traf = 45
        self.trafk = 0.45
        self.name = params.echoname[7]

    def event(self):
        k = None
        if not random.randint(0, 20) or person.you.reput < 0:
            return 0
        s = 'salloc(80)'
        if random.randint(0, 5) == 0:
            if not person.you.wprof:
                pass
            k = (random.randint(0, int((person.you.reput >> 2) / 10))) * 10
            if not k:
                k = 5
            person.you.income += k
            s = f"Информация из эхи VERY.COOL позволила вам зарабатывать на ${k} больше!"
            message(s, 0x1F)
        elif random.randint(0, 5) == 1:
            if person.you.ftime < 5 * 60:
                k = (random.randint(0, 3) + 1) * 10
                if k < person.you.wtime - 60:
                    person.you.ftime += k
                    person.you.wtime -= k
                    s = f"Информация из эхи VERY.COOL позволила вам освободить {k} минут в день!"
                    message(s, 0x1F)
        else:
            k = random.randint(0, (person.you.reput_() >> 3)) + 1
            person.you.money += k
            s = f"Информация из эхи VERY.COOL позволила вам заработать ${k}!"
            message(s, 0x1F)
        return 1


class Hardw(Echo):
    def __init__(self):
        super().__init__(8)
        self.traf = 100
        self.trafk = 0.4
        self.name = params.echoname[8]

    def event(self):
        if not random.randint(0, 3):
            person.you.skill[2] += 1


class Softw(Echo):
    def __init__(self):
        super().__init__(9)
        self.traf = 100
        self.trafk = 0.4
        self.name = params.echoname[9]

    def event(self):
        if not random.randint(0, 3):
            person.you.skill[1] += 1


class Fecho(Echo):
    def __init__(self):
        super().__init__(10)
        self.izverg = 0
        self.traf = 1024
        self.trafk = 0.01
        self.name = params.echoname[10]

    def event(self):
        if not random.randint(0, 5):
            l = random.randint(0, 1024) + 32
            l = incsoft(l)
            ttt = random.randint(0, l) < (l >> 5)
            person.you.virus += ttt
            if not random.randint(0, 5):
                person.you.antiv = params.D
                message("По файлэхе пришел свежий антивирус! Полезная вещь...", 0x1F)
                chmood(1)
            return 1
        return 0


def exch_event():
    if not random.randint(0, 8):
        person.you.skill[3] += 1


def bllog_event():
    if not random.randint(0, 8):
        person.you.skill[3] += 1

