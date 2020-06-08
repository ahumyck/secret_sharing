from pair import pairing

class Oracle:
    def __init__(self):
        pass
    
    def __restore_polynomial(self, shares, l):
        restored_ring = IntegerModRing(l)
        restored_p_ring = PolynomialRing(restored_ring, "x")
        return restored_p_ring.lagrange_polynomial(shares.values())
    
    def __restore_secret_point(self, polynomial):
        coefs = polynomial.list()
        return int(coefs[0]), int(coefs[-1])
    
    def __shadow_verification(self, shares, secret_point, Vs, Q, W):
        for key in shares:
            u = pairing(shares[key], Q, W)
            if u != Vs[key]:
                return False, "Possible cheater detected: {}".format(key)
            
        u = pairing(secret_point, Q, W)
        if u != Vs[0]:
            return False, "V0 is corrupted, dealer is possible cheater"
        
        return True, "Secrets were not compromised"
        
    def restore_secrets(self, public_secrets, shares, verification_information, pairing_params):
        Vs = verification_information['Vs']
        Q = verification_information['Q']
        L, G, H, W = pairing_params
        
        polynomial = self.__restore_polynomial(shares, L)
        secret_point = self.__restore_secret_point(polynomial)
        verification_result = self.__shadow_verification(shares, secret_point, Vs, Q, W)
        
        a, b = secret_point
        P = a * G + b * H
        
        res = []
        for i in range(len(public_secrets)):
            Pi = W.weil_pairing((i + 1) * P, L)
            res.append(public_secrets[i] + Pi)
        return res, verification_result
        
    def verification(self, share, V, Q, W):
        return pairing(share, Q, W) == V