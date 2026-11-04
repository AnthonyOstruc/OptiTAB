# -*- coding: utf-8 -*-
"""Vérification de la notion « Concentration et loi des grands nombres » (Terminale).

    python verif_lgn.py

Contrôle chaque résultat numérique du cours, de la fiche et des exercices
(fractions exactes et scipy pour les valeurs exactes des lois binomiales),
exécute le programme Python du cours (200 exécutions : l'affichage proposé
doit être plausible) et vérifie les données des figures.
"""
import contextlib
import io
import re
from fractions import Fraction as F
from math import comb, isclose, sqrt
from pathlib import Path

from scipy.stats import binom

ICI = Path(__file__).resolve().parent
erreurs = []


def chk(cond, msg):
    if not cond:
        erreurs.append(msg)


def approx(x, v, tol):
    return abs(x - v) <= tol


# ------------------------------------------------------------------ cours
mu, V = 20 * F(1, 2), 20 * F(1, 4)
chk(mu == 10 and V == 5 and V / 16 == F(5, 16) and approx(5 / 16, 0.31, 0.005), "cours : B(20 ; 0,5), majorant 5/16 ≈ 0,31")
exact20 = binom.cdf(6, 20, 0.5) + binom.sf(13, 20, 0.5)
chk(approx(exact20, 0.115, 0.0005), f"cours : P(|X-10| >= 4) exacte ≈ 0,115 ({exact20})")
chk(approx(1 / 9, 0.11, 0.005), "cours : 1/9 ≈ 0,11")
chk(F(1, 4) / (2000 * F(5, 100) ** 2) == F(5, 100) and F(1, 4) / (1999 * F(5, 100) ** 2) > F(5, 100), "cours : n >= 2 000 (pièce)")
chk(F(1, 4) / (F(5, 100) ** 2) == 100, "cours : 0,25 / 0,05² = 100")
for p in (F(0), F(1, 3), F(1, 2), F(7, 10), F(1)):
    chk(p * (1 - p) == F(1, 4) - (p - F(1, 2)) ** 2, "cours : p(1-p) = 1/4 - (p - 1/2)²")
n_sond = 1 / (4 * F(5, 100) * F(3, 100) ** 2)
chk(approx(float(n_sond), 5555.6, 0.05) and int(n_sond) + 1 == 5556, "cours : sondage n >= 5 555,6 → 5 556")
exact100 = binom.cdf(40, 100, 0.5) + binom.sf(59, 100, 0.5)
chk(approx(exact100, 0.057, 0.0005), f"cours : P(|F100 - 0,5| >= 0,1) exacte ≈ 0,057 ({exact100})")
chk(F(1, 4) / (100 * F(1, 10) ** 2) == F(1, 4), "cours : majorant 0,25")

# programme Python du cours : exécuté 200 fois
texte = (ICI / "cours_98.txt").read_text(encoding="utf-8")
blocs = re.findall(r"```python\n(.*?)```", texte, re.S)
consoles = re.findall(r"```console\n(.*?)```", texte, re.S)
chk(len(blocs) == 1 and len(consoles) == 1, "cours : un programme et un affichage attendus")
vals = []
for _ in range(200):
    tampon = io.StringIO()
    with contextlib.redirect_stdout(tampon):
        exec(compile(blocs[0], "<cours>", "exec"), {"__name__": "__main__"})
    vals.append(float(tampon.getvalue()))
moy = sum(vals) / len(vals)
aff = float(consoles[0])
chk(min(vals) <= aff <= max(vals) and approx(moy, exact100, 0.004), f"simulation : affichage {aff}, moyenne {moy:.4f}")
print(f"  simulation du cours : 200 exécutions entre {min(vals)} et {max(vals)}, moyenne {moy:.4f} (exact {exact100:.4f}, affiché {aff})")
lignes = [l for b in blocs for l in b.splitlines()]
chk(max(map(len, lignes)) <= 34, "cours : ligne de code trop longue pour un téléphone")
chk(repr(0.6 - 0.5) == "0.09999999999999998" and not abs(40 / 100 - 0.5) >= 0.1 and not abs(60 / 100 - 0.5) >= 0.1,
    "cours : piège des décimaux (0.6 - 0.5)")

# ------------------------------------------------------------------ exercice 821
chk(F(47, 100) == F(47, 100) and abs(F(47, 100) - F(1, 2)) == F(3, 100), "821 Q1")
chk(F(21, 6) == F(7, 2), "821 Q2 : E = 3,5")
chk(F(1, 4) / (1000 * F(5, 100) ** 2) == F(1, 10) and F(52, 100) - F(1, 2) == F(2, 100), "821 Q3 : majorant 0,1")
# Q4 réécrite (finition 2026-11-02) : majorants pour n = 50 et n = 1 000, vérifiés avec sympy
import sympy as sp  # noqa: E402
_n = sp.Rational
chk(_n(1, 4) / (50 * _n(1, 10) ** 2) == _n(1, 2), "821 Q4 b : majorant 0,5 pour n = 50")
chk(_n(1, 4) / (1000 * _n(1, 10) ** 2) == _n(1, 40) and _n(1, 40) == _n(25, 1000), "821 Q4 b : majorant 0,025 pour n = 1 000")
chk(all(F(k, 1001) != F(1, 2) for k in range(1002)), "821 Q5 : 0,5 non atteint pour n = 1 001")

# ------------------------------------------------------------------ exercice 822
chk(F(4, 16) == F(1, 4), "822 Q1")
chk(F(9, 36) == F(1, 4), "822 Q2")
chk(F(4, 100) / F(25, 100) == F(16, 100), "822 Q3")
chk(1 - F(25, 100) == F(3, 4), "822 Q4")
chk(F(225, 100) / 9 == F(1, 4), "822 Q5")

# ------------------------------------------------------------------ exercice 825
chk(F(16) / (400 * F(5, 100)) == F(8, 10) and approx(sqrt(0.8), 0.894, 0.0005) and 0.9 >= sqrt(0.8), "825 Q1 : δ")
chk(F(16) / (400 * F(9, 10) ** 2) <= F(5, 100), "825 Q1 : δ = 0,9 convient")
chk(F(16) / (400 * F(89, 100) ** 2) > F(5, 100), "825 Q1 : δ = 0,89 ne convient pas")
chk(F(4) / (250 * F(1, 10)) == F(16, 100) and sqrt(0.16) == 0.4, "825 Q2")
chk(1 - F(400) / (1000 * 4) == F(9, 10), "825 Q3")
chk(1 / (4 * F(2500) * F(4, 100)) == F(1, 400) and sqrt(1 / 400) == 0.05, "825 Q4")
d5 = sqrt(4.5)
chk(F(9) / (200 * F(1, 100)) == F(9, 2) and isclose(d5, 3 * sqrt(2) / 2) and approx(d5, 2.12, 0.005), "825 Q5 : δ")
chk(approx(2 * d5, 4.24, 0.005) and 45.2 - 2.122 >= 43.07 and 45.2 + 2.122 <= 47.33 and 2.122 >= d5, "825 Q5 : intervalle")

# ------------------------------------------------------------------ exercice 823
def n_min(Vx, d, a):
    n = 1
    while F(Vx) / (n * F(d) ** 2) > F(a):
        n += 1
    return n


chk(n_min(F(1, 4), F(1, 10), F(5, 100)) == 500, "823 Q1")
chk(n_min(F(24, 100), F(2, 100), F(5, 100)) == 12000, "823 Q2")
Vde = F(91, 6) - F(7, 2) ** 2
chk(Vde == F(35, 12) and F(35, 12) / (F(1, 4) * F(1, 10)) == F(350, 3) and n_min(Vde, F(1, 2), F(1, 10)) == 117, "823 Q3")
chk(n_min(F(1, 4), F(5, 100), F(1, 100)) == 10000, "823 Q4")
chk(F(21, 100) / (F(9, 10000) * F(1, 10)) == F(7000, 3) and n_min(F(21, 100), F(3, 100), F(1, 10)) == 2334, "823 Q5")

# ------------------------------------------------------------------ exercice 824
chk(F(9, 100) / (100 * F(1, 100)) == F(9, 100), "824 Q1")
p = 1 / 37
d = p - 0.024
chk(approx(p, 0.02703, 5e-6) and approx(d, 0.00303, 5e-6) and approx(0.031 - p, 0.00397, 5e-6) and d < 0.031 - p, "824 Q2 : δ")
borne = p * (1 - p) / (10000 * d * d)
chk(approx(p * (1 - p), 0.02630, 5e-6) and approx(borne, 0.287, 0.0005) and approx(1 - borne, 0.713, 0.0005), f"824 Q2 : borne ({borne})")
chk(approx(0.02630 / (10000 * 0.00303 ** 2), 0.287, 0.001), "824 Q2 : calcul avec les valeurs arrondies")
chk(p - 0.004 < 0.024, "824 Q2 : δ = 0,004 déborde à gauche")
exact_roul = binom.cdf(310, 10000, p) - binom.cdf(239, 10000, p)
chk(approx(exact_roul, 0.965, 0.0005), f"824 Q2 : valeur exacte ≈ 0,965 ({exact_roul})")
chk(approx(0.0475 / 0.9, 0.053, 0.0005), "824 Q3")
chk(n_min(25, F(1, 2), F(5, 100)) == 2000, "824 Q4")
d824 = sqrt(0.008)
chk(F(16, 100) / (500 * F(4, 100)) == F(8, 1000) and approx(d824, 0.0894, 5e-5) and 0.0895 >= d824, "824 Q5 : δ")
chk(9.82 - 0.0895 >= 9.73 and 9.82 + 0.0895 <= 9.91, "824 Q5 : intervalle")

# ------------------------------------------------------------------ figures
import importlib.util  # noqa: E402
spec = importlib.util.spec_from_file_location("fig", ICI / "figures" / "figures.py")
fig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fig)
chk(all(isclose(fig._P[k], comb(20, k) / 2 ** 20) for k in range(21)), "figure bt_binomiale : probabilités")
for g, t in zip(fig.GRAINES, fig._TRAJ):
    chk(all(0.25 < f < 0.76 for _, f in t), f"figure lgn_convergence : trajectoire {g} hors du cadre")
chk(approx(1 / sqrt(0.2 * 80), 0.25, 1e-9), "figure lgn_convergence : bande 0,5 ± 1/sqrt(0,2 n), α = 0,05")

# figures ajoutées le 2026-11-02 (sympy)
x, n_s, p_s = sp.symbols("x n p", positive=True)
# 821 : simulation (graine 2), ce que dit le corrigé de la lecture
sim = fig.SIM821
sorties = [n for n, f in sim if abs(f - 0.5) >= 0.1]
chk(sorties and max(sorties) < 100 and min(sorties) <= 50, f"figure 821 : sorties de la bande aux rangs {sorties[:3]}… (dernière {max(sorties)})")
chk(all(0.2 < f < 0.8 for _, f in sim), "figure 821 : trajectoire dans le cadre 0,2–0,8")
debut = [f for n, f in sim if n <= 50]
chk(0.25 <= min(debut) <= 0.32 and 0.48 <= max(debut) <= 0.55, f"figure 821 : début entre 0,3 et 0,5 environ ({min(debut):.3f} ; {max(debut):.3f})")
chk(approx(sim[-1][1], 0.5, 0.01), f"figure 821 : f_1000 = {sim[-1][1]}")
# 822 : intervalle centré, δ = 0,5 et majorant 0,16
chk(_n(5) - _n(9, 2) == _n(11, 2) - _n(5) == _n(1, 2) and (_n(2, 10) ** 2) / _n(1, 2) ** 2 == _n(16, 100), "figure 822 : δ = 0,5, majorant 0,16")
# 823 : 0,25 / (n × 0,1²) = 25/n, intersection avec y = 0,05 en n = 500, courbe sous la droite pour n >= 500
chk(sp.simplify(_n(1, 4) / (n_s * _n(1, 10) ** 2) - 25 / n_s) == 0, "823 : majorant = 25/n")
chk(sp.solve(sp.Eq(25 / n_s, _n(5, 100)), n_s) == [500], "figure 823 : intersection n = 500")
chk(sp.solve_univariate_inequality(25 / x <= _n(1, 20), x, relational=False).intersect(sp.Interval.open(0, sp.oo)) == sp.Interval(500, sp.oo), "figure 823 : 25/n <= 0,05 ssi n >= 500")
chk(25 / 170 < 0.155 and 25 / 330 < 0.09, "figure 823 : courbe dans le cadre, étiquette au-dessus")
# 825 : p(1 - p) = 1/4 - (p - 1/2)², maximum 1/4 en 1/2
chk(sp.expand(p_s * (1 - p_s) - (_n(1, 4) - (p_s - _n(1, 2)) ** 2)) == 0, "825 : p(1-p) = 1/4 - (p - 1/2)²")
chk(sp.solve(sp.diff(p_s * (1 - p_s), p_s), p_s) == [_n(1, 2)] and (p_s * (1 - p_s)).subs(p_s, _n(1, 2)) == _n(1, 4), "figure 825 : sommet (1/2 ; 1/4)")

# ====================================================================== Enrichissement 2026-11-02
nb_avant = len(erreurs)
controles = 0


def ck(cond, msg):
    global controles
    controles += 1
    chk(cond, "enrichissement : " + msg)


def r3(v):
    return round(float(v), 3)


# ---------------------------------------------------------------- nouveau-1 : Bienaymé-Tchebychev, loi connue
L1 = {0: F(5, 100), 1: F(10, 100), 2: F(20, 100), 3: F(30, 100), 4: F(20, 100), 5: F(10, 100), 6: F(5, 100)}
E1 = sum(k * p for k, p in L1.items())
V1 = sum((k - E1) ** 2 * p for k, p in L1.items())
ck(sum(L1.values()) == 1 and E1 == 3 and V1 == F(21, 10), "n1 : loi, E = 3, V = 2,1")
ck([k * L1[k] for k in range(1, 7)] == [F(1, 10), F(4, 10), F(9, 10), F(8, 10), F(5, 10), F(3, 10)], "n1 : termes de E(X)")
ck([(k - 3) ** 2 * L1[k] for k in range(7)] == [F(45, 100), F(4, 10), F(2, 10), 0, F(2, 10), F(4, 10), F(45, 100)], "n1 : termes de V(X)")
ck(round(sqrt(2.1), 2) == 1.45, "n1 : σ ≈ 1,45")
ex1 = {d: sum(p for k, p in L1.items() if abs(k - 3) >= d) for d in (1, 2, 3)}
ck(V1 / 4 == F(21, 40) and ex1[2] == F(3, 10), "n1 : δ = 2, majorant 0,525, exacte 0,3")
ck(V1 / 9 == F(7, 30) and r3(F(7, 30)) == 0.233 and ex1[3] == F(1, 10), "n1 : δ = 3, majorant 7/30 ≈ 0,233, exacte 0,1")
ck(1 - V1 / 4 == F(19, 40) and L1[2] + L1[3] + L1[4] == F(7, 10), "n1 : P(1 < X < 5) ≥ 0,475, exacte 0,7")
ck(V1 / 1 == F(21, 10) and ex1[1] == 1 - L1[3] == F(7, 10) and 1 ** 2 < V1 and sqrt(2.1) > 1, "n1 : δ = 1, majorant 2,1 > 1, exacte 0,7")

# ---------------------------------------------------------------- nouveau-2 : concentration pour un gain moyen
L2 = {-1: F(1, 2), 0: F(3, 10), 4: F(2, 10)}
E2 = sum(k * p for k, p in L2.items())
V2 = sum((k - E2) ** 2 * p for k, p in L2.items())
ck(E2 == F(3, 10) and V2 == F(361, 100) and sqrt(3.61) == 1.9, "n2 : E = 0,3, V = 3,61, σ = 1,9")
ck([(k - E2) ** 2 for k in (-1, 0, 4)] == [F(169, 100), F(9, 100), F(1369, 100)]
   and [(k - E2) ** 2 * p for k, p in L2.items()] == [F(845, 1000), F(27, 1000), F(2738, 1000)], "n2 : termes de la variance")
b100, b1000 = V2 / (100 * F(3, 10) ** 2), V2 / (1000 * F(3, 10) ** 2)
ck(b100 == F(361, 900) and r3(b100) == 0.401 and b1000 == F(361, 9000) and r3(b1000) == 0.04, "n2 : majorants 3,61/9 ≈ 0,401 et 3,61/90 ≈ 0,040")
d2 = V2 / (1000 * F(5, 100))
ck(d2 == F(722, 10000) and round(sqrt(float(d2)), 4) == 0.2687, "n2 : δ² ≥ 0,0722, δ ≥ 0,2687")
ck(V2 / (1000 * F(27, 100) ** 2) <= F(5, 100) < V2 / (1000 * F(26, 100) ** 2), "n2 : δ = 0,27 convient, 0,26 non")
ck(F(3, 10) - F(27, 100) == F(3, 100) and F(3, 10) + F(27, 100) == F(57, 100) and 1000 * F(3, 100) == 30 and 1000 * F(57, 100) == 570, "n2 : intervalles ]0,03 ; 0,57[ et ]30 ; 570[")

# ---------------------------------------------------------------- nouveau-3 : simulation et loi des grands nombres
TAILLES = (50, 100, 200, 500, 1000)
ck(all(F(4, 25) / (n * F(5, 100) ** 2) == F(64, n) for n in TAILLES), "n3 : majorant 0,16/(n × 0,0025) = 64/n")
ck([float(F(64, n)) for n in TAILLES] == [1.28, 0.64, 0.32, 0.128, 0.064], "n3 : majorants 1,28 ; 0,64 ; 0,32 ; 0,128 ; 0,064")
ck(all((abs(F(s, n) - F(1, 5)) >= F(5, 100)) == (abs(20 * s - 4 * n) >= n) for n in (7, 50, 100, 333, 1000) for s in range(n + 1)),
   "n3 : |s/n − 0,2| ≥ 0,05 ⟺ |20s − 4n| ≥ n (tous les s)")
ck(abs(25 / 100 - 0.2) == 0.04999999999999999 and not abs(25 / 100 - 0.2) >= 0.05 and abs(20 * 25 - 4 * 100) >= 100,
   "n3 : piège des décimaux pour s = 25, n = 100")
exacts3 = [sum(binom.pmf(k, n, 0.2) for k in range(n + 1) if abs(20 * k - 4 * n) >= n) for n in TAILLES]
ck([round(float(v), 3) for v in exacts3[:4]] == [0.376, 0.26, 0.092, 0.006] and round(float(exacts3[4]), 4) == 0.0001,
   f"n3 : valeurs exactes {[round(float(v), 5) for v in exacts3]}")
# programme de l'énoncé exécuté réellement (graine 1) : il doit redonner le tableau de l'énoncé
blocs = re.findall(r"```python\n(.*?)```", (ICI / "exercices.txt").read_text(encoding="utf-8"), re.S)
code3 = next(b for b in blocs if "def ecarts(n, N)" in b and "randint(1, 5)" in b)
import random  # noqa: E402
espace = {}
exec(code3, espace)
random.seed(1)
sim3 = [espace["ecarts"](n, 1000) for n in TAILLES]
ck(sim3 == [0.398, 0.25, 0.091, 0.004, 0.0], f"n3 : programme exécuté (graine 1) → {sim3}")
ck(all(s <= float(F(64, n)) for s, n in zip(sim3, TAILLES)), "n3 : simulation sous le majorant")
ck(F(254, 1000) - F(1, 5) == F(54, 1000) and F(54, 1000) >= F(5, 100), "n3 : 254 rouges, écart 0,054 ≥ 0,05")
p1000 = binom.cdf(149, 1000, 0.2) + binom.sf(249, 1000, 0.2)
ck(5e-5 < p1000 < 5e-4, f"n3 : P(|F_1000 − 0,2| ≥ 0,05) exacte de l'ordre de 0,0001 ({p1000:.2e})")

# ---------------------------------------------------------------- nouveau-4 : taille d'échantillon et coût
ck(all(p * (1 - p) == F(1, 4) - (p - F(1, 2)) ** 2 <= F(1, 4) for p in (F(0), F(1, 10), F(1, 2), F(9, 10), F(1))), "n4 : p(1 − p) = 1/4 − (p − 1/2)² ≤ 1/4")
taille = lambda Vx, d, a: Vx / (a * d ** 2)  # noqa: E731
ck(taille(F(1, 4), F(5, 100), F(5, 100)) == 2000 and 4 * F(5, 100) * F(5, 100) ** 2 == F(5, 10000) and 2000 * 3 == 6000, "n4 : n ≥ 2 000, 6 000 euros")
ck(taille(F(1, 4), F(25, 1000), F(5, 100)) == 8000 and 4 * F(5, 100) * F(25, 1000) ** 2 == F(125, 1000000) and 8000 * 3 == 24000, "n4 : n ≥ 8 000, 24 000 euros")
ck(F(4500, 3) == 1500 and 1 / (4 * 1500 * F(5, 100)) == F(1, 300), "n4 : n = 1 500, δ² ≥ 1/300")
ck(round(1 / sqrt(300), 4) == 0.0577 and F(57, 1000) ** 2 < F(1, 300) <= F(58, 1000) ** 2, "n4 : δ = 0,058 (0,057 ne convient pas)")
ck(sp.diff(p_s * (1 - p_s), p_s).subs(p_s, _n(1, 10)) > 0 and sp.solve(sp.diff(p_s * (1 - p_s), p_s), p_s) == [_n(1, 2)]
   and F(1, 10) * F(9, 10) == F(9, 100), "n4 : p(1 − p) croissante sur [0 ; 1/2], ≤ 0,09 si p ≤ 0,1")
ck(taille(F(9, 100), F(2, 100), F(5, 100)) == 4500 and F(5, 100) * F(2, 100) ** 2 == F(2, 100000) and 4500 * 3 == 13500, "n4 : n ≥ 4 500 (13 500 euros)")
ck(taille(F(1, 4), F(2, 100), F(5, 100)) == 12500 and 4 * F(5, 100) * F(2, 100) ** 2 == F(8, 100000) and 12500 * 3 == 37500, "n4 : sans information n ≥ 12 500 (37 500 euros)")

# ---------------------------------------------------------------- nouveau-5 : Bienaymé-Tchebychev et loi binomiale
n5, p5 = 50, 0.2
ck(50 * F(1, 5) == 10 and 50 * F(1, 5) * F(4, 5) == 8 and F(8, 25) == F(32, 100), "n5 : E = 10, V = 8, majorant 0,32")
a5, b5 = binom.cdf(5, n5, p5), binom.sf(14, n5, p5)
ck(round(a5, 3) == 0.048 and round(b5, 3) == 0.061 and round(a5 + b5, 3) == 0.109, f"n5 : P(X ≤ 5) ≈ 0,048, P(X ≥ 15) ≈ 0,061, somme ≈ 0,109 ({a5 + b5:.5f})")
ck(2.8 < 0.32 / (a5 + b5) < 3.1, "n5 : environ trois fois moins que le majorant")
ck(round(sqrt(160), 1) == 12.6 and min(d for d in range(1, 30) if F(8, d * d) <= F(5, 100)) == 13, "n5 : δ² ≥ 160, plus petit entier δ = 13")
ck([k for k in range(51) if abs(k - 10) < 13] == list(range(0, 23)), "n5 : |X − 10| < 13 ⟺ X ∈ {0 ; … ; 22}")
ex5 = {d: sum(binom.pmf(k, n5, p5) for k in range(51) if abs(k - 10) >= d) for d in range(1, 14)}
ck(round(ex5[6], 3) == 0.049 and ex5[5] > 0.05 >= ex5[6] and round(1 - ex5[6], 3) == 0.951, "n5 : P(|X − 10| ≥ 6) ≈ 0,049 ; P(5 ≤ X ≤ 15) ≈ 0,951")
ck(min(d for d in range(1, 14) if ex5[d] <= 0.05) == 6 and [k for k in range(51) if abs(k - 10) < 6] == list(range(5, 16)), "n5 : δ exact = 6, X ∈ {5 ; … ; 15}")

# ---------------------------------------------------------------- nouveau-6 : type examen
pF, pGF, pGnF = F(6, 10), F(4, 10), F(15, 100)
pG = pF * pGF + (1 - pF) * pGnF
ck(pF * pGF == F(24, 100) and (1 - pF) * pGnF == F(6, 100) and pG == F(3, 10), "n6 : P(F ∩ G) = 0,24, P(F̄ ∩ G) = 0,06, P(G) = 0,3")
ck(pF * (1 - pGF) == F(36, 100) and (1 - pF) * (1 - pGnF) == F(34, 100), "n6 : autres chemins 0,36 et 0,34 (figure)")
ck(pF * pGF / pG == F(8, 10), "n6 : P_G(F) = 0,8")
ck(round(comb(20, 6) * 0.3 ** 6 * 0.7 ** 14, 3) == 0.192 and round(binom.pmf(6, 20, 0.3), 3) == 0.192, "n6 : P(X = 6) ≈ 0,192")
ck(round(binom.sf(9, 20, 0.3), 3) == 0.048, "n6 : P(X ≥ 10) ≈ 0,048")
ck(20 * F(3, 10) == 6 and 20 * F(3, 10) * F(7, 10) == F(42, 10), "n6 : E(X) = 6, V(X) = 4,2")
ck([k for k in range(21) if abs(k - 6) < 4] == list(range(3, 10)) and 1 - F(42, 10) / 16 == F(7375, 10000), "n6 : 3 ≤ X ≤ 9 ⟺ |X − 6| < 4, minorant 0,737 5")
ex6 = binom.cdf(9, 20, 0.3) - binom.cdf(2, 20, 0.3)
ck(round(ex6, 3) == 0.917, f"n6 : P(3 ≤ X ≤ 9) ≈ 0,917 ({ex6:.5f})")
ck(all(5 * k - (20 - k) == 6 * k - 20 for k in range(21)) and 6 * 6 - 20 == 16, "n6 : T = 6X − 20, E(T) = 16")
ck([k for k in range(21) if 6 * k - 20 > 0] == list(range(4, 21)) and round(binom.sf(3, 20, 0.3), 3) == 0.893, "n6 : T > 0 ⟺ X ≥ 4, P ≈ 0,893")
EY = 5 * F(3, 10) - F(7, 10)
VY = F(3, 10) * (5 - EY) ** 2 + F(7, 10) * (-1 - EY) ** 2
ck(EY == F(8, 10) and (5 - EY) ** 2 == F(1764, 100) and (-1 - EY) ** 2 == F(324, 100) and VY == F(756, 100)
   and F(3, 10) * F(1764, 100) == F(5292, 1000) and F(7, 10) * F(324, 100) == F(2268, 1000), "n6 : E(Y) = 0,8, V(Y) = 7,56")
nmin = VY / (F(8, 10) ** 2 * F(5, 100))
ck(nmin == F(23625, 100) and VY / (237 * F(64, 100)) <= F(5, 100) < VY / (236 * F(64, 100)), "n6 : n ≥ 236,25, n = 237 (236 ne convient pas)")

# ---------------------------------------------------------------- figures de l'enrichissement
ck(fig.SIM_N3 == dict(zip(TAILLES, sim3)), "figure n3 : proportions simulées identiques au programme")
ck(fig.LOI_N1 == {k: float(v) for k, v in L1.items()}, "figure n1 : loi des colis")
ck(all(isclose(fig.LOI_N5[k], binom.pmf(k, 50, 0.2), rel_tol=1e-9) for k in range(26)), "figure n5 : B(50 ; 0,2)")
ck(all(isclose(fig.LOI_N6[k], binom.pmf(k, 20, 0.3), rel_tol=1e-9) for k in range(21)), "figure n6 : B(20 ; 0,3)")
ck(max(fig.LOI_N5.values()) < 0.155 and max(fig.LOI_N6.values()) < 0.205, "figures n5 et n6 : cotes au-dessus des barres")
ck("(0,-1.5)" not in fig.FIGURES["n2_loi"] and "(-1,0.5) (0,0.3) (4,0.2)" in fig.FIGURES["n2_loi"], "figure n2 : loi du gain")
print(f"  enrichissement : {controles} contrôles, {len(erreurs) - nb_avant} erreur(s)")

print("OK : tout est vérifié" if not erreurs else f"{len(erreurs)} erreur(s)")
for e in erreurs:
    print("  ✗", e)
raise SystemExit(1 if erreurs else 0)
