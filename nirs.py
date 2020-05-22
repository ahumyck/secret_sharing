#!/usr/bin/env python
# coding: utf-8

# In[1]:


def pairings(Qs, P, W):
        res = []
        for Q in Qs:
            res.append(pairing(Q, P, W))
        return res

def pairing(Q, P, W):
    r1, s1 = Q
    r2, s2 = P
    return (r1 * s2 - r2 * s1) * W


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

        for i in range(1,self.n ,1):
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
        
        
        


# In[2]:


def secret_example(E, how_many_secrets):
    secrets = []
    for i in range(how_many_secrets):
        secrets.append(E.random_element())
    return secrets

t, n = 2, 3
dealer = Dealer(t, n)
E, q, l, k, W = dealer.get_public_bulletin()
secrets = secret_example(E, t) #secret_example
print("secrets = ", secrets)
user_points = dealer.compute_shares()
print("up =", user_points)
public_information = dealer.get_public_bulletin_secrets(secrets)
print("public =", public_information)

print("public")
for info in public_information:
    print(info)



# In[3]:


def subtract(Rs, Ts):
    res = []
    for R, T in zip(Rs, Ts):
        res.append(R - T)
    return res

# def calculate_pseudo_shares(Qs, UPs, W):
#     S = []
#     for Q in Qs:
#         tmp = []
#         for user_point in UPs:
#             tmp.append(pairing(Q, user_point, W))
#         S.append(tmp)
#     return S

def calculate_j_symbol(u, j):
    res = 1
    for i in range(len(u)):
        if i == j:
            continue
        else:
            res *= (u[j] - u[i])
    return 1/res


def calculate_last_matrix_row(u):
    y = []
    for i in range(len(u)):
        y.append(calculate_j_symbol(u, i))
    return y

def restore_last_point(last_matrix_row, user_points):
    x, y = 0, 0
    for row_element, user_point in zip(last_matrix_row, user_points):
        a, b = user_point
        x += row_element * a
        y += row_element * b
    return int(x), int(y)

def unpack_public_information(public_information):
    rs = []
    qs = []

    for info in public_information:
        rs.append(info[-1])
        qs.append((info[0], info[1]))
        
    return qs, rs

def collegium(UPs, rows):
    ups = []
    for i in range(len(rows)):
        ups.append(UPs[rows[i]])
    
    return ups

user_who_wants_their_secret = [0, 2]
qqqq, rrrr = unpack_public_information(public_information)
user_collegium = collegium(user_points, user_who_wants_their_secret)
last_matrix_row = calculate_last_matrix_row(user_who_wants_their_secret)
pppp = restore_last_point(last_matrix_row, user_collegium)
eeee = pairings(qqqq, pppp, W)
ssss = subtract(rrrr, eeee)
print(ssss)
       
    


# In[ ]:




