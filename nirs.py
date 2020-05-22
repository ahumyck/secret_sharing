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
        


# In[2]:


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
user_points = compute_shares(A, numbers) #giveaway to Users
Qs = transform_to_points(generate_pairings_numbers(t, l))
shares_as_points = pairings(Qs,P,W)
Rs = add(shares_as_points, secrets)

public_information = generate_public_shares(Qs,Rs)

print("secrets = {}".format(secrets))
print("user_points = {}".format(user_points))

print("\npublic")
for info in public_information:
    print(info)



# In[3]:


def subtract(Rs, Ts):
    res = []
    for R, T in zip(Rs, Ts):
        res.append(R - T)
    return res

def calculate_S(Qs, UPs, W, rows):
    S = []
    for Q in Qs:
        tmp = []
        for row in rows:
            tmp.append(pairing(Q, UPs[row], W))
        S.append(tmp)
    return S

rows = [0, 2]
pseudo_shares = calculate_S(Qs, user_points, W, rows)
    


# In[4]:


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

def restore_last_point(last_matrix_row, user_points, rows):
    x, y = 0, 0
    for i in range(len(rows)):
        a, b = user_points[rows[i]]
        x += last_matrix_row[i] * a
        y += last_matrix_row[i] * b
    return x, y


def get_coefficients_from_public_information(public_information):
    qs = []
    for info in public_information:
        qs.append((info[0], info[1]))
    return qs

def get_points_from_public_information(public_information):
    rs = []
    for info in public_information:
        rs.append(info[-1])
    return rs


last_matrix_row = calculate_last_matrix_row(rows)
pppp = restore_last_point(last_matrix_row, user_points, rows)
print("expected ~P(t) =", P)
print("~actual  ~P(t) =", pppp)
if P == pppp:
    qqqq = get_coefficients_from_public_information(public_information)
    rrrr = get_points_from_public_information(public_information)
    eeee = pairings(qqqq, P, W)
    ssss = subtract(rrrr, eeee)
    print(ssss)
       


# In[ ]:




