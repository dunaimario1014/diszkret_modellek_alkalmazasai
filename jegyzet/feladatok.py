# ==============================================================================
# DISZKRÉT MODELLEK ALKALMAZÁSAI - KOMPLETT PYTHON PUSKA (CHEAT SHEET)
# ==============================================================================
#
# TARTALOMJEGYZÉK:
#   0. GYORSTÜZELŐ PUSKA: Praktikus trükkök, len() szabályok, SymPy csapdák
#   1. OSZTHATÓSÁG: Osztók, Sigma-függvények, Aliquot-sorozat, Tökéletes számok
#   2. PRÍMEK ÉS Z_m: Egységek, Irreducibilisek, Prímek, Kanonikus alak, Sziták
#   3. LNKO ÉS EUKLIDESZI ALGORITMUSOK: Prímfaktoros, Bővített, Bináris (Stein)
#   4. DIOFANTIKUS EGYENLETEK: LinDiophantineEq, Nemnegatív megoldások, Multi
#   5. MARADÉKRENDSZEREK ÉS KONGRUENCIÁK: Inverz, Kongruenciák, Kínai maradéktétel (CRT)
#   6. DISZKRÉT LOGARITMUS: Gyorshatványozás, Rend, Generátorok, BSGS, Rabok
#   7. EULER-FERMAT ÉS PRÍMTESZTEK: Euler-phi, Carmichael, Fermat, Miller-Rabin
#   8. DIFFIE-HELLMAN ÉS ELGAMAL: Kulcscsere, ElGamal törés, Étkező kriptográfusok, Milliomosok
#   9. RSA: Validálás, Titkosítás/Aláírás, Faktorizációs törés, CRT gyorsítás
#
# ==============================================================================
# 0. GYORSTÜZELŐ PUSKA: PRAKTIKUS ÖSSZEFÜGGÉSEK ÉS TRÜKKÖK
# ==============================================================================
#
# --- [A] MIT JELENT A len() KÜLÖNBÖZŐ FÜGGVÉNYEK EREDMÉNYÉRE HÍVVA? ---
# 1. len(my_solve_mod(a, b, m)):
#    Az a*x ≡ b (mod m) lineáris kongruencia megoldásainak száma Z_m-ben.
#    - Képlettel (számolás nélkül): d = math.gcd(a, m).
#      Ha b % d == 0, akkor pontosan `d` darab megoldás van, különben 0!
#
# 2. len(powers_mod(a, m)):
#    Ha gcd(a, m) == 1, akkor ez pontosan az `a` elem MULTIPLIKATÍV RENDJE
#    modulo m, azaz ord_m(a) = sympy.n_order(a, m).
#    - Ha p prím és len(powers_mod(a, p)) == p - 1, akkor `a` GENERÁTOR (primitív gyök)!
#
# 3. len([a for a in range(m) if is_unit_mod_n(a, m)]):
#    A Z_m gyűrű egységeinek (invertálható elemeinek) száma, ami pontosan
#    az Euler-féle φ(m) függvény: sympy.totient(m).
#
# 4. len(generators(p)) (prím p esetén):
#    Modulo p pontosan φ(p - 1) = sympy.totient(p - 1) darab generátor létezik!
#
# 5. len(quadratic_residues(p)) (páratlan prím p esetén):
#    Modulo p pontosan (p + 1) // 2 darab kvadratikus maradék van (a 0-val együtt),
#    és (p - 1) // 2 darab nemnulla kvadratikus maradék.
#
# 6. len(canonical_form(n)) vagy len(sympy.factorint(n)):
#    Az `n` szám KÜLÖNBÖZŐ prímtényezőinek a száma (ω(n) függvény).
#
# --- [B] GCD (LNKO) ALAPÚ GYORS DÖNTÉSEK (CIKLUS NÉLKÜL!) ---
# - a | b (mod m) [divides_mod_n(a, b, m)]  <==>  b % math.gcd(a, m) == 0
# - a és b asszociáltak mod m               <==>  math.gcd(a, m) == math.gcd(b, m)
# - a egység mod m [is_unit_mod_n(a, m)]    <==>  math.gcd(a, m) == 1
# - a nullosztó mod m (a % m != 0)          <==>  1 < math.gcd(a, m) < m
# - a*x + b*y = c diofantikus megoldható    <==>  c % math.gcd(a, b) == 0
# - a*x ≡ b (mod m) kongruencia megoldható  <==>  b % math.gcd(a, m) == 0
#
# --- [C] BEÉPÍTETT PYTHON ÉS SYMPY FÜGGVÉNYEK (FIGYELJ A PARAMÉTEREKRE!) ---
# - Moduláris hatványozás: pow(alap, kitevo, mod) -> O(log(kitevo)) gyors!
# - Moduláris inverz:      pow(a, -1, m)          -> ValueError-t dob, ha gcd(a, m) != 1
# - Bővített Euklideszi:   x, y, g = sympy.gcdex(a, b) -> VIGYÁZAT: (x, y, gcd) a sorrend!
# - Prímfelbontás:         sympy.factorint(360)   -> {2: 3, 3: 2, 5: 1} dict-et ad!
# - Kínai maradéktétel:    sympy.ntheory.modular.crt(m_lista, c_lista)[0]
#                          -> VIGYÁZAT: a SymPy-nál a MODULUSOK listája van elöl!
# - Diszkrét logaritmus:   sympy.discrete_log(p, b, a) az a^x ≡ b (mod p)-hez
#                          -> VIGYÁZAT: (modulus, eredmény, alap) a paramétersorrend!
# ==============================================================================

import math
import random
import hashlib
from time import perf_counter
from math import isqrt, gcd
import sympy
from sympy import isprime, totient, factorint, n_order, discrete_log, primitive_root, randprime
from sympy.ntheory.modular import crt


# ==============================================================================
# 1. OSZTHATÓSÁG, OSZTÓK ÖSSZEGE ÉS TÖKÉLETES SZÁMOK
# ==============================================================================

# 3 különböző módszer annak eldöntésére, hogy a | b (természetes számokon):
def divides0(a: int, b: int) -> bool:
    return b % a == 0 if a != 0 else b == 0

def divides1(a: int, b: int) -> bool:
    return (b // a) * a == b if a != 0 else b == 0

def divides2(a: int, b: int) -> bool:
    return divmod(b, a)[1] == 0 if a != 0 else b == 0


# Oszthatóság vizsgálata: ∀n ∈ N: a | (n^3 - n)
# MATEMATIKAI HÁTTÉR: n^3 - n = (n - 1) * n * (n + 1), ami 3 egymást követő egész
# szorzata, így mindig osztható 2-vel és 3-mal, tehát a legnagyobb ilyen szám a 6.
def divides_all(a: int, limit: int) -> bool:
    return all((n**3 - n) % a == 0 for n in range(1, limit + 1))

def find_largest(max_a: int, limit: int) -> int:
    for a in range(max_a, 0, -1):
        if divides_all(a, limit):
            return a
    return 1


# Osztók száma τ(a) és osztók összege σ(a)
# SYMPY TRÜKK: sympy.divisor_count(a) és sum(sympy.divisors(a))
def num_of_divisors(a: int) -> int:
    # Gyökig érdemes menni: minden d < sqrt(a) osztóhoz tartozik egy a // d pár
    count = 0
    for d in range(1, isqrt(a) + 1):
        if a % d == 0:
            count += 1 if d * d == a else 2
    return count

def sum_of_divisors(a: int) -> int:
    total = 0
    for d in range(1, isqrt(a) + 1):
        if a % d == 0:
            total += d if d * d == a else (d + a // d)
    return total


# Hányados-sorozat (Aliquot-sorozat): s_0 = k, s_{i+1} = σ(s_i) - s_i
# Terminál 0-val, vagy megáll az első periódus záróeleménél (pl. [25, 6, 6]).
def divisor_sum_iteration(k: int) -> list[int]:
    seq = [k]
    while seq[-1] != 0:
        nxt = sum_of_divisors(seq[-1]) - seq[-1]
        if nxt in seq:
            seq.append(nxt)
            break
        seq.append(nxt)
    return seq


# Tökéletes számok: σ(n) - n == n (azaz σ(n) == 2*n, pl. 6, 28, 496, 8128)
def perfect_numbers(s: set[int]) -> set[int]:
    return {x for x in s if x > 0 and sum_of_divisors(x) - x == x}


# ==============================================================================
# 2. PRÍMEK, SZÁMELMÉLET ALAPTÉTELE ÉS A Z_m GYŰRŰ
# ==============================================================================

# --- [HÁZI FELADAT 1]: Oszthatóság, egységek, irreducibilisek és prímek Z_n-ben ---
def divides_mod_n(a: int, b: int, m: int) -> bool:
    # Definíció szerint: ∃c ∈ Z_m: a*c ≡ b (mod m)
    # GYORS ALTERNATÍVA: return b % math.gcd(a, m) == 0
    for c in range(m):
        if (a * c) % m == b % m:
            return True
    return False

def is_associated_mod_n(a: int, b: int, n: int) -> bool:
    # Definíció szerint: a | b és b | a (mod n)
    # GYORS ALTERNATÍVA: return math.gcd(a, n) == math.gcd(b, n)
    return divides_mod_n(a, b, n) and divides_mod_n(b, a, n)

def is_unit_mod_n(a: int, n: int) -> bool:
    # Definíció szerint: a | 1 (mod n)
    # GYORS ALTERNATÍVA: return math.gcd(a, n) == 1
    return divides_mod_n(a, 1, n)

def is_irreducible_mod_n(a: int, n: int) -> bool:
    # Nem 0, nem egység, és ha a ≡ b*c (mod n), akkor b vagy c egység.
    if a % n == 0 or is_unit_mod_n(a, n):
        return False
    for b in range(n):
        for c in range(n):
            if (b * c) % n == a % n:
                if not is_unit_mod_n(b, n) and not is_unit_mod_n(c, n):
                    return False
    return True

def is_prime_mod_n(p: int, n: int) -> bool:
    # Nem 0, nem egység, és ha p | a*b (mod n), akkor p | a vagy p | b (mod n).
    if p <= 0 or p % n == 0 or is_unit_mod_n(p, n):
        return False
    for a in range(n):
        for b in range(n):
            if divides_mod_n(p, a * b, n):
                if not divides_mod_n(p, a, n) and not divides_mod_n(p, b, n):
                    return False
    return True

# Jegyzetbeli aliasok és kigyűjtő függvények:
is_unit_mod_m = is_unit_mod_n
divides_mod_m = divides_mod_n
is_irreducible_mod_m = is_irreducible_mod_n
is_prime_mod_m = is_prime_mod_n

def irreducibles_of(m: int) -> list[int]:
    return [a for a in range(m) if is_irreducible_mod_m(a, m)]

def primes_of(m: int) -> list[int]:
    return [a for a in range(m) if is_prime_mod_m(a, m)]

# ELMÉLETI VÁLASZOK A JEGYZET KÉRDÉSEIRE:
# 1. Miért üres irreducibles_of(7) és primes_of(7)?
#    Mert m=7 prím, így Z_7 test: a 0-n kívül MINDEN elem (1..6) egység!
#    A definíció pedig kiköti, hogy sem a 0, sem az egységek nem lehetnek prímek/irreducibilisek.
# 2. Miért prím a 2 Z_6-ban, de nem irreducibilis?
#    Mert Z_6-ban vannak nullosztók (nem Gauss-gyűrű): 2 ≡ 2 * 4 (mod 6), ahol sem a 2,
#    sem a 4 nem egység, ezért a 2 felbontható (nem irreducibilis), viszont a prím
#    tulajdonságot (2 | a*b => 2 | a vagy 2 | b) teljesíti.


# Kanonikus alak: n = p1^a1 * ... * pm^am -> [(p1, a1), ...]
# SYMPY TRÜKK: sorted(sympy.factorint(n).items())
def canonical_form(n: int) -> list[tuple[int, int]]:
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            count = 0
            while n % d == 0:
                n //= d
                count += 1
            factors.append((d, count))
        d += 1
    if n > 1:
        factors.append((n, 1))
    return factors


# Osztók száma kanonikus alakból: τ(n) = (a1 + 1) * (a2 + 1) * ... * (am + 1)
# BÓNUSZ KÉPLET: Osztók összege kanonikus alakból: σ(n) = ∏ (p_i^(a_i + 1) - 1) // (p_i - 1)
def num_of_divisors_from_factors(n: int) -> int:
    res = 1
    for _, alpha in canonical_form(n):
        res *= (alpha + 1)
    return res


# Eratoszthenész szitája (n-nél szigorúan kisebb prímek)
# SYMPY TRÜKK: list(sympy.primerange(2, n))
def primes_up_to_n(n: int) -> list[int]:
    if n <= 2:
        return []
    sieve = [True] * n
    sieve[0] = sieve[1] = False
    for p in range(2, isqrt(n - 1) + 1):
        if sieve[p]:
            sieve[p * p : n : p] = [False] * len(range(p * p, n, p))
    return [i for i, is_p in enumerate(sieve) if is_p]


# Ikerprímek [a, b] zárt intervallumban: (p, p + 2), ahol a <= p és p + 2 <= b
def list_twin_primes(a: int, b: int) -> list[tuple[int, int]]:
    primes_set = set(primes_up_to_n(b + 1))
    return [(p, p + 2) for p in range(max(2, a), b - 1) if p in primes_set and (p + 2) in primes_set]


# Optimalizált szita 1: Páros számok nélkül (csak a páratlanokat tároljuk: index i -> szám 2*i + 3)
def primes_up_to_n_without_even(n: int) -> list[int]:
    if n <= 2:
        return []
    size = (n - 3) // 2 + 1  # 3, 5, 7, ..., n-1 darabszáma
    sieve = [True] * size
    for i in range(isqrt(n - 1) // 2):
        if sieve[i]:
            p = 2 * i + 3
            start = (p * p - 3) // 2
            sieve[start::p] = [False] * len(range(start, size, p))
    return [2] + [2 * i + 3 for i in range(size) if sieve[i]]


# Optimalizált szita 2: 2, 3, 5 többszörösei nélkül (30*i + M[j] kerékszita)
def primes_up_to_n_without_2_3_5(n: int) -> list[int]:
    if n <= 2:
        return []
    small = [p for p in (2, 3, 5) if p < n]
    if n <= 7:
        return small
    M = [1, 7, 11, 13, 17, 19, 23, 29]
    m_idx = {r: idx for idx, r in enumerate(M)}
    candidates = [30 * i + r for i in range(n // 30 + 1) for r in M if 1 < 30 * i + r < n]
    pos = {val: idx for idx, val in enumerate(candidates)}
    sieve = [True] * len(candidates)

    for idx, p in enumerate(candidates):
        if p * p >= n:
            break
        if sieve[idx]:
            for mult in range(p * p, n, 2 * p):
                if (mult % 30) in m_idx and mult in pos:
                    sieve[pos[mult]] = False
    return small + [candidates[i] for i in range(len(candidates)) if sieve[i]]


# ==============================================================================
# 3. LEGNAGYOBB KÖZÖS OSZTÓ (LNKO), LKKT ÉS EUKLIDESZI ALGORITMUSOK
# ==============================================================================

# LNKO prímtényezős felbontással (minden közös prímből a MINIMÁLIS kitevő)
def greatest_common_divisor(a: int, b: int) -> int:
    fa, fb = factorint(a), factorint(b)
    res = 1
    for p in set(fa.keys()) & set(fb.keys()):
        res *= p ** min(fa[p], fb[p])
    return res


# LKKT prímtényezős felbontással (minden prímből a MAXIMÁLIS kitevő)
# GYORS KÉPLET: (a * b) // math.gcd(a, b)  vagy  math.lcm(a, b)
def least_common_multiple(a: int, b: int) -> int:
    fa, fb = factorint(a), factorint(b)
    res = 1
    for p in set(fa.keys()) | set(fb.keys()):
        res *= p ** max(fa.get(p, 0), fb.get(p, 0))
    return res


# Klasszikus Euklideszi-algoritmus
def gcd_w_eukl(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return abs(a)


# Bővített Euklideszi-algoritmus: visszaadja (x, y, r)-t, ahol a*x + b*y == r == gcd(a, b)
# SYMPY TRÜKK: x, y, r = map(int, sympy.gcdex(a, b))
def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    r0, r1 = a, b
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return x0, y0, r0


# Bináris GCD (Stein-algoritmus): csak összeadás/kivonás és bitshift (<<, >>)
def binary_gcd(a: int, b: int) -> int:
    if a == 0: return b
    if b == 0: return a
    shift = 0
    while ((a | b) & 1) == 0:
        a >>= 1
        b >>= 1
        shift += 1
    while (a & 1) == 0:
        a >>= 1
    while b != 0:
        while (b & 1) == 0:
            b >>= 1
        if a > b:
            a, b = b, a
        b = b - a
    return a << shift


# Bővített Bináris GCD (Binary xGCD) a jegyzet 8 lépéses algoritmusa alapján
def binary_xgcd(a: int, b: int) -> tuple[int, int, int]:
    d = 0
    while (a & 1) == 0 and (b & 1) == 0:
        a >>= 1
        b >>= 1
        d += 1
    if (b & 1) == 0:
        a, b, s = b, a, 1
    else:
        s = 0
    ra, rb, x, y, u, v = a, b, 1, 0, 0, 1
    while True:
        while (ra & 1) == 0:
            ra >>= 1
            if (x & 1) == 0:
                x >>= 1
                y >>= 1
            else:
                x = (x - b) >> 1
                y = (y + a) >> 1
        if ra == rb:
            return (x, y, ra << d) if s == 0 else (y, x, ra << d)
        if ra > rb:
            ra, x, y = ra - rb, x - u, y - v
        else:
            ra, x, y, rb, u, v = rb - ra, u - x, v - y, ra, x, y


# ==============================================================================
# 4. LINEÁRIS DIOFANTIKUS EGYENLETEK (a*x + b*y = c)
# ==============================================================================

# Egész megoldások száma Z felett: vagy 0, vagy végtelen (math.inf)
def num_of_solutions(a: int, b: int, c: int):
    if a == 0 and b == 0:
        return math.inf if c == 0 else 0
    return math.inf if c % math.gcd(a, b) == 0 else 0


# --- [HÁZI FELADAT 2]: LinDiophantineEq osztály ---
class LinDiophantineEq:
    """
    Az a * x + b * y == c diofantikus egyenlet megoldásait reprezentáló osztály.
    - Általános megoldásképlet:
      x_t = x0 + t * (b // g)
      y_t = y0 - t * (a // g), ahol g = gcd(a, b) és t ∈ Z.
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
            x0 = old_s if val_a >= 0 else -old_s
            y0 = old_t if val_b >= 0 else -old_t
            return x0, y0, old_r

        x0, y0, g = extgcd(a, b)
        if g == 0 or c % g != 0:
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
            # Legkisebb nemnegatív x beállítása modulo |dx| segítségével:
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


# Nemnegatív egész megoldások száma (x >= 0, y >= 0)
# PRAKTIKUS TRÜKK: Ha a > 0 és b > 0, akkor a legkisebb nemnegatív x0-hoz tartozó
# y0 a lehető legnagyobb y érték. Mivel x lépésenként nő, y pedig |dy|-nal csökken,
# a nemnegatív megoldások száma O(1) időben: (y0 // abs(dy)) + 1 (ha y0 >= 0, különben 0)!
def num_of_nat_solutions(a: int, b: int, c: int):
    E = LinDiophantineEq(a, b, c)
    if not E.is_solvable():
        return 0
    if a * b < 0:
        # Ellentétes előjelű együtthatóknál x és y egyszerre nő az egyik irányba -> végtelen megoldás
        return math.inf
    if a < 0 and b < 0:
        return num_of_nat_solutions(-a, -b, -c) if c <= 0 else 0
    x0, y0 = E.next_solution()
    if y0 < 0:
        return 0
    dy_step = abs(a // math.gcd(a, b))
    return (y0 // dy_step) + 1


# 100000 pengő kifizetése 47 és 79 pengős érmékkel: 47*x + 79*y = 100000
def num_of_payments() -> int:
    return num_of_nat_solutions(47, 79, 100000)


# Csokoládé feladat: 70*x + 130*y + 150*z = 5000 és x + y + z = 50 (x, y, z >= 0)
# Behelyettesítve z = 50 - x - y >= 0:
# 70x + 130y + 150(50 - x - y) = 5000  ==>  80x + 20y = 2500 (és x + y <= 50)
def num_of_purchases() -> int:
    E = LinDiophantineEq(80, 20, 2500)
    count = 0
    while True:
        x, y = E.next_solution()
        if y < 0:
            break
        if x + y <= 50:  # ami biztosítja, hogy z = 50 - x - y >= 0
            count += 1
    return count


# Többváltozós diofantikus egyenlet: sum(L[i] * x_i) == c, ahol x_i >= 0 és sum(x_i) >= s
def multi(L: list[int], c: int, s: int = 0) -> int:
    if c < 0:
        return 0
    if len(L) == 1:
        return 1 if (c % L[0] == 0 and c // L[0] >= s) else 0
    if len(L) == 2:
        if s <= 0:
            return num_of_nat_solutions(L[0], L[1], c)
        E = LinDiophantineEq(L[0], L[1], c)
        if not E.is_solvable():
            return 0
        count = 0
        while True:
            x, y = E.next_solution()
            if y < 0:
                break
            if x + y >= s:
                count += 1
        return count
    # Rekurzív visszavezetés kevesebb változóra:
    total = 0
    for x0 in range(c // L[0] + 1):
        total += multi(L[1:], c - L[0] * x0, max(0, s - x0))
    return total


# ==============================================================================
# 5. MARADÉKRENDSZEREK, INVERZ, KONGRUENCIÁK ÉS KÍNAI MARADÉKTÉTEL (CRT)
# ==============================================================================

# Maradékosztály reprezentánsa (0..m-1 között)
def find_class_representative(x: int, m: int) -> int:
    return x % m


# Lista elemeinek osztályozása modulo m
def classify_elements(input_set: list[int], m: int) -> dict[int, list[int]]:
    result = {}
    for x in input_set:
        rep = x % m
        result.setdefault(rep, []).append(x)
    return result


# Moduláris inverz: a * x ≡ 1 (mod m)
# PYTHON TRÜKK: pow(a, -1, m) (Python 3.8+ beépített, ValueError-t dob ha nincs inverz)
def invmod(a: int, m: int) -> int | None:
    x, _, g = extended_gcd(a, m)
    return x % m if g == 1 else None


# --- [HÁZI FELADAT 3]: Lineáris kongruencia megoldása: a * x ≡ b (mod m) ---
# FONTOS TULAJDONSÁG:
# - Megoldható <==> b % gcd(a, m) == 0
# - Megoldások száma Z_m-ben: len(my_solve_mod(a, b, m)) == gcd(a, m) (ha megoldható, különben 0)
def my_solve_mod(a: int, b: int, m: int) -> list[int]:
    d = math.gcd(a, m)
    megoldasok = []
    if b % d == 0:
        m_red = m // d
        x, _, _ = sympy.gcdex(a, m)
        res = int(x * (b // d)) % m
        # Vagy: res = ((b // d) * invmod(a // d, m_red)) % m_red, ami a legkisebb megoldást adja
        megoldasok.append(res)
        for _ in range(d - 1):
            res = (res + m_red) % m
            megoldasok.append(res)
    return megoldasok


# Kínai maradéktétel (CRT): x ≡ c[i] (mod m[i]), ahol m[i] páronként relatív prímek
# SYMPY TRÜKK: int(sympy.ntheory.modular.crt(m, c)[0]) -> m van elöl!
def my_crt(c: list[int], m: list[int]) -> int:
    M = math.prod(m)
    x = 0
    for ci, mi in zip(c, m):
        Mi = M // mi
        yi = invmod(Mi, mi)  # Mi * yi ≡ 1 (mod mi)
        x = (x + ci * Mi * yi) % M
    return x


# Általános lineáris kongruenciarendszer megoldása: a[i] * x ≡ b[i] (mod m[i])
# (A modulusoknak NEM kell relatív prímeknek lenniük!)
def solve_system(a: list[int], b: list[int], m: list[int]) -> set[int]:
    # Kezdjük az x ≡ 0 (mod 1) triviális állapottal, és lépésenként szűkítjük a jelölteket
    current_solutions = {0}
    current_mod = 1
    for ai, bi, mi in zip(a, b, m):
        new_mod = math.lcm(current_mod, mi)
        next_solutions = set()
        for x0 in current_solutions:
            # x0 + k * current_mod alakú számokat keresünk a [0, new_mod) tartományban
            for x in range(x0, new_mod, current_mod):
                if (ai * x - bi) % mi == 0:
                    next_solutions.add(x)
        current_solutions = next_solutions
        current_mod = new_mod
        if not current_solutions:
            return set()
    return current_solutions


# Kvadratikus maradékok modulo m: azon b ∈ {0..m-1} számok, melyekre x^2 ≡ b (mod m) megoldható
def quadratic_residues(m: int) -> set[int]:
    return {(x * x) % m for x in range(m)}


def moduli(a, b):
    diff = abs(a - b)
    # Ha m >= 1 kell, akkor range(1, diff + 1)
    return [m for m in range(2, diff + 1) if diff % m == 0]


# Gyors O(sqrt(n)) megoldás (ha nagy számokkal is tesztelik):
def moduli_fast(a, b):
    diff = abs(a - b)
    moduli = set()
    for d in range(1, math.isqrt(diff) + 1):
        if diff % d == 0:
            if d > 1:
                moduli.add(d)
            if diff // d > 1:
                moduli.add(diff // d)
    return sorted(moduli)

def moduli(nums):
    # Kiszámoljuk az első elemtől vett különbségek legnagyobb közös osztóját
    g = 0
    for x in nums[1:]:
        g = math.gcd(g, abs(x - nums[0]))
    
    # g összes 1-nél nagyobb osztója
    return [m for m in range(2, g + 1) if g % m == 0]


def moduli(m):
    moduli = []
    d = 2
    temp = m
    while d * d <= temp:
        if temp % d == 0:
            pk = 1
            while temp % d == 0:
                pk *= d
                temp //= d
            moduli.append(pk)
        d += 1
    if temp > 1:
        moduli.append(temp)
    return sorted(moduli)

def moduli(a, b, max_m):
    # 1. eset: Ha a feladat azt kéri, hogy MEGOLDHATÓ legyen ax ≡ b (mod m):
    return [m for m in range(2, max_m + 1) if b % math.gcd(a, m) == 0]

    # 2. eset: Ha azt kéri, hogy EGYÉRTELMŰ megoldása legyen ax ≡ b (mod m):
    # return [m for m in range(2, max_m + 1) if math.gcd(a, m) == 1]

    # 3. eset: Ha adott a megoldások száma is (pl. d darab megoldás):
    # return [m for m in range(2, max_m + 1) if math.gcd(a, m) == d and b % d == 0]

def congruence_moduli(a, k, b):
    diff = abs(a**k - b)
    return [m for m in range(2, diff + 1) if diff % m == 0]


# ==============================================================================
# 6. DISZKRÉT LOGARITMUS, GYORSHATVÁNYOZÁS, REND ÉS GENERÁTOROK
# ==============================================================================

# Gyorshatványozás (Square-and-Multiply algoritmus): O(log k) szorzás
def fastpow(a: int, k: int) -> int:
    if k == 0:
        return 1
    res = 1
    base = a
    while k > 0:
        if k & 1:
            res *= base
        base *= base
        k >>= 1
    return res


# Egy elem pozitív kitevőjű hatványainak halmaza modulo m
# TRÜKK: Ha gcd(a, m) == 1, akkor len(powers_mod(a, m)) == ord_m(a) = sympy.n_order(a, m)!
def powers_mod(a: int, m: int) -> set[int]:
    visited = set()
    cur = a % m
    while cur not in visited:
        visited.add(cur)
        cur = (cur * a) % m
    return visited


# Generátorok (primitív gyökök) keresése modulo p (p prím)
# MAT. TRÜKK: `a` pontosan akkor generátor mod p, ha p-1 minden q prímosztójára:
# pow(a, (p - 1) // q, p) != 1. Így nem kell végigszámolni az összes hatványt!
def generators(p: int) -> set[int]:
    if p == 2:
        return {1}
    prime_factors = factorint(p - 1).keys()
    return {
        a for a in range(1, p)
        if all(pow(a, (p - 1) // q, p) != 1 for q in prime_factors)
    }


# Diszkrét logaritmus keresése Brute-Force módszerrel: a^x ≡ b (mod p)
# SYMPY TRÜKK: sympy.discrete_log(p, b, a) -> figyelj a (p, b, a) sorrendre!
def discrete_log_brute(a: int, b: int, p: int) -> int | None:
    if b == 0:
        return None
    cur = 1
    for x in range(p - 1):
        if cur == b:
            return x
        cur = (cur * a) % p
    return None


# Rabok feladványa (cikluskövető stratégia):
# Minden rab kiszabadul <==> a permutációban minden ciklus hossza <= m.
def prisoners_escape(keys: list[int], m: int) -> bool:
    n = len(keys)
    for prisoner in range(1, n + 1):
        curr_box = prisoner
        for _ in range(m):
            found_key = keys[curr_box - 1]
            if found_key == prisoner:
                break
            curr_box = found_key
        else:
            return False  # Nem találta meg m lépésből
    return True


# Baby-step, Giant-step (BSGS) algoritmus: a^x ≡ b (mod p) megoldása O(sqrt(p)) időben
# x = i*q + j, ahol q = ceil(sqrt(p - 1)), és a^j ≡ b * (a^(-q))^i (mod p)
def baby_step_giant_step(a: int, b: int, p: int) -> int | None:
    if b == 1:
        return 0
    if b == 0:
        return None
    q = isqrt(p - 1) + (1 if isqrt(p - 1)**2 < p - 1 else 0)
    if q == 0:
        return 0 if b == 1 else None

    # 1. Baby-step: a^j mod p eltárolása (0 <= j < q)
    baby_table = {}
    cur = 1
    for j in range(q):
        if cur not in baby_table:
            baby_table[cur] = j
        cur = (cur * a) % p

    # 2. Giant-step: b * (a^(-q))^i mod p keresése a táblában (0 <= i < q)
    a_inv_q = pow(a, -q, p)
    giant = b % p
    for i in range(q):
        if giant in baby_table:
            return i * q + baby_table[giant]
        giant = (giant * a_inv_q) % p
    return None


# ==============================================================================
# 7. EULER-FERMAT-TÉTEL ÉS VALÓSZÍNŰSÉGI PRÍMTESZTEK
# ==============================================================================

# Euler-féle φ (totient) függvény: φ(m) = m * ∏_{p|m} (1 - 1/p)
# SYMPY TRÜKK: int(sympy.totient(m))
def my_phi(m: int) -> int:
    res = m
    for p in factorint(m):
        res = (res // p) * (p - 1)
    return res


# Inverz Euler-phi: legkisebb m, amelyre φ(m) == n (vagy None, ha nincs ilyen)
def inverse_phi(n: int) -> int | None:
    if n == 1:
        return 1
    if n % 2 == 1:
        return None  # m > 2 esetén φ(m) mindig páros!
    # Biztonságos felső korlát: m <= 4 * n (kis számokra bőségesen elég)
    for m in range(2, 6 * n + 2):
        if my_phi(m) == n:
            return m
    return None


# Carmichael-számok keresése (összetett c > 1, amelyre ∀(a,c)=1 esetén a^(c-1) ≡ 1 (mod c))
# KORSELT-KRITÉRIUM (Sokkal gyorsabb!): c összetett, négyzetmentes, és minden p | c
# prímosztóra (p - 1) | (c - 1). Pl. 561 = 3 * 11 * 17, 1105, 1729.
def is_carmichael(c: int) -> bool:
    if c < 2 or isprime(c):
        return False
    factors = factorint(c)
    # Négyzetmentes (minden kitevő 1) és (p - 1) osztja (c - 1)-et:
    return all(exp == 1 and (c - 1) % (p - 1) == 0 for p, exp in factors.items())

def find_carmichael(A: set[int]) -> set[int]:
    return {c for c in A if is_carmichael(c)}


# Legkisebb 1 < a < m alap, amelyre a^(m-1) != 1 (mod m)
def first_base(m: int) -> int | None:
    for a in range(2, m):
        if pow(a, m - 1, m) != 1:
            return a
    return None


# Fermat prímteszt és próbaosztásos (trial division) prímteszt
def fermat_test(m: int, bases: list[int]) -> bool:
    if m < 2:
        return False
    if m in (2, 3):
        return True
    for a in bases:
        if 2 <= a <= m - 2:
            if gcd(a, m) != 1 or pow(a, m - 1, m) != 1:
                return False
    return True

def trial_division(m: int) -> bool:
    if m < 2:
        return False
    if m in (2, 3):
        return True
    if m % 2 == 0:
        return False
    for d in range(3, isqrt(m) + 1, 2):
        if m % d == 0:
            return False
    return True


# Miller-Rabin valószínűségi prímteszt: m - 1 = 2^k * d (d páratlan)
def miller_rabin(m: int, bases: list[int]) -> bool:
    if m < 2:
        return False
    if m in (2, 3):
        return True
    if m % 2 == 0:
        return False

    # m - 1 = 2^k * d felbontása
    d = m - 1
    k = 0
    while (d & 1) == 0:
        d >>= 1
        k += 1

    for a in bases:
        if 2 <= a <= m - 2:
            if gcd(a, m) != 1:
                return False
            x = pow(a, d, m)
            if x == 1 or x == m - 1:
                continue
            for _ in range(k - 1):
                x = (x * x) % m
                if x == m - 1:
                    break
                if x == 1:
                    return False
            else:
                return False
    return True


# ==============================================================================
# 8. DIFFIE-HELLMAN, ELGAMAL ÉS KRIPTOGRÁFIAI PROTOKOLLOK
# ==============================================================================

# Diffie-Hellman kulcscsere résztvevő
class DH_participant:
    def __init__(self, p: int, g: int):
        self.p = p
        self.g = g
        self.x = random.randint(2, p - 2)
        self.pub = pow(g, self.x, p)

    def get_pub(self) -> int:
        return self.pub

    def calculate_common_key(self, pub_of_other: int) -> int:
        return pow(pub_of_other, self.x, self.p)


# ElGamal aszimmetrikus titkosítás
def elgamal_keygen(p: int, g: int) -> tuple[tuple[int, int, int], int]:
    x = random.randint(2, p - 2)
    h = pow(g, x, p)
    return (p, g, h), x

def elgamal_encrypt(pubkey: tuple[int, int, int], m: int) -> tuple[int, int]:
    p, g, h = pubkey
    x_B = random.randint(2, p - 2)
    c1 = pow(g, x_B, p)
    s = pow(h, x_B, p)
    c2 = (m * s) % p
    return c1, c2

def elgamal_decrypt(pubkey: tuple[int, int, int], x: int, cipher: tuple[int, int]) -> int:
    p, _, _ = pubkey
    c1, c2 = cipher
    s = pow(c1, x, p)
    s_inv = pow(s, -1, p)  # Vagy Fermat-tétellel: pow(c1, p - 1 - x, p)
    return (c2 * s_inv) % p


# ElGamal feltörése diszkrét logaritmussal (h = g^x mod p -> x = discrete_log(p, h, g))
def elgamal_break(pubkey: tuple[int, int, int], cipher: tuple[int, int]) -> int:
    p, g, h = pubkey
    x = int(discrete_log(p, h, g))
    return elgamal_decrypt(pubkey, x, cipher)


# Étkező kriptográfusok (Dining Cryptographers)
def dining_cryptographers(secrets: list[int], p: int, g: int) -> int:
    n = len(secrets)
    participants = [DH_participant(p, g) for _ in range(n)]
    # Publikus s_i értékek kiszámítása
    published_s = []
    for i in range(n):
        si = secrets[i]
        for j in range(n):
            if i != j:
                k_ij = participants[i].calculate_common_key(participants[j].get_pub())
                sgn = 1 if i > j else -1
                si = (si + sgn * k_ij) % p
        published_s.append(si)
    # A maszkok kiejtik egymást, így az összeg pontosan a titkok összege mod p:
    return sum(published_s) % p


# Szociális milliomos probléma (Socialist Millionaire Problem: w_A == w_B tesztelése)
def socialist_millionaires(w_A: int, w_B: int, p: int, g: int) -> bool:
    while True:
        x_A, y_A, r_A = [random.randint(2, p - 2) for _ in range(3)]
        x_B, y_B, r_B = [random.randint(2, p - 2) for _ in range(3)]
        s_x = pow(g, x_A * x_B, p)
        s_y = pow(g, y_A * y_B, p)
        P_A = pow(s_y, r_A, p)
        Q_A = (pow(g, r_A, p) * pow(s_x, w_A, p)) % p
        P_B = pow(s_y, r_B, p)
        Q_B = (pow(g, r_B, p) * pow(s_x, w_B, p)) % p
        if P_A != P_B and Q_A != Q_B:
            break
    q_ratio = (Q_A * pow(Q_B, -1, p)) % p
    c = pow(q_ratio, y_A * y_B, p)
    p_ratio = (P_A * pow(P_B, -1, p)) % p
    return c == p_ratio


# ==============================================================================
# 9. RSA TITKOSÍTÁS, HITELESÍTÉS, FELTÖRÉS ÉS CRT GYORSÍTÁS
# ==============================================================================

# --- [HÁZI FELADAT 4]: RSA paraméterek validálása ---
def are_valid_rsa_parameters(p: int, q: int, d: int, e: int) -> bool:
    phi = (p - 1) * (q - 1)
    return (
        bool(isprime(p))
        and bool(isprime(q))
        and p != q
        and 2 < e < phi
        and gcd(e, phi) == 1
        and (e * d) % phi == 1
    )


# RSA osztály titkosításhoz és digitális aláíráshoz
def digest(n: int, message: bytes) -> int:
    return int.from_bytes(hashlib.sha256(message).digest(), 'big') % n

class RSA:
    def __init__(self, p: int, q: int, e: int):
        self.p = p
        self.q = q
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        self.e = e
        self.d = pow(e, -1, self.phi)

    def public_key(self) -> tuple[int, int]:
        return (self.n, self.e)

    @staticmethod
    def encrypt(pubkey: tuple[int, int], message: int) -> int:
        n, e = pubkey
        return pow(message, e, n)

    def decrypt(self, secret: int) -> int:
        return pow(secret, self.d, self.n)

    def sign(self, message: bytes) -> tuple[bytes, int]:
        h = digest(self.n, message)
        s = pow(h, self.d, self.n)
        return (message, s)

    @staticmethod
    def verify(pubkey: tuple[int, int], signed_message: tuple[bytes, int]) -> bool:
        n, e = pubkey
        message, s = signed_message
        return pow(s, e, n) == digest(n, message)


# RSA feltörése faktorizációval (sympy.factorint)
def rsa_break(n: int, e: int, c: int) -> int:
    factors = list(factorint(n).keys())
    p, q = factors[0], factors[1]
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    return pow(c, d, n)


# Gyors RSA visszafejtés Kínai maradéktétellel (CRT)
def decrypt_crt(c: int, p: int, q: int, d: int) -> int:
    dp = d % (p - 1)
    dq = d % (q - 1)
    q_inv = pow(q, -1, p)
    mp = pow(c, dp, p)
    mq = pow(c, dq, q)
    md = (q_inv * (mp - mq)) % p
    return mq + q * md


# ==============================================================================
# ÖNÁLLÓ TESZTELŐ BLOKK (MINDEN JEGYZETBELI ÉS HÁZI ASSERT ELLENŐRZÉSE)
# ==============================================================================
if __name__ == "__main__":
    # 1. Oszthatóság tesztek
    for div_fn in (divides0, divides1, divides2):
        assert div_fn(3, 18) is True and div_fn(16, 1) is False and div_fn(5, 0) is True
    assert find_largest(100, 1000) == 6
    assert num_of_divisors(36) == 9 and sum_of_divisors(36) == 91
    assert divisor_sum_iteration(95) == [95, 25, 6, 6] and divisor_sum_iteration(20) == [20, 22, 14, 10, 8, 7, 1, 0]
    assert perfect_numbers({6, 28, 496, 100}) == {6, 28, 496}

    # 2. Prímek és Z_m tesztek
    assert irreducibles_of(6) == [] and primes_of(6) == [2, 3, 4]
    assert irreducibles_of(12) == [2, 10] and primes_of(12) == [2, 3, 9, 10]
    assert canonical_form(360) == [(2, 3), (3, 2), (5, 1)]
    assert num_of_divisors_from_factors(36) == 9
    assert primes_up_to_n(30) == primes_up_to_n_without_even(30) == primes_up_to_n_without_2_3_5(30)
    assert list_twin_primes(62, 109) == [(71, 73), (101, 103), (107, 109)]

    # 3. LNKO és Euklideszi tesztek
    assert greatest_common_divisor(24, 36) == 12 and least_common_multiple(24, 36) == 72
    for a in range(1, 15):
        for b in range(1, 15):
            x, y, r = extended_gcd(a, b)
            bx, by, br = binary_xgcd(a, b)
            assert x * a + y * b == r == gcd_w_eukl(a, b) == binary_gcd(a, b) == br == bx * a + by * b

    # 4. Diofantikus tesztek
    assert num_of_solutions(3, 5, 7) == math.inf and num_of_solutions(6, 9, 20) == 0
    assert num_of_payments() == 27 and num_of_purchases() == 7
    assert multi([7, 13, 15], 500, 50) == 40

    # 5. Maradékrendszerek és CRT tesztek
    assert find_class_representative(-6, 5) == 4
    assert classify_elements([1, 7, 9, 10], 4) == {1: [1, 9], 3: [7], 2: [10]}
    assert invmod(3, 11) == 4 and invmod(2, 6) is None
    assert my_solve_mod(175, 1540, 1792) == [60, 316, 572, 828, 1084, 1340, 1596]
    assert my_crt([2, 3, 2], [3, 5, 7]) == 23
    assert solve_system([2, 3], [2, 6], [4, 9]) == {5, 11, 17, 23, 29, 35}
    assert quadratic_residues(11) == {0, 1, 3, 4, 5, 9}

    # 6. Diszkrét logaritmus tesztek
    assert fastpow(3, 19) == 3**19
    assert powers_mod(3, 11) == {1, 3, 4, 5, 9}
    assert generators(11) == {2, 6, 7, 8}
    assert discrete_log_brute(2, 8, 11) == 3 and baby_step_giant_step(2, 8, 11) == 3
    assert prisoners_escape([2, 1, 4, 3], 2) is True and prisoners_escape([2, 3, 4, 1], 3) is False

    # 7. Euler-Fermat és Prímtesztek
    assert my_phi(36) == 12 and inverse_phi(24) == 35 and inverse_phi(14) is None
    assert find_carmichael({1, 2, 341, 561, 1105, 1729}) == {561, 1105, 1729}
    assert first_base(561) == 3 and first_base(7) is None
    assert fermat_test(341, [2]) is True and trial_division(341) is False
    assert miller_rabin(2047, [2]) is True and miller_rabin(2047, [2, 3]) is False

    # 8. Diffie-Hellman és ElGamal tesztek
    alice_dh, bob_dh = DH_participant(65537, 3), DH_participant(65537, 3)
    assert alice_dh.calculate_common_key(bob_dh.get_pub()) == bob_dh.calculate_common_key(alice_dh.get_pub())
    assert elgamal_break((23, 5, 8), (17, 18)) == 13
    assert dining_cryptographers([10, 20, 30], 65537, 3) == 60
    assert socialist_millionaires(500, 500, 65537, 3) is True
    assert socialist_millionaires(500, 600, 65537, 3) is False

    # 9. RSA tesztek
    assert are_valid_rsa_parameters(854383, 911683, 559913054987, 519917050283) is True
    alice_rsa = RSA(61, 53, 17)
    assert alice_rsa.decrypt(RSA.encrypt(alice_rsa.public_key(), 65)) == 65
    assert RSA.verify(alice_rsa.public_key(), alice_rsa.sign(b"Diszkret modellek")) is True
    assert rsa_break(3233, 17, 2790) == 65
    assert decrypt_crt(2790, 61, 53, 2753) == 65

    print("MINDEN PUSKA FÜGGVÉNY ÉS TESZTESET SIKERESEN LEFUTOTT (OK)!")



# =====================================================
# FONTOS TÉTELEK
# =====================================================

# gcd(a,b)|c
# <=> ax+by=c megoldható

# gcd(a,b)*lcm(a,b)=ab

# p prím
# =>
# φ(p)=p−1

# a^(p−1) ≡ 1 (mod p)

# Euler-Fermat:
# a^φ(m) ≡ 1 (mod m)
# ha gcd(a,m)=1

# RSA:
# e*d ≡ 1 (mod φ(n))

# Moduláris inverz létezik
# <=> gcd(a,m)=1

# Zm egységek:
# gcd(a,m)=1

# Lineáris kongruencia:
# a*x ≡ b (mod m)
# akkor oldható meg
# ha gcd(a,m)|b

# Diofantikus:
# ax+by=c
# akkor oldható meg
# ha gcd(a,b)|c