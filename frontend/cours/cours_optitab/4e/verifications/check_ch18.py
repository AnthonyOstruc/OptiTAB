# -*- coding: utf-8 -*-
"""Contrôles du chapitre 18 (algorithmique et programmation) — 4ème.
Les scripts des figures sont ré-exécutés en Python pour vérifier chaque résultat annoncé."""
import random
import sys
from math import sqrt, ceil, log2
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "graphe"))
from scratch4e import Tortue  # noqa: E402

r = lambda v, n=2: round(v + 1e-9, n)  # noqa: E731


def poly(n, c, x=0, y=0):
    t = Tortue(x, y)
    t.stylo = True
    for _ in range(n):
        t.avancer(c)
        t.horaire(360 / n)
    return t


# D1
t = poly(4, 100)
pts = [b for a, b in t.traits]
assert [(r(x), r(y)) for x, y in pts] == [(100, 0), (100, -100), (0, -100), (0, 0)] and 4 * 100 == 400
assert 360 / 3 == 120 and 360 / 6 == 60
# D2
prog = lambda x: x * 3 - 5  # noqa: E731
assert prog(4) == 7 and prog(-2) == -11 and prog(0) == -5 and prog(5) == 10
# D3
c = s = 0
trace = []
for _ in range(5):
    c += 1
    s += c
    trace.append((c, s))
assert trace == [(1, 1), (2, 3), (3, 6), (4, 10), (5, 15)] and sum(range(1, 11)) == 55 and sum(range(1, 101)) == 5050
# D4
age = lambda a: "majeur" if a > 17 else "mineur"  # noqa: E731
assert age(15) == "mineur" and age(18) == "majeur" and age(17) == "mineur"
# D5
A, C, B = (-100, 0), (0, 100), (100, 0)
d2 = lambda P, Q: (P[0] - Q[0]) ** 2 + (P[1] - Q[1]) ** 2  # noqa: E731
assert d2(A, B) == 200 ** 2 and d2(A, C) == 20000 == d2(B, C) and r(sqrt(20000), 1) == 141.4
assert d2(A, C) + d2(B, C) == d2(A, B) and 200 * 100 / 2 == 10000
# D6
n, e, suite = 1, 0, []
while not n > 100:
    n *= 2
    e += 1
    suite.append(n)
assert suite == [2, 4, 8, 16, 32, 64, 128] and e == 7
n, e = 1, 0
while not n > 1000:
    n *= 2
    e += 1
assert (n, e) == (1024, 10)
# D7
t = poly(3, 100)
assert r(t.x) == 0 and r(t.y) == 0 and r(t.o % 360) == 90

# E1
assert [360 / k for k in (5, 6, 8)] == [72, 60, 45] and 5 * 80 == 400 and 36 * 10 == 360 and 180 - 72 == 108
t = poly(36, 10)
assert r(t.x) == 0 and r(t.y) == 0
# E2
t = Tortue(-75, 20)
for _ in range(5):
    t.avancer(150)
    t.horaire(144)
assert r(t.x) == -75 and r(t.y) == 20 and (t.o - 90) == 720 and 5 * 150 == 750 and 180 - 144 == 36
# E3
t = Tortue(-200, 0)
trace = 0
for _ in range(6):
    t.stylo = True
    for _ in range(4):
        t.avancer(30)
        t.antihoraire(90)
    t.stylo = False
    t.avancer(60)
assert len(t.traits) == 24 and r(t.x) == 160 and r(t.y) == 0 and 24 * 30 == 720 and 60 - 30 == 30
# E4
A_ = lambda x: (x + 3) * 2  # noqa: E731
B_ = lambda x: 2 * x + 6  # noqa: E731
C_ = lambda x: x * x + 6  # noqa: E731
assert A_(5) == B_(5) == 16 and A_(-4) == B_(-4) == -2 and all(A_(x) == B_(x) for x in range(-50, 51))
assert C_(2) == A_(2) == 10 and C_(1) == 7 and A_(1) == 8
# E5
random.seed(4)
f = sum(random.randint(1, 6) == 6 for _ in range(100000)) / 100000
assert abs(f - 1 / 6) < 0.01 and r(1 / 6, 3) == 0.167
# E6
t = Tortue()
t.stylo = True
for _ in range(4):
    t.avancer(100)
    t.horaire(60)
assert not (r(t.x) == 0 and r(t.y) == 0) and 180 - 60 == 120
# E7
assert 3 * 2 == 6

# P1
def partie(myst, lo=1, hi=100):
    essais, props = 0, []
    while True:
        g = (lo + hi) // 2
        essais += 1
        props.append(g)
        if g == myst:
            return essais, props
        if g < myst:
            lo = g + 1
        else:
            hi = g - 1


assert partie(81) == (4, [50, 75, 88, 81])
assert max(partie(m)[0] for m in range(1, 101)) == 7 and ceil(log2(100)) == 7 and ceil(log2(1000)) == 10
assert max(partie(m, 1, 1000)[0] for m in range(1, 1001)) == 10
# P2
t = Tortue()
t.stylo = True
L = 10
pos = []
for _ in range(10):
    t.avancer(L)
    t.antihoraire(90)
    L += 10
    pos.append((r(t.x), r(t.y)))
assert pos[:4] == [(10, 0), (10, 20), (-20, 20), (-20, -20)] and pos[-1] == (50, 60) and L == 110
assert sum(range(10, 101, 10)) == 550 and 10 * 90 == 900 and r(sqrt(6100), 1) == 78.1


# P3
def monnaie(s):
    reste, p2 = s, 0
    while not reste < 2:
        reste -= 2
        p2 += 1
    return p2, reste


assert monnaie(7) == (3, 1) and monnaie(10) == (5, 0) and monnaie(1) == (0, 1) and monnaie(15) == (7, 1)
assert (18 // 5, monnaie(18 % 5)) == (3, (1, 1))
# P4
F = lambda c: c * 1.8 + 32  # noqa: E731
assert r(F(0)) == 32 and r(F(100)) == 212 and r(F(37), 1) == 98.6 and r(F(-40)) == -40 and r((50 - 32) / 1.8) == 10
# P5
x = y = 0
for _ in range(3):
    x += 40
    y += 30
assert (x, y) == (120, 90) and sqrt(40 ** 2 + 30 ** 2) == 50 and sqrt(120 ** 2 + 90 ** 2) == 150
for _ in range(2):
    x -= 60
assert (x, y) == (0, 90) and 3 * 70 + 2 * 60 == 330
# P6
vals = [2 * x * x - 3 for x in range(-3, 4)]
assert vals == [15, 5, -1, -3, -1, 5, 15] and min(vals) == -3 and (3 - (-3)) / 0.5 + 1 == 13
# P7
somme7 = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 7)
assert somme7 == 6 and r(1000 / 6, 1) == 166.7 and r(1 / 6, 3) == 0.167
random.seed(7)
f = sum(random.randint(1, 6) + random.randint(1, 6) == 7 for _ in range(100000)) / 100000
assert abs(f - 1 / 6) < 0.01

print("check_ch18 : tous les contrôles passent.")
