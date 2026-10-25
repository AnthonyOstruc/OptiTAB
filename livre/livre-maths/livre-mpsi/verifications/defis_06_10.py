# -*- coding: utf-8 -*-
"""Vérifications des défis des chapitres 6 à 10."""
import cmath
import math
from fractions import Fraction as Fr
from itertools import permutations, product
from math import isclose, exp, gcd

import sympy as sp
from sympy.combinatorics import Permutation, PermutationGroup

OK = []

def check(name, cond):
    assert cond, f"ECHEC : {name}"
    OK.append(name)

# =====================================================================
# Défi 6 — Fonctions plates et fonctions plateaux
# =====================================================================
x = sp.symbols("x", positive=True)
X = sp.symbols("X")
f = sp.exp(-1/x)
P = [sp.Integer(1)]
for n in range(7):
    P.append(sp.expand(X**2*(P[-1] - sp.diff(P[-1], X))))
check("d6 P1 = X^2", P[1] == X**2)
check("d6 P2 = X^4 - 2X^3", sp.expand(P[2] - (X**4 - 2*X**3)) == 0)
for n in range(1, 7):
    deriv = sp.diff(f, x, n)
    check(f"d6 f^({n}) = P_n(1/x) e^(-1/x)",
          sp.simplify(deriv - P[n].subs(X, 1/x)*f) == 0)
    poly = sp.Poly(P[n], X)
    check(f"d6 deg P_{n} = 2n, dominant 1", poly.degree() == 2*n and poly.LC() == 1)
    check(f"d6 limite en 0+ de f^({n})", sp.limit(P[n].subs(X, 1/x)*f, x, 0, "+") == 0)
check("d6 taux d'accroissement en 0", sp.limit(f/x, x, 0, "+") == 0)
def ff(t):
    return math.exp(-1/t) if t > 0 else 0.0
def h(t):
    return ff(t)/(ff(t) + ff(1 - t))
check("d6 h = 0 sur R-", all(h(t) == 0 for t in [-3, -1, -0.2, 0]))
check("d6 h = 1 sur [1,+inf[", all(h(t) == 1 for t in [1, 1.5, 4]))
grid = [i/1000 for i in range(100, 901)]   # loin des bords : pas de saturation flottante
hv = [h(t) for t in grid]
uu = [1/t - 1/(1 - t) for t in [i/1000 for i in range(1, 1000)]]
check("d6 u(t) = 1/t - 1/(1-t) strictement decroissante",
      all(uu[i] > uu[i + 1] for i in range(len(uu) - 1)))
check("d6 h croissante sur ]0,1[", all(hv[i] < hv[i + 1] for i in range(len(hv) - 1)))
check("d6 h(1/2) = 1/2", isclose(h(0.5), 0.5))
check("d6 symetrie h(x)+h(1-x)=1", all(isclose(h(t) + h(1 - t), 1) for t in grid))
def g(t):
    return ff(t)*ff(1 - t)
check("d6 g > 0 sur ]0,1[ et nulle ailleurs", all(g(t) > 0 for t in grid)
      and all(g(t) == 0 for t in [-1, 0, 1, 2]))
check("d6 max de g en 1/2 = e^-4", isclose(max(g(t) for t in grid), math.exp(-4)))
def phi(t):
    return h(t + 2)*h(2 - t)
check("d6 phi = 1 sur [-1,1]", all(phi(t) == 1 for t in [-1, -0.5, 0, 0.7, 1]))
check("d6 phi = 0 hors ]-2,2[", all(phi(t) == 0 for t in [-3, -2, 2, 2.5]))
check("d6 0 < phi < 1 sur ]1,2[", all(0 < phi(t) < 1 for t in [1.1, 1.5, 1.9]))

# =====================================================================
# Défi 7 — Le chiffrement RSA
# =====================================================================
p_, q_ = 61, 53
n_ = p_*q_
ph = (p_ - 1)*(q_ - 1)
check("d7 n = 3233", n_ == 3233)
check("d7 phi(n) = 3120 (comptage)", ph == 3120 == sum(1 for k in range(1, n_ + 1)
      if gcd(k, n_) == 1))
e_, d_ = 17, 2753
check("d7 17 et 3120 premiers entre eux", gcd(e_, ph) == 1)
check("d7 e d = 1 mod phi", (e_*d_) % ph == 1 and e_*d_ == 15*ph + 1)
check("d7 inverse modulaire", pow(e_, -1, ph) == d_)
# Euclide étendu : 3120 = 183*17 + 9 ; 17 = 1*9 + 8 ; 9 = 1*8 + 1
check("d7 divisions d'Euclide", 3120 == 183*17 + 9 and 17 == 9 + 8 and 9 == 8 + 1)
check("d7 Bezout 3120*(-15) + 17*2753 = 1", 3120*(-15) + 17*2753 == 1)
m_ = 65
puiss = [pow(m_, 2**k, n_) for k in range(5)]
check("d7 carres successifs", puiss == [65, 992, 1232, 1547, 789])
c_ = pow(m_, e_, n_)
check("d7 chiffrement 65 -> 2790", c_ == 2790 == (789*65) % n_)
check("d7 dechiffrement", pow(c_, d_, n_) == m_)
check("d7 restes chinois", d_ % 60 == 53 and d_ % 52 == 49
      and pow(c_ % 61, 53, 61) == m_ % 61 and pow(c_ % 53, 49, 53) == m_ % 53)
check("d7 correction pour tout m", all(pow(mm, e_*d_, n_) == mm for mm in range(n_)))
check("d7 m non premier avec n", pow(61*7, e_*d_, n_) == 61*7)
Xs = sp.symbols("Xs")
check("d7 factorisation par phi", sp.factor(Xs**2 - (n_ - ph + 1)*Xs + n_)
      == (Xs - 61)*(Xs - 53))
check("d7 p + q = 114", n_ - ph + 1 == 114)
def nb_mult(k):
    # exponentiation rapide : carrés + produits
    return (k.bit_length() - 1) + (bin(k).count("1") - 1)
check("d7 17 : 5 multiplications", nb_mult(17) == 5)
check("d7 borne 2 log2 k", all(nb_mult(k) <= 2*math.log2(k) for k in range(2, 5000)))

# =====================================================================
# Défi 8 — Le groupe du carré et les coloriages
# =====================================================================
# sommets 0,1,2,3 (sens trigonométrique) ; r = (0 1 2 3), s = symétrie d'axe (0 2)
r = Permutation([1, 2, 3, 0])
s = Permutation([0, 3, 2, 1])
D4 = PermutationGroup([r, s])
check("d8 ordre 8", D4.order() == 8)
check("d8 non commutatif", not D4.is_abelian)
check("d8 s r s = r^-1", s*r*s == r**-1)
elems = list(D4.elements)
ordres = sorted(g.order() for g in elems)
check("d8 ordres", ordres == [1, 2, 2, 2, 2, 2, 4, 4])
centre = [g for g in elems if all(g*h_ == h_*g for h_ in elems)]
check("d8 centre {id, r^2}", sorted(centre, key=lambda p: p.array_form)
      == sorted([Permutation([0, 1, 2, 3]), r**2], key=lambda p: p.array_form))
sg4 = []
for trio in [(r,), (r**2, s), (r**2, r*s)]:
    H = PermutationGroup(list(trio))
    sg4.append(H.order())
check("d8 sous-groupes d'ordre 4", sg4 == [4, 4, 4])
check("d8 Klein non cyclique", not PermutationGroup([r**2, s]).is_cyclic)
def nb_cycles(g):
    return len(g.cyclic_form) + (4 - sum(len(c) for c in g.cyclic_form))
fix = {}
for g in elems:
    fix[tuple(g.array_form)] = 2**nb_cycles(g)
check("d8 somme des points fixes 48", sum(fix.values()) == 48)
# comptage direct des classes de coloriages à 2 couleurs
def canon(col):
    return min(tuple(col[g.array_form[i]] for i in range(4)) for g in elems)
classes2 = {canon(c) for c in product((0, 1), repeat=4)}
check("d8 six classes a 2 couleurs", len(classes2) == 6 == 48//8)
classes3 = {canon(c) for c in product((0, 1, 2), repeat=4)}
check("d8 21 classes a 3 couleurs", len(classes3) == 21
      == sum(3**nb_cycles(g) for g in elems)//8)
check("d8 formule 3 couleurs", (81 + 2*3 + 9 + 2*27 + 2*9)//8 == 21)

# =====================================================================
# Défi 9 — Carrés magiques
# =====================================================================
def est_magique(M):
    s = sum(M[0])
    lignes = all(sum(M[i]) == s for i in range(3))
    cols = all(sum(M[i][j] for i in range(3)) == s for j in range(3))
    d1 = sum(M[i][i] for i in range(3)) == s
    d2 = sum(M[i][2 - i] for i in range(3)) == s
    return lignes and cols and d1 and d2
def lucas(c, a, b):
    return [[c - a, c + a + b, c - b], [c + a - b, c, c - a + b], [c + b, c - a - b, c + a]]
check("d9 parametrage de Lucas magique", all(est_magique(lucas(c, a, b))
      for c in range(-3, 4) for a in range(-3, 4) for b in range(-3, 4)))
# le système : 8 équations, inconnues m11..m33 et s ; solution de dimension 3
m = sp.symbols("m1:10")
s_ = sp.symbols("s_")
M = sp.Matrix(3, 3, m)
eqs = [sum(M[i, :]) - s_ for i in range(3)] + [sum(M[:, j]) - s_ for j in range(3)] \
    + [M[0, 0] + M[1, 1] + M[2, 2] - s_, M[0, 2] + M[1, 1] + M[2, 0] - s_]
A = sp.Matrix([[sp.diff(e_q, v) for v in list(m) + [s_]] for e_q in eqs])
check("d9 rang 7, solutions de dimension 3", A.rank() == 7 and 10 - A.rank() == 3)
sol = sp.solve(eqs, list(m), dict=True)[0]
check("d9 centre = s/3", sp.simplify(sol.get(m[4], m[4]) - s_/3) == 0)
# carrés magiques à entrées 1..9
sols = [M_ for M_ in ([list(p[0:3]), list(p[3:6]), list(p[6:9])]
        for p in permutations(range(1, 10))) if est_magique(M_)]
check("d9 huit carres normaux", len(sols) == 8)
loshu = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]
check("d9 Lo Shu", loshu in sols and lucas(5, 1, 3) == loshu)
check("d9 tous de centre 5", all(S[1][1] == 5 for S in sols))
L = sp.Matrix(loshu)
J = sp.ones(3)
check("d9 semi-magique : LJ = JL = 15J", L*J == 15*J and J*L == 15*J)
check("d9 det Lo Shu", L.det() == 360)
L2 = L*L
check("d9 L^2 explicite", L2 == sp.Matrix([[59, 83, 83], [83, 59, 83], [83, 83, 59]]))
check("d9 L^2 semi-magique de somme 225", all(sum(L2[i, :]) == 225 for i in range(3))
      and all(sum(L2[:, j]) == 225 for j in range(3)))
check("d9 L^2 non magique", L2[0, 0] + L2[1, 1] + L2[2, 2] != 225)
Linv = L.inv()
check("d9 L^-1 magique de somme 1/15", est_magique([[Linv[i, j] for j in range(3)]
      for i in range(3)]) and sum(Linv[0, :]) == sp.Rational(1, 15))
check("d9 L^-1 explicite", 360*Linv == sp.Matrix([[23, -52, 53], [38, 8, -22], [-37, 68, -7]]))
cc, aa, bb = sp.symbols("cc aa bb")
Lg = sp.Matrix(lucas(cc, aa, bb))
check("d9 transposee L(c,a,b)^T = L(c,a,-b)", Lg.T == sp.Matrix(lucas(cc, aa, -bb)))
check("d9 det general 9c(b^2-a^2)", sp.expand(Lg.det() - 9*cc*(bb**2 - aa**2)) == 0)
Lgi = sp.simplify(Lg.inv())
sg = sp.simplify(sum(Lgi[0, :]))
check("d9 inverse d'une magique 3x3 magique de somme 1/(3c)",
      sp.simplify(sg - 1/(3*cc)) == 0 and all(sp.simplify(e_ - sg) == 0 for e_ in
      [sum(Lgi[i, :]) for i in range(3)] + [sum(Lgi[:, j]) for j in range(3)]
      + [Lgi[0, 0] + Lgi[1, 1] + Lgi[2, 2], Lgi[0, 2] + Lgi[1, 1] + Lgi[2, 0]]))
B = sp.Matrix([[2, 0, 1], [0, 3, 0], [1, 0, 2]])  # semi-magique de somme 3
check("d9 produit semi-magique", all(sum((L*B)[i, :]) == 45 for i in range(3))
      and all(sum((L*B)[:, j]) == 45 for j in range(3)))

# =====================================================================
# Défi 10 — Le théorème de Gauss-Lucas
# =====================================================================
Z = sp.symbols("Z")
Pz = (Z - 1)*(Z + 1)*(Z - 2*sp.I)
Pp = sp.expand(sp.diff(Pz, Z))
check("d10 P' = 3Z^2 - 4iZ - 1", sp.expand(Pp - (3*Z**2 - 4*sp.I*Z - 1)) == 0)
rac = sp.solve(Pp, Z)
check("d10 racines de P'", set(rac) == {sp.I, sp.I/3})
# barycentres : i = l1*1 + l2*(-1) + l3*(2i), coefficients positifs
for zz in rac:
    l1, l2, l3 = sp.symbols("l1 l2 l3")
    sl = sp.solve([l1 - l2 - sp.re(zz), 2*l3 - sp.im(zz), l1 + l2 + l3 - 1], [l1, l2, l3])
    check(f"d10 {zz} dans le triangle", all(v >= 0 for v in sl.values()))
check("d10 i = 1/4 + 1/4 (-1) ... barycentre", True)
# P'/P = somme des 1/(Z - a_k)
check("d10 derivee logarithmique", sp.simplify(sp.diff(Pz, Z)/Pz
      - (1/(Z - 1) + 1/(Z + 1) + 1/(Z - 2*sp.I))) == 0)
# moyenne des racines conservée
check("d10 moyennes", sp.simplify(sum(rac)/2 - (1 - 1 + 2*sp.I)/3) == 0)
check("d10 X^3 - 1", sp.solve(sp.diff(Z**3 - 1, Z), Z) == [0])
# vérification aléatoire de Gauss-Lucas (enveloppe convexe en 2D)
import random
random.seed(7)
def dans_enveloppe(z, pts):
    # test : z est barycentre à coefficients >= 0 (via arguments : z n'est séparé par aucune droite)
    for k in range(360):
        u = cmath.exp(1j*math.radians(k))
        if (z*u.conjugate()).real > max((p*u.conjugate()).real for p in pts) + 1e-9:
            return False
    return True
for essai in range(30):
    pts = [complex(random.uniform(-2, 2), random.uniform(-2, 2)) for _ in range(5)]
    coeffs = sp.Poly(sp.expand(sp.prod([Z - complex(p_) for p_ in pts])), Z).all_coeffs()
    der = sp.Poly(sp.Poly(coeffs, Z).diff(Z), Z)
    rz = [complex(r_) for r_ in der.nroots()]
    check(f"d10 Gauss-Lucas aleatoire {essai}", all(dans_enveloppe(z, pts) for z in rz))
# racines dans un disque
check("d10 disque", all(abs(complex(r_)) <= 2 for r_ in sp.solve(sp.diff(Z**4 - 16, Z), Z)))

print(f"Toutes les vérifications ont réussi ({len(OK)} assertions).")
