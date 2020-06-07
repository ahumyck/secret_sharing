from pair import pairing, pairings2

class Dealer:
    def __init__(self, t, n, random_distributor = None):
        if random_distributor is None:
            from random import randint
            self.random_distributor = randint
        
        self.t = t
        self.n = n
        self.p = 47
        self.r = 6
        self.q = self.p ** self.r
        self.k = 1
        self.l = 103
        F.<x> = GF(self.q)
        self.E = EllipticCurve(F, [4, 0])
        self.G, self.H  = self.__torsion_subgroup_generators()

        alpha = 51
        beta = 35
        self.W = alpha * self.G + beta * self.H
        self.__polynomial_generation()
    
    
    def __torsion_subgroup_generators(self):
        G, H = self.E.gens()
        n = G.order() // self.l
        return n * G, n * H
    
    def __polynomial_generation(self):
        a0, b0 = self.random_distributor(0, self.l), self.random_distributor(0, self.l)
        self.secret_point = (a0, b0)
        f = [a0]
        for i in range(1, self.t-1, 1):
            f.append(self.random_distributor(0, self.l))
        f.append(b0)
        
        ring = IntegerModRing(self.l)
        p_ring = PolynomialRing(ring, "x")
        self.polynomial = p_ring(f)
        
    def __subtract(self, Rs, Ts):
        res = []
        for R, T in zip(Rs, Ts):
            res.append(R - T)
        return res
        

    def verification_information(self):
        c = self.random_distributor(0, self.l - 1)
        d = self.random_distributor(0, self.l - 1)
        Q = (c, d)
        
        Vs = dict()
        Vs[0] = pairing(self.secret_point, Q, self.W)
        for i in range(len(self.shares)):
            Vs[i + 1] = pairing(self.shares[i], Q, self.W)
            
        verification_info = dict()
        verification_info['Q'] = Q
        verification_info['Vs'] = Vs
        
        return verification_info
    
    def get_public_bulletin_secrets(self, secrets):
        p = pairings2(self.secret_point, self.shares, self.W)
        return self.__subtract(secrets, p)
            
    def get_public_bulletin(self):
        return self.E, self.q, self.l, self.k, self.G, self.H, self.W
    
    def compute_share(self, value):
        return value, self.polynomial(value)
    
    def compute_shares(self):
        self.shares = []
        for i in range(1, self.t + 1, 1):
            self.shares.append(self.compute_share(i))
        
        return self.shares