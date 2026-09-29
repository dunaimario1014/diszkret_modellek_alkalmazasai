import math
import sympy
def my_solve_mod(a: int, b: int, m: int) -> list[int]:
    d = math.gcd(a, m)
    megoldasok = []
    if b % d == 0:
        m_red = m // d
        x, y, _ = sympy.gcdex(a, m)
        res = (x * (b // d)) % m
        megoldasok.append(res)
        for i in range(d - 1):
            res = (res + m_red) % m
            megoldasok.append(res)
    return megoldasok

if __name__ == "__main__":

  tests = [
    ((2472, 1769, 4386), []), ((4625, 3701, 6495), []), ((4340, 277, 5445), []), ((3410, 4964, 5000), []), ((6052, 2475, 8054), []),
    ((3037, 3657, 9763), [657]),
    ((8149, 4493, 9490), [6847]),
    ((4423, 4909, 5498), [3105]),
    ((5459, 5858, 9545), [5292]),
    ((5374, 388, 6528), [5566, 2302]),
    ((6824, 6308, 7436), [3975, 5834, 257, 2116]),
    ((175, 1540, 1792), [60, 316, 572, 828, 1084, 1340, 1596]),
  ]

  for test in tests:
    try:
      assert test[1] == my_solve_mod(*test[0])
    except NotImplementedError:
      print(f"ModSolve: not implemented")
      exit(1)
    except AssertionError as message:
      print(f"LinDiophantineEq: FAILED ({message})")
      exit(1)
  print(f"ModSolve: OK")
