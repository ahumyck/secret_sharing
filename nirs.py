#!/usr/bin/env python
# coding: utf-8

# In[26]:


def discriminant(a, b, p):
    return (4*a*a*a + 27*b*b) % p

def generate_random_elliptic_curve(field, prime):
    d = 0
    while d == 0:
        a = field.random_element()
        b = field.random_element()
        d = discriminant(a, b, prime)
    return EllipticCurve(field, [a,b])


def irredicublePolynomial(prime,power):
    R = GF(prime)['x']
    counter = 0
    for p in R.polynomials(power):
        if p.is_irreducible():
            return p

q = 139
F.<x> = GF(q)
E = generate_random_elliptic_curve(F, q)
print(E)


# In[62]:


t = 5
n = 8
l = 13


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

def compute_coefficients(A, t, l):
    _a, _b = generate_pairings_numbers(t, l)
    a = (A * _a.transpose()).column(0)
    b = (A * _b.transpose()).column(0)
    
    a_b = []
    for i in range(len(a)):
        a_b.append((a[i],b[i]))
        
    return a_b
    
    
    

m = treshold_matrix_generation(t, n)
print(compute_coefficients(m, t, l))
    



# In[ ]:




