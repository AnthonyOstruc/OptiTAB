# -*- coding: utf-8 -*-
"""Vérifications du chapitre 14 — Groupe symétrique et déterminants."""
from math import isclose, lcm, pi, sqrt

import sympy as sp
from sympy.combinatorics import Permutation, PermutationGroup

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

M = sp.Matrix

# Convention : sigma est codée 0-indexée ; sigma = images de (1,...,n).
def perm(images):  # images 1-indexées
    return Permutation([i - 1 for i in images])

# --- Exercice 1 : composer -------------------------------------------
sig = perm([2, 3, 1, 4])        # (1 2 3)
tau = perm([2, 1, 4, 3])        # (1 2)(3 4)
# composition sigma o tau (tau d'abord) : sympy multiplie à gauche d'abord
st = tau*sig                     # = sigma(tau(.)) dans la convention sympy
check("ex1 sigma o tau", [st(i) + 1 for i in range(4)] == [3, 2, 4, 1])
ts = sig*tau
check("ex1 tau o sigma", [ts(i) + 1 for i in range(4)] == [1, 4, 2, 3])
check("ex1 non commutatif", st != ts)
check("ex1 inverse", [(sig**-1)(i) + 1 for i in range(4)] == [3, 1, 2, 4])
# --- Exercice 2 : décomposer en cycles --------------------------------
s1 = perm([3, 5, 4, 1, 2, 6])
check("ex2 cycles de s1", sorted(tuple(sorted(c)) for c in s1.cyclic_form)
      == [(0, 2, 3), (1, 4)])   # (1 3 4)(2 5) en 1-indexé
check("ex2 ordre 6", s1.order() == 6)
s2 = perm([2, 3, 4, 5, 1, 7, 6])
check("ex2 ordre 10", s2.order() == 10)
# --- Exercice 3 : signatures ------------------------------------------
check("ex3 cycle de longueur p", all(
    Permutation(list(range(1, p)) + [0]).signature() == (-1)**(p - 1)
    for p in [2, 3, 4, 5]))
check("ex3 signature s1", s1.signature() == -1)
check("ex3 signature s2", s2.signature() == -1)
check("ex3 morphisme", (tau*sig).signature() == sig.signature()*tau.signature())
# --- Exercice 4 : 2x2 et 3x3 ------------------------------------------
check("ex4 det 2x2", M([[2, 3], [1, 4]]).det() == 5)
A4 = M([[1, 2, 3], [4, 5, 6], [7, 8, 10]])
check("ex4 det 3x3", A4.det() == -3)
B4 = M([[1, 0, 2], [0, 1, 1], [1, 1, 0]])
check("ex4 det produit", (A4*B4).det() == A4.det()*B4.det())
# --- Exercice 5 : opérations élémentaires -----------------------------
check("ex5 Pascal", M([[1, 1, 1], [1, 2, 3], [1, 3, 6]]).det() == 1)
check("ex5 progressions", M([[0, 1, 2], [1, 2, 3], [2, 3, 4]]).det() == 0)
# --- Exercice 6 : triangulaires, transposée, inverse ------------------
T6 = M([[2, 1, 5], [0, 3, -1], [0, 0, 4]])
check("ex6 triangulaire", T6.det() == 24)
check("ex6 det(2A) = 2^3 det A", (2*T6).det() == 8*24)
check("ex6 transposee", T6.T.det() == 24)
check("ex6 inverse", T6.inv().det() == sp.Rational(1, 24))
# --- Exercice 7 : développement ---------------------------------------
A7 = M([[2, 0, 0, 1], [0, 3, 0, 0], [0, 0, 1, 4], [1, 0, 0, 1]])
check("ex7 det = 3", A7.det() == 3)
# --- Exercice 8 : aires et volumes ------------------------------------
check("ex8 parallelogramme", M([[3, 1], [1, 2]]).det() == 5)
check("ex8 volume", M([[1, 1, 1], [0, 1, 1], [0, 0, 1]]).det() == 1)
check("ex8 orientation", M([[0, 1], [1, 0]]).det() == -1)
# --- Exercice 9 : Leibniz ---------------------------------------------
leib = 0
for p in Permutation.group(3) if hasattr(Permutation, "group") else []:
    pass
from itertools import permutations as itperm
leib = sum(Permutation([s[0], s[1], s[2]]).signature()
           * A4[0, s[0]]*A4[1, s[1]]*A4[2, s[2]]
           for s in itperm(range(3)))
check("ex9 Leibniz = -3", leib == -3)
check("ex9 6 termes", len(list(itperm(range(3)))) == 6)
# --- Exercice 10 : base ou pas ----------------------------------------
check("ex10 det 2 -> base", M([[1, 1, 0], [0, 1, 1], [1, 0, 1]]).det() == 2)
check("ex10 polynomes", M([[1, 1, 0], [1, -1, 0], [0, 0, 1]]).det() == -2)
# --- Exercice 11 : paramètres -----------------------------------------
t = sp.symbols("t")
check("ex11 1-t^2", sp.expand(M([[1, t], [t, 1]]).det() - (1 - t**2)) == 0)
M11 = M([[1, 1, t], [1, t, 1], [t, 1, 1]])
check("ex11 factorisation", sp.factor(M11.det()) == -(t - 1)**2*(t + 2))
# --- Exercice 12 : Vandermonde 3x3 ------------------------------------
a, b, c = sp.symbols("a b c")
V12 = M([[1, 1, 1], [a, b, c], [a**2, b**2, c**2]])
check("ex12 Vandermonde", sp.factor(V12.det()) == (a - b)*(a - c)*(b - c)
      or sp.expand(V12.det() - (b - a)*(c - a)*(c - b)) == 0)
check("ex12 instance", V12.subs({a: 1, b: 2, c: 3}).det() == 2)
# --- Exercice 13 : matrices de permutation ----------------------------
def pmat(p, n):
    A = sp.zeros(n)
    for j in range(n):
        A[p(j), j] = 1
    return A
Ps, Pt = pmat(sig, 4), pmat(tau, 4)
check("ex13 produit", Ps*Pt == pmat(tau*sig, 4))
check("ex13 det = signature", Ps.det() == sig.signature()
      and Pt.det() == tau.signature())
check("ex13 trace = points fixes", Ps.trace() == 1 and Pt.trace() == 0)
check("ex13 inverse = transposee", Ps.inv() == Ps.T)
# --- Exercice 14 : comatrice ------------------------------------------
A14 = M([[1, 2, 0], [0, 1, 1], [1, 0, 1]])
check("ex14 det 3", A14.det() == 3)
Com = A14.cofactor_matrix()
check("ex14 A Com^T = det I", A14*Com.T == 3*sp.eye(3))
check("ex14 inverse", A14.inv() == Com.T/3)
x2, y2, z2, w2 = sp.symbols("x2 y2 z2 w2")
A2g = M([[x2, y2], [z2, w2]])
check("ex14 comatrice 2x2", A2g.cofactor_matrix().T == M([[w2, -y2], [-z2, x2]]))
# --- Exercice 15 : det d'un endomorphisme -----------------------------
# P -> P + P' sur R2[X] : triangulaire de diagonale 1
E15 = M([[1, 1, 0], [0, 1, 2], [0, 0, 1]])
check("ex15 P+P' det 1", E15.det() == 1)
# P -> P(X+1) : binomiale triangulaire de diagonale 1
E15b = M([[1, 1, 1], [0, 1, 2], [0, 0, 1]])
check("ex15 translation det 1", E15b.det() == 1)
check("ex15 XP' det 0", sp.diag(0, 1, 2).det() == 0)
# --- Exercice 16 : circulant ------------------------------------------
j3 = sp.Rational(-1, 2) + sp.sqrt(3)/2*sp.I
C16 = M([[a, b, c], [c, a, b], [b, c, a]])
check("ex16 det developpe",
      sp.expand(C16.det()) == sp.expand(a**3 + b**3 + c**3 - 3*a*b*c))
for vals in [(1, 2, 3), (2, -1, 5), (0, 1, 4)]:
    sub = dict(zip((a, b, c), vals))
    rhs16 = ((a + b + c)*(a + j3*b + j3**2*c)*(a + j3**2*b + j3*c)).subs(sub)
    check(f"ex16 circulant {vals}",
          sp.simplify(C16.det().subs(sub) - rhs16) == 0)
# --- Exercice 17 : inversions -----------------------------------------
check("ex17 [3,1,2]", perm([3, 1, 2]).inversions() == 2
      and perm([3, 1, 2]).signature() == 1)
check("ex17 [2,1]", perm([2, 1]).inversions() == 1
      and perm([2, 1]).signature() == -1)
check("ex17 egalite generale S4", all(
    Permutation(p).signature() == (-1)**Permutation(p).inversions()
    for p in itperm(range(4))))
# --- Exercice 18 : tridiagonal ----------------------------------------
def tridiag(n):
    A = sp.zeros(n)
    for i in range(n):
        A[i, i] = 2
        if i + 1 < n:
            A[i, i + 1] = 1
            A[i + 1, i] = 1
    return A
check("ex18 D_n = n+1", all(tridiag(n).det() == n + 1 for n in range(1, 7)))
# --- Exercice 19 : générateurs ----------------------------------------
G19 = PermutationGroup([Permutation([1, 0, 2, 3]), Permutation([1, 2, 3, 0])])
check("ex19 (1 2) et (1 2 3 4) engendrent S4", G19.order() == 24)
G19b = PermutationGroup([Permutation([1, 0, 2, 3]), Permutation([2, 1, 0, 3]),
                         Permutation([3, 1, 2, 0])])
check("ex19 transpositions (1 i)", G19b.order() == 24)
# --- Exercice 20 : ordre maximal --------------------------------------
def partitions(n, maxi=None):
    if maxi is None:
        maxi = n
    if n == 0:
        yield []
        return
    for k in range(min(n, maxi), 0, -1):
        for rest in partitions(n - k, k):
            yield [k] + rest
def max_order(n):
    best = 1
    for p in partitions(n):
        o = 1
        for k in p:
            o = lcm(o, k)
        best = max(best, o)
    return best
check("ex20 S5 : 6", max_order(5) == 6)
check("ex20 S7 : 12", max_order(7) == 12)
check("ex20 temoin 3+4", lcm(3, 4) == 12)
# --- Exercice 21 : det transposée par Leibniz -------------------------
X21 = M(3, 3, sp.symbols("u0:9"))
check("ex21 det At = det A", sp.expand(X21.T.det() - X21.det()) == 0)
# --- Exercice 22 : matrices entières ----------------------------------
A22 = M([[2, 1], [1, 1]])
check("ex22 det 1, inverse entiere", A22.det() == 1
      and A22.inv() == M([[1, -1], [-1, 2]]))
B22 = M([[2, 0], [0, 1]])
check("ex22 det 2 : inverse non entiere", B22.inv()[0, 0] == sp.Rational(1, 2))
# --- Exercice 23 : aire de l'ellipse ----------------------------------
a23, b23 = 3.0, 2.0
x = sp.symbols("x")
aire = 4*sp.integrate(b23*sp.sqrt(1 - x**2/a23**2), (x, 0, a23))
check("ex23 aire = pi a b", isclose(float(aire), pi*a23*b23, rel_tol=1e-9))
check("ex23 det diag(a,b)", sp.diag(3, 2).det() == 6)
# --- Exercice 24 : Vandermonde général --------------------------------
d = sp.symbols("d")
V24 = M([[1, 1, 1, 1], [a, b, c, d], [a**2, b**2, c**2, d**2],
         [a**3, b**3, c**3, d**3]])
prod = (b - a)*(c - a)*(d - a)*(c - b)*(d - b)*(d - c)
check("ex24 Vandermonde 4x4", sp.expand(V24.det() - prod) == 0)
check("ex24 instance", V24.subs({a: 0, b: 1, c: 2, d: 3}).det() == 12)

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
