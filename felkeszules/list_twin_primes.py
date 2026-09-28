from math import sqrt
def is_prime(a:int) -> bool:
    if a < 2:
        return False

    for i in range(2,int(sqrt(a)+1)):
        if a%i == 0:
            return False
    
    return True

def list_twin_primes(a, b) -> list[int]:
    primes = []
    for i in range(a, b+1):
        if is_prime(i) == True:
            primes.append(i)

    result = []

    for i in primes:
        for j in primes:
            if j-i == 2:
                result.append((i,j))

    return result



#TEST

assert list_twin_primes(130, 181) == [(137, 139), (149, 151), (179, 181)], 'list_twin_primes(130, 181) eredménye hibás'
assert list_twin_primes(12, 70) == [(17, 19), (29, 31), (41, 43), (59, 61)], 'list_twin_primes(12, 70) eredménye hibás'
assert list_twin_primes(62, 109) == [(71, 73), (101, 103), (107, 109)], 'list_twin_primes(62, 109) eredménye hibás'
assert list_twin_primes(75, 91) == [], 'list_twin_primes(75, 91) eredménye hibás'
assert list_twin_primes(110, 172) == [(137, 139), (149, 151)], 'list_twin_primes(110, 172) eredménye hibás'
assert list_twin_primes(109, 226) == [(137, 139), (149, 151), (179, 181), (191, 193), (197, 199)], 'list_twin_primes(109, 226) eredménye hibás'
print("OK!")