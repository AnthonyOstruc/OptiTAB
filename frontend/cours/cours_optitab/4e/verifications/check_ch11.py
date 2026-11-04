# -*- coding: utf-8 -*-
"""Contrôles du chapitre 11 (probabilités) — 4ème : dénombrements exhaustifs."""
from fractions import Fraction as F
from itertools import product
from math import pi

D = lambda s: F(s)  # noqa: E731
r = lambda v, n=3: round(float(v) + 1e-12, n)  # noqa: E731
P = lambda fav, tot: F(len(fav), len(tot))  # noqa: E731

# urne
urne = ["R"] * 5 + ["B"] * 3 + ["V"] * 2
assert P([b for b in urne if b == "R"], urne) == F(1, 2) and P([b for b in urne if b == "B"], urne) == F(3, 10)
assert P([b for b in urne if b == "V"], urne) == F(1, 5) and F(4, 12) == F(1, 3)
# dé
de = range(1, 7)
assert P([x for x in de if x % 2 == 0], de) == F(1, 2) and P([x for x in de if x % 3 == 0], de) == F(1, 3)
assert P([x for x in de if x >= 4], de) == F(1, 2)
# roue 8
cols = {1: "R", 2: "B", 3: "R", 4: "J", 5: "V", 6: "R", 7: "B", 8: "J"}
S8 = list(cols)
assert P([s for s in S8 if cols[s] == "R"], S8) == F(3, 8) and P([s for s in S8 if cols[s] == "V"], S8) == F(1, 8)
assert P([s for s in S8 if cols[s] == "R" and s % 2 == 0], S8) == F(1, 8)
assert P([s for s in S8 if cols[s] == "R" or s % 2 == 0], S8) == F(3, 4)
# cartes
jeu = list(product(["pique", "coeur", "carreau", "trefle"], ["7", "8", "9", "10", "V", "D", "R", "A"]))
assert len(jeu) == 32 and P([c for c in jeu if c[0] == "coeur"], jeu) == F(1, 4)
assert P([c for c in jeu if c[1] == "A"], jeu) == F(1, 8) and P([c for c in jeu if c[1] in "VDR"], jeu) == F(3, 8)
assert P([c for c in jeu if c[0] in ("coeur", "carreau")], jeu) == F(1, 2)
# D5, D6
assert r(1 / 6, 2) == 0.17 and r(5 / 6, 2) == 0.83 and r(1 / 3, 2) == 0.33
assert 1 - D('0.35') == D('0.65') and 100 - 45 - 30 == 25
# D7
mot = list("PROBABILITE")
assert len(mot) == 11 and mot.count("B") == 2 and sum(1 for c in mot if c in "AEIOUY") == 5
assert sum(1 for c in mot if c in "LIT") == 4

# E1 deux dés
dd = list(product(de, de))
assert len(dd) == 36 and P([d for d in dd if sum(d) == 7], dd) == F(1, 6)
assert P([d for d in dd if sum(d) >= 10], dd) == F(1, 6) and P([d for d in dd if d[0] == d[1]], dd) == F(1, 6)
assert P([d for d in dd if sum(d) % 2 == 0], dd) == F(1, 2)
assert max(range(2, 13), key=lambda s: sum(1 for d in dd if sum(d) == s)) == 7
# E2
assert [F(7, 10), F(56, 100), F(512, 1000), F(4985, 10000)] == [D('0.7'), D('0.56'), D('0.512'), D('0.4985')]
# E3
assert 6 * 3 == 18 and 18 - 10 == 8 and F(4, 18) == F(2, 9) and F(8, 18) == F(4, 9) and F(4, 16) == F(1, 4)
assert F(4 + 10, 18 + 10) == F(1, 2)
# E4
assert 180 + 90 + 60 + 30 == 360 and [F(a, 360) for a in (180, 90, 60, 30)] == [F(1, 2), F(1, 4), F(1, 6), F(1, 12)]
assert 1200 * F(1, 12) == 100
# E5
pp = list(product("PF", "PF"))
assert P([x for x in pp if x.count("P") == 1], pp) == F(1, 2) and P([x for x in pp if "P" in x], pp) == F(3, 4)
assert len(list(product("PF", repeat=3))) == 8
# E6
la = [95, 103, 98, 107, 96, 101]
assert sum(la) == 600 and r(95 / 600) == 0.158 and r(107 / 600) == 0.178 and r(7 / 600) == 0.012
assert F(180, 600) == D('0.3')
# E7
assert P([d for d in dd if (d[0] * d[1]) % 2 == 1], dd) == F(1, 4)

# P1
assert 360 * F(1, 6) == 60 and 360 - 60 * 5 == 60 and 60 * 6 == 360
# P2
assert F(3, 5) == D('0.6') and r(5 / 9) == 0.556 and r(8 / 15) == 0.533 and F(8, 14) == F(4, 7)
assert r(4 / 7) == 0.571 and r((0.6 + 5 / 9) / 2) == 0.578 and F(6, 10) == F(3, 5) and F(3, 6) == F(1, 2)
# P3
assert len(list(product(range(10), repeat=3))) == 1000 and 1000 * 5 == 5000 == 3600 + 23 * 60 + 20
assert 10 * 9 * 8 == 720 and r(50000 / 3600, 1) == 13.9 and r(5000 / 3600, 2) == 1.39
# P4
tr = [60, 65, 70, 75, 80, 150]
assert sum(tr) == 500 and [F(t, 500) for t in tr] == [D('0.12'), D('0.13'), D('0.14'), D('0.15'), D('0.16'), D('0.3')]
assert D('0.13') + D('0.15') + D('0.3') == D('0.58') and 200 * D('0.3') == 60 and round(200 / 6) == 33
# P5
assert F(64, 120) == F(8, 15) and F(75, 120) == F(5, 8) and F(40, 120) == F(1, 3) and F(21, 120) == F(7, 40)
assert F(40, 64) == F(5, 8) and F(64 + 35, 120) == F(33, 40) == 1 - F(21, 120)
# P6
pfc = list(product(["P", "F", "C"], repeat=2))
bat = {("P", "C"), ("C", "F"), ("F", "P")}
assert P([x for x in pfc if x[0] == x[1]], pfc) == F(1, 3) and P([x for x in pfc if x in bat], pfc) == F(1, 3)
# P7
assert r(pi / 16) == 0.196 and r(pi / 4) == 0.785 and r(3 * pi / 16) == 0.589 and r(1 - pi / 4) == 0.215
assert round(200 * pi / 16) == 39

print("check_ch11 : tous les contrôles passent.")
