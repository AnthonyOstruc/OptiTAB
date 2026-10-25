# -*- coding: utf-8 -*-
"""Vérifications du chapitre 13 — Matrices."""
from math import isclose, sqrt, comb

import sympy as sp

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

M = sp.Matrix

# --- Exercice 1 : écrire des matrices ----------------------------------
A1 = M([[1, 1], [2, -1], [1, 0]])          # u(x,y) = (x+y, 2x-y, x)
check("ex1 u(1,0) et u(0,1)", A1*M([1, 0]) == M([1, 2, 1]) and A1*M([0, 1]) == M([1, -1, 0]))
D1 = M([[0, 1, 0], [0, 0, 2], [0, 0, 0]])  # dérivation, base (1, X, X^2)
check("ex1 D(X^2) = 2X", D1*M([0, 0, 1]) == M([0, 2, 0]))
T1 = sp.diag(0, 1, 2)                       # P -> XP'
check("ex1 XP' diagonale", T1*M([1, 1, 1]) == M([0, 1, 2]))
# --- Exercice 2 : produits ---------------------------------------------
A2, B2 = M([[1, 2], [3, 4]]), M([[0, 1], [1, 0]])
check("ex2 AB", A2*B2 == M([[2, 1], [4, 3]]))
check("ex2 BA different", B2*A2 == M([[3, 4], [1, 2]]) and A2*B2 != B2*A2)
C2 = M([[1, 0], [2, 1]])
check("ex2 associativite", (A2*B2)*C2 == A2*(B2*C2))
# --- Exercice 3 : Y = AX -----------------------------------------------
A3 = M([[1, 1], [1, 2]])
check("ex3 image", A3*M([1, 2]) == M([3, 5]))
check("ex3 antecedent unique", list(sp.linsolve((A3, M([3, 5]))))[0] == (1, 2))
# --- Exercice 4 : noyau, image, rang -----------------------------------
A4 = M([[1, 2, 3], [2, 4, 6], [1, 1, 1]])
check("ex4 rang 2", A4.rank() == 2)
check("ex4 noyau", (A4*M([1, -2, 1])).is_zero_matrix)
check("ex4 image libre", M([[1, 2, 1], [2, 4, 1]]).rank() == 2)
# --- Exercice 5 : inversibles ------------------------------------------
check("ex5 inverse 2x2", A2.inv() == M([[-2, 1], [sp.Rational(3, 2), -sp.Rational(1, 2)]]))
B5 = M([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
check("ex5 B non inversible (rang 2)", B5.rank() == 2)
T5 = M([[2, 1, 5], [0, 3, -1], [0, 0, 4]])
check("ex5 triangulaire inversible", T5.rank() == 3)
# --- Exercice 6 : matrice de passage -----------------------------------
P6 = M([[1, 1], [1, -1]])
check("ex6 P inverse", P6.inv() == sp.Rational(1, 2)*M([[1, 1], [1, -1]]))
check("ex6 coordonnees de (3,1)", P6.inv()*M([3, 1]) == M([2, 1]))
check("ex6 reconstruction", 2*M([1, 1]) + 1*M([1, -1]) == M([3, 1]))
# --- Exercice 7 : projecteur dans la bonne base ------------------------
Pr = sp.Rational(1, 2)*M([[1, 1], [1, 1]])
check("ex7 diagonalise", P6.inv()*Pr*P6 == sp.diag(1, 0))
# --- Exercice 8 : trace ------------------------------------------------
check("ex8 tr(AB) = tr(BA)", (A2*B2).trace() == (B2*A2).trace() == 5)
check("ex8 trace non multiplicative", (A2*B2).trace() != A2.trace()*B2.trace())
check("ex8 trace projecteur = rang", Pr.trace() == 1 == Pr.rank())
# --- Exercice 9 : puissances par changement de base --------------------
A9 = M([[1, 2], [2, 1]])
check("ex9 diagonalisation", P6.inv()*A9*P6 == sp.diag(3, -1))
for n in [1, 2, 5, 8]:
    An = sp.Rational(1, 2)*M([[3**n + (-1)**n, 3**n - (-1)**n],
                              [3**n - (-1)**n, 3**n + (-1)**n]])
    check(f"ex9 A^{n}", A9**n == An)
# --- Exercice 10 : rang avec paramètre ---------------------------------
t = sp.symbols("t")
M10 = M([[1, 1, t], [1, t, 1], [t, 1, 1]])
check("ex10 det", sp.factor(M10.det()) == -(t - 1)**2*(t + 2))
check("ex10 rangs", M10.subs(t, 0).rank() == 3 and M10.subs(t, 1).rank() == 1
      and M10.subs(t, -2).rank() == 2)
# --- Exercice 11 : équivalence et J_r ----------------------------------
A11 = M([[1, 2, 3], [2, 4, 6]])
check("ex11 rang 1", A11.rank() == 1)
Q11 = M([[1, 0], [-2, 1]])
P11 = M([[1, -2, -3], [0, 1, 0], [0, 0, 1]])
check("ex11 QAP = J1", Q11*A11*P11 == M([[1, 0, 0], [0, 0, 0]]))
check("ex11 rang transposee", A11.T.rank() == 1)
# --- Exercice 12 : Cramer ----------------------------------------------
A12 = M([[2, 1], [1, 3]])
check("ex12 det 5", A12.det() == 5)
check("ex12 formules de Cramer",
      M([[5, 1], [5, 3]]).det()/5 == 2 and M([[2, 5], [1, 5]]).det()/5 == 1)
check("ex12 solution", A12*M([2, 1]) == M([5, 5]))
# --- Exercice 13 : C comme plan réel -----------------------------------
a, b = sp.symbols("a b", real=True)
J13 = M([[0, -1], [1, 0]])
check("ex13 J^2 = -I", J13*J13 == -sp.eye(2))
C13 = a*sp.eye(2) + b*J13
check("ex13 forme", C13 == M([[a, -b], [b, a]]))
check("ex13 det = module carre", sp.expand(C13.det()) == a**2 + b**2)
th = sp.symbols("theta", real=True)
R13 = M([[sp.cos(th), -sp.sin(th)], [sp.sin(th), sp.cos(th)]])
check("ex13 rotation", sp.simplify(R13.det()) == 1)
# --- Exercice 14 : semblables ou pas -----------------------------------
N14, N14b = M([[0, 1], [0, 0]]), M([[0, 0], [1, 0]])
S14 = M([[0, 1], [1, 0]])
check("ex14 N et N' semblables", S14.inv()*N14*S14 == N14b)
check("ex14 I seule dans sa classe", S14.inv()*sp.eye(2)*S14 == sp.eye(2))
check("ex14 traces distinctes", sp.diag(1, 0).trace() != sp.eye(2).trace())
check("ex14 meme trace, pas semblables", N14.trace() == 0 and N14 != sp.zeros(2))
# --- Exercice 15 : la dérivation et la base de Taylor ------------------
D15 = M([[0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 3], [0, 0, 0, 0]])
check("ex15 rang 3", D15.rank() == 3)
P15 = M([[comb(j, i)*(-1)**(j - i) if j >= i else 0 for j in range(4)]
         for i in range(4)])  # coordonnées de (X-1)^j dans (X^i)
check("ex15 meme matrice dans la base de Taylor", P15.inv()*D15*P15 == D15)
# --- Exercice 16 : trace, invariants -----------------------------------
X16 = M(2, 2, sp.symbols("x0:4"))
Y16 = M(2, 2, sp.symbols("y0:4"))
check("ex16 tr(AB) = tr(BA) symbolique",
      sp.expand((X16*Y16).trace() - (Y16*X16).trace()) == 0)
P16 = M([[2, 1], [1, 1]])
check("ex16 invariance similitude", (P16.inv()*A2*P16).trace() == A2.trace())
check("ex16 tr(A+I) = tr A + n", (A2 + sp.eye(2)).trace() == A2.trace() + 2)
# --- Exercice 17 : matrices extraites ----------------------------------
A17 = M([[1, 2, 3, 4], [2, 4, 6, 8], [1, 1, 1, 1]])
check("ex17 rang 2", A17.rank() == 2)
check("ex17 extraite inversible", M([[1, 2], [1, 1]]).det() != 0)
minors3 = [A17[:, cols].det() for cols in
           [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]]
check("ex17 tous les mineurs 3x3 nuls", all(m == 0 for m in minors3))
# --- Exercice 18 : rang 1 ----------------------------------------------
U18, V18 = M([1, 2, 3]), M([2, 1, 1])
A18 = U18*V18.T
check("ex18 rang 1", A18.rank() == 1)
check("ex18 A^2 = tr(A) A", A18*A18 == A18.trace()*A18 and A18.trace() == 7)
# --- Exercice 19 : commutant d'une diagonale ---------------------------
D19 = sp.diag(1, 2, 3)
M19 = M(3, 3, sp.symbols("m0:9"))
eqs = (M19*D19 - D19*M19).values()
sol = sp.solve(eqs, M19.free_symbols, dict=True)[0]
offdiag = [M19[i, j] for i in range(3) for j in range(3) if i != j]
check("ex19 commutant = diagonales", all(sol.get(s, s) == 0 for s in offdiag))
# --- Exercice 20 : centre de M_n ---------------------------------------
E11, E12 = M([[1, 0], [0, 0]]), M([[0, 1], [0, 0]])
A20 = M(2, 2, sp.symbols("c0:4"))
eqs20 = list((A20*E11 - E11*A20).values()) + list((A20*E12 - E12*A20).values())
sol20 = sp.solve(eqs20, A20.free_symbols, dict=True)[0]
A20r = A20.subs(sol20)
check("ex20 centre = scalaires",
      A20r[0, 1] == 0 and A20r[1, 0] == 0 and A20r[0, 0] == A20r[1, 1])
# --- Exercice 21 : trigonalisation 2x2 ---------------------------------
A21 = M([[1, 1], [-1, 3]])
check("ex21 (A-2I)^2 = 0", (A21 - 2*sp.eye(2))**2 == sp.zeros(2))
check("ex21 v propre", A21*M([1, 1]) == 2*M([1, 1]))
check("ex21 w", (A21 - 2*sp.eye(2))*M([0, 1]) == M([1, 1]))
P21 = M([[1, 0], [1, 1]])
check("ex21 forme reduite", P21.inv()*A21*P21 == M([[2, 1], [0, 2]]))
for n in [1, 2, 3, 6]:
    An = 2**n*sp.eye(2) + n*2**(n - 1)*(A21 - 2*sp.eye(2))
    check(f"ex21 A^{n}", A21**n == An)
# --- Exercice 22 : tr(A Aᵀ) --------------------------------------------
A22 = M([[1, 2], [3, -1]])
check("ex22 somme des carres", (A22*A22.T).trace() == 1 + 4 + 9 + 1)
B22 = M([[0, 1], [1, 2]])
lhs = (A22*B22.T).trace()**2
rhs = (A22*A22.T).trace()*(B22*B22.T).trace()
check("ex22 Cauchy-Schwarz", lhs <= rhs)
# --- Exercice 23 : rang de la transposée -------------------------------
for Mat in [A4, A17, A11]:
    check(f"ex23 rg A = rg At ({Mat.shape})", Mat.rank() == Mat.T.rank())
# --- Exercice 24 : Fibonacci matriciel ---------------------------------
F24 = M([[1, 1], [1, 0]])
Fib = [0, 1]
for _ in range(20):
    Fib.append(Fib[-1] + Fib[-2])
for n in [1, 2, 7, 15]:
    check(f"ex24 F^{n}", F24**n == M([[Fib[n + 1], Fib[n]], [Fib[n], Fib[n - 1]]]))
    check(f"ex24 Cassini n={n}",
          Fib[n + 1]*Fib[n - 1] - Fib[n]**2 == (-1)**n)
phi = (1 + sqrt(5))/2
check("ex24 valeurs propres", all(
    isclose(r, v, abs_tol=1e-9) for r, v in
    zip(sorted(float(x) for x in F24.eigenvals()), sorted([1 - phi, phi]))))

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
