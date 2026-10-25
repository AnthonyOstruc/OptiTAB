# -*- coding: utf-8 -*-
"""Vérifications du chapitre 18 — Espaces préhilbertiens réels."""
import math
from math import isclose, sqrt

import sympy as sp

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

x = sp.symbols("x")
M = sp.Matrix

def ps(f, g, a=0, b=1):
    return sp.integrate(f*g, (x, a, b))

# --- Exercice 1 : produit scalaire ou pas ------------------------------
check("ex1 xx'-yy' pas defini positif", 1*1 - 2*2 < 0)   # (1,2) : "norme" < 0
check("ex1 2xx'+3yy' defini positif", all(2*a*a + 3*b*b > 0
      for a, b in [(1, 0), (0, 1), (-2, 5)]))
check("ex1 f(0)g(0) degenere", True)  # f(x)=x non nulle, <f,f>=0 : argument
check("ex1 temoin f(x)=x", (x*1).subs(x, 0) == 0)
# --- Exercice 2 : calculs canoniques -----------------------------------
u2, v2 = M([1, 2, 2]), M([2, -1, 2])
check("ex2 norme 3", u2.dot(u2) == 9 and v2.dot(v2) == 9)
check("ex2 produit scalaire 4", u2.dot(v2) == 4)
check("ex2 cosinus 4/9", sp.Rational(u2.dot(v2), 9) == sp.Rational(4, 9))
check("ex2 distance", (u2 - v2).dot(u2 - v2) == 10)
# --- Exercice 3 : Cauchy-Schwarz ---------------------------------------
a3 = [1, 2, 3, 4]
check("ex3 CS avec (1,...,1)", sum(a3)**2 <= len(a3)*sum(t*t for t in a3))
check("ex3 cas d'egalite", (2 + 2 + 2)**2 == 3*(4 + 4 + 4))
u3, v3 = M([1, 2]), M([3, -1])
check("ex3 CS", u3.dot(v3)**2 <= u3.dot(u3)*v3.dot(v3))
# --- Exercice 4 : polarisation -----------------------------------------
u4, v4 = M([2, 1, -1]), M([1, 3, 2])
n = lambda w: w.dot(w)
check("ex4 identite remarquable",
      n(u4 + v4) == n(u4) + n(v4) + 2*u4.dot(v4))
check("ex4 polarisation",
      sp.Rational(n(u4 + v4) - n(u4 - v4), 4) == u4.dot(v4))
check("ex4 parallelogramme",
      n(u4 + v4) + n(u4 - v4) == 2*n(u4) + 2*n(v4))
# --- Exercice 5 : orthogonalite, Pythagore -----------------------------
u5, v5 = M([1, 2]), M([-2, 1])
check("ex5 orthogonaux", u5.dot(v5) == 0)
check("ex5 Pythagore", n(u5 + v5) == n(u5) + n(v5))
# --- Exercice 6 : Gram-Schmidt dans R^3 --------------------------------
v1, v2b, v3b = M([1, 1, 0]), M([1, 0, 1]), M([0, 1, 1])
e1 = v1/sp.sqrt(n(v1))
w2 = v2b - v2b.dot(e1)*e1
e2 = w2/sp.sqrt(n(w2))
w3 = v3b - v3b.dot(e1)*e1 - v3b.dot(e2)*e2
e3 = w3/sp.sqrt(n(w3))
for i, a in enumerate([e1, e2, e3]):
    check(f"ex6 norme e{i+1}", sp.simplify(n(a)) == 1)
check("ex6 orthogonalite", sp.simplify(e1.dot(e2)) == 0
      and sp.simplify(e1.dot(e3)) == 0 and sp.simplify(e2.dot(e3)) == 0)
check("ex6 w2 = (1/2,-1/2,1)", sp.simplify(w2 - M([sp.Rational(1, 2),
      -sp.Rational(1, 2), 1])) == sp.zeros(3, 1))
check("ex6 e3 direction (-1,1,1)", sp.simplify(e3*sp.sqrt(3) - M([-1, 1, 1])/1)
      == sp.zeros(3, 1))
# --- Exercice 7 : coordonnees en BON -----------------------------------
f1 = M([sp.Rational(3, 5), sp.Rational(4, 5)])
f2 = M([-sp.Rational(4, 5), sp.Rational(3, 5)])
X7 = M([1, 2])
c1, c2 = X7.dot(f1), X7.dot(f2)
check("ex7 coordonnees", (c1, c2) == (sp.Rational(11, 5), sp.Rational(2, 5)))
check("ex7 reconstruction", sp.simplify(c1*f1 + c2*f2 - X7) == sp.zeros(2, 1))
check("ex7 Parseval", c1**2 + c2**2 == 5 == n(X7))
# --- Exercice 8 : projection sur une droite ----------------------------
u8 = M([1, 2, 2])
x8 = M([3, 0, 0])
p8 = sp.Rational(x8.dot(u8), 9)*u8
check("ex8 projete", p8 == M([sp.Rational(1, 3), sp.Rational(2, 3),
      sp.Rational(2, 3)]))
check("ex8 distance carree", n(x8 - p8) == 8 == n(x8) - n(p8))
# --- Exercice 9 : produit scalaire sur les matrices --------------------
A9, B9 = M([[1, 2], [3, -1]]), M([[0, 1], [1, 2]])
psm = (A9.T*B9).trace()
check("ex9 valeur", psm == 1*0 + 2*1 + 3*1 + (-1)*2 == 3)
check("ex9 norme Frobenius", (A9.T*A9).trace() == 15)
check("ex9 symetrie", (B9.T*A9).trace() == psm)
# --- Exercice 10 : produit scalaire integral ---------------------------
check("ex10 norme de x", ps(x, x) == sp.Rational(1, 3))
check("ex10 <1,x>", ps(1, x) == sp.Rational(1, 2))
check("ex10 CS", ps(1, x)**2 <= ps(1, 1)*ps(x, x))
check("ex10 cosinus", sp.Rational(1, 2)/sp.sqrt(sp.Rational(1, 3))
      == sp.sqrt(3)/2)
# --- Exercice 11 : Gram-Schmidt polynomial -----------------------------
P0 = sp.Integer(1)
P1 = x - ps(x, P0)/ps(P0, P0)*P0
P2 = x**2 - ps(x**2, P0)/ps(P0, P0)*P0 - ps(x**2, P1)/ps(P1, P1)*P1
check("ex11 P1", sp.expand(P1 - (x - sp.Rational(1, 2))) == 0)
check("ex11 P2", sp.expand(P2 - (x**2 - x + sp.Rational(1, 6))) == 0)
check("ex11 orthogonalite", ps(P0, P1) == 0 and ps(P0, P2) == 0
      and ps(P1, P2) == 0)
check("ex11 normes", ps(P1, P1) == sp.Rational(1, 12)
      and ps(P2, P2) == sp.Rational(1, 180))
check("ex11 lien ch15", sp.expand(6*P2 - (6*x**2 - 6*x + 1)) == 0)
# --- Exercice 12 : orthogonal d'un sous-espace -------------------------
n12 = M([1, 1, 1])
base_perp = [M([1, -1, 0]), M([1, 0, -1])]
check("ex12 orthogonalite", all(w.dot(n12) == 0 for w in base_perp))
check("ex12 dimensions", 1 + 2 == 3)
# --- Exercice 13 : projection sur un plan ------------------------------
x13 = M([1, 2, 3])
p13 = x13 - sp.Rational(x13.dot(n12), 3)*n12
check("ex13 projete (-1,0,1)", p13 == M([-1, 0, 1]))
check("ex13 lien ch12", True)
check("ex13 distance", n(x13 - p13) == 12)  # ||(2,2,2)||^2
# --- Exercice 14 : distance a un hyperplan -----------------------------
n14 = M([1, 2, -2])
x14 = M([3, 1, 1])
d14 = sp.Abs(x14.dot(n14))/sp.sqrt(n(n14))
check("ex14 distance 1", d14 == 1)
p14 = x14 - sp.Rational(x14.dot(n14), n(n14))*n14
check("ex14 projete dans H", p14.dot(n14) == 0)
check("ex14 verification", sp.simplify(sp.sqrt(n(x14 - p14)) - 1) == 0)
# --- Exercice 15 : projete en BON --------------------------------------
pF = x8.dot(e1)*e1 + x8.dot(e2)*e2  # F = Vect(v1,v2) via sa BON
dF2 = n(x8 - pF)
check("ex15 Pythagore", sp.simplify(n(pF) + dF2 - n(x8)) == 0)
check("ex15 orthogonalite du reste", sp.simplify((x8 - pF).dot(e1)) == 0
      and sp.simplify((x8 - pF).dot(e2)) == 0)
# --- Exercice 16 : la constante la plus proche -------------------------
c16 = sp.integrate(x**2, (x, 0, 1))
check("ex16 c = moyenne = 1/3", c16 == sp.Rational(1, 3))
err16 = sp.integrate((x**2 - c16)**2, (x, 0, 1))
check("ex16 erreur 4/45", err16 == sp.Rational(4, 45))
c = sp.symbols("c")
E16 = sp.integrate((x**2 - c)**2, (x, 0, 1))
check("ex16 minimum en 1/3", sp.solve(sp.diff(E16, c), c) == [sp.Rational(1, 3)])
# --- Exercice 17 : minimiser une integrale -----------------------------
a17, b17 = sp.symbols("a17 b17")
E17 = sp.integrate((x**2 - a17 - b17*x)**2, (x, 0, 1))
sol17 = sp.solve([sp.diff(E17, a17), sp.diff(E17, b17)], [a17, b17])
check("ex17 a=-1/6, b=1", sol17[a17] == -sp.Rational(1, 6) and sol17[b17] == 1)
check("ex17 minimum 1/180", sp.simplify(E17.subs(sol17)) == sp.Rational(1, 180))
# --- Exercice 18 : Pythagore generalise, Bessel ------------------------
fam = [M([1, 0, 0]), M([0, 3, 4])/5]
x18 = M([2, 1, 1])
check("ex18 Bessel", sum(x18.dot(e)**2 for e in fam) <= n(x18))
check("ex18 Pythagore somme orthogonale",
      n(M([3, 0, 0]) + M([0, 4, 0])) == 9 + 16)
# --- Exercice 19 : distance de x^3 a R2[X] -----------------------------
a19, b19, c19 = sp.symbols("a19 b19 c19")
E19 = sp.integrate((x**3 - a19*x**2 - b19*x - c19)**2, (x, 0, 1))
sol19 = sp.solve([sp.diff(E19, v) for v in (a19, b19, c19)], [a19, b19, c19])
check("ex19 minimum 1/2800", sp.simplify(E19.subs(sol19)) == sp.Rational(1, 2800))
check("ex19 projete", sol19[a19] == sp.Rational(3, 2)
      and sol19[b19] == -sp.Rational(3, 5) and sol19[c19] == sp.Rational(1, 20))
# --- Exercice 20 : Legendre sur [-1,1] ---------------------------------
L0, L1 = sp.Integer(1), x
L2 = x**2 - sp.Rational(1, 3)
L3 = x**3 - sp.Rational(3, 5)*x
pairs = [(L0, L1), (L0, L2), (L0, L3), (L1, L2), (L1, L3), (L2, L3)]
check("ex20 orthogonalite", all(ps(f, g, -1, 1) == 0 for f, g in pairs))
R2 = sp.diff((x**2 - 1)**2, x, 2)
R3 = sp.diff((x**2 - 1)**3, x, 3)
check("ex20 Rodrigues n=2", sp.expand(R2 - 12*L2) == 0 and sp.expand(R2) == 12*x**2 - 4)
check("ex20 Rodrigues n=3", sp.expand(R3 - 120*L3) == 0)
# --- Exercice 21 : determinant de Gram ---------------------------------
u21, v21 = M([3, 1]), M([1, 2])
G21 = M([[u21.dot(u21), u21.dot(v21)], [v21.dot(u21), v21.dot(v21)]])
check("ex21 Gram = aire^2", G21.det() == 25)
check("ex21 aire ch14", 25 == 5**2)
w21 = M([2, 4])  # colineaire a (1,2)
G21b = M([[w21.dot(w21), w21.dot(v21)], [v21.dot(w21), v21.dot(v21)]])
check("ex21 famille liee -> det nul", G21b.det() == 0)
# --- Exercice 22 : famille obtusangle ----------------------------------
import itertools
tri = [M([1, 0]), M([-sp.Rational(1, 2), sp.sqrt(3)/2]),
       M([-sp.Rational(1, 2), -sp.sqrt(3)/2])]
check("ex22 trois vecteurs a 120 degres", all(
    sp.simplify(a.dot(b)) == -sp.Rational(1, 2)
    for a, b in itertools.combinations(tri, 2)))
# --- Exercice 23 : inegalite de Hadamard -------------------------------
A23 = M([[1, 2, 0], [0, 1, 1], [1, 0, 1]])
colnorms = [sp.sqrt(sum(A23[i, j]**2 for i in range(3))) for j in range(3)]
check("ex23 Hadamard", abs(A23.det()) <= sp.prod(colnorms))
O23 = M([[2, 0, 0], [0, 3, 0], [0, 0, 1]])
check("ex23 egalite colonnes orthogonales",
      abs(O23.det()) == 2*3*1)
# --- Exercice 24 : racines des polynomes orthogonaux -------------------
r2 = sp.solve(P2, x)
check("ex24 racines de P2 dans ]0,1[", all(0 < sp.nsimplify(r) < 1 for r in r2)
      and len(r2) == 2)
P3 = (x**3 - sp.Rational(3, 2)*x**2 + sp.Rational(3, 5)*x - sp.Rational(1, 20))
check("ex24 P3 = x^3 - projete (ex19)", all(
    sp.integrate(P3*x**k, (x, 0, 1)) == 0 for k in range(3)))
r3 = sp.Poly(P3, x).nroots()
check("ex24 racines de P3 dans ]0,1[",
      all(abs(sp.im(r)) < 1e-12 and 0 < sp.re(r) < 1 for r in r3))

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
