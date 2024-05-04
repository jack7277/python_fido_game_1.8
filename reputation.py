import person
from wnds import message


def chrep(dr, chrp=1):
    person.you.reput += dr
    if person.you.reput > 1024:
        if person.you.reput - dr < 1024:
            message("И слух о вас гремит по всей Сети великой...", 0x1F)
        person.you.reput = 1024
    elif dr < 0:
        if person.you.status == 2:
            if person.you.reput < 128:
                if chrp:
                    message("За особо раздражающее поведение вы лишены нодового адреса", 0x4F)
                    person.you.status = 1
                    maxpnt = person.you.points = 0
                else:
                    person.you.reput = 128
        elif person.you.status == 1:
            if person.you.reput < 32:
                if chrp:
                    message("За плохое поведение босс погнал вас из поинтов", 0x4F)
                    person.you.status = 0
                    # for i in range(params.LE + 1, E):
                    #     del echoes[params.E - 1]
                else:
                    person.you.reput = 32
        elif person.you.status == 0:
            if person.you.reput < -8:
                if chrp:
                    # wnds.block(1, 24, 0x4F)
                    message("Это ж кем надо быть, чтоб ни один сисоп не хотел иметь с вами дела!\n"
                            "         Вообще таким, как вы, надо винт форматировать... \n"
                            "                    Идите-ка отсюда, пока целы!", 0x4F)
                    quit(1)
                else:
                    person.you.reput = -8
