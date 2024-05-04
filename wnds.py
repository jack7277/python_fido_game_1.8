# word = int
# byte = int


scr = bytearray(b'\x00' * 0xB8000000)
scrw = bytearray(b'\x00' * 0xB8000000)
low = bytearray(b'\x00' * 0x00000000)
Border = [218, 196, 191, 179, 217, 192, 201, 205, 187, 186, 188, 200, 214, 196, 183, 186, 189, 211, 213, 205, 184, 179,
          190, 212]
SSB = 0
DDB = 6
SDB = 12
DSB = 18
BRDR = SSB


def fidomess(from_, to, subj, text, y=5, x=8):
    i = 0 # todo debug
    # q = openbox(y, x, y + 16, x + 60, 0x1E)
    prnc(y + 1, x + 1, "From : ", 0x13)
    prnc(y + 1, x + 8, from_, 0x13)
    prnc(y + 2, x + 1, "To   : ", 0x13)
    prnc(y + 2, x + 8, to, 0x13)
    prnc(y + 3, x + 1, "Subj : ", 0x13)
    prnc(y + 3, x + 8, subj, 0x13)
    for i in range(x + 1, x + 60):
        scrs(y + 4, i, '─')
    scrs(y + 4, i, 195)
    scrs(y + 4, 60 + x, 180)
    prn(y + 5, x + 1, "Hi ")
    i = wrtword(y + 5, x + 4, to)
    scrs(y + 5, x + 4 + i, '!')
    i = write(y + 7, x + 1, text)
    wrtword(y + 8 + i, x + 1, from_)
    anykey()
    # closebox(y, x, y + 16, x + 60, q)


def up(c):
    if 'a' <= chr(c) <= 'z' or 160 <= c <= 175:
        return c & 0xDF
    elif 224 <= c <= 239:
        return c - 80
    else:
        return c


def prn(y, x, st):
    print(st)


def message(s, c, wait=1, y=0xFF, x=0):
    prn(0, 0, s)


def chatr(y, x, l, c):
    for i in range(l):
        scr[y * 160 + 1 + ((x + i) << 1)] = c


def wrt(y, x, st, n):
    i = 0
    while st[i] >= 15 and i < n:
        scr[y * 160 + ((x + i) << 1)] = st[i]
        i += 1


def wrtword(y, x, st):
    i = 0
    while st[i] != 0 and st[i] != ' ':
        scr[y * 160 + ((x + i) << 1)] = ord(st[i])
        i += 1
    return i


def write(y, x, s):
    print(s)
    # i = x
    # j = y
    # while s:
    #     if s == '\n':
    #         j += 1
    #         i = x
    #     elif s != '\r':
    #         scr[j * 160 + (i << 1)] = ord(s)
    #         i += 1
    #     s = s[1:]
    # return j - y + 1


def writen(y, x, s, n):
    print(s)
    # i = x
    # j = y
    # k = 0
    # while s[k] and j < y + n:
    #     if s[k] == '\n':
    #         j += 1
    #         i = x
    #     elif s[k] != '\r':
    #         scr[j * 160 + (i << 1)] = ord(s[k])
    #         i += 1
    #     k += 1
    # return k


def prnc(y, x, st, c):
    # 1f - белые буквы на синем фоне
    # 0x74 - красные на сером, самый низ индекс 24
    print(st)
    # if st is None:
    #     return
    # i = 0
    # while st[i] != 0:
    #     scr[y * 160 + (x + i) * 2] = ord(st[i])
    #     scr[y * 160 + (x + i) * 2 + 1] = c
    #     i += 1


def prncc(y, x, st, c):
    print(st)
    # if st is None:
    #     return
    # i = 0
    # while st[i] != 0:
    #     if st[i] < 16:
    #         c = (c & 0xF0) | st[i]
    #     elif st[i] < 32:
    #         c = c | (st[i] << 4)
    #     elif st[i] == 255:
    #         c = (c & 0xF0)
    #     else:
    #         scr[y * 160 + (x << 1)] = st[i]
    #         scr[y * 160 + (x << 1) + 1] = c
    #         x += 1
    #     i += 1


def clrbl(t, l, b, r, c1):
    for i in range(t, b + 1):
        for j in range(l, r + 1):
            scr[i * 160 + j * 2 + 1] = c1
            scr[i * 160 + j * 2] = 32


def _box(t, l, b, r, c1, brdr):
    clrbl(t, l, b, r, c1)
    for i in range(t + 1, b):
        scr[i * 160 + l * 2] = Border[brdr + 3]
        scr[i * 160 + r * 2] = Border[brdr + 3]
    for i in range(t + 1, b + 1):
        scr[i * 160 + (r + 1) * 2 + 1] &= 7
        scr[i * 160 + (r + 2) * 2 + 1] &= 7
    for i in range(l + 1, r):
        scr[b * 160 + i * 2] = Border[brdr + 1]
        scr[t * 160 + i * 2] = Border[brdr + 1]
    for i in range(l + 2, r + 3):
        scr[(b + 1) * 160 + i * 2 + 1] &= 7
    scr[b * 160 + r * 2] = Border[brdr + 4]
    scr[t * 160 + r * 2] = Border[brdr + 2]
    scr[b * 160 + l * 2] = Border[brdr + 5]
    scr[t * 160 + l * 2] = Border[brdr]


def box(t, l, b, r, c):
    _box(t, l, b, r, c, BRDR)


def openbox(t, l, b, r, c):
    # q = bytearray((b - t + 2) * (r - l + 3) * 2)
    # gettext(l + 1, t + 1, r + 3, b + 2, q)
    # box(t, l, b, r, c)
    # return q
    pass


def closebox(t, l, b, r, q):
    # puttext(l + 1, t + 1, r + 3, b + 2, q)
    # del q
    pass


def block(t, b, c):
    return
    # w = (c << 8) | ord('±')
    # for j in range(t, b + 1):
    #     for i in range(80):
    #         scrw[j * 80 + i] = w


def _menu(t, l, b, r, n, c1, c2, ar, hdr, h, cl, menufunc):
    q = openbox(t, l, b, r, c1)
    prn(t, (r + l + 1 - len(hdr)) // 2, hdr)
    for i in range(1, n + 1):
        prn(t + i, l + 2, ar[i - 1])
    sel = min(h, n)
    while True:
        for i in range(l + 2, r):
            scr[(t + sel) * 160 + i * 2 + 1] = c2
        if menufunc is not None:
            menufunc(sel)
        c = ord(input())
        if c:
            if sel != n:
                i = sel + 1
            else:
                i = 1
            while i != sel:
                if up(ord(ar[i - 1][0])) == up(c):
                    for j in range(l + 2, r):
                        scr[(t + sel) * 160 + j * 2 + 1] = c1
                    sel = i
                    break
                i = 1 if i == n else i + 1
        if c == 27:
            closebox(t, l, b, r, q)
            return 0
        elif c == 13:
            if cl:
                closebox(t, l, b, r, q)
            else:
                del q
            return sel
        elif c == 0:
            c = ord(input())
            if c == 73:  # PgUp
                if sel > 1:
                    for i in range(l + 2, r):
                        scr[(t + sel) * 160 + i * 2 + 1] = c1
                    sel = 1
            elif c == 81:  # PgDn
                if sel < n:
                    for i in range(l + 2, r):
                        scr[(t + sel) * 160 + i * 2 + 1] = c1
                    sel = n
            elif c == 72:  # Up
                for i in range(l + 2, r):
                    scr[(t + sel) * 160 + i * 2 + 1] = c1
                sel = sel - 1 if sel > 1 else n
            elif c == 80:  # Down
                for i in range(l + 2, r):
                    scr[(t + sel) * 160 + i * 2 + 1] = c1
                sel = 1 if sel == n else sel + 1


def menu(t, l, c1, c2, ar, hdr, h):
    n = 0
    s = 0
    while ar[n] is not None:
        s = max(s, len(ar[n]))
        n += 1
    s = max(s, len(hdr))
    return _menu(t, l, t + n + 1, l + s + 3, n, c1, c2, ar, hdr, h, 1, None)


def menuf(t, l, c1, c2, ar, hdr, h, func):
    n = 0
    s = 0
    while ar[n] is not None:
        s = max(s, len(ar[n]))
        n += 1
    s = max(s, len(hdr))
    return _menu(t, l, t + n + 1, l + s + 3, n, c1, c2, ar, hdr, h, 1, func)


def menuncl(t, l, c1, c2, ar, hdr, h):
    n = 0
    s = 0
    while ar[n] is not None:
        s = max(s, len(ar[n]))
        n += 1
    s = max(s, len(hdr))
    return _menu(t, l, t + n + 1, l + s + 3, n, c1, c2, ar, hdr, h, 0, None)
