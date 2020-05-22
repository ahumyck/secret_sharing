#!/usr/bin/env python
# coding: utf-8

# In[1]:


def torsion_subgroup_generators(E, r):
    G, H = E.gens()
    n = G.order() // r
    return n * G, n * H

p = 47
r = 6
q = p ** r
k = 1
l = 103
F.<x> = GF(q)
E = EllipticCurve(F, [4, 0])
G, H  = torsion_subgroup_generators(E, l)

alpha = 51 #not in public
beta = 35 #not in public
W = alpha * G + beta * H
        


# In[46]:


def generate_public_shares(Qs, Rs):
    keys = []
    for Q, R in zip(Qs, Rs):
        c, d = Q
        keys.append((c, d, R))
    return keys


def add(pairings, secrets):
    res = []
    for p, s in zip(pairings, secrets):
        res.append(p + s)
    return res


def pairings(Qs, P, W):
    res = []
    for Q in Qs:
        res.append(pairing(Q,P,W))
    return res

def pairing(Q, P, W):
    r1, s1 = Q
    r2, s2 = P
    return (r1 * s2 - r2 * s1) * W


def secret_example(E, how_many_secrets):
    secrets = []
    for i in range(how_many_secrets):
        secrets.append(E.random_element())
    return secrets
        

def threshold_matrix_generation(t,n):
    m = [[1] * t]
    
    for i in range(1,n ,1):
        column = [i + 1] * (t - 1)
        for j in range(len(column)):
            column[j] = column[j] ** (j + 1)
        column = [1] + column
        m.append(column)
        
    return matrix(m)

def generate_pairings_numbers(t, l):
    from random import randint
    a = []
    b = []
    for i in range(t):
        a.append(randint(1,l - 1))
        b.append(randint(1,l - 1))
    return a, b

def compute_shares(A, numbers):
    _a, _b = matrix([numbers[0]]), matrix([numbers[1]])
    a = (A * _a.transpose()).column(0)
    b = (A * _b.transpose()).column(0)
    return list(zip(a,b))


def transform_to_points(numbers):
    a, b = numbers
    return list(zip(a,b))

t, n = 2, 3
secrets = secret_example(E, t) #secret_example
A = threshold_matrix_generation(t, n)
numbers = generate_pairings_numbers(t, l)
Ps = transform_to_points(numbers)
P = Ps[-1]
print(Ps[-1])
user_points = compute_shares(A, numbers) #giveaway to Users
Qs = transform_to_points(generate_pairings_numbers(t, l))
shares_as_points = pairings(Qs,P,W)
Rs = add(shares_as_points, secrets)

public_information = generate_public_shares(Qs,Rs)

# print("matrix")
# print(A)
print("secrets = {}".format(secrets))
print("numbers = {}".format(numbers))
print("user_points = {}".format(user_points))
print("Ps = {}".format(Ps))
print("Qs = {}".format(Qs))
# print("Rs = {}".format(Rs))

print("\npublic")
for info in public_information:
    print(info)



# In[47]:


def subtract(Rs, Ts):
    res = []
    for R, T in zip(Rs, Ts):
        res.append(R - T)
    return res
    

def invert_matrix(A, rows):
    print(A.matrix_from_rows(rows))
    return A.matrix_from_rows(rows).inverse()

def calculate_S(Qs, UPs, W, rows):
    S = []
    for Q in Qs:
        tmp = []
        for row in rows:
            tmp.append(pairing(Q, UPs[row], W))
        S.append(tmp)
    return S


def calculate_T(Ss, A):
    rows = A.rows()
    Ts = []
    for i in range(len(rows)):
        T = int(rows[-1][0]) * Ss[i][0]
        for j in range(1, len(rows[i]), 1):
            T += int(rows[-1][j]) * Ss[i][j]
        Ts.append(T)
    return Ts

"""
    Each of them can calculate {y(k)}
    and use it to restore ~P(t), so instead
    we can calculate pairing e(i) = (Q(i), ~P(t)) to get our secret back
    with following formula : S(i) = R(i) - e(i)
"""


rows = [0, 1]
pseudo_shares = calculate_S(Qs, user_points, W, rows)
inv = invert_matrix(A, rows)
print(inv)
Ts = calculate_T(pseudo_shares, inv)
recovered_secrets = subtract(Rs, Ts)
print("secrets = {}".format(recovered_secrets))
    


# In[60]:


print("user_points = {}".format(user_points))
print("public")
for info in public_information:
    print(info)
# print(numbers)
_a, _b = matrix([numbers[0]]), matrix([numbers[1]])
_a = _a.transpose()
_b = _b.transpose()
a = A * _a
b = A * _b
print("rows = {}".format(rows))
print(_a)
print(_b)
# print()
print(a.column(0))
print(b.column(0))

def v(a, b, rows):
    a1 = []
    b1 = []
    for i in range(len(rows)):
        a1.append(a.column(0)[rows[i]])
        b1.append(b.column(0)[rows[i]])
    
    return matrix(a1), matrix(b1)

print()
print(inv)
print()
aa, bb = v(a, b, rows)
aaa = aa * inv
bbb = bb * inv
print(aaa)
print(bbb)

pppp = (int(aaa.row(0)[1]), int(bbb.row(0)[1]))
print(pppp)
Q1 = (public_information[0][0], public_information[0][1])
Q2 = (public_information[1][0], public_information[1][1])
print(Q1, Q2)
e1 = pairing(Q1, pppp, W)
e2 = pairing(Q2, pppp, W)

print(shares_as_points)

# print(e1)
# print(e2)

print(Rs[0] - e1)
print(Rs[1] - e2)
        


# In[ ]:




