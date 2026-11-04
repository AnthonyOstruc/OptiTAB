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
print(f"\n{ok} vérifications : tout est juste.")
