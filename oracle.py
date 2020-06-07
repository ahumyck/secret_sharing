from pair import pairing, pairings2

class Oracle:
    def __init__(self):
        pass
    
    def __add(self, Rs, Ts):
        res = []
        for R, T in zip(Rs, Ts):
            res.append(R + T)
        return res
    
    def __restore_polynomial(self, shares, l):
        restored_ring = IntegerModRing(l)
        restored_p_ring = PolynomialRing(restored_ring, "x")
        return restored_p_ring.lagrange_polynomial(shares)
    
    def __restore_secret_point(self, polynomial):
        coefs = polynomial.list()
        return coefs[0], coefs[-1]
        
    def restore_secrets(self, public_secrets, shares, Vs, Q, l, W):
        polynomial = self.__restore_polynomial(shares, l)
        secret_point = self.__restore_secret_point(polynomial)
        res, msg = self.__verificate_each_shadow(shares, secret_point, Vs, Q, W)
        print(msg)
        if res:
            p = pairings2(secret_point, shares, W)
            return self.__add(public_secrets, p)
        else:
            raise SystemExit
    
    def __verificate_each_shadow(self, shares, secret_point, Vs, Q, W):
        for i in range(len(shares)):
            u = pairing(shares[i], Q, W)
            if u != Vs[i + 1]:
                return False, "shadow corrupted"
            
        u = pairing(secret_point, Q, W)
        if u != Vs[0]:
            return False, "secret point corrupted"
        
        return True, "Secrets were not compromised "
        
    def verificate(self, Q, share, v, W):
        u = pairing(share, Q, W)
        return v == u