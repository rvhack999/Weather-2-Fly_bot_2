def calc_cof_t(t):
    if t < -30:
        return 0
    elif -30 <= t < -20:
        return 0.25
    elif -20 <= t < -10:
        return 0.5
    elif -10 <= t < 0:
        return 0.75
    elif t > 0:
        return 1


def calc_cof_w(w):
    if 5 <= w:
        return 0
    elif 3 <= w < 5:
        return 0.25
    elif 2 <= w < 3:
        return 0.5
    elif 1 <= w < 2:
        return 0.75
    elif w < 1:
        return 1

