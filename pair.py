def pairings(Qs, P, W):
        res = []
        for Q in Qs:
            res.append(pairing(Q, P, W))
        return res

def pairing(Q, P, W):
    r1, s1 = Q
    r2, s2 = P
    return (r1 * s2 - r2 * s1) * W