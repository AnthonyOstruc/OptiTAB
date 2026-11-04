# -*- coding: utf-8 -*-
"""Vérification (sympy) de tous les résultats de la notion « Limites des fonctions »."""
import sympy as sp

x = sp.symbols("x", real=True)
oo = sp.oo
ok = 0
erreurs = []


def L(expr, pt, attendu, dirn="+-", nom=""):
    global ok
    if dirn == "+-" and pt not in (oo, -oo):
        val = sp.limit(expr, x, pt, dir="+-")
    else:
        val = sp.limit(expr, x, pt, dir=dirn if dirn != "+-" else "+")
    if sp.simplify(val - attendu) == 0 if attendu not in (oo, -oo) else val == attendu:
        ok += 1
    else:
        erreurs.append(f"{nom} : limite {val} ≠ {attendu}")


def E(a, b, nom):
    global ok
    if sp.simplify(a - b) == 0:
        ok += 1
    else:
        erreurs.append(f"{nom} : identité fausse")


def V(cond, nom):
    global ok
    if cond:
        ok += 1
    else:
        erreurs.append(nom)


# ------------------------------------------------------------------ cours
f = (2*x + 1)/(x - 1)
L(f, oo, 2, nom="cours f +oo"); L(f, -oo, 2, nom="cours f -oo")
L(f, 1, oo, "+", "cours f 1+"); L(f, 1, -oo, "-", "cours f 1-")
E(f, 2 + 3/(x - 1), "cours f décomposée")
E((x**2 - 1)/(x - 2), x + 2 + 3/(x - 2), "cours asymptote oblique")
L((3*x**2 - 5*x + 1)/(x**2 + 2), oo, 3, nom="cours FI quotient")
L(sp.sqrt(x + 1) - sp.sqrt(x), oo, 0, nom="cours conjugué")
L(sp.exp(-x**2), oo, 0, nom="cours exp(-x^2)")
L(sp.sqrt(4 + 1/x), oo, 2, nom="cours sqrt(4+1/x)")
L(sp.sin(x)/x, oo, 0, nom="cours sin x / x")
L(x + sp.cos(x), oo, oo, nom="cours x + cos x")
L((sp.exp(x) - 1)/x, 0, 1, nom="cours (e^x-1)/x")
L(sp.sin(x)/x, 0, 1, nom="cours sin x/x en 0")
for n in range(1, 6):
    L(sp.exp(x)/x**n, oo, oo, nom=f"cours e^x/x^{n}")
    L(x**n*sp.exp(-x), oo, 0, nom=f"cours x^{n}e^-x")
    L(x**n*sp.exp(x), -oo, 0, nom=f"cours x^{n}e^x")
    xp = sp.symbols("xp", positive=True)
    E(sp.exp(xp)/xp**n, (sp.exp(xp/n)/(xp/n))**n/n**n, f"cours identité n={n}")
L(x**2/sp.exp(x), oo, 0, nom="cours x^2/e^x")
L(x**2 - sp.exp(x), oo, -oo, nom="cours x^2-e^x")
L(sp.log(x)/x, oo, 0, nom="cours ln x / x"); L(x*sp.log(x), 0, 0, "+", "cours x ln x")
g = sp.exp(x) - x**2/2
V(all(g.subs(x, t) > 0 for t in [0, 0.5, 1, 2, 5, 10]), "cours e^x > x^2/2")
r1, r2 = sp.nsolve(sp.exp(x) - x**3, x, 1.8), sp.nsolve(sp.exp(x) - x**3, x, 4.5)
V(abs(r1 - 1.857) < 1e-3 and abs(r2 - 4.536) < 1e-3, "cours e^x = x^3 en 1,857 et 4,536")
# tableau des limites de référence
for n in (2, 4):
    L(x**n, -oo, oo, nom="tab x^n pair -oo"); L(1/x**n, 0, oo, "-", "tab 1/x^n pair 0-")
for n in (1, 3):
    L(x**n, -oo, -oo, nom="tab x^n impair -oo"); L(1/x**n, 0, -oo, "-", "tab 1/x^n impair 0-")
    L(1/x**n, 0, oo, "+", "tab 1/x^n impair 0+")
L(1/sp.sqrt(x), 0, oo, "+", "tab 1/sqrt 0+"); L(1/sp.sqrt(x), oo, 0, nom="tab 1/sqrt +oo")
L(sp.exp(x), -oo, 0, nom="tab exp -oo")

# ------------------------------------------------------------------ 1188
L(3*x**2 - 2*x + 1, 2, 9, nom="1188 Q1"); L(1/x**3, oo, 0, nom="1188 Q2")
L(x**4, oo, oo, nom="1188 Q3"); L(sp.sqrt(x + 1), oo, oo, nom="1188 Q4"); L(sp.exp(x), -oo, 0, nom="1188 Q5")
# ------------------------------------------------------------------ 1189
L(1/x + 3, oo, 3, nom="1189 Q1"); L(5*x**2, 2, 20, nom="1189 Q2")
L((2*x + 1)/(3*x - 2), oo, sp.Rational(2, 3), nom="1189 Q3"); L((x**2 + 1)/(x - 1), 3, 5, nom="1189 Q4")
L(x/x**2, oo, 0, nom="1189 Q5")
# ------------------------------------------------------------------ 1197 DS
L(2*x**2 - 5*x + 1, 3, 4, nom="DS A1"); L((3*x**2 + 2*x - 1)/(x**2 + 5), oo, 3, nom="DS A2")
L(x**3 - 2*x**2, oo, oo, nom="DS A3"); L((x**2 - 4)/(x - 2), 2, 4, nom="DS B1")
L((2*x**2 - x + 1)/(3*x**2 + 4*x - 2), oo, sp.Rational(2, 3), nom="DS B2")
L(sp.sqrt(x**2 + 1) - x, oo, 0, nom="DS B3")
E(sp.sqrt(x**2 + 1) - x, 1/(sp.sqrt(x**2 + 1) + x), "DS B3 conjugué")
L((2*x + sp.sin(x))/(x + 1), oo, 2, nom="DS C1")
L((2*x - 1)/(x + 1), oo, 2, nom="DS C1 g"); L((2*x + 1)/(x + 1), oo, 2, nom="DS C1 h")
L(x**2*sp.cos(1/x), 0, 0, nom="DS C2")
fd = (3*x + 2)/(x - 1)
L(fd, 1, oo, "+", "DS D1 1+"); L(fd, 1, -oo, "-", "DS D1 1-"); L(fd, oo, 3, nom="DS D1 +oo"); L(fd, -oo, 3, nom="DS D1 -oo")
gd = (x**2 - 1)/(x + 2)
L(gd, -2, oo, "+", "DS D2 -2+"); L(gd, -2, -oo, "-", "DS D2 -2-")
E(gd, x - 2 + 3/(x + 2), "DS D2 décomposition")
L(gd - (x - 2), oo, 0, nom="DS D2 oblique +oo"); L(gd - (x - 2), -oo, 0, nom="DS D2 oblique -oo")
L(sp.sin(4*x)/x, 0, 4, nom="DS E1"); L(sp.exp(x)/x**3, oo, oo, nom="DS E2"); L(sp.log(x**2)/x, oo, 0, nom="DS E3")
# ------------------------------------------------------------------ 867
f1 = (x**2 - 1)/(x - 2)
L(f1, 2, oo, "+", "867 Q1 2+"); L(f1, 2, -oo, "-", "867 Q1 2-"); E(f1, x + 2 + 3/(x - 2), "867 Q1 décomp")
g2 = (2*x + 1)/(x + 3)
L(g2, -3, -oo, "+", "867 Q2 -3+"); L(g2, -3, oo, "-", "867 Q2 -3-"); L(g2, oo, 2, nom="867 Q2 +oo"); L(g2, -oo, 2, nom="867 Q2 -oo")
h3 = (x**3 + 1)/(x**2 - 1)
E(h3, x + 1/(x - 1), "867 Q3 décomp"); L(h3, -1, sp.Rational(-3, 2), nom="867 Q3 en -1")
L(h3, 1, oo, "+", "867 Q3 1+"); L(h3, 1, -oo, "-", "867 Q3 1-")
k4 = (x**2 + 2*x)/(x + 1)
E(k4, x + 1 - 1/(x + 1), "867 Q4 décomp")
L(k4, -1, -oo, "+", "867 Q4 -1+ (corrigé : -oo)"); L(k4, -1, oo, "-", "867 Q4 -1- (corrigé : +oo)")
m5 = (x**2 - 4)/(x**2 + 1)
L(m5, oo, 1, nom="867 Q5 +oo"); L(m5, -oo, 1, nom="867 Q5 -oo"); E(m5, 1 - 5/(x**2 + 1), "867 Q5 écriture")
V(m5.subs(x, 0) == -4 and sp.solve(sp.diff(m5, x), x) == [0], "867 Q5 minimum -4 en 0")
# ------------------------------------------------------------------ 1190
L((x**2 - 1)/(x - 1), 1, 2, nom="1190 Q1"); L((x**3 - 1)/(x**2 - 1), 1, sp.Rational(3, 2), nom="1190 Q2")
E(x**3 - 1, (x - 1)*(x**2 + x + 1), "1190 Q2 factorisation")
L((x**2 - 3*x + 2)/(2*x**2 + x - 1), oo, sp.Rational(1, 2), nom="1190 Q3")
L(x**2 - x, oo, oo, nom="1190 Q4"); L((x**2 + 1)/(x**3 - 2*x), oo, 0, nom="1190 Q5")
# ------------------------------------------------------------------ 1195
L(1/x, 0, oo, "+", "1195 Q1+"); L(1/x, 0, -oo, "-", "1195 Q1-"); L(sp.sqrt(x), 0, 0, "+", "1195 Q2")
L((x**2 - 4)/(x - 2), 2, 4, nom="1195 Q3"); L(sp.Abs(x)/x, 0, 1, "+", "1195 Q4+"); L(sp.Abs(x)/x, 0, -1, "-", "1195 Q4-")
# Q5 réécrite (finition 2026-11-02) : g(x) = (2x + 1)/(1 - x)
L((2*x + 1)/(1 - x), 1, -oo, "+", "1195 Q5 droite"); L((2*x + 1)/(1 - x), 1, oo, "-", "1195 Q5 gauche")
L((2*x + 1)/(1 - x), oo, -2, nom="1195 Q5 figure y=-2 en +oo"); L((2*x + 1)/(1 - x), -oo, -2, nom="1195 Q5 figure y=-2 en -oo")
E((2*x + 1)/(1 - x), -2 + 3/(1 - x), "1195 Q5 forme -2 + 3/(1-x)")
# ------------------------------------------------------------------ 1194
L((sp.sqrt(1 + x) - 1)/x, 0, sp.Rational(1, 2), nom="1194 Q1"); L((sp.sqrt(x) - 1)/(x - 1), 1, sp.Rational(1, 2), nom="1194 Q2")
L(sp.sqrt(x**2 + x) - x, oo, sp.Rational(1, 2), nom="1194 Q3"); L(sp.sqrt(x**2 + 2*x + 1) - x, oo, 1, nom="1194 Q4")
L((sp.sqrt(x**2 + 1) - x)/x, oo, 0, nom="1194 Q5")
# ------------------------------------------------------------------ 1193
L((sp.exp(x) - 1)/x, 0, 1, nom="1193 Q1"); L(sp.log(1 + x)/x, 0, 1, nom="1193 Q2")
L(sp.exp(x)/x**2, oo, oo, nom="1193 Q3"); L(sp.log(x)/x, oo, 0, nom="1193 Q4"); L((sp.exp(2*x) - sp.exp(x))/x, 0, 1, nom="1193 Q5")
# ------------------------------------------------------------------ 1192
L(sp.sin(2*x)/x, 0, 2, nom="1192 Q1"); L(sp.sin(3*x)/sp.sin(5*x), 0, sp.Rational(3, 5), nom="1192 Q2")
# Q3 et Q4 réécrites (finition 2026-11-02) : taux d'accroissement de cos en 0 et de sin en pi
L(sp.sin(x)/x, 0, 1, nom="1192 rappel sin x / x")
L((sp.cos(x) - 1)/x, 0, 0, nom="1192 Q3"); V(sp.diff(sp.cos(x), x).subs(x, 0) == 0, "1192 Q3 cos'(0) = 0")
L(sp.sin(x)/(x - sp.pi), sp.pi, -1, nom="1192 Q4"); V(sp.diff(sp.sin(x), x).subs(x, sp.pi) == -1, "1192 Q4 sin'(pi) = -1")
E(sp.sin(x), -sp.sin(x - sp.pi), "1192 Q4 sin x = -sin(x - pi)")
E(sp.sin(sp.pi) + (-1)*(x - sp.pi), sp.pi - x, "1192 Q4 tangente y = -x + pi")
L(sp.sin(x**2)/x**2, 0, 1, nom="1192 Q5")
# ------------------------------------------------------------------ 1196 (réécrit le 2026-11-02)
import numpy as np
T = np.linspace(0, 1000, 200001)
V(np.all(T + np.sin(T) >= T - 1), "1196 Q1 minoration x + sin x >= x - 1")
TN = np.linspace(-1000, 0, 200001)
V(np.all(TN + 2*np.cos(TN) <= TN + 2), "1196 Q2 majoration x + 2 cos x <= x + 2")
L(x + 2, -oo, -oo, nom="1196 Q2 majorante")
V(np.all(np.sqrt(T**2 + T) >= T), "1196 Q3 minoration")
TP = T[T > 0]
V(np.all(-TP*np.sin(TP) >= -TP - 1e-9) and np.all(TP**2 - TP*np.sin(TP) >= TP*(TP - 1) - 1e-9), "1196 Q4 minoration")
L(x*(x - 1), oo, oo, nom="1196 Q4 minorante")
T7 = np.linspace(0, 30, 30001)
V(np.all(np.exp(T7) + 3*np.cos(T7) >= np.exp(T7) - 3), "1196 Q5 minoration")
L(sp.exp(x) - 3, oo, oo, nom="1196 Q5 minorante")
# ------------------------------------------------------------------ figures ajoutées (finition 2026-11-02)
L(1/x + 3, oo, 3, nom="1189 figure asymptote y = 3"); V(all(1/t + 3 > 3 for t in np.linspace(0.2, 10.4, 50)), "1189 courbe au-dessus")
E((x**2 - 1)/(x - 1), x + 1, "1190 figure : droite y = x + 1 privée de (1 ; 2)")
V(sp.solve(sp.diff(sp.log(x)/x, x), x) == [sp.E], "1193 figure : maximum en e")
E((sp.log(x)/x).subs(x, sp.E), 1/sp.E, "1193 figure : maximum 1/e")
L((2*x - 1)/(x + 1), oo, 2, nom="1197 C1 figure gendarme bas"); L((2*x + 1)/(x + 1), oo, 2, nom="1197 C1 figure gendarme haut")
V(all((2*t - 1)/(t + 1) <= (2*t + np.sin(t))/(t + 1) <= (2*t + 1)/(t + 1) for t in np.linspace(0, 30, 3001)), "1197 C1 encadrement")
# ------------------------------------------------------------------ 1191
L(x**2*sp.sin(1/x), 0, 0, nom="1191 Q1"); L(sp.sin(x)/x, oo, 0, nom="1191 Q2"); L(x*sp.cos(1/x), 0, 0, nom="1191 Q3")
L((x + sp.sin(x))/(x + sp.cos(x)), oo, 1, nom="1191 Q4"); L((x**2 + sp.cos(x))/(x**2 + 1), oo, 1, nom="1191 Q5")
L(sp.cos(x)/x, oo, 0, nom="1191 Q4 cos x / x"); L((x**2 - 1)/(x**2 + 1), oo, 1, nom="1191 Q5 minorante")

print(f"{ok} contrôles réussis, {len(erreurs)} erreur(s)")
for e in erreurs:
    print("  ✗", e)
