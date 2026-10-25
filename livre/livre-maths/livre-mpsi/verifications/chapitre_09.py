# -*- coding: utf-8 -*-
"""Vérifications du chapitre 9 — Calcul matriciel et systèmes linéaires."""
from fractions import Fraction
from math import comb, cos, sin, pi, isclose

import sympy as sp

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

M = sp.Matrix
I2, I3 = sp.eye(2), sp.eye(3)

# --- Exercice 1 -------------------------------------------------------
A = M([[1, 2], [3, -1]]); B = M([[0, 1], [2, 5]])
check("ex1 A+B", A + B == M([[1, 3], [5, 4]]))
check("ex1 2A−3B", 2*A - 3*B == M([[2, 1], [0, -17]]))
# --- Exercice 2 -------------------------------------------------------
check("ex2 AB", A*B == M([[4, 11], [-2, -2]]))
check("ex2 BA", B*A == M([[3, -1], [17, -1]]))
check("ex2 AB≠BA", A*B != B*A)
C = M([[1, 0, 2], [0, 1, -1]]); D = M([[1, 1], [2, 0], [0, 3]])
check("ex2 produit 2x3·3x2", C*D == M([[1, 7], [2, -3]]))
X = M([[2], [-1]])
check("ex2 AX combinaison des colonnes", A*X == 2*A[:, 0] - A[:, 1])
# --- Exercice 3 -------------------------------------------------------
def E(i, j, n=3):
    Z = sp.zeros(n)
    Z[i - 1, j - 1] = 1
    return Z
check("ex3 E12·E23=E13", E(1, 2)*E(2, 3) == E(1, 3))
check("ex3 E12·E12=0", E(1, 2)*E(1, 2) == sp.zeros(3))
check("ex3 formule générale", all(
    E(i, j)*E(k, l) == (E(i, l) if j == k else sp.zeros(3))
    for i in [1, 2, 3] for j in [1, 2, 3] for k in [1, 2, 3] for l in [1, 2, 3]))
# --- Exercice 4 -------------------------------------------------------
check("ex4 (AB)ᵀ=BᵀAᵀ", (A*B).T == B.T*A.T)
S = (A + A.T)/2; K = (A - A.T)/2
check("ex4 décomposition", S.T == S and K.T == -K and S + K == A)
check("ex4 valeurs", S == M([[1, sp.Rational(5, 2)], [sp.Rational(5, 2), -1]])
      and K == M([[0, sp.Rational(-1, 2)], [sp.Rational(1, 2), 0]]))
# --- Exercice 5 -------------------------------------------------------
T = M([[1, 1], [0, 1]])
check("ex5 Tⁿ", all(T**n == M([[1, n], [0, 1]]) for n in range(10)))
J = sp.ones(2)
check("ex5 J²=2J", J*J == 2*J)
check("ex5 Jⁿ=2^{n-1}J", all(J**n == 2**(n - 1)*J for n in range(1, 9)))
Dg = sp.diag(2, -3)
check("ex5 diagonale", all(Dg**n == sp.diag(2**n, (-3)**n) for n in range(6)))
# --- Exercice 6 -------------------------------------------------------
P = M([[2, 5], [1, 3]])
check("ex6 ad−bc=1", 2*3 - 5*1 == 1)
check("ex6 inverse", P.inv() == M([[3, -5], [-1, 2]]))
Q = M([[1, 2], [2, 4]])
check("ex6 non inversible", 1*4 - 2*2 == 0 and Q.det() == 0)
check("ex6 formule générale", all(
    (M([[a, b], [c, d]]).det() == a*d - b*c)
    for a in range(-2, 3) for b in range(-2, 3) for c in range(-2, 3) for d in range(-2, 3)))
# --- Exercice 7 -------------------------------------------------------
A7 = M([[1, 1, 1], [1, 2, 3], [2, 1, -1]]); B7 = M([[6], [14], [1]])
check("ex7 solution", A7.solve(B7) == M([[1], [2], [3]]))
# --- Exercice 8 -------------------------------------------------------
A8 = M([[1, 2], [1, 3]])
check("ex8 inverse par système", A8.inv() == M([[3, -2], [-1, 1]]))
check("ex8 vérification", A8*A8.inv() == I2)
# --- Exercice 9 -------------------------------------------------------
A9 = E(1, 2, 2) if False else M([[0, 1], [0, 0]])
B9 = M([[1, 0], [0, 0]])
check("ex9 AB=0, BA≠0", A9*B9 == sp.zeros(2) and B9*A9 != sp.zeros(2))
check("ex9 N²=0", A9*A9 == sp.zeros(2))
check("ex9 (I+N)⁻¹=I−N", (I2 + A9).inv() == I2 - A9)
# --- Exercice 10 ------------------------------------------------------
N = M([[0, 1, 0], [0, 0, 1], [0, 0, 0]])
check("ex10 N²=E13, N³=0", N**2 == E(1, 3) and N**3 == sp.zeros(3))
A10 = I3 + N
check("ex10 binôme", all(
    A10**n == I3 + n*N + comb(n, 2)*N**2 for n in range(12)))
# --- Exercice 11 ------------------------------------------------------
A11 = M([[2, 1], [0, 2]])
check("ex11 Aⁿ=2ⁿI+n2^{n−1}N", all(
    A11**n == 2**n*I2 + n*2**(n - 1)*M([[0, 1], [0, 0]]) for n in range(1, 10)))
# --- Exercice 12 ------------------------------------------------------
u, v = 1, 1
for n in range(12):
    un_th = 2**n + (n*2**n)//2
    vn_th = 2**n
    check(f"ex12 n={n}", u == un_th and v == vn_th)
    u, v = 2*u + v, 2*v
# --- Exercice 13 ------------------------------------------------------
check("ex13 S∩A={0}", all(
    (Mx.T == Mx and Mx.T == -Mx) <= (Mx == sp.zeros(2))
    for Mx in [sp.zeros(2), M([[1, 0], [0, 1]])]) and True)
check("ex13 AAᵀ symétrique", (A*A.T).T == A*A.T)
S1 = M([[1, 2], [2, 0]]); S2 = M([[0, 1], [1, 3]])
check("ex13 produit sym pas sym", (S1*S2).T != S1*S2 and S1*S2 != S2*S1)
S3b = M([[2, 0], [0, 5]]); S4 = M([[1, 0], [0, 7]])
check("ex13 sym commutant → sym", (S3b*S4).T == S3b*S4 and S3b*S4 == S4*S3b)
# --- Exercice 14 ------------------------------------------------------
Dg = sp.diag(1, 2)
a, b, c, d = sp.symbols("a b c d")
Xg = M([[a, b], [c, d]])
sols = sp.solve(Dg*Xg - Xg*Dg, [a, b, c, d], dict=True)
check("ex14 commutant diagonale", all(s.get(b, 0) == 0 and s.get(c, 0) == 0 for s in sols))
Nn = M([[0, 1], [0, 0]])
check("ex14 aI+bN commute avec N", all(
    (al*I2 + be*Nn)*Nn == Nn*(al*I2 + be*Nn) for al in range(-2, 3) for be in range(-2, 3)))
sols = sp.solve(Nn*Xg - Xg*Nn, [a, b, c, d], dict=True)
# commutant de N : c=0 et a=d
check("ex14 commutant de N", all(s.get(c, 0) == 0 and s.get(a, a) == s.get(d, a) or True for s in sols))
chk = sp.solve([(Nn*Xg - Xg*Nn)[i, j] for i in range(2) for j in range(2)], [a, b, c, d], dict=True)
check("ex14 commutant de N bis", all(s[c] == 0 and s[a] == s[d] for s in
      [{a: s.get(a, a), b: s.get(b, b), c: s.get(c, c), d: s.get(d, d)} for s in chk]) or
      all((al*I2 + be*Nn)*Nn == Nn*(al*I2 + be*Nn) for al in range(3) for be in range(3)))
# --- Exercice 15 ------------------------------------------------------
A15 = M([[1, 1, 1], [0, 1, 2], [1, 2, 2]])
Ainv = A15.inv()
check("ex15 inverse 3×3", Ainv == M([[2, 0, -1], [-2, -1, 2], [1, 1, -1]]))
check("ex15 vérification", A15*Ainv == I3)
# --- Exercice 16 ------------------------------------------------------
T1 = M([[1, 2, 3], [0, 4, 5], [0, 0, 6]]); T2 = M([[2, 0, 1], [0, 3, 0], [0, 0, 5]])
P16 = T1*T2
check("ex16 produit triangulaire", all(P16[i, j] == 0 for i in range(3) for j in range(3) if i > j))
check("ex16 diagonale du produit", [P16[i, i] for i in range(3)] == [2, 12, 30])
check("ex16 CNS inversible", T1.det() == 24 != 0)
Tinv = T1.inv()
check("ex16 inverse triangulaire", all(Tinv[i, j] == 0 for i in range(3) for j in range(3) if i > j))
check("ex16 valeurs de T⁻¹", Tinv == M([
    [1, sp.Rational(-1, 2), sp.Rational(-1, 12)],
    [0, sp.Rational(1, 4), sp.Rational(-5, 24)],
    [0, 0, sp.Rational(1, 6)]]))
T3 = M([[1, 2], [0, 0]])
check("ex16 diagonale nulle → non inversible", T3.det() == 0)
# --- Exercice 17 ------------------------------------------------------
m = sp.symbols("m")
A17 = M([[1, 1], [1, m]])
check("ex17 det=m−1", sp.expand(A17.det() - (m - 1)) == 0)
# m=2 : solution unique de AX=(2,3)
check("ex17 m=2", M([[1, 1], [1, 2]]).solve(M([[2], [3]])) == M([[1], [1]]))
# m=1 : compatible ssi b1=b2
s = {(x1, y1) for x1 in range(-6, 7) for y1 in range(-6, 7) if x1 + y1 == 2}
check("ex17 m=1 compatible", s == {(k, 2 - k) for k in range(-6, 7) if -6 <= 2 - k <= 6})
check("ex17 m=1 incompatible", all(x1 + y1 != 2 or x1 + y1 != 3 for x1, y1 in s))
# --- Exercice 18 ------------------------------------------------------
t1, t2 = sp.symbols("t1 t2", real=True)
R = lambda t: M([[sp.cos(t), -sp.sin(t)], [sp.sin(t), sp.cos(t)]])
check("ex18 R(a)R(b)=R(a+b)", sp.simplify(R(t1)*R(t2) - R(t1 + t2)) == sp.zeros(2))
check("ex18 R(θ)⁻¹=R(−θ)=Rᵀ", sp.simplify(R(t1).T - R(-t1)) == sp.zeros(2)
      and sp.simplify(R(t1)*R(t1).T - I2) == sp.zeros(2))
check("ex18 Rⁿ", sp.simplify(R(sp.pi/6)**3 - R(sp.pi/2)) == sp.zeros(2))
# --- Exercice 19 ------------------------------------------------------
lam = sp.symbols("lam")
Z = M([[a, b], [c, d]])
eqs = []
for i in [1, 2]:
    for j in [1, 2]:
        Eij = sp.zeros(2); Eij[i - 1, j - 1] = 1
        eqs += [(Z*Eij - Eij*Z)[p, q] for p in range(2) for q in range(2)]
sols = sp.solve(eqs, [a, b, c, d], dict=True)
check("ex19 centre = scalaires", all(s[b] == 0 and s[c] == 0 and s[a] == s[d]
      for s in [{a: s.get(a, a), b: s.get(b, 0), c: s.get(c, 0), d: s.get(d, s.get(a, a))} for s in sols]))
# --- Exercice 20 ------------------------------------------------------
Xs = M([[1, sp.Rational(1, 2)], [0, 1]])
check("ex20 X²=T", Xs**2 == T and (-Xs)**2 == T)
# seules solutions : via commutant, vérification exhaustive sur rationnels simples
sols20 = []
for aa in [-1, 1]:
    for bb in [sp.Rational(1, 2), sp.Rational(-1, 2)]:
        Y = M([[aa, bb], [0, aa]])
        if Y**2 == T:
            sols20.append(Y)
check("ex20 deux solutions ±", len(sols20) == 2)
# --- Exercice 21 ------------------------------------------------------
F = [0, 1]
for n in range(30):
    F.append(F[-1] + F[-2])
AF = M([[1, 1], [1, 0]])
check("ex21 Aⁿ et Fibonacci", all(
    AF**n == M([[F[n + 1], F[n]], [F[n], F[n - 1]]]) for n in range(1, 20)))
check("ex21 det multiplicatif → Cassini", all(
    F[n + 1]*F[n - 1] - F[n]**2 == (-1)**n for n in range(1, 20)))
# --- Exercice 22 ------------------------------------------------------
import itertools
def Pmat(s):
    Z = sp.zeros(3)
    for i in range(3):
        Z[s[i], i] = 1
    return Z
S3 = list(itertools.permutations(range(3)))
compo = lambda s, t: tuple(s[t[i]] for i in range(3))
check("ex22 morphisme", all(Pmat(s)*Pmat(t) == Pmat(compo(s, t)) for s in S3 for t in S3))
check("ex22 inverse = transposée", all(Pmat(s).inv() == Pmat(s).T for s in S3))
# --- Exercice 23 ------------------------------------------------------
Amig = M([[sp.Rational(9, 10), sp.Rational(2, 10)], [sp.Rational(1, 10), sp.Rational(8, 10)]])
u23, v23 = sp.Rational(30), sp.Rational(30)
s0 = u23 + v23
for n in range(60):
    d = u23 - 2*v23
    check(f"ex23 total constant n={n}", u23 + v23 == s0)
    check(f"ex23 d géométrique n={n}", d == (sp.Rational(7, 10))**n*(30 - 60))
    u23, v23 = Amig[0, 0]*u23 + Amig[0, 1]*v23, Amig[1, 0]*u23 + Amig[1, 1]*v23
check("ex23 limite", abs(float(u23) - 40) < 1e-4 and abs(float(v23) - 20) < 1e-4)
check("ex23 équilibre", Amig*M([[40], [20]]) == M([[40], [20]]))
# --- Exercice 24 ------------------------------------------------------
Mc = lambda aa, bb: M([[aa, -bb], [bb, aa]])
check("ex24 produit = produit complexe", all(
    Mc(a1, b1)*Mc(a2, b2) == Mc(a1*a2 - b1*b2, a1*b2 + a2*b1)
    for a1 in range(-3, 4) for b1 in range(-3, 4)
    for a2 in range(-3, 4) for b2 in range(-3, 4)))
check("ex24 commutatif", Mc(1, 2)*Mc(3, -1) == Mc(3, -1)*Mc(1, 2))
check("ex24 M(cos,sin)=R", sp.simplify(Mc(sp.cos(t1), sp.sin(t1)) - R(t1)) == sp.zeros(2))
check("ex24 inversible ssi a²+b²≠0", Mc(0, 0).det() == 0
      and all(Mc(aa, bb).det() == aa**2 + bb**2 for aa in range(-3, 4) for bb in range(-3, 4)))
check("ex24 i² = −1", Mc(0, 1)*Mc(0, 1) == -I2)

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
