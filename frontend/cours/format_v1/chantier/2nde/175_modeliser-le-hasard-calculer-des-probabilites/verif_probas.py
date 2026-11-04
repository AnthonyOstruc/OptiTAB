# -*- coding: utf-8 -*-
"""Vérification (fractions exactes) de tous les résultats de la notion 175."""
from fractions import Fraction as Fr
from itertools import product, permutations

ok = 0


def eq(a, b, msg):
    global ok
    assert a == b, f"{msg} : {a} != {b}"
    ok += 1


# ---------------- cours
eq(5 * Fr(1, 10) + Fr(1, 2), 1, "dé truqué somme")
eq(Fr(1, 10) * 2 + Fr(1, 2), Fr(7, 10), "dé truqué pair")
eq(Fr(8 + 12 - 3, 32), Fr(17, 32), "cartes")
pieces = list(product("PF", repeat=2))
eq(Fr(sum("P" in t for t in pieces), 4), Fr(3, 4), "au moins un pile")
des = list(product(range(1, 7), repeat=2))
eq(Fr(sum(a + b == 7 for a, b in des), 36), Fr(1, 6), "somme 7")
eq(sum(a + b == 2 for a, b in des), 1, "somme 2")
eq(Fr(sum(a == 6 or b == 6 for a, b in des), 36), Fr(11, 36), "au moins un 6")
eq(1 - Fr(25, 36), Fr(11, 36), "au moins un 6 contraire")
eq(Fr(sum(a == b for a, b in des), 36), Fr(1, 6), "double")
E = set(range(1, 11))
A0 = {k for k in E if k % 2 == 0}
B0 = {k for k in E if k >= 7}
eq(A0 & B0, {8, 10}, "cours A∩B")
eq(A0 | B0, {2, 4, 6, 7, 8, 9, 10}, "cours A∪B")
eq(E - A0, {1, 3, 5, 7, 9}, "cours non A")
eq(sum(a != 6 and b != 6 for a, b in des), 25, "aucun 6")
# modèle à partir de fréquences (cours) : punaise
eq(Fr(372, 1000), Fr(93, 250), "punaise")

# ---------------- 2002 simulation
eq(Fr(9, 50), Fr(18, 100), "freq 9/50")
eq(Fr(9, 50) - Fr(1, 6), Fr(1, 75), "écart")

# ---------------- 1994
O = set(range(1, 16))
A = {k for k in O if k % 3 == 0}
B = {k for k in O if k % 2 == 1}
C = {k for k in O if k >= 10}
eq(A, {3, 6, 9, 12, 15}, "A")
eq(B, {1, 3, 5, 7, 9, 11, 13, 15}, "B")
eq(C, {10, 11, 12, 13, 14, 15}, "C")
eq(A & B, {3, 9, 15}, "A∩B")
eq(Fr(len(A & B), 15), Fr(1, 5), "P(A∩B)")
eq(B | C, {1, 3, 5, 7, 9, 10, 11, 12, 13, 14, 15}, "B∪C")
eq(Fr(len(B | C), 15), Fr(11, 15), "P(B∪C)")
eq(Fr(len(B), 15) + Fr(len(C), 15) - Fr(len(B & C), 15), Fr(11, 15), "formule B∪C")
eq(B & C, {11, 13, 15}, "B∩C")
eq(O - C, set(range(1, 10)), "non C")
eq(Fr(9, 15), Fr(3, 5), "P(non C)")
eq(A | C, {3, 6, 9, 10, 11, 12, 13, 14, 15}, "A∪C")
eq(O - (A | C), {1, 2, 4, 5, 7, 8}, "non(A∪C)")
eq(Fr(6, 15), Fr(2, 5), "P(non(A∪C))")

# ---------------- 1993
eq({k for k in range(1, 9) if k % 3 == 0}, {3, 6}, "dé 8")
eq({k for k in range(10) if k % 2 == 0}, {0, 2, 4, 6, 8}, "chiffres pairs")
jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
eq({j for j in jours if j[0] == "m"}, {"mardi", "mercredi"}, "jours m")

# ---------------- 1999 sans remise, dénombrement
urne = ["R1", "R2", "B1", "B2", "B3"]
tir = list(permutations(urne, 2))
eq(len(tir), 20, "20 issues")
typ = lambda t: t[0][0] + t[1][0]
cnt = {k: sum(typ(t) == k for t in tir) for k in ("RR", "RB", "BR", "BB")}
eq(cnt, {"RR": 2, "RB": 6, "BR": 6, "BB": 6}, "comptes")
eq(Fr(2, 20), Fr(1, 10), "RR")
eq(Fr(12, 20), Fr(3, 5), "une de chaque")
eq(1 - Fr(1, 10), Fr(9, 10), "au moins une bleue")
eq(Fr(sum("B" in typ(t) for t in tir), 20), Fr(9, 10), "au moins une bleue direct")
eq(Fr(8, 20), Fr(2, 5), "même couleur")

# ---------------- 1995
eq(Fr(3, 8) + Fr(1, 8), Fr(1, 2), "R∪V")
eq(1 - Fr(4, 8), Fr(1, 2), "non B")

# ---------------- 1997 + 1997 Venn
eq(Fr(52, 120), Fr(13, 30), "P(S)")
eq(Fr(48, 120), Fr(2, 5), "P(G)")
eq(Fr(20, 120), Fr(1, 6), "P(S∩G)")
eq(Fr(52 + 48 - 20, 120), Fr(2, 3), "P(S∪G)")
eq(120 - 80, 40, "ni ni")
eq(Fr(32, 120), Fr(4, 15), "esp seul")
eq(48 - 20, 28, "all seul")
eq(32 + 20 + 28 + 40, 120, "venn total")
eq(Fr(2, 3) + Fr(1, 6), Fr(13, 30) + Fr(2, 5), "relation")
eq(Fr(2, 3) + Fr(1, 6), Fr(5, 6), "5/6")

# ---------------- 1996 roue 1..4
p = {1: Fr(12, 100), 2: Fr(35, 100), 3: Fr(28, 100)}
p[4] = 1 - sum(p.values())
eq(p[4], Fr(25, 100), "p4")
eq(p[1] + p[3], Fr(40, 100), "impair")
eq(1 - p[2], Fr(65, 100), "non 2")
eq(p[2] + p[4], Fr(60, 100), "pair")
eq(1 - (p[1] + p[3]), Fr(60, 100), "pair contraire")

# ---------------- 2001 Q4
eq(Fr(len({3, 6, 9}), 10), Fr(3, 10), "dé 10 mult 3")

# ---------------- 1998 dés 4 et 6
d = list(product(range(1, 5), range(1, 7)))
eq(len(d), 24, "24")
eq(sum(a + b == 5 for a, b in d), 4, "S=5")
eq(Fr(4, 24), Fr(1, 6), "P(S=5)")
eq(sum(a + b >= 8 for a, b in d), 6, "S>=8")
eq(Fr(6, 24), Fr(1, 4), "P(S>=8)")
eq(sum((a + b) % 2 == 0 for a, b in d), 12, "pair")
eq(sum(a != 1 and b != 1 for a, b in d), 15, "aucun 1")
eq(Fr(sum(a == 1 or b == 1 for a, b in d), 24), Fr(3, 8), "au moins un 1")

# ---------------- 2000
eq(Fr(26, 40), Fr(65, 100), "fA")
eq(Fr(108, 200), Fr(54, 100), "fB")

# ---------------- 2003 trois lancers
t3 = list(product("PF", repeat=3))
eq(len(t3), 8, "8 issues")
eq(Fr(sum(t.count("P") == 2 for t in t3), 8), Fr(3, 8), "deux P")
eq(Fr(sum("F" in t for t in t3), 8), Fr(7, 8), "au moins un F")
Cc = {t for t in t3 if len(set(t)) == 1}
D = {t for t in t3 if t[0] == "P"}
eq(Fr(len(Cc), 8), Fr(1, 4), "P(C)")
eq(Fr(len(D), 8), Fr(1, 2), "P(D)")
eq(Fr(len(Cc & D), 8), Fr(1, 8), "C∩D")
eq(Fr(len(Cc | D), 8), Fr(5, 8), "C∪D")
eq(Fr(1, 4) + Fr(1, 2) - Fr(1, 8), Fr(5, 8), "formule")
eq(Fr(56, 200), Fr(28, 100), "fréquence 56/200")
eq(200 * Fr(1, 4), 50, "attendu")

# ---------------- nouveau-1 dé pipé
eff = {1: 120, 2: 110, 3: 130, 4: 115, 5: 125, 6: 400}
eq(sum(eff.values()), 1000, "total 1000")
eq(Fr(eff[6], 1000), Fr(4, 10), "f6")
q = (1 - Fr(4, 10)) / 5
eq(q, Fr(12, 100), "p autre")
eq(2 * q + Fr(4, 10), Fr(64, 100), "P(pair) modèle")
eq(Fr(eff[2] + eff[4] + eff[6], 1000), Fr(625, 1000), "f pair")
eq(Fr(64, 100) - Fr(625, 1000), Fr(15, 1000), "écart pair")

# ---------------- nouveau-2 tableau croisé
FD, FE, GD, GE = 84, 46, 66, 54
eq(FD + FE, 130, "filles")
eq(GD + GE, 120, "garçons")
eq(FD + GD, 150, "DP")
eq(FE + GE, 100, "externes")
eq(Fr(130, 250), Fr(52, 100), "P(F)")
eq(Fr(150, 250), Fr(6, 10), "P(D)")
eq(Fr(84, 250), Fr(336, 1000), "P(F∩D)")
eq(Fr(130 + 150 - 84, 250), Fr(784, 1000), "P(F∪D)")
eq(250 - 54, 196, "196")
eq(Fr(54, 250), Fr(216, 1000), "ni F ni D")
eq(1 - Fr(784, 1000), Fr(216, 1000), "contraire")
eq(Fr(52, 100) + Fr(6, 10), Fr(112, 100), "somme >1")

# ================= Finition 2026-11-02 : figures et code
import random
import re
from pathlib import Path

ICI = Path(__file__).parent
# 1994 : zones du diagramme de Venn (figure e1994_venn)
Om = set(range(1, 16))
A = {k for k in Om if k % 3 == 0}
B = {k for k in Om if k % 2 == 1}
C = {k for k in Om if k >= 10}
eq(A - B - C, {6}, "Venn 1994 : A seul")
eq(B - A - C, {1, 5, 7}, "Venn 1994 : B seul")
eq(C - A - B, {10, 14}, "Venn 1994 : C seul")
eq((A & B) - C, {3, 9}, "Venn 1994 : A et B seulement")
eq((A & C) - B, {12}, "Venn 1994 : A et C seulement")
eq((B & C) - A, {11, 13}, "Venn 1994 : B et C seulement")
eq(A & B & C, {15}, "Venn 1994 : les trois")
eq(Om - A - B - C, {2, 4, 8}, "Venn 1994 : aucun")
# 1998 : cases vertes des deux tableaux
D4 = list(product(range(1, 5), range(1, 7)))
eq(sum(a + b >= 8 for a, b in D4), 6, "1998 Q3 : 6 cases vertes")
eq(sum(a == 1 or b == 1 for a, b in D4), 9, "1998 Q5 : 9 cases vertes")
eq(Fr(9, 24), Fr(3, 8), "1998 Q5 : 3/8")
# cours : au moins un 6 (figure cours_au_moins_un6)
eq(sum(a == 6 or b == 6 for a, b in des), 11, "cours : 11 cases vertes")
# 1996 : roue à l'échelle
eq(Fr(12, 100) + Fr(35, 100) + Fr(28, 100) + Fr(25, 100), 1, "roue 1996 : total 1")
eq(round(360 * 0.35 / (360 * 0.12), 2), 2.92, "roue 1996 : secteur 2 près de 3 fois le secteur 1")
# 2000 : écarts de la figure
eq(Fr(26, 40), Fr(65, 100), "2000 : f_A = 0,65")
eq(Fr(108, 200), Fr(54, 100), "2000 : f_B = 0,54")
eq(Fr(65, 100) - Fr(1, 2), Fr(15, 100), "2000 : écart 0,15")
eq(Fr(54, 100) - Fr(1, 2), Fr(4, 100), "2000 : écart 0,04")
# 3755 : Venn des effectifs
eq(46 + 84 + 66 + 54, 250, "Venn 3755 : 250 élèves")
# 3754 : fréquences du diagramme
eq([Fr(x, 1000) for x in (120, 110, 130, 115, 125, 400)],
   [Fr(12, 100), Fr(11, 100), Fr(13, 100), Fr(115, 1000), Fr(125, 1000), Fr(4, 10)], "3754 : fréquences")
# 2002 : le code de l'énoncé est exécuté (graine fixe)
EX = (ICI / "exercices.txt").read_text(encoding="utf-8")
code = re.search(r"Id: 2002\n.*?```python\n(.*?)```", EX, re.S).group(1)
env = {}
exec(code, env)
random.seed(2002)
f = env["frequence_six"](50)
eq(0 <= f <= 1 and (f * 50) == int(f * 50), True, "2002 : le code s'exécute et renvoie k/50")
eq(Fr(9, 50), Fr(18, 100), "2002 Q4 : 9/50 = 0,18")

print(f"{ok} vérifications : tout est juste.")
