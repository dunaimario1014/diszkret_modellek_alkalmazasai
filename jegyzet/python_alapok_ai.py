# ==============================================================================
# 1. ALAPTÍPUSOK, OPERÁTOROK ÉS TÍPUSKONVERZIÓ
# ==============================================================================

egesz = 42
lebegopontos = 3.14
szoveg = "Python"
logikai = True
ures = None

# Matematikai és bitműveletek
alap_muv = (10 + 3, 10 - 3, 10 * 3, 10 / 3) # (13, 7, 30, 3.3333333333333335)
egesz_oszt = 10 // 3                        # 3 (lefelé kerekít)
maradek = 10 % 3                            # 1
hatvany = 2 ** 10                           # 1024
bit_muv = (5 & 3, 5 | 3, 5 ^ 3, ~5, 5 << 1, 5 >> 1) # (1, 7, 6, -6, 10, 2)

# Típuskonverziók és számrendszerek
szam_strbol = int("42")                     # 42
bin_strbol = int("1010", 2)                 # 10 (kettes számrendszerből)
hex_strbol = int("ff", 16)                  # 255 (tizenhatosból)
bin_alak = bin(10)                          # '0b1010'
hex_alak = hex(255)                         # '0xff'
tipus_ell = isinstance(42, (int, float))    # True (több típusra is ellenőriz)


# ==============================================================================
# 2. STRINGEK (SZÖVEGEK) KEZELÉSE ÉS FORMÁZÁSA
# ==============================================================================

s = "  helló, Python világ!  "

# Tisztítás, kis- és nagybetűsítés
s_strip = s.strip()                         # 'helló, Python világ!' (bal: lstrip, jobb: rstrip)
s_upper = s_strip.upper()                   # 'HELLÓ, PYTHON VILÁG!'
s_lower = s_strip.lower()                   # 'helló, python világ!'
s_title = s_strip.title()                   # 'Helló, Python Világ!'

# Keresés, csere, darabolás, összefűzés
ind = s_strip.find("Python")                # 7 (-1, ha nincs benne; az .index() hibát dob)
db_o = s_strip.count("l")                   # 3
cserelt = s_strip.replace("Python", "C++")  # 'helló, C++ világ!'
szavak = s_strip.split(" ")                 # ['helló,', 'Python', 'világ!']
ossze = "-".join(["a", "b", "c"])           # 'a-b-c'

# Ellenőrzések és karakterkódok (kriptográfiában gyakori)
kezdodik = s_strip.startswith(("h", "H"))   # True (tuple-t is elfogad!)
szam_e = "12345".isdigit()                  # True (isalpha: betű, isalnum: betű+szám)
ascii_kod = ord("A")                        # 65
karakter = chr(65)                          # 'A'

# F-string formázás (Python 3.6+)
pi = 3.14159265
f_alap = f"Érték: {pi:.2f}"                 # 'Érték: 3.14' (2 tizedesjegy)
f_pad = f"{42:05d}"                         # '00042' (nullákkal feltöltve 5 hosszig)
f_bin = f"{10:08b}"                         # '00001010' (8 bites bináris)
f_debug = f"{egesz=}"                       # 'egesz=42' (változónév + érték)


# ==============================================================================
# 3. LISTÁK (LIST) - Módosítható (Mutable), rendezett sorozat
# ==============================================================================

lista = [10, 20, 30, 40, 50]

# Indexelés és szeletelés (Slicing): lista[start:stop:step] - minden sorozatra (str, tuple) működik!
elso = lista[0]                             # 10
utolso = lista[-1]                          # 50
szelet = lista[1:4]                         # [20, 30, 40] (1-től 4-ig, a 4. már nincs benne)
minden_masodik = lista[::2]                 # [10, 30, 50]
megforditva = lista[::-1]                   # [50, 40, 30, 20, 10]

# Elem hozzáadása
lista.append(60)                            # [10, 20, 30, 40, 50, 60] (végére 1 elem)
lista.insert(1, 15)                         # [10, 15, 20, 30, 40, 50, 60] (1-es indexre)
lista.extend([70, 80])                      # [10, 15, 20, 30, 40, 50, 60, 70, 80] (több elem a végére)

# Elem törlése és kivétele
kidobott_utolso = lista.pop()               # 80 -> lista: [10, 15, 20, 30, 40, 50, 60, 70]
kidobott_index = lista.pop(1)               # 15 -> lista: [10, 20, 30, 40, 50, 60, 70]
lista.remove(40)                            # [10, 20, 30, 50, 60, 70] (első 40-es értéket törli)
del lista[0:2]                              # [30, 50, 60, 70] (szelet törlése)

# Keresés, rendezés, másolás
pozicio = lista.index(50)                   # 1 (50-es elem indexe)
benne_van = 60 in lista                     # True
lista.reverse()                             # [70, 60, 50, 30] (helyben fordítja meg)
lista.sort()                                # [30, 50, 60, 70] (helyben rendez)
lista.sort(reverse=True)                    # [70, 60, 50, 30] (csökkenő)

# Rendezés egyedi kulcs alapján (pl. abszolút érték szerint, új listába)
szamok = [-15, 2, -19, 8]
rendezett = sorted(szamok, key=abs)         # [2, 8, -15, -19]

# Sekély másolás (hogy az eredeti ne módosuljon)
masolat = lista.copy()                      # [70, 60, 50, 30] (vagy: lista[:])


# ==============================================================================
# 4. TUPLE (N-ES) - Nem módosítható (Immutable), rendezett, hash-elhető
# ==============================================================================

ures_tuple = ()
egy_elemu = (42,)                           # (42,) -> A vessző KÖTELEZŐ, különben csak zárójel!
t = (10, 20, 30, 20, 40)

t_db = t.count(20)                          # 2
t_ind = t.index(30)                         # 2

# Kicsomagolás (Unpacking) - bárhol működik (listánál, generátornál is)
a, b, c = (1, 2, 3)                         # a=1, b=2, c=3
a, b = b, a                                 # a=2, b=1 (változók cseréje segédváltozó nélkül)
elso_t, *kozepso_t, utolso_t = (1, 2, 3, 4, 5) # elso_t=1, kozepso_t=[2, 3, 4], utolso_t=5


# ==============================================================================
# 5. SZÓTÁRAK (DICT) - Kulcs-érték párok (O(1) gyors keresés)
# ==============================================================================

ures_dict = {}
d = {"a": 1, "b": 2, "c": 3}
d_parokbol = dict([("x", 10), ("y", 20)])   # {'x': 10, 'y': 20}
d_zipbol = dict(zip(["a", "b"], [1, 2]))    # {'a': 1, 'b': 2}

# Olvasás és módosítás
ertek_a = d["a"]                            # 1 (KeyError, ha nem létezik a kulcs)
ertek_bizt = d.get("z", 0)                  # 0 (biztonságos: ha nincs 'z', alapértéket ad)
d["d"] = 4                                  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# Ha nincs ilyen kulcs, létrehozza az alapértékkel, és visszaadja (listák gyűjtésére kiváló)
d.setdefault("e", 5)                        # 5 -> d: {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}

# Összefésülés és törlés
d.update({"a": 99, "f": 6})                 # {'a': 99, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
d_uj = d | {"g": 7}                         # Új dict összefűzéssel (Python 3.9+)
kivett_ertek = d.pop("f", None)             # 6 (törli 'f'-et; None-t ad, ha nem létezett)

# Lekérdezések (nézetek)
kulcsok = list(d.keys())                    # ['a', 'b', 'c', 'd', 'e']
ertekek = list(d.values())                  # [99, 2, 3, 4, 5]
elemek = list(d.items())                    # [('a', 99), ('b', 2), ('c', 3), ('d', 4), ('e', 5)]
kulcs_ell = "a" in d                        # True (mindig a kulcsokban keres!)


# ==============================================================================
# 6. HALMAZOK (SET) - Egyedi, rendezetlen elemek, halmazműveletek
# ==============================================================================

ures_set = set()                            # A {} üres szótárat csinál, NEM halmazt!
h1 = {1, 2, 3, 3, 3}                        # {1, 2, 3} (duplikációkat automatikusan törli)
h2 = set([3, 4, 5])                         # {3, 4, 5} (lista duplikációinak szűrésére is)

# Módosítás
h1.add(0)                                   # {0, 1, 2, 3}
h1.update([6, 7])                           # {0, 1, 2, 3, 6, 7}
h1.discard(99)                              # Nem dob hibát, ha a 99 nincs benne (.remove() hibát dob)
h1.discard(0); h1.discard(6); h1.discard(7) # Visszaállítva: {1, 2, 3}

# Matematikai halmazműveletek
unio = h1 | h2                              # {1, 2, 3, 4, 5} (vagy: h1.union(h2))
metszet = h1 & h2                           # {3}             (vagy: h1.intersection(h2))
kulonbseg = h1 - h2                         # {1, 2}          (vagy: h1.difference(h2))
szimm_kul = h1 ^ h2                         # {1, 2, 4, 5}    (vagy: h1.symmetric_difference(h2))
reszhalmaz = {1, 2} <= h1                   # True            (valódi részhalmaz: <)


# ==============================================================================
# 7. COMPREHENSIONS (EGYSOROS GENERÁLÁS)
# ==============================================================================

# List comprehension: [kifejezés for elem in sorozat if feltétel]
negyzetek = [x**2 for x in range(5)]                    # [0, 1, 4, 9, 16]
paros_negyzet = [x**2 for x in range(6) if x % 2 == 0]  # [0, 4, 16]

# Ha-akkor-különben (if-else) a kifejezésben (ekkor az if ELŐRE kerül!)
cimkek = ["páros" if x % 2 == 0 else "páratlan" for x in range(3)] # ['páros', 'páratlan', 'páros']

# Mátrix kilapítása (dupla ciklus: balról jobbra olvasandó)
matrix = [[1, 2], [3, 4]]
lapos = [elem for sor in matrix for elem in sor]        # [1, 2, 3, 4]

# Dict, Set és Generator comprehension
dict_comp = {x: x**2 for x in range(3)}                 # {0: 0, 1: 1, 2: 4}
dict_forditva = {v: k for k, v in dict_comp.items()}    # {0: 0, 1: 1, 4: 2} (kulcs-érték csere)
set_comp = {x % 3 for x in range(10)}                   # {0, 1, 2}
gen_exp = (x**2 for x in range(5))                      # Generátor (nem foglal memóriát, sum()-ba kiváló)


# ==============================================================================
# 8. VEZÉRLÉSI SZERKEZETEK (IF, FOR, WHILE, MATCH)
# ==============================================================================

# Elágazás és Ternary (egysoros) operátor
x_ert = 15
if 10 <= x_ert < 20:                        # Láncolt összehasonlítás!
    allapot = "közepes"                     # 'közepes'
elif x_ert >= 20:
    allapot = "nagy"
else:
    allapot = "kicsi"

egysoros_if = "pozitív" if x_ert > 0 else "nem pozitív" # 'pozitív'

# Rozmár operátor (Walrus: :=) -> értékadás és kiértékelés egyben (Python 3.8+)
if (hossz := len([1, 2, 3])) > 2:
    rozmar_eredmeny = hossz                 # 3

# For ciklusok és hasznos iterátorok
r_alap = list(range(4))                     # [0, 1, 2, 3]
r_lepes = list(range(10, 2, -2))            # [10, 8, 6, 4] (visszafelé kettesével)

# enumerate: index és érték egyszerre (start paraméterrel eltolható a sorszámozás)
enum_lista = [(i, v) for i, v in enumerate(["a", "b"], start=1)] # [(1, 'a'), (2, 'b')]

# zip: több lista párhuzamos bejárása (a legrövidebbig tart)
zip_lista = list(zip([1, 2], ["a", "b"], [True, False])) # [(1, 'a', True), (2, 'b', False)]

# For-Else: az 'else' ág CSAK akkor fut le, ha a ciklus NEM 'break'-kel állt meg!
for n in [2, 4, 6]:
    if n % 2 == 1:
        break
else:
    nincs_paratlan = True                   # True (mivel sosem futott bele a break-be)

# Match-Case (mintafelismerés, Python 3.10+)
pont = (0, 5)
match pont:
    case (0, 0):
        hely = "Origó"
    case (0, y) if y > 0:                   # Kicsomagolás + feltétel (guard)
        hely = f"Pozitív Y tengely: {y}"    # 'Pozitív Y tengely: 5'
    case _:                                 # Default ág
        hely = "Egyéb"


# ==============================================================================
# 9. HASZNOS BEÉPÍTETT FÜGGVÉNYEK (BUILT-INS) ÉS ITERTOOLS / COLLECTIONS
# ==============================================================================

szam_sor = [-5, 2, 8, -1, 4]

# Aggregációk
minimum = min(szam_sor)                     # -5
min_abs = min(szam_sor, key=abs)            # -1 (legkisebb abszolút értékű!)
maximum = max(szam_sor)                     # 8
szumma = sum(szam_sor, start=100)           # 108 (100 + az elemek összege)
kerek = round(3.14159, 2)                   # 3.14

# Logikai ellenőrzések sorozatokra
minden_igaz = all(x > 0 for x in [1, 2, 3]) # True (igaz, ha MINDEN elemre igaz)
van_igaz = any(x < 0 for x in szam_sor)     # True (igaz, ha LEGALÁBB EGY elemre igaz)

# Map és Filter
lekepezve = list(map(abs, szam_sor))        # [5, 2, 8, 1, 4] (függvény alkalmazása minden elemre)
szurve = list(filter(None, [0, 1, "", "a"]))# [1, 'a'] (kiszűri a hamis/üres értékeket)

# Gyakoriságszámlálás (Counter) és Alapértelmezett szótár (defaultdict)
from collections import Counter, defaultdict

szamlalo = Counter("abrakadabra")           # Counter({'a': 5, 'b': 2, 'r': 2, 'k': 1, 'd': 1})
leggyakoribb_2 = szamlalo.most_common(2)    # [('a', 5), ('b', 2)]

csoportok = defaultdict(list)               # Ha nem létezik a kulcs, automatikusan üres listát hoz létre
csoportok["páros"].append(2)                # {'páros': [2]} (nincs KeyError!)

# Kombinatorika (itertools)
from itertools import permutations, combinations, product

perm = list(permutations([1, 2, 3], 2))     # [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)] (sorrend számít)
komb = list(combinations([1, 2, 3], 2))     # [(1, 2), (1, 3), (2, 3)] (sorrend nem számít)
descartes = list(product([0, 1], repeat=2)) # [(0, 0), (0, 1), (1, 0), (1, 1)] (Descartes-szorzat)