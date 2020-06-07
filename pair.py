def pairing(Q, P, W):
    r1, s1 = Q
    r2, s2 = P
    k = int(r1 * s2 - r2 * s1)
    return k * W

def pairings2(P, Qs, W):
    res = []
    for Q in Qs:
        res.append(pairing(P, Q, W))
    return res

def pairings1(Ps, Q, W):
    res = []
    for P in Ps:
        res.append(pairing(P, Q, W))
    return res