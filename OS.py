from fido_random import _rnd
from params import os, showtime, delay, D
from person import you
from wnds import write, menuf, message, prn

OSnames = [
    "MSDOS 5.0",
    "MSDOS+Win'3.11",
    "Windows 95",
    "Windows NT",
    "OS/2",
    "Linux",
    None
]


def OSinfo(n):
    s = f"Install time {os[n - 1]['itime']} min.\nSpace required {os[n - 1]['memory'] >> 10}M"
    write(14, 2, s)


def instOS(n=0):
    o = None
    i = None
    y = 10
    x = 0
    res = 0
    Time = 30  # ?????? тут этого не должно быть
    if not n:
        # q = openbox(13, 0, 16, 22, 0x30)
        o = menuf(12, 25, 0x70, 0x0F, OSnames, "Install", 1, OSinfo)
        # closebox(13, 0, 16, 22, q)
    else:
        o = n + 1
    while (1):
        if o:
            o -= 1
            if os[o]['memory'] > Time:
                message("Сегодня не успеем...", 0x4F)
                break
            if os[o]['mincomp'] > you.comp:
                message("У вас слишком хилый компьютер!", 0x4F)
                break
            if you.soft + os[o]['memory'] > you.hdspace:
                message("Не хватает места на винте!", 0x4F)
                break
            # q = openbox(y, x, y + 6, x + 40, 0x0F)
            prn(0, 0, f"Installing {OSnames[o]}...")
            # prn(y + 1, x + 1, s)
            for i in range(1, os[o]['itime'] + 1):
                percent = 100 if i == os[o]['itime'] else i * 100 / os[o]['itime']
                prn(0, 0, f"{percent} complete")
                s = ''
                prn(y + 3, x + 2, s)
                Time -= 1
                showtime()
                if o > 0 and _rnd(400 / (you.skill[1] + 1)) and not _rnd(10):
                    message("Глюки!!! Придется переинсталлировать заново...", 0x4F)
                    break
                delay(400)
            # closebox(y, x, y + 6, x + 40, q)
            you.os = o
            res = 1
            if you.osreq:
                you.wdate = D + 6
    return res
