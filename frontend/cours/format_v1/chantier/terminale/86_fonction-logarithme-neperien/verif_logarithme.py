# -*- coding: utf-8 -*-
"""Vérification (sympy / numpy) de tous les résultats de la notion
« Fonction logarithme népérien » (Terminale) : cours, fiche, exercices, figures.

    python verif_logarithme.py      → « 0 échec » attendu
"""
import math

import numpy as np
import sympy as sp

x, y, a, h, t, k, lam = sp.symbols("x y a h t k lambda", real=True)
xp = sp.symbols("xp", positive=True)
E = sp.E
ln = sp.log
echecs = []


def ok(cond, msg):
    if not bool(cond):
        echecs.append(msg)
        print("ÉCHEC :", msg)


def egal(u, v, msg):
    ok(sp.simplify(u - v) == 0, f"{msg} : {u} ≠ {v}")


def proche(u, v, msg, tol=5e-3):
    ok(abs(float(u) - float(v)) < tol, f"{msg} : {float(u)} ≈? {v}")


def solutions(eq, dom):
    return sp.solveset(eq, x, domain=dom)


R = sp.S.Reals
oo = sp.oo

# ------------------------------------------------------------------ cours
egal(ln(8), 3 * ln(2), "ln 8 = 3 ln 2")
egal(sp.expand_log(ln(sp.Rational(1, 9)), force=True), -2 * ln(3), "ln(1/9) = -2 ln 3")
egal(ln(sp.sqrt(E)), sp.Rational(1, 2), "ln sqrt(e) = 1/2")
egal(ln(32), 5 * ln(2), "ln 32 = 5 ln 2")
egal(sp.expand_log(ln(sp.Rational(1, 8)), force=True), -3 * ln(2), "ln(1/8) = -3 ln 2")
ok(solutions(sp.Eq(2 * x - 1, x + 3), sp.Interval.open(sp.Rational(1, 2), oo)) == sp.FiniteSet(4), "ln(2x-1)=ln(x+3) → 4")
proche(math.log(1000) / math.log(2), 9.97, "seuil 2^n > 1000", 5e-3)
ok(2 ** 9 <= 1000 < 2 ** 10, "2^9 ≤ 1000 < 2^10")
proche(math.log(0.001) / math.log(0.8), 30.96, "seuil 0,8^n < 0,001", 5e-3)
ok(0.8 ** 30 >= 0.001 > 0.8 ** 31, "0,8^30 ≥ 0,001 > 0,8^31")
proche(math.log(2) / 5730 * 1e4, 1.21, "λ carbone 14 (×10^4)", 5e-3)
ok(sp.limit(x * ln(x), x, 0, "+") == 0, "x ln x → 0")
ok(sp.limit(ln(x) / x, x, oo) == 0, "ln x / x → 0")
ok(sp.limit(ln(x) / x ** 3, x, oo) == 0, "ln x / x^3 → 0")
ok(sp.limit(ln(1 + x) / x, x, 0) == 1, "ln(1+x)/x → 1")
egal(sp.diff(ln(x ** 2 + 1), x), 2 * x / (x ** 2 + 1), "(ln(x²+1))'")
egal(sp.diff(ln(xp), xp), 1 / xp, "(ln x)' = 1/x")
# tangente en 1 : y = x - 1, et ln x ≤ x - 1
egal(sp.diff(ln(xp), xp).subs(xp, 1), 1, "pente en 1")
xs = np.linspace(0.01, 30, 20000)
ok(np.all(np.log(xs) <= xs - 1 + 1e-12), "ln x ≤ x − 1")
ok(np.all(np.log(xs) < np.sqrt(xs)), "ln x < sqrt(x)")
# demi-vie : N(T)/N0 = 1/2, N(2T)/N0 = 1/4
L14 = math.log(2) / 5730
proche(math.exp(-L14 * 5730), 0.5, "N(T) = N0/2", 1e-12)
proche(math.exp(-L14 * 11460), 0.25, "N(2T) = N0/4", 1e-12)
proche(math.exp(-L14 * 17190), 0.125, "N(3T) = N0/8", 1e-12)
# exemple ln(x) ≤ 2
ok(sp.solveset(ln(x) <= 2, x, sp.Interval.open(0, oo)) == sp.Interval.Lopen(0, E ** 2), "ln x ≤ 2")

# ------------------------------------------------------------------ 1244 puissances
egal(ln(sp.sqrt(E)), sp.Rational(1, 2), "1244 Q1")
egal(ln(E ** 5), 5, "1244 Q2")
egal(ln(1 / E ** 2), -2, "1244 Q3")
egal(ln(sp.root(E, 3)), sp.Rational(1, 3), "1244 Q4")
egal(ln(sp.exp(2 * 3 - 1)), 5, "1244 Q5")

# ------------------------------------------------------------------ 1243 propriétés
egal(ln(8) + ln(2), 4 * ln(2), "1243 Q1")
egal(sp.expand_log(ln(27) - ln(3), force=True), 2 * ln(3), "1243 Q2")
egal(sp.expand_log(2 * ln(5) + 3 * ln(2) - ln(200), force=True), 0, "1243 Q3")
egal(sp.Rational(16, 9) * sp.Rational(3, 4), sp.Rational(4, 3), "1243 Q4")
egal(ln(E ** 3) + ln(E ** -2) - ln(E), 0, "1243 Q5")

# ------------------------------------------------------------------ 1245 dérivées
egal(sp.diff(ln(3 * x + 1), x), 3 / (3 * x + 1), "1245 Q1")
egal(sp.diff(ln(x ** 2 - 4), x), 2 * x / (x ** 2 - 4), "1245 Q2")
egal(sp.diff(xp ** 2 * ln(xp), xp), xp * (2 * ln(xp) + 1), "1245 Q3")
egal(sp.diff(ln(xp) / xp, xp), (1 - ln(xp)) / xp ** 2, "1245 Q4")
egal(sp.diff(ln(sp.sqrt(x ** 2 + 1)), x), x / (x ** 2 + 1), "1245 Q5")
ok(sp.solveset(3 * x + 1 > 0, x, R) == sp.Interval.open(-sp.Rational(1, 3), oo), "1245 D_f")
ok(sp.solveset(x ** 2 - 4 > 0, x, R) == sp.Union(sp.Interval.open(-oo, -2), sp.Interval.open(2, oo)), "1245 D_g")

# ------------------------------------------------------------------ 1247 équations
I1 = sp.Interval.open(sp.Rational(1, 3), oo)
ok(solutions(sp.Eq(x + 2, 3 * x - 1), I1) == sp.FiniteSet(sp.Rational(3, 2)), "1247 Q1")
proche(math.log(3.5), 1.2528, "1247 Q1 ordonnée du point commun", 1e-3)
ok(solutions(sp.Eq(ln(x), 2), sp.Interval.open(0, oo)) == sp.FiniteSet(E ** 2), "1247 Q2")
proche(math.e ** 2, 7.389, "e^2", 1e-3)
# Q3 : domaine x > 2, simplification x + 2, solution e − 2 rejetée
egal(sp.cancel((x ** 2 - 4) / (x - 2)), x + 2, "1247 Q3 simplification")
ok(sp.solveset(x ** 2 - 4 > 0, x, R).intersect(sp.solveset(x - 2 > 0, x, R)) == sp.Interval.open(2, oo), "1247 Q3 domaine")
ok(float(E - 2) < 2, "1247 Q3 e−2 hors domaine")
proche(E - 2, 0.718, "e − 2", 1e-3)
ok(sp.solveset(ln(x ** 2 - 4) - ln(x - 2) - 1, x, sp.Interval.open(2, oo)) == sp.EmptySet, "1247 Q3 S vide")
proche(math.log(4), 1.386, "ln 4", 1e-3)
ok(solutions(sp.Eq(x ** 2 - 1, 8), sp.Interval.open(1, oo)) == sp.FiniteSet(3), "1247 Q4")
proche(math.log(8), 2.079, "ln 8", 1e-3)
ok(sp.solveset(sp.Eq(x ** 2, x ** 2 + 3), x, sp.Interval.open(0, oo)) == sp.EmptySet, "1247 Q5")

# ------------------------------------------------------------------ 1248 inéquations
P = sp.Interval.open(0, oo)
ok(sp.solveset(x + 1 < 2 * x, x, P) == sp.Interval.open(1, oo), "1248 Q1")
proche(math.log(2), 0.693, "ln 2", 1e-3)
ok(sp.solveset(ln(x) >= -1, x, P) == sp.Interval(sp.exp(-1), oo), "1248 Q2")
proche(math.exp(-1), 0.368, "1/e", 1e-3)
ok(sp.solveset(2 * x + 3 <= 1, x, sp.Interval.open(-sp.Rational(3, 2), oo)) == sp.Interval.Lopen(-sp.Rational(3, 2), -1), "1248 Q3")
D4 = sp.Union(sp.Interval.open(-oo, -1), sp.Interval.open(1, oo))
ok(sp.solveset(x ** 2 - 1 > 3, x, D4) == sp.Union(sp.Interval.open(-oo, -2), sp.Interval.open(2, oo)), "1248 Q4")
proche(math.log(3), 1.0986, "ln 3", 1e-3)
ok(sp.solveset(x ** 2 - 2 * x - 8 <= 0, x, sp.Interval.open(2, oo)) == sp.Interval.Lopen(2, 4), "1248 Q5")
egal(sp.expand((x - 4) * (x + 2)), x ** 2 - 2 * x - 8, "1248 Q5 factorisation")

# ------------------------------------------------------------------ 1249 limites
ok(sp.limit(x * ln(x), x, 0, "+") == 0, "1249 Q1")
ok(sp.limit(ln(x) / x, x, oo) == 0, "1249 Q2")
ok(sp.limit(ln(1 + x) / x, x, 0) == 1, "1249 Q3")
ok(sp.limit(x / ln(x), x, oo) == oo, "1249 Q4")
ok(sp.limit(ln(x) / (x - 1), x, 1) == 1, "1249 Q5")

# ------------------------------------------------------------------ 1250 applications
kk = math.log(2) / 3
tt = math.log(100) / kk
proche(tt, 19.93, "1250 Q1 t", 5e-3)
egal(3 * ln(100) / ln(2), 6 * ln(10) / ln(2), "1250 Q1 forme exacte")
n2 = math.log(2) / math.log(1.05)
proche(n2, 14.21, "1250 Q2", 5e-3)
proche(1.05 ** 14, 1.980, "1,05^14", 1e-3)
proche(1.05 ** 15, 2.079, "1,05^15", 1e-3)
ok(1000 * 1.05 ** 14 < 2000 < 1000 * 1.05 ** 15, "1250 Q2 : 15 ans")
proche(1000 * 1.05 ** 14, 1979.93, "C(14)", 1e-2)
proche(1000 * 1.05 ** 15, 2078.93, "C(15)", 1e-2)
ks = sp.solve(sp.Eq(20 + 80 * sp.exp(-10 * k), 60), k)
ok(len(ks) == 1 and sp.simplify(ks[0] - ln(2) / 10) == 0, "1250 Q3 k")
proche(math.log(2) / 10, 0.0693, "1250 Q3 k ≈", 1e-4)
lam_v = math.log(2) / 30
proche(lam_v, 0.0231, "1250 Q4 λ ≈", 1e-4)
proche(math.exp(-100 * lam_v), 0.0992, "1250 Q4 fraction", 1e-4)
egal(sp.exp(-100 * ln(2) / 30), 2 ** sp.Rational(-10, 3), "1250 Q4 forme exacte")
proche(math.exp(8), 2981, "1250 Q5 e^8", 1)

# ------------------------------------------------------------------ 1246 études
f = ln(2 * x - 1)
egal(sp.diff(f, x), 2 / (2 * x - 1), "1246 Q1 f'")
ok(sp.limit(f, x, sp.Rational(1, 2), "+") == -oo and sp.limit(f, x, oo) == oo, "1246 Q1 limites")
g = xp * ln(xp)
egal(sp.diff(g, xp), ln(xp) + 1, "1246 Q2 g'")
egal(g.subs(xp, 1 / E), -1 / E, "1246 Q2 min")
proche(1 / math.e, 0.368, "1246 Q2 1/e", 1e-3)
ok(sp.limit(x * ln(x), x, 0, "+") == 0 and sp.limit(x * ln(x), x, oo) == oo, "1246 Q2 limites")
hh = ln(x ** 2 - 3 * x + 2)
egal(sp.diff(hh, x), (2 * x - 3) / (x ** 2 - 3 * x + 2), "1246 Q3 h'")
ok(sp.solveset(x ** 2 - 3 * x + 2 > 0, x, R) == sp.Union(sp.Interval.open(-oo, 1), sp.Interval.open(2, oo)), "1246 Q3 D")
ok(sp.limit(hh, x, 1, "-") == -oo and sp.limit(hh, x, 2, "+") == -oo, "1246 Q3 limites finies")
ok(sp.limit(hh, x, oo) == oo and sp.limit(hh, x, -oo) == oo, "1246 Q3 limites infinies")
egal(hh.subs(x, 3 - x), hh, "1246 Q3 symétrie x = 3/2")
kf = ln(xp) / xp ** 2
egal(sp.diff(kf, xp), (1 - 2 * ln(xp)) / xp ** 3, "1246 Q4 k'")
egal(kf.subs(xp, sp.sqrt(E)), 1 / (2 * E), "1246 Q4 max")
proche(1 / (2 * math.e), 0.184, "1/(2e)", 1e-3)
ok(sp.limit(ln(x) / x ** 2, x, 0, "+") == -oo and sp.limit(ln(x) / x ** 2, x, oo) == 0, "1246 Q4 limites")
m = ln((x + 1) / (x - 1))
egal(sp.diff(m, x), -2 / ((x - 1) * (x + 1)), "1246 Q5 m'")
ok(sp.solveset((x + 1) / (x - 1) > 0, x, R) == sp.Union(sp.Interval.open(-oo, -1), sp.Interval.open(1, oo)), "1246 Q5 D")
ok(sp.limit(m, x, oo) == 0 and sp.limit(m, x, -oo) == 0, "1246 Q5 limites infinies")
ok(sp.limit(m, x, -1, "-") == -oo and sp.limit(m, x, 1, "+") == oo, "1246 Q5 limites finies")
egal(sp.simplify(((-x + 1) / (-x - 1)) * ((x + 1) / (x - 1))), 1, "1246 Q5 imparité (produit des quotients = 1)")
for xv in (1.3, 2, 5.5, 40):
    proche(float(m.subs(x, -xv) + m.subs(x, xv)), 0, f"1246 Q5 m(−x) = −m(x) en {xv}", 1e-12)

# ------------------------------------------------------------------ 1251 synthèse 1
F = ln(x ** 2 - 4 * x + 3)
egal(sp.diff(F, x), 2 * (x - 2) / ((x - 1) * (x - 3)), "1251 Q1 f'")
ok(sp.solveset(x ** 2 - 4 * x + 3 > 0, x, R) == sp.Union(sp.Interval.open(-oo, 1), sp.Interval.open(3, oo)), "1251 Q1 D")
ok(sp.discriminant(x ** 2 - 4 * x + 3, x) == 4, "1251 Q1 Δ")
ok(sp.limit(F, x, 1, "-") == -oo and sp.limit(F, x, 3, "+") == -oo, "1251 Q1 limites finies")
ok(sp.limit(F, x, oo) == oo and sp.limit(F, x, -oo) == oo, "1251 Q1 limites infinies")
egal(sp.expand(F.subs(x, 4 - x)), sp.expand(F), "1251 Q1 symétrie x = 2")
sol = sp.solve([x * y - 12, x - 3 * y], [x, y], dict=True)
ok({(s[x], s[y]) for s in sol} == {(6, 2), (-6, -2)}, "1251 Q2 système algébrique")
egal(ln(6) + ln(2) - ln(12), 0, "1251 Q2 vérif 1")
egal(sp.expand_log(ln(6) - ln(2) - ln(3), force=True), 0, "1251 Q2 vérif 2")
G = x - ln(1 + x)
egal(sp.diff(G, x), x / (1 + x), "1251 Q3 g'")
ok(sp.limit(G, x, -1, "+") == oo and sp.limit(G, x, oo) == oo, "1251 Q3 limites")
ok(G.subs(x, 0) == 0, "1251 Q3 g(0)")
ok(sp.limit(ln(x ** 2 + 1) / x, x, oo) == 0, "1251 Q4")
egal(sp.expand(xp ** 2 * (1 + 1 / xp ** 2)), xp ** 2 + 1, "1251 Q4 factorisation")
egal(sp.expand_log(ln(xp ** 2) + ln(1 + 1 / xp ** 2) - ln(xp ** 2 * (1 + 1 / xp ** 2)), force=True), 0, "1251 Q4 ln du produit")
# Q5 : nombre de solutions de ln x = a x selon a
H = lambda av: (lambda X: np.log(X) - av * X)
Xs = np.concatenate([np.logspace(-8, 0, 200000), np.linspace(1, 400, 400000)])


def nb_zeros(av):
    v = H(av)(Xs)
    return int(np.sum(np.sign(v[:-1]) * np.sign(v[1:]) < 0))


ok(nb_zeros(-0.5) == 1, "1251 Q5 a = −0,5 : 1 solution")
ok(sp.solveset(sp.Eq(ln(x), 0), x, sp.Interval.open(0, oo)) == sp.FiniteSet(1), "1251 Q5 a = 0 : 1 solution")
ok(nb_zeros(-2) == 1 and nb_zeros(0.3) == 2 and nb_zeros(1) == 0, "1251 Q5 autres valeurs de a")
ok(nb_zeros(0.2) == 2, "1251 Q5 a = 0,2 : 2 solutions")
ok(nb_zeros(0.6) == 0, "1251 Q5 a = 0,6 : 0 solution")
av = float(1 / sp.E)
ok(abs(np.max(H(av)(np.linspace(0.5, 10, 200001)))) < 1e-9, "1251 Q5 a = 1/e : maximum nul (tangence)")
egal((-ln(a) - 1).subs(a, 1 / E), 0, "1251 Q5 max nul pour a = 1/e")
egal(sp.expand_log(ln(1 / a) - 1, force=True), -ln(a) - 1, "1251 Q5 valeur du maximum")
# points de la figure : a = 0,2 → deux solutions
from scipy.optimize import brentq  # noqa: E402
r1 = brentq(lambda X: math.log(X) - 0.2 * X, 1, 5)
r2 = brentq(lambda X: math.log(X) - 0.2 * X, 5, 30)
print(f"   (figure 1251 Q5 : a = 0,2 → x ≈ {r1:.4f} et x ≈ {r2:.4f})")
r3 = brentq(lambda X: math.log(X) + 0.5 * X, 0.1, 2)
print(f"   (figure 1251 Q5 : a = −0,5 → x ≈ {r3:.4f})")

# ------------------------------------------------------------------ 1252 synthèse 2
f2 = ln(xp) - xp + 2
egal(sp.diff(f2, xp), (1 - xp) / xp, "1252 Q1 f'")
egal(f2.subs(xp, 1), 1, "1252 Q2 f(1)")
ok(sp.limit(ln(x) - x + 2, x, 0, "+") == -oo and sp.limit(ln(x) - x + 2, x, oo) == -oo, "1252 Q3 limites")
al = brentq(lambda X: math.log(X) - X + 2, 1e-6, 1)
be = brentq(lambda X: math.log(X) - X + 2, 1, 10)
proche(al, 0.159, "1252 α", 1e-3)
proche(be, 3.146, "1252 β", 1e-3)
ok(math.log(0.15) - 0.15 + 2 < 0 < math.log(0.16) - 0.16 + 2, "1252 encadrement α ∈ ]0,15 ; 0,16[")
ok(math.log(3.14) - 3.14 + 2 > 0 > math.log(3.15) - 3.15 + 2, "1252 encadrement β ∈ ]3,14 ; 3,15[")
print(f"   (1252 : α ≈ {al:.5f}, β ≈ {be:.5f} ; f(0,15) ≈ {math.log(0.15) + 1.85:.4f}, f(0,16) ≈ {math.log(0.16) + 1.84:.4f},"
      f" f(3,14) ≈ {math.log(3.14) - 1.14:.4f}, f(3,15) ≈ {math.log(3.15) - 1.15:.4f})")

# ============================================================== finition 2026-11-02
# 1250 Q5 (nouvelle question) : seuil C_n = 50 × 0,8^n < 5
n_seuil = sp.log(sp.Rational(1, 10)) / sp.log(sp.Rational(4, 5))
proche(float(n_seuil), 10.32, "1250 Q5 ln 0,1 / ln 0,8 ≈ 10,32", 5e-3)
ok(sp.log(sp.Rational(4, 5)) < 0, "1250 Q5 ln 0,8 < 0")
C = lambda m: 50 * 0.8 ** m
proche(C(10), 5.37, "1250 Q5 C10 ≈ 5,37", 5e-3)
proche(C(11), 4.29, "1250 Q5 C11 ≈ 4,29", 5e-3)
ok(C(10) >= 5 > C(11), "1250 Q5 plus petit n = 11")
ok(all(C(m) >= 5 for m in range(11)) and all(C(m) < 5 for m in range(11, 40)), "1250 Q5 suite décroissante sous le seuil")
# 1250 Q3 figure : T(10) = 60, T -> 20
kk = math.log(2) / 10
proche(20 + 80 * math.exp(-10 * kk), 60, "1250 Q3 T(10) = 60", 1e-9)
# 1245 Q2 figure : domaine de ln(x^2 - 4)
ok(sp.solveset(x**2 - 4 > 0, x, sp.S.Reals) == sp.Union(sp.Interval.open(-oo, -2), sp.Interval.open(2, oo)), "1245 domaine")
# 1249 figures : valeurs remarquables
egal((x * ln(x)).diff(x).subs(x, sp.exp(-1)), 0, "1249 x ln x : minimum en 1/e")
egal((ln(x) / x).subs(x, sp.E), sp.exp(-1), "1249 ln x / x : maximum 1/e en e")
egal(sp.diff(ln(1 + x), x).subs(x, 0), 1, "1249 tangente de ln(1+x) en 0 : pente 1")
ok(sp.limit(x * ln(x), x, 0, "+") == 0 and sp.limit(ln(x) / x, x, oo) == 0, "1249 limites des figures")
# 1251 Q5 figure synth1_ax : droites a = 0,3 (deux points), a = 1/e (tangence en (e ; 1)), a = −0,5 (un point)
proche(brentq(lambda X: math.log(X) - 0.3 * X, 1, 3), 1.63134, "1251 fig a = 0,3 : 1er point", 1e-4)
proche(brentq(lambda X: math.log(X) - 0.3 * X, 3, 30), 5.93779, "1251 fig a = 0,3 : 2e point", 1e-4)
proche(brentq(lambda X: math.log(X) + 0.5 * X, 0.1, 2), 0.7035, "1251 fig a = −0,5 : point", 1e-4)
egal(sp.log(sp.E) - sp.E / sp.E, 0, "1251 fig a = 1/e : (e ; 1) sur les deux courbes")
# 1252 figures : f(1) = 1 maximum, zéros α et β utilisés sur les deux figures
proche(math.log(0.15859) - 0.15859 + 2, 0, "1252 fig f(α) ≈ 0", 1e-4)
proche(math.log(3.14619) - 3.14619 + 2, 0, "1252 fig f(β) ≈ 0", 1e-4)
# 1250 Q5 figure : légendes C10 ≈ 5,37 et C11 ≈ 4,29 (arrondis au centième)
ok(round(C(10), 2) == 5.37 and round(C(11), 2) == 4.29, "1250 fig arrondis C10 et C11")

print(f"\n{len(echecs)} échec(s)")
