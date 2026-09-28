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
        self.a = a
        self.b = b
        self.c = c
        self._solvable = False

        def extgcd(val_a, val_b):
            old_r, r = abs(val_a), abs(val_b)
            old_s, s = 1, 0
            old_t, t = 0, 1
            while r != 0:
                quotient = old_r // r
                old_r, r = r, old_r - quotient * r
                old_s, s = s, old_s - quotient * s
                old_t, t = t, old_t - quotient * t

            if val_a >= 0:
                x0 = old_s
            else:
                x0 = -old_s
            if val_b >= 0:
                y0 = old_t
            else:
                y0 = -old_t
            return x0, y0, old_r


        x0, y0, g = extgcd(a, b)

        if c % g != 0:
            return
            
        self._solvable = True
        
        factor = c // g
        x1 = x0 * factor
        y1 = y0 * factor

        if b == 0:
            self._dx = 0
            self._dy = 1
            self._x = x1
            self._y = 0 
        else:
            self._dx = b // g
            self._dy = -(a // g)
            
            self._x = x1 % abs(self._dx)
            k = (self._x - x1) // self._dx
            self._y = y1 + k * self._dy

    def is_solvable(self) -> bool:
        return self._solvable

    def next_solution(self) -> tuple[int, int]:
        if not self._solvable:
            raise ValueError("The equation has no integer solutions.")
        
        current_solution = (self._x, self._y)
        self._x += self._dx
        self._y += self._dy
        return current_solution

    def prev_solution(self) -> tuple[int, int]:
        if not self._solvable:
            raise ValueError("The equation has no integer solutions.")
            
        self._x -= self._dx
        self._y -= self._dy
        return (self._x, self._y)

# Do not modify or delete this part!
# From here there are no further exercises, this part is only for testing purposes.
def tester_diophantine(a,b,c,n):
    "Returns with the solutions around the first one with an n radius."
    E = LinDiophantineEq(a, b, c)
    if not E.is_solvable():
        return None
    for i in range(n):
        E.prev_solution()
    solutions = []
    for i in range(2 * n + 1):
        solutions.append(E.next_solution())
    return solutions


if __name__ == '__main__':
    import math

    tests = [
        ((12, 11, -40, 3), [(-29, 28), (-18, 16), (-7, 4), (4, -8), (15, -20), (26, -32), (37, -44)]),
        ((30, 7, 32, 3), [(-19, 86), (-12, 56), (-5, 26), (2, -4), (9, -34), (16, -64), (23, -94)]),
        ((28, -7, 148, 3), None)
    ]

    for test in tests:
        try:
            assert test[1] == tester_diophantine(*test[0])
            print(f"LinDiophantineEq: OK")
        except NotImplementedError:
            print(f"LinDiophantineEq: not implemented")
        except AssertionError as message:
            print(f"LinDiophantineEq: FAILED ({message})")

