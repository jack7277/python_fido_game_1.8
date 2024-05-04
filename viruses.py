from random import randint

import params
from person import you
from wnds import message, prn, prnc


def vircheck(y, x):
    q = None
    i = 0
    t = 0
    if not you.antiv.date:
        message("Дык нету у вас антивируса!", 0x4F)
        return 0
    t = int(you.soft / (1024 + you.comp * 2048))
    if t >= params.Time:
        message("Сегодня не успеем провериться...", 0x4F)
        return 0
    # q = openbox(y, x, y + 6, x + 40, 0x0F)
    prn(y + 1, x + 1, "Antivirus starts...")
    s = 'salloc(15)'
    for i in range(t + 1):
        percent_complete = 100 if i == t else i * 100 / t
        prn(0, 0, f"{percent_complete} complete")
        prn(y + 3, x + 2, s)
        params.Time -= 1
        params.showtime()
        params.delay(400)
    lstscn = params.D
    i = you.virus / (randint(0, 1) * ((params.D - you.antiv) >> 3) + 1)
    if i:
        prn(0, 0, f"{i} virus(es) found & cured!")
        you.virus -= i
        prnc(y + 4, x + 1, s, 0x0C)
    else:
        prn(y + 4, x + 1, "No viruses found")
    if params.D - you.antiv > 16:
        prn(y + 5, x + 1, "Warning: you antivirus is too old!")
    # anykey()
    # closebox(y, x, y + 6, x + 40, q)
    # free(s)
    return i
