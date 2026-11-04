# -*- coding: utf-8 -*-
"""Vérification de tous les résultats de la notion « Équations différentielles ».

    python verif_equations-differentielles.py

Chaque résultat du cours, de la fiche et des exercices est recalculé avec sympy
(dsolve pour les équations, valeurs exactes puis approchées). Le script s'arrête
sur la première incohérence (assert).
"""
import sympy as sp

x, t = sp.symbols("x t", real=True)
C = sp.Symbol("C")
y = sp.Function("y")


def resout(eq, ic=None, var=x):
    """Solution de l'équation (forme y' = …) avec condition initiale éventuelle."""
    sol = sp.dsolve(sp.Eq(y(var).diff(var), eq(y(var), var)), y(var), ics=ic)
    return sp.simplify(sol.rhs)


def egal(a, b):
    return sp.simplify(sp.expand(a - b)) == 0


def approx(v, n=6):
    return float(sp.N(v, 15))


def verifie(nom, expr, attendu, tol=None):
    if tol is None:
        assert egal(expr, attendu), f"{nom} : {expr} != {attendu}"
        print(f"  ok  {nom} : {sp.simplify(expr)}")
    else:
        v = approx(expr)
        assert abs(v - attendu) <= tol, f"{nom} : {v} != {attendu}"
        print(f"  ok  {nom} : {v:.6g} (≈ {attendu})")


print("== COURS")
# I. y' = 2x
verifie("primitives de 2x", resout(lambda Y, X: 2 * X, {y(0): C}), x**2 + C)
f = 3 * sp.exp(2 * x)
verifie("3e^{2x} solution de y'=2y", f.diff(x) - 2 * f, 0)
# II. y' = ay
a = sp.Symbol("a", nonzero=True)
verifie("y'=ay", resout(lambda Y, X: a * Y, {y(0): C}), C * sp.exp(a * x))
verifie("y'=3y, y(0)=2", resout(lambda Y, X: 3 * Y, {y(0): 2}), 2 * sp.exp(3 * x))
verifie("y'=-2y", resout(lambda Y, X: -2 * Y, {y(0): C}), C * sp.exp(-2 * x))
# démonstration : g = f e^{-ax}, g' = (f' - a f) e^{-ax}
F = sp.Function("f")
g = F(x) * sp.exp(-a * x)
verifie("dérivée de g", g.diff(x) - (F(x).diff(x) - a * F(x)) * sp.exp(-a * x), 0)
# III. y' = ay + b
b = sp.Symbol("b")
sol = resout(lambda Y, X: a * Y + b, {y(0): C - b / a})
verifie("y'=ay+b", sol, C * sp.exp(a * x) - b / a)
verifie("y'=-0,5y+2, y(0)=0", resout(lambda Y, X: -sp.Rational(1, 2) * Y + 2, {y(0): 0}),
        4 - 4 * sp.exp(-x / 2))
verifie("2y'+y=1 -> y'=-y/2+1/2, constante 1",
        resout(lambda Y, X: -Y / 2 + sp.Rational(1, 2), {y(0): C + 1}), C * sp.exp(-x / 2) + 1)
# famille de la figure : 4 + K e^{-x/2}
for K in (4, 2, -2, -4):
    h = 4 + K * sp.exp(-x / 2)
    verifie(f"courbe K={K} solution", h.diff(x) - (-h / 2 + 2), 0)
# figure y' = 0,5 y : C e^{x/2}
for K in (2, 1, sp.Rational(1, 2), -sp.Rational(1, 2), -1):
    h = K * sp.exp(x / 2)
    verifie(f"courbe C={K} solution de y'=0,5y", h.diff(x) - h / 2, 0)
# IV. y' = 2y - 4x : y_p = 2x + 1
yp = 2 * x + 1
verifie("y_p = 2x+1", yp.diff(x) - (2 * yp - 4 * x), 0)
verifie("y'=2y-4x", resout(lambda Y, X: 2 * Y - 4 * X, {y(0): C + 1}), C * sp.exp(2 * x) + 2 * x + 1)
verifie("y'=2y-4x, y(0)=0", resout(lambda Y, X: 2 * Y - 4 * X, {y(0): 0}), -sp.exp(2 * x) + 2 * x + 1)
# V. café : T' = -0,1 (T - 20), T(0) = 90
T = resout(lambda Y, X: -sp.Rational(1, 10) * (Y - 20), {y(0): 90}, t)
verifie("café T(t)", T, 20 + 70 * sp.exp(-t / 10))
t40 = sp.solve(sp.Eq(T, 40), t)[0]
verifie("café 40 °C : t = 10 ln 3,5", t40, 10 * sp.log(sp.Rational(7, 2)))
verifie("café 40 °C (approché)", t40, 12.53, 0.005)
# tableau de modèles
k, Ta, T0, E, R, Cc, d, Q0, N0 = sp.symbols("k T_a T_0 E R C_c d Q_0 N_0", positive=True)
verifie("Newton général", resout(lambda Y, X: -k * (Y - Ta), {y(0): T0}, t), Ta + (T0 - Ta) * sp.exp(-k * t))
verifie("condensateur", resout(lambda Y, X: (E - Y) / (R * Cc), {y(0): 0}, t), E * (1 - sp.exp(-t / (R * Cc))))
verifie("apport constant", resout(lambda Y, X: -k * Y + d, {y(0): Q0}, t), d / k + (Q0 - d / k) * sp.exp(-k * t))

print("== EXERCICES")
print("-- 1132 Vérification de solutions")
Y1 = 3 * sp.exp(2 * x) - 2
verifie("Q1", Y1.diff(x) - (2 * Y1 + 4), 0)
T2 = 20 + 80 * sp.exp(-t / 10)
verifie("Q2", T2.diff(t) - (-(T2 - 20) / 10), 0)
P3 = 100 * sp.exp(t / 20)
verifie("Q3", P3.diff(t) - P3 / 20, 0)
Z4 = sp.exp(2 * x) + 1
verifie("Q4 : z' - (2z+4) = -6 (pas solution)", Z4.diff(x) - (2 * Z4 + 4), -6)

print("-- 1128 Circuit RC")
RC = sp.Integer(1000) * sp.Rational(10, 10**6)
verifie("RC = 0,01", RC, sp.Rational(1, 100))
u = resout(lambda Y, X: (5 - Y) / RC, {y(0): 0}, t)
verifie("u(t)", u, 5 * (1 - sp.exp(-100 * t)))
verifie("u(0,02)", u.subs(t, sp.Rational(2, 100)), 4.3233, 0.0001)
verifie("u(5 tau)", u.subs(t, 5 * RC), 4.9663, 0.0001)
verifie("pourcentage à 5 tau", 100 * (1 - sp.exp(-5)), 99.326, 0.001)
verifie("limite", sp.limit(u, t, sp.oo), 5)

print("-- 1123 Croissance démographique")
P = resout(lambda Y, X: sp.Rational(3, 100) * Y, {y(0): 5000}, t)
verifie("P(t)", P, 5000 * sp.exp(3 * t / 100))
verifie("P(10)", P.subs(t, 10), 6749.29, 0.01)
td = sp.solve(sp.Eq(P, 10000), t)[0]
verifie("doublement : ln2/0,03", td, 100 * sp.log(2) / 3)
verifie("doublement (approché)", td, 23.105, 0.001)

print("-- 1127 Croissance de population avec apport")
P = resout(lambda Y, X: Y / 50 + 50, {y(0): 1000}, t)
verifie("P(t)", P, 3500 * sp.exp(t / 50) - 2500)
verifie("P(5)", P.subs(t, 5), 1368.10, 0.01)
t2000 = sp.solve(sp.Eq(P, 2000), t)[0]
verifie("t(2000) = 50 ln(9/7)", t2000, 50 * sp.log(sp.Rational(9, 7)))
verifie("t(2000) (approché)", t2000, 12.566, 0.001)
verifie("ln(9/7)", sp.log(sp.Rational(9, 7)), 0.25131, 0.00001)
assert sp.limit(P, t, sp.oo) == sp.oo
print("  ok  limite +oo")

print("-- 1126 Décroissance radioactive")
N = resout(lambda Y, X: -Y / 50, {y(0): 1000}, t)
verifie("N(t)", N, 1000 * sp.exp(-t / 50))
Th = sp.solve(sp.Eq(N, 500), t)[0]
verifie("demi-vie = 50 ln 2", Th, 50 * sp.log(2))
verifie("demi-vie (approché)", Th, 34.657, 0.001)
t100 = sp.solve(sp.Eq(N, 100), t)[0]
verifie("t(100) = 50 ln 10", t100, 50 * sp.log(10))
verifie("t(100) (approché)", t100, 115.129, 0.001)

print("-- 1129 Uranium 238")
lam = sp.Rational(49, 10) * sp.Integer(10)**-18
an = sp.Rational(3156, 1000) * 10**7
tt = 10**9 * an
verifie("t = 3,156e16 s", tt, sp.Rational(3156, 1000) * 10**16)
verifie("lambda t", lam * tt, 0.154644, 0.000001)
verifie("proportion restante", sp.exp(-lam * tt), 0.85672, 0.00001)
Tu = sp.log(2) / lam
verifie("demi-vie en s", Tu, 1.41459e17, 0.0001e17)
verifie("demi-vie en milliards d'années", Tu / an / 10**9, 4.4822, 0.0001)
ecart = (Tu / an / 10**9 - sp.Rational(447, 100)) / sp.Rational(447, 100) * 100
verifie("écart relatif avec 4,47 (en %)", ecart, 0.27, 0.01)

print("-- 1124 Mélange")
Q = resout(lambda Y, X: 1 - Y / 50, {y(0): 0}, t)
verifie("Q(t)", Q, 50 * (1 - sp.exp(-t / 50)))
verifie("débit de sel entrant 2 x 0,5", 2 * sp.Rational(1, 2), 1)
verifie("Q(30)", Q.subs(t, 30), 22.559, 0.001)
verifie("limite 50", sp.limit(Q, t, sp.oo), 50)

print("-- 1125 Refroidissement de Newton")
T = resout(lambda Y, X: -(Y - 20) / 10, {y(0): 80}, t)
verifie("T(t)", T, 20 + 60 * sp.exp(-t / 10))
verifie("T(10)", T.subs(t, 10), 42.073, 0.001)
t25 = sp.solve(sp.Eq(T, 25), t)[0]
verifie("t(25) = 10 ln 12", t25, 10 * sp.log(12))
verifie("t(25) (approché)", t25, 24.849, 0.001)

print("-- 1130 Température")
T = resout(lambda Y, X: -(Y - 25) / 50, {y(0): 100}, t)
verifie("T(t)", T, 25 + 75 * sp.exp(-t / 50))
verifie("forme y'=ay+b : b = 0,5", sp.expand(-(y(t) - 25) / 50).coeff(y(t), 0), sp.Rational(1, 2))
verifie("T(60)", T.subs(t, 60), 47.590, 0.001)
t30 = sp.solve(sp.Eq(T, 30), t)[0]
verifie("t(30) = 50 ln 15", t30, 50 * sp.log(15))
verifie("t(30) (approché)", t30, 135.40, 0.01)

print("-- 1131 Croissance logistique")
Pf = sp.Function("P")
Pt = 1000 / (1 + 9 * sp.exp(-t / 10))
verifie("P vérifie l'équation logistique", Pt.diff(t) - Pt / 10 * (1 - Pt / 1000), 0)
verifie("P(0) = 100", Pt.subs(t, 0), 100)
# z = 1/P vérifie z' = -0,1 z + 0,0001 pour toute solution P > 0
Pg = Pf(t)
z = 1 / Pg
zp = z.diff(t).subs(Pg.diff(t), Pg / 10 * (1 - Pg / 1000))
verifie("z' = -0,1 z + 0,0001", zp - (-z / 10 + sp.Rational(1, 10000)), 0)
zs = resout(lambda Y, X: -Y / 10 + sp.Rational(1, 10000), {y(0): sp.Rational(1, 100)}, t)
verifie("z(t)", zs, sp.Rational(9, 1000) * sp.exp(-t / 10) + sp.Rational(1, 1000))
verifie("P = 1/z", 1 / zs, Pt)
verifie("P(20)", Pt.subs(t, 20), 450.85, 0.01)
verifie("e^{-2}", sp.exp(-2), 0.1353, 0.0001)
verifie("P'(t) = 900 e^{-0,1t} / (1 + 9e^{-0,1t})^2 > 0", Pt.diff(t),
        900 * sp.exp(-t / 10) / (1 + 9 * sp.exp(-t / 10))**2)
verifie("limite 1000", sp.limit(Pt, t, sp.oo), 1000)
print("== FINITION 2026-11-02 : figures et nouveaux exercices")
print("-- cours IV, figure : y' = 2y - 4x")
for K in (2, sp.Rational(1, 2), -sp.Rational(1, 2), -2, -1):
    h = 2 * x + 1 + K * sp.exp(2 * x)
    verifie(f"courbe C={K} solution de y'=2y-4x", h.diff(x) - (2 * h - 4 * x), 0)
verifie("en -oo, écart à la droite -> 0", sp.limit(sp.exp(2 * x), x, -sp.oo), 0)
print("-- 1132, figure : y' = 2y + 4")
for K in (3, 1, -1, -3):
    h = K * sp.exp(2 * x) - 2
    verifie(f"courbe C={K} solution de y'=2y+4", h.diff(x) - (2 * h + 4), 0)
verifie("3e^{2x}-2 passe par (0;1)", (3 * sp.exp(2 * x) - 2).subs(x, 0), 1)
print("-- 1123, 1127, 1129, 1130 : valeurs portées sur les figures")
verifie("P(10) = 6749,3", (5000 * sp.exp(sp.Rational(3, 100) * t)).subs(t, 10), 6749.29, 0.01)
verifie("doublement ln2/0,03", sp.log(2) / sp.Rational(3, 100), 23.105, 0.001)
verifie("1127 P(5)", (3500 * sp.exp(t / 50) - 2500).subs(t, 5), 1368.1, 0.05)
verifie("1127 t(2000)", 50 * sp.log(sp.Rational(9, 7)), 12.566, 0.001)
lam = sp.Rational(49, 10) * sp.Rational(1, 10)**18
an = sp.Rational(3156, 1000) * 10**7
k_gan = lam * an * 10**9          # λ exprimé par milliard d'années
verifie("1129 λ par milliard d'années", k_gan, 0.154644, 1e-6)
verifie("1129 85,67 %", 100 * sp.exp(-k_gan), 85.67, 0.005)
verifie("1129 demi-vie 4,4823", sp.log(2) / k_gan, 4.4823, 0.0001)
verifie("1130 T(60)", (25 + 75 * sp.exp(-t / 50)).subs(t, 60), 47.59, 0.005)
verifie("1130 t(30)", 50 * sp.log(15), 135.4, 0.05)

print("-- nouveau-1 : y' = -0,5y + 1")
E1 = lambda Y, X: -Y / 2 + 1
verifie("solution constante 2", E1(sp.Integer(2), x), 0)
verifie("solutions C e^{-x/2} + 2", resout(E1, {y(0): C + 2}), C * sp.exp(-x / 2) + 2)
f1 = resout(E1, {y(0): 4})
verifie("f (passe par A(0;4))", f1, 2 * sp.exp(-x / 2) + 2)
g1 = resout(E1, {y(2): 0})
verifie("g (passe par B(2;0))", g1, 2 - 2 * sp.exp(1 - x / 2))
verifie("g : C = -2e", sp.simplify(g1 - 2) / sp.exp(-x / 2), -2 * sp.E)
verifie("limite 2", sp.limit(C * sp.exp(-x / 2) + 2, x, sp.oo), 2)
for K in (4, 2, -2, -4):
    h = 2 + K * sp.exp(-x / 2)
    verifie(f"figure : courbe C={K} solution", h.diff(x) - E1(h, x), 0)

print("-- nouveau-2 : y' + y = 2e^{-x}")
u = 2 * x * sp.exp(-x)
verifie("u'(x)", u.diff(x), 2 * sp.exp(-x) - 2 * x * sp.exp(-x))
verifie("u solution", u.diff(x) + u - 2 * sp.exp(-x), 0)
E2 = lambda Y, X: -Y + 2 * sp.exp(-X)
verifie("solutions (2x + C)e^{-x}", resout(E2, {y(0): C}), (2 * x + C) * sp.exp(-x))
f2 = resout(E2, {y(0): 1})
verifie("f(x) = (2x + 1)e^{-x}", f2, (2 * x + 1) * sp.exp(-x))
verifie("f'(x) = (1 - 2x)e^{-x}", f2.diff(x), (1 - 2 * x) * sp.exp(-x))
verifie("autre méthode f' = 2e^{-x} - f", f2.diff(x) - (2 * sp.exp(-x) - f2), 0)
verifie("racine de f'", sp.solve(f2.diff(x), x)[0], sp.Rational(1, 2))
verifie("f(1/2) = 2/√e", f2.subs(x, sp.Rational(1, 2)), 2 / sp.sqrt(sp.E))
verifie("f(1/2) ≈ 1,21", f2.subs(x, sp.Rational(1, 2)), 1.2131, 0.0001)
verifie("f(0) = 1", f2.subs(x, 0), 1)
verifie("limite +oo", sp.limit(f2, x, sp.oo), 0)
verifie("x e^{-x} -> 0", sp.limit(x * sp.exp(-x), x, sp.oo), 0)
print("\nTout est juste.")
