from math import sqrt

def eraszt(n:int) -> list[int]:
    is_prime = [True] * (n+1)

    if n >= 0: is_prime[0] = False
    if n <= 1: is_prime[1] = False

    p = 2

    while p*p < n:
        if is_prime[p] == True:
            for i in range(p*p, n+1, p):
                is_prime[i] = False

        p+=1

    
    primes = []
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            
    return primes


print(eraszt(2000))