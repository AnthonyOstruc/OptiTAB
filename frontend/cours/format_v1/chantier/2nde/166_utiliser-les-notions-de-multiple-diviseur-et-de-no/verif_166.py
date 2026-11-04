# -*- coding: utf-8 -*-
"""Vérification de tous les résultats de la notion 166 (cours, fiche, exercices)."""
from math import gcd
from fractions import Fraction
from sympy import factorint, isprime, divisors, primerange

def lcm(*xs):
    r = 1
    for x in xs:
        r = r * x // gcd(r, x)
    return r

def ok(cond, msg):
    assert cond, msg
    print("OK", msg)

# ---------------- cours / fiche
ok(36 == 4 * 9, "36 = 4 x 9")
ok(divisors(36) == [1, 2, 3, 4, 6, 9, 12, 18, 36], "diviseurs de 36")
ok(sum(map(int, "4512")) == 12 and 4512 % 3 == 0, "4512 divisible par 3")
ok(isprime(97) and all(97 % p for p in (2, 3, 5, 7)) and 11**2 > 97, "97 premier")
ok(factorint(84) == {2: 2, 3: 1, 7: 1} and factorint(126) == {2: 1, 3: 2, 7: 1}, "84, 126")
ok(Fraction(84, 126) == Fraction(2, 3), "84/126 = 2/3")
ok(gcd(84, 126) == 42 and 84 // 42 == 2 and 126 // 42 == 3, "bouquets 42 (2 roses, 3 tulipes)")
ok(factorint(360) == {2: 3, 3: 2, 5: 1}, "360 = 2^3 3^2 5")
ok(360 == 2 * 180 and 180 == 2 * 90 and 90 == 2 * 45 and 45 == 3 * 15 and 15 == 3 * 5, "arbre 360")
pr = list(primerange(1, 101))
ok(len(pr) == 25 and pr[-1] == 97, "25 premiers < 100")
ok(7**2 < 100 < 11**2, "crible : 2, 3, 5, 7 suffisent")

# ---------------- 1923 algorithmique
def est_multiple(a, b):
    return a % b == 0
def est_premier(n, trace=None):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if trace is not None:
            trace.append(i)
        if n % i == 0:
            return False
        i = i + 1
    return True
ok(est_multiple(84, 7) and 84 == 7 * 12, "1923 Q1")
ok(not est_multiple(85, 7) and 85 == 7 * 12 + 1, "1923 Q2")
ok(est_multiple(0, 5), "1923 Q3")
t = []; r = est_premier(49, t)
ok(r is False and t == [2, 3, 4, 5, 6, 7], "1923 Q4 i = 2..7")
t = []; r = est_premier(97, t)
ok(r is True and t == [2, 3, 4, 5, 6, 7, 8, 9], "1923 Q5 i = 2..9")

# ---------------- 1916 division euclidienne
ok(divmod(125, 7) == (17, 6), "1916 Q1")
ok(156 % 12 == 0 and 156 == 12 * 13, "1916 Q2")
ok(divmod(83, 9) == (9, 2), "1916 Q3")
ok(max(m for m in range(0, 71, 8)) == 64, "1916 Q4")
ok(divmod(2024, 9) == (224, 8) and sum(map(int, "2024")) == 8, "1916 Q5")

# ---------------- 1915
ok(72 == 9 * 8 and 65 == 8 * 8 + 1, "1915 Q1-2")
ok(divisors(24) == [1, 2, 3, 4, 6, 8, 12, 24], "1915 Q3")
ok(54 == 6 * 9 and 203 == 7 * 29, "1915 Q4-5")

# ---------------- 1918 critères
ok([d for d in (2, 3, 4, 5, 6, 9, 10) if 7290 % d == 0] == [2, 3, 5, 6, 9, 10], "1918 Q1")
ok(1428 % 4 == 0 and 1428 % 6 == 0 and 1428 % 9 != 0, "1918 Q2")
ok([a for a in range(10) if (240 + a) % 3 == 0] == [0, 3, 6, 9], "1918 Q3")
ok([b for b in range(10) if (305 + 10 * b) % 9 == 0] == [1], "1918 Q4")
ok(all(5040 % d == 0 for d in (4, 6, 10)), "1918 Q5")

# ---------------- 1920 décompositions
ok(factorint(84) == {2: 2, 3: 1, 7: 1}, "1920 Q1")
ok(factorint(120) == {2: 3, 3: 1, 5: 1} and 120 == 2 * 60 and 60 == 2 * 30 and 30 == 2 * 15, "1920 Q2 (arbre)")
ok(factorint(45) == {3: 2, 5: 1} and factorint(210) == {2: 1, 3: 1, 5: 1, 7: 1}, "1920 Q3-4")
ok([d for d in divisors(60) if d > 10] == [12, 15, 20, 30, 60], "1920 Q5")

# ---------------- 1924 preuves
couples = [(a, b) for a in range(10) for b in range(10) if (7020 + 100 * a + b) % 12 == 0]
ok(sorted(couples) == sorted([(0, 0), (3, 0), (6, 0), (9, 0), (2, 4), (5, 4), (8, 4), (1, 8), (4, 8), (7, 8)]), "1924 Q3 (10 couples)")
ok(sorted(7020 + 100 * a + b for a, b in couples) == [7020, 7128, 7224, 7320, 7428, 7524, 7620, 7728, 7824, 7920], "1924 Q3 nombres")
ok(sum(d for d in divisors(6) if d < 6) == 6, "1924 Q2")
ok(all((n * n - 1) % 8 == 0 for n in range(1, 2000, 4)), "1924 Q4")
ok(all((n * n) % 9 == 0 for n in range(0, 3000, 3)), "1924 Q5")

# ---------------- 1919 primalité
ok(isprime(29) and 5**2 <= 29 < 6**2, "1919 Q1")
ok(91 == 7 * 13, "1919 Q2")
ok(isprime(97) and divmod(97, 7) == (13, 6), "1919 Q3")
ok([n for n in (21, 23, 25, 29, 31) if isprime(n)] == [23, 29, 31], "1919 Q4")
ok(121 == 11**2, "1919 Q5")

# ---------------- 1917 parité
ok(38 == 2 * 19 and 57 == 2 * 28 + 1, "1917 Q1-2")
ok(all((2 * k + 1)**2 == 2 * (2 * k * k + 2 * k) + 1 for k in range(-50, 50)), "1917 Q5")

# ---------------- 1921 PGCD
for (a, b, f) in ((84, 126, Fraction(2, 3)), (45, 60, Fraction(3, 4)), (150, 210, Fraction(5, 7)), (168, 252, Fraction(2, 3))):
    ok(Fraction(a, b) == f, f"1921 {a}/{b} = {f}")
ok(gcd(84, 126) == 42 and gcd(45, 60) == 15 and gcd(150, 210) == 30 and gcd(168, 252) == 84, "1921 PGCD")
ok(gcd(72, 120) == 24 and factorint(72) == {2: 3, 3: 2}, "1921 Q3")
ok(factorint(150) == {2: 1, 3: 1, 5: 2} and factorint(168) == {2: 3, 3: 1, 7: 1} and factorint(252) == {2: 2, 3: 2, 7: 1}, "1921 décompositions")

# ---------------- 1922 PPCM
ok(lcm(12, 18) == 36 and lcm(45, 60) == 180, "1922 Q1-2")
ok(min(n for n in range(201, 1000) if n % 9 == 0 and n % 14 == 0) == 252 and lcm(9, 14) == 126, "1922 Q3")
ok(Fraction(1, 6) + Fraction(1, 8) == Fraction(7, 24) and lcm(6, 8) == 24, "1922 Q4")
ok(lcm(6, 8, 9) == 72, "1922 Q5")

# ---------------- 1925 kermesse
ok(gcd(84, 126) == 42, "1925 Q1-2")
communs = [t for t in range(0, 181) if t % 12 == 0 and t % 18 == 0]
ok(communs == [0, 36, 72, 108, 144, 180], "1925 Q3-4 (6 clignotements)")
ok(min(n for n in range(100, 1000) if n % 90 == 0) == 180, "1925 Q5")
# ================= finition 2026-11-02
import sympy as sp

# 1914 (réécrit) : somme de deux multiples
ok(35 == 7 * 5 and 56 == 7 * 8 and 35 + 56 == 91 == 7 * 13, "1914 Q1")
k, kp, a = sp.symbols("k kp a", integer=True)
ok(sp.expand(7 * k + 7 * kp - 7 * (k + kp)) == 0, "1914 Q2")
ok(sp.expand(k * a + kp * a - (k + kp) * a) == 0, "1914 Q3")
ok(7007 == 7 * 1001 and 140 == 7 * 20 and 7007 + 140 == 7147 == 7 * 1021 and 7007 - 140 == 6867 == 7 * 981, "1914 Q4")
ok((3 + 4) % 7 == 0 and 3 % 7 and 4 % 7, "1914 Q5 contre-exemple")
ok(all((7 * x + 7 * y) % 7 == 0 for x in range(-20, 20) for y in range(-20, 20)), "1914 balayage")


# 1923 Q6 et cours : fonction plus_grand_multiple (exécutée)
def plus_grand_multiple(a, b):
    m = 0
    while m + a <= b:
        m = m + a
    return m


ok(plus_grand_multiple(8, 70) == 64 and 8 * 8 == 64 and 8 * 9 == 72 > 70, "1923 Q6 / 1916 Q4 figure")
ok(all(plus_grand_multiple(a_, b_) == (b_ // a_) * a_ for a_ in range(1, 15) for b_ in range(0, 120)), "plus_grand_multiple")
vals = []
m = 0
while m + 8 <= 70:
    vals.append(m)
    m += 8
vals.append(m)
ok(vals == [0, 8, 16, 24, 32, 40, 48, 56, 64], "1923 Q6 valeurs de m")

# 1915 Q3 (figure) : rectangles de 24
ok(divisors(24) == [1, 2, 3, 4, 6, 8, 12, 24] and all(24 == l * h for l, h in [(24, 1), (12, 2), (8, 3), (6, 4)]), "1915 figure")

# 1919 (figure) : crible 20-39
ok([n for n in range(20, 40) if isprime(n)] == [23, 29, 31, 37], "premiers 20-39")
ok(all(any(n % p == 0 for p in (2, 3, 5)) for n in range(20, 40) if not isprime(n)), "composés 20-39 : 2, 3 ou 5")
ok(7 ** 2 == 49 > 39, "inutile de tester 7")

# 1917 (figure) et cours
ok(7 == 2 * 3 + 1 and 5 == 2 * 2 + 1 and 12 == 2 * 6 and 8 == 2 * 4 and 9 == 2 * 4 + 1, "parité figures")

# 1922 Q2 (figure) : feux 45 s / 60 s
ok([t for t in range(1, 400) if t % 45 == 0 and t % 60 == 0][0] == 180 == lcm(45, 60), "feux 180 s")
ok([t for t in range(0, 181) if t % 45 == 0] == [0, 45, 90, 135, 180] and [t for t in range(0, 181) if t % 60 == 0] == [0, 60, 120, 180], "frise feux")

print("Tout est juste.")
