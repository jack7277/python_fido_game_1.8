from person import you
from wnds import message


def decmoney(x):
    if (you.money - x) < 0:
        message("Вы залезли в долги! Это может плохо кончиться!", 0x4F)
        return 1
    else:
        return 0
