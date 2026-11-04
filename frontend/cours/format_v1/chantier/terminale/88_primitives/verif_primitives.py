# -*- coding: utf-8 -*-
"""Vérification (sympy) de toutes les primitives de la notion « Primitives » (Terminale).

    python verif_primitives.py

Pour chaque cas : F' - f = 0 sur l'intervalle (simplification symbolique puis
contrôle numérique en plusieurs points de l'intervalle), condition F(x0) = y0
quand l'énoncé en donne une. Couvre le cours, la fiche et les 10 exercices.
"""
import sys

import sympy as sp

x = sp.symbols("x", real=True)
E = sp.E
OK = True


def verifie(nom, f, F, intervalle, condition=None):
    """intervalle = (a, b) bornes numériques (sp.oo admis) ; condition = (x0, y0)."""
    global OK
    a, b = intervalle
    d = sp.simplify(sp.diff(F, x) - f)
    # points de contrôle strictement dans l'intervalle
    lo = -3 if a == -sp.oo else float(a)
    hi = 3 if b == sp.oo else float(b)
    if a == -sp.oo and b != sp.oo:
        lo = hi - 4
    if b == sp.oo and a != -sp.oo:
        hi = lo + 4
    pts = [lo + (hi - lo) * k / 7 for k in range(1, 7)]
    num = max(abs(complex(sp.N((sp.diff(F, x) - f).subs(x, p)))) for p in pts)
    bon = (d == 0) or num < 1e-9
    msg = "" if bon else f" (F'-f = {d}, écart numérique {num:.2e})"
    if condition is not None:
        x0, y0 = condition
        v = sp.simplify(F.subs(x, x0) - y0)
        if v != 0:
            bon = False
            msg += f" (condition F({x0}) = {y0} non vérifiée : F({x0}) = {sp.simplify(F.subs(x, x0))})"
    OK &= bon
    print(("OK  " if bon else "ERR ") + nom + msg)


R = (-sp.oo, sp.oo)
Rp = (0, sp.oo)
Rm = (-sp.oo, 0)
sq = sp.sqrt
ln = sp.log

print("== Cours / fiche")
verifie("ex. déf. : 3x^2+2", 3 * x**2 + 2, x**3 + 2 * x, R)
verifie("ex. condition : 2x, F(1)=3", 2 * x, x**2 + 2, R, (1, 3))
verifie("usuelle x^4", x**4, x**5 / 5, R)
verifie("usuelle 1/x^2 (x>0)", 1 / x**2, -1 / x, Rp)
verifie("usuelle 1/x^2 (x<0)", 1 / x**2, -1 / x, Rm)
for n in range(2, 6):
    verifie(f"usuelle 1/x^{n}", 1 / x**n, -1 / ((n - 1) * x**(n - 1)), Rp)
verifie("usuelle 1/sqrt(x)", 1 / sq(x), 2 * sq(x), Rp)
verifie("usuelle 1/x", 1 / x, ln(x), Rp)
verifie("usuelle sin", sp.sin(x), -sp.cos(x), R)
verifie("usuelle cos", sp.cos(x), sp.sin(x), R)
verifie("ex. linéarité 3x^2-4cos x+1/x", 3 * x**2 - 4 * sp.cos(x) + 1 / x, x**3 - 4 * sp.sin(x) + ln(x), Rp)
verifie("composée 2x(x^2+1)^3", 2 * x * (x**2 + 1)**3, (x**2 + 1)**4 / 4, R)
verifie("composée 3x^2/(x^3+1)", 3 * x**2 / (x**3 + 1), ln(x**3 + 1), (-1, sp.oo))
verifie("composée x e^{x^2}", x * sp.exp(x**2), sp.exp(x**2) / 2, R)
verifie("composée e^{2x+1}", sp.exp(2 * x + 1), sp.exp(2 * x + 1) / 2, R)
verifie("composée cos(3x)", sp.cos(3 * x), sp.sin(3 * x) / 3, R)
verifie("1/x sur ]-oo;0[ : ln(-x)", 1 / x, ln(-x), Rm)
verifie("identification x e^x", x * sp.exp(x), (x - 1) * sp.exp(x), R)
verifie("lecture graphique x^2-1", x**2 - 1, x**3 / 3 - x, R)
F_lien = x**3 / 3 - x
assert F_lien.subs(x, -1) == sp.Rational(2, 3) and F_lien.subs(x, 1) == -sp.Rational(2, 3)
print("OK  F(-1) = 2/3, F(1) = -2/3 (tableau de variations du cours)")
# formes générales u'u^n, u'/u^n, u'/sqrt(u), u'/u, u'e^u, u'cos u, u'sin u avec u quelconque
u = sp.Function("u")(x)
up = sp.diff(u, x)
for n in range(0, 5):
    assert sp.simplify(sp.diff(u**(n + 1) / (n + 1), x) - up * u**n) == 0
for n in range(2, 6):
    assert sp.simplify(sp.diff(-1 / ((n - 1) * u**(n - 1)), x) - up / u**n) == 0
assert sp.simplify(sp.diff(2 * sq(u), x) - up / sq(u)) == 0
assert sp.simplify(sp.diff(ln(u), x) - up / u) == 0
assert sp.simplify(sp.diff(sp.exp(u), x) - up * sp.exp(u)) == 0
assert sp.simplify(sp.diff(sp.sin(u), x) - up * sp.cos(u)) == 0
assert sp.simplify(sp.diff(-sp.cos(u), x) - up * sp.sin(u)) == 0
print("OK  tableau des formes composées (u quelconque)")
# intégration par parties, forme « primitives » : (uv - G)' = uv' dès que G' = u'v
v = sp.Function("v")(x)
G = sp.Function("G")(x)
expr = sp.diff(u * v - G, x).subs(sp.Derivative(G, x), sp.diff(u, x) * v)
assert sp.simplify(expr - u * sp.diff(v, x)) == 0
print("OK  formule (uv - G)' = uv' si G' = u'v")
# cas affine : (1/a) F(ax+b) primitive de f(ax+b)
a_, b_ = sp.symbols("a b", real=True, nonzero=True)
Fg = sp.Function("F")
assert sp.simplify(sp.diff(Fg(a_ * x + b_) / a_, x) - sp.Subs(sp.Derivative(Fg(x), x), x, a_ * x + b_).doit()) == 0
print("OK  cas affine (1/a) F(ax+b)")

print("== 1221 Calculs de base")
verifie("Q1", 3 * x**2 + 2, x**3 + 2 * x + 3, R, (0, 3))
verifie("Q2", 5 * x**4, x**5 + 1, R, (1, 2))
verifie("Q3", 7 - 4 * x, 7 * x - 2 * x**2 + 5, R, (0, 5))
verifie("Q4", sp.exp(x), sp.exp(x), R, (0, 1))
verifie("Q5", sp.cos(x), sp.sin(x), R, (0, 0))

print("== 1222 Linéarité")
verifie("Q1", 2 * x**3 - 5 * x + 4, x**4 / 2 - 5 * x**2 / 2 + 4 * x + 1, R, (0, 1))
verifie("Q2", x**2 + 3 * x + 1, x**3 / 3 + 3 * x**2 / 2 + x + 2, R, (0, 2))
verifie("Q3", 6 * sp.exp(x) - 3, 6 * sp.exp(x) - 3 * x - 6, R, (0, 0))
verifie("Q4", 4 * sp.cos(x) - 2 * sp.sin(x), 4 * sp.sin(x) + 2 * sp.cos(x) - 1, R, (0, 1))
verifie("Q5 (indication : (x sqrt x)' = 3/2 sqrt x)", sq(x), sp.Rational(2, 3) * x * sq(x), Rp)
verifie("Q5", sq(x) + 1 / sq(x), sp.Rational(2, 3) * x * sq(x) + 2 * sq(x) + sp.Rational(1, 3), Rp, (1, 3))

print("== 1223 Exponentielles et trigonométriques")
verifie("Q1", sp.exp(3 * x), sp.exp(3 * x) / 3, R, (0, sp.Rational(1, 3)))
verifie("Q2", sp.exp(2 * x + 1), sp.exp(2 * x + 1) / 2, R, (0, E / 2))
verifie("Q3", sp.sin(2 * x), -sp.cos(2 * x) / 2 + sp.Rational(1, 2), R, (0, 0))
verifie("Q4", sp.cos(5 * x), sp.sin(5 * x) / 5 + sp.Rational(1, 5), R, (0, sp.Rational(1, 5)))
verifie("Q5", 3 * sp.exp(x) - 2 * sp.cos(2 * x), 3 * sp.exp(x) - sp.sin(2 * x) - 1, R, (0, 2))

print("== 1224 Fonctions rationnelles simples")
verifie("Q1 sur ]-oo;0[", 1 / x, ln(-x), Rm)
verifie("Q2", 2 * x / (x**2 + 1), ln(x**2 + 1), R)
verifie("Q3 sur ]-1/3;+oo[", 1 / (3 * x + 1)**3, -1 / (6 * (3 * x + 1)**2), (-sp.Rational(1, 3), sp.oo))
verifie("Q4 sur ]0;+oo[", (x - 1) / x**2, ln(x) + 1 / x, Rp)
verifie("Q5 sur ]3/2;+oo[", 5 / (2 * x - 3), sp.Rational(5, 2) * ln(2 * x - 3), (sp.Rational(3, 2), sp.oo))

print("== 1228 Formes composées")
verifie("Q1", (3 * x - 2)**4, (3 * x - 2)**5 / 15, R)
verifie("Q2 sur ]-5/2;+oo[", 1 / (2 * x + 5), ln(2 * x + 5) / 2, (-sp.Rational(5, 2), sp.oo))
verifie("Q3", sp.sin(3 * x - 1), -sp.cos(3 * x - 1) / 3, R)
verifie("Q4", sp.cos(4 * x + 2), sp.sin(4 * x + 2) / 4, R)
verifie("Q5", sp.exp(5 * x - 3), sp.exp(5 * x - 3) / 5, R)

print("== 1226 Intégration par parties")
verifie("Q1", x * sp.exp(x), (x - 1) * sp.exp(x), R)
verifie("Q2", x * sp.cos(x), x * sp.sin(x) + sp.cos(x), R)
verifie("Q3 sur ]0;+oo[", ln(x), x * ln(x) - x, Rp)
verifie("Q4 (G = primitive de -2x cos x)", -2 * x * sp.cos(x), -2 * (x * sp.sin(x) + sp.cos(x)), R)
verifie("Q4", x**2 * sp.sin(x), -x**2 * sp.cos(x) + 2 * x * sp.sin(x) + 2 * sp.cos(x), R)
verifie("Q5", x * sp.exp(2 * x), (2 * x - 1) / 4 * sp.exp(2 * x), R)

print("== 1227 Intégration par parties avancée")
verifie("Q1 (G = primitive de 2x e^x)", 2 * x * sp.exp(x), 2 * (x - 1) * sp.exp(x), R)
verifie("Q1", x**2 * sp.exp(x), (x**2 - 2 * x + 2) * sp.exp(x), R)
verifie("Q2 sur ]0;+oo[", x * ln(x), x**2 / 2 * ln(x) - x**2 / 4, Rp)
verifie("Q3", x * sp.sin(2 * x), -x / 2 * sp.cos(2 * x) + sp.sin(2 * x) / 4, R)
verifie("Q4", (x + 1) * sp.exp(x), x * sp.exp(x), R)
verifie("Q5 (primitive de x sin x)", x * sp.sin(x), -x * sp.cos(x) + sp.sin(x), R)
verifie("Q5", x**2 * sp.cos(x), x**2 * sp.sin(x) + 2 * x * sp.cos(x) - 2 * sp.sin(x), R)

print("== 1230 Mélanges classiques")
verifie("Q1", x * sp.exp(x), (x - 1) * sp.exp(x), R)
verifie("Q2", x * sp.sin(x), -x * sp.cos(x) + sp.sin(x), R)
verifie("Q3", sp.exp(x) + sp.cos(x), sp.exp(x) + sp.sin(x), R)
verifie("Q4", x**2 + sp.exp(2 * x), x**3 / 3 + sp.exp(2 * x) / 2, R)
verifie("Q5 sur ]0;+oo[", 1 / x + 1 / x**2, ln(x) - 1 / x, Rp)

print("== 1229 Racines, puissances et inverses")
verifie("Q1 (indication : (x^2 sqrt x)' = 5/2 x sqrt x)", x * sq(x), sp.Rational(2, 5) * x**2 * sq(x), Rp)
verifie("Q2", 1 / sq(x), 2 * sq(x), Rp)
verifie("Q3 (primitive de sqrt(x+1))", sq(x + 1), sp.Rational(2, 3) * (x + 1) * sq(x + 1), (-1, sp.oo))
verifie("Q3", x / sq(x + 1), sp.Rational(2, 3) * (x - 2) * sq(x + 1), (-1, sp.oo))
assert sp.simplify(sp.Rational(2, 3) * (x + 1) * sq(x + 1) - 2 * sq(x + 1) - sp.Rational(2, 3) * (x - 2) * sq(x + 1)) == 0
print("OK  Q3 forme factorisée = forme développée")
verifie("Q4 sur ]-2;+oo[", 1 / (x + 2)**2, -1 / (x + 2), (-2, sp.oo))
verifie("Q5 sur ]-1/2;+oo[", 1 / sq(2 * x + 1), sq(2 * x + 1), (-sp.Rational(1, 2), sp.oo))

print("== 1225 Substitution (reconnaître u'f(u))")
verifie("Q1", 2 * x * (x**2 + 1)**3, (x**2 + 1)**4 / 4, R)
verifie("Q2", 2 * x / (x**2 + 1), ln(x**2 + 1), R)
verifie("Q3", x * sp.exp(x**2), sp.exp(x**2) / 2, R)
verifie("Q4 sur ]-3/2;+oo[", 1 / sq(2 * x + 3), sq(2 * x + 3), (-sp.Rational(3, 2), sp.oo))
verifie("Q5 sur ]-1;+oo[", 1 / (x + 1)**2, -1 / (x + 1), (-1, sp.oo))

print("== Figures")
# famille x^2 + C : la seule qui passe par (1 ; 3) est C = 2 ; famille x^3 + 2x + C : par (0 ; 3), C = 3
assert sp.solve(sp.Eq(1 + sp.Symbol("C"), 3))[0] == 2
assert (x**3 + 2 * x + 3).subs(x, 0) == 3
print("OK  constantes des figures")


def controle(nom, cond):
    global OK
    cond = bool(cond)
    OK &= cond
    print(("OK  " if cond else "ERR ") + nom)


print("== Finition 2026-11-02 : figures des exercices 1223 et 1224")
G3 = -sp.cos(2 * x) / 2 + sp.Rational(1, 2)
controle("1223 Q3 : -1/2 cos(2x) vaut -1/2 en 0 ; F = courbe décalée de +1/2, F(0) = 0",
         (-sp.cos(2 * x) / 2).subs(x, 0) == -sp.Rational(1, 2) and G3.subs(x, 0) == 0)
controle("1223 figure : F(±pi/2) = 1, F(±pi) = 0", G3.subs(x, sp.pi / 2) == 1 and G3.subs(x, sp.pi) == 0)
controle("1224 Q1 : ln(-x) décroissante sur ]-oo;0[ (dérivée 1/x < 0)",
         sp.simplify(sp.diff(ln(-x), x) - 1 / x) == 0 and all((1 / x).subs(x, v) < 0 for v in (-4, -1, -0.1)))

print("== nouveau-1 : reconnaître la courbe d'une primitive")
f1 = x**2 - 2 * x
F1 = x**3 / 3 - x**2 + 1
verifie("F primitive de f, F(0) = 1", f1, F1, R, (0, 1))
verifie("G primitive de f, G(3) = 2", f1, F1 + 1, R, (3, 2))
controle("signe de f : + avant 0, - entre 0 et 2, + après 2",
         sp.solveset(f1 < 0, x, sp.S.Reals) == sp.Interval.open(0, 2))
controle("F max local 1 en 0, min local -1/3 en 2", F1.subs(x, 0) == 1 and F1.subs(x, 2) == -sp.Rational(1, 3))
controle("F(3) = 1 ≠ 2 : aucune primitive par A et B", F1.subs(x, 3) == 1)
controle("Q1 : C1 décroît en 0 (pente -2) alors que C2 y vaut 1 > 0 : C1 ne peut pas être F",
         sp.diff(f1, x).subs(x, 0) == -2 and F1.subs(x, 0) == 1)
controle("figure : f(±fenêtre) = 4,29 ; F(-1,3) ≈ -1,42 ; F(3,3) ≈ 2,09",
         abs(float(f1.subs(x, 3.3)) - 4.29) < 1e-9 and abs(float(F1.subs(x, -1.3)) + 1.4223) < 1e-3
         and abs(float(F1.subs(x, 3.3)) - 2.089) < 1e-3)

print("== nouveau-2 : remplissage d'une cuve")
t = sp.symbols("t", real=True)
q = 40 * sp.exp(-t / 10)
V = 500 - 400 * sp.exp(-t / 10)
controle("(-400 e^(-0,1t))' = q", sp.simplify(sp.diff(-400 * sp.exp(-t / 10), t) - q) == 0)
controle("V' = q et V(0) = 100", sp.simplify(sp.diff(V, t) - q) == 0 and V.subs(t, 0) == 100)
controle("lim V = 500 et V < 500", sp.limit(V, t, sp.oo) == 500 and all(float(V.subs(t, v)) < 500 for v in (0, 10, 50, 200)))
sol = sp.solve(sp.Eq(V, 400), t)
controle("V(t) = 400 <=> t = 10 ln 4", len(sol) == 1 and sp.simplify(sol[0] - 10 * ln(4)) == 0)
controle("10 ln 4 ≈ 13,863 min ≈ 13 min 52 s", abs(float(10 * ln(4)) - 13.863) < 1e-3
         and round((float(10 * ln(4)) - 13) * 60) == 52)
d = V.subs(t, 10) - V.subs(t, 5)
controle("V(10) - V(5) = 400(e^-0,5 - e^-1) ≈ 95,5", sp.simplify(d - 400 * (sp.exp(-sp.Rational(1, 2)) - sp.exp(-1))) == 0
         and round(float(d), 1) == 95.5)
controle("figure : q(0) = 40, q(40) ≈ 0,73 ; V(40) ≈ 492,7", q.subs(t, 0) == 40 and abs(float(q.subs(t, 40)) - 0.733) < 1e-3
         and abs(float(V.subs(t, 40)) - 492.67) < 0.01)

print("\nTOUT EST JUSTE" if OK else "\nERREURS")
sys.exit(0 if OK else 1)
