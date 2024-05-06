import params
from fido_date import *
from fido_random import random_
from reputation import chrep


class Person:
    def __init__(self):
        self.name = ""  # salloc(31) длина 31 символ
        self.status = 0
        self.sysop = 0
        self.modem = 0
        self.comp = 0
        self.hd = 0
        self.mreli = 32767
        self.creli = 32767
        self.hreli = 32767
        self.income = 0
        self.expens = -150
        self.spay = 0
        self.money = 300
        self.debt = 0
        self.soft = 0
        self.os = 0
        self.osreq = 0
        self.hdspace = 20 * 1024
        self.virus = 0
        self.ftime = 20 * 60
        self.wtime = 0
        self.wdays = 0
        self.sdays = -1
        self.wprof = 0
        self.sprof = 0
        self.mood = 0
        self.tired = 0
        self.reput = 0
        self.moder = 0
        self.points = 0
        self.friends = 0
        self.antiv = Date()
        self.wdate = Date()
        self.grad = Date()
        self.tries = 0
        self.army = 0
        self.intens = 0
        self.mark = 0.0
        self.echo = [0] * 5
        self.skill = [0, 100, 0, 0]  # 0,prg,hrd,trd

    def reput_(self):
        return self.reput + self.skill[1] + self.skill[2] + self.skill[3]


you = Person()


