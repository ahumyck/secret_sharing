from dealer import Dealer
from oracle import Oracle

t, n = 3, 5
dealer = Dealer(t, n)

E, q, L, k, G, H, W = dealer.get_public_bulletin()
shares = dealer.compute_shares()

def secret_example(field, how_many_secrets):
    secrets = []
    for i in range(how_many_secrets):
        secrets.append(field.random_element())
    return secrets


F.<x> = GF(q)
secrets = secret_example(F, 2)
masked_secrets = dealer.get_public_bulletin_secrets(secrets)
ver_info = dealer.verification_information()

pairing_params = L, G, H, W
def build_authorized_set_of_users(shares, user_set):
    res = dict()
    for key in shares:
        if key in user_set:
            res[key] = shares[key]
    return res


user_set = [1, 3, 5]
authorized_shares = build_authorized_set_of_users(shares, user_set)
oracle = Oracle()
r_secrets, verification_result = oracle.restore_secrets(masked_secrets, 
                                        authorized_shares, ver_info, pairing_params)

result, msg = verification_result
if result:
    print(msg)
    print(r_secrets)