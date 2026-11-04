# -*- coding: utf-8 -*-
"""Vérification (sympy) de tous les résultats de la notion « Fonction exponentielle »
(Terminale) : cours 89, fiche 30 et les 13 exercices.

    python verif_fonction_exponentielle.py      → « TOUT EST JUSTE » ou la liste des erreurs
"""
import sympy as sp

x, t, X = sp.symbols("x t X", real=True)
E = sp.E
erreurs = []


def egal(nom, a, b):
    if sp.simplify(sp.expand(a - b)) != 0:
        erreurs.append(f"{nom} : {sp.simplify(a)} ≠ {sp.simplify(b)}")


def proche(nom, valeur, attendu, tol=5e-3):
    v = float(valeur)
    if abs(v - attendu) > tol:
        erreurs.append(f"{nom} : {v} ≠ {attendu}")


def limite(nom, expr, point, attendu, dir="+"):
    l = sp.limit(expr, x, point, dir=dir) if point not in (sp.oo, -sp.oo) else sp.limit(expr, x, point)
    if l != attendu:
        erreurs.append(f"{nom} : limite {l} ≠ {attendu}")


def ensemble(nom, rel, attendu, domaine=sp.S.Reals):
    s = sp.solveset(rel, x, domaine)
    if s != attendu:
        erreurs.append(f"{nom} : solutions {s} ≠ {attendu}")


def signe_change(nom, expr, a, gauche, droite, eps=1e-3):
    g, d = float(expr.subs(x, a - eps)), float(expr.subs(x, a + eps))
    if (g > 0) != (gauche == "+") or (d > 0) != (droite == "+"):
        erreurs.append(f"{nom} : signes autour de {a} = {g:+.3g} / {d:+.3g}")


# ============================================================== COURS 89
exp = sp.exp
egal("cours exemple e^{2x}>=e^{1-x}", sp.solve(sp.Eq(2 * x, 1 - x), x)[0], sp.Rational(1, 3))
limite("cours lim +oo e^x", exp(x), sp.oo, sp.oo)
limite("cours lim -oo e^x", exp(x), -sp.oo, 0)
limite("cours lim (e^x-1)/x", (exp(x) - 1) / x, 0, 1)
for n in (1, 2, 3, 5):
    limite(f"croiss. comp. e^x/x^{n}", exp(x) / x**n, sp.oo, sp.oo)
    limite(f"croiss. comp. x^{n}e^-x", x**n * exp(-x), sp.oo, 0)
    limite(f"croiss. comp. x^{n}e^x en -oo", x**n * exp(x), -sp.oo, 0)
# démonstration n = 1 : phi = e^x - x^2/2 croissante sur [0;+oo[, phi(0) = 1
phi = exp(x) - x**2 / 2
egal("démo phi'", sp.diff(phi, x), exp(x) - x)
egal("démo phi(0)", phi.subs(x, 0), 1)
# cas général : e^x/x^n = (1/n^n) (e^{x/n}/(x/n))^n
for n in (2, 3, 4):
    egal(f"démo réécriture n={n}", exp(x) / x**n, (sp.Integer(1) / n**n) * (exp(x / n) / (x / n))**n)
# méthode : e^x - x^2 = e^x (1 - x^2/e^x)
egal("méthode factorisation", exp(x) * (1 - x**2 / exp(x)), exp(x) - x**2)
limite("méthode e^x - x^2", exp(x) - x**2, sp.oo, sp.oo)
# exemples de limites
limite("ex e^{2x}-e^x", exp(2 * x) - exp(x), sp.oo, sp.oo)
limite("ex (x+1)/e^x", (x + 1) / exp(x), sp.oo, 0)
limite("ex x^2 e^x en -oo", x**2 * exp(x), -sp.oo, 0)
# e^u
egal("(e^{-x^2})'", sp.diff(exp(-x**2), x), -2 * x * exp(-x**2))
limite("e^{-x^2} en +oo", exp(-x**2), sp.oo, 0)
limite("e^{-x^2} en -oo", exp(-x**2), -sp.oo, 0)
egal("(e^{x^2})'", sp.diff(exp(x**2), x), 2 * x * exp(x**2))
egal("(e^{3x-1})'", sp.diff(exp(3 * x - 1), x), 3 * exp(3 * x - 1))
# étude de x e^{-x}
f = x * exp(-x)
limite("étude f en -oo", f, -sp.oo, -sp.oo)
limite("étude f en +oo", f, sp.oo, 0)
egal("étude f'", sp.diff(f, x), (1 - x) * exp(-x))
egal("étude f''", sp.diff(f, x, 2), (x - 2) * exp(-x))
egal("étude f(1)", f.subs(x, 1), 1 / E)
egal("étude f(2)", f.subs(x, 2), 2 / E**2)
proche("1/e ≈ 0,37", 1 / E, 0.37)
proche("2/e^2 ≈ 0,27", 2 / E**2, 0.27)
signe_change("étude f' en 1", sp.diff(f, x), 1, "+", "-")
signe_change("étude f'' en 2", sp.diff(f, x, 2), 2, "-", "+")
# modèle condensateur
u = 5 * (1 - exp(-t / 2))
egal("u(0)", u.subs(t, 0), 0)
egal("u'(t)", sp.diff(u, t), sp.Rational(5, 2) * exp(-t / 2))
if sp.limit(u, t, sp.oo) != 5:
    erreurs.append("lim u")
proche("u(4) ≈ 4,32", u.subs(t, 4), 4.32)
proche("u(2) ≈ 3,16", u.subs(t, 2), 3.16)
proche("e ≈ 2,718", E, 2.718, 5e-4)

# ============================================================== FICHE 30
egal("fiche (e^{ax+b})'", sp.diff(exp(3 * x + 2), x), 3 * exp(3 * x + 2))
uu, vv = x**2 + 1, -x
egal("fiche (u e^v)'", sp.diff(uu * exp(vv), x), (sp.diff(uu, x) + uu * sp.diff(vv, x)) * exp(vv))

# ============================================================== EX 1210 dérivées
egal("1210 Q1", sp.diff(exp(x), x), exp(x))
egal("1210 Q2", sp.diff(exp(3 * x), x), 3 * exp(3 * x))
egal("1210 Q3", sp.diff(exp(-2 * x + 1), x), -2 * exp(-2 * x + 1))
egal("1210 Q4", sp.diff(5 * exp(2 * x), x), 10 * exp(2 * x))
egal("1210 Q5", sp.diff(exp(x**2), x), 2 * x * exp(x**2))

# ============================================================== EX 1209 limites
limite("1209 Q1", exp(x), sp.oo, sp.oo)
limite("1209 Q2", exp(x), -sp.oo, 0)
limite("1209 Q3", (exp(x) - 1) / x, 0, 1)
if not (E**2 < E**3):
    erreurs.append("1209 Q5")
proche("e^2 ≈ 7,39", E**2, 7.39)
proche("e^3 ≈ 20,09", E**3, 20.09)

# ============================================================== EX 1208 algèbre
egal("1208 Q1", exp(2 * x + 3) * exp(-x), exp(x + 3))
egal("1208 Q2", exp(3 * x) / exp(2 * x + 1), exp(x - 1))
egal("1208 Q3", exp(x)**2 * exp(-3 * x), exp(-x))
egal("1208 Q4", exp(x) * exp(-x), 1)
egal("1208 Q5", exp(x + 2) * exp(3 * x - 1) / exp(2 * x), exp(2 * x + 1))

# ============================================================== EX 1212 équations
ensemble("1212 Q1", sp.Eq(exp(2 * x + 1), exp(x - 3)), sp.FiniteSet(-4))
ensemble("1212 Q2", sp.Eq(exp(x), 5), sp.FiniteSet(sp.log(5)))
proche("ln 5 ≈ 1,609", sp.log(5), 1.609, 5e-4)
ensemble("1212 Q3", sp.Eq(exp(2 * x) - 4 * exp(x) + 3, 0), sp.FiniteSet(0, sp.log(3)))
egal("1212 Q3 factorisation", (X - 1) * (X - 3), X**2 - 4 * X + 3)
proche("ln 3 ≈ 1,099", sp.log(3), 1.099, 5e-4)
ensemble("1212 Q4", exp(x - 1) < exp(2 * x + 3), sp.Interval.open(-4, sp.oo))
ensemble("1212 Q5", exp(x) >= 7, sp.Interval(sp.log(7), sp.oo))
proche("ln 7 ≈ 1,946", sp.log(7), 1.946, 5e-4)
# figure Q3 : minimum de e^{2x}-4e^x+3 en x = ln 2, valeur -1
g3 = exp(2 * x) - 4 * exp(x) + 3
egal("1212 fig Q3 min", g3.subs(x, sp.log(2)), -1)
egal("1212 fig Q3 lim -oo", sp.limit(g3, x, -sp.oo), 3)

# ============================================================== EX 1217 croissances comparées
f = exp(x) - x
g = exp(x) / x
egal("1217 f'", sp.diff(f, x), exp(x) - 1)
egal("1217 g'", sp.diff(g, x), exp(x) * (x - 1) / x**2)
limite("1217 f +oo", f, sp.oo, sp.oo)
limite("1217 f -oo", f, -sp.oo, sp.oo)
limite("1217 g 0+", g, 0, sp.oo, "+")
limite("1217 g +oo", g, sp.oo, sp.oo)
egal("1217 f(0)", f.subs(x, 0), 1)
egal("1217 g(1)", g.subs(x, 1), E)
signe_change("1217 f' en 0", sp.diff(f, x), 0, "-", "+")
signe_change("1217 g' en 1", sp.diff(g, x), 1, "-", "+")

# ============================================================== EX 1213 x e^x
g = x * exp(x)
egal("1213 g'", sp.diff(g, x), (1 + x) * exp(x))
signe_change("1213 g' en -1", sp.diff(g, x), -1, "-", "+")
egal("1213 g(-1)", g.subs(x, -1), -1 / E)
limite("1213 +oo", g, sp.oo, sp.oo)
limite("1213 -oo", g, -sp.oo, 0)
egal("1213 tangente", g.subs(x, 0) + sp.diff(g, x).subs(x, 0) * x, x)
proche("-1/e ≈ -0,37", -1 / E, -0.37)

# ============================================================== EX 1216 avancées
ensemble("1216 Q1", sp.Eq(exp(2 * x) - 5 * exp(x) + 6, 0), sp.FiniteSet(sp.log(2), sp.log(3)))
egal("1216 Q1 factorisation", (X - 2) * (X - 3), X**2 - 5 * X + 6)
proche("ln 2 ≈ 0,693", sp.log(2), 0.693, 5e-4)
g1 = exp(2 * x) - 5 * exp(x) + 6
egal("1216 fig Q1 min", g1.subs(x, sp.log(sp.Rational(5, 2))), -sp.Rational(1, 4))
ensemble("1216 Q2", sp.Eq(x**2, 3 * x - 2), sp.FiniteSet(1, 2))
ensemble("1216 Q3", exp(2 * x) - 3 * exp(x) + 2 <= 0, sp.Interval(0, sp.log(2)))
egal("1216 Q3 factorisation", (X - 1) * (X - 2), X**2 - 3 * X + 2)
# Q4 : e^{x+1} > 2 e^{x-1}  <=>  e^2 > 2 : vrai pour tout x
egal("1216 Q4 réécriture", exp(x + 1), E**2 * exp(x - 1))
if not (E**2 > 2):
    erreurs.append("1216 Q4")
ensemble("1216 Q4", exp(x + 1) - 2 * exp(x - 1) > 0, sp.S.Reals)
ensemble("1216 Q5", x**2 - 4 * x + 3 >= 0, sp.Union(sp.Interval(-sp.oo, 1), sp.Interval(3, sp.oo)))
egal("1216 Q5 factorisation", (x - 1) * (x - 3), x**2 - 4 * x + 3)
egal("1216 fig Q5 min", exp(x**2 - 4 * x + 3).subs(x, 2), exp(-1))

# ============================================================== EX 1218 logarithme
s1 = sp.log(E**2 + 1) / 2
egal("1218 Q1 vérif", sp.log(exp(2 * s1) - 1), 2)
if not (s1 > 0):
    erreurs.append("1218 Q1 domaine")
proche("1218 Q1 ≈ 1,06", s1, 1.06)
ensemble("1218 Q2", sp.Eq(x + 1, 3), sp.FiniteSet(2))
ensemble("1218 Q3", sp.Eq(x**2 - 1, x + 1), sp.FiniteSet(-1, 2))
dom3 = sp.solveset(x**2 - 1 > 0, x, sp.S.Reals).intersect(sp.solveset(x + 1 > 0, x, sp.S.Reals))
if dom3 != sp.Interval.open(1, sp.oo):
    erreurs.append(f"1218 Q3 domaine : {dom3}")
ensemble("1218 Q4", sp.Eq(x**2 - 3 * x + 2, 0), sp.FiniteSet(1, 2))
ensemble("1218 Q5", exp(x) - 1 >= E, sp.Interval(sp.log(E + 1), sp.oo))
proche("ln(e+1) ≈ 1,31", sp.log(E + 1), 1.31)
ensemble("1218 domaine Q5", exp(x) - 1 > 0, sp.Interval.open(0, sp.oo))

# ============================================================== EX 1211 étude complète
f = exp(2 * x) - 3 * exp(x) + 2
egal("1211 f'", sp.diff(f, x), 2 * exp(2 * x) - 3 * exp(x))
egal("1211 f' factorisée", sp.diff(f, x), exp(x) * (2 * exp(x) - 3))
signe_change("1211 f' en ln(3/2)", sp.diff(f, x), sp.log(sp.Rational(3, 2)), "-", "+")
egal("1211 min", f.subs(x, sp.log(sp.Rational(3, 2))), -sp.Rational(1, 4))
proche("ln(3/2) ≈ 0,405", sp.log(sp.Rational(3, 2)), 0.405, 5e-4)
ensemble("1211 Q4", sp.Eq(f, 0), sp.FiniteSet(0, sp.log(2)))
ensemble("1211 Q5", f >= 0, sp.Union(sp.Interval(-sp.oo, 0), sp.Interval(sp.log(2), sp.oo)))
limite("1211 +oo", f, sp.oo, sp.oo)
limite("1211 -oo", f, -sp.oo, 2)
egal("1211 factorisation +oo", exp(2 * x) * (1 - 3 / exp(x) + 2 / exp(2 * x)), f)
# position par rapport à l'asymptote y = 2 : f - 2 = e^x (e^x - 3) < 0 pour x < ln 3
egal("1211 f-2", f - 2, exp(x) * (exp(x) - 3))

# ============================================================== EX 1220 convexité
f = exp(-x**2)
egal("1220 f'", sp.diff(f, x), -2 * x * exp(-x**2))
egal("1220 f''", sp.diff(f, x, 2), 2 * (2 * x**2 - 1) * exp(-x**2))
r = sp.sqrt(2) / 2
signe_change("1220 f'' en -r", sp.diff(f, x, 2), -r, "+", "-")
signe_change("1220 f'' en r", sp.diff(f, x, 2), r, "-", "+")
egal("1220 f(r)", f.subs(x, r), 1 / sp.sqrt(E))
proche("1/sqrt(e) ≈ 0,61", 1 / sp.sqrt(E), 0.61)
proche("sqrt2/2 ≈ 0,71", r, 0.71)
limite("1220 +oo", f, sp.oo, 0)
limite("1220 -oo", f, -sp.oo, 0)
# tangente au point d'inflexion d'abscisse r : pente f'(r) = -sqrt(2)/sqrt(e)
egal("1220 pente inflexion", sp.diff(f, x).subs(x, r), -sp.sqrt(2) * exp(-sp.Rational(1, 2)))
egal("1220 f'(0) = 0, max 1", f.subs(x, 0), 1)

# ============================================================== EX 1214 composée
h = exp(x**2 - 2 * x)
egal("1214 h'", sp.diff(h, x), 2 * (x - 1) * exp(x**2 - 2 * x))
signe_change("1214 h' en 1", sp.diff(h, x), 1, "-", "+")
egal("1214 h(1)", h.subs(x, 1), 1 / E)
limite("1214 +oo", h, sp.oo, sp.oo)
limite("1214 -oo", h, -sp.oo, sp.oo)
egal("1214 symétrie h(2-x)=h(x)", h.subs(x, 2 - x), h)

# ============================================================== EX 1219 modélisation
N = 1000 * exp(sp.Rational(1, 50) * t)
egal("1219 N(0)", N.subs(t, 0), 1000)
proche("1219 N(50) ≈ 2718,28", N.subs(t, 50), 2718.28, 0.01)
t2 = sp.solve(sp.Eq(N, 2000), t)[0]
egal("1219 doublement", t2, 50 * sp.log(2))
proche("1219 50 ln 2 ≈ 34,66", t2, 34.66)
egal("1219 N'", sp.diff(N, t), 20 * exp(sp.Rational(1, 50) * t))
egal("1219 N' = 0,02 N", sp.diff(N, t), sp.Rational(1, 50) * N)
t10 = sp.solve(sp.Eq(N, 10000), t)[0]
egal("1219 N = 10000", t10, 50 * sp.log(10))
proche("1219 50 ln 10 ≈ 115,13", t10, 115.13)
proche("1219 N'(0) = 20", sp.diff(N, t).subs(t, 0), 20)
proche("1219 N'(50) ≈ 54,4", sp.diff(N, t).subs(t, 50), 54.37, 0.01)

# ============================================================== EX 1215 optimisation
k = x**2 * exp(-x)
egal("1215 k'", sp.diff(k, x), x * (2 - x) * exp(-x))
signe_change("1215 k' en 2", sp.diff(k, x), 2, "+", "-")
egal("1215 k(2)", k.subs(x, 2), 4 / E**2)
proche("4/e^2 ≈ 0,54", 4 / E**2, 0.54)
egal("1215 k(0)", k.subs(x, 0), 0)
limite("1215 +oo", k, sp.oo, 0)
if not all(float(sp.diff(k, x).subs(x, v)) > 0 for v in (0.1, 1, 1.9)):
    erreurs.append("1215 croissance sur ]0;2[")

# ============================================================== finition 2026-11-02 : nouvelles figures
# cours / fiche : croissances comparées e^x et x^3
a1 = sp.nsolve(sp.exp(x) - x**3, x, 1.8)
a2 = sp.nsolve(sp.exp(x) - x**3, x, 4.5)
proche("croissances : 1re intersection ≈ 1,86", a1, 1.857, 1e-3)
proche("croissances : 2e intersection ≈ 4,54", a2, 4.5364, 1e-4)
proche("croissances : ordonnée ≈ 93,35", sp.exp(a2), 93.354, 1e-3)
for v in (2.5, 3, 4, 4.5):
    if not float(v**3) > float(sp.exp(v)):
        erreurs.append(f"croissances : x^3 > e^x attendu en {v}")
for v in (4.6, 5, 6, 10, 20):
    if not float(sp.exp(v)) > float(v**3):
        erreurs.append(f"croissances : e^x > x^3 attendu en {v}")
# 1209 : tangente en 0, sécante (AM), asymptote
egal("1209 tangente en 0", sp.diff(sp.exp(x), x).subs(x, 0) * x + 1, x + 1)
proche("1209 pente de (AM) = e - 1", E - 1, 1.71828, 1e-5)
limite("1209 asymptote -oo", sp.exp(x), -sp.oo, 0)
limite("1209 taux en 0", (sp.exp(x) - 1) / x, 0, 1)
# 1210 : signes des dérivées
egal("1210 g'", sp.diff(sp.exp(3 * x), x), 3 * sp.exp(3 * x))
egal("1210 h'", sp.diff(sp.exp(-2 * x + 1), x), -2 * sp.exp(-2 * x + 1))
egal("1210 h(0) = e", sp.exp(-2 * x + 1).subs(x, 0), E)
# figure optim_max : maximum 4/e^2 en 2
proche("optim_max 4/e^2", 4 / E**2, 0.54134, 1e-5)

# ============================================================== bilan
if erreurs:
    print(f"{len(erreurs)} ERREUR(S) :")
    for e in erreurs:
        print("  ✗", e)
    raise SystemExit(1)
print("TOUT EST JUSTE : cours, fiche et 13 exercices vérifiés.")
