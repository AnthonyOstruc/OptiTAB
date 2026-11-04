# -*- coding: utf-8 -*-
"""Vérification de tous les résultats de la notion 171 (fonctions de référence)."""
from fractions import Fraction as F
import sympy as sp

x = sp.symbols("x", real=True)
R = sp.S.Reals
ok = 0


def eq(a, b, msg):
    global ok
    assert a == b, f"{msg} : {a} != {b}"
    ok += 1


def sol(expr, dom=R):
    return sp.solveset(expr, x, dom)


I = sp.Interval
# ---------------------------------------------------------------- cours
eq(sol(-2 * x + 3 < 7), I.open(-2, sp.oo), "cours affine")
eq(sol(x**2 <= 4), I(-2, 2), "cours x2<=4")
eq(sol(x**2 > 4), sp.Union(I.open(-sp.oo, -2), I.open(2, sp.oo)), "cours x2>4")
eq(sol(x**2 < 9), I.open(-3, 3), "cours x2<9")
eq((-3.1)**2 > (-2.7)**2, True, "cours comparer carres")
eq(sol(1 / x < 2, R - sp.FiniteSet(0)), sp.Union(I.open(-sp.oo, 0), I.open(F(1, 2), sp.oo)), "cours 1/x<2")
eq(sol(sp.sqrt(x) - 3, I(0, sp.oo)), sp.FiniteSet(9), "cours sqrt=3")
eq(sol(sp.sqrt(x) <= 3, I(0, sp.oo)), I(0, 9), "cours sqrt<=3")
eq(sol(sp.sqrt(x) < 3, I(0, sp.oo)), I.Ropen(0, 9), "cours sqrt<3")
eq(sol(x**3 + 8), sp.FiniteSet(-2), "cours cube=-8")
eq(sol(x**3 <= 27), I(-sp.oo, 3), "cours cube<=27")
eq(sp.sqrt(2.5) < sp.sqrt(2.6), True, "cours sqrt comparer")
eq(sp.factor(x**2 - x), x * (x - 1), "demo x2-x")
eq(sp.factor(x**3 - x**2), x**2 * (x - 1), "demo x3-x2")
eq((F(1, 2)**2, F(1, 2)**3), (F(1, 4), F(1, 8)), "0,5^2 0,5^3")


def balayage(pas):
    v = 1
    while v**2 < 2:
        v = v + pas
    return v - pas, v


for pas, (a, b) in [(0.1, (1.4, 1.5)), (0.01, (1.41, 1.42)), (0.001, (1.414, 1.415))]:
    r = balayage(pas)
    eq((round(r[0], 3), round(r[1], 3)), (a, b), f"balayage {pas}")
    eq(a < 2**0.5 < b, True, f"encadrement {pas}")
eq(round(balayage(0.1)[0], 16) != 1.4, True, "affichage approché 1,4000000000000004")
eq(F(14, 10)**2, F(196, 100), "1,4^2")
eq(F(15, 10)**2, F(225, 100), "1,5^2")
for line in ["def balayage(pas):", "    x = 1", "    while x**2 < 2:", "        x = x + pas", "    return x - pas, x"]:
    assert len(line) <= 30, line

# ---------------------------------------------------------------- 2025
f = lambda t: 2 * t + 3
eq((f(-2), f(0), f(3)), (-1, 3, 9), "2025 Q1")
eq(sol(2 * x + 3), sp.FiniteSet(sp.Rational(-3, 2)), "2025 Q3")
eq(sol(2 * x + 3 - 11), sp.FiniteSet(4), "2025 Q4")
eq(sol(-3 * x + 1 <= -8), I(3, sp.oo), "2025 Q5")
# ---------------------------------------------------------------- 2026
eq(((-3)**2, 2**2, 0**2, (-5)**2, 5**2), (9, 4, 0, 25, 25), "2026 Q1-2")
eq(sol(x**2 - 49), sp.FiniteSet(-7, 7), "2026 Q3")
eq(sol(x**2), sp.FiniteSet(0), "2026 Q4")
eq(((-4)**2, (-1)**2), (16, 1), "2026 Q5")
# ---------------------------------------------------------------- 2029
eq(((-2)**3, 0**3, 3**3), (-8, 0, 27), "2029 Q1")
eq(sol(x**3 - 27), sp.FiniteSet(3), "2029 Q2")
eq(sol(x**3 + 125), sp.FiniteSet(-5), "2029 Q3")
eq(sol(x**3 >= 8), I(2, sp.oo), "2029 Q5")
# ---------------------------------------------------------------- 2027
eq((F(1, 2), F(1, -4), 1 / F(1, 3)), (F(1, 2), F(-1, 4), F(3)), "2027 Q1")
eq(sol(1 / x - 2, R - sp.FiniteSet(0)), sp.FiniteSet(F(1, 2)), "2027 Q4")
eq(F(1, -3), -F(1, 3), "2027 Q5")
# ---------------------------------------------------------------- 2028
eq(sol(sp.sqrt(x) - 7, I(0, sp.oo)), sp.FiniteSet(49), "2028 Q3")
eq(sol(sp.sqrt(x) + 2, I(0, sp.oo)), sp.S.EmptySet, "2028 Q4")
# ---------------------------------------------------------------- 2030
g = lambda t: -2 * t + 5
eq((g(1), g(4)), (3, -3), "2030 Q1")
eq((1 / F(1, 2), F(1, 2)), (F(2), F(1, 2)), "2030 Q3")
eq(F(1, -2) < F(1, 3), True, "2030 Q6")
# ---------------------------------------------------------------- nouveau-2
eq(sp.imageset(sp.Lambda(x, x**2), I(2, 5)), I(4, 25), "n2 Q1")
eq(sp.imageset(sp.Lambda(x, 1 / x), I(2, 5)), I(F(1, 5), F(1, 2)), "n2 Q2")
eq(sp.imageset(sp.Lambda(x, sp.sqrt(x)), I(2, 5)), I(sp.sqrt(2), sp.sqrt(5)), "n2 Q3")
eq(round(float(sp.sqrt(2)), 2), 1.41, "n2 Q3 approx")
eq(round(float(sp.sqrt(5)), 2), 2.24, "n2 Q3 approx")
eq(sp.imageset(sp.Lambda(x, x**2), I(-3, 2)), I(0, 9), "n2 Q4")
eq(sp.imageset(sp.Lambda(x, x**3), I(-3, 2)), I(-27, 8), "n2 Q5")
# ---------------------------------------------------------------- 2031
eq(sol(2 * x - 7 - 5), sp.FiniteSet(6), "2031 Q1")
eq(sol(x**2 - 16), sp.FiniteSet(-4, 4), "2031 Q2")
eq(sol(1 / x + 3, R - sp.FiniteSet(0)), sp.FiniteSet(F(-1, 3)), "2031 Q3")
eq(sol(sp.sqrt(x) - 5, I(0, sp.oo)), sp.FiniteSet(25), "2031 Q4")
eq(sol(x**3 + 27), sp.FiniteSet(-3), "2031 Q5")
eq(sol(x**2 + 4), sp.S.EmptySet, "2031 Q6")
# ---------------------------------------------------------------- 2032
eq(sol(sp.sqrt(x) >= 4, I(0, sp.oo)), I(16, sp.oo), "2032 Q2")
eq(sol(1 / x > 2, R - sp.FiniteSet(0)), I.open(0, F(1, 2)), "2032 Q3")
eq(sol(-3 * x + 1 <= 10), I(-3, sp.oo), "2032 Q4")
eq(sol(x**3 <= -8), I(-sp.oo, -2), "2032 Q5")
# ---------------------------------------------------------------- nouveau-1
eq(sol(1 / x + 1, R - sp.FiniteSet(0)), sp.FiniteSet(-1), "n1 Q1")
eq(sol(1 / x >= -1, R - sp.FiniteSet(0)), sp.Union(I(-sp.oo, -1), I.open(0, sp.oo)), "n1 Q3")
# ---------------------------------------------------------------- 2033
eq(sol(x**2 - x, I(0, sp.oo)), sp.FiniteSet(0, 1), "2033 Q3")
eq(sol(x**2 <= x, I(0, sp.oo)), I(0, 1), "2033 Q4")
eq(sol(x**3 >= x**2, I(0, sp.oo)), sp.Union(sp.FiniteSet(0), I(1, sp.oo)), "2033 Q5")
# ---------------------------------------------------------------- 2034
eq(sol(1 / x - x, R - sp.FiniteSet(0)), sp.FiniteSet(-1, 1), "2034 Q2")
eq(sp.expand((x - 1) * (x - 4)), x**2 - 5 * x + 4, "2034 Q3b")
eq(sp.expand((x - 2)**2), x**2 - 4 * x + 4, "2034 Q3c")
eq(sol(sp.sqrt(x) - (x - 2), I(0, sp.oo)), sp.FiniteSet(4), "2034 Q3")
# ---------------------------------------------------------------- nouveau-3
eq([F(k, 10)**2 for k in range(11, 16)], [F(121, 100), F(144, 100), F(169, 100), F(196, 100), F(225, 100)], "n3 tableau")
eq((F(141, 100)**2, F(142, 100)**2), (F(19881, 10000), F(20164, 10000)), "n3 Q4")
eq((F(1414, 1000)**2, F(1415, 1000)**2), (F(1999396, 1000000), F(2002225, 1000000)), "n3 Q5")
# ---------------------------------------------------------------- figures de la finition 2026-11-02
eq(sol(-2 * x + 3 - 7), sp.FiniteSet(-2), "fig cours_affine intersection")
eq(sol(-2 * x + 3), sp.FiniteSet(F(3, 2)), "fig cours_affine zéro (graduation 2 au-dessus)")
eq(sol(1 / x - 2, R - sp.FiniteSet(0)), sp.FiniteSet(F(1, 2)), "fig cours_inverse_ineq")
eq([(2 * t + 3) for t in (-2, 0, 3, 4)], [-1, 3, 9, 11], "fig ex_affine_f points")
eq(sol(2 * x + 3), sp.FiniteSet(F(-3, 2)), "fig ex_affine_f zéro")
eq(sol(-3 * x + 1 + 8), sp.FiniteSet(3), "fig ex_affine_g intersection")
eq(sol(-3 * x + 1 <= -8), I(3, sp.oo), "fig ex_affine_g solution")
eq(((-5)**2, 5**2, (-4)**2, (-1)**2), (25, 25, 16, 1), "fig carré sym/compare")
eq(sol(x**3 - 8), sp.FiniteSet(2), "fig ex_cube_8")
eq((F(1, 3), F(1, -3)), (F(1, 3), F(-1, 3)), "fig ex_inverse_sym3")
eq(sol(sp.sqrt(x) - 3, I(0, sp.oo)), sp.FiniteSet(9), "fig ex_racine_3")
eq((F(1, -2), round(1 / 3, 2)), (F(-1, 2), 0.33), "fig ex_inverse_compare")
eq((sol(x**2 - 16), sol(x**2 + 4)), (sp.FiniteSet(-4, 4), sp.S.EmptySet), "fig ex_carre_16")
eq([F(k, 10)**2 for k in range(11, 16)], [F(121, 100), F(144, 100), F(169, 100), F(196, 100), F(225, 100)], "fig balayage points")
eq(1.4 < 2**0.5 < 1.5, True, "fig balayage √2")
# ---------------------------------------------------------------- exécution réelle du code du texte
import re  # noqa: E402
import textwrap  # noqa: E402
from pathlib import Path  # noqa: E402

ICI = Path(__file__).resolve().parent
for nom in ("cours_217.txt", "exercices.txt"):
    t = (ICI / nom).read_text(encoding="utf-8")
    for code in [textwrap.dedent(b) for b in re.findall(r"```python\n(.*?)```", t, re.S)]:
        ns = {}
        exec(code, ns)
        for pas, (a, b) in [(0.1, (1.4, 1.5)), (0.01, (1.41, 1.42)), (0.001, (1.414, 1.415))]:
            r = ns["balayage"](pas)
            eq((round(r[0], 3), round(r[1], 3)), (a, b), f"exec {nom} balayage({pas})")
        eq(repr(ns["balayage"](0.1)[0]), "1.4000000000000004", f"exec {nom} : affichage 1.4000000000000004")
print(f"verif_171 : {ok} contrôles, tous corrects")
