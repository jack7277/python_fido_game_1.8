import datetime

def round(f):
    return int(f + (0.5 if f > 0 else -0.5))


mofs = [0, 31, 31 + 28, 31 + 28 + 31, 31 + 28 + 31 + 30, 31 + 28 + 31 + 30 + 31, 31 + 28 + 31 + 30 + 31 + 30,
        31 + 28 + 31 + 30 + 31 + 30 + 31, 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31,
        31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30, 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31,
        31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30]




def getfiledate(handle):
    # Not implemented
    return 0


# Example usage
# D = getcurdate()
# d1 = D
# D -= 4 * 365
# print(f"{D.day()}/{D.month()}/{D.year()}")
# d = d1.date
# D = Date()
# D.Date = d
# print(f"{D.day()}/{D.month()}/{D.year()}")
