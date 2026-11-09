print('Diszkrét modellek és alkalmazásai - 1. ZH minta - gépes rész')

# A math és a sympy használható, kivéve a sympy.crypto modult és a feladatnál
# külön tiltott függvényeket. A fájl futtatása minden feladatra kiírja, hogy
# OK, not implemented vagy FAILED, az utóbbinál azt is, mit vártunk és mi jött ki.
import math
import sympy


# 1. feladat (5 pont) --------------------------------------------------------
# Add vissza növekvő listában azokat az a elemeket (0≤a<m), amelyek önmaguk
# inverzei modulo m, vagyis a·a≡1 (m).
# Nem használható: sympy.ntheory.sqrt_mod.
def self_inverse(m):
    returned = []
    for a in range(1, m):
        if ((a*a)%m) == 1:
            returned.append(a)
    return returned


# 2. feladat (5 pont) --------------------------------------------------------
# Ha (a,m)=1, add vissza a legkisebb pozitív r kitevőt, amelyre a^k≡a^r (m)
# biztosan teljesül. Ha k osztható φ(m)-mel, az eredmény φ(m), nem 0.
def reduce_exponent(a, k, m):
    if sympy.totient(m) % k == 0:
        return sympy.totient(m)
    if math.gcd(a,m) == 1:
        for r in range(2,m):
            if(pow(a,k,m) == pow(a,r,m)):
                return r



# 3. feladat (7 pont) --------------------------------------------------------
# Egy n>1 egész számról döntsd el, hogy prímhatvány-e, vagyis felírható-e
# n=p^k alakban, ahol p prím és k≥1.
# Nem használható: sympy.perfect_power.
def is_prime_power(n):
    for p in range(2, n+1):
        if sympy.isprime(p):
            for k in range(1,n):
                if n == pow(p,k):
                    return True
    return False

# 4. feladat (9 pont) --------------------------------------------------------
# Egy RSA modulusról (n=pq) a támadó megszerezte φ(n) értékét. Add vissza a
# (p,q) párt, p<q.
# Nem használható: sympy.factorint.
def rsa_factor_from_phi(n, phi):
    for q in range(2,n):
        if sympy.isprime(q):
            for p in range(2, n):
                if sympy.isprime(p) and n == p*q and p<q:
                    return p,q


# Do not modify this part!
if __name__ == '__main__':
    tests = [
        ('self_inverse', "assert self_inverse(8) == [1, 3, 5, 7], f'self_inverse(8): várt [1, 3, 5, 7], kapott {self_inverse(8)!r}'\nassert self_inverse(7) == [1, 6], f'self_inverse(7): várt [1, 6], kapott {self_inverse(7)!r}'\nassert self_inverse(12) == [1, 5, 7, 11], f'self_inverse(12): várt [1, 5, 7, 11], kapott {self_inverse(12)!r}'\nassert self_inverse(2) == [1], f'self_inverse(2): várt [1], kapott {self_inverse(2)!r}'\nassert self_inverse(15) == [1, 4, 11, 14], f'self_inverse(15): várt [1, 4, 11, 14], kapott {self_inverse(15)!r}'"),
        ('reduce_exponent', "assert reduce_exponent(7, 222, 10) == 2, f'reduce_exponent(7, 222, 10): várt 2, kapott {reduce_exponent(7, 222, 10)!r}'\nassert reduce_exponent(7, 8, 10) == 4, f'reduce_exponent(7, 8, 10): várt 4, kapott {reduce_exponent(7, 8, 10)!r}'\nassert reduce_exponent(3, 5, 7) == 5, f'reduce_exponent(3, 5, 7): várt 5, kapott {reduce_exponent(3, 5, 7)!r}'\nassert reduce_exponent(2, 100, 7) == 4, f'reduce_exponent(2, 100, 7): várt 4, kapott {reduce_exponent(2, 100, 7)!r}'\nassert pow(7, int(reduce_exponent(7, 222, 10)), 10) == pow(7, 222, 10), f'pow(7, int(reduce_exponent(7, 222, 10)), 10): várt {pow(7, 222, 10)!r}, kapott {pow(7, int(reduce_exponent(7, 222, 10)), 10)!r}'"),
        ('is_prime_power', "assert is_prime_power(8), f'is_prime_power(8): várt True, kapott {is_prime_power(8)!r}'\nassert is_prime_power(7), f'is_prime_power(7): várt True, kapott {is_prime_power(7)!r}'\nassert not is_prime_power(12), f'is_prime_power(12): várt False, kapott {is_prime_power(12)!r}'\nassert is_prime_power(243), f'is_prime_power(243): várt True, kapott {is_prime_power(243)!r}'\nassert not is_prime_power(1000), f'is_prime_power(1000): várt False, kapott {is_prime_power(1000)!r}'"),
        ('rsa_factor_from_phi', "assert rsa_factor_from_phi(33, 20) == (3, 11), f'rsa_factor_from_phi(33, 20): várt {(3, 11)!r}, kapott {rsa_factor_from_phi(33, 20)!r}'\nassert rsa_factor_from_phi(3233, 3120) == (53, 61), f'rsa_factor_from_phi(3233, 3120): várt {(53, 61)!r}, kapott {rsa_factor_from_phi(3233, 3120)!r}'\nassert rsa_factor_from_phi(10403, 10200) == (101, 103), f'rsa_factor_from_phi(10403, 10200): várt {(101, 103)!r}, kapott {rsa_factor_from_phi(10403, 10200)!r}'"),
    ]
    for name, code in tests:
        try:
            exec(code, globals())
            print(f'{name:28} OK')
        except NotImplementedError:
            print(f'{name:28} not implemented')
        except AssertionError as e:
            print(f'{name:28} FAILED: {e}')