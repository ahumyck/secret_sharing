def pairing(Q, P, W):
    r1, s1 = Q
    r2, s2 = P
    k = int(r1 * s2 - r2 * s1)
    return k * W