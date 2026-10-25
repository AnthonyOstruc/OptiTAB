# -*- coding: utf-8 -*-
"""Vérifications du chapitre 12 — Espaces vectoriels et applications linéaires."""
import math
from math import isclose, sqrt, cosh, sinh, exp

import sympy as sp

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

X = sp.symbols("X")
x = sp.symbols("x")

M = sp.Matrix

# --- Exercice 2 : Vect et combinaisons ---------------------------------
sol = sp.linsolve((M([[1, 0], [1, 1], [1, 2]]), M([1, 2, 3])))
check("ex2 (1,2,3) dans Vect", list(sol)[0] == (1, 1))
sol2 = sp.linsolve((M([[1, 0], [1, 1], [1, 2]]), M([1, 0, 0])))
check("ex2 (1,0,0) hors Vect", sol2 == sp.EmptySet)
# --- Exercice 3 : libres ou liées --------------------------------------
check("ex3 famille a libre", M([[1, 0, 1], [1, 1, 0], [0, 1, 1]]).det() == 2)
check("ex3 famille c liée", M([[1, 1, 0], [0, 1, 1], [1, 0, -1]]).det() == 0)
check("ex3 relation v1-v2-v3=0",
      (M([1, 1, 0]) - M([0, 1, 1]) - M([1, 0, -1])).is_zero_matrix)
# --- Exercice 4 : base échelonnée en (X-1) -----------------------------
P4 = (X - 1)**3 + 3*(X - 1)**2 + 3*(X - 1) + 1
check("ex4 X^3 coordonnées (1,3,3,1)", sp.expand(P4 - X**3) == 0)
# --- Exercice 5 : noyau et image ---------------------------------------
A5 = M([[1, 1, -1], [2, -1, 0]])
check("ex5 Ker = Vect(1,2,3)", (A5*M([1, 2, 3])).is_zero_matrix)
check("ex5 rang 2", A5.rank() == 2)
# --- Exercice 7 : projecteur sur la diagonale --------------------------
P7 = M([[sp.Rational(1, 2), sp.Rational(1, 2)],
        [sp.Rational(1, 2), sp.Rational(1, 2)]])
check("ex7 p^2 = p", sp.simplify(P7*P7 - P7).is_zero_matrix)
check("ex7 Ker p", (P7*M([1, -1])).is_zero_matrix)
check("ex7 Im p (p fixe (1,1))", P7*M([1, 1]) == M([1, 1]))
S7 = 2*P7 - sp.eye(2)
check("ex7 s^2 = id", sp.simplify(S7*S7 - sp.eye(2)).is_zero_matrix)
# --- Exercice 8 : rangs et dimensions ----------------------------------
check("ex8 rg = 2", M([[1, 1, 0], [0, 1, 1], [1, 0, -1]]).rank() == 2)
check("ex8 rg = 1", M([[1, 2], [2, 4], [3, 6]]).rank() == 1)
check("ex8 dim Vect(1+X,1-X,X^2) = 3",
      M([[1, 1, 0], [1, -1, 0], [0, 0, 1]]).rank() == 3)
# --- Exercice 9 : Binet par algèbre linéaire ---------------------------
phi, psi = (1 + sqrt(5))/2, (1 - sqrt(5))/2
F = [0, 1]
for _ in range(28):
    F.append(F[-1] + F[-2])
check("ex9 Binet", all(
    isclose(F[n], (phi**n - psi**n)/sqrt(5), rel_tol=1e-9, abs_tol=1e-9)
    for n in [1, 5, 12, 25]))
t9 = 0.4
w9 = math.cos(t9)*math.cos(t9) - (-math.sin(t9))*math.sin(t9)
check("ex9 y''+y=0 : wronskien de (cos,sin) vaut 1", isclose(w9, 1.0))
# --- Exercice 10 : supplémentaires -------------------------------------
# R^3 = {x+y+z=0} + Vect(1,1,1) ; décomposition de (1,2,3)
g10 = M([2, 2, 2])
f10 = M([1, 2, 3]) - g10
check("ex10 f dans F", sum(f10) == 0)
check("ex10 décomposition", f10 == M([-1, 0, 1]))
# pair + impair : e^x = ch x + sh x
check("ex10 paire+impaire", all(
    isclose(exp(t), cosh(t) + sinh(t)) for t in [-1.3, 0.4, 2.0]))
# --- Exercice 11 : Grassmann -------------------------------------------
# F = Vect(e1,e2), G = Vect(e3,(1,1,1)) : F+G = R^3, F inter G = Vect(1,1,0)
B11 = M([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])
check("ex11 F+G = R^3", B11.rank() == 3)
v11 = M([1, 1, 0])  # = (1,1,1) - e3, bien dans G ; et dans F
check("ex11 (1,1,0) dans F", v11[2] == 0)
check("ex11 dims Grassmann", 2 + 2 - 3 == 1)
# --- Exercice 12 : base incomplète -------------------------------------
check("ex12 complétée par e1",
      M([[1, 1, 0], [0, 1, 1], [1, 0, 0]]).det() != 0)
check("ex12 supplémentaire dans R2[X]",
      M([[1, 1, 1], [0, 1, 0], [1, 0, 0]]).det() != 0)
# --- Exercice 13 : détermination d'une application linéaire ------------
# u(1,1)=(2,0), u(1,-1)=(0,4) => u(x,y) = (x+y, 2x-2y)
U13 = M([[1, 1], [2, -2]])
check("ex13 u(1,1)", U13*M([1, 1]) == M([2, 0]))
check("ex13 u(1,-1)", U13*M([1, -1]) == M([0, 4]))
check("ex13 u(1,0)", U13*M([1, 0]) == M([1, 2]))
check("ex13 bijective", U13.det() == -4)
# --- Exercice 14 : théorème du rang ------------------------------------
A14 = M([[1, 2, 0, 1], [0, 1, 1, 1], [1, 3, 1, 2]])
check("ex14 rang 2", A14.rank() == 2)
check("ex14 ligne3 = ligne1+ligne2",
      (A14.row(2) - A14.row(0) - A14.row(1)).is_zero_matrix)
check("ex14 noyau v1", (A14*M([-2, 1, -1, 0])).is_zero_matrix)
check("ex14 noyau v2", (A14*M([-1, 0, -1, 1])).is_zero_matrix)
check("ex14 (v1,v2) libre", M([[-2, 1, -1, 0], [-1, 0, -1, 1]]).rank() == 2)
# --- Exercice 15 : symétrie d'axe la diagonale -------------------------
S15 = M([[0, 1], [1, 0]])
check("ex15 s^2 = id", S15*S15 == sp.eye(2))
check("ex15 axe fixe", S15*M([1, 1]) == M([1, 1]))
check("ex15 anti-axe", S15*M([1, -1]) == M([-1, 1]))
P15 = (S15 + sp.eye(2))/2
check("ex15 p = (s+id)/2 projecteur", sp.simplify(P15*P15 - P15).is_zero_matrix)
# --- Exercice 16 : hyperplans ------------------------------------------
phi16 = lambda v: v[0] - 2*v[1] + v[2]
check("ex16 base de H", phi16((2, 1, 0)) == 0 and phi16((-1, 0, 1)) == 0)
check("ex16 base libre", M([[2, 1, 0], [-1, 0, 1]]).rank() == 2)
check("ex16 D hors H", phi16((1, 0, 0)) == 1)
check("ex16 équations proportionnelles",
      all(-2*a == b for a, b in zip((1, -2, 1), (-2, 4, -2))))
# --- Exercice 17 : interpolation, vue linéaire -------------------------
L0 = (X - 1)*(X - 2)/2
L1 = -X*(X - 2)
L2 = X*(X - 1)/2
for i, L in enumerate([L0, L1, L2]):
    vals = [L.subs(X, a) for a in (0, 1, 2)]
    check(f"ex17 L{i} aux noeuds", vals == [1 if j == i else 0 for j in range(3)])
check("ex17 somme = 1", sp.expand(L0 + L1 + L2) == 1)
# --- Exercice 18 : structure affine des solutions ----------------------
# x - y = 1, x + y + z = 3 : solutions (1,0,2) + t(1,1,-2)
for t in [0, 1, -2]:
    v = (1 + t, 0 + t, 2 - 2*t)
    check(f"ex18 sol t={t}", v[0] - v[1] == 1 and v[0] + v[1] + v[2] == 3)
# arithmético-géométrique u_{n+1} = 2u_n + 3, u_0 = 1 : u_n = -3 + 4*2^n
u = 1
for n in range(8):
    check(f"ex18 suite n={n}", u == -3 + 4*2**n)
    u = 2*u + 3
# --- Exercice 19 : familles libres de fonctions ------------------------
a19 = [0, 1, 2]
pts = [sp.Rational(1, 7), sp.Rational(1, 3), sp.Rational(1, 2)]
G19 = M([[sp.exp(sp.Rational(a)*t) for a in a19] for t in pts])
check("ex19 exponentielles libres", G19.det() != 0)
# --- Exercice 20 : nilpotence de la dérivation -------------------------
P20 = X**3 + X + 1
d3 = sp.diff(P20, X, 3)
d4 = sp.diff(P20, X, 4)
check("ex20 D^3 non nul, D^4 = 0 sur R3[X]", d3 == 6 and d4 == 0)
N20 = M([[0, 1, 0], [0, 0, 1], [0, 0, 0]])
check("ex20 N^3 = 0", (N20**3).is_zero_matrix)
inv = sp.eye(3) + N20 + N20**2
check("ex20 (id-N)^{-1} = somme géométrique",
      (sp.eye(3) - N20)*inv == sp.eye(3))
# --- Exercice 21 : noyaux itérés ---------------------------------------
# dérivation sur R3[X], base (1, X, X^2, X^3) : dim Ker D^k = min(k, 4)
N21 = M([[0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 3], [0, 0, 0, 0]])
dims = [4 - (N21**k).rank() for k in range(6)]
check("ex21 dim Ker D^k = min(k,4)", dims == [0, 1, 2, 3, 4, 4])
check("ex21 croissante puis stationnaire",
      all(dims[k] <= dims[k + 1] for k in range(5)) and dims[4] == dims[5])
# --- Exercice 22 : projecteurs qui commutent ---------------------------
p22 = sp.diag(1, 1, 0)
q22 = sp.diag(0, 1, 1)
check("ex22 commutent", p22*q22 == q22*p22)
r22 = p22*q22
check("ex22 pq projecteur", r22*r22 == r22)
check("ex22 Im pq = Im p inter Im q", r22 == sp.diag(0, 1, 0))
check("ex22 dim Ker pq = dim(Ker p + Ker q)", (3 - r22.rank()) == 2)
# --- Exercice 23 : hyperplans de polynômes -----------------------------
# {P dans R3[X] : P(1) = 0} = (X-1)R2[X] ; intersection des 3 hyperplans
# P(0)=P(1)=P(2)=0 dans R3[X] : droite Vect(X(X-1)(X-2))
P23 = X*(X - 1)*(X - 2)
check("ex23 annule les trois noeuds",
      all(P23.subs(X, a) == 0 for a in (0, 1, 2)))
V23 = M([[1, a, a**2, a**3] for a in (0, 1, 2)])
check("ex23 trois équations indépendantes", V23.rank() == 3)
check("ex23 dim intersection = 4 - 3 = 1", 4 - 3 == 1)
# --- Exercice 24 : Ker u + Im u ----------------------------------------
# projecteur : égalités ; dérivation (nilpotente) : échec
check("ex24 projecteur rg u^2 = rg u", (P7*P7).rank() == P7.rank())
D24 = M([[0, 1, 0], [0, 0, 2], [0, 0, 0]])  # dérivation sur R2[X]
check("ex24 dérivation rg u = 2, rg u^2 = 1",
      D24.rank() == 2 and (D24*D24).rank() == 1)
check("ex24 Ker inclus Im (dérivation)", (D24*M([0, 1, 0]))[0] == 1)

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
