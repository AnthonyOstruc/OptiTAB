# -*- coding: utf-8 -*-
"""Vérifications du chapitre 20 — Fonctions de deux variables."""
import math
from math import isclose, sqrt, cos, sin, exp, log

import sympy as sp

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

x, y, t, r, th = sp.symbols("x y t r theta", real=True)

# --- Exercice 1 : derivees partielles ----------------------------------
f1 = x**2*y + y**3
check("ex1 fx", sp.diff(f1, x) == 2*x*y)
check("ex1 fy", sp.diff(f1, y) == x**2 + 3*y**2)
f1b = sp.exp(x*y)
check("ex1 exp", sp.diff(f1b, x) == y*sp.exp(x*y)
      and sp.diff(f1b, y) == x*sp.exp(x*y))
f1c = sp.ln(x**2 + y**2)
check("ex1 ln", sp.simplify(sp.diff(f1c, x) - 2*x/(x**2 + y**2)) == 0)
# --- Exercice 2 : DL a l'ordre 1 ---------------------------------------
f2 = x**2 + y**2
grad2 = (sp.diff(f2, x).subs({x: 1, y: 2}), sp.diff(f2, y).subs({x: 1, y: 2}))
check("ex2 gradient (2,4)", grad2 == (2, 4))
approx = 5 + 2*0.02 + 4*(-0.01)
exact = (1.02)**2 + (1.99)**2
check("ex2 approximation lineaire", isclose(approx, exact, abs_tol=1e-3))
# --- Exercice 3 : plan tangent -----------------------------------------
check("ex3 plan tangent z=5+2(x-1)+4(y-2)",
      5 + 2*(1 - 1) + 4*(2 - 2) == f2.subs({x: 1, y: 2}))
f3 = x*y
check("ex3 xy en (2,3)", (sp.diff(f3, x).subs({x: 2, y: 3}),
      sp.diff(f3, y).subs({x: 2, y: 3})) == (3, 2))
# --- Exercice 4 : gradient ---------------------------------------------
gnorm = sp.sqrt(sum(sp.diff(f2, v)**2 for v in (x, y))).subs({x: 3, y: 4})
check("ex4 norme du gradient", gnorm == 10)
check("ex4 radial", sp.Matrix([2*x, 2*y]).subs({x: 3, y: 4}) == sp.Matrix([6, 8]))
# --- Exercice 5 : lignes de niveau -------------------------------------
# gradient orthogonal au niveau : f = x^2 + y^2, cercle parametre
gamma5 = (sp.cos(t), sp.sin(t))
gradf5 = sp.Matrix([2*x, 2*y]).subs({x: gamma5[0], y: gamma5[1]})
dgamma5 = sp.Matrix([sp.diff(gamma5[0], t), sp.diff(gamma5[1], t)])
check("ex5 gradient orthogonal au cercle",
      sp.simplify(gradf5.dot(dgamma5)) == 0)
check("ex5 niveau de xy par (1,2)", (1*2) == 2)
# --- Exercice 6 : derivee selon un vecteur -----------------------------
f6 = x**2*y
grad6 = sp.Matrix([sp.diff(f6, x), sp.diff(f6, y)]).subs({x: 1, y: 1})
u6 = sp.Matrix([sp.Rational(3, 5), sp.Rational(4, 5)])
check("ex6 gradient (2,1)", grad6 == sp.Matrix([2, 1]))
check("ex6 derivee directionnelle 2", grad6.dot(u6) == 2)
# --- Exercice 7 : regle de la chaine -----------------------------------
g7 = f2.subs({x: sp.cos(t), y: sp.sin(t)})
check("ex7 constante sur le cercle", sp.simplify(sp.diff(g7, t)) == 0)
g7b = f3.subs({x: sp.cos(t), y: sp.sin(t)})
check("ex7 xy sur le cercle", sp.simplify(sp.diff(g7b, t) - sp.cos(2*t)) == 0)
# --- Exercice 8 : points critiques -------------------------------------
for f8, pt, nature in [(x**2 + y**2, (0, 0), "min"),
                       (x**2 - y**2, (0, 0), "selle"),
                       (x*y, (0, 0), "selle")]:
    gx = sp.diff(f8, x).subs({x: pt[0], y: pt[1]})
    gy = sp.diff(f8, y).subs({x: pt[0], y: pt[1]})
    check(f"ex8 point critique {f8}", (gx, gy) == (0, 0))
check("ex8 selle de x^2-y^2", (0.1)**2 - 0 > 0 > 0 - (0.1)**2)
# --- Exercice 9 : derivees partielles sans continuite ------------------
f9 = lambda a, b: a*b/(a*a + b*b) if (a, b) != (0, 0) else 0.0
check("ex9 limite selon y=x", isclose(f9(1e-9, 1e-9), 0.5))
check("ex9 limite selon y=0", f9(1e-9, 0) == 0.0)
check("ex9 derivees partielles nulles en 0",
      (f9(1e-9, 0) - 0)/1e-9 == 0 and (f9(0, 1e-9) - 0)/1e-9 == 0)
# --- Exercice 10 : composees -------------------------------------------
u, v = sp.symbols("u v", real=True)
F10 = sp.Function("F")
h10 = (u + v)**2*(u*v) + (u*v)**3   # f(x,y)=x^2 y + y^3 en x=u+v, y=uv
dhu = sp.diff(h10, u)
fx = (2*x*y).subs({x: u + v, y: u*v})
fy = (x**2 + 3*y**2).subs({x: u + v, y: u*v})
check("ex10 regle de la chaine", sp.simplify(dhu - (fx*1 + fy*v)) == 0)
# --- Exercice 11 : gradient et ellipse ---------------------------------
f11 = x**2 + 2*y**2
gamma11 = (sp.sqrt(3)*sp.cos(t), sp.sqrt(sp.Rational(3, 2))*sp.sin(t))
niveau = sp.simplify(f11.subs({x: gamma11[0], y: gamma11[1]}))
check("ex11 parametre le niveau 3", niveau == 3)
grad11 = sp.Matrix([2*x, 4*y]).subs({x: gamma11[0], y: gamma11[1]})
dg11 = sp.Matrix([sp.diff(gamma11[0], t), sp.diff(gamma11[1], t)])
check("ex11 orthogonalite", sp.simplify(grad11.dot(dg11)) == 0)
# --- Exercice 12 : derivee le long d'un arc ----------------------------
f12 = x**2*y
direct = sp.diff(f12.subs({x: t, y: t**2}), t)
grad12 = sp.Matrix([2*x*y, x**2]).subs({x: t, y: t**2})
chain = grad12.dot(sp.Matrix([1, 2*t]))
check("ex12 les deux calculs donnent 4t^3",
      sp.simplify(direct - chain) == 0 and sp.expand(direct) == 4*t**3)
# --- Exercice 13 : petites EDP -----------------------------------------
phi = sp.Function("phi")
f13 = x*y + phi(y)
check("ex13 solution de fx = y", sp.diff(f13, x) == y)
# --- Exercice 14 : x^3+y^3-3xy -----------------------------------------
f14 = x**3 + y**3 - 3*x*y
crit = sp.solve([sp.diff(f14, x), sp.diff(f14, y)], [x, y], dict=True)
crit_reels = [c for c in crit if c[x].is_real and c[y].is_real]
check("ex14 deux points critiques reels",
      sorted((c[x], c[y]) for c in crit_reels) == [(0, 0), (1, 1)])
check("ex14 (0,0) pas extremum", (0.1)**3 - 0 - 0 > 0 > (-0.1)**3)
vals = [float(f14.subs({x: 1 + a/100, y: 1 + b/100}))
        for a in range(-5, 6) for b in range(-5, 6)]
check("ex14 (1,1) minimum local", all(vv >= -1 - 1e-12 for vv in vals)
      and float(f14.subs({x: 1, y: 1})) == -1)
# --- Exercice 15 : extremums sur un carre ------------------------------
f15 = x**2 + y**2 - x - y
check("ex15 point critique (1/2,1/2)",
      sp.solve([sp.diff(f15, x), sp.diff(f15, y)], [x, y])
      == {x: sp.Rational(1, 2), y: sp.Rational(1, 2)})
check("ex15 minimum -1/2", f15.subs({x: sp.Rational(1, 2), y: sp.Rational(1, 2)})
      == -sp.Rational(1, 2))
grid = [float(f15.subs({x: a/20, y: b/20})) for a in range(21) for b in range(21)]
check("ex15 min et max sur le carre",
      isclose(min(grid), -0.5) and isclose(max(grid), 0.0))
check("ex15 max aux coins", f15.subs({x: 0, y: 0}) == 0
      and f15.subs({x: 1, y: 1}) == 0 and f15.subs({x: 1, y: 0}) == 0)
# --- Exercice 16 : le plan tangent approxime ---------------------------
f16 = sp.sqrt(x**2 + y**2)
g16 = sp.Matrix([sp.diff(f16, x), sp.diff(f16, y)]).subs({x: 3, y: 4})
check("ex16 gradient (3/5,4/5)", g16 == sp.Matrix([sp.Rational(3, 5),
      sp.Rational(4, 5)]))
approx16 = 5 + float(g16[0])*0.03 + float(g16[1])*(-0.04)
exact16 = sqrt(3.03**2 + 3.96**2)
check("ex16 approximation", isclose(approx16, exact16, abs_tol=5e-4))
# --- Exercice 17 : identite d'Euler ------------------------------------
f17 = x**2*y
check("ex17 Euler degre 3", sp.simplify(
    x*sp.diff(f17, x) + y*sp.diff(f17, y) - 3*f17) == 0)
f17b = x**3 - 2*x*y**2
check("ex17 Euler bis", sp.simplify(
    x*sp.diff(f17b, x) + y*sp.diff(f17b, y) - 3*f17b) == 0)
lam = sp.symbols("lambda", positive=True)
check("ex17 homogeneite", sp.simplify(
    f17.subs({x: lam*x, y: lam*y}) - lam**3*f17) == 0)
# --- Exercice 18 : droite de regression --------------------------------
a18, b18 = sp.symbols("a18 b18")
pts = [(0, 0), (1, 1), (2, 1)]
E18 = sum((a18*px + b18 - py)**2 for px, py in pts)
sol18 = sp.solve([sp.diff(E18, a18), sp.diff(E18, b18)], [a18, b18])
check("ex18 pente 1/2", sol18[a18] == sp.Rational(1, 2))
check("ex18 ordonnee 1/6", sol18[b18] == sp.Rational(1, 6))
check("ex18 erreur minimale", sp.simplify(E18.subs(sol18)) == sp.Rational(1, 6))
# --- Exercice 19 : Schwarz et son contre-exemple -----------------------
f19 = sp.exp(x*y)*sp.sin(x + y)
check("ex19 Schwarz pour une C^2", sp.simplify(
    sp.diff(f19, x, y) - sp.diff(f19, y, x)) == 0)
def f19b(a, b):
    if (a, b) == (0.0, 0.0):
        return 0.0
    return a*b*(a*a - b*b)/(a*a + b*b)
# valeurs exactes du contre-exemple : d2f/dxdy(0,0) = -1, d2f/dydx(0,0) = +1
h, d = 1e-8, 1e-3  # pas interieur h tres petit devant le pas exterieur d
dfx_at_0_y = lambda b: (f19b(h, b) - f19b(-h, b))/(2*h)   # ~ d f/dx (0,b)
dfy_at_x_0 = lambda a: (f19b(a, h) - f19b(a, -h))/(2*h)   # ~ d f/dy (a,0)
cross1 = (dfx_at_0_y(d) - dfx_at_0_y(-d))/(2*d)   # d/dy (df/dx) en 0
cross2 = (dfy_at_x_0(d) - dfy_at_x_0(-d))/(2*d)   # d/dx (df/dy) en 0
check("ex19 croisees -1 et +1", isclose(cross1, -1, abs_tol=1e-3)
      and isclose(cross2, 1, abs_tol=1e-3))
# --- Exercice 20 : fonctions harmoniques -------------------------------
for f20 in [x**2 - y**2, x*y, sp.exp(x)*sp.cos(y), sp.ln(x**2 + y**2)]:
    lap = sp.simplify(sp.diff(f20, x, 2) + sp.diff(f20, y, 2))
    check(f"ex20 harmonique {f20}", lap == 0)
# --- Exercice 21 : x^4+y^4-2(x-y)^2 ------------------------------------
f21 = x**4 + y**4 - 2*(x - y)**2
crit21 = sp.solve([sp.diff(f21, x), sp.diff(f21, y)], [x, y], dict=True)
reels21 = sorted(set((c[x], c[y]) for c in crit21 if c[x].is_real and c[y].is_real))
check("ex21 trois points critiques",
      reels21 == [(-sp.sqrt(2), sp.sqrt(2)), (0, 0), (sp.sqrt(2), -sp.sqrt(2))])
check("ex21 valeur minimale -8",
      f21.subs({x: sp.sqrt(2), y: -sp.sqrt(2)}) == -8)
check("ex21 (0,0) pas extremum",
      float(f21.subs({x: sp.Rational(1, 10), y: sp.Rational(1, 10)})) > 0
      > float(f21.subs({x: sp.Rational(1, 10), y: -sp.Rational(1, 10)})))
mini = min(float(f21.subs({x: a/10, y: b/10}))
           for a in range(-25, 26) for b in range(-25, 26))
check("ex21 minimum global -8", isclose(mini, -8, abs_tol=0.3))
# --- Exercice 22 : distance d'un point a une parabole ------------------
d22 = x**2 + (x**2 - 1)**2
crit22 = sp.solve(sp.diff(d22, x), x)
vals22 = sorted(sp.simplify(d22.subs(x, c)) for c in crit22)
check("ex22 points critiques 0, +-1/sqrt(2)",
      sorted(crit22) == [-sp.sqrt(2)/2, 0, sp.sqrt(2)/2])
check("ex22 distance minimale sqrt(3)/2", vals22[0] == sp.Rational(3, 4))
# --- Exercice 23 : polaires --------------------------------------------
f23 = x**2 + y**2
g23 = f23.subs({x: r*sp.cos(th), y: r*sp.sin(th)})
check("ex23 f en polaires = r^2", sp.simplify(g23) == r**2)
check("ex23 d/dr = 2r, d/dtheta = 0",
      sp.simplify(sp.diff(g23, r)) == 2*r and sp.simplify(sp.diff(g23, th)) == 0)
f23b = sp.atan2(y, x)
# derivee de l'angle le long d'un rayon : nulle
check("ex23 angle constant sur un rayon", sp.simplify(
    sp.diff(sp.atan2(r*sp.sin(th), r*sp.cos(th)), r)) == 0)
# --- Exercice 24 : moindres carres matriciels --------------------------
A24 = sp.Matrix([[0, 1], [1, 1], [2, 1]])
B24 = sp.Matrix([0, 1, 1])
X24 = (A24.T*A24).inv()*A24.T*B24
check("ex24 equations normales", X24 == sp.Matrix([sp.Rational(1, 2),
      sp.Rational(1, 6)]))
res = A24*X24 - B24
check("ex24 residu orthogonal aux colonnes", (A24.T*res).is_zero_matrix)
check("ex24 cout minimal 1/6", sp.simplify(res.dot(res)) == sp.Rational(1, 6))

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
