import hashlib

def digest(n, message):
    return int.from_bytes(hashlib.sha256(message).digest(), 'big') % n

class RSA:
    def __init__(self, p, q, e):
        self.e = e
        self.n = p*q
        phi = (p-1)*(q-1)
        self.d = pow(e, -1, phi)
    def public_key(self):
        return(self.n, self.e)
    @staticmethod
    def encrypt(pubkey, message):
        n, e = pubkey
        return pow(message, e, n)
    def decrypt(self, secret):
        return pow(secret, self.d, self.n)
    def sign(self, message):
        return (message, pow(digest(self.n, message), self.d, self.n))
    @staticmethod
    def verify(pubkey, signed_message):
        n, e = pubkey
        message, signature = signed_message
        return digest(n, message) == pow(signature, e, n)
        

alice = RSA(61, 53, 17)
assert alice.public_key() == (3233, 17), 'public_key() eredménye hibás'
assert RSA.encrypt(alice.public_key(), 65) == 2790, 'encrypt(65) eredménye hibás'
assert alice.decrypt(2790) == 65, 'decrypt(2790) eredménye hibás'
for m in range(0, 3233, 97):
    assert alice.decrypt(RSA.encrypt(alice.public_key(), m)) == m, f'decrypt(encrypt({m})) nem adja vissza az üzenetet'
signed = alice.sign(b'Diszkret modellek')
assert RSA.verify(alice.public_key(), signed), 'a saját aláírás nem validálható'
assert not RSA.verify(alice.public_key(), (b'Diszkret modelek', signed[1])), 'módosított üzenet aláírása validálódik'
bob = RSA(1009, 1013, 65537)
assert not RSA.verify(bob.public_key(), signed), 'más kulcsú aláírás validálódik'
print("RSA: OK!")


import random

class DH_participant:
    def __init__(self, p, g):
        self.p = p
        self.g = g
        self.x = random.randint(1,p-1)
    def get_pub(self): # returns with the public parameter
        return pow(self.g, self.x, self.p)

    def calculate_common_key(self, pub_of_other):
        return pow(pub_of_other, self.x, self.p)

Alice = DH_participant(65537, 3)
Bob = DH_participant(65537, 3)
assert Alice.calculate_common_key(Bob.get_pub()) == Bob.calculate_common_key(Alice.get_pub()), 'a két fél kulcsa eltér'
assert Alice.get_pub() != Bob.get_pub(), 'a két fél publikus értéke megegyezik, a titok nem véletlen'
print("Diffie-Helman: OK!")