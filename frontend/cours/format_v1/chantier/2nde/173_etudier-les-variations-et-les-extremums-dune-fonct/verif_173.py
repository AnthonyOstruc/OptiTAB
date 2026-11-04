# -*- coding: utf-8 -*-
"""Vérification de tous les résultats de la notion 173 (variations, extremums)."""
import sys
from pathlib import Path

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent / "figures"))
from figures import hermite_val, COURBE_COURS, COURBE_EX  # noqa: E402

x, u, v = sp.symbols("x u v", real=True)
R = sp.Rational
N = 0


def ok(cond, msg):
    global N
    N += 1
    if not bool(cond):
        print("ÉCHEC :", msg)
        sys.exit(1)


def extremums(f, a, b):
    """max / min exacts de f sur [a ; b] (points critiques + bornes)."""
    pts = [a, b] + [c for c in sp.solve(sp.diff(f, x), x) if c.is_real and a <= c <= b]
    vals = [sp.nsimplify(f.subs(x, p)) for p in pts]
    return max(vals), min(vals)


def croissante(f, a, b, strict=True):
    xs = [a + (b - a) * k / 400 for k in range(401)]
    ys = [float(f.subs(x, t)) if hasattr(f, "subs") else f(t) for t in xs]
    return all(y2 > y1 for y1, y2 in zip(ys, ys[1:]))


def decroissante(f, a, b):
    xs = [a + (b - a) * k / 400 for k in range(401)]
    ys = [float(f.subs(x, t)) if hasattr(f, "subs") else f(t) for t in xs]
    return all(y2 < y1 for y1, y2 in zip(ys, ys[1:]))


# ------------------------------------------------------------------ cours
fc = lambda t: hermite_val(COURBE_COURS, t)
ok(abs(fc(-3) - 2) < 1e-12 and abs(fc(-1) + 2) < 1e-12 and abs(fc(2) - 3) < 1e-12 and abs(fc(5)) < 1e-12, "cours noeuds")
ok(decroissante(fc, -3, -1) and croissante(fc, -1, 2) and decroissante(fc, 2, 5), "cours monotonie")
ok(fc(0) < 2, "cours : max sur [-3;0] = f(-3) = 2")
ok(max(fc(-3 + 8 * k / 1000) for k in range(1001)) <= 3 + 1e-9, "cours max 3")
ok(min(fc(-3 + 8 * k / 1000) for k in range(1001)) >= -2 - 1e-9, "cours min -2")
# démonstrations
ok(sp.expand((v - u) * (v + u) - (v**2 - u**2)) == 0, "carré")
ok(sp.simplify(1 / v - 1 / u - (u - v) / (u * v)) == 0, "inverse")
a_, b_ = sp.symbols("a b", positive=True)
ok(sp.simplify(sp.sqrt(b_) - sp.sqrt(a_) - (b_ - a_) / (sp.sqrt(b_) + sp.sqrt(a_))) == 0, "racine")
m, p = sp.symbols("m p")
ok(sp.expand((m * v + p) - (m * u + p) - m * (v - u)) == 0, "affine")
# balayage du cours
fb = lambda t: -t * t + 4 * t
h = (5 - 0) / 100
mx = fb(0)
for k in range(1, 101):
    mx = max(mx, fb(0 + k * h))
ok(abs(mx - 4) < 1e-12, "balayage cours")
ok((-2 * x + 5).subs(x, 0) == 5 and (-2 * x + 5).subs(x, 3) == -1, "cours exemple affine")
ok(fc(0) <= fc(1), "cours f(0) <= f(1)")
ok(fc(-2) < 2 and fc(1) > -2, "cours : f(-2), f(1) non comparables par le tableau seul")

# --------------------------------------------------------- 2024 balayage
f = -x**2 + 5 * x
ok(sp.expand(R(25, 4) - (x - R(5, 2))**2 - f) == 0, "2024 forme")
ok([f.subs(x, t) for t in range(5)] == [0, 4, 6, 6, 4], "2024 images")


def prog(n):
    def ff(t):
        return t * (5 - t)
    a, b = 0, 4
    x_max, y_max = a, ff(a)
    for i in range(1, n + 1):
        t = a + i * (b - a) / n
        if ff(t) > y_max:
            x_max, y_max = t, ff(t)
    return x_max, y_max


ok(prog(4) == (2.0, 6.0), "2024 n=4")
ok(prog(8) == (2.5, 6.25), "2024 n=8")
ok(prog(40)[1] == 6.25 or abs(prog(40)[1] - 6.25) < 1e-9, "2024 n=40")

# ------------------------------------------------ 2012 (courbe lue)
fe = lambda t: hermite_val(COURBE_EX, t)
ok([round(fe(t), 12) for t in (-4, -2, 1, 4)] == [1, 3, -2, 2], "2012 noeuds")
ok(croissante(fe, -4, -2) and decroissante(fe, -2, 1) and croissante(fe, 1, 4), "2012 monotonie")
ok(-2 < fe(0) < 2 and fe(-1) > fe(0), "2012 f(0), comparaison")

# ------------------------------------------------ 2018 tableau
# g(0) <= 2 < 3 = g(4,5) : pur raisonnement, rien à calculer.

# ------------------------------------------------ 2015 racine
r = sp.sqrt(5 - 2 * x)
ok([r.subs(x, -2), r.subs(x, 0), r.subs(x, R(5, 2)), r.subs(x, R(1, 2))] == [3, sp.sqrt(5), 0, 2], "2015 images")
ok(0 < sp.sqrt(5) < 3, "2015 valeur intermédiaire placée entre 3 et 0")
ok(decroissante(r, -2, R(5, 2)), "2015 décroissante")
ok(sp.solve_univariate_inequality(r >= 2, x, relational=False).intersect(sp.Interval(-2, R(5, 2))) == sp.Interval(-2, R(1, 2)), "2015 inéquation")

# ------------------------------------------------ 2021 affine
pa = -3 * x + 7
ok(pa.subs(x, 1) == 4 and pa.subs(x, 5) == -8 and pa.subs(x, 0) == 7 and pa.subs(x, -2) == 13, "2021")
ok(R(-8 - 4, 5 - 1) == -3, "2021 taux")

# ------------------------------------------------ 2020 référence
ok(extremums(x**2, -3, 2) == (9, 0), "2020 carré")
ok(R(1, 2) > R(1, 5) and R(-1, 2) < R(-1, 5), "2020 inverse")
ok(extremums(1 / x, R(1, 2), 4) == (2, R(1, 4)), "2020 inverse extremums")
ok(sp.Rational(-31, 10)**2 > sp.Rational(-27, 10)**2, "2020 carrés négatifs")
ok(sp.solve_univariate_inequality(sp.sqrt(x) >= 3, x, relational=False) == sp.Interval(9, sp.oo), "2020 racine")

# ------------------------------------------------ 2019 affine
fa = 4 - 3 * x
ok(fa.subs(x, -2) == 10 and fa.subs(x, 2) == -2 and fa.subs(x, 1) == 1, "2019")
ok(sp.solve_univariate_inequality(fa >= 1, x, relational=False) == sp.Interval(-sp.oo, 1), "2019 inéq")

# ------------------------------------------------ 2014 parabole
g = -2 * x**2 + 12 * x - 11
ok(sp.expand(-2 * (x - 3)**2 + 7 - g) == 0, "2014 forme")
ok([g.subs(x, t) for t in (0, 3, 4, 5)] == [-11, 7, 5, -1], "2014 valeurs")
ok(extremums(g, 0, 5) == (7, -11) and extremums(g, 4, 5) == (5, -1), "2014 extremums")

# ------------------------------------------------ 2013 parabole
f13 = (x + 3)**2 - 1
ok([f13.subs(x, t) for t in (-6, -3, 2, 0)] == [8, -1, 24, 8], "2013 valeurs")
ok(sp.solve_univariate_inequality(f13 <= 8, x, relational=False).intersect(sp.Interval(-6, 2)) == sp.Interval(-6, 0), "2013 inéq")
ok(extremums(f13, -6, 2) == (24, -1), "2013 extremums")

# ------------------------------------------------ 2016 valeur absolue
hh = lambda t: abs(t - 2) + 1
ok([hh(t) for t in (-1, 2, 6)] == [4, 1, 5], "2016")
ok(sp.solve_univariate_inequality(sp.Abs(x - 2) + 1 <= 4, x, relational=False) == sp.Interval(-1, 5), "2016 inéq")

# ------------------------------------------------ 2017 rationnelle
q = 1 / (x**2 + 1)
ok([q.subs(x, t) for t in (-3, 0, 3)] == [R(1, 10), 1, R(1, 10)], "2017")
ok(croissante(q, -3, 0) and decroissante(q, 0, 3), "2017 variations")

# ------------------------------------------------ 2022 parabole
f22 = -(x - 2)**2 + 5
ok([f22.subs(x, t) for t in (-1, 2, 6, 0, 4)] == [-4, 5, -11, 1, 1], "2022")
ok(sp.solve_univariate_inequality(f22 >= 1, x, relational=False) == sp.Interval(0, 4), "2022 inéq")

# ------------------------------------------------ 2023 rectangle
A = x * (10 - x)
ok(sp.expand(25 - (x - 5)**2 - A) == 0 and sp.expand(A - (-x**2 + 10 * x)) == 0, "2023 formes")
ok(sp.solve_univariate_inequality(A >= 21, x, relational=False) == sp.Interval(3, 7), "2023 inéq")
ok(A.subs(x, 3) == 21 and A.subs(x, 7) == 21 and A.subs(x, 5) == 25, "2023 valeurs")

# ------------------------------------------------ nouveau-1
F = x**2 + 4 * x
ok(sp.expand(F.subs(x, v) - F.subs(x, u) - (v - u) * (v + u + 4)) == 0, "n1 factorisation")
ok(F.subs(x, -4) == 0 and F.subs(x, -3) == -3 and F.subs(x, 0) == 0 and F.subs(x, 1) == 5, "n1 contre-exemple")
G = 3 - 2 / x
ok(sp.simplify(G.subs(x, v) - G.subs(x, u) - 2 * (v - u) / (u * v)) == 0, "n1 g")
ok(croissante(F, -2, 6) and croissante(G, R(1, 10), 10), "n1 variations")

# ------------------------------------------------ nouveau-2
f1 = R(1, 2) * x + 1
g2 = -2 * x + 3
ok(f1.subs(x, -2) == 0 and f1.subs(x, 0) == 1 and f1.subs(x, 2) == 2, "n2 f")
ok(g2.subs(x, 0) == 3 and g2.subs(x, 1) == 1 and g2.subs(x, R(3, 2)) == 0, "n2 g")
ok(f1.subs(x, -3) == R(-1, 2) and f1.subs(x, 3) == R(5, 2) and g2.subs(x, -3) == 9 and g2.subs(x, 3) == -3, "n2 bornes")

# ------------------------------------------------ figures de la finition 2026-11-02
from figures import COURBE_2018  # noqa: E402

h18 = lambda t: hermite_val(COURBE_2018, t)
ok([h18(t) for t in (-3, 1, 4)] == [2, -4, 3], "fig 2018 nœuds = tableau")
ok(decroissante(h18, -3, 1) and croissante(h18, 1, 4), "fig 2018 sens de variation de la courbe")
r15 = sp.sqrt(5 - 2 * x)
ok(r15.subs(x, -2) == 3 and r15.subs(x, R(5, 2)) == 0 and r15.subs(x, R(1, 2)) == 2, "fig 2015 points")
ok(sp.solveset(r15 >= 2, x, sp.Interval(-2, R(5, 2))) == sp.Interval(-2, R(1, 2)), "fig 2015 solution")
p21 = -3 * x + 7
ok([p21.subs(x, t) for t in (-2, 1, 2, 5)] == [13, 4, 1, -8], "fig 2021 points et marche +1 / -3")
ok([(x**2).subs(x, t) for t in (-3, 0, 2)] == [9, 0, 4], "fig 2020")
f19 = 4 - 3 * x
ok([f19.subs(x, t) for t in (-2, 1, 2)] == [10, 1, -2], "fig 2019 points")
ok(sp.solveset(f19 >= 1, x, sp.Interval(-2, 2)) == sp.Interval(-2, 1), "fig 2019 solution")
g14 = -2 * (x - 3)**2 + 7
ok([g14.subs(x, t) for t in (0, 3, 4, 5)] == [-11, 7, 5, -1], "fig 2014 points")
ok(decroissante(g14, 4, 5), "fig 2014 décroissante sur [4 ; 5]")
f13 = (x + 3)**2 - 1
ok([f13.subs(x, t) for t in (-6, -3, 0, 2)] == [8, -1, 8, 24], "fig 2013 points")
ok(sp.solveset(f13 <= 8, x, sp.Interval(-6, 2)) == sp.Interval(-6, 0), "fig 2013 solution")
h16 = sp.Abs(x - 2) + 1
ok([h16.subs(x, t) for t in (-1, 2, 5, 6)] == [4, 1, 4, 5], "fig 2016 points")
ok(sp.solveset(h16 <= 4, x, sp.Interval(-1, 6)) == sp.Interval(-1, 5), "fig 2016 solution")
c17 = 1 / (x**2 + 1)
ok([c17.subs(x, t) for t in (-3, 0, 3)] == [R(1, 10), 1, R(1, 10)], "fig 2017 points")
F46 = x**2 + 4 * x
ok([F46.subs(x, t) for t in (-4, -3, -2)] == [0, -3, -4] and croissante(F46, -2, R(23, 20)), "fig 3746")
fa = -2 * x + 5
ok(fa.subs(x, 0) == 5 and fa.subs(x, 3) == -1, "fig cours affine")

# ------------------------------------------------ exécution réelle du code écrit dans le texte
import contextlib  # noqa: E402
import io  # noqa: E402
import re  # noqa: E402
import textwrap  # noqa: E402

ICI = Path(__file__).resolve().parent


def blocs(nom):
    t = (ICI / nom).read_text(encoding="utf-8")
    return [textwrap.dedent(b) for b in re.findall(r"```python\n(.*?)```", t, re.S)]


ns = {}
exec(blocs("cours_225.txt")[0], ns)
ok(repr(ns["maximum"](lambda t: -t**2 + 4 * t, 0, 5, 100)) == "4.0", "exec cours : maximum(f, 0, 5, 100) renvoie 4.0")
prog2024 = blocs("exercices.txt")[0]
for n, attendu in ((4, "2.0 6.0\n"), (8, "2.5 6.25\n")):
    code = prog2024.replace("a, b, n = 0, 4, 4", f"a, b, n = 0, 4, {n}")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(code, {})
    ok(buf.getvalue() == attendu, f"exec 2024 n = {n} : affiche {buf.getvalue()!r}")

print("OK :", N, "contrôles")
