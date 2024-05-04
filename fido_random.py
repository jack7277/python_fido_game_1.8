from random import randint


def _rnd(x):
    return int((randint(0, x) * x) / (randint(0, 0x7fff) + 1))


def lrandom(x):
    return x if x == 0 else (randint(0, 0xFFFF) * randint(0, 0xFFFF)) % x


def random_(x):
    return -randint(0, -x) if x < 0 else randint(0, x)
