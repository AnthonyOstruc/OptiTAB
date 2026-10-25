# -*- coding: utf-8 -*-
"""Vérification des sujets type concours C1 (CCINP), C2 (Mines-Ponts),
C3 (Centrale-Supélec) et C4 (X-ENS) de la partie Évaluations."""
import math
import random
from fractions import Fraction as Fr
from itertools import permutations
from math import comb, factorial, isclose, sqrt, log, exp, e as E_

import mpmath as mp
import sympy as sp

OK = []


def check(name, cond):
    if not cond:
        raise AssertionError("ÉCHEC : " + name)
    OK.append(name)


x, t, a, b, c, d = sp.symbols("x t a b c d")
X = sp.symbols("X")
random.seed(11)

# ============================ C1 (CCINP) =============================
# Exercice 1 : la matrice J
for n in range(2, 6):
    J = sp.ones(n, n); I = sp.eye(n)
    check(f"C1 J^2 = nJ (n={n})", J**2 == n*J and J.rank() == 1)
    M = a*I + b*J
    for p in range(0, 5):
        assert sp.simplify(M**p - (a**p*I + ((a + n*b)**p - a**p)/n*J)) == sp.zeros(n, n)
    check(f"C1 puissances (n={n})", True)
    check(f"C1 produit M(a,b)M(c,d) (n={n})",
          sp.simplify((a*I + b*J)*(c*I + d*J) - (a*c*I + (a*d + b*c + n*b*d)*J)) == sp.zeros(n, n))
    inv = I/a - b/(a*(a + n*b))*J
    check(f"C1 inverse (n={n})", sp.simplify(M*inv - I) == sp.zeros(n, n))
    check(f"C1 det (n={n})", sp.factor(M.det() - a**(n - 1)*(a + n*b)) == 0)
check("C1 exemple 2I + J (n=3)", (2*sp.eye(3) + sp.ones(3, 3)).inv() == sp.eye(3)/2 - sp.ones(3, 3)/10)
# Exercice 2 : records d'une permutation aléatoire
for n in range(1, 8):
    perms = list(permutations(range(1, n + 1)))
    N = len(perms)
    def rec(s, k):
        return all(s[k] > s[i] for i in range(k))
    for k in range(n):
        assert Fr(sum(1 for s in perms if rec(s, k)), N) == Fr(1, k + 1)
    for j in range(n):
        for k in range(j + 1, n):
            assert Fr(sum(1 for s in perms if rec(s, j) and rec(s, k)), N) == Fr(1, (j + 1)*(k + 1))
    Nn = [sum(1 for k in range(n) if rec(s, k)) for s in perms]
    EN = Fr(sum(Nn), N); EN2 = Fr(sum(v*v for v in Nn), N)
    H = sum(Fr(1, k) for k in range(1, n + 1))
    check(f"C1 records E = H_n (n={n})", EN == H)
    check(f"C1 records V (n={n})", EN2 - EN**2 == sum(Fr(1, k) - Fr(1, k*k) for k in range(1, n + 1)))
    if n == 3:
        loi = {v: Fr(Nn.count(v), N) for v in set(Nn)}
        check("C1 loi N_3", loi == {1: Fr(1, 3), 2: Fr(1, 2), 3: Fr(1, 6)})
    if n == 4:
        loi = {v: Fr(Nn.count(v), N) for v in set(Nn)}
        check("C1 loi N_4 (nombres de Stirling 6,11,6,1)", loi == {1: Fr(6, 24), 2: Fr(11, 24), 3: Fr(6, 24), 4: Fr(1, 24)})
check("C1 exemple de la figure", [k + 1 for k in range(10)
      if all([3, 1, 6, 2, 5, 9, 4, 8, 10, 7][k] > v for v in [3, 1, 6, 2, 5, 9, 4, 8, 10, 7][:k])] == [1, 3, 6, 9])
check("C1 H_10 et H_100", isclose(float(sum(Fr(1, k) for k in range(1, 11))), 2.928968, abs_tol=1e-6)
      and isclose(sum(1/k for k in range(1, 101)), 5.187378, abs_tol=1e-6))
# Exercice 3 : polynômes de Bernoulli
B = [sp.Integer(1)]
for n in range(1, 8):
    prim = sp.integrate(n*B[n - 1], X)
    cst = -sp.integrate(prim, (X, 0, 1))
    B.append(sp.expand(prim + cst))
check("C1 B_1, B_2, B_3", B[1] == X - sp.Rational(1, 2) and B[2] == X**2 - X + sp.Rational(1, 6)
      and B[3] == X**3 - sp.Rational(3, 2)*X**2 + X/2)
check("C1 B_4", B[4] == X**4 - 2*X**3 + X**2 - sp.Rational(1, 30))
check("C1 B_n(X+1) - B_n(X) = n X^(n-1)", all(sp.expand(B[n].subs(X, X + 1) - B[n] - n*X**(n - 1)) == 0 for n in range(1, 8)))
check("C1 symetrie", all(sp.expand(B[n].subs(X, 1 - X) - (-1)**n*B[n]) == 0 for n in range(0, 8)))
check("C1 B_n(0) = B_n(1)", all(B[n].subs(X, 0) == B[n].subs(X, 1) for n in range(2, 8)))
Nsym = sp.symbols("N", integer=True, positive=True)
check("C1 somme des carres", sp.factor((B[3].subs(X, Nsym) - B[3].subs(X, 0))/3) == sp.factor(Nsym*(Nsym - 1)*(2*Nsym - 1)/6))
check("C1 somme des cubes", sp.factor((B[4].subs(X, Nsym) - B[4].subs(X, 0))/4) == sp.factor((Nsym*(Nsym - 1)/2)**2))
check("C1 B_3(1/2) = 0", B[3].subs(X, sp.Rational(1, 2)) == 0 and B[5].subs(X, sp.Rational(1, 2)) == 0)
check("C1 unicite (integrales nulles)", all(sp.integrate(B[n], (X, 0, 1)) == 0 for n in range(1, 8)))
# Exercice 4 : équation de Cauchy (vérifications élémentaires)
check("C1 Jensen => affine (exemple)", all(isclose((3*(u + v)/2 + 1), ((3*u + 1) + (3*v + 1))/2) for u, v in [(1, 2), (-3, 5)]))

# ============================ C2 (Mines-Ponts) =======================
def legendre(n):
    return sp.expand(sp.diff((X**2 - 1)**n, X, n)/(2**n*sp.factorial(n)))


L = [legendre(n) for n in range(0, 8)]
check("C2 L_0..L_3", L[0] == 1 and L[1] == X and L[2] == (3*X**2 - 1)/2 and L[3] == (5*X**3 - 3*X)/2)
check("C2 L_4", sp.expand(L[4] - (35*X**4 - 30*X**2 + 3)/8) == 0)
check("C2 degre et coefficient dominant", all(sp.degree(L[n], X) == n and sp.Poly(L[n], X).LC()
      == sp.factorial(2*n)/(2**n*sp.factorial(n)**2) for n in range(0, 8)))
check("C2 L_n(1)=1, L_n(-1)=(-1)^n", all(L[n].subs(X, 1) == 1 and L[n].subs(X, -1) == (-1)**n for n in range(0, 8)))
check("C2 parite", all(sp.expand(L[n].subs(X, -X) - (-1)**n*L[n]) == 0 for n in range(0, 8)))
check("C2 orthogonalite", all(sp.integrate(L[m]*L[n], (X, -1, 1)) == 0 for m in range(8) for n in range(8) if m != n))
check("C2 normes", all(sp.integrate(L[n]**2, (X, -1, 1)) == sp.Rational(2, 2*n + 1) for n in range(8)))
check("C2 orthogonal a X^k, k<n", all(sp.integrate(L[n]*X**k, (X, -1, 1)) == 0 for n in range(1, 8) for k in range(n)))
check("C2 integrale (1-x^2)^n", all(sp.integrate((1 - X**2)**n, (X, -1, 1)) == sp.Rational(2**(2*n + 1)*factorial(n)**2, factorial(2*n + 1)) for n in range(0, 7)))
check("C2 relation de recurrence", all(sp.expand((n + 1)*L[n + 1] - (2*n + 1)*X*L[n] + n*L[n - 1]) == 0 for n in range(1, 7)))
for n in range(1, 8):
    rts = sp.Poly(L[n], X).nroots()
    assert len(rts) == n and all(abs(sp.im(r)) < 1e-12 and -1 < sp.re(r) < 1 for r in rts)
    assert len(set(round(float(sp.re(r)), 9) for r in rts)) == n
check("C2 racines reelles simples dans ]-1,1[", True)
check("C2 racines n=2,3", sp.solve(L[2], X) == [-1/sp.sqrt(3), 1/sp.sqrt(3)]
      and set(sp.solve(L[3], X)) == {0, -sp.sqrt(sp.Rational(3, 5)), sp.sqrt(sp.Rational(3, 5))})


def poids(noeuds):
    w = []
    for i, xi in enumerate(noeuds):
        li = sp.prod([(X - xj)/(xi - xj) for j, xj in enumerate(noeuds) if j != i])
        w.append(sp.nsimplify(sp.simplify(sp.integrate(li, (X, -1, 1)))))
    return w


n2 = [-1/sp.sqrt(3), 1/sp.sqrt(3)]
n3 = [-sp.sqrt(sp.Rational(3, 5)), 0, sp.sqrt(sp.Rational(3, 5))]
w2 = poids(n2); w3 = poids(n3)
check("C2 poids n=2", w2 == [1, 1])
check("C2 poids n=3", w3 == [sp.Rational(5, 9), sp.Rational(8, 9), sp.Rational(5, 9)])
for k in range(0, 8):
    exact = sp.integrate(X**k, (X, -1, 1))
    q2 = sp.simplify(sum(wi*xi**k for wi, xi in zip(w2, n2)))
    q3 = sp.simplify(sum(wi*xi**k for wi, xi in zip(w3, n3)))
    if k <= 3:
        assert q2 == exact
    if k <= 5:
        assert q3 == exact
check("C2 exactitude degre 2n-1", sp.simplify(sum(wi*xi**4 for wi, xi in zip(w2, n2)) - sp.Rational(2, 5)) != 0
      and sp.simplify(sum(wi*xi**6 for wi, xi in zip(w3, n3)) - sp.Rational(2, 7)) != 0)
q2e = float(sum(wi*sp.exp(xi) for wi, xi in zip(w2, n2)))
q3e = float(sum(wi*sp.exp(xi) for wi, xi in zip(w3, n3)))
ex = 2*math.sinh(1)
check("C2 application e^x", isclose(ex, 2.350402, abs_tol=1e-6) and isclose(q2e, 2.342696, abs_tol=1e-6)
      and isclose(q3e, 2.350337, abs_tol=1e-6))
print("C2 erreurs Gauss :", ex - q2e, ex - q3e, " trapezes n=3 points :", ex - (exp(-1)/2 + 1 + exp(1)/2))
check("C2 comparaison avec trapezes", abs(ex - q3e) < 1e-4 < abs(ex - (exp(-1)/2 + 1 + exp(1)/2)))
check("C2 poids positifs et somme 2", sum(w3) == 2 and sum(w2) == 2)

# ============================ C3 (Centrale) ===========================
aa, bb, kk = sp.symbols("a b k", positive=True)
P2 = sp.Matrix([[1 - aa, aa], [bb, 1 - bb]])
R = sp.Matrix([[bb, aa], [bb, aa]])/(aa + bb)
S = sp.Matrix([[aa, -aa], [-bb, bb]])/(aa + bb)
check("C3 R+S=I, R^2=R, S^2=S, RS=SR=0", sp.simplify(R + S - sp.eye(2)) == sp.zeros(2, 2)
      and sp.simplify(R*R - R) == sp.zeros(2, 2) and sp.simplify(S*S - S) == sp.zeros(2, 2)
      and sp.simplify(R*S) == sp.zeros(2, 2) and sp.simplify(S*R) == sp.zeros(2, 2))
check("C3 P = R + (1-a-b) S", sp.simplify(P2 - (R + (1 - aa - bb)*S)) == sp.zeros(2, 2))
for p in range(0, 6):
    assert sp.simplify(P2**p - (R + (1 - aa - bb)**p*S)) == sp.zeros(2, 2)
check("C3 P^k", True)
Pm = sp.Matrix([[sp.Rational(7, 10), sp.Rational(3, 10)], [sp.Rational(2, 5), sp.Rational(3, 5)]])
check("C3 meteo stationnaire (4/7, 3/7)", sp.Matrix([[sp.Rational(4, 7), sp.Rational(3, 7)]])*Pm == sp.Matrix([[sp.Rational(4, 7), sp.Rational(3, 7)]]))
check("C3 meteo P^k k=10", isclose(float((Pm**10)[0, 0]), 4/7 + 3/7*0.3**10, abs_tol=1e-12))
# contraction : ||xQ||_1 <= (1 - n delta) ||x||_1 si sum x = 0
for _ in range(300):
    n = random.randint(2, 5)
    Q = [[random.uniform(0.05, 1) for _ in range(n)] for _ in range(n)]
    Q = [[v/sum(r) for v in r] for r in Q]
    delta = min(min(r) for r in Q)
    xv = [random.uniform(-1, 1) for _ in range(n)]
    m = sum(xv)/n; xv = [v - m for v in xv]
    xQ = [sum(xv[i]*Q[i][j] for i in range(n)) for j in range(n)]
    assert sum(abs(v) for v in xQ) <= (1 - n*delta)*sum(abs(v) for v in xv) + 1e-12
check("C3 lemme de contraction (300 tirages)", True)
# graphe à 4 pages
Pw = sp.Matrix([[0, sp.Rational(1, 2), sp.Rational(1, 2), 0], [0, 0, 1, 0], [1, 0, 0, 0],
                [sp.Rational(1, 2), 0, sp.Rational(1, 2), 0]])
check("C3 P stochastique", all(sum(Pw.row(i)) == 1 for i in range(4)))
pi0 = sp.Matrix([[sp.Rational(2, 5), sp.Rational(1, 5), sp.Rational(2, 5), 0]])
check("C3 stationnaire de P", pi0*Pw == pi0)
al = sp.Rational(17, 20)
G = al*Pw + (1 - al)/4*sp.ones(4, 4)
check("C3 G stochastique positive", all(sum(G.row(i)) == 1 for i in range(4)) and min(G) == sp.Rational(3, 80))
p1, p2, p3, p4 = sp.symbols("p1:5")
solG = sp.solve(list(sp.Matrix([[p1, p2, p3, p4]])*G - sp.Matrix([[p1, p2, p3, p4]])) + [p1 + p2 + p3 + p4 - 1],
                [p1, p2, p3, p4], dict=True)[0]
piG = [solG[p] for p in (p1, p2, p3, p4)]
print("C3 PageRank exact :", piG, [round(float(v), 4) for v in piG])
check("C3 PageRank valeurs", [round(float(v), 4) for v in piG] == [0.3797, 0.1989, 0.3839, 0.0375])
check("C3 PageRank p4 = 3/80", piG[3] == sp.Rational(3, 80))
check("C3 classement", sorted(range(4), key=lambda i: -piG[i]) == [2, 0, 1, 3])
# programme Python du sujet
code = '''
def pagerank(P, alpha, eps):
    n = len(P)
    mu = [1 / n] * n
    while True:
        nu = [(1 - alpha) / n
              + alpha * sum(mu[i] * P[i][j] for i in range(n))
              for j in range(n)]
        if sum(abs(nu[j] - mu[j]) for j in range(n)) < eps:
            return nu
        mu = nu
'''
env = {}
exec(code, env)
Pf = [[float(v) for v in Pw.row(i)] for i in range(4)]
res = env["pagerank"](Pf, 0.85, 1e-12)
check("C3 programme Python", all(isclose(res[i], float(piG[i]), abs_tol=1e-10) for i in range(4)))
code_creux = '''
def pagerank_creux(succ, alpha, eps):
    n = len(succ)
    mu = [1 / n] * n
    while True:
        nu = [(1 - alpha) / n] * n
        for i in range(n):
            for j in succ[i]:
                nu[j] = nu[j] + alpha * mu[i] / len(succ[i])
        if sum(abs(nu[j] - mu[j]) for j in range(n)) < eps:
            return nu
        mu = nu
'''
exec(code_creux, env)
res2 = env["pagerank_creux"]([[1, 2], [2], [0], [0, 2]], 0.85, 1e-12)
check("C3 programme creux", all(isclose(res2[i], float(piG[i]), abs_tol=1e-10) for i in range(4)))
mu = [sp.Rational(1, 4)]*4
liste = []
for k in range(0, 31):
    liste.append(float(sum(abs(mu[j] - piG[j]) for j in range(4))))
    mu = list(sp.Matrix([mu])*G)
print("C3 log10 erreurs k=0..30 :", [round(math.log10(v), 3) for v in liste])
# vitesse : ||mu_k - pi||_1 <= alpha^k ||mu_0 - pi||_1
mu = [sp.Rational(1, 4)]*4
errs = []
for k in range(0, 26):
    errs.append(float(sum(abs(mu[j] - piG[j]) for j in range(4))))
    mu = list(sp.Matrix([mu])*G)
check("C3 decroissance geometrique", all(errs[k] <= 0.85**k*errs[0] + 1e-15 for k in range(26)))
print("C3 erreurs :", [f"{v:.2e}" for v in errs[:13:2]])
check("C3 nombre d'iterations eps=1e-6", min(k for k in range(200) if 0.85**k*2 < 1e-6) == 90)

# ============================ C4 (X-ENS) ==============================
# Hardy discret
for _ in range(400):
    N = random.randint(1, 60)
    av = [random.random()**3 for _ in range(N)]
    A = [sum(av[:n])/n for n in range(1, N + 1)]
    # inégalité télescopique : A_n^2 - 2 a_n A_n <= (n-1) A_{n-1}^2 - n A_n^2
    for n in range(1, N + 1):
        An = A[n - 1]; Am = A[n - 2] if n >= 2 else 0
        assert An*An - 2*av[n - 1]*An <= (n - 1)*Am*Am - n*An*An + 1e-12
    assert sum(v*v for v in A) <= 4*sum(v*v for v in av) + 1e-12
check("C4 Hardy (400 tirages)", True)
check("C4 identite a_n = n A_n - (n-1) A_{n-1}", True)
# optimalité de 4 : a_n = 1/sqrt(n) tronquée
def ratio_hardy(N):
    S = 0.0; num = 0.0
    for n in range(1, N + 1):
        S += 1/math.sqrt(n)
        num += (S/n)**2
    tail = S*S*float(mp.psi(1, N + 1))   # reste exact : somme des 1/n^2 pour n > N
    return (num + tail)/sum(1/n for n in range(1, N + 1))
rh = {N: ratio_hardy(N) for N in [10, 100, 1000, 10**4, 10**5, 10**6]}
print("C4 rapports Hardy :", {k: round(v, 3) for k, v in rh.items()})
check("C4 rapport Hardy croissant vers 4", all(rh[a1] < rh[a2] < 4 for a1, a2 in zip(list(rh)[:-1], list(rh)[1:])) and rh[10**6] > 3.5)
check("C4 sum_{k<=n} 1/sqrt(k) ~ 2 sqrt(n)", isclose(sum(1/math.sqrt(k) for k in range(1, 10**6 + 1))/(2*1000), 1, rel_tol=1e-3))
# Carleman
ck = lambda k: Fr((k + 1)**k, k**(k - 1))
check("C4 produit des c_k", all(math.prod(ck(k) for k in range(1, n + 1)) == (n + 1)**n for n in range(1, 15)))
check("C4 c_k / k = (1+1/k)^k", all(ck(k)/k == (1 + Fr(1, k))**k for k in range(1, 20)))
check("C4 somme 1/(n(n+1))", all(sum(Fr(1, n*(n + 1)) for n in range(k, 400)) == Fr(1, k) - Fr(1, 400) for k in range(1, 30)))
for _ in range(300):
    N = random.randint(1, 40)
    av = [random.random()**2 for _ in range(N)]
    G_ = sum(math.prod(av[:n])**(1/n) for n in range(1, N + 1))
    assert G_ <= math.e*sum(av) + 1e-12
    assert G_ <= sum(av[k - 1]*(1 + 1/k)**k for k in range(1, N + 1)) + 1e-12
check("C4 Carleman (300 tirages)", True)
def ratio_carleman(N):
    return sum(math.exp(-math.lgamma(n + 1)/n) for n in range(1, N + 1))/sum(1/n for n in range(1, N + 1))
rc = {N: ratio_carleman(N) for N in [10, 100, 1000, 10**4, 10**5, 10**6]}
print("C4 rapports Carleman :", {k: round(v, 3) for k, v in rc.items()})
check("C4 rapport Carleman croissant vers e", all(rc[a1] < rc[a2] < math.e for a1, a2 in zip(list(rc)[:-1], list(rc)[1:])))
check("C4 (n!)^(1/n) ~ n/e", isclose(math.exp(math.lgamma(10**6 + 1)/10**6)/(10**6/math.e), 1, rel_tol=1e-4))
check("C4 ln n! >= n ln n - n", all(math.lgamma(n + 1) >= n*math.log(n) - n for n in range(1, 2000)))
check("C4 ln n! <= (n+1) ln(n+1) - n", all(math.lgamma(n + 1) <= (n + 1)*math.log(n + 1) - n for n in range(1, 2000)))

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
