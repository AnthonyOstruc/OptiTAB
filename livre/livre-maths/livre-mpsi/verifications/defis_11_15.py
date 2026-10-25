# -*- coding: utf-8 -*-
"""Vérifications des défis des chapitres 11 à 15."""
import math
from fractions import Fraction as Fr
from math import isclose, exp, log, sqrt, pi, comb, factorial

import sympy as sp

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

# =====================================================================
# Défi 11 — La fonction W de Lambert
# =====================================================================
y = sp.symbols("y")
def W(v):
    # Newton sur x e^x = v, branche principale (v >= -1/e)
    x = log(1 + v) if v > -0.3 else -0.5
    for _ in range(200):
        x -= (x*exp(x) - v)/((1 + x)*exp(x))
    return x
check("d11 W(0) = 0, W(e) = 1", abs(W(0.0)) < 1e-15 and isclose(W(math.e), 1))
check("d11 W(-1/e) = -1", isclose(W(-1/math.e + 1e-12), -1, abs_tol=1e-5))
dl = sp.series(sp.LambertW(y), y, 0, 5).removeO()
check("d11 DL ordre 4", sp.expand(dl - (y - y**2 + sp.Rational(3, 2)*y**3
      - sp.Rational(8, 3)*y**4)) == 0)
check("d11 coefficients (-n)^(n-1)/n!", all(
    sp.series(sp.LambertW(y), y, 0, 8).removeO().coeff(y, n)
    == sp.Rational((-n)**(n - 1), factorial(n)) for n in range(1, 8)))
check("d11 W(0,01)", isclose(W(0.01), 0.01 - 0.0001 + 1.5e-6, abs_tol=3e-8))
# dérivée W' = W/(y(1+W))
for v in [0.5, 2.0, 10.0]:
    h_ = 1e-6
    deriv = (W(v + h_) - W(v - h_))/(2*h_)
    check(f"d11 W'({v})", isclose(deriv, W(v)/(v*(1 + W(v))), rel_tol=1e-6))
# asymptotique
for v in [1e10, 1e30, 1e100]:
    L1, L2 = log(v), log(log(v))
    check(f"d11 W ~ ln y ({v:g})", isclose(W(v)/L1, 1, rel_tol=0.25))
    err = W(v) - (L1 - L2 + L2/L1)
    check(f"d11 developpement a 3 termes ({v:g})", abs(err) < 1.5*(L2/L1)**2 + 0.05)
check("d11 W(y) - (ln y - ln ln y) -> 0",
      abs(W(1e300) - (log(1e300) - log(log(1e300)))) < 0.1)
# x^x = y : x = ln y / W(ln y)
for v in [1e6, 1e20]:
    xs = log(v)/W(log(v))
    check(f"d11 x^x = y ({v:g})", isclose(xs*log(xs), log(v), rel_tol=1e-10))
check("d11 point (-1/e, -1)", isclose((-1)*exp(-1), -1/math.e))
L20 = log(1e20)
check("d11 y = 1e20 : W(ln y) ~ 2,800 et x ~ 16,45",
      isclose(W(L20), 2.800, abs_tol=1e-3) and isclose(L20/W(L20), 16.45, abs_tol=5e-3)
      and isclose(L20/log(L20), 12.0, abs_tol=0.05))

# =====================================================================
# Défi 12 — L'opérateur de différence et la base binomiale
# =====================================================================
X = sp.symbols("X")
def Delta(P):
    return sp.expand(P.subs(X, X + 1) - P)
def H(k):
    return sp.expand(sp.prod([X - i for i in range(k)])/sp.factorial(k)) if k else sp.Integer(1)
check("d12 Delta H_k = H_{k-1}", all(sp.expand(Delta(H(k)) - H(k - 1)) == 0
      for k in range(1, 8)))
check("d12 Delta^4 nul sur R3[X]", all(sp.expand(
    Delta(Delta(Delta(Delta(X**d))))) == 0 for d in range(4)))
check("d12 deg Delta P = deg P - 1", sp.degree(Delta(X**5), X) == 4
      and sp.Poly(Delta(X**5), X).LC() == 5)
# Newton : P = sum Delta^k P(0) H_k
for P in [X**3, X**4 - 2*X + 7, X*(X + 1)/2]:
    coeffs = []
    Q = P
    for k in range(6):
        coeffs.append(Q.subs(X, 0))
        Q = Delta(Q)
    check(f"d12 formule de Newton pour {P}",
          sp.expand(sum(c*H(k) for k, c in enumerate(coeffs)) - P) == 0)
check("d12 X^2 = 2H_2 + H_1", sp.expand(2*H(2) + H(1) - X**2) == 0)
Q = 2*H(3) + H(2)
check("d12 Delta Q = X^2", sp.expand(Delta(Q) - X**2) == 0)
n = sp.symbols("n", integer=True, positive=True)
check("d12 somme des carres", sp.simplify(Q.subs(X, n) - Q.subs(X, 0)
      - (n - 1)*n*(2*n - 1)/6) == 0)
check("d12 X^3 en base H", sp.expand(6*H(3) + 6*H(2) + H(1) - X**3) == 0)
# table des différences de X^3
vals = [k**3 for k in range(6)]
d1 = [vals[i + 1] - vals[i] for i in range(5)]
d2 = [d1[i + 1] - d1[i] for i in range(4)]
d3 = [d2[i + 1] - d2[i] for i in range(3)]
check("d12 table", d1 == [1, 7, 19, 37, 61] and d2 == [6, 12, 18, 24] and d3 == [6, 6, 6])
# polynômes à valeurs entières : H_k(m) entier pour m entier relatif
check("d12 H_k(m) entiers", all(H(k).subs(X, m).is_integer
      for k in range(6) for m in range(-6, 7)))
check("d12 X(X+1)/2 non a coefficients entiers mais a valeurs entieres",
      all((m*(m + 1)//2)*2 == m*(m + 1) for m in range(-10, 11)))
# matrice de Delta dans la base canonique de R3[X]
M = sp.Matrix([[sp.Poly(Delta(X**j), X).coeff_monomial(X**i) for j in range(4)]
               for i in range(4)])
check("d12 matrice de Delta", M == sp.Matrix([[0, 1, 1, 1], [0, 0, 2, 3],
      [0, 0, 0, 3], [0, 0, 0, 0]]))
check("d12 rang 3", M.rank() == 3 and (M**4).is_zero_matrix and not (M**3).is_zero_matrix)

# =====================================================================
# Défi 13 — Les matrices 2x2 à similitude près
# =====================================================================
a, b, c, d = sp.symbols("a b c d")
A = sp.Matrix([[a, b], [c, d]])
check("d13 Cayley-Hamilton 2x2", sp.expand(A*A - A.trace()*A + A.det()*sp.eye(2))
      == sp.zeros(2))
def compagnon(t, dt):
    return sp.Matrix([[0, -dt], [1, t]])
for Am in [sp.Matrix([[1, 1], [0, 1]]), sp.Matrix([[2, 1], [-1, 0]]),
           sp.Matrix([[0, -1], [1, 0]]), sp.Matrix([[1, -2], [1, -1]]),
           sp.Matrix([[3, 2], [1, 4]])]:
    x0 = sp.Matrix([1, 0])
    if (Am*x0).equals(Am[0, 0]*x0):
        x0 = sp.Matrix([0, 1])
    P = x0.row_join(Am*x0)
    check(f"d13 base (x, Ax) pour {Am.tolist()}", P.det() != 0)
    check(f"d13 forme compagnon {Am.tolist()}",
          P.inv()*Am*P == compagnon(Am.trace(), Am.det()))
T1, T2 = sp.Matrix([[1, 1], [0, 1]]), sp.Matrix([[1, 0], [1, 1]])
check("d13 T1 et T2 memes trace et det", T1.trace() == T2.trace() and T1.det() == T2.det())
check("d13 [[2,1],[-1,0]] semblable a T1", sp.Matrix([[2, 1], [-1, 0]]).trace() == 2
      and sp.Matrix([[2, 1], [-1, 0]]).det() == 1)
R, S = sp.Matrix([[0, -1], [1, 0]]), sp.Matrix([[1, -2], [1, -1]])
check("d13 R et S trace 0 det 1", R.trace() == S.trace() == 0 and R.det() == S.det() == 1)
P_RS = sp.Matrix([[1, 1], [0, 1]])  # passage explicite
Pr = sp.Matrix([1, 0]).row_join(R*sp.Matrix([1, 0]))
Ps = sp.Matrix([1, 0]).row_join(S*sp.Matrix([1, 0]))
Q = Ps*Pr.inv()
check("d13 Q^-1 S Q = R", Q.inv()*S*Q == R)
check("d13 Q explicite", Q == sp.Matrix([[1, 1], [0, 1]]))
# puissances quand tr = 2, det = 1
B = sp.Matrix([[2, 1], [-1, 0]])
check("d13 (B-I)^2 = 0", (B - sp.eye(2))**2 == sp.zeros(2))
check("d13 B^n = I + n(B-I)", all(B**k == sp.eye(2) + k*(B - sp.eye(2)) for k in range(8)))
# suites u_{n+2} = 2u_{n+1} - u_n : arithmétiques
u = [3, 5]
for _ in range(10):
    u.append(2*u[-1] - u[-2])
check("d13 suite arithmetique", all(u[k] == 3 + 2*k for k in range(12)))
# scalaire : seule dans sa classe
check("d13 lI seule dans sa classe", sp.Matrix([[1, 2], [3, 4]]).inv()*(5*sp.eye(2))
      *sp.Matrix([[1, 2], [3, 4]]) == 5*sp.eye(2))

# =====================================================================
# Défi 14 — Déterminant de Cauchy et matrices de Hilbert
# =====================================================================
def cauchy_formule(av, bv):
    n_ = len(av)
    num = sp.prod([(av[j] - av[i])*(bv[j] - bv[i]) for i in range(n_) for j in range(i + 1, n_)])
    den = sp.prod([av[i] + bv[j] for i in range(n_) for j in range(n_)])
    return num/den
for n_ in range(1, 3):
    av = sp.symbols(f"a1:{n_ + 1}")
    bv = sp.symbols(f"b1:{n_ + 1}")
    Cm = sp.Matrix(n_, n_, lambda i, j: 1/(av[i] + bv[j]))
    check(f"d14 formule de Cauchy symbolique n={n_}",
          sp.simplify(Cm.det() - cauchy_formule(av, bv)) == 0)
import random
random.seed(14)
for essai in range(40):
    n_ = random.randint(3, 6)
    av = [sp.Rational(random.randint(1, 60), random.randint(1, 9)) for _ in range(n_)]
    bv = [sp.Rational(random.randint(1, 60), random.randint(1, 9)) for _ in range(n_)]
    Cm = sp.Matrix(n_, n_, lambda i, j: 1/(av[i] + bv[j]))
    check(f"d14 formule de Cauchy exacte (essai {essai}, n={n_})",
          Cm.det() == cauchy_formule(av, bv))
# relation de récurrence C_n / C_{n-1}
av = [sp.Rational(k*k + 1, 3) for k in range(1, 6)]
bv = [sp.Rational(2*k + 5, 7) for k in range(1, 6)]
def Cdet(n_):
    return sp.Matrix(n_, n_, lambda i, j: 1/(av[i] + bv[j])).det()
for n_ in range(2, 6):
    fac = sp.prod([(av[n_ - 1] - av[k])*(bv[n_ - 1] - bv[k]) for k in range(n_ - 1)]) / (
        sp.prod([av[k] + bv[n_ - 1] for k in range(n_)])*sp.prod([av[n_ - 1] + bv[k] for k in range(n_ - 1)]))
    check(f"d14 recurrence n={n_}", Cdet(n_) == fac*Cdet(n_ - 1))
def hilbert(n_):
    return sp.Matrix(n_, n_, lambda i, j: sp.Rational(1, i + j + 1))
dets = {n_: hilbert(n_).det() for n_ in range(1, 9)}
check("d14 det H2, H3, H4", dets[2] == sp.Rational(1, 12) and dets[3] == sp.Rational(1, 2160)
      and dets[4] == sp.Rational(1, 6048000))
def sf(n_):
    return math.prod(factorial(k) for k in range(1, n_))
check("d14 det H_n = c_n^4 / c_2n", all(dets[n_] == sp.Rational(sf(n_)**4, sf(2*n_))
      for n_ in range(1, 9)))
logs = [float(sp.log(dets[n_], 10)) for n_ in range(1, 9)]
check("d14 log10 det", [round(v, 2) for v in logs] == [0.0, -1.08, -3.33, -6.78,
      -11.43, -17.27, -24.32, -32.56])
check("d14 H3^-1 entiere", hilbert(3).inv() == sp.Matrix([[9, -36, 30], [-36, 192, -180],
      [30, -180, 180]]))
check("d14 H4^-1 entiere", all(v.is_integer for v in hilbert(4).inv()))
xs = sp.symbols("xs")
check("d14 H_n matrice de Gram", all(sp.integrate(xs**i*xs**j, (xs, 0, 1)) == hilbert(4)[i, j]
      for i in range(4) for j in range(4)))
# instabilité numérique : H_8 x = b
import numpy as np
H8 = np.array([[1/(i + j + 1) for j in range(8)] for i in range(8)])
x_exact = np.ones(8)
bvec = H8 @ x_exact
x_pert = np.linalg.solve(H8, bvec + 1e-8*np.array([1, -1]*4))
check("d14 instabilite", np.max(np.abs(x_pert - x_exact)) > 0.1)

# =====================================================================
# Défi 15 — L'intégrale de Gauss
# =====================================================================
check("d15 1+u <= e^u", all(1 + u_ <= exp(u_) for u_ in [-0.99, -0.5, 0, 0.3, 2]))
for nn in [1, 3, 10]:
    check(f"d15 encadrement n={nn}", all(
        (1 - t*t/nn)**nn <= exp(-t*t) + 1e-15 <= (1 + t*t/nn)**(-nn) + 2e-15
        for t in [i*sqrt(nn)/50 for i in range(51)]))
def wallis(k):
    w = [pi/2, 1.0]
    for j in range(2, k + 1):
        w.append((j - 1)/j*w[j - 2])
    return w[k]
import mpmath
mpmath.mp.dps = 30
for nn in [5, 20, 80]:
    I1 = float(mpmath.quad(lambda t: (1 - t*t/nn)**nn, [0, mpmath.sqrt(nn)]))
    check(f"d15 sqrt(n) W_(2n+1) (n={nn})", isclose(I1, sqrt(nn)*wallis(2*nn + 1), rel_tol=1e-10))
    I2 = float(mpmath.quad(lambda t: (1 + t*t/nn)**(-nn), [0, mpmath.sqrt(nn)]))
    check(f"d15 majoration par sqrt(n) W_(2n-2) (n={nn})", I2 <= sqrt(nn)*wallis(2*nn - 2))
    F = float(mpmath.quad(lambda t: mpmath.e**(-t*t), [0, mpmath.sqrt(nn)]))
    check(f"d15 encadrement de F(sqrt n) (n={nn})",
          sqrt(nn)*wallis(2*nn + 1) <= F <= sqrt(nn)*wallis(2*nn - 2))
check("d15 limites -> sqrt(pi)/2", isclose(sqrt(2000)*wallis(4001), sqrt(pi)/2, rel_tol=1e-3)
      and isclose(sqrt(2000)*wallis(3998), sqrt(pi)/2, rel_tol=1e-3))
G = float(mpmath.quad(lambda t: mpmath.e**(-t*t), [0, mpmath.inf]))
check("d15 valeur", isclose(G, sqrt(pi)/2, rel_tol=1e-12))
check("d15 F(1) <= 1 + 1/e", float(mpmath.quad(lambda t: mpmath.e**(-t*t), [0, 1])) <= 1)
check("d15 e^(-t^2) <= e^(-t) pour t >= 1", all(exp(-t*t) <= exp(-t) for t in [1, 1.5, 3]))
aa = 3.0
check("d15 changement de variable", isclose(float(mpmath.quad(lambda t: mpmath.e**(-aa*t*t),
      [0, mpmath.inf])), sqrt(pi)/(2*sqrt(aa)), rel_tol=1e-12))
check("d15 loi normale", isclose(float(mpmath.quad(lambda t: mpmath.e**(-t*t/2),
      [-mpmath.inf, mpmath.inf]))/sqrt(2*pi), 1, rel_tol=1e-12))
check("d15 P(|N|<=1.96) ~ 0.95", isclose(float(mpmath.quad(lambda t: mpmath.e**(-t*t/2),
      [-1.96, 1.96]))/sqrt(2*pi), 0.95, abs_tol=1e-3))

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
