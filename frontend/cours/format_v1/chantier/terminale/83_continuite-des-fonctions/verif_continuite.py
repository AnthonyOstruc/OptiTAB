# -*- coding: utf-8 -*-
"""Vérification numérique et symbolique de la notion 83 « Continuité des fonctions ».

    python verif_continuite.py

Chaque résultat du cours, de la fiche et des 5 exercices est recalculé avec
sympy / numpy ; le script s'arrête sur la première erreur (assert).
"""
import math

import numpy as np
import sympy as sp

x, h, a, b, l = sp.symbols("x h a b ell", real=True)
ok = 0


def verifie(cond, msg):
    global ok
    assert cond, msg
    ok += 1
    print("  ✓", msg)


def lim(expr, pt, d="+-"):
    return sp.limit(expr, x, pt, dir=d)


print("== Cours")
# exemple de raccord : f(x) = x + 1 (x < 1), 3 - x (x >= 1)
verifie(lim(x + 1, 1, "-") == 2 and lim(3 - x, 1, "+") == 2 and (3 - 1) == 2, "raccord x+1 / 3-x continu en 1 (valeur 2)")
# partie entière
verifie(math.floor(2.7) == 2 and math.floor(1) == 1 and math.floor(0.99) == 0, "E(2,7)=2, E(1)=1, E(0,99)=0")
verifie(math.floor(1 - 1e-9) == 0, "limite à gauche de E en 1 : 0")
# prolongement (x^2-4)/(x-2)
verifie(lim((x**2 - 4) / (x - 2), 2) == 4, "lim (x²-4)/(x-2) en 2 = 4")
# suite u_{n+1} = sqrt(u_n + 2), u0 = 0
u = [0.0]
for _ in range(60):
    u.append(math.sqrt(u[-1] + 2))
verifie(all(u[k] < u[k + 1] <= 2 for k in range(15)), "suite croissante et majorée par 2 (15 premiers termes)")
ts = np.linspace(0, 2, 20001)
verifie(bool(np.all(np.sqrt(ts + 2) >= ts - 1e-15) and np.all(np.sqrt(ts + 2) <= 2 + 1e-15)),
        "si 0 ≤ u ≤ 2 alors u ≤ √(u+2) ≤ 2 (hérédité de la récurrence)")
verifie(abs(u[-1] - 2) < 1e-12, "suite convergente vers 2")
verifie(set(sp.solve(sp.Eq(l**2 - l - 2, 0), l)) == {2, -1}, "ℓ² − ℓ − 2 = 0 : ℓ = 2 ou ℓ = −1")
print("     u0..u4 =", [round(v, 4) for v in u[:5]])
# x^3 + x - 1
f = x**3 + x - 1
verifie(f.subs(x, 0) == -1 and f.subs(x, 1) == 1, "f(0) = −1, f(1) = 1")
verifie(sp.diff(f, x) == 3 * x**2 + 1, "f'(x) = 3x² + 1 > 0")
alpha = sp.nsolve(f, x, 0.7)
verifie(abs(alpha - 0.6823278038) < 1e-9, f"α ≈ {float(alpha):.6f}")


def dichotomie(fn, a_, b_, e):
    pas = [(a_, b_)]
    while b_ - a_ > e:
        m = (a_ + b_) / 2
        if fn(a_) * fn(m) <= 0:
            b_ = m
        else:
            a_ = m
        pas.append((a_, b_))
    return (a_, b_), pas


res, pas = dichotomie(lambda t: t * t * t + t - 1, 0, 1, 0.001)
verifie(res == (0.681640625, 0.6826171875), f"dichotomie(f, 0, 1, 0.001) = {res}")
verifie(res[0] < alpha < res[1] and res[0] < 0.682 < res[1], "α et 0,682 dans l'encadrement final")
verifie(len(pas) - 1 == 10, "10 étapes (1/2^10 < 0,001)")
print("     étapes 0..5 :", pas[:6])
# 1/x : signes contraires sans annulation
verifie((1 / sp.Integer(-1)) < 0 < (1 / sp.Integer(1)), "1/x : −1 < 0 < 1 sans solution de 1/x = 0")
verifie(((x**2 - 1)**2).subs(x, 2) == 9 and ((x**2 - 1)**2).subs(x, -2) == 9, "(x²−1)² vaut 9 en ±2")

print("== Exercice 868 (vérification de continuité)")
verifie(lim((x**2 - 4) / (x - 2), 2) == 4, "Q1 lim = 4")
g1, g2 = x**2, 2 * x - 1
verifie(g2.subs(x, 1) == 1 and lim(g1, 1, "-") == 1 and lim(g2, 1, "+") == 1, "Q2 g(1) = 1, limites 1 et 1")
verifie(lim(sp.sin(x) / x, 0) == 1 and sp.diff(sp.sin(x), x).subs(x, 0) == 1, "Q3 lim sin x / x = sin'(0) = 1")
verifie(lim((x**2 - 1) / (x - 1), 1) == 2, "Q4 lim (x²−1)/(x−1) = 2 = k(1)")
verifie(lim(sp.Abs(x - 3), 3, "-") == 0 and lim(sp.Abs(x - 3), 3, "+") == 0, "Q5 lim |x−3| = 0 = m(3)")

print("== Exercice 870 (classification)")
verifie(lim(1 / (x - 1), 1, "-") == -sp.oo and lim(1 / (x - 1), 1, "+") == sp.oo, "Q1 −∞ à gauche, +∞ à droite")
verifie(lim(x + 1, 0, "-") == 1 and lim(x - 1, 0, "+") == -1 and (0 - 1) == -1, "Q2 limites 1 et −1, g(0) = −1, saut 2")
verifie(lim(1 / x**2, 0, "-") == sp.oo and lim(1 / x**2, 0, "+") == sp.oo, "Q3 +∞ des deux côtés")
n = sp.symbols("n", integer=True, positive=True)
xn = 1 / (sp.pi / 2 + 2 * n * sp.pi)
yn = 1 / (-sp.pi / 2 + 2 * n * sp.pi)
verifie(sp.limit(xn, n, sp.oo) == 0 and sp.limit(yn, n, sp.oo) == 0, "Q4 x_n → 0 et y_n → 0")
verifie(all(abs(math.sin(1 / float(xn.subs(n, k))) - 1) < 1e-9 and abs(math.sin(1 / float(yn.subs(n, k))) + 1) < 1e-9
            for k in range(1, 30)), "Q4 k(x_n) = 1 et k(y_n) = −1")
verifie(all(float(yn.subs(n, k)) > 0 for k in range(1, 30)), "Q4 y_n > 0 pour n ≥ 1")
verifie(lim(x**2, 1, "-") == 1 and lim(x + 1, 1, "+") == 2, "Q5 limites 1 et 2, m(1) = 2, saut 1")

print("== Exercice 872 (prolongement)")
verifie(sp.expand((x - 2) * (x**2 + 2 * x + 4)) == x**3 - 8, "Q1 x³ − 8 = (x − 2)(x² + 2x + 4)")
verifie(lim((x**3 - 8) / (x - 2), 2) == 12, "Q1 lim = 12")
verifie(lim(sp.sin(2 * x) / x, 0) == 2, "Q2 lim = 2")
verifie(lim(sp.log(1 + x) / x, 0) == 1 and sp.diff(sp.log(1 + x), x).subs(x, 0) == 1, "Q3 lim = 1 (dérivée de ln(1+x) en 0)")
verifie(lim((sp.exp(x) - 1) / x, 0) == 1, "Q4 lim = 1")
verifie(sp.simplify((sp.sqrt(x + 1) - 1) / x - 1 / (sp.sqrt(x + 1) + 1)) == 0, "Q5 conjugué : 1/(√(x+1)+1)")
verifie(lim((sp.sqrt(x + 1) - 1) / x, 0) == sp.Rational(1, 2), "Q5 lim = 1/2")

print("== Exercice 869 (TVI)")
f = x**3 - 3 * x + 1
verifie([f.subs(x, t) for t in (0, 1, 2)] == [1, -1, 3], "Q1 f(0)=1, f(1)=−1, f(2)=3")
racines = sorted(float(r) for r in sp.Poly(f, x).nroots())
verifie(0 < racines[1] < 1 < racines[2] < 2, f"Q1 racines dans [0;2] : {racines[1]:.4f} et {racines[2]:.4f} (et {racines[0]:.4f})")
f = sp.exp(x) - 2 * x
verifie(sp.solve(sp.diff(f, x), x) == [sp.log(2)], "Q2 f'(x) = 0 ⇔ x = ln 2")
mini = sp.simplify(f.subs(x, sp.log(2)))
verifie(sp.simplify(mini - (2 - 2 * sp.log(2))) == 0 and float(mini) > 0, f"Q2 minimum 2 − 2 ln 2 ≈ {float(mini):.4f} > 0")
verifie(f.subs(x, 0) == 1 and abs(float(f.subs(x, 1)) - (math.e - 2)) < 1e-12, "Q2 f(0) = 1, f(1) = e − 2")
verifie(0 < math.log(2) < 1, "Q2 0 < ln 2 < 1")
xs = np.linspace(-5, 5, 200001)
verifie((np.exp(xs) - 2 * xs).min() > 0.61, "Q2 e^x − 2x > 0 sur [−5 ; 5] (aucune solution)")
# Q3 réécrite (finition 2026-11-02) : ln x = 2 − x sur [1 ; 2]
f = sp.log(x) + x - 2
verifie(sp.diff(f, x) == 1 / x + 1, "Q3 f'(x) = 1/x + 1 > 0")
verifie(f.subs(x, 1) == -1 and f.subs(x, 2) == sp.log(2) and float(sp.log(2)) > 0, "Q3 f(1) = −1, f(2) = ln 2 > 0")
verifie(abs(float(f.subs(x, sp.Rational(3, 2))) + 0.095) < 5e-4 and abs(float(f.subs(x, sp.Rational(8, 5))) - 0.070) < 5e-4,
        "Q3 f(1,5) ≈ −0,095 et f(1,6) ≈ 0,070")
al = sp.nsolve(f, x, 1.5)
verifie(1.5 < al < 1.6 and abs(al - 1.557) < 5e-4, f"Q3 α ≈ {float(al):.4f} (figure : 1,5571 ; 0,4429)")
verifie(abs(float(2 - al) - 0.4429) < 1e-4, "Q3 figure : ordonnée du point d'intersection")
f = sp.cos(x) - x
verifie(f.subs(x, 0) == 1 and f.subs(x, sp.pi / 2) == -sp.pi / 2, "Q4 f(0) = 1, f(π/2) = −π/2")
c = sp.nsolve(f, x, 0.7)
verifie(abs(c - 0.7390851332) < 1e-9, f"Q4 solution ≈ {float(c):.6f}")
f = x**4 - 2 * x**2 + 1
verifie(sp.factor(f) == (x - 1)**2 * (x + 1)**2, "Q5 x⁴ − 2x² + 1 = (x² − 1)²")
verifie(set(sp.solve(f, x)) == {-1, 1} and f.subs(x, 2) == 9 and f.subs(x, -2) == 9, "Q5 solutions ±1, f(±2) = 9")

print("== Exercice 871 (applications)")
# Q1 réécrite (finition 2026-11-02) : méthode de Héron
hh = (x + 2 / x) / 2
verifie(set(sp.solve(sp.Eq(l, hh.subs(x, l)), l)) == {-sp.sqrt(2), sp.sqrt(2)}, "Q1 ℓ = h(ℓ) ⇔ ℓ² = 2")
uh = [sp.Integer(1)]
for _ in range(3):
    uh.append(sp.nsimplify((uh[-1] + 2 / uh[-1]) / 2))
verifie(uh[1:] == [sp.Rational(3, 2), sp.Rational(17, 12), sp.Rational(577, 408)], "Q1 u1 = 3/2, u2 = 17/12, u3 = 577/408")
verifie(abs(float(uh[2]) - 1.41667) < 5e-6 and abs(float(uh[3]) - 1.414216) < 5e-7, "Q1 valeurs approchées de u2, u3")
v = 1.0
for _ in range(40):
    v = (v + 2 / v) / 2
    assert v >= 1
verifie(abs(v - math.sqrt(2)) < 1e-15, "Q1 u_n ≥ 1 et u_n → √2 (numérique)")
verifie(sp.solve(sp.diff(hh, x), x) == [sp.sqrt(2)] or sp.sqrt(2) in sp.solve(sp.diff(hh, x), x), "Q1 figure : h minimale en √2")
f = x**5 - 5 * x + 1
verifie(sp.expand(sp.diff(f, x) - 5 * (x - 1) * (x + 1) * (x**2 + 1)) == 0, "Q2 f'(x) = 5(x−1)(x+1)(x²+1)")
verifie(f.subs(x, -1) == 5 and f.subs(x, 1) == -3 and f.subs(x, 0) == 1, "Q2 f(−1)=5, f(1)=−3, f(0)=1")
verifie(sp.limit(f, x, -sp.oo) == -sp.oo and sp.limit(f, x, sp.oo) == sp.oo, "Q2 limites −∞ et +∞")
r5 = sorted(float(sp.re(r)) for r in sp.Poly(f, x).nroots() if abs(sp.im(r)) < 1e-12)
verifie(len(r5) == 3 and r5[0] < -1 < r5[1] < 1 < r5[2], f"Q2 trois racines réelles : {[round(v, 4) for v in r5]}")
verifie(sp.solve(sp.Eq(a * 1 + b, 1 ** 2), b) == [1 - a], "Q3 continuité en 1 ⇔ a + b = 1")
for aa in (2, 0, -1):
    bb = 1 - aa
    verifie(aa * 1 + bb == 1, f"Q3 exemple a = {aa}, b = {bb} : la droite passe par (1 ; 1)")
f = sp.exp(x) - x - 2
verifie(sp.limit(f, x, -sp.oo) == sp.oo and sp.limit(f, x, sp.oo) == sp.oo, "Q4 limites +∞ et +∞")
verifie(sp.limit(sp.exp(x) / x, x, sp.oo) == sp.oo, "Q4 e^x / x → +∞")
verifie(f.subs(x, 0) == -1, "Q4 f(0) = −1")
verifie(float(f.subs(x, -2)) > 0 > float(f.subs(x, -1)) and float(f.subs(x, 1)) < 0 < float(f.subs(x, 2)),
        "Q4 f(−2) > 0 > f(−1) et f(1) < 0 < f(2)")
r1 = sp.nsolve(f, x, -1.8)
r2 = sp.nsolve(f, x, 1.1)
verifie(-2 < r1 < -1 and 1 < r2 < 2, f"Q4 solutions ≈ {float(r1):.4f} et {float(r2):.4f}")
# Q5 réécrite (finition 2026-11-02) : dichotomie pour β
fe = lambda t: math.exp(t) - t - 2


def dicho_beta(a_, b_, e):
    etapes = []
    while b_ - a_ > e:
        m = (a_ + b_) / 2
        etapes.append((a_, b_, m, fe(m)))
        if fe(a_) * fe(m) <= 0:
            b_ = m
        else:
            a_ = m
    return (a_, b_), etapes


res, et = dicho_beta(1, 2, 0.01)
verifie(res == (1.140625, 1.1484375), f"Q5 dichotomie(1, 2, 0.01) = {res}")
verifie(len(et) == 7 and 1 / 2**6 > 0.01 >= 1 / 2**7, "Q5 7 étapes (1/2^6 ≈ 0,016 ; 1/2^7 ≈ 0,0078)")
attendu = [(1, 2, 1.5, 0.98), (1, 1.5, 1.25, 0.24), (1, 1.25, 1.125, -0.045), (1.125, 1.25, 1.1875, 0.092),
           (1.125, 1.1875, 1.15625, 0.022), (1.125, 1.15625, 1.140625, -0.012), (1.140625, 1.15625, 1.1484375, 0.0049)]
for (a1, b1, m1, fm1), (a2, b2, m2, fm2) in zip(et, attendu):
    assert (a1, b1, m1) == (a2, b2, m2) and abs(fm1 - fm2) < 0.0051 * (1 if abs(fm2) > 0.01 else 0.2), (a1, b1, m1, fm1)
verifie(True, "Q5 tableau des étapes (intervalles, milieux, signes et valeurs de f(m))")
verifie(fe(1) < 0 and res[0] < float(r2) < res[1] and 1.14 < float(r2) < 1.15, f"Q5 β ≈ {float(r2):.6f} dans l'encadrement")
verifie(abs(res[1] - res[0] - 0.0078125) < 1e-15, "Q5 amplitude finale 0,0078125")

print("== Données des figures")
print("  sin(2x)/x en ±0,5 :", [round(math.sin(2 * t) / t, 4) for t in (-0.5, 0.5)])
print("  ln(1+x)/x en −0,9 ; 3 :", [round(math.log(1 + t) / t, 4) for t in (-0.9, 3)])
print("  (e^x−1)/x en −3 ; 2 :", [round((math.exp(t) - 1) / t, 4) for t in (-3, 2)])
print("  (√(x+1)−1)/x en −1 ; 4 :", [round((math.sqrt(t + 1) - 1) / t, 4) for t in (-1, 4)])
print("  x⁵ − 5x + 1 : extremums", f.subs(x, -1) if False else (5, -3))
# ====================================================================== Enrichissement 2026-11-02
print("== Enrichissement 2026-11-02")
xs = sp.symbols("x", real=True)
x = xs

print("-- nouveau-1 (lecture graphique)")
A = 2 - sp.Rational(4, 9) * (x + 1) ** 2      # [-4 ; -1]
B = sp.Rational(3, 2) * x + sp.Rational(3, 2)  # ]-1 ; 1]
B2 = -2 * x + 5                                # [1 ; 2[
C = 1 - (x - 2) ** 2 / 3                       # ]2 ; 5]
verifie(A.subs(x, -4) == -2 and A.subs(x, -1) == 2, "A(−4) = −2 et f(−1) = A(−1) = 2")
verifie(lim(B, -1, "+") == 0 and B.subs(x, 1) == 3 and B2.subs(x, 1) == 3, "limite 0 à droite de −1 ; f(1) = 3 des deux morceaux")
verifie(lim(B2, 2, "-") == 1 and lim(C, 2, "+") == 1 and C.subs(x, 5) == -2, "limites 1 et 1 en 2, f(5) = −2 (f(2) = 3 posé)")
verifie(sp.diff(B, x) == sp.Rational(3, 2) and sp.diff(B2, x) == -2, "pentes 3/2 à gauche de 1 et −2 à droite : pas dérivable en 1")
verifie(sp.diff(A, x).subs(x, -2) > 0 and all(sp.diff(A, x).subs(x, t) >= 0 for t in (-4, -3, -2, -1)), "A croissante sur [−4 ; −1]")
verifie(all(sp.diff(C, x).subs(x, t) <= 0 for t in (2, 3, 4, 5)) and sp.solve(sp.Eq(C, 2), x) == [],
        "C décroissante sur ]2 ; 5], C < 1 < 2 : f(x) = 2 sans solution sur [2 ; 5]")
zA = min(float(s) for s in sp.solve(sp.Eq(A, 0), x)); zC = max(float(s) for s in sp.solve(sp.Eq(C, 0), x))
verifie(abs(zA - (-1 - 3 / math.sqrt(2))) < 1e-12 and abs(zC - (2 + math.sqrt(3))) < 1e-12,
        f"figure : A s'annule en {zA:.3f}, C en {zC:.3f} (graduations −3 et 4 déplacées)")

print("-- nouveau-2 (fonctions de référence, partie entière)")
m_ = (2 * x + 1) / (x - 3)
verifie(sp.solve(sp.denom(sp.together(m_)), x) == [3], "m non définie en 3")
verifie(m_.subs(x, 0) == sp.Rational(-1, 3) and m_.subs(x, 4) == 9 and sp.solve(m_, x) == [sp.Rational(-1, 2)],
        "m(0) = −1/3, m(4) = 9, m s'annule seulement en −1/2 ∉ [0 ; 4]")
verifie(all((x ** 2 + 1).subs(x, t) >= 1 for t in (-3, 0, 2)) and sp.solve(sp.Eq(x ** 2 + 1, 0), x) == [], "x² + 1 ≥ 1 > 0")
verifie(math.floor(2.5) == 2 and math.floor(2) == 2 and math.floor(-0.5) == -1, "E(2,5) = 2, E(2) = 2, E(−0,5) = −1")
verifie(math.floor(2 - 1e-9) == 1 and math.floor(2 + 1e-9) == 2, "limites de E en 2 : 1 à gauche, 2 à droite")
verifie(lim(x - 1, 2, "-") == 1 and lim(x - 2, 2, "+") == 0 and 2 - math.floor(2) == 0, "d(2) = 0, limites 1 à gauche et 0 à droite")
verifie(all(abs((t - math.floor(t)) - (t - 1)) < 1e-12 for t in (1.0, 1.5, 1.999)), "d(x) = x − 1 sur [1 ; 2[")

print("-- nouveau-3 (morceaux et paramètres)")
a_ = sp.symbols("a", real=True)
verifie(lim(x ** 2 - 2 * x + a_, 2, "-") == a_ and (3 * x - 1).subs(x, 2) == 5 and sp.solve(sp.Eq(a_, 5), a_) == [5], "f(2) = 5, limite à gauche a : a = 5")
verifie((x ** 2 - 2 * x + 3).subs(x, 2) == 3 and (x ** 2 - 2 * x + 5).subs(x, -1) == 8 and (3 * x - 1).subs(x, 4) == 11,
        "figure : a = 3 s'arrête en (2 ; 3) ; a = 5 part de (−1 ; 8) ; 3x − 1 vaut 11 en 4")
mm = sp.symbols("m", real=True)
gd = (x ** 2 + 3) / (x + 1)
verifie((mm * sp.exp(x - 1)).subs(x, 1) == mm and lim(gd, 1, "+") == 2, "g(1) = m et limite à droite 2 : m = 2")
bb = sp.symbols("b", real=True)
C10 = sp.Rational(5, 2) + sp.Rational(8, 5) * 10
verifie(C10 == sp.Rational(37, 2) and sp.solve(sp.Eq(sp.Rational(6, 5) * 10 + bb, C10), bb) == [sp.Rational(13, 2)], "C(10) = 18,5 = 12 + b : b = 6,5")
verifie(sp.Rational(6, 5) * 25 + sp.Rational(13, 2) == sp.Rational(73, 2), "C(25) = 36,5")
verifie(sp.solve(sp.Eq(sp.Rational(6, 5) * x + sp.Rational(13, 2), sp.Rational(61, 2)), x) == [20] and C10 < sp.Rational(61, 2),
        "C(x) = 30,5 : x = 20 (course de plus de 10 km)")
verifie(sp.Rational(6, 5) * 20 + sp.Rational(13, 2) == sp.Rational(61, 2), "figure : point (20 ; 30,5)")

print("-- nouveau-4 (nombre de solutions, balayage)")
f4 = 2 * x ** 3 - 3 * x ** 2 - 1
verifie(sp.limit(f4, x, -sp.oo) == -sp.oo and sp.limit(f4, x, sp.oo) == sp.oo, "limites −∞ et +∞")
verifie(sp.factor(sp.diff(f4, x)) == 6 * x * (x - 1), "f'(x) = 6x(x − 1)")
verifie(f4.subs(x, 0) == -1 and f4.subs(x, 1) == -2 and f4.subs(x, 2) == 3, "f(0) = −1, f(1) = −2, f(2) = 3")
grille = np.linspace(-50, 1, 200001)
verifie(float(np.max(2 * grille ** 3 - 3 * grille ** 2 - 1)) <= -1 + 1e-12, "sur ]−∞ ; 1], f ≤ −1 (maximum en 0)")
racines = [r for r in sp.Poly(f4, x).nroots() if abs(sp.im(r)) < 1e-12]
alpha4 = float(sp.re(racines[0]))
verifie(len(racines) == 1 and 1.67 < alpha4 < 1.68, f"une seule racine réelle α ≈ {alpha4:.4f} ∈ ]1,67 ; 1,68[")
tab = {1.5: -1, 1.6: -0.488, 1.7: 0.156}
verifie(all(abs(float(f4.subs(x, sp.Rational(str(k)))) - v) < 1e-12 for k, v in tab.items()), "balayage au pas 0,1 : −1 ; −0,488 ; 0,156")
tab2 = {1.66: -0.118, 1.67: -0.052, 1.68: 0.016}
verifie(all(abs(float(f4.subs(x, sp.Rational(str(k)))) - v) < 0.0006 for k, v in tab2.items()), "balayage au pas 0,01 : ≈ −0,118 ; −0,052 ; 0,016")
verifie(sp.expand((x - sp.Rational(1, 2)) * (2 * x ** 2 - 2 * x - 1) - (f4 + sp.Rational(3, 2))) == 0, "f(x) + 1,5 = (x − 0,5)(2x² − 2x − 1)")
sols = sorted(float(s) for s in sp.solve(sp.Eq(f4, sp.Rational(-3, 2)), x))
verifie(len(sols) == 3 and sols[0] < 0 < sols[1] < 1 < sols[2] and abs(sols[1] - 0.5) < 1e-12
        and abs(sols[0] + 0.366) < 5e-4 and abs(sols[2] - 1.366) < 5e-4, f"f(x) = −1,5 : trois solutions {[round(s, 5) for s in sols]}")

print("-- nouveau-5 (suite et point fixe)")
f5 = (5 * x + 4) / (x + 2)
verifie(sp.simplify(sp.diff(f5, x) - 6 / (x + 2) ** 2) == 0, "f'(x) = 6/(x + 2)²")
verifie(f5.subs(x, 4) == 4 and f5.subs(x, 0) == 2, "f(4) = 4 et f(0) = 2 (hérédité : [0 ; 4] → [2 ; 4])")
verifie(set(sp.solve(sp.Eq(f5, x), x)) == {-1, 4} and sp.factor(x ** 2 - 3 * x - 4) == (x - 4) * (x + 1), "points fixes −1 et 4")
us = [sp.Integer(0)]
for _ in range(7):
    us.append(sp.nsimplify(f5.subs(x, us[-1])))
verifie(us[1:4] == [2, sp.Rational(7, 2), sp.Rational(43, 11)] and us[4] == sp.Rational(259, 65), "u1 = 2, u2 = 3,5, u3 = 43/11, u4 = 259/65")
verifie(all(0 <= us[k] <= us[k + 1] <= 4 for k in range(7)), "0 ≤ u_n ≤ u_{n+1} ≤ 4 (7 premiers rangs)")
tab5 = [(3, 3.9091, 0.0909), (4, 3.9846, 0.0154), (5, 3.9974, 0.0026), (6, 3.9996, 0.0004)]
verifie(all(abs(float(us[k]) - u) < 5e-5 and abs(float(4 - us[k]) - e) < 5e-5 for k, u, e in tab5), "tableau des termes et des écarts 4 − u_n")


def seuil(e):
    u, n = 0, 0
    while 4 - u >= e:
        u = (5 * u + 4) / (u + 2)
        n = n + 1
    return n


verifie(seuil(0.001) == 6 and 4 - us[5] >= sp.Rational(1, 1000) > 4 - us[6], "seuil(0.001) renvoie 6 (programme exécuté)")

print("-- nouveau-6 (type examen)")
g6 = x ** 2 - 4 + 2 * sp.log(x)
f6 = x / 2 + (1 - sp.log(x)) / x
verifie(sp.limit(g6, x, 0, "+") == -sp.oo and sp.limit(g6, x, sp.oo) == sp.oo, "g : −∞ en 0, +∞ en +∞")
verifie(sp.simplify(sp.diff(g6, x) - (2 * x + 2 / x)) == 0, "g'(x) = 2x + 2/x")
alpha6 = sp.nsolve(g6, x, 1.7)
verifie(1.71 < alpha6 < 1.72 and g6.subs(x, 1.71) < 0 < g6.subs(x, 1.72), f"α ≈ {float(alpha6):.5f} ∈ ]1,71 ; 1,72[")
verifie(abs(float(g6.subs(x, 1.71)) + 0.003) < 5e-4 and abs(float(g6.subs(x, 1.72)) - 0.043) < 5e-4, "g(1,71) ≈ −0,003 et g(1,72) ≈ 0,043")
verifie(sp.limit(f6, x, 0, "+") == sp.oo and sp.limit(f6, x, sp.oo) == sp.oo and sp.limit(sp.log(x) / x, x, sp.oo) == 0, "f : +∞ en 0 et en +∞")
verifie(sp.simplify(sp.diff((1 - sp.log(x)) / x, x) - (sp.log(x) - 2) / x ** 2) == 0, "((1 − ln x)/x)' = (ln x − 2)/x²")
verifie(sp.simplify(sp.diff(f6, x) - g6 / (2 * x ** 2)) == 0, "f'(x) = g(x)/(2x²)")
L = sp.symbols("L", positive=True)
fa = (L / 2 + (1 - (2 - L ** 2 / 2)) / L)
verifie(sp.simplify(fa - (L - 1 / L)) == 0, "ln α = 2 − α²/2 donne f(α) = α − 1/α")
verifie(abs(float(f6.subs(x, alpha6)) - float(alpha6 - 1 / alpha6)) < 1e-12, f"f(α) ≈ {float(f6.subs(x, alpha6)):.5f} = α − 1/α")
h = lambda t: t - 1 / t  # noqa: E731
verifie(abs(h(1.71) - 1.1252) < 5e-5 and abs(h(1.72) - 1.1386) < 5e-5 and 1.12 < h(1.71) and h(1.72) < 1.14, "h(1,71) ≈ 1,1252, h(1,72) ≈ 1,1386 : 1,12 < f(α) < 1,14")
beta6 = sp.nsolve(f6 - 2, x, 0.8)
gamma6 = sp.nsolve(f6 - 2, x, 4.2)
verifie(abs(beta6 - 0.777) < 5e-4 and abs(gamma6 - 4.208) < 5e-4 and beta6 < alpha6 < gamma6, f"f(x) = 2 : β ≈ {float(beta6):.4f}, γ ≈ {float(gamma6):.4f}")
grille = np.linspace(0.05, 60, 400001)
fg = grille / 2 + (1 - np.log(grille)) / grille
verifie(int(np.sum(np.diff(np.sign(fg - 2)) != 0)) == 2, "f − 2 change de signe exactement deux fois sur ]0 ; 60]")

print("-- figures de l'enrichissement")
import importlib.util  # noqa: E402
from pathlib import Path  # noqa: E402
_spec = importlib.util.spec_from_file_location("fig83", Path(__file__).resolve().parent / "figures" / "figures.py")
_fig = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_fig)
F_ = _fig.FIGURES
verifie(all(s in F_["n1_lecture"] for s in (r"{2-4/9*(x+1)^2}", r"{1.5*x+1.5}", r"{-2*x+5}", r"{1-(x-2)^2/3}", r"\pnt{2}{3}", r"\pntv{2}{1}", r"\pntv{-1}{0}")),
        "figure n1 : morceaux et points conformes à l'énoncé")
verifie(all(s in F_["n4_solutions_corrige"] for s in ("{-0.36603}{-1.5}", "{0.5}{-1.5}", "{1.36603}{-1.5}", "{1.67765}{0}")), "figure n4 : solutions placées")
verifie(abs((1 - math.sqrt(3)) / 2 + 0.36603) < 1e-5 and abs(alpha4 - 1.67765) < 1e-5, "figure n4 : coordonnées exactes")
verifie("(axis cs:3.90909,3.90909)" in F_["n5_escalier_corrige"] and abs(43 / 11 - 3.90909) < 1e-5, "figure n5 : u3 = 43/11")
verifie("{1.71063}{1.12606}" in F_["n6_f_corrige"] and abs(alpha6 - 1.71063) < 1e-5 and abs(f6.subs(x, alpha6) - 1.12606) < 1e-5,
        "figure n6 : minimum (α ; f(α))")
verifie("{0.77707}{2}" in F_["n6_f_corrige"] and "{4.20767}{2}" in F_["n6_f_corrige"] and abs(beta6 - 0.77707) < 1e-5 and abs(gamma6 - 4.20767) < 1e-5,
        "figure n6 : β et γ")

print(f"\n{ok} vérifications : tout est juste.")
