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

print("OK : tout est vérifié" if not erreurs else f"{len(erreurs)} erreur(s)")
for e in erreurs:
    print("  ✗", e)
raise SystemExit(1 if erreurs else 0)
