import math

a = 21
b = 10
print("Division (result is float)           a/b             = ", a/b)
print("Floor division (result is integer):  a//b            = ", a//b)
print("                                     math.floor(a/b) = ", math.floor(a/b))
print("Remainder:                           a%b             = ", a%b)
print("Divmod:                              divmod(a,b)     = ", divmod(a,b))

def divides(a: int, b: int) -> bool:
    """Return True iff a divides b."""
    return b % a == 0

def divides2(a:int, b:int) -> bool:
    _, r = divmod(b, a)
    return r == 0

def divides3(a:int, b:int) -> bool:
    """Return True iff a divides b."""
    return (b / a) * a == b 


def divides_all(a, limit):
    if a == 0:
        return False

    for n in range(1, limit+1):
        if (n**3-n) % a != 0:
            return False
    return True

def find_largest(max_a, limit):

    for a in range(max_a, 0, -1):
            if divides_all(a, limit):
                return a

    return None

assert divides_all(1, 100) == True, 'divides_all(1, 100) eredménye hibás'
assert divides_all(2, 100) == True, 'divides_all(2, 100) eredménye hibás'
assert divides_all(3, 100) == True, 'divides_all(3, 100) eredménye hibás'
assert divides_all(4, 100) == False, 'divides_all(4, 100) eredménye hibás'
assert divides_all(5, 100) == False, 'divides_all(5, 100) eredménye hibás'
assert divides_all(6, 100) == True, 'divides_all(6, 100) eredménye hibás'
assert divides_all(7, 100) == False, 'divides_all(7, 100) eredménye hibás'
assert divides_all(12, 100) == False, 'divides_all(12, 100) eredménye hibás'
assert divides_all(6, 1) == True, 'divides_all(6, 1) eredménye hibás'
assert divides_all(6, 10000) == True, 'divides_all(6, 10000) eredménye hibás'
assert find_largest(20, 100) == 6, 'find_largest(20, 100) eredménye hibás'
assert find_largest(100, 100) == 6, 'find_largest(100, 100) eredménye hibás'
assert find_largest(100, 1000) == 6, 'find_largest(100, 1000) eredménye hibás'
assert find_largest(3, 100) == 3, 'find_largest(3, 100) eredménye hibás'
print("OK!")


def num_of_divisors(a):
    count = 0
    for i in range(1, a+1):
        if a % i == 0:
            count += 1
    return count

def sum_of_divisors(a):
    total = 0
    for i in range(1, a+1):
        if a % i == 0:
            total += i
    return total

assert num_of_divisors(1) == 1, 'num_of_divisors(1) eredménye hibás'
assert num_of_divisors(6) == 4, 'num_of_divisors(6) eredménye hibás'
assert num_of_divisors(12) == 6, 'num_of_divisors(12) eredménye hibás'
assert num_of_divisors(13) == 2, 'num_of_divisors(13) eredménye hibás'
assert num_of_divisors(16) == 5, 'num_of_divisors(16) eredménye hibás'
assert num_of_divisors(28) == 6, 'num_of_divisors(28) eredménye hibás'
assert num_of_divisors(36) == 9, 'num_of_divisors(36) eredménye hibás'
assert num_of_divisors(100) == 9, 'num_of_divisors(100) eredménye hibás'

assert sum_of_divisors(1) == 1, 'sum_of_divisors(1) eredménye hibás'
assert sum_of_divisors(6) == 12, 'sum_of_divisors(6) eredménye hibás'
assert sum_of_divisors(12) == 28, 'sum_of_divisors(12) eredménye hibás'
assert sum_of_divisors(13) == 14, 'sum_of_divisors(13) eredménye hibás'
assert sum_of_divisors(16) == 31, 'sum_of_divisors(16) eredménye hibás'
assert sum_of_divisors(28) == 56, 'sum_of_divisors(28) eredménye hibás'
assert sum_of_divisors(36) == 91, 'sum_of_divisors(36) eredménye hibás'
assert sum_of_divisors(100) == 217, 'sum_of_divisors(100) eredménye hibás'
print("OK!")