import random

import params
from fido import you, message, chmood, chrep, fidomess, echtime, _rnd, proposal


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
            fidomess(from_, you.name, "moderatorial [!]" if self.plus > 2 else "moderatorial [+]", s, y, x)
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

    def event(self):
        i = 0
        self.traf += _rnd(params.Style * 3) - 2
        if self.traf < 0:
            traf = 0
        self.traf *= params.Style / float(1.5 + _rnd(params.Style * 2) / 4.0)
        while int(echtime(0)) > 24 * 60:
            self.traf /= 2
        chmood(_rnd(self.traf) >> 2)
        if params.Style == 3:
            if (you.friends - random.randint(0, 20)) < 0:
                you.friends = 0
        else:
            you.friends += (random.randint(0, params.Style + 1))
        for i in range(1, 4):
            if _rnd(you.skill[i] >> 6):
                if proposal(i):
                    break
        return self.traf


class Local(Echo):
    def __init__(self):
        super().__init__(1)
        self.izverg = 0
        self.traf = 10
        self.trafk = 0.5

    def local_event(self):
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


class Point(Echo):
    def __init__(self):
        super().__init__(2)
        self.traf = 15

    def event(self):
        return 0


class Exch(Echo):
    def __init__(self):
        super().__init__(3)

    def event(self):
        return 0


class Bllog(Echo):
    def __init__(self):
        super().__init__(4)

    def event(self):
        return 0


class Ruanekdot(Echo):
    def __init__(self):
        super().__init__(5)
        self.izverg = 4
        self.traf = 70
        self.trafk = 0.5

    def event(self):
        return 0


class Job(Echo):
    def __init__(self):
        super().__init__(6)
        self.izverg = 2.0
        self.traf = 35
        self.trafk = 0.2

    def event(self):
        return 0


class Vcool(Echo):
    def __init__(self):
        super().__init__(7)
        self.izverg = 2.0
        self.traf = 45
        self.trafk = 0.45

    def event(self):
        return 0


class Hardw(Echo):
    def __init__(self):
        super().__init__(8)
        self.traf = 100
        self.trafk = 0.4

    def event(self):
        return 0


class Softw(Echo):
    def __init__(self):
        super().__init__(9)
        self.traf = 100
        self.trafk = 0.4

    def event(self):
        return 0


class Fecho(Echo):
    def __init__(self):
        super().__init__(10)
        self.izverg = 0
        self.traf = 1024
        self.trafk = 0.01

    def event(self):
        return 0




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
