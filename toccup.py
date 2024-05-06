from random import randint

import fido
import params
from time_spend import mailtime, worktime, studtime, joytime


class Toccup:
    def __init__(self, name, ord, func):
        self.name = name
        self.ord = ord
        self.func = func

occup = [
    Toccup("Почта      ", 1, mailtime),
    Toccup("Работа     ", 2, worktime),
    Toccup("Учеба      ", 3, studtime),
    Toccup("Развлечения", 4, joytime)
]
