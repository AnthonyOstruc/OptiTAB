# -*- coding: utf-8 -*-
"""Vérification de tous les résultats de la notion « Calcul intégral » (Terminale).

    python verif_calcul-integral.py

Chaque ligne compare la valeur écrite dans le cours, la fiche ou un corrigé à un
calcul exact (sympy) ; les aires sont recalculées avec la valeur absolue
(intégration numérique), les signes et intersections sont contrôlés.
"""
import sympy as sp

x, t = sp.symbols("x t", real=True)
E = sp.E
pi = sp.pi
nb_ok = 0
erreurs = []


def egal(nom, calcule, attendu):
    global nb_ok
    if isinstance(calcule, sp.MatrixBase):
        if calcule.shape == attendu.shape and all(sp.simplify(p - q) == 0 for p, q in zip(calcule, attendu)):
            nb_ok += 1
        else:
            erreurs.append(f"{nom} : calculé {list(calcule)} ≠ écrit {list(attendu)}")
        return
    c, a = sp.nsimplify(sp.simplify(calcule)), sp.nsimplify(sp.simplify(attendu))
    if sp.simplify(c - a) == 0 or abs(float(c) - float(a)) < 1e-12:
        nb_ok += 1
    else:
        erreurs.append(f"{nom} : calculé {c} ≠ écrit {a}")


def proche(nom, calcule, attendu, tol=0.05):
    global nb_ok
    if abs(float(calcule) - float(attendu)) <= tol:
        nb_ok += 1
    else:
        erreurs.append(f"{nom} : calculé {float(calcule):.6f} ≠ écrit {attendu}")


def I(f, a, b, v=x):
    return sp.integrate(f, (v, a, b))


def aire(f, a, b, v=x):
    """Aire géométrique entre la courbe et l'axe (intégrale de |f|), numérique
    (scipy, en coupant l'intervalle aux zéros de f, trouvés indépendamment)."""
    import numpy as np
    from scipy.integrate import quad
    from scipy.optimize import brentq
    g = sp.lambdify(v, f, "numpy")
    a, b = float(a), float(b)
    grille = np.linspace(a, b, 4001)
    vals = g(grille) * np.ones_like(grille)
    coupures = [a]
    for k in range(len(grille) - 1):
        if vals[k] == 0:
            coupures.append(grille[k])
        elif vals[k] * vals[k + 1] < 0:
            coupures.append(brentq(g, grille[k], grille[k + 1], xtol=1e-13, maxiter=1000))
    coupures.append(b)
    return sum(abs(quad(g, u, w, epsabs=1e-13, epsrel=1e-13, limit=200)[0])
               for u, w in zip(coupures, coupures[1:]) if w > u)


def aire_entre(f, g, a, b):
    return aire(f - g, a, b)


# ------------------------------------------------------------------ cours
egal("cours ex. ∫0^2 x²", I(x**2, 0, 2), sp.Rational(8, 3))
egal("cours ex. ∫1^e 1/x", I(1 / x, 1, E), 1)
egal("cours ex. ∫0^1 e^{2x}", I(sp.exp(2 * x), 0, 1), (E**2 - 1) / 2)
egal("cours ex. ∫0^1 (x - x²)", I(x - x**2, 0, 1), sp.Rational(1, 6))
egal("cours ex. ∫0^{2π} sin", I(sp.sin(x), 0, 2 * pi), 0)
proche("cours ex. aire sin sur [0;2π]", aire(sp.sin(x), 0, 2 * pi), 4, 1e-9)
egal("cours ex. valeur moyenne x² sur [0;3]", I(x**2, 0, 3) / 3, 3)
egal("cours ex. IPP ∫0^1 x e^x", I(x * sp.exp(x), 0, 1), 1)
egal("cours ex. IPP ∫1^e ln x", I(sp.log(x), 1, E), 1)
egal("cours ex. ∫1^2 x²", I(x**2, 1, 2), sp.Rational(7, 3))
# encadrement e^{-x²} : 2/3 ≤ ∫0^1 e^{-x²} ≤ 1
egal("cours encadrement ∫0^1 (1 - x²)", I(1 - x**2, 0, 1), sp.Rational(2, 3))
proche("cours ∫0^1 e^{-x²} ≈ 0,7468", I(sp.exp(-x**2), 0, 1).evalf(), 0.7468, 1e-4)
# méthode des rectangles : x² sur [0;2], n = 100 → 2,6268 ; n = 8 : 2,1875 et 3,1875
h = sp.Rational(2, 100)
egal("cours rectangles n = 100", sum((k * h) ** 2 * h for k in range(100)), sp.Rational(26268, 10000))
h = sp.Rational(2, 8)
egal("cours rectangles n = 8 (inférieurs)", sum((k * h) ** 2 * h for k in range(8)), sp.Rational(21875, 10000))
egal("cours rectangles n = 8 (supérieurs)", sum((k * h) ** 2 * h for k in range(1, 9)), sp.Rational(31875, 10000))
proche("cours 8/3 ≈ 2,6667", sp.Rational(8, 3), 2.6667, 1e-4)

# ------------------------------------------------------------------ 1231 intégrales de base
egal("1231 Q1", I(3 * x**2 + 2 * x - 1, 0, 2), 10)
egal("1231 Q2", I(2 * x + 5, 1, 3), 18)
egal("1231 Q3", I(x**3, 0, 1), sp.Rational(1, 4))
egal("1231 Q4", I(x**2 - 3 * x + 2, -1, 2), sp.Rational(9, 2))
F = x**3 / 3 - 3 * x**2 / 2 + 2 * x
egal("1231 Q4 F(2)", F.subs(x, 2), sp.Rational(2, 3))
egal("1231 Q4 F(-1)", F.subs(x, -1), sp.Rational(-23, 6))
egal("1231 Q5", I(sp.sqrt(x), 0, 4), sp.Rational(16, 3))

# ------------------------------------------------------------------ 1232 propriétés
egal("1232 Q1", I(3 * x**2 - 2 * x + 4, 0, 2), 12)
egal("1232 Q2 ∫0^1", I(x**2, 0, 1), sp.Rational(1, 3))
egal("1232 Q2 ∫1^2", I(x**2, 1, 2), sp.Rational(7, 3))
egal("1232 Q2 ∫0^2", I(x**2, 0, 2), sp.Rational(8, 3))
egal("1232 Q3", I(x + 1, 2, 0), -4)
egal("1232 Q4", 2 * 5 + 3 * 2, 16)
egal("1232 Q5", I(x**2 + 1, 1, 1), 0)

# ------------------------------------------------------------------ 1235 aires entre deux courbes
egal("1235 Q1", I(2 * x - x**2, 0, 2), sp.Rational(4, 3))
proche("1235 Q1 |.|", aire_entre(2 * x, x**2, 0, 2), 4 / 3, 1e-9)
egal("1235 Q2", I(x - x**2, 0, 1), sp.Rational(1, 6))
proche("1235 Q2 |.|", aire_entre(x, x**2, 0, 1), 1 / 6, 1e-9)
egal("1235 Q3 partie 1", I(sp.cos(x) - sp.sin(x), 0, pi / 4), sp.sqrt(2) - 1)
egal("1235 Q3 partie 2", I(sp.sin(x) - sp.cos(x), pi / 4, pi / 2), sp.sqrt(2) - 1)
proche("1235 Q3 |.|", aire_entre(sp.sin(x), sp.cos(x), 0, pi / 2), float(2 * sp.sqrt(2) - 2), 1e-9)
egal("1235 Q4", I(sp.exp(x) - 1, 0, 1), E - 2)
proche("1235 Q4 |.|", aire_entre(sp.exp(x), 1, 0, 1), float(E - 2), 1e-9)
egal("1235 Q5 partie 1", I(x**3 - x, -1, 0), sp.Rational(1, 4))
egal("1235 Q5 partie 2", I(x - x**3, 0, 1), sp.Rational(1, 4))
proche("1235 Q5 |.|", aire_entre(x**3, x, -1, 1), 0.5, 1e-9)

# ------------------------------------------------------------------ 1234 aires sous la courbe
egal("1234 Q1", I(x**2, 0, 3), 9)
egal("1234 Q2 intégrale", I(2 * x + 1, -1, 2), 6)
egal("1234 Q2 partie négative", I(2 * x + 1, -1, sp.Rational(-1, 2)), sp.Rational(-1, 4))
egal("1234 Q2 partie positive", I(2 * x + 1, sp.Rational(-1, 2), 2), sp.Rational(25, 4))
proche("1234 Q2 |.|", aire(2 * x + 1, -1, 2), 6.5, 1e-9)
egal("1234 Q3", I(sp.sqrt(x), 0, 4), sp.Rational(16, 3))
egal("1234 Q4", I(sp.sin(x), 0, pi), 2)
egal("1234 Q5", I(sp.exp(x), 0, 1), E - 1)

# ------------------------------------------------------------------ 1239 applications géométriques
egal("1239 Q1 partie 1", I(x**3, -1, 0), sp.Rational(-1, 4))
egal("1239 Q1 partie 2", I(x**3, 0, 2), 4)
proche("1239 Q1 |.|", aire(x**3, -1, 2), 17 / 4, 1e-9)
egal("1239 Q2 intersections", sp.Matrix(sorted(sp.solve(sp.Eq(x**2, 4 * x - x**2), x))), sp.Matrix([0, 2]))
egal("1239 Q2", I(4 * x - 2 * x**2, 0, 2), sp.Rational(8, 3))
proche("1239 Q2 |.|", aire_entre(x**2, 4 * x - x**2, 0, 2), 8 / 3, 1e-9)
egal("1239 Q3 A1", I(sp.cos(x) - sp.sin(x), 0, pi / 4), sp.sqrt(2) - 1)
egal("1239 Q3 A2", I(sp.sin(x) - sp.cos(x), pi / 4, 5 * pi / 4), 2 * sp.sqrt(2))
egal("1239 Q3 A3", I(sp.cos(x) - sp.sin(x), 5 * pi / 4, 2 * pi), 1 + sp.sqrt(2))
proche("1239 Q3 |.|", aire_entre(sp.sin(x), sp.cos(x), 0, 2 * pi), float(4 * sp.sqrt(2)), 1e-9)
egal("1239 Q4", I(sp.exp(x) - sp.exp(-x), 0, 1), E + 1 / E - 2)
egal("1239 Q5 intersections", sp.Matrix(sorted(sp.solve(sp.Eq(x**4 - 2 * x**2, 2 * x**2), x))), sp.Matrix([-2, 0, 2]))
egal("1239 Q5", 2 * I(4 * x**2 - x**4, 0, 2), sp.Rational(128, 15))
egal("1239 Q5 ∫0^2", I(4 * x**2 - x**4, 0, 2), sp.Rational(64, 15))
proche("1239 Q5 |.|", aire_entre(x**4 - 2 * x**2, 2 * x**2, -2, 2), 128 / 15, 1e-9)

# ------------------------------------------------------------------ 1237 forme u'f(u)
egal("1237 Q1", I(2 * x * (x**2 + 1) ** 3, 0, 2), 156)
egal("1237 Q2", I(2 * x / (x**2 + 1), 0, 1), sp.log(2))
egal("1237 Q3", I(x * sp.exp(x**2), 0, 1), (E - 1) / 2)
egal("1237 Q4", I(1 / sp.sqrt(2 * x + 3), 0, 2), sp.sqrt(7) - sp.sqrt(3))
egal("1237 Q5", I(1 / (x + 1) ** 2, 1, 2), sp.Rational(1, 6))
for nom, prim, f in [("Q1", (x**2 + 1) ** 4 / 4, 2 * x * (x**2 + 1) ** 3),
                     ("Q2", sp.log(x**2 + 1), 2 * x / (x**2 + 1)),
                     ("Q3", sp.exp(x**2) / 2, x * sp.exp(x**2)),
                     ("Q4", sp.sqrt(2 * x + 3), 1 / sp.sqrt(2 * x + 3)),
                     ("Q5", -1 / (x + 1), 1 / (x + 1) ** 2)]:
    egal(f"1237 {nom} primitive", sp.diff(prim, x) - f, 0)

# ------------------------------------------------------------------ 1233 exponentielles et trigonométriques
egal("1233 Q1", I(sp.exp(2 * x), 0, 1), (E**2 - 1) / 2)
egal("1233 Q2", I(sp.sin(x), 0, pi / 2), 1)
egal("1233 Q3", I(sp.cos(x), 0, pi), 0)
egal("1233 Q4", I(sp.exp(x) + sp.sin(x), 0, 1), E - sp.cos(1))
egal("1233 Q5", I(sp.exp(-x), -1, 1), E - 1 / E)

# ------------------------------------------------------------------ 1241 fonctions de signe quelconque
egal("1241 Q1 intégrale", I(x**2 - 1, -2, 1), 0)
egal("1241 Q1 A1", I(x**2 - 1, -2, -1), sp.Rational(4, 3))
egal("1241 Q1 A2", I(x**2 - 1, -1, 1), sp.Rational(-4, 3))
proche("1241 Q1 aire", aire(x**2 - 1, -2, 1), 8 / 3, 1e-9)
egal("1241 Q2 intégrale", I(x**3 - x, -1, 2), sp.Rational(9, 4))
egal("1241 Q2 A1", I(x**3 - x, -1, 0), sp.Rational(1, 4))
egal("1241 Q2 A2", I(x**3 - x, 0, 1), sp.Rational(-1, 4))
egal("1241 Q2 A3", I(x**3 - x, 1, 2), sp.Rational(9, 4))
proche("1241 Q2 aire", aire(x**3 - x, -1, 2), 11 / 4, 1e-9)
egal("1241 Q3 intégrale", I(sp.sin(x), 0, 2 * pi), 0)
egal("1241 Q3 A2", I(sp.sin(x), pi, 2 * pi), -2)
proche("1241 Q3 aire", aire(sp.sin(x), 0, 2 * pi), 4, 1e-9)
egal("1241 Q4 intégrale", I(x**2 - 4, -2, 2), sp.Rational(-32, 3))
proche("1241 Q4 aire", aire(x**2 - 4, -2, 2), 32 / 3, 1e-9)
egal("1241 Q5 intégrale", I(x**2 - 4 * x + 3, 0, 3), 0)
egal("1241 Q5 A1", I(x**2 - 4 * x + 3, 0, 1), sp.Rational(4, 3))
egal("1241 Q5 A2", I(x**2 - 4 * x + 3, 1, 3), sp.Rational(-4, 3))
proche("1241 Q5 aire", aire(x**2 - 4 * x + 3, 0, 3), 8 / 3, 1e-9)

# ------------------------------------------------------------------ 1238 intégration par parties
egal("1238 Q1", I(x * sp.exp(x), 0, 1), 1)
egal("1238 Q2", I(x * sp.cos(x), 0, pi / 2), pi / 2 - 1)
egal("1238 Q3", I(sp.log(x), 1, E), 1)
egal("1238 Q4", I(x * sp.exp(2 * x), 0, 1), (E**2 + 1) / 4)
egal("1238 Q4 crochet", (x * sp.exp(2 * x) / 2).subs(x, 1) - 0, E**2 / 2)
egal("1238 Q4 seconde intégrale", I(sp.exp(2 * x), 0, 1) / 2, (E**2 - 1) / 4)
egal("1238 Q5", I(x * sp.sin(x), 0, pi), pi)

# ------------------------------------------------------------------ 1240 modélisation
mu1 = I(1000 * sp.exp(sp.Rational(2, 100) * t), 0, 10, t) / 10
egal("1240 Q1 exact", mu1, 5000 * (sp.exp(sp.Rational(1, 5)) - 1))
proche("1240 Q1 ≈ 1 107", mu1.evalf(), 1107.0, 0.05)
v = 3 * t**2 - 6 * t + 2
egal("1240 Q2 déplacement", I(v, 0, 3, t), 6)
t1, t2 = 1 - 1 / sp.sqrt(3), 1 + 1 / sp.sqrt(3)
egal("1240 Q2 racines", sp.Matrix(sorted(sp.solve(v, t), key=lambda r: float(r))), sp.Matrix([t1, t2]))
dist = aire(v, 0, 3, t)
proche("1240 Q2 distance = 6 + 8√3/9", dist, float(6 + 8 * sp.sqrt(3) / 9), 1e-9)
proche("1240 Q2 distance ≈ 7,54", dist, 7.54, 0.005)
X = t**3 - 3 * t**2 + 2 * t
egal("1240 Q2 x(t1)", X.subs(t, t1), 2 * sp.sqrt(3) / 9)
egal("1240 Q2 x(t2)", X.subs(t, t2), -2 * sp.sqrt(3) / 9)
egal("1240 Q3", I(100 - 2 * x, 0, 50), 2500)
mu4 = I(20 + 80 * sp.exp(-t / 10), 0, 10, t) / 10
egal("1240 Q4 exact", mu4, 100 - 80 / E)
proche("1240 Q4 ≈ 70,6", mu4.evalf(), 70.6, 0.05)
egal("1240 Q4 primitive", sp.diff(20 * t - 800 * sp.exp(-t / 10), t) - (20 + 80 * sp.exp(-t / 10)), 0)
V = 1000 * (1 - t / 24) ** 2
egal("1240 Q5 primitive", sp.diff(-8000 * (1 - t / 24) ** 3, t) - V, 0)
egal("1240 Q5 intégrale", I(V, 0, 12, t), 7000)
egal("1240 Q5 exact", I(V, 0, 12, t) / 12, sp.Rational(1750, 3))
proche("1240 Q5 ≈ 583,3", sp.Rational(1750, 3), 583.3, 0.05)

# ------------------------------------------------------------------ 1236 valeur moyenne
egal("1236 Q1", I(x**2, 0, 3) / 3, 3)
egal("1236 Q2", I(sp.sin(x), 0, pi) / pi, 2 / pi)
egal("1236 Q3", I(sp.exp(x), 0, 1), E - 1)
egal("1236 Q4", I(2 * x + 1, 1, 4) / 3, 6)
egal("1236 Q5", I(sp.cos(x), 0, pi / 2) / (pi / 2), 2 / pi)
proche("1236 2/π ≈ 0,64", 2 / pi, 0.64, 0.005)
proche("1236 e - 1 ≈ 1,72", E - 1, 1.72, 0.005)
# valeur moyenne atteinte (théorème des valeurs intermédiaires) : x² = 3 en √3, etc.
egal("1236 Q1 x² = 3", sp.sqrt(3) ** 2, 3)
egal("1236 Q3 e^x = e - 1", sp.exp(sp.log(E - 1)), E - 1)
egal("1236 Q4 2x + 1 = 6", sp.solve(2 * x + 1 - 6, x)[0], sp.Rational(5, 2))

# ------------------------------------------------------------------ 1242 type bac
f = x**2 - 2 * x + 1
egal("1242 Q1 intégrale", I(f, 0, 3), 3)
egal("1242 Q1 forme", sp.expand((x - 1) ** 2) - f, 0)
egal("1242 Q2", I(sp.exp(x) - 1, 0, 2) / 2, (E**2 - 3) / 2)
egal("1242 Q3", I(x * sp.exp(2 * x), 0, 1), (E**2 + 1) / 4)
egal("1242 Q4", I(2 * x - 2 * x**2, 0, 1), sp.Rational(1, 3))
proche("1242 Q4 |.|", aire_entre(x**2, 2 * x - x**2, 0, 1), 1 / 3, 1e-9)
egal("1242 Q5 intégrale", I(1 / (x + 1), 0, 2), sp.log(3))
egal("1242 Q5 moyenne", I(1 / (x + 1), 0, 2) / 2, sp.log(3) / 2)

# ------------------------------------------------------------------ arrondis écrits dans les corrigés (2 décimales)
for nom, val, ecrit in [
    ("1235 Q3 2√2 - 2", 2 * sp.sqrt(2) - 2, 0.83), ("1235 Q4 e - 2", E - 2, 0.72),
    ("1234 Q5 e - 1", E - 1, 1.72), ("1239 Q1 17/4", sp.Rational(17, 4), 4.25),
    ("1239 Q3 4√2", 4 * sp.sqrt(2), 5.66), ("1239 Q4 e + 1/e - 2", E + 1 / E - 2, 1.09),
    ("1239 Q5 128/15", sp.Rational(128, 15), 8.53), ("1237 Q4 √7 - √3", sp.sqrt(7) - sp.sqrt(3), 0.91),
    ("1233 Q1 (e² - 1)/2", (E**2 - 1) / 2, 3.19), ("1233 Q4 e - cos 1", E - sp.cos(1), 2.18),
    ("1233 Q5 e - 1/e", E - 1 / E, 2.35), ("1238 Q2 π/2 - 1", pi / 2 - 1, 0.57),
    ("1238 Q4 (e² + 1)/4", (E**2 + 1) / 4, 2.10), ("1240 Q2 t1", 1 - sp.sqrt(3) / 3, 0.42),
    ("1240 Q2 t2", 1 + sp.sqrt(3) / 3, 1.58), ("1242 Q2 (e² - 3)/2", (E**2 - 3) / 2, 2.19),
    ("1242 Q3 (e² + 1)/4", (E**2 + 1) / 4, 2.10), ("1242 Q5 ln 3 / 2", sp.log(3) / 2, 0.55),
]:
    proche(nom, sp.N(val), ecrit, 0.005)
egal("1240 Q5 forme u'u² : -24 u' u² = u²", -24 * sp.diff(1 - t / 24, t) * (1 - t / 24) ** 2 - (1 - t / 24) ** 2, 0)
egal("1240 Q2 t1 = (6 - 2√3)/6", (6 - 2 * sp.sqrt(12) / 2) / 6 - (1 - sp.sqrt(3) / 3), 0)
egal("1234 Q2 triangle 1", sp.Rational(1, 2) * sp.Rational(1, 2) * 1, sp.Rational(1, 4))
egal("1234 Q2 triangle 2", sp.Rational(1, 2) * sp.Rational(5, 2) * 5, sp.Rational(25, 4))
egal("1241 Q2 11/4 - 2 × 1/4", sp.Rational(11, 4) - 2 * sp.Rational(1, 4), sp.Rational(9, 4))
egal("cours moyenne f(3/2)", sp.Rational(9, 4), sp.Rational(3, 2) ** 2)
egal("cours moyenne (f(0) + f(3))/2", sp.Rational(9, 2), sp.Rational(0 + 9, 2))
egal("1236 Q4 f(5/2)", 2 * sp.Rational(5, 2) + 1, 6)
egal("1238 Q3 primitive de ln", sp.diff(x * sp.log(x) - x, x) - sp.log(x), 0)

# ------------------------------------------------------------------ valeurs portées sur les figures
proche("figure 2/π", 2 / pi, 0.6366, 1e-4)
proche("figure e - 1", E - 1, 1.7183, 1e-4)
proche("figure √2/2", sp.sqrt(2) / 2, 0.7071, 1e-4)

# ================================================================== FINITION 2026-11-02
# cours : encadrement de e^{-x²}, suite d'intégrales x^n/(1+x), IPP illustrée
egal("cours ∫(1 - x²) sur [0;1]", I(1 - x**2, 0, 1), sp.Rational(2, 3))
proche("cours 2/3 ≤ ∫e^{-x²} ≤ 1", sp.N(sp.Integral(sp.exp(-x**2), (x, 0, 1))), 0.7468, 1e-4)
for k in range(1, 9):
    Jk = sp.N(sp.Integral(x**k / (1 + x), (x, 0, 1)))
    Jk1 = sp.N(sp.Integral(x**(k + 1) / (1 + x), (x, 0, 1)))
    if 0 <= Jk1 <= Jk <= 1 / (k + 1):
        nb_ok += 1
    else:
        erreurs.append(f"cours suite x^n/(1+x) : encadrement faux pour n = {k}")
egal("cours ∫_0^1 x^n = 1/(n+1) (n = 5)", I(x**5, 0, 1), sp.Rational(1, 6))
egal("cours IPP [x ln x]_1^e", (x * sp.log(x)).subs(x, E) - (x * sp.log(x)).subs(x, 1), E)
egal("cours IPP ∫_1^e (1/x)·x", I(1, 1, E), E - 1)
egal("cours IPP aire A2 = ∫_0^1 e^x", I(sp.exp(x), 0, 1), E - 1)
egal("cours IPP ∫_1^e ln x", I(sp.log(x), 1, E), 1)
# aire A2 « à gauche de la courbe de ln » calculée directement : ∫_0^1 e^y dy (domaine {0≤y≤1, 0≤x≤e^y})
egal("cours IPP A1 + A2 = rectangle e × 1", I(sp.log(x), 1, E) + I(sp.exp(t), 0, 1, t), E)

# 1231 Q4 : découpage aux zéros 1 et 2
F = x**3 / 3 - 3 * x**2 / 2 + 2 * x
egal("1231 Q4 F(1)", F.subs(x, 1), sp.Rational(5, 6))
egal("1231 Q4 ∫_{-1}^1", I(x**2 - 3 * x + 2, -1, 1), sp.Rational(14, 3))
egal("1231 Q4 ∫_1^2", I(x**2 - 3 * x + 2, 1, 2), -sp.Rational(1, 6))
egal("1231 Q4 14/3 - 1/6", sp.Rational(14, 3) - sp.Rational(1, 6), sp.Rational(9, 2))
# 1232 Q2 (figure) et 1233 Q3 (remarque + figure)
egal("1232 fig 1/3", I(x**2, 0, 1), sp.Rational(1, 3))
egal("1232 fig 7/3", I(x**2, 1, 2), sp.Rational(7, 3))
egal("1233 Q3 ∫_0^{π/2} cos", I(sp.cos(x), 0, pi / 2), 1)
egal("1233 Q3 ∫_{π/2}^π cos", I(sp.cos(x), pi / 2, pi), -1)
# 1240 Q2 : partie orange (marche arrière) et Q4 : demi-somme
v = 3 * t**2 - 6 * t + 2
t1, t2 = 1 - sp.sqrt(3) / 3, 1 + sp.sqrt(3) / 3
egal("1240 Q2 ∫_{t1}^{t2} v", I(v, t1, t2, t), -4 * sp.sqrt(3) / 9)
proche("1240 Q2 4√3/9 ≈ 0,77", sp.N(4 * sp.sqrt(3) / 9), 0.77, 0.005)
egal("1240 Q2 v(1) = -1 (figure)", v.subs(t, 1), -1)
egal("1240 Q2 v(3) = 11 (figure)", v.subs(t, 3), 11)
T = 20 + 80 * sp.exp(-t / 10)
proche("1240 Q4 (T(0) + T(10))/2 ≈ 74,7", sp.N((T.subs(t, 0) + T.subs(t, 10)) / 2), 74.7, 0.05)
proche("1240 Q4 μ ≈ 70,6 (figure 70,57)", sp.N(I(T, 0, 10, t) / 10), 70.57, 0.005)
# 1242 Q3 réécrite : ∫_1^e x ln x
egal("1242 Q3 ∫_1^e x ln x", I(x * sp.log(x), 1, E), (E**2 + 1) / 4)
egal("1242 Q3 [x²/2 ln x]_1^e", (x**2 / 2 * sp.log(x)).subs(x, E) - 0, E**2 / 2)
egal("1242 Q3 ∫_1^e x/2", I(x / 2, 1, E), (E**2 - 1) / 4)
proche("1242 figure μ (e² - 3)/2", sp.N((E**2 - 3) / 2), 2.1945, 1e-4)
proche("1242 figure μ ln 3 / 2", sp.N(sp.log(3) / 2), 0.5493, 1e-4)

# nouveau-1 : I_n = ∫_0^1 x^n e^x
n = sp.Symbol("n", integer=True, nonnegative=True)
In = [sp.simplify(I(x**k * sp.exp(x), 0, 1)) for k in range(12)]
egal("N1 I0", In[0], E - 1)
for k in range(11):
    egal(f"N1 relation I_{k + 1} = e - {k + 1} I_{k}", In[k + 1], E - (k + 1) * In[k])
egal("N1 I1", In[1], 1)
egal("N1 I2", In[2], E - 2)
egal("N1 I3", In[3], 6 - 2 * E)
proche("N1 I0 ≈ 1,72", sp.N(In[0]), 1.72, 0.005)
proche("N1 I2 ≈ 0,72", sp.N(In[2]), 0.72, 0.005)
proche("N1 I3 ≈ 0,56", sp.N(In[3]), 0.56, 0.005)
for k in range(11):
    if not (1 / (k + 1) <= float(In[k]) <= float(E) / (k + 1) and float(In[k + 1]) <= float(In[k])):
        erreurs.append(f"N1 encadrement / décroissance faux pour n = {k}")
    else:
        nb_ok += 1
# IPP générale (n symbolique) : dérivée de x^{n+1} e^x
egal("N1 (x^{n+1} e^x)' = (n+1)x^n e^x + x^{n+1} e^x",
     sp.diff(x**(n + 1) * sp.exp(x), x) - ((n + 1) * x**n * sp.exp(x) + x**(n + 1) * sp.exp(x)), 0)
proche("N1 (n+1) I_n → e (n = 60)", sp.N(61 * sp.Integral(x**60 * sp.exp(x), (x, 0, 1))), float(E), 0.05)

# nouveau-2 : J = ∫_0^1 1/(1+x²) = π/4, rectangles
f = 1 / (1 + x**2)
egal("N2 f'", sp.diff(f, x), -2 * x / (1 + x**2)**2)
egal("N2 f(1/4)", f.subs(x, sp.Rational(1, 4)), sp.Rational(16, 17))
egal("N2 f(1/2)", f.subs(x, sp.Rational(1, 2)), sp.Rational(4, 5))
egal("N2 f(3/4)", f.subs(x, sp.Rational(3, 4)), sp.Rational(16, 25))
s4 = sp.Rational(1, 4) * sum(f.subs(x, sp.Rational(k, 4)) for k in range(1, 5))
S4 = sp.Rational(1, 4) * sum(f.subs(x, sp.Rational(k, 4)) for k in range(0, 4))
egal("N2 s4", s4, sp.Rational(2449, 3400))
egal("N2 S4", S4, sp.Rational(1437, 1700))
proche("N2 s4 ≈ 0,720", sp.N(s4), 0.720, 0.0005)
proche("N2 S4 ≈ 0,845", sp.N(S4), 0.845, 0.0005)
egal("N2 J = π/4", I(f, 0, 1), pi / 4)
if s4 <= pi / 4 <= S4 and sp.Rational(1, 2) <= pi / 4 <= 1:
    nb_ok += 1
else:
    erreurs.append("N2 encadrements de J faux")
for N in (4, 10, 500):
    sN = sum(sp.Rational(1, N) * f.subs(x, sp.Rational(k + 1, N)) for k in range(N))
    SN = sum(sp.Rational(1, N) * f.subs(x, sp.Rational(k, N)) for k in range(N))
    egal(f"N2 S{N} - s{N} = 1/(2N)", SN - sN, sp.Rational(1, 2 * N))
    if N == 500:
        proche("N2 s500 ≈ 0,784 898", sp.N(sN), 0.784898, 5e-7)
        proche("N2 S500 ≈ 0,785 898", sp.N(SN), 0.785898, 5e-7)
        if 3.139 <= 4 * float(sN) and 4 * float(SN) <= 3.144 and 4 * float(sN) <= float(pi) <= 4 * float(SN):
            nb_ok += 1
        else:
            erreurs.append("N2 encadrement de π faux")
proche("N2 4 × 0,784 898", 4 * 0.784898, 3.139592, 1e-9)
proche("N2 4 × 0,785 898", 4 * 0.785898, 3.143592, 1e-9)
if sp.Rational(1, 2 * 499) > sp.Rational(1, 1000) and sp.Rational(1, 2 * 500) <= sp.Rational(1, 1000):
    nb_ok += 1
else:
    erreurs.append("N2 n = 500 n'est pas le plus petit entier")
# le code Python des corrigés, exécuté réellement
code = '''
def f(x):
    return 1 / (1 + x ** 2)

def rectangles(n):
    h = 1 / n
    s = 0
    S = 0
    for k in range(n):
        s = s + h * f((k + 1) * h)
        S = S + h * f(k * h)
    return s, S
'''
ns = {}
exec(code, ns)
s500, S500 = ns["rectangles"](500)
proche("N2 programme s500", s500, 0.784898, 5e-7)
proche("N2 programme S500", S500, 0.785898, 5e-7)
s4p, S4p = ns["rectangles"](4)
proche("N2 programme s4", s4p, float(s4), 1e-12)
proche("N2 programme S4", S4p, float(S4), 1e-12)

print(f"{nb_ok} contrôle(s) exact(s) ou numérique(s) réussi(s), {len(erreurs)} erreur(s)")
for e in erreurs:
    print("  ✗", e)
raise SystemExit(1 if erreurs else 0)
