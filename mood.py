from person import you
from wnds import message
import init


def chmood(dm):
    you.mood += dm
    if you.mood < 0:
        message("Это конец!\n"
                "В приступе тяжелой депрессии вы  разбили молотком модем,\n"
                "выкинули из окна компьютер и повесились на сетевом шнуре.\n"
                "                       RIP.", 0x4F)
        quit(2)
    if you.mood <= 10:
        message(" Депрессия до добра не доводит!\n"
                "Нужно срочно поднять настроение!", 0x4F)
    elif you.mood > 150:
        if you.mood - dm < 150:
            message("Компьютер и модем - что еще человеку для счастья надо?", 0x1F)
        you.mood = 150
