# -*- coding: utf-8 -*-
"""Vérification des calculs de la notion 262 (5e : multiples, diviseurs et partages).

Cours, fiche et 10 exercices : chaque résultat numérique est recalculé
(sympy pour les diviseurs et la primalité). Lancer : python verif_262.py
"""
import importlib.util
from math import gcd, lcm
from pathlib import Path

from sympy import divisors, isprime, primerange

n_ok = 0


def ok(cond, msg):
    global n_ok
    assert cond, msg
    n_ok += 1


def de(a, b, q, r):
    """a = b × q + r est la division euclidienne."""
    ok(a == b * q + r and 0 <= r < b and divmod(a, b) == (q, r), f"division {a} / {b}")


def criteres(n):
    """Critères 2, 3, 4, 5, 9, 10 (tels qu'énoncés dans le cours) contre la vraie divisibilité."""
    s = sum(map(int, str(n)))
    c = {2: str(n)[-1] in "02468", 3: s % 3 == 0, 4: int(str(n)[-2:]) % 4 == 0,
         5: str(n)[-1] in "05", 9: s % 9 == 0, 10: str(n)[-1] == "0"}
    for d, v in c.items():
        ok(v == (n % d == 0), f"critère {d} pour {n}")
    return {d for d, v in c.items() if v}


def communs(*ns):
    return sorted(set.intersection(*(set(divisors(n)) for n in ns)))


# ------------------------------------------------------------------ cours
de(23, 5, 4, 3)
de(158, 7, 22, 4)
ok(158 == 7 * 21 + 11 and 11 > 7, "fausse division 158 = 7 × 21 + 11")
ok(7 * 22 == 154 and 154 <= 158 < 161 == 7 * 23, "encadrement 158")
ok(56 == 8 * 7, "56 = 8 × 7")
de(60, 7, 8, 4)
ok([9 * k for k in range(5)] == [0, 9, 18, 27, 36], "multiples de 9")
ok(divisors(24) == [1, 2, 3, 4, 6, 8, 12, 24] and 24 % 5 != 0, "diviseurs de 24")
ok(set(criteres(1548)) == {2, 3, 4, 9}, "critères 1 548")
ok(1548 == 9 * 172 == 4 * 387, "1 548 = 9 × 172 = 4 × 387")
de(34, 4, 8, 2)
ok(23 % 3 != 0, "23 non divisible par 3")
ok(12 % 3 == 0 and 12 % 9 != 0, "12 divisible par 3, pas par 9")
ok(isprime(13) and divisors(15) == [1, 3, 5, 15] and not isprime(1), "13, 15, 1")
ok(list(primerange(1, 30)) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29], "premiers < 30")
ok(list(primerange(1, 51)) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47], "premiers < 50 (crible)")
ok(87 == 3 * 29 and 8 + 7 == 15, "87 = 3 × 29")
ok(isprime(89) and all(89 % p for p in (2, 3, 5, 7)), "89 premier")
ok(all(isprime(n) == (n > 1 and all(n % p or n == p for p in (2, 3, 5, 7))) for n in range(1, 100)),
   "règle : < 100, tester 2, 3, 5, 7")
ok(9 == 3 * 3 and 21 == 3 * 7 and 49 == 7 * 7, "impairs non premiers")
ok(divisors(12) == [1, 2, 3, 4, 6, 12] and divisors(18) == [1, 2, 3, 6, 9, 18], "diviseurs 12 et 18")
ok(communs(12, 18) == [1, 2, 3, 6] and 12 // 6 == 2 and 18 // 6 == 3, "lots cours 12 et 18")
ok(lcm(4, 6) == 12 and [m for m in range(1, 40) if m % 4 == 0 and m % 6 == 0] == [12, 24, 36], "guirlandes")
ok(10 % 4 and 10 % 6, "4 + 6 = 10 pas multiple")

# ------------------------------------------------------------------ fiche
de(50, 8, 6, 2)
ok(6 + 1 == 7, "7 pages")

# ------------------------------------------------------------------ 2731 division euclidienne
de(347, 9, 38, 5)
ok(9 * 38 == 342, "9 × 38")
de(254, 6, 42, 2)
ok(6 * 4 == 24 <= 25 < 30 and 25 - 24 == 1 and 14 - 12 == 2, "étapes 254 / 6")
ok(6 * 41 + 8 == 246 + 8 == 254 and 8 > 6 and 6 * 42 == 252, "égalités 254")
de(260, 6, 43, 2)
ok(260 == 254 + 6, "260 = 254 + 6")

# ------------------------------------------------------------------ 2726 multiples et diviseurs
ok(42 == 6 * 7 and 35 == 5 * 7 and 90 == 9 * 10, "produits")
ok([m for m in range(50, 101) if m % 8 == 0] == [56, 64, 72, 80, 88, 96], "multiples de 8 entre 50 et 100")
ok(8 * 6 == 48 and 8 * 7 == 56 and 104 > 100, "bornes")
de(91, 7, 13, 0)
de(100, 7, 14, 2)
ok(0 % 8 == 0 and 37 % 1 == 0 and 6 % 24 != 0 and 24 % 6 == 0, "vrai ou faux")

# ------------------------------------------------------------------ 2730 critères
ok(criteres(360) == {2, 3, 4, 5, 9, 10}, "360")
ok(criteres(1245) == {3, 5}, "1 245")
ok(criteres(2718) == {2, 3, 9}, "2 718")
ok(criteres(5116) == {2, 4}, "5 116")
ok(60 == 4 * 15 and 18 == 4 * 4 + 2 and 16 == 4 * 4, "deux derniers chiffres")
ok((3 + 6, 1 + 2 + 4 + 5, 2 + 7 + 1 + 8, 5 + 1 + 1 + 6) == (9, 12, 18, 13), "sommes")
ok(min(n for n in range(100, 1000) if n % 2 == 0 and n % 5 == 0 and n % 9 == 0) == 180, "plus petit 180")
ok(180 == 2 * 90 == 5 * 36 == 9 * 20, "180")

# ------------------------------------------------------------------ 2738 rectangles
ok(divisors(36) == [1, 2, 3, 4, 6, 9, 12, 18, 36], "diviseurs de 36")
paires = [(d, 36 // d) for d in divisors(36) if d <= 36 // d]
ok(paires == [(1, 36), (2, 18), (3, 12), (4, 9), (6, 6)], "rectangles 36")
de(36, 5, 7, 1)
ok([2 * (a + b) for a, b in paires] == [74, 40, 30, 26, 24], "périmètres")
ok(min(2 * (a + b) for a, b in paires) == 24, "périmètre minimal")
ok(divisors(37) == [1, 37] and isprime(37), "37 premier")
de(37, 6, 6, 1)
ok(7 * 7 == 49 > 37 and 3 + 7 == 10, "arrêt 37")

# ------------------------------------------------------------------ 2737 chiffre manquant
ok([c for c in range(10) if (402 + 10 * c) % 3 == 0] == [0, 3, 6, 9], "4□2 divisible par 3")
ok([400 + 10 * c + 2 for c in range(10) if (402 + 10 * c) % 9 == 0] == [432] and 432 == 9 * 48, "4□2 par 9")
ok(all((402 + 10 * c) % 5 for c in range(10)), "4□2 jamais par 5")
ok([c for c in range(10) if (570 + c) % 4 == 0] == [2, 6], "57□ par 4")
ok(572 % 3 != 0 and 576 % 3 == 0 and 576 == 3 * 192, "57□ par 3")
ok(4 * 18 == 72 and 4 * 19 == 76 and 4 * 17 == 68, "multiples de 4 entre 70 et 79")
ok([c for c in range(10) if (205 + 10 * c) % 9 == 0] == [2], "2□5 par 9")
ok(225 == 9 * 25 == 5 * 45 and 225 % 10, "225")

# ------------------------------------------------------------------ 2728 nombres premiers
ok(sorted(n for n in range(4, 51, 2)) == [n for n in range(2, 51) if n % 2 == 0 and n != 2], "pairs rayés")
ok([n for n in range(4, 51) if n % 3 == 0 and n % 2 and n != 3] == [9, 15, 21, 27, 33, 39, 45], "multiples de 3 restants")
ok([n for n in range(6, 51) if n % 5 == 0 and n % 2 and n % 3 and n != 5] == [25, 35], "multiples de 5 restants")
ok([n for n in range(8, 51) if n % 7 == 0 and n % 2 and n % 3 and n % 5 and n != 7] == [49], "multiples de 7 restants")
reste = [n for n in range(2, 51) if all(n % p or n == p for p in (2, 3, 5, 7))]
ok(reste == list(primerange(1, 51)) and len(reste) == 15, "crible 1-50")
ok(11 * 11 == 121 > 50, "arrêt à 7")
ok(51 == 3 * 17 and 57 == 3 * 19 and 91 == 7 * 13 and isprime(97), "51, 57, 91, 97")
ok(not any(isprime(n) for n in (51, 57, 91)), "51, 57, 91 non premiers")
de(97, 7, 13, 6)
ok(9 + 7 == 16 and 16 % 3, "97 et 3")
ok(divisors(9) == [1, 3, 9], "9 non premier")

# ------------------------------------------------------------------ 2729 œufs
de(38, 6, 6, 2)
ok(6 * 6 == 36 <= 38 < 42 == 6 * 7, "encadrement 38")
ok(7 * 6 - 38 == 4, "places vides")
de(245, 12, 20, 5)
ok(12 * 20 == 240 and 12 * 21 == 252 and 20 * 4 == 80, "245 œufs, 80 €")
de(20, 3, 6, 2)

# ------------------------------------------------------------------ 2727 bonbons
de(18, 4, 4, 2)
ok(18 == 3 * 6 and 30 == 3 * 10, "3 sachets")
ok(divisors(18) == [1, 2, 3, 6, 9, 18] and divisors(30) == [1, 2, 3, 5, 6, 10, 15, 30], "diviseurs 18, 30")
ok(communs(18, 30) == [1, 2, 3, 6] and gcd(18, 30) == 6, "sachets possibles")
ok(18 // 6 == 3 and 30 // 6 == 5, "composition")
ok(18 + 30 == 48 == 8 * 6, "48 = 8 × 6")
de(18, 8, 2, 2)
de(30, 8, 3, 6)

# ------------------------------------------------------------------ 2745 navettes (minutes après 9 h)
A = [10 + 8 * k for k in range(20)]
B = [14 + 12 * k for k in range(20)]
ok([t for t in A if t <= 50] == [10, 18, 26, 34, 42, 50], "départs A")
ok([t for t in B if t <= 50] == [14, 26, 38, 50], "départs B")
com = sorted(set(A) & set(B))
ok(com[:3] == [26, 50, 74], "départs communs 9 h 26, 9 h 50, 10 h 14")
ok(lcm(8, 12) == 24 and com[1] - com[0] == 24 == com[2] - com[1], "toutes les 24 min")
ok(26 - 10 == 16 == 2 * 8 and 26 - 14 == 12, "vérification 9 h 26")
ok(74 - 10 == 64 == 8 * 8 and len([t for t in A if t <= 74]) == 9, "9 départs de A")
ok(10 + 24 == 34 and 34 not in B, "erreur 9 h 34")

# ------------------------------------------------------------------ 2744 kermesse
de(213, 9, 23, 6)
ok(21 - 18 == 3 and 33 - 27 == 6, "étapes 213 / 9")
ok(24 * 9 == 216 and 216 - 213 == 3, "minibus")
ok(84 % 9 != 0 and 8 + 4 == 12, "pas 9 lots")
de(84, 9, 9, 3)
ok(divisors(84) == [1, 2, 3, 4, 6, 7, 12, 14, 21, 28, 42, 84], "diviseurs 84")
ok(communs(84, 126) == [1, 2, 3, 6, 7, 14, 21, 42], "lots possibles")
ok(126 == 2 * 63 == 3 * 42 == 6 * 21 == 7 * 18 == 14 * 9, "produits 126")
de(126, 4, 31, 2)
ok(max(d for d in communs(84, 126) if d <= 20) == 14 and 84 // 14 == 6 and 126 // 14 == 9, "14 lots")
ok([n for n in range(100, 201) if n % 36 == 0 and (n // 10) % 10 == 4] == [144], "ticket 144")
ok(144 == 4 * 36 == 9 * 16 and 44 == 4 * 11, "144")
ok([n for n in range(90, 101) if isprime(n)] == [97], "seul premier entre 90 et 100")
ok(93 % 3 == 0 and 99 % 3 == 0 and 91 == 7 * 13, "éliminations")

# ------------------------------------------------------------------ figures : divisions posées
spec = importlib.util.spec_from_file_location("fig262", Path(__file__).parent / "figures" / "figures.py")
fig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fig)
for a, b, etapes in [(158, 7, [(1, 15, 14, 1), (2, 18, 14, 4)]),
                     (347, 9, [(1, 34, 27, 7), (2, 77, 72, 5)]),
                     (254, 6, [(1, 25, 24, 1), (2, 14, 12, 2)]),
                     (213, 9, [(1, 21, 18, 3), (2, 33, 27, 6)])]:
    q, r, e = fig.etapes_division(a, b)
    ok((q, r) == divmod(a, b) and e == etapes, f"figure division {a} / {b}")
ok(sum(1 for n in range(2, 51) if isprime(n)) == 15, "légende du crible")

print(f"verif_262 : {n_ok} contrôles, tout est juste.")
