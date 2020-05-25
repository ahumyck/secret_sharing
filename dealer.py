from pair import pairing, pairings

class Dealer:
    def __init__(self, t, n):
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
        
        self.__threshold_matrix_generation()
        self.numbers = self.__generate_pairings_numbers()
        self.P = self.__transform_to_points(self.numbers)[-1]
        
        
    def __torsion_subgroup_generators(self):
        G, H = self.E.gens()
        n = G.order() // self.l
        return n * G, n * H
    
    def __add(self, pairings, secrets):
        res = []
        for p, s in zip(pairings, secrets):
            res.append(p + s)
        return res
                
    
    def __threshold_matrix_generation(self):
        A = [[1] * self.t]

        for i in range(1,self.n, 1):
            column = [i + 1] * (self.t - 1)
            for j in range(len(column)):
                column[j] = column[j] ** (j + 1)
            column = [1] + column
            A.append(column)
        
        self.m = matrix(A)
        
    def __generate_pairings_numbers(self):
        from random import randint
        a = []
        b = []
        for i in range(self.t):
            a.append(randint(1,self.l - 1))
            b.append(randint(1,self.l - 1))
        return a,b
        
    def __transform_to_points(self, numbers):
        a, b = self.numbers
        return list(zip(a,b))
    
    def __generate_public_shares(self, Qs, Rs):
        keys = []
        for Q, R in zip(Qs, Rs):
            c, d = Q
            keys.append((c, d, R))
        return keys

    def compute_shares(self):
        _a, _b = matrix([self.numbers[0]]), matrix([self.numbers[1]])
        a = (self.m * _a.transpose()).column(0)
        b = (self.m * _b.transpose()).column(0)
        return list(zip(a,b))

    def get_public_bulletin(self):
        return self.E, self.q, self.l, self.k, self.W
    
    def get_public_bulletin_secrets(self, secrets):
        Qs = self.__transform_to_points(self.__generate_pairings_numbers())
        shares_as_points = pairings(Qs, self.P, self.W)
        Rs = self.__add(shares_as_points, secrets)
        return self.__generate_public_shares(Qs, Rs)