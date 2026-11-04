# -*- coding: utf-8 -*-
"""Vérification de la notion « Notion de liste » (Terminale) : chaque programme est EXÉCUTÉ.

    python verif_listes.py            # contrôle complet (code de sortie 0 si tout est juste)
    python verif_listes.py --sorties  # affiche la sortie réelle de chaque programme
    python verif_listes.py --remplir  # réécrit les blocs console avec la sortie réelle

1. Programmes (moteur_verif.py) : chaque programme Python du cours, de la fiche
   et de chaque exercice est exécuté ; chaque affichage imprimé est comparé à
   l'affichage réel ; les simulations doivent appeler seed(…) ; largeur des
   lignes de code limitée pour le téléphone ; boucle sans fin détectée.
2. Contrôles mathématiques (sympy, valeurs exactes) des valeurs du texte et des figures.
"""
import math
import sys
from math import comb
from pathlib import Path

import sympy as sp

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import moteur_verif as mv  # noqa: E402

FICHIERS = ["cours_105.txt", "fiche_37.txt", "exercices.txt"]
erreurs = []
n_controles = 0


def chk(cond, msg):
    global n_controles
    n_controles += 1
    if not cond:
        erreurs.append("maths : " + msg)


tot = {"programmes": 0, "affichages": 0, "trous": 0}
for nom in FICHIERS:
    p = ICI / nom
    if not p.exists():
        continue
    e, st = mv.analyser(p, remplir="--remplir" in sys.argv, montrer="--sorties" in sys.argv)
    erreurs += e
    for k in tot:
        tot[k] += st[k]
    print(f"{nom} : {st['programmes']} programme(s) exécuté(s), {st['affichages']} affichage(s) comparé(s), "
          f"{st['trous']} programme(s) à compléter")

R = sp.Rational
COURS = (ICI / "cours_105.txt").read_text(encoding="utf-8")

# ------------------------------------------------------------------ cours
u = [1]
for _ in range(5):
    u.append(2 * u[-1] + 1)
chk(u == [2 ** (k + 1) - 1 for k in range(6)] and sum(u) == 120, "cours : u_n = 2^(n+1) - 1, somme 120")
E = range(1, 21)
A = {x for x in E if x % 2 == 0}
B = {x for x in E if x % 3 == 0}
chk(len(A) == 10 and len(B) == 6 and A & B == {6, 12, 18} and len(A | B) == 13 == len(A) + len(B) - len(A & B),
    "cours : card(A ∪ B) = 10 + 6 - 3 = 13")
v = [sp.Integer(2)]
while v[-1] <= 100:
    v.append(R(3, 2) * v[-1])
chk(len(v) - 1 == 10 and round(float(v[9]), 2) == 76.89 and round(float(v[10]), 2) == 115.33, "cours : seuil 100 → 10")
chk(round(math.log(50) / math.log(1.5), 2) == 9.65, "cours : ln 50 / ln 1,5 ≈ 9,65")
chk(comb(6, 3) * R(1, 2) ** 6 == R(20, 64) == R(3125, 10000), "cours : P(X = 3) = 20/64 = 0,3125")
E_c = [int(l.split()[1]) for l in mv.bloc_console_apres(COURS, "E = [R.count(k)").splitlines()]
chk(sum(E_c) == 10000 and len(E_c) == 7, "cours : effectifs de la simulation (10 000 valeurs)")
chk(comb(4, 2) == 6 and 4 * 3 == 12 and 3 ** 2 == 9, "cours : 9 couples, 12 couples distincts, 6 parties")

# ------------------------------------------------------------------ exercices
# 836 : u0 = 100, u_{n+1} = 0,5 u_n + 20
u = [sp.Integer(100)]
for _ in range(5):
    u.append(R(1, 2) * u[-1] + 20)
chk(u == [100, 70, 55, R(95, 2), R(175, 4), R(335, 8)], "836 : termes 100 ; 70 ; 55 ; 47,5 ; 43,75 ; 41,875")
chk(all(u[k] == 40 + 60 * R(1, 2) ** k for k in range(6)), "836 : u_n = 40 + 60 × 0,5^n")
# 838
E = range(1, 31)
A = {x for x in E if x % 3 == 0}
B = {x for x in E if x % 5 == 0}
chk(len(A) == 10 and len(B) == 6 and A & B == {15, 30} and len(A | B) == 14 and 30 - 14 == 16, "838 : 10, 6, {15, 30}, 14, 16")
chk([d for d in range(1, 37) if 36 % d == 0] == [1, 2, 3, 4, 6, 9, 12, 18, 36], "838 : diviseurs de 36")
# 837
couples = [(a, b) for a in range(1, 6) for b in range(1, 6) if a != b]
chk(len(couples) == 20 and comb(5, 2) == 10 and R(sum(1 for a, b in couples if a + b == 5), 20) == R(1, 5),
    "837 : 20 tirages, 10 parties, P(somme = 5) = 0,2")
chk(R(sum(1 for a in range(1, 6) for b in range(1, 6) if a + b == 5), 25) == R(4, 25), "837 : avec remise 4/25")
# 840 : u0 = 1000, u_{n+1} = 1,02 u_n + 100
u = [sp.Integer(1000)]
for _ in range(10):
    u.append(R(102, 100) * u[-1] + 100)
chk(u[1] == 1120 and u[2] == R(62120, 50), "840 : u1 = 1120, u2 = 1242,4")
chk(all(u[k] == 6000 * R(102, 100) ** k - 5000 for k in range(11)), "840 : u_n = 6000 × 1,02^n - 5000")
chk(min(k for k in range(11) if u[k] >= 2000) == 8 and round(float(u[7]), 2) == 1892.11 and round(float(u[8]), 2) == 2029.96,
    "840 : seuil 2000 → 8")
chk(round(math.log(7 / 6) / math.log(1.02), 2) == 7.78, "840 : ln(7/6)/ln(1,02) ≈ 7,78")
chk(sum(R(2, 100) * u[k] for k in range(8)) == u[8] - 1000 - 800 and round(float(u[8] - 1800), 2) == 229.96,
    "840 : somme des intérêts = u8 - 1800 ≈ 229,96")
# 839
S = [sum(R(1, 2 ** k) for k in range(n + 1)) for n in range(25)]
chk(S[:4] == [1, R(3, 2), R(7, 4), R(15, 8)] and all(S[n] == 2 - R(1, 2 ** n) for n in range(25)), "839 : S_n = 2 - 1/2^n")
chk(float(S[10]) == 1.9990234375 and min(n for n in range(25) if 2 - S[n] < R(1, 10 ** 6)) == 20, "839 : S10, seuil 20")
chk(round(6 * math.log(10) / math.log(2), 2) == 19.93, "839 : 6 ln 10 / ln 2 ≈ 19,93")
# nouveau-1
T = [[a, b, c] for a in "PF" for b in "PF" for c in "PF"]
chk(len(T) == 8 and T[5] == ["F", "P", "F"] and sum(1 for t in T if t.count("P") == 2) == 3 == comb(3, 2), "n1 : 8 triplets, T[5], 3 avec deux P")
chk(2 ** 10 == 1024, "n1 : 2^10")
# nouveau-2
C2 = [(a, b) for a in range(1, 6) for b in range(1, 6) if a < b]
chk(len(C2) == 10 == comb(5, 2) == comb(5, 3), "n2 : 10 parties")
chk(sum(1 for p in C2 if 5 in p) == 4 and [a + b for a, b in C2].count(7) == 2, "n2 : 4 parties avec 5, 2 de somme 7")
# nouveau-3 : B(5 ; 0,4)
P5 = [comb(5, k) * R(2, 5) ** k * R(3, 5) ** (5 - k) for k in range(6)]
chk(sum(P5) == 1 and sum(k * P5[k] for k in range(6)) == 2, "n3 : loi B(5 ; 0,4), E(X) = 2")
# nouveau-4
p = R(52, 100)
chk(p * (1 - p) == R(2496, 10000) and p * (1 - p) / (400 * R(5, 100) ** 2) == R(2496, 10000), "n4 : V et majorant 0,2496")
nmin = min(n for n in range(1, 5000) if p * (1 - p) / (n * R(5, 100) ** 2) <= R(5, 100))
chk(nmin == 1997 and float(p * (1 - p) / (R(5, 100) * R(5, 100) ** 2)) == 1996.8, "n4 : n = 1997 (1996,8)")
# nouveau-6
chk(comb(20, 10) * R(1, 2 ** 20) == R(46189, 262144) and round(comb(20, 10) / 2 ** 20, 3) == 0.176, "n6 : P(X20 = 0) ≈ 0,176")
s = sp.Symbol("s")
chk(sp.expand(s - (20 - s)) == 2 * s - 20, "n6 : X20 = 2S - 20")

# ------------------------------------------------------------------ bilan
print(f"{tot['programmes']} programme(s) exécuté(s), {tot['affichages']} affichage(s) comparé(s), "
      f"{tot['trous']} programme(s) à compléter non exécuté(s)")
print(f"{n_controles} contrôle(s) mathématique(s)")
for e in erreurs:
    print("  ✗", e)
print("OK : tout est vérifié" if not erreurs else f"{len(erreurs)} erreur(s)")
raise SystemExit(1 if erreurs else 0)
