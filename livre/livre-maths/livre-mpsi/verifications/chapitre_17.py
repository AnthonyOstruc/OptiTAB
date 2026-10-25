# -*- coding: utf-8 -*-
"""Vérifications du chapitre 17 — Probabilités sur un univers fini."""
import math
from fractions import Fraction as Fr
from itertools import product, permutations
from math import comb, factorial, isclose, sqrt, pi

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

# --- Exercice 1 : modéliser --------------------------------------------
des = [(a, b) for a in range(1, 7) for b in range(1, 7)]
check("ex1 univers 36", len(des) == 36)
check("ex1 somme 7", Fr(sum(1 for a, b in des if a + b == 7), 36) == Fr(1, 6))
pieces = list(product("PF", repeat=3))
check("ex1 deux piles", Fr(sum(1 for t in pieces if t.count("P") == 2), 8) == Fr(3, 8))
# --- Exercice 2 : opérations -------------------------------------------
pA, pB, pAB = Fr(1, 2), Fr(2, 5), Fr(1, 5)
check("ex2 union", pA + pB - pAB == Fr(7, 10))
check("ex2 difference", pA - pAB == Fr(3, 10))
check("ex2 ni A ni B", 1 - Fr(7, 10) == Fr(3, 10))
# --- Exercice 3 : conditionnelles (urne 3R 2B, sans remise) ------------
urne = ["R"]*3 + ["B"]*2
tirages = list(permutations(range(5), 2))
pRR = Fr(sum(1 for i, j in tirages if urne[i] == "R" and urne[j] == "R"),
         len(tirages))
check("ex3 P(RR)", pRR == Fr(3, 10) == Fr(3, 5)*Fr(2, 4))
pR1 = Fr(sum(1 for i, j in tirages if urne[i] == "R"), len(tirages))
check("ex3 P(R2|R1)", pRR/pR1 == Fr(1, 2))
# --- Exercice 4 : probabilités totales ---------------------------------
pR = Fr(1, 2)*Fr(2, 3) + Fr(1, 2)*Fr(1, 3)
check("ex4 totales", pR == Fr(1, 2))
# --- Exercice 5 : Bayes ------------------------------------------------
pM, sens, spec = Fr(1, 100), Fr(95, 100), Fr(90, 100)
pPlus = pM*sens + (1 - pM)*(1 - spec)
pMsachantPlus = pM*sens/pPlus
check("ex5 Bayes", pMsachantPlus == Fr(95, 1085) == Fr(19, 217))
check("ex5 valeur", isclose(float(pMsachantPlus), 0.0876, abs_tol=2e-4))
# --- Exercice 6 : uniforme et Bernoulli --------------------------------
EX = Fr(sum(range(1, 7)), 6)
EX2 = Fr(sum(k*k for k in range(1, 7)), 6)
check("ex6 de : E = 7/2", EX == Fr(7, 2))
check("ex6 de : V = 35/12", EX2 - EX**2 == Fr(35, 12))
p = Fr(1, 3)
check("ex6 Bernoulli", p*(1 - p) == Fr(2, 9))
# --- Exercice 7 : binomiale --------------------------------------------
check("ex7 P(X=2)", comb(5, 2)*Fr(1, 3)**2*Fr(2, 3)**3 == Fr(80, 243))
check("ex7 E et V", 5*Fr(1, 3) == Fr(5, 3) and 5*Fr(1, 3)*Fr(2, 3) == Fr(10, 9))
check("ex7 somme des P", sum(comb(5, k)*Fr(1, 3)**k*Fr(2, 3)**(5 - k)
      for k in range(6)) == 1)
# --- Exercice 8 : espérance --------------------------------------------
check("ex8 transfert E(X^2)", EX2 == Fr(91, 6))
check("ex8 linearite", 2*EX + 3 == 10)
# --- Exercice 9 : indépendance -----------------------------------------
pA9 = Fr(sum(1 for a, b in des if a % 2 == 0), 36)
pB9 = Fr(sum(1 for a, b in des if (a + b) % 2 == 0), 36)
pAB9 = Fr(sum(1 for a, b in des if a % 2 == 0 and (a + b) % 2 == 0), 36)
check("ex9 dés indépendants", pAB9 == pA9*pB9 == Fr(1, 4))
# deux pièces : A, B, C deux à deux indépendants mais pas mutuellement
pcs = list(product((0, 1), repeat=2))
A9 = [t for t in pcs if t[0] == 1]
B9 = [t for t in pcs if t[1] == 1]
C9 = [t for t in pcs if t[0] == t[1]]
def pr(ev):
    return Fr(len(ev), 4)
check("ex9 deux a deux", pr([t for t in A9 if t in B9]) == pr(A9)*pr(B9)
      and pr([t for t in A9 if t in C9]) == pr(A9)*pr(C9)
      and pr([t for t in B9 if t in C9]) == pr(B9)*pr(C9))
inter = [t for t in A9 if t in B9 and t in C9]
check("ex9 pas mutuelle", pr(inter) == Fr(1, 4) != pr(A9)*pr(B9)*pr(C9))
# --- Exercice 10 : loi conjointe ---------------------------------------
# table P(X=i, Y=j), i,j dans {0,1} : 1/4, 1/4 / 1/4, 1/4 independante ;
# et 1/2, 0 / 0, 1/2 : memes marginales, pas independante
margX = [Fr(1, 2), Fr(1, 2)]
check("ex10 marginales identiques", margX[0] + margX[1] == 1)
check("ex10 dependance", Fr(1, 2) != margX[0]*margX[0])
# --- Exercice 11 : min et max de deux dés ------------------------------
U = [min(a, b) for a, b in des]
V = [max(a, b) for a, b in des]
EU = Fr(sum(U), 36)
EV = Fr(sum(V), 36)
check("ex11 P(U>=k)", all(Fr(sum(1 for u in U if u >= k), 36)
      == Fr((7 - k)**2, 36) for k in range(1, 7)))
check("ex11 E(U) = 91/36", EU == Fr(91, 36))
check("ex11 E(V) = 161/36", EV == Fr(161, 36) and EU + EV == 7)
# --- Exercice 12 : variance et covariance ------------------------------
EXY = Fr(sum(a*b for a, b in des), 36)
check("ex12 des independants E(XY)=E(X)E(Y)", EXY == EX*EX)
check("ex12 V(X+Y) = 2V(X)", Fr(sum((a + b)**2 for a, b in des), 36)
      - Fr(sum(a + b for a, b in des), 36)**2 == Fr(35, 6))
EUV = Fr(sum(u*v for u, v in zip(U, V)), 36)
covUV = EUV - EU*EV
check("ex12 UV = XY donc E(UV) = E(X)E(Y)", EUV == EXY == Fr(49, 4))
check("ex12 Cov(U,V) > 0", covUV == Fr(49, 4) - Fr(91, 36)*Fr(161, 36)
      and covUV > 0)
# --- Exercice 13 : binomiale comme somme -------------------------------
n13, p13 = 4, Fr(1, 2)
lois = {}
for t in product((0, 1), repeat=n13):
    s = sum(t)
    lois[s] = lois.get(s, 0) + 1
check("ex13 somme de Bernoulli = binomiale", all(
    Fr(lois[k], 2**n13) == comb(n13, k)*p13**k*(1 - p13)**(n13 - k)
    for k in range(n13 + 1)))
# --- Exercice 14 : indicatrices et décorrélation -----------------------
# X uniforme sur {-1,0,1}, Y = X^2 : Cov = 0, pas indépendantes
vals = [-1, 0, 1]
EX14 = Fr(sum(vals), 3)
EY14 = Fr(sum(x*x for x in vals), 3)
EXY14 = Fr(sum(x*x*x for x in vals), 3)
check("ex14 Cov nulle", EXY14 - EX14*EY14 == 0)
pX0Y1 = Fr(0)  # X = 0 force Y = 0
check("ex14 pas independantes", pX0Y1 == 0 and Fr(1, 3)*Fr(2, 3) != 0)
# --- Exercice 15 : points fixes d'une permutation aléatoire ------------
for n15 in range(2, 8):
    fixes = [sum(1 for i in range(n15) if s[i] == i)
             for s in permutations(range(n15))]
    E15 = Fr(sum(fixes), factorial(n15))
    E15c = Fr(sum(f*f for f in fixes), factorial(n15))
    check(f"ex15 E = 1 (n={n15})", E15 == 1)
    check(f"ex15 V = 1 (n={n15})", E15c - E15**2 == 1)
# --- Exercice 16 : Markov et Tchebychev --------------------------------
check("ex16 Markov", Fr(2, 10) == Fr(1, 5))
pexact = Fr(sum(1 for k in range(1, 7) if abs(Fr(k) - Fr(7, 2)) >= 2), 6)
check("ex16 exact 1/3", pexact == Fr(1, 3))
check("ex16 borne Tchebychev", pexact <= Fr(35, 12)/4)
# --- Exercice 17 : loi faible des grands nombres -----------------------
check("ex17 sigma^2/n eps^2", Fr(1, 4)/(Fr(1, 20)*Fr(1, 100)) == 500)
# simulation exacte : binomiale n=500, p=1/2 : P(|M - 1/2| >= 0.1)
n17 = 500
tail = sum(comb(n17, k) for k in range(n17 + 1)
           if abs(Fr(k, n17) - Fr(1, 2)) >= Fr(1, 10))
check("ex17 vraie probabilite bien plus petite",
      Fr(tail, 2**n17) < Fr(1, 100000))
# --- Exercice 18 : anniversaires ---------------------------------------
def p_anniv(n):
    q = 1.0
    for k in range(n):
        q *= (365 - k)/365
    return 1 - q
check("ex18 n=23", isclose(p_anniv(23), 0.5073, abs_tol=2e-4))
check("ex18 n=22 insuffisant", p_anniv(22) < 0.5 < p_anniv(23))
check("ex18 n=50", p_anniv(50) > 0.96)
# --- Exercice 19 : dérangements probabilistes --------------------------
D = [1, 0]
for n in range(2, 12):
    D.append((n - 1)*(D[n - 1] + D[n - 2]))
check("ex19 P(derangement) -> 1/e",
      isclose(D[10]/factorial(10), 1/math.e, rel_tol=1e-7))
for k in [0, 1, 2, 3]:
    pk = comb(10, k)*D[10 - k]/factorial(10)
    check(f"ex19 P(k={k}) ~ e^-1/k!",
          isclose(pk, math.exp(-1)/factorial(k), rel_tol=2e-4))
# --- Exercice 20 : concentration binomiale -----------------------------
check("ex20 p(1-p) <= 1/4", all(Fr(p, 10)*(1 - Fr(p, 10)) <= Fr(1, 4)
      for p in range(11)))
n20, eps = 100, Fr(1, 10)
tail20 = sum(comb(n20, k) for k in range(n20 + 1)
             if abs(Fr(k, n20) - Fr(1, 2)) >= eps)
check("ex20 Tchebychev couvre la vraie queue",
      Fr(tail20, 2**n20) <= Fr(1, 4)/(n20*eps**2))
check("ex20 sondage n = 2000", Fr(1, 4)/(2000*Fr(1, 20)**2) == Fr(1, 20))
# --- Exercice 21 : Monty Hall ------------------------------------------
gains_change, gains_garde = 0, 0
for voiture in range(3):
    for choix in range(3):
        # l'animateur ouvre une porte ni choisie ni gagnante
        if choix == voiture:
            gains_garde += 2  # deux ouvertures possibles, chacune compte 1
            # en changeant on perd dans les deux cas
        else:
            gains_change += 2  # une seule porte ouvrable, poids double
check("ex21 changer gagne 2/3", Fr(gains_change, gains_change + gains_garde)
      == Fr(2, 3))
# --- Exercice 22 : espérance du maximum --------------------------------
def Emax(n, N):
    # max de n tirages uniformes independants sur {1..N}
    return sum(1 - Fr(k, N)**n for k in range(N))
brute22 = {}
for t in product(range(1, 7), repeat=2):
    m = max(t)
    brute22[m] = brute22.get(m, 0) + 1
check("ex22 P(M<=k) = (k/N)^n", all(
    Fr(sum(c for m, c in brute22.items() if m <= k), 36) == Fr(k, 6)**2
    for k in range(1, 7)))
check("ex22 n=2 N=6", Emax(2, 6) == Fr(161, 36))  # = E(V) de l'exercice 11
check("ex22 limite Riemann", isclose(float(Emax(3, 1000))/1000, 3/4, abs_tol=2e-3))
# --- Exercice 23 : marche aléatoire ------------------------------------
for n23 in [2, 4, 8]:
    pos = {}
    for t in product((-1, 1), repeat=n23):
        s = sum(t)
        pos[s] = pos.get(s, 0) + 1
    check(f"ex23 P(S=0) n={n23}",
          Fr(pos[0], 2**n23) == Fr(comb(n23, n23//2), 2**n23))
    E23 = Fr(sum(s*c for s, c in pos.items()), 2**n23)
    V23 = Fr(sum(s*s*c for s, c in pos.items()), 2**n23)
    check(f"ex23 E=0 V=n (n={n23})", E23 == 0 and V23 == n23)
check("ex23 equivalent", isclose(
    comb(200, 100)/4**100, 1/sqrt(pi*100), rel_tol=2e-3))
# --- Exercice 24 : polynômes de Bernstein ------------------------------
def bernstein(f, n, x):
    if x == 0:
        return f(0.0)
    if x == 1:
        return f(1.0)
    # poids binomiaux en logarithmes (évite tout débordement)
    lx, l1x = math.log(x), math.log(1 - x)
    lgn = math.lgamma(n + 1)
    return sum(
        f(k/n)*math.exp(lgn - math.lgamma(k + 1) - math.lgamma(n - k + 1)
                        + k*lx + (n - k)*l1x)
        for k in range(n + 1))
f24 = lambda t: abs(t - 0.4)  # continue non derivable
err = max(abs(bernstein(f24, 400, x/50) - f24(x/50)) for x in range(51))
err2 = max(abs(bernstein(f24, 1600, x/50) - f24(x/50)) for x in range(51))
check("ex24 convergence uniforme", err < 0.04 and err2 < err)
check("ex24 B_n(1) = 1", isclose(bernstein(lambda t: 1, 30, 0.37), 1))
check("ex24 B_n(x->x) = x", isclose(bernstein(lambda t: t, 30, 0.37), 0.37))

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
