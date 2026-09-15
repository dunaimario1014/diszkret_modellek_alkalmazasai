# Írj programot, amely egy adott Z_m struktúrában definíció alapján meghatározza az egységeket, irreducibiliseket és prímeket!
import math
def divides_mod_n(a:int, b:int, m:int) -> bool:
    for c in range(m):
        if(a * c) % m == b % m:
            return True
    return False

def is_associated_mod_n(a:int, b:int, n:int) -> bool:
    if divides_mod_n(a, b, n) and divides_mod_n(b, a, n):
        return True
    return False

def is_unit_mod_n(a:int, n:int) -> bool:
    if divides_mod_n(a, 1, n):
        return True
    return False

def is_irreducible_mod_n(a:int, n:int) -> bool:
    if a == 0 or is_unit_mod_n(a, n):
        return False
    
    for b in range(n):
        for c in range(n):
            if (b*c)%n == a%n:
                if not is_unit_mod_n(b,n) and not is_unit_mod_n(c,n):
                    return False
    return True
    
def is_prime_mod_n(p:int, n:int) -> bool:
    if p <= 0 or is_unit_mod_n(p,n):
        return False
    for a in range(n):
        for b in range(n):
            if divides_mod_n(p,a*b,n):
                if not divides_mod_n(p,a,n) and not divides_mod_n(p,b,n):
                    return False
    return True

# DO NOT MODIFY THE FOLLOWING
if __name__ == "__main__":
    testcases = [
        ( divides_mod_n, [ ((1, 1, 2), True), ((1, 1, 3), True), ((1, 3, 4), True), ((2, 1, 4), False), ((2, 2, 4), True), ((2, 3, 4), False) ] ),
        ( is_associated_mod_n, [ ((1, 1, 2), True), ((1, 1, 3), True), ((1, 2, 4), False), ((1, 3, 4), True), ((2, 1, 4), False), ((2, 2, 4), True), ((2, 3, 4), False), ((3, 1, 4), True), ] ),
        ( is_unit_mod_n, [ ((0, 2), False), ((1, 2), True), ((0, 3), False), ((1, 3), True), ((0, 6), False), ((1, 6), True), ((2, 6), False), ((3, 6), False), ((4, 6), False), ((5, 6), True), ] ),
        ( is_irreducible_mod_n, [ ((0, 2), False), ((1, 2), False), ((1, 4), False), ((2, 4), True), ((3, 4), False), ((3, 6), False), ((4, 6), False), ((5, 6), False), ((6, 8), True), ((6, 10), False), ] ),
        ( is_prime_mod_n, [ ((0, 2), False), ((1, 2), False), ((2, 4), True), ((3, 6), True), ((4, 6), True), ((1, 10), False), ((2, 10), True), ] ),
    ]

    for func, tcs in testcases:
        error = False
        try:
            for iput, oput in tcs:
                assert func(*iput) == oput, f"Failed for {func.__name__} with input {iput}, the result was {func(*iput)}, but expected {oput}"
        except NotImplementedError:
            print(f"{func.__name__}: not implemented")
            error = True
        except AssertionError as ae:
            print(f"{func.__name__}: {ae}")
            error = True
        if not error:
            print(f"{func.__name__}: OK")
