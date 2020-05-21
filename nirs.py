#!/usr/bin/env python
# coding: utf-8

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

alpha = 51
beta = 35
W = alpha * G + beta * H


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


def pairings(Qs, Ps, W):
    res = []
    for Q, P in zip(Qs, Ps):
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
        a.append(randint(0,l - 1))
        b.append(randint(0,l - 1))
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
A = treshold_matrix_generation(t, n)
numbers = generate_pairings_numbers(t, l)
Ps = transform_to_points(numbers)
user_points = compute_shares(A, numbers) #giveaway to Users
Qs = transform_to_points(generate_pairings_numbers(t, l))
shares_as_points = pairings(Qs,Ps,W)
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


def subtract(Rs, Ts):
    res = []
    for R, T in zip(Rs, Ts):
        res.append(R - T)
    return res
    

def invert_matrix(A, rows):
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
        T = Integer(rows[i][0]) * Ss[i][0]
        for j in range(1, len(rows[i]), 1):
            T += Integer(rows[i][j]) * Ss[i][j]
        Ts.append(T)
    return Ts


rows = [0, 1]
Ss = calculate_S(Qs, user_points, W, rows)
inv = invert_matrix(A, rows)
Ts = calculate_T(Ss, inv)
recover = subtract(Rs, Ts)
print("secrets = {}".format(recover))



