# -*- coding: utf-8 -*-
"""Vérification de tous les résultats numériques de la notion 174 (Seconde, statistiques)."""
from fractions import Fraction as F
from math import ceil, sqrt

def ok(cond, msg):
    assert cond, msg
    print("ok :", msg)

def rangee(eff):
    """eff = {valeur: effectif} -> liste rangée"""
    L = []
    for v in sorted(eff):
        L += [v] * eff[v]
    return L

def mediane(L):
    L = sorted(L); n = len(L)
    return L[n // 2] if n % 2 else (L[n // 2 - 1] + L[n // 2]) / 2

def q1(L):
    L = sorted(L); return L[ceil(len(L) / 4) - 1]

def q3(L):
    L = sorted(L); return L[ceil(3 * len(L) / 4) - 1]

def moy(L):
    return sum(F(x) for x in L) / len(L)

def ecart_type(L):
    m = moy(L)
    return sqrt(sum((F(x) - m) ** 2 for x in L) / len(L))

# ---------------- cours
S = [4, 7, 8, 9, 10, 11, 12, 12, 14, 15, 19]
ok(mediane(S) == 11 and q1(S) == 8 and q3(S) == 14, "cours : Me 11, Q1 8, Q3 14")
ok(moy(S) == 11 and sum((x - 11) ** 2 for x in S) == 170, "cours : moyenne 11, somme des carrés 170")
ok(round(ecart_type(S), 1) == 3.9, "cours : sigma ~ 3,9")
ok(F(24 + 50 + 96 + 60, 20) == F(23, 2), "cours : moyenne pondérée 11,5")
ok(abs(1.05 * 1.03 - 1.0815) < 1e-12 and abs(1.1 * 0.9 - 0.99) < 1e-12, "cours : 1,0815 et 0,99")
S90 = S[:-1] + [90]
ok(mediane(S90) == 11 and moy(S90) == F(192, 11) and round(192 / 11, 1) == 17.5, "cours : 19 -> 90, Me 11, moyenne ~ 17,5")
ok(F(12, 80) == F(15, 100), "cours : 80 -> 92, +15 %")
A = [9, 10, 10, 11, 11, 11, 12, 12, 13]; B = [4, 6, 8, 10, 11, 13, 14, 16, 17]
ok(moy(A) == 11 and moy(B) == 11, "figure dispersion : même moyenne 11")
ok(round(ecart_type(A), 1) == 1.2 and round(ecart_type(B), 1) == 4.2, "figure dispersion : sigma 1,2 et 4,2")
ok(F(1, 1) / F(125, 100) == F(4, 5), "réciproque de +25 % : -20 %")
ok(F(60, 100) * F(45, 100) == F(27, 100), "cours : 45 % de 60 % = 27 %")

# ---------------- 1991 Python
def statistiques(L):
    n = len(L); m = sum(L) / n
    V = 0
    for x in L:
        V = V + (x - m) ** 2
    V = V / n; s = V ** 0.5
    a = m - 2 * s; b = m + 2 * s
    c = 0
    for x in L:
        if a <= x <= b:
            c = c + 1
    return m, s, c / n, a, b
m, s, p, a, b = statistiques([9, 9, 11, 11]); ok((m, s, p) == (10, 1, 1), "1991 : (10, 1, 1)")
m, s, p, a, b = statistiques([0, 0, 0, 0, 0, 10])
ok(abs(s - 5 * sqrt(5) / 3) < 1e-12 and abs(p - 5 / 6) < 1e-12, "1991/1990 : s = 5V5/3, prop 5/6")
ok(round(a, 2) == -5.79 and round(b, 2) == 9.12 and round(s, 2) == 3.73, "1991/1990 : intervalle [-5,79 ; 9,12], s ~ 3,73")
ok(F(10, 6) == F(5, 3) and moy([0] * 5 + [10]) == F(5, 3), "1991 : m = 5/3")
ok(sum((F(x) - F(5, 3)) ** 2 for x in [0] * 5 + [10]) / 6 == F(125, 9), "1991 : V = 125/9")
ok(ecart_type([9, 9, 11, 11]) == 1, "1991 Q3 : s = 1")

# ---------------- 1988
ok(abs(1.8 * 18 + 32 - 64.4) < 1e-12 and 9 + 4 == 13 and 0.8 * 50 == 40, "1988 : 64,4 ; 13 ; 40")
# ---------------- 1976 / 1975
ok(F(40, 100) * F(25, 100) == F(1, 10) and F(60, 100) * F(30, 100) == F(18, 100), "1976 : 10 % et 18 %")
ok(F(15, 100) * F(20, 100) * 500 == 15 and F(55, 100) * F(40, 100) == F(22, 100), "1976 : 15 cadres ; 22 %")
ok(F(12, 100) / F(40, 100) == F(3, 10), "1976 : 30 %")
ok(F(7, 28) == F(1, 4) and F(18, 100) * 250 == 45 and F(312, 1200) == F(13, 50), "1975 : 25 %, 45, 26 %")
ok(F(75, 1000) * 2000 == 150 and F(12, 80) == F(3, 20), "1975 : 150 ; 3/20")

# ---------------- 1979 (N = 50)
fr = [F(12, 100), F(28, 100), F(30, 100), F(20, 100), F(10, 100)]
eff = [f * 50 for f in fr]
ok(eff == [6, 14, 15, 10, 5] and sum(eff) == 50, "1979 : effectifs 6, 14, 15, 10, 5")
ok(fr[0] + fr[1] == F(40, 100) and fr[3] + fr[4] == F(30, 100), "1979 : moins de 4 min 40 %, au moins 6 min 30 %")
ok(sum(e * c for e, c in zip(eff, [1, 3, 5, 7, 9])) / 50 == F(476, 100), "1979 : moyenne approchée 238/50 = 4,76")

# ---------------- 1981
s1 = [3, 4, 6, 9, 12, 13, 18, 20]; s2 = [14, 2, 9, 5, 18, 11, 7, 3, 10]
s3 = [6, 7, 8, 9, 10, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20]
ok((mediane(s1), q1(s1), q3(s1)) == (10.5, 4, 13), "1981 : série 1")
ok((mediane(s2), q1(s2), q3(s2)) == (9, 5, 11), "1981 : série 2")
ok((mediane(s3), q1(s3), q3(s3)) == (13, 9, 17), "1981 : série 3")
ok((min(s1), max(s1), min(s2), max(s2), min(s3), max(s3)) == (3, 20, 2, 18, 6, 20), "1981 : extrêmes")

# ---------------- 1980
sA = [0, 1, 2, 2, 3, 4, 1, 0, 5, 2, 3, 2, 1, 4, 2, 3, 2, 4, 5, 1, 4, 3, 1, 2, 0, 3, 2, 4, 5, 0]
cA = {v: sA.count(v) for v in range(6)}
ok(cA == {0: 4, 1: 5, 2: 8, 3: 5, 4: 5, 5: 3} and len(sA) == 30, "1980 : effectifs série A 4,5,8,5,5,3")
ok(sum(sA) == 71 and round(float(moy(sA)), 2) == 2.37, "1980 : moyenne A 71/30 ~ 2,37")
ok((mediane(sA), q1(sA), q3(sA)) == (2, 1, 4), "1980 : A Me 2, Q1 1, Q3 4")
LB = rangee({8: 5, 10: 12, 12: 16, 14: 12, 16: 5})
ok(moy(LB) == 12 and (mediane(LB), q1(LB), q3(LB)) == (12, 10, 14), "1980 : B moyenne 12, Me 12, Q1 10, Q3 14")
ok(round(ecart_type(LB), 2) == 2.26 and sum((x - 12) ** 2 for x in LB) == 256, "1980 : écart type B = racine(5,12) ~ 2,26")
ok(round(ecart_type(sA), 2) == 1.52, "1980 : écart type A ~ 1,52")

# ---------------- 1987
ok(F(2 * 8 + 6 * 10 + 7 * 12 + 5 * 15, 20) == F(1175, 100), "1987 : 11,75")
ok(abs((3 * 2 + 5 * 1.5 + 2 * 3) / 10 - 1.95) < 1e-12, "1987 : 1,95 €/kg")
ok(F(110, 9) == F(4 * 12 + 3 * 14 + 2 * 10, 9) and round(110 / 9, 2) == 12.22, "1987 : 110/9")
ok((5 * 10 + 5 * 14) / 10 == 12 and F(46, 40) == F(115, 100), "1987 : x = 5 ; 1,15")

# ---------------- 1989
t1 = [5, 7, 8, 9, 10, 10, 11, 12, 14, 15, 18, 20]; t2 = [2, 3, 3, 4, 5, 6, 7, 8, 8, 9]
ok((q1(t1), q3(t1)) == (8, 14) and (q1(t2), q3(t2)) == (3, 8), "1989 : quartiles")
ok(mediane(t1) == 10.5 and mediane(t2) == 5.5, "1989 : médianes 10,5 et 5,5")

# ---------------- 1978
e78 = [12, 28, 44, 50, 34, 12]
cum = [sum(e78[:i + 1]) for i in range(6)]
ok(cum == [12, 40, 84, 134, 168, 180], "1978 : cumuls")
ok(round(46 / 180 * 100, 1) == 25.6, "1978 : 25,6 %")
ok(sum(e * c for e, c in zip(e78, [1, 3, 5, 7, 9, 11])) == 1104 and round(1104 / 180, 2) == 6.13, "1978 : moyenne ~ 6,13")
ok(cum[2] < 90 and cum[3] >= 91, "1978 : rangs 90 et 91 dans la classe [6 ; 8[")
ok(round(40 / 180 * 100, 1) == 22.2, "1978 : moins de 4 h : 22,2 %")

# ---------------- 1977
m77 = [248, 248.5, 249, 249.5, 250, 250.5, 251, 251.5, 252]; n77 = [2, 8, 18, 34, 52, 40, 26, 14, 6]
ok(sum(n77) == 200, "1977 : N = 200")
f77 = [F(n, 200) for n in n77]
ok([float(f) for f in f77] == [0.01, 0.04, 0.09, 0.17, 0.26, 0.20, 0.13, 0.07, 0.03], "1977 : fréquences")
c77 = [sum(n77[:i + 1]) for i in range(9)]
ok(c77 == [2, 10, 28, 62, 114, 154, 180, 194, 200], "1977 : effectifs cumulés croissants")
L77 = []
for v, n in zip(m77, n77):
    L77 += [v] * n
ok((mediane(L77), q1(L77), q3(L77)) == (250, 249.5, 250.5), "1977 : Me 250, Q1 249,5, Q3 250,5")
ok(sum((F(str(v)) - 250) * n for v, n in zip(m77, n77)) == 28, "1977 : somme des n_i(x_i - 250) = 28")
ok(sum(F(str(v)) * n for v, n in zip(m77, n77)) / 200 == F("250.14"), "1977 : moyenne 250,14 (linéarité)")
ok([F(str(v)) - 250 for v in m77] == [F(x, 2) for x in range(-4, 5)], "1977 : écarts -2 ; -1,5 ; … ; 2")
ok(sum(F(x, 2) * n for x, n in zip(range(-4, 5), n77)) == 28, "1977 : 2 x (-4 -12 -18 -17 + 0 + 20 + 26 + 21 + 12)/… = 28")
ok(c77[3] == 62 and F(62, 200) == F(31, 100), "1977 : moins de 250 g : 31 %")
ok(F(sum(n77[2:7]), 200) == F(85, 100), "1977 : entre 249 et 251 g : 85 %")

# ---------------- 1984 / 1986 / 1985
ok(F(12, 80) == F(15, 100) and F(-150, 1500) == F(-1, 10) and F(260, 1) / F(13, 10) == 200, "1984")
ok(F(1) / F(125, 100) - 1 == F(-1, 5) and F(1) / F(7, 10) - 1 == F(3, 7), "1986 : -20 % ; 3/7")
ok(round(float(F(3, 7)) * 100, 1) == 42.9 and round(float(F(-3, 28)) * 100, 1) == -10.7, "1986 : 42,9 % ; -10,7 %")
ok(F(420, 500) == F(84, 100) and F(1) / F(84, 100) - 1 == F(4, 21) and round(400 / 21, 1) == 19.0, "1986 : 19,0 %")
ok(F(12, 10) * F(85, 100) == F(102, 100) and F(9, 10) * F(11, 10) == F(99, 100), "1985 : 1,02 ; 0,99")
ok(F(105, 100) ** 3 == F("1.157625") and 1500 * F("1.157625") == F("1736.4375"), "1985 : 1736,44")
ok(F(7, 10) * F(8, 10) == F(56, 100) and F(108, 100) * F(112, 100) == F("1.2096"), "1985 : -44 % ; 20,96 %")

# ---------------- 1982 (28 notes, Q1 = 10, Q3 = 15)
ok(ceil(28 / 4) == 7 and ceil(3 * 28 / 4) == 21 and 21 - 6 >= 14, "1982 : au moins 15 notes sur 28 dans [10 ; 15]")

# ---------------- 1983
eff83 = {5: 1, 7: 2, 8: 3, 9: 3, 10: 4, 11: 5, 12: 6, 13: 4, 14: 2, 15: 1, 16: 1}
L83 = rangee(eff83)
ok(len(L83) == 32 and sum(L83) == 348 and moy(L83) == F(10875, 1000), "1983 : N 32, somme 348, moyenne 10,875")
ok((mediane(L83), q1(L83), q3(L83)) == (11, 9, 12), "1983 : Me 11, Q1 9, Q3 12")
ok(round(21 / 32 * 100, 1) == 65.6 and 6 / 32 == 0.1875, "1983 : 65,6 % ; 18,75 %")
ok(32 * F("10.875") == 348 and 30 * F("11.65") == F("349.5"), "1983 Q5 : sommes 348 et 349,5")
ok((348 + F("349.5")) / 62 == F("11.25"), "1983 Q5 : moyenne des 62 élèves 11,25")
ok((F("10.875") + F("11.65")) / 2 == F("11.2625") and F("22.525") / 2 == F("11.2625"), "1983 Q6 : 11,2625 != 11,25")
c83 = []
t = 0
for v in sorted(eff83):
    t += eff83[v]; c83.append(t)
ok(c83 == [1, 3, 6, 9, 13, 18, 24, 28, 30, 31, 32], "1983 : effectifs cumulés")

# ---------------- 1992
ok(0.35 * 800 == 280 and 0.4 * 280 == 112 and abs(0.6 * 520 - 312) < 1e-9, "1992 : 280, 112, 312")
rec = 112 * 6 * F(9, 10) + 168 * 6 + 312 * 9 * F(9, 10) + 208 * 9
ok(rec == 6012 and F(6012, 800) == F("7.515") and rec * F(105, 100) == F("6312.6"), "1992 : 6012 ; 7,515 ; 6312,6")

# ---------------- nouveau-1 : salaires
sal = [1500, 1550, 1600, 1600, 1700, 1750, 1800, 1900, 2000, 2400, 6400]
ok(sum(sal) == 24200 and moy(sal) == 2200 and mediane(sal) == 1750, "nouveau-1 : moyenne 2200, médiane 1750")
sal2 = sal[:-1] + [9700]
ok(moy(sal2) == 2500 and mediane(sal2) == 1750, "nouveau-1 : après hausse, moyenne 2500, médiane 1750")
ok(round(2500 / 2200 * 100 - 100, 1) == 13.6 and F(9700, 6400) - 1 == F(33, 64), "nouveau-1 : +13,6 % ; hausse dirigeant")
ok(round(float(F(33, 64)) * 100, 1) == 51.6, "nouveau-1 : hausse du dirigeant 51,6 %")
ok((q1(sal), q3(sal), q1(sal2), q3(sal2)) == (1600, 2000, 1600, 2000), "nouveau-1 : Q1 1600, Q3 2000 (inchangés)")
ok(sum(1 for x in sal if x < 2200) == 9, "nouveau-1 : 9 salariés sur 11 sous la moyenne")

# ---------------- nouveau-2 : deux groupes
GA = rangee({8: 2, 10: 3, 12: 3, 14: 2}); GB = rangee({5: 2, 8: 2, 12: 2, 14: 2, 16: 2})
ok(moy(GA) == 11 and moy(GB) == 11, "nouveau-2 : moyennes 11 et 11")
ok(sum((x - 11) ** 2 for x in GA) == 42 and sum((x - 11) ** 2 for x in GB) == 160, "nouveau-2 : sommes 42 et 160")
ok(round(ecart_type(GA), 2) == 2.05 and ecart_type(GB) == 4, "nouveau-2 : sA ~ 2,05 ; sB = 4")
ok((mediane(GA), q1(GA), q3(GA)) == (11, 10, 12), "nouveau-2 : A Me 11, Q1 10, Q3 12")
ok((mediane(GB), q1(GB), q3(GB)) == (12, 8, 14), "nouveau-2 : B Me 12, Q1 8, Q3 14")
ok(sum(1 for x in GB if x >= 12) == 6 and sum(1 for x in GA if x >= 12) == 5, "nouveau-2 : notes >= 12 : 6 et 5")
# ================= Finition 2026-11-02
import re
import sys
from pathlib import Path
import sympy as sp

ICI = Path(__file__).parent
EX = (ICI / "exercices.txt").read_text(encoding="utf-8")

# 1991 : le code de l'énoncé est exécuté tel quel
code = re.search(r"Id: 1991\n.*?```python\n(.*?)```", EX, re.S).group(1)
env = {}
exec(code, env)
ok(env["stats"]([9, 9, 11, 11]) == (10.0, 1.0, 1.0), "1991 Q3 : stats([9, 9, 11, 11]) renvoie (10.0, 1.0, 1.0)")
m, s, p = env["stats"]([0, 0, 0, 0, 0, 10])
ok((round(m, 2), round(s, 2), round(p, 2)) == (1.67, 3.73, 0.83), "1991 Q4 : (1,67 ; 3,73 ; 0,83) avec le vrai code")

# 1990 réécrit : températures
A90 = [22, 23, 23, 24, 24, 25, 25, 26]
B90 = [18, 20, 22, 24, 24, 26, 28, 30]
ok(sum(A90) == 192 and sum(B90) == 192 and moy(A90) == 24 and moy(B90) == 24, "1990 Q1 : sommes 192, moyennes 24")
ok(sum((x - 24) ** 2 for x in A90) == 12 and sum((x - 24) ** 2 for x in B90) == 112, "1990 Q2 : sommes des carrés 12 et 112")
ok(sp.sqrt(sp.Rational(12, 8)) == sp.sqrt(sp.Rational(3, 2)) and round(float(sp.sqrt(sp.Rational(3, 2))), 2) == 1.22, "1990 Q2 : sigma_A = racine(1,5) ~ 1,22")
ok(sp.sqrt(sp.Rational(112, 8)) == sp.sqrt(14) and round(float(sp.sqrt(14)), 2) == 3.74, "1990 Q2 : sigma_B = racine(14) ~ 3,74")
B2 = B90[:-1] + [42]
ok(sum(B2) == 204 and moy(B2) == F(51, 2) and mediane(B2) == 24, "1990 Q4 : moyenne 25,5 ; médiane 24")
ok(sum((F(x) - F(51, 2)) ** 2 for x in B2) == 382, "1990 Q4 : somme des carrés 382")
sig = sp.sqrt(sp.Rational(382, 8))
ok(round(float(sig), 2) == 6.91 and sp.Rational(382, 8) == sp.Rational(4775, 100), "1990 Q4 : sigma' = racine(47,75) ~ 6,91")
ok(round(float(2 * sig), 2) == 13.82 and round(float(25.5 - 2 * sig), 2) == 11.68 and round(float(25.5 + 2 * sig), 2) == 39.32,
   "1990 Q5 : bornes 11,68 et 39,32")
ok(sum(1 for x in B2 if 25.5 - 2 * float(sig) <= x <= 25.5 + 2 * float(sig)) == 7 and F(7, 8) == F(875, 1000), "1990 Q5 : 7/8 = 87,5 %")
ok(all([(x - 25.5) ** 2 for x in B2][i] == v for i, v in enumerate([56.25, 30.25, 12.25, 2.25, 2.25, 0.25, 6.25, 272.25])), "1990 Q4 : carrés des écarts")

# 1987 : erreur fréquente
ok(round((2 + 1.5 + 3) / 3, 2) == 2.17, "1987 Q2 : moyenne non pondérée 2,17 (erreur)")

# 1985 Q3 : chaîne du salaire (figure)
ok(1500 * F(105, 100) == 1575 and 1575 * F(105, 100) == F("1653.75") and round(float(F("1653.75") * F(105, 100)), 2) == 1736.44,
   "1985 : 1 575 ; 1 653,75 ; 1 736,44")
ok(F(105, 100) ** 3 == F("1.157625"), "1985 : 1,05^3 = 1,157625")
# 1986 Q2 : figure
ok(100 * F(7, 10) == 70 and 70 * F(10, 7) == 100 and round(float(F(3, 7)) * 100, 1) == 42.9, "1986 : 100 -> 70 -> 100, +42,9 %")

# ---------------- figures : les données dessinées sont celles des énoncés
sys.path.insert(0, str(ICI / "figures"))
import figures as FIG  # noqa: E402
ok("e1983_boite" in FIG.FIGURES and len(L83) == 32, "figures : 1983, 32 notes")
P89 = [5, 7, 8, 9, 10, 10, 11, 12, 14, 15, 18, 20]
ok((min(P89), q1(P89), mediane(P89), q3(P89), max(P89)) == (5, 8, 10.5, 14, 20), "figure 1989 : 5 ; 8 ; 10,5 ; 14 ; 20")
ok((q1(L83), mediane(L83), q3(L83), min(L83), max(L83)) == (9, 11, 12, 5, 16), "figure 1983 : 5 ; 9 ; 11 ; 12 ; 16")
ok(F(3, 10) * F(4, 10) == F(12, 100) and F(25, 100) * F(40, 100) == F(10, 100), "figures emboîtées : 12 % et 10 %")
for cm, t in ((0.8, -20), (1.15, 15), (1.25, 25), (0.88, -12), (0.90, -10), (1.08, 8)):
    ok(round((cm - 1) * 100) == t, f"axe des coefficients : {cm} <-> {t} %")
ok(F(1, 1) * 1.20 * 0.85 == 1.02 or abs(1.20 * 0.85 - 1.02) < 1e-12, "1985 Q1 : 1,20 x 0,85 = 1,02")
ok(sum([1500, 1550, 1600, 1600, 1700, 1750, 1800, 1900, 2000, 2400]) + 6400 == 24200, "figure 3758 : 24 200")
print("TOUT EST JUSTE")
