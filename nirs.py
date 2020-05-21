#!/usr/bin/env python
# coding: utf-8

# In[18]:


def torsion_subgroup_generator(E, r):
    G, H = E.gens()
    n = G.order() // r
    return n * G, n * H

p = 47
r = 6
q = p ** r
k = 1
F.<x> = GF(q)
E = EllipticCurve(F, [4, 0])
G, H  = torsion_subgroup_generator(E, 103)

alpha = 51
beta = 35
W = alpha * G + beta * H
        


# In[ ]:


def secret_example(E, how_many_secrets):
    secrets = []
    for i in range(how_many_secrets):
        secrets.append(E.random_element())
    
    return secrets
        

def treshold_matrix_generation(t,n):
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
    return (matrix([a]),matrix([b]))

def compute_shares(A, t, l):
    _a, _b = generate_pairings_numbers(t, l)
    a = (A * _a.transpose()).column(0)
    b = (A * _b.transpose()).column(0)
    
    a_b = []
    for i in range(len(a)):
        a_b.append((a[i],b[i]))
        
    return a_b

# E, q, l, k, alpha, beta, W = example()
# t, n = 2, 3
# secrets_number = 2
# A = treshold_matrix_generation(t, n)
# p_shares = compute_shares(A, t, l)
# secrets = secret_example(E, secrets_number)
# print(p_shares)


# In[ ]:





# In[ ]:




