from dealer import Dealer
from oracle import Oracle

def secret_example(E, how_many_secrets):
    secrets = []
    for i in range(how_many_secrets):
        secrets.append(E.random_element())
    return secrets

t, n = 3, 5
d = Dealer(t, n)
E, q, l, k , G, H, W = d.get_public_bulletin()
secrets = secret_example(E, t)

secrets = secret_example(E, t) #secret_example
print("secrets =", secrets)

shares = d.compute_shares()
print("shares =", shares)
ver_info = d.verification_information()
Vs = ver_info['Vs']
Q = ver_info['Q']
print("Vs =", Vs)
print("Q =", Q)
Rs = d.get_public_bulletin_secrets(secrets)
print("Rs =", Rs)
print("\n\n------------------------------\n\n")
O = Oracle()
r_secrets = O.restore_secrets(Rs, shares, Vs, Q, l, W)
print("secrets = ", r_secrets)