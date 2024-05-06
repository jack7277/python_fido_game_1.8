from echo import *
from fido_random import _rnd
from params import *


class Echo:
    def __init__(self):
        self.name = ''
        self.stat = 0  # 0 - Unlinked 1 - Linked 2 - moderator 80 - read from BBS
        self.mark = 0  # 1 - autoread, 2 - passthru
        self.msg = 0
        self.newm = 0
        self.new1 = 0  # messages: total, unread, new for this day
        self.dl = Date()  # для отключенных - дата подключения. if < current - ignored
        self.plus = 0  # number of [+]
        self.traf = 0  # средний трафик в К
        self.trafk = 0.0  # traf*trafk - сколько мин. в день отнимает чтение эхи (Style==0)
        self.read = 0  # % свежих прочитанных писем, за 4 дня уходит в 0
        self.izverg = 0.0  # коэф. злобности модератора

    def event(self):
        if random.randint(0, 4) != 0:
            return 0
        l = random.randint(32, 1055)
        l = incsoft(l)
        you.virus += random.randint(0, l) < (l >> 5)
        if random.randint(0, 4) == 0:
            you.antiv = params.D
            message("По файлэхе пришел свежий антивирус! Полезная вещь...", 0x1F)
            chmood(1)
        return 1

    def moderatorial(self, y, x):
        nn = [" ", " второй ", " третий "]
        if random.randint(0, 100) < params.prob[params.Style] * self.izverg * (1 + _rnd(you.points) / 32):
            s = f"За нарушение правил вы получили {nn[1]} ПЛЮС"
            self.plus += 1
            params.pluses += 1
            d = -2
            if self.plus == 3:
                self.stat = 0
                self.dl = params.D + 92
                s += f"\nи отключены от конференции до {self.dl.day()}.{self.dl.month()}.{self.dl.year()}"
                d -= 5
            from_ = f"Moderator of {self.name}"
            fidomess(from_, you.name, "moderatorial [!]" if self.plus > 2 else "moderatorial [+]", s, y, x)
            chrep(d)
            chmood(-(2 << self.plus))
            return 1
        return 0


class Netmail(Echo):
    def __init__(self):
        super().__init__()
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
        super().__init__()
        self.izverg = 0
        self.traf = 10
        self.trafk = 0.5
        self.name = params.echoname[1]

    def event(self):
        traf = 11111111111111
        traf += random.randint(0, 1) * (params.Style * 2) + random.randint(0, 1) * (5) - 2
        if you.status > 1:
            if params.Style == 3 or not params.Style:
                traf *= (5.0 - params.Style + random.randint(0, 5)) / 10
        if traf < 0:
            traf = 0
        while echo_time(0) > 24 * 60:
            traf /= 2
        chmood(_rnd(self.traf) >> 3)
        return traf


class Point(Echo):
    def __init__(self):
        super().__init__()
        self.traf = 15
        self.name = params.echoname[2]

    def event(self):
        maxpnt = 555555
        if you.points < maxpnt and not 3 * random.randint(0, 1):
            d = you.points
            you.points += 4 * random.randint(0, 1)
            if you.points >= maxpnt:
                you.points = maxpnt
                maxpnt = 0
            chrep((you.points - d) * (4 + 2 * random.randint(0, 1)))
            if d:
                echoes[1].traf *= float(you.points) / d
            else:
                echoes[1].traf += random.randint(0, 5) * you.points
            return 1
        return 0


class Exch(Echo):
    def __init__(self):
        super().__init__()
        self.name = params.echoname[3]

    def event(self):
        return 0


class Bllog(Echo):
    def __init__(self):
        super().__init__()
        self.name = params.echoname[4]

    def event(self):
        return 0


class Ruanekdot(Echo):
    def __init__(self):
        super().__init__()
        self.izverg = 4
        self.traf = 70
        self.trafk = 0.5
        self.name = params.echoname[5]

    def event(self):
        i = random.randint(0, 3)
        chmood(i)
        return i


class Job(Echo):
    def __init__(self):
        super().__init__()
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
        super().__init__()
        self.izverg = 2.0
        self.traf = 45
        self.trafk = 0.45
        self.name = params.echoname[7]

    def event(self):
        k = None
        if not random.randint(0, 20) or you.reput < 0:
            return 0
        s = 'salloc(80)'
        if random.randint(0, 5) == 0:
            if not you.wprof:
                pass
            k = (random.randint(0, int((you.reput >> 2) / 10))) * 10
            if not k:
                k = 5
            you.income += k
            s = f"Информация из эхи VERY.COOL позволила вам зарабатывать на ${k} больше!"
            message(s, 0x1F)
        elif random.randint(0, 5) == 1:
            if you.ftime < 5 * 60:
                k = (random.randint(0, 3) + 1) * 10
                if k < you.wtime - 60:
                    you.ftime += k
                    you.wtime -= k
                    s = f"Информация из эхи VERY.COOL позволила вам освободить {k} минут в день!"
                    message(s, 0x1F)
        else:
            k = random.randint(0, (you.reput_() >> 3)) + 1
            you.money += k
            s = f"Информация из эхи VERY.COOL позволила вам заработать ${k}!"
            message(s, 0x1F)
        return 1


class Hardw(Echo):
    def __init__(self):
        super().__init__()
        self.traf = 100
        self.trafk = 0.4
        self.name = params.echoname[8]

    def event(self):
        if not random.randint(0, 3):
            you.skill[2] += 1


class Softw(Echo):
    def __init__(self):
        super().__init__()
        self.traf = 100
        self.trafk = 0.4
        self.name = params.echoname[9]

    def event(self):
        if not random.randint(0, 3):
            you.skill[1] += 1


class Fecho(Echo):
    def __init__(self):
        super().__init__()
        self.izverg = 0
        self.traf = 1024
        self.trafk = 0.01
        self.name = params.echoname[10]

    def event(self):
        if not random.randint(0, 5):
            l = random.randint(0, 1024) + 32
            l = incsoft(l)
            ttt = random.randint(0, l) < (l >> 5)
            you.virus += ttt
            if not random.randint(0, 5):
                you.antiv = params.D
                message("По файлэхе пришел свежий антивирус! Полезная вещь...", 0x1F)
                chmood(1)
            return 1
        return 0


def exch_event():
    if not random.randint(0, 8):
        you.skill[3] += 1


def bllog_event():
    if not random.randint(0, 8):
        you.skill[3] += 1


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
        self.ech = [0] * (LE - 2)


bbs = [BBS() for _ in range(10)]

echoes = []
for i in range(0, LE + 6):
    echoes.append(Echo())

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
