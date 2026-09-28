print('Diszkrét modellek és alkalmazásai - Lab 3 - GCD and Diophantine equations')

# GCD and Diophantine equations
# Topics:
#  - greatest common divisor and least common multiple from prime factorization
#  - Euclidean algorithm
#  - extended Euclidean algorithm
#  - linear Diophantine equations
#
# help:
#  - https://compalg.elte.gitlab-pages.hu/dimoa-web/gyakorlatok/number_theory/lnko
#  - https://compalg.elte.gitlab-pages.hu/dimoa-web/gyakorlatok/number_theory/diofantikus

import sympy
# 1. GCD from prime factorization ---------------------------------------------
def gcd_factor(a: int, b: int) -> int:
    """
    Return the greatest common divisor of a and b using their prime
    factorizations.

    You may use sympy.factorint(n), which returns the factorization as a
    dict {prime: exponent}, e.g. factorint(360) == {2: 3, 3: 2, 5: 1}.
    Do not use math.gcd.
    """
    fa = sympy.factorint(a)
    fb = sympy.factorint(b)
    ret={}
    for ak, av in fa.items():
        for bk, bv in fb.items():
            if ak == bk:
                ret[ak] = min(av, bv)
    r = 1
    for rk, rv in ret.items():
        r *= rk ** rv
    return r

# 2. LCM from prime factorization ---------------------------------------------
def lcm_factor(a: int, b: int) -> int:
    """
    Return the least common multiple of a and b using their prime
    factorizations.

    Do not use math.lcm.
    """
    for i in range(max(a, b), a * b + 1):
        if i % a == 0 and i % b == 0:
            return i
    return a * b

# 3. Euclidean algorithm ------------------------------------------------------
def gcd_euclid(a: int, b: int) -> int:
    """
    Return the greatest common divisor of a and b using the Euclidean
    algorithm (repeated division with remainder).

    Do not use math.gcd.
    """
    q, r = divmod(a, b)
    while r != 0:
        a, b = b, r
        q, r = divmod(a, b)
    return b

# 4. Extended Euclidean algorithm ---------------------------------------------
def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Return (x, y, r) such that

        a * x + b * y == r   and   r == gcd(a, b).
    """
    raise NotImplementedError


# 5. Number of integer solutions ----------------------------------------------
def num_of_solutions(a: int, b: int, c: int) -> float:
    """
    Return the number of integer solutions (x, y) of a * x + b * y == c.

    This is either 0 or math.inf.
    """
    raise NotImplementedError


# 6. Linear Diophantine equation ----------------------------------------------
class LinDiophantineEq:
    """
    Represents the equation a * x + b * y == c over the integers.

    - is_solvable() tells whether there is an integer solution.
    - next_solution() and prev_solution() step through the solutions.
    - The first call of next_solution() returns the solution with the
      smallest non-negative x.
    - Store only one solution at a time.
    """

    def __init__(self, a: int, b: int, c: int):
        self.t = 0
        self.g = ...

    def is_solvable(self) -> bool:
        raise NotImplementedError

    def actual_solution()
        self.t
        

    def next_solution(self) -> tuple[int, int]:
        self.t += 1
        return self.actual_solution()
    def prev_solution(self) -> tuple[int, int]:
        raise NotImplementedError


# 7. Paying with two coins ----------------------------------------------------
def num_of_payments(amount: int, coin1: int, coin2: int) -> int:
    """
    Return in how many ways amount can be paid using coins of value coin1
    and coin2 (non-negative number of each).

    Brute force is not allowed, use LinDiophantineEq.
    """
    raise NotImplementedError


# Practice exercises ----------------------------------------------------------

# 8. Binary GCD ---------------------------------------------------------------
def binary_gcd(a: int, b: int) -> int:
    """
    Return gcd(a, b) using only additive (+, -) and shift (<<, >>)
    operations.

    Use the identities
        gcd(2a, 2b) == 2 * gcd(a, b)
        gcd(2a, b) == gcd(a, b)        if b is odd
        gcd(a, b) == gcd(a - b, b)     if a >= b
    """
    raise NotImplementedError


# 9. Binary extended GCD ------------------------------------------------------
def binary_xgcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Return (x, y, r) with a * x + b * y == r == gcd(a, b) using the
    binary extended GCD algorithm.
    """
    raise NotImplementedError


# 10. Number of non-negative solutions ----------------------------------------
def num_of_nat_solutions(a: int, b: int, c: int) -> float:
    """
    Return the number of solutions (x, y) of a * x + b * y == c with
    x >= 0 and y >= 0.

    Return math.inf if there are infinitely many.
    """
    raise NotImplementedError


# 11. Buying chocolate --------------------------------------------------------
def num_of_purchases() -> int:
    """
    A shop sells three kinds of chocolate for 70, 130 and 150 forints.
    Return in how many ways one can buy exactly 50 chocolates for exactly
    5000 forints.

    Brute force is not allowed, reduce the problem to a linear
    Diophantine equation in two unknowns.
    """
    raise NotImplementedError


# 12. Multi-coin count --------------------------------------------------------
def multi(L: list[int], c: int, s: int = 0) -> int:
    """
    Return the number of non-negative integer solutions of

        L[0] * x_0 + L[1] * x_1 + ... + L[n] * x_n == c

    if s == 0, otherwise the number of those solutions that also satisfy

        x_0 + x_1 + ... + x_n >= s.
    """
    raise NotImplementedError


# Do not modify this part!
# From here there are no further exercises, this part is only for testing purposes.
if __name__ == '__main__':
    import math

    def check_xgcd(fn, a, b):
        x, y, r = fn(a, b)
        return a * x + b * y == r and r == math.gcd(a, b)

    def check_eq():
        E = LinDiophantineEq(9, 6, 13)
        if E.is_solvable():
            return False
        E = LinDiophantineEq(12, 30, 72)
        return (E.is_solvable()
                and E.next_solution() == (1, 2)
                and E.next_solution() == (6, 0)
                and E.prev_solution() == (1, 2)
                and E.prev_solution() == (-4, 4))

    tests = [
        ("gcd_factor", lambda: gcd_factor(24, 36) == 12 and gcd_factor(252, 198) == 18),
        ("lcm_factor", lambda: lcm_factor(24, 36) == 72 and lcm_factor(4, 6) == 12),
        ("gcd_euclid", lambda: gcd_euclid(252, 198) == 18 and gcd_euclid(24, 36) == 12),
        ("extended_gcd", lambda: check_xgcd(extended_gcd, 252, 198) and check_xgcd(extended_gcd, 24, 36)),
        ("num_of_solutions", lambda: num_of_solutions(3, 5, 7) == math.inf and num_of_solutions(6, 9, 20) == 0),
        ("LinDiophantineEq", check_eq),
        ("num_of_payments", lambda: num_of_payments(100000, 47, 79) == 27),
        ("binary_gcd", lambda: binary_gcd(252, 198) == 18 and binary_gcd(24, 36) == 12),
        ("binary_xgcd", lambda: check_xgcd(binary_xgcd, 252, 198) and check_xgcd(binary_xgcd, 24, 36)),
        ("num_of_nat_solutions", lambda: num_of_nat_solutions(12, 30, 72) == 2 and num_of_nat_solutions(-12, 30, 72) == math.inf),
        ("num_of_purchases", lambda: num_of_purchases() == 7),
        ("multi", lambda: multi([2, 3], 12) == 3 and multi([2, 3], 12, 5) == 2),
    ]

    for name, test in tests:
        try:
            assert test()
            print(f"{name:20} OK")
        except NotImplementedError:
            print(f"{name:20} not implemented")
        except AssertionError:
            print(f"{name:20} FAILED")
