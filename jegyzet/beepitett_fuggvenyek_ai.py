import math
import secrets
import sympy as sp
from sympy.ntheory.modular import crt, solve_congruence
from sympy.ntheory.residue_ntheory import (
    discrete_log,
    primitive_root,
    is_primitive_root,
    n_order,
)

#Ezt a jegyzetet AI-al generáltattam le, amiben a beépített
#python függvények vannak a tananyaghoz kapcsolódóan

# ==============================================================================
# 1. OSZTHATÓSÁG ÉS OSZTÓK VIZSGÁLATA
# ==============================================================================

# divmod(a, b): Egyszerre adja vissza az egészrész-hányadost és a maradékot
q, r = divmod(47, 7)             # Kimenet: q = 6, r = 5 (mert 47 = 6*7 + 5)

# Pozitív osztók lekérdezése
osztok = sp.divisors(36)         # Kimenet: [1, 2, 3, 4, 6, 9, 12, 18, 36]
osztok_gen = sp.divisors(36, generator=True) # Memóriatakarékos generátor objektum

# Valódi osztók (maga a szám nélkül)
valodi_osztok = sp.proper_divisors(36)       # Kimenet: [1, 2, 3, 4, 6, 9, 12, 18]

# Osztók száma: d(n) vagy τ(n)
db = sp.divisor_count(36)        # Kimenet: 9
# Opcionális 2. paraméter (modulus): hány olyan osztó van, ami osztható pl. 3-mal?
db_3_mal = sp.divisor_count(36, 3) # Kimenet: 6 (Ezek: 3, 6, 9, 12, 18, 36)

# Osztók k-adik hatványösszege: σ_k(n) -> alapértelmezett k=1
szigma_0 = sp.divisor_sigma(36, 0) # Kimenet: 9  (0. hatványok összege = osztók száma)
szigma_1 = sp.divisor_sigma(36, 1) # Kimenet: 91 (1. hatványok: osztók sima összege)
szigma_2 = sp.divisor_sigma(36, 2) # Kimenet: 2210 (osztók négyzetösszege: 1^2 + 2^2 + ...)


# ==============================================================================
# 2. LEGNAGYOBB KÖZÖS OSZTÓ (LNKO) ÉS LEGKISEBB KÖZÖS TÖBBSZÖRÖS (LKKT)
# ==============================================================================

# math.gcd és math.lcm: 0, 2, vagy akár tetszőleges számú bemenetet is elfogadnak!
lnko_2 = math.gcd(48, 180)              # Kimenet: 12
lnko_sok = math.gcd(48, 180, 300, 72)   # Kimenet: 12 (több bemenet)
lnko_lista = math.gcd(*[48, 180, 300])  # Kimenet: 12 (lista kicsomagolása *-gal)

lkkt_2 = math.lcm(12, 18)               # Kimenet: 36
lkkt_sok = math.lcm(12, 18, 24, 30)     # Kimenet: 360 (több bemenet)

# SymPy alternatíva (listát, tuple-t és több argumentumot is elfogad)
sp_lnko = sp.ilcm(12, 18, 24)           # Kimenet: 72
sp_lkkt = sp.igcd(48, 180, 300)         # Kimenet: 12

# Bővített euklideszi algoritmus: a*x + b*y = gcd(a, b)
# Visszatérési érték: (x, y, lnko)
x_bezout, y_bezout, g = sp.gcdex(48, 180)
# Kimenet: x_bezout = -1, y_bezout = 0 helyett egész megoldás: (-1, 0 nem jó) ->
# Valós kimenet: x_bezout = -1, y_bezout = 0? Nem, SymPy-ban: (-1, 1, 12) ha (180, 48),
# sp.gcdex(48, 180) pontos kimenete: (4, -1, 12) -> mert 48*(4) + 180*(-1) = 192 - 180 = 12


# ==============================================================================
# 3. PRÍMEK ÉS A SZÁMELMÉLET ALAPTÉTELE (KANONIKUS FELBONTÁS)
# ==============================================================================

# Prímteszt (determinisztikus 2^64-ig, felette Miller-Rabin + Baillie-PSW)
prim_e_1 = sp.isprime(997)              # Kimenet: True
prim_e_2 = sp.isprime(999)              # Kimenet: False

# Számelmélet alaptétele: prímtényezős felbontás {prímalap: kitevő} szótárként
kanonikus = sp.factorint(1260)          # Kimenet: {2: 2, 3: 2, 5: 1, 7: 1} (2^2 * 3^2 * 5 * 7)
# Opcionális visual=True paraméterrel kifejezésként adja vissza:
vizualis_felbontas = sp.factorint(1260, visual=True) # Kimenet: 2**2*3**2*5**1*7**1
# Opcionális multiple=True paraméterrel sima listát ad a tényezőkkel (multiplicitással):
lista_felbontas = sp.factorint(1260, multiple=True)  # Kimenet: [2, 2, 3, 3, 5, 7]

# Csak az egyedi prímtényezők listája (kitevők nélkül):
egyedi_primek = sp.primefactors(1260)   # Kimenet: [2, 3, 5, 7]

# Prímek keresése, számlálása és generálása
otodik_prim = sp.prime(5)               # Kimenet: 11 (Az 5. prímszám: 2, 3, 5, 7, 11)
hany_prim_van = sp.primepi(20)          # Kimenet: 8  (π(20): hány prím van 20-ig bezárólag)

kovetkezo = sp.nextprime(100)           # Kimenet: 101 (100 utáni első prím)
kovetkezo_3 = sp.nextprime(100, ith=3)  # Kimenet: 107 (100 utáni 3. prím: 101, 103, 107)
elozo = sp.prevprime(100)               # Kimenet: 97  (100 előtti utolsó prím)

# Prímek listázása adott intervallumon: primerange([start,] stop)
primek_20ig = list(sp.primerange(20))       # Kimenet: [2, 3, 5, 7, 11, 13, 17, 19] (1 bemenet: 0-tól)
primek_inter = list(sp.primerange(10, 30))  # Kimenet: [11, 13, 17, 19, 23, 29] (2 bemenet: 10-től 30-ig)

# Véletlen prímszám adott [a, b) intervallumon
veletlen_prim = sp.randprime(1000, 2000)    # Kimenet: pl. 1453 (minden futáskor más prím)


# ==============================================================================
# 4. MARADÉKRENDSZEREK, MODULÁRIS INVERZ ÉS KÍNAI MARADÉKTÉTEL (CRT)
# ==============================================================================

# Beépített pow() függvény: 2 vagy 3 bemenetet fogad el!
sima_hatvany = pow(7, 3)                # Kimenet: 343 (2 bemenet: 7^3)
mod_hatvany = pow(7, 128, 19)           # Kimenet: 11  (3 bemenet: 7^128 mod 19 - gyorshatványozással!)

# Moduláris inverz: a^(-1) mod m (olyan x, amelyre a*x ≡ 1 mod m)
# Feltétel: math.gcd(a, m) == 1
inverz_builtin = pow(3, -1, 11)         # Kimenet: 4 (mert 3 * 4 = 12 ≡ 1 mod 11)
inverz_sympy = sp.mod_inverse(3, 11)    # Kimenet: 4 (SymPy megfelelője)

# Kínai maradéktétel (CRT): x ≡ v_i (mod m_i) kongruenciarendszer megoldása
# Példa: x ≡ 2 (mod 3), x ≡ 3 (mod 5), x ≡ 2 (mod 7)
modulusok = [3, 5, 7]
maradekok = [2, 3, 2]
crt_megoldas, crt_modulus = crt(modulusok, maradekok)
# Kimenet: crt_megoldas = 23, crt_modulus = 105 (azaz x ≡ 23 mod 105)

# Alternatíva: solve_congruence(*maradek_modulus_parok) -> tetszőleges számú (maradék, modulus) tuple-t fogad!
kongr_megoldas = solve_congruence((2, 3), (3, 5), (2, 7))
# Kimenet: (23, 105)


# ==============================================================================
# 5. EULER–FERMAT-TÉTEL ÉS REDUKÁLT TOTIENS
# ==============================================================================

# Euler-féle φ(n) (totient) függvény: n-hez relatív prímek száma 1-től n-ig
phi_40 = sp.totient(40)                 # Kimenet: 16

# Carmichael-féle λ(n) (reduced totient) függvény: a legkisebb univerzális kitevő, amire a^λ(n) ≡ 1 (mod n)
lambda_40 = sp.reduced_totient(40)      # Kimenet: 4 (míg φ(40)=16, már a 4. hatvány is mindig 1-et ad mod 40!)

# Euler–Fermat-tétel ellenőrzése: ha gcd(a, n) == 1, akkor a^φ(n) ≡ 1 (mod n)
a_ef, n_ef = 7, 40
euler_teszt = pow(a_ef, int(phi_40), n_ef)          # Kimenet: 1 (mert 7^16 ≡ 1 mod 40)
carmichael_teszt = pow(a_ef, int(lambda_40), n_ef)  # Kimenet: 1 (mert 7^4 = 2401 = 60*40 + 1 ≡ 1 mod 40)

# Moduláris inverz számítása közvetlenül az Euler–Fermat-tétellel: a^(φ(n)-1) mod n
inverz_eulerrel = pow(a_ef, int(phi_40) - 1, n_ef)  # Kimenet: 23 (mert 7 * 23 = 161 ≡ 1 mod 40)


# ==============================================================================
# 6. DIOFANTIKUS EGYENLETEK (TÖBB VÁLTOZÓVAL ÉS TÍPUSSAL)
# ==============================================================================

x, y, z = sp.symbols("x y z", integer=True)

# A) Kétváltozós lineáris diofantikus egyenlet: 15*x + 25*y = 105 (0-ra rendezve!)
diof_2valtozos = sp.diophantine(15*x + 25*y - 105)
# Kimenet: {(5*t_0 + 7, -3*t_0)} -> ahol t_0 tetszőleges egész szám

# B) Háromváltozós lineáris diofantikus egyenlet: 6*x + 10*y + 15*z = 1
diof_3valtozos = sp.diophantine(6*x + 10*y + 15*z - 1)
# Kimenet: {(5*t_0 + 15*t_1 + 1, -3*t_0 + 15*t_2 + 1, -15*t_1 - 10*t_2 - 1)}

# C) Másodfokú (Pitagoraszi / Pell) diofantikus egyenlet: x^2 + y^2 = 25
diof_masodfoku = sp.diophantine(x**2 + y**2 - 25)
# Kimenet: {(-5, 0), (-4, -3), (-4, 3), (-3, -4), (-3, 4), (0, -5), (0, 5), (3, -4), (3, 4), (4, -3), (4, 3), (5, 0)}


# ==============================================================================
# 7. MULTIPLIKATÍV REND, PRIMITÍV GYÖKÖK ÉS DISZKRÉT LOGARITMUS
# ==============================================================================

# Multiplikatív rend (order): a legkisebb k > 0 kitevő, amelyre a^k ≡ 1 (mod n)
rend = n_order(3, 7)                    # Kimenet: 6 (mert 3^6 ≡ 1 mod 7, és kisebb kitevőre nem 1)

# Primitív gyök (generátor): olyan g elem, melynek rendje pontosan φ(n)
prim_gyok = primitive_root(41)          # Kimenet: 6 (a legkisebb primitív gyök mod 41)
prim_gyok_e = is_primitive_root(6, 41)  # Kimenet: True

# Diszkrét logaritmus: b^x ≡ a (mod n) -> keressük x-et!
# Szintaxis: discrete_log(modulus, eredmeny_a, alap_b, order=None)
# 1. Alap hívás (automatikus algoritmusválasztás: Baby-step Giant-step / Pollard-rho / Pohlig-Hellman)
dlog_x = discrete_log(41, 13, 6)        # Kimenet: 27 (mert 6^27 ≡ 13 mod 41)

# 2. Gyorsított hívás ismert renddel (ha az alap rendjét előre tudjuk, átadható 'order' paraméterként)
dlog_gyors = discrete_log(41, 13, 6, order=40) # Kimenet: 27


# ==============================================================================
# 8. DIFFIE–HELLMAN KULCSCSERE (KOMPLETT PÉLDA KONKRÉT SZÁMOKKAL)
# ==============================================================================

# 1. Nyilvános paraméterek: p prímszám és g primitív gyök modulo p
dh_p = 467
dh_g = primitive_root(dh_p)             # Kimenet: 2 (2 primitív gyök mod 467)

# 2. Privát (titkos) kulcsok (élesben: secrets.randbelow(dh_p - 3) + 2)
alice_titkos = 153
bob_titkos = 298

# 3. Nyilvános kulcsok generálása: g^titkos mod p
alice_nyilvanos = pow(dh_g, alice_titkos, dh_p) # Kimenet: 156 (2^153 mod 467)
bob_nyilvanos = pow(dh_g, bob_titkos, dh_p)     # Kimenet: 39  (2^298 mod 467)

# 4. Közös titok kiszámítása mindkét oldalon
kozos_titok_alice = pow(bob_nyilvanos, alice_titkos, dh_p) # Kimenet: 220 (39^153 mod 467)
kozos_titok_bob = pow(alice_nyilvanos, bob_titkos, dh_p)   # Kimenet: 220 (156^298 mod 467)


# ==============================================================================
# 9. RSA ALGORITMUS (KOMPLETT PÉLDA + KÍNAI MARADÉKTÉTELES GYORSÍTÁS)
# ==============================================================================

# 1. Két prímszám választása (élesben: sp.randprime(10**100, 10**101))
rsa_p = 61
rsa_q = 53

# 2. Modulus (n) és Euler-féle φ(n)
rsa_n = rsa_p * rsa_q                   # Kimenet: 3233
rsa_phi = (rsa_p - 1) * (rsa_q - 1)     # Kimenet: 3120 (sp.totient(3233) is 3120)

# 3. Nyilvános kitevő (e), amely relatív prím phi-hez
rsa_e = 17                              # math.gcd(17, 3120) -> Kimenet: 1

# 4. Titkos kitevő (d): e moduláris inverze modulo phi
rsa_d = pow(rsa_e, -1, rsa_phi)         # Kimenet: 2753 (mert 17 * 2753 = 46801 = 15*3120 + 1)

# 5. Titkosítás (c = m^e mod n) és Visszafejtés (m = c^d mod n)
uzenet = 65
titkositott = pow(uzenet, rsa_e, rsa_n)       # Kimenet: 2790 (65^17 mod 3233)
visszafejtett = pow(titkositott, rsa_d, rsa_n)# Kimenet: 65   (2790^2753 mod 3233)

# +1: RSA-CRT visszafejtés (a gyakorlatban így gyorsítják 4x-esére a visszafejtést a Kínai Maradéktétellel)
dp = rsa_d % (rsa_p - 1)                # Kimenet: 53 (2753 mod 60)
dq = rsa_d % (rsa_q - 1)                # Kimenet: 49 (2753 mod 52)
m_p = pow(titkositott, dp, rsa_p)       # Kimenet: 4  (2790^53 mod 61)
m_q = pow(titkositott, dq, rsa_q)       # Kimenet: 12 (2790^49 mod 53)
visszafejtett_crt, _ = crt([rsa_p, rsa_q], [m_p, m_q]) # Kimenet: 65 (x ≡ 4 mod 61 és x ≡ 12 mod 53)