print('Diszkrét modellek és alkalmazásai - Lab 5 - Euler and Fermat theorem')

# Euler and Fermat theorem
# Topics:
#  - Euler's phi function
#  - Euler-Fermat theorem
#  - Fermat's little theorem
#  - modular powers
#  - modular inverse using Euler-Fermat
#
# help:
#  - https://compalg.elte.gitlab-pages.hu/dimoa-web/gyakorlatok/number_theory/fermat
import sympy

# 1. Euler's phi function --------------------------------------------------------
def phi(n: int) -> int:
    """
    Return Euler's phi function value phi(n).

    This is the number of integers k with 1 <= k <= n such that gcd(k, n) == 1.

    Examples:
        phi(8) == 4, because 1, 3, 5, 7 are coprime to 8.
        phi(12) == 4, because 1, 5, 7, 11 are coprime to 12.
    """
    if n == 1:
        return 1
    ret = 0
    for k in range(1, n):
        if sympy.gcd(k,n) == 1:
            ret += 1
    
    return ret

# 2. Product formula for phi -----------------------------------------------------
def phi_from_factorization(factors: dict[int, int]) -> int:
    """
    Return phi(n) from the prime factorization of n.

    The input is a dictionary of the form

        {prime: exponent}

    representing

        n = p1^e1 * p2^e2 * ... * pk^ek.

    Use the formula

        phi(n) = n * (1 - 1/p1) * (1 - 1/p2) * ... * (1 - 1/pk).

    Example:
        phi_from_factorization({2: 3, 3: 1}) == phi(24) == 8
    """
    raise NotImplementedError

# 3. Reduced residue system ------------------------------------------------------
def reduced_residue_system(m: int) -> list[int]:
    """
    Return the reduced residue system modulo m.

    That is, return the list of all numbers a with

        0 <= a < m and gcd(a, m) == 1.

    The result should be sorted increasingly.

    Example:
        reduced_residue_system(10) == [1, 3, 7, 9]
    """
    raise NotImplementedError

# 4. Euler-Fermat theorem check --------------------------------------------------
def euler_fermat_check(a: int, m: int) -> bool:
    """
    Return whether the Euler-Fermat congruence holds for a and m.

    If gcd(a, m) == 1, then Euler-Fermat says that

        a^phi(m) == 1 (mod m).

    Return True if this congruence holds, and False otherwise.

    You may use the phi function above.
    """
    phis = phi(m)

    

# 5. Modular power using Euler-Fermat --------------------------------------------
def euler_fermat_power(a: int, k: int, m: int) -> int:
    """
    Return the smallest non-negative representative of a^k modulo m.

    You may assume that gcd(a, m) == 1.

    Use Euler-Fermat theorem to reduce the exponent k modulo phi(m).
    Do not use pow(a, k, m).
    """
    raise NotImplementedError


# 6. Fermat's little theorem -----------------------------------------------------
def fermat_little_theorem(a: int, p: int) -> bool:
    """
    Return whether Fermat's little theorem holds for a and p.

    You may assume that p is prime.

    If p does not divide a, then Fermat's little theorem says that

        a^(p - 1) == 1 (mod p).

    Return True if this congruence holds, and False otherwise.
    """
    raise NotImplementedError


# 7. Modular inverse using Euler-Fermat ------------------------------------------
def invmod_euler(a: int, m: int) -> int | None:
    """
    Return the inverse of a modulo m using Euler-Fermat theorem.

    If gcd(a, m) != 1, then the inverse does not exist, so return None.

    If gcd(a, m) == 1, then

        a^(phi(m) - 1)

    is the inverse of a modulo m.

    Return the smallest non-negative representative of the inverse.

    Do not use pow(a, -1, m).
    """
    raise NotImplementedError



# 8. Find exponent period --------------------------------------------------------
def exponent_period(a: int, m: int) -> int | None:
    """
    Return the smallest positive integer t such that

        a^t == 1 (mod m).

    If gcd(a, m) != 1, return None.

    This number is called the multiplicative order of a modulo m.
    """
    raise NotImplementedError


# 9. Last digit using Euler-Fermat -----------------------------------------------
def last_digit_of_power(a: int, k: int) -> int:
    """
    Return the last digit of a^k.

    That is, return a^k modulo 10.

    You may use Euler-Fermat theorem when a and 10 are coprime.
    Handle all values of a, including those not coprime to 10.
    """
    raise NotImplementedError


# Do not modify this part!
# From here there are no further exercises, this part is only for testing purposes.
if __name__ == '__main__':
    import math

    def check_phi():
        expected = {
            1: 1,
            2: 1,
            3: 2,
            4: 2,
            5: 4,
            6: 2,
            7: 6,
            8: 4,
            9: 6,
            10: 4,
            12: 4,
            15: 8,
            16: 8,
            18: 6,
            20: 8,
            24: 8,
            30: 8,
            36: 12,
        }

        for n, value in expected.items():
            if phi(n) != value:
                return False

        return True

    def check_reduced_residue_system():
        return (
            reduced_residue_system(8) == [1, 3, 5, 7]
            and reduced_residue_system(10) == [1, 3, 7, 9]
            and reduced_residue_system(12) == [1, 5, 7, 11]
            and reduced_residue_system(15) == [1, 2, 4, 7, 8, 11, 13, 14]
        )

    def check_euler_fermat_check():
        for m in range(2, 40):
            for a in range(1, 80):
                expected = math.gcd(a, m) == 1 and pow(a, phi(m), m) == 1
                if euler_fermat_check(a, m) != expected:
                    return False

        return True

    def check_euler_fermat_power():
        cases = [
            (3, 100, 10),
            (5, 123, 12),
            (7, 222, 15),
            (11, 50, 16),
            (13, 77, 18),
            (17, 91, 20),
            (19, 101, 21),
            (23, 88, 25),
        ]

        for a, k, m in cases:
            if euler_fermat_power(a, k, m) != pow(a, k, m):
                return False

        return True

    def check_fermat_little_theorem():
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

        for p in primes:
            for a in range(1, 3 * p):
                expected = a % p != 0 and pow(a, p - 1, p) == 1
                if fermat_little_theorem(a, p) != expected:
                    return False

        return True

    def check_invmod_euler():
        for m in range(2, 40):
            for a in range(1, m):
                try:
                    expected = pow(a, -1, m)
                except ValueError:
                    expected = None

                if invmod_euler(a, m) != expected:
                    return False

        return True

    def check_phi_from_factorization():
        return (
            phi_from_factorization({2: 3}) == 4
            and phi_from_factorization({2: 3, 3: 1}) == 8
            and phi_from_factorization({3: 2, 5: 1}) == 24
            and phi_from_factorization({2: 2, 5: 2}) == 40
        )

    def check_exponent_period():
        cases = [
            (3, 10, 4),
            (2, 5, 4),
            (5, 8, 2),
            (2, 9, 6),
            (4, 9, 3),
            (2, 10, None),
        ]

        for a, m, expected in cases:
            if exponent_period(a, m) != expected:
                return False

        return True

    def check_last_digit_of_power():
        cases = [
            (2, 10, 4),
            (3, 7, 7),
            (7, 100, 1),
            (9, 13, 9),
            (10, 50, 0),
            (12, 8, 6),
            (15, 3, 5),
        ]

        for a, k, expected in cases:
            if last_digit_of_power(a, k) != expected:
                return False

        return True

    tests = [
        ("phi", check_phi),
        ("reduced_residue_system", check_reduced_residue_system),
        ("euler_fermat_check", check_euler_fermat_check),
        ("euler_fermat_power", check_euler_fermat_power),
        ("fermat_little_theorem", check_fermat_little_theorem),
        ("invmod_euler", check_invmod_euler),
        ("phi_from_factorization", check_phi_from_factorization),
        ("exponent_period", check_exponent_period),
        ("last_digit_of_power", check_last_digit_of_power),
    ]

    for name, test in tests:
        try:
            assert test()
            print(f"{name:30} OK")
        except NotImplementedError:
            print(f"{name:30} not implemented")
        except AssertionError:
            print(f"{name:30} FAILED")