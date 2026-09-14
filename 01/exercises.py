print('Diszkrét modellek és alkalmazásai - Lab 1 - Python practice')
import math
# Python practice
# Topics:
#  - branches
#  - loops
#  - lists
#  - dictionaries
#  - simple algorithms

# help: https://compalg.elte.gitlab-pages.hu/dimoa-web/category/python

# 1. Triangle area ------------------------------------------------------------
# Calculate the area of a triangle from its side lengths.
# Return None if the sides cannot form a triangle.
def triangle_area(a: float | int, b: float | int, c: float | int) -> float | None:
    if a + b <= c or a + c <= b or b + c <= a:
        return None
    s = (a+b+c)/2
    return math.sqrt(s*(s-a)*(s-b)*(s-c))

# 2. Maximum of three numbers -------------------------------------------------
def max3(a, b, c):
    """Return the largest of the three numbers."""
    m = a
    for x in (b, c):
        if  x > m:
            m = x
    return m

# 3. Leap year ----------------------------------------------------------------
def is_leap(year: int) -> bool:
    """Return True iff year is a leap year."""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


# 4. Factorial ----------------------------------------------------------------
def factorial(n: int) -> int | None:
    """Return n!, or None if n is negative."""
    if n < 0:
        return None
    result = 1
    for i in range(2, n+1):
        result = result * i
    return result


# 5. Digit sum ----------------------------------------------------------------
def digit_sum(n: int, base: int = 10) -> int:
    """Return the sum of the digits of n."""
    total = 0
    while n > 0:
        total += n % base
        n //= base
    return total

# 6. Prime test ---------------------------------------------------------------
def is_prime(n: int) -> bool:
    """Return True iff n is prime."""
    sq = int (math.sqrt(n) + 1)
    if n < 2:
        return False
    for i in range(2, sq):
        if n % i == 0:
            return False
    return True
# 7. Fibonacci ----------------------------------------------------------------
def fibonacci(n: int) -> int:
    """
    Return the nth Fibonacci number.

    
    Your solution should also work efficiently for n=1000.
    """

    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a


# 8. Horner polynomial evaluation ---------------------------------------------
def horner(coeffs: list[int | float], x: int | float) -> int | float:
    """
    coeffs=[2,3,5] represents

        2x² + 3x + 5

    Evaluate the polynomial using Horner's method.
    """
    result = 0
    for coeff in coeffs:
        result = result * x + coeff
    return result

# 9. Pascal row ---------------------------------------------------------------
# candidate for TMS exercise
def pascal_row(n: int) -> list[int]:
    """
    Return the nth row of Pascal's triangle.

    Examples:
        pascal_row(0) -> [1]
        pascal_row(4) -> [1,4,6,4,1]

    Use only lists and calculate level-by-level (the list behaves as a queue, only `[0], pop(0)` and `append` can be used).
    """

    

# 10. Character histogram -----------------------------------------------------
def char_count(text: str) -> dict[str, int]:
    """
    Example:
        banana -> {'b':1,'a':3,'n':2}
    """
    raise NotImplementedError


# 11. Word histogram ----------------------------------------------------------
def word_count(words: str) -> dict[str, int]:
    raise NotImplementedError


# 12. Sparse polynomial -------------------------------------------------------
def sparse_poly(poly: list[int | float]) -> dict[int, int | float]:
    """
    Polynomial representation: [5,0,0,1,-7]

        5x⁴ + 3x - 7

    becomes

        {
            4: 5,
            1: 3,
            0: -7
        }
    """
    raise NotImplementedError


# Matrix multiply
def matrix_mul(a: list[list[int | float]], b: list[list[int | float]]) -> list[list[int | float]]:
    raise NotImplementedError


# +1 Complete the Set class.
# ---------------------------------------------------------------------------
class MySet:

    def __init__(self, values=None):
        self.data = []

        if values is not None:
            for v in values:
                if v not in self.data:
                    self.data.append(v)

    def __repr__(self):
        return "{" + ", ".join(map(str, self.data)) + "}"

    def contains(self, value):
        return value in self.data

    # Equality check with '=='
    def __eq__(self, other):
        return self.data == other.data

    # Implement the union of two sets.
    def union(self, other):
        raise NotImplementedError

    # + operator
    def _add__(self, other):
        return self.union(other)

    # Implement the intersection of two sets.
    def intersection(self, other):
        raise NotImplementedError


# Do not modify this part!
# From here there are no further exercises, this part is only for testing purposes.
if __name__ == '__main__':

    tests = [
        ("triangle_area", lambda: triangle_area(3, 4, 5) == 6),
        ("max3", lambda: max3(1, 7, 2) == 7),
        ("is_leap", lambda: is_leap(2024) and not is_leap(2023)),
        ("factorial", lambda: factorial(5) == 120),
        ("digit_sum", lambda: digit_sum(12345) == 15),
        ("is_prime", lambda: is_prime(17) and not is_prime(21)),
        ("fibonacci", lambda: fibonacci(10) == 55),
        ("horner", lambda: horner([2, 3, 5], 2) == 19),
        ("pascal_row", lambda: pascal_row(4) == [1, 4, 6, 4, 1]),
        ("char_count", lambda: char_count("banana") == {'b': 1, 'a': 3, 'n': 2}),
        ("word_count", lambda: word_count("aa a b aa bb c bb") == {'a': 1, 'aa': 2, 'b': 1, 'bb': 2, 'c': 1}),
        ("sparse_poly", lambda: sparse_poly([2, 0, 1]) == {2: 2, 0: 1}),
        ("matrix_mul", lambda: matrix_mul([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[19, 22], [43, 50]])
    ]

    for name, test in tests:
        try:
            assert test()
            print(f"{name:20} OK")
        except NotImplementedError:
            print(f"{name:20} not implemented")
        except AssertionError:
            print(f"{name:20} FAILED")

    s1 = MySet([1, 2, 3])
    s2 = MySet([3, 4, 5])
    try:
        assert MySet([i for i in range(1, 6)]) == s1.union(s2)
        print(f"{'Set:union':20} OK")
    except NotImplementedError:
        print(f"{'Set:union':20} not implemented")
    except AssertionError:
        print(f"{'Set:union':20} FAILED")
    try:
        assert MySet([3]) == s1.intersection(s2)
        print(f"{'Set:intersection':20} OK")
    except NotImplementedError:
        print(f"{'Set:intersection':20} not implemented")
    except AssertionError:
        print(f"{'Set:intersection':20} FAILED")
