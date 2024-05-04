from echo import Echo, Local, Point, Exch, Bllog, Ruanekdot, Job, Vcool, Hardw, Softw, Fecho
from params import LE
from person import you

echoes = []
for i in range(0, LE + 6):
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

