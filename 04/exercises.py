print('Diszkrét modellek és alkalmazásai - Lab 4 - Congruences and residue systems')

# Congruences and residue systems
# Topics:
#  - residue classes and residue systems
#  - modular inverse
#  - linear congruences
#  - systems of linear congruences, Chinese remainder theorem
#
# help:
#  - https://compalg.elte.gitlab-pages.hu/dimoa-web/gyakorlatok/number_theory/kongruencia


# 1. Representative of a residue class ----------------------------------------
def find_class_representative(x: int, m: int) -> int:
    """
    Return the representative of the residue class of x modulo m, chosen
    from 0, 1, ..., m - 1.

    A negative x has a non-negative representative as well, for example
    find_class_representative(-1, 5) == 4.
    """
    return x % m


# 2. Classifying a list -------------------------------------------------------
def classify_elements(input_set: list[int], m: int) -> dict[int, list[int]]:
    """
    Group the elements of the list by their residue class modulo m.

    The keys are the representatives 0, 1, ..., m - 1, the values are the
    elements belonging to that class, in their original order. A class
    with no element gets no key.
    """
    result = {}

    for elem in input_set:
        mod = elem % m
        if mod in result:
            result[mod].append(elem)
        else:
            result[mod] = [elem]
    return result


# 3. Modular inverse ----------------------------------------------------------
def invmod(a: int, m: int) -> int | None:
    """
    Return the inverse of a modulo m, that is, the x with 0 <= x < m for
    which a * x == 1 (mod m). Return None if there is no such x.

    Use the extended Euclidean algorithm: in the form a * x + m * y ==
    gcd(a, m) the coefficient of a is the inverse, provided that
    gcd(a, m) == 1. Do not use pow(a, -1, m).
    """
    for i in range(m):
        if (a*i)%m == 1:
            return i
    return None


# 4. Linear congruence --------------------------------------------------------
def my_solve_mod(a: int, b: int, m: int) -> set[int]:
    """
    Return the set of solutions x with 0 <= x < m of

        a * x == b (mod m),

    or the empty set if there is no solution. The invmod function above
    may be used.

    Let d = gcd(a, m). There is a solution exactly when d divides b, and
    then the coefficient of the reduced congruence is already invertible
    modulo m / d. From its single solution the d solutions follow at
    distance m / d from each other.
    """
    megoldasok = set()
    for i in range(m):
        if (a*i)%m == b%m:
            megoldasok.add(i)
    return megoldasok


# Practice exercises ----------------------------------------------------------

# 5. Chinese remainder theorem ------------------------------------------------
def my_crt(c: list[int], m: list[int]) -> int:
    """
    Solve the system

        x == c[i] (mod m[i])

    for pairwise coprime moduli, and return the single solution with
    0 <= x < m[0] * m[1] * ... * m[n]. The invmod function above may be
    used.

    Build the solution one congruence at a time. Start with x = c[0] and
    M = m[0]. Taking a new congruence, with u = invmod(M, m[i]) the value

        x' = x + M * u * (c[i] - x)

    is still x modulo M, but it is already c[i] modulo m[i]. Then reduce
    x' modulo M * m[i], and the modulus grows to M * m[i].
    """
    raise NotImplementedError


# 6. System of linear congruences ---------------------------------------------
def solve_system(a: list[int], b: list[int], m: list[int]) -> set[int]:
    """
    Return the set of solutions x with 0 <= x < lcm(m[0], ..., m[n]) of
    the system

        a[i] * x == b[i] (mod m[i]),

    or the empty set if there is no solution. The moduli are not
    necessarily coprime.

    Take the congruences one by one. If the first ones are already solved
    modulo M, then taking a new congruence the modulus becomes
    lcm(M, m[i]). Lift every solution so far to the new modulus in steps
    of M, and keep those that satisfy the new congruence too.
    """
    raise NotImplementedError


# 7. Quadratic residues -------------------------------------------------------
def quadratic_residues(m: int) -> set[int]:
    """
    Return the set of those b with 0 <= b < m for which

        x * x == b (mod m)

    has a solution.
    """
    raise NotImplementedError


# Do not modify this part!
# From here there are no further exercises, this part is only for testing purposes.
if __name__ == '__main__':
    import math

    def check_invmod():
        for m in range(2, 40):
            for a in range(1, m):
                try:
                    expected = pow(a, -1, m)
                except ValueError:
                    expected = None
                if invmod(a, m) != expected:
                    return False
        return True

    def check_solve_mod():
        for m in range(2, 30):
            for a in range(1, m + 1):
                for b in range(m):
                    expected = {x for x in range(m) if (a * x - b) % m == 0}
                    if set(my_solve_mod(a, b, m)) != expected:
                        return False
        return True

    def check_crt():
        if my_crt([2, 3, 2], [3, 5, 7]) != 23 or my_crt([1, 1], [4, 9]) != 1:
            return False
        for m in ([3, 5, 7], [4, 9, 25], [2, 3, 5, 7], [11, 13]):
            product = math.prod(m)
            for start in range(0, product, max(1, product // 20)):
                c = [start % mi for mi in m]
                x = my_crt(c, m)
                if not (0 <= x < product) or any(x % mi != ci for ci, mi in zip(c, m)):
                    return False
        return True

    def check_system():
        cases = [
            ([1, 1, 1], [2, 3, 2], [3, 5, 7]),
            ([3, 4], [1, 2], [7, 10]),
            ([2, 3], [2, 6], [4, 9]),
            ([2, 3], [4, 3], [6, 9]),
            ([4, 6, 3], [2, 3, 9], [6, 8, 12]),
            ([5, 2], [3, 0], [11, 4]),
        ]
        for a, b, m in cases:
            L = math.lcm(*m)
            expected = {x for x in range(L)
                        if all((ai * x - bi) % mi == 0 for ai, bi, mi in zip(a, b, m))}
            if solve_system(a, b, m) != expected:
                return False
        return True

    tests = [
        ("find_class_representative", lambda: find_class_representative(14, 5) == 4 and find_class_representative(-1, 5) == 4 and find_class_representative(-10, 5) == 0),
        ("classify_elements", lambda: classify_elements([1, 7, 9, 10], 3) == {1: [1, 7, 10], 0: [9]} and classify_elements([-4, 6, -10, 12, -123], 4) == {0: [-4, 12], 2: [6, -10], 1: [-123]}),
        ("invmod", check_invmod),
        ("my_solve_mod", check_solve_mod),
        ("my_crt", check_crt),
        ("solve_system", check_system),
        ("quadratic_residues", lambda: quadratic_residues(11) == {0, 1, 3, 4, 5, 9} and quadratic_residues(8) == {0, 1, 4} and quadratic_residues(12) == {0, 1, 4, 9}),
    ]

    for name, test in tests:
        try:
            assert test()
            print(f"{name:25} OK")
        except NotImplementedError:
            print(f"{name:25} not implemented")
        except AssertionError:
            print(f"{name:25} FAILED")
