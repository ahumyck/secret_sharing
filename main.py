from dealer import Dealer
from oracle import Oracle

def secret_example(E, how_many_secrets):
    secrets = []
    for i in range(how_many_secrets):
        secrets.append(E.random_element())
    return secrets

def collegium(UPs, rows):
    ups = []
    for i in range(len(rows)):
        ups.append(UPs[rows[i]])
    
    return ups

t, n = 2, 5
dealer = Dealer(t, n)
E, q, l, k, W = dealer.get_public_bulletin()
secrets = secret_example(E, t) #secret_example
print("secrets = ", secrets)
user_points = dealer.compute_shares()
print("user points =", user_points)
public_information = dealer.get_public_bulletin_secrets(secrets)

print("public")
for info in public_information:
    print(info)

users_who_wants_their_secret = [0, 2]
collegium_points = collegium(user_points, users_who_wants_their_secret)

oracle = Oracle(public_information, user_who_wants_their_secret, collegium_points)
secrets = oracle.restore_secrets(W)
print(secrets)