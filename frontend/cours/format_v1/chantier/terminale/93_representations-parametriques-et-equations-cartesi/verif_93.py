# -*- coding: utf-8 -*-
"""Vérification exacte (sympy) de tous les résultats de la notion 93 :
représentations paramétriques et équations cartésiennes (Terminale).

    python verif_93.py      → « TOUT EST JUSTE » ou la liste des erreurs
"""
from sympy import Matrix, Rational as R, acos, deg, sqrt, symbols, solve, simplify, N, Eq, linsolve

t, s, k, u, l, x, y, z, m = symbols("t s k u lambda x y z m")
ERREURS = []


def ok(cond, msg):
    if not bool(cond):
        ERREURS.append(msg)


def V(*c):
    return Matrix(c)


def colineaires(a, b):
    return a.cross(b) == V(0, 0, 0) if len(a) == 3 else a[0] * b[1] - a[1] * b[0] == 0


def point(A, w, p):
    return A + p * w


def angle_deg(a, b):
    return N(deg(acos(a.dot(b) / (a.norm() * b.norm()))), 10)


# ======================================================================= cours
# I. d : A(1;2;-1), u(2;-1;3) ; B(5;0;5) ∈ d (t = 2) ; C(3;1;1) ∉ d
A, w = V(1, 2, -1), V(2, -1, 3)
ok(point(A, w, 2) == V(5, 0, 5), "cours I : B")
ok(point(A, w, 1) == V(3, 1, 2), "cours I : C (t = 1 donne z = 2)")
# II. plan par A(2;0;1), n(1;-2;3) : x - 2y + 3z - 5 = 0
ok(1 * 2 - 2 * 0 + 3 * 1 - 5 == 0, "cours II : plan")
# III. d ∩ P, P : x + y + z - 8 = 0
n = V(1, 1, 1)
ok(w.dot(n) == 4, "cours III : u.n")
M = point(A, w, t)
sol = solve(M[0] + M[1] + M[2] - 8, t)
ok(sol == [R(3, 2)], "cours III : t")
ok(point(A, w, R(3, 2)) == V(4, R(1, 2), R(7, 2)), "cours III : I")
# IV. d1 (1+t ; t ; 2-t), d2 (3+2s ; 1+s ; s) : non coplanaires
d1 = V(1 + t, t, 2 - t)
d2 = V(3 + 2 * s, 1 + s, s)
ok(not colineaires(V(1, 1, -1), V(2, 1, 1)), "cours IV : colinéarité")
s12 = solve([d1[0] - d2[0], d1[1] - d2[1]], [t, s])
ok(s12 == {t: 0, s: -1}, "cours IV : t, s")
ok((d1[2] - d2[2]).subs(s12) != 0, "cours IV : troisième équation")
ok(solve(list(d1 - d2), [t, s]) == [], "cours IV : aucune solution")
# IV bis. cube : (AB) et (CG) non coplanaires
Ac, Bc, Cc, Gc = V(0, 0, 0), V(1, 0, 0), V(1, 1, 0), V(1, 1, 1)
ok(solve(list(point(Ac, Bc - Ac, t) - point(Cc, Gc - Cc, s)), [t, s]) == [], "cours cube : (AB),(CG)")
ok(not colineaires(Bc - Ac, Gc - Cc), "cours cube : directions")
# V. P1 : x+y+z = 3, P2 : x-y+2z = 1
sv = solve([x + y + z - 3, x - y + 2 * z - 1], [x, y])
ok(simplify(sv[x] - (2 - R(3, 2) * z)) == 0 and simplify(sv[y] - (1 + R(1, 2) * z)) == 0, "cours V : droite")
dirV = V(-3, 1, 2)
ok(dirV.dot(V(1, 1, 1)) == 0 and dirV.dot(V(1, -1, 2)) == 0, "cours V : vecteur directeur (-3;1;2)")
# VI. projeté de O sur x + 2y + 2z - 9 = 0 : H(1;2;2), OH = 3
nP = V(1, 2, 2)
kk = solve(nP.dot(k * nP) - 9, k)
ok(kk == [1], "cours VI : k")
ok((kk[0] * nP).norm() == 3, "cours VI : OH")
# VI. projeté de M(9;0;1) sur d : (t ; 2t ; 1+2t) : H(1;2;3), MH = 6√2
Mv, Ad, ud = V(9, 0, 1), V(0, 0, 1), V(1, 2, 2)
tt = solve((point(Ad, ud, t) - Mv).dot(ud), t)
ok(tt == [1], "cours VI : t (droite)")
H = point(Ad, ud, 1)
ok(H == V(1, 2, 3), "cours VI : H (droite)")
ok(simplify((H - Mv).norm() - 6 * sqrt(2)) == 0, "cours VI : MH")

# =================================================================== exercices
# 983 (plan) : A(3;-2), u(1;2)
A2, u2 = Matrix([3, -2]), Matrix([1, 2])
ok(A2 + 2 * u2 == Matrix([5, 2]), "983 Q2")
ok(A2 - 2 * u2 == Matrix([1, -6]), "983 Q3")
ok(solve(-2 + 2 * t - 4, t) == [3] and A2 + 3 * u2 == Matrix([6, 4]), "983 Q4")

# 984 : A(1;2;-3), u(2;-1;4)
A, w = V(1, 2, -3), V(2, -1, 4)
ok(point(A, w, 1) == V(3, 1, 1), "984 Q2")
ok(point(A, w, 2) == V(5, 0, 5), "984 Q3")
ok(solve(-3 + 4 * t - 5, t) == [2], "984 Q4")
tc = solve(1 + 2 * t, t)[0]
ok(tc == R(-1, 2) and point(A, w, tc)[1] == R(5, 2), "984 Q5")

# 986 : plan par A(1;2;-1), n(3;-1;2)
n = V(3, -1, 2)
P = lambda X: 3 * X[0] - X[1] + 2 * X[2] + 1
ok(P(V(1, 2, -1)) == 0, "986 Q1")
ok(P(V(2, 5, 1)) == 4, "986 Q2")
u1, u2v = V(1, 3, 0), V(0, 2, 1)
ok(u1.dot(n) == 0 and u2v.dot(n) == 0 and not colineaires(u1, u2v), "986 Q3")
ok(P(V(0, 0, 0)) == 1, "986 Q5")

# 989 : d1 (t ; 2t ; 1+t), d2 (1+s ; 2+s ; 2+s)
d1 = V(t, 2 * t, 1 + t)
d2 = V(1 + s, 2 + s, 2 + s)
ok(not colineaires(V(1, 2, 1), V(1, 1, 1)), "989 Q2")
ok(solve(list(d1 - d2), [t, s]) == {t: 1, s: 0}, "989 Q3")
ok(d1.subs(t, 1) == V(1, 2, 2) and d2.subs(s, 0) == V(1, 2, 2), "989 Q4")
cos989 = V(1, 2, 1).dot(V(1, 1, 1)) / (V(1, 2, 1).norm() * V(1, 1, 1).norm())
ok(simplify(cos989 - 2 * sqrt(2) / 3) == 0, "989 Q5 cos")
a989 = angle_deg(V(1, 2, 1), V(1, 1, 1))
ok(abs(a989 - 19.47) < 0.005, f"989 Q5 angle {a989}")

# 985 (réécrit le 2026-11-02, dans l'espace) : d (A(1;-1;3), u(2;1;-1)), d' (A'(5;1;1), u'(-4;-2;2))
A85, u85, A85p, u85p = V(1, -1, 3), V(2, 1, -1), V(5, 1, 1), V(-4, -2, 2)
ok(u85p == -2 * u85, "985 Q2 u' = -2u")
tt85 = solve(1 + 2 * t - 5, t)
ok(tt85 == [2] and point(A85, u85, 2) == A85p, "985 Q3 A' ∈ d (t = 2)")
ok(point(A85p, u85p, s).subs(s, 1) == A85, "985 Q3 contrôle : A ∈ d' (s = 1)")
tr = solve(3 - t, t)
ok(tr == [3] and point(A85, u85, 3) == V(7, 2, 0), "985 Q4 R(7;2;0)")
E85 = V(0, 2, -1)
ok(point(E85, u85, k) == V(2 * k, 2 + k, -1 - k), "985 Q5 Δ")
te = solve(1 + 2 * t, t)[0]
ok(te == R(-1, 2) and (-1 + te) == R(-3, 2) and R(-3, 2) != 2, "985 Q5 E ∉ d")
ok(not colineaires(E85 - A85, u85), "985 Q5 Δ et d strictement parallèles")

# figures ajoutées (finition 2026-11-02)
# 1109 : plan Q contenant d1 et d4 ; d2, d3 le traversent en G, E
nQ = V(2, 1, -1).cross(V(-1, 0, 3) - V(1, -1, 2))
ok(nQ.dot(V(1, -1, 1)) != 0 and nQ.dot(V(1, -2, 1)) != 0, "fig 1109 : d2, d3 sécantes au plan Q")
ok(nQ.dot(V(1, 1, 2) - V(1, -1, 2)) == 0 and nQ.dot(V(3, 0, 1) - V(1, -1, 2)) == 0, "fig 1109 : G et E dans Q")
ok(solve(list(V(1, -1, 2) + t * V(2, 1, -1) - V(1, 1, 2)), t) == [], "fig 1109 : G ∉ d1")
# 992 : D hors de (ABC), I sur (d) et dans (ABC)
ok(0 + 4 * (-1) + 3 * 4 - 7 != 0, "fig 992 : D ∉ (ABC)")
# 989 : I(1;2;2) intersection
ok(V(1, 2, 2) == point(V(0, 0, 1), V(1, 2, 1), 1) == point(V(1, 2, 2), V(1, 1, 1), 0), "fig 989 : I")

# 1109
A, uu = V(1, -1, 2), V(2, 1, -1)
B, C = V(0, 2, 1), V(3, -1, 4)
ok(C - B == V(3, -3, 3), "1109 Q2 BC")
D1 = point(A, uu, t)
D2 = point(B, V(1, -1, 1), k)
D3 = V(3 + s, -2 * s, 1 + s)
D4 = point(V(-1, 0, 3), uu, l)
ok(D2.subs(k, 3) == C, "1109 Q2 C ∈ d2")
ok(not colineaires(uu, V(1, -1, 1)), "1109 Q5 colinéarité")
s12 = solve([D1[0] - D2[0], D1[1] - D2[1]], [t, k])
ok(s12 == {t: R(2, 3), k: R(7, 3)}, "1109 Q5 t,k")
ok((D1[2]).subs(s12) == R(4, 3) and D2[2].subs(s12) == R(10, 3), "1109 Q5 troisième")
ok(solve(list(D1 - D2), [t, k]) == [], "1109 Q5 aucune solution")
ok(solve(list(D1 - D3), [t, s]) == {t: 1, s: 0} and D1.subs(t, 1) == V(3, 0, 1), "1109 Q6")
ok(solve(list(D2 - D4), [k, l]) == {k: 1, l: 1} and D2.subs(k, 1) == V(1, 1, 2), "1109 Q7")

# 991 : d1 (1+2t ; 3-t ; -1+t), d2 (2+s ; 1+2s ; 3s)
d1 = V(1 + 2 * t, 3 - t, -1 + t)
d2 = V(2 + s, 1 + 2 * s, 3 * s)
ok(not colineaires(V(2, -1, 1), V(1, 2, 3)), "991 Q2")
s13 = solve([d1[0] - d2[0], d1[2] - d2[2]], [t, s])
ok(s13 == {t: R(2, 5), s: R(-1, 5)}, "991 Q3 t,s")
ok(d1[1].subs(s13) == R(13, 5) and d2[1].subs(s13) == R(3, 5), "991 Q3 L2")
ok(solve(list(d1 - d2), [t, s]) == [], "991 Q3 aucune solution")

# 990 : P1 x+y+z-1 = 0, P2 2x-y+z+3 = 0
n1, n2 = V(1, 1, 1), V(2, -1, 1)
ok(not colineaires(n1, n2), "990 Q2")
dd = V(-4 + 2 * t, t, 5 - 3 * t)
ok(simplify(n1.dot(dd) - 1) == 0 and simplify(n2.dot(dd) + 3) == 0, "990 Q3")
ok(V(2, 1, -3).dot(n1) == 0 and V(2, 1, -3).dot(n2) == 0, "990 Q4 direction")
ok(n1.dot(n2) == 2, "990 Q5 produit scalaire")
ok(simplify(n1.dot(n2) / (n1.norm() * n2.norm()) - sqrt(2) / 3) == 0, "990 Q5 cos")
a990 = angle_deg(n1, n2)
ok(abs(a990 - 61.87) < 0.005, f"990 Q5 angle {a990}")

# 988 : d (1+2t ; 3-t ; -1+t), P : x+2y-z+4 = 0
uu, n = V(2, -1, 1), V(1, 2, -1)
ok(uu.dot(n) == -1, "988 Q2")
dd = V(1 + 2 * t, 3 - t, -1 + t)
eq = n.dot(dd) + 4
ok(simplify(eq - (12 - t)) == 0, "988 Q3 équation")
ok(dd.subs(t, 12) == V(25, -9, 11), "988 Q3 I")
A = V(1, 3, -1)
kk = solve(n.dot(A + k * n) + 4, k)
ok(kk == [-2], "988 Q5 k")
H = A - 2 * n
ok(H == V(-1, -1, 1), "988 Q5 H")
ok(simplify((H - A).norm() - 2 * sqrt(6)) == 0, "988 Q5 AH")
ok(simplify(abs(n.dot(A) + 4) / n.norm() - 2 * sqrt(6)) == 0, "988 Q5 formule")

# 992
A, B, C = V(1, 0, 2), V(3, 1, 0), V(2, -1, 3)
ok(B - A == V(2, 1, -2) and C - A == V(1, -1, 1), "992 vecteurs")
ok(not colineaires(B - A, C - A), "992 non alignés")
nn = V(1, 4, 3)
ok(nn.dot(B - A) == 0 and nn.dot(C - A) == 0, "992 Q2 normal")
pl = lambda X: X[0] + 4 * X[1] + 3 * X[2] - 7
ok(pl(A) == 0 and pl(B) == 0 and pl(C) == 0, "992 Q2 équation")
ok(pl(V(0, -1, 4)) == 1, "992 Q3")
ok(V(1, -1, 2).dot(nn) == 3, "992 Q4")
dd = V(1 + t, 2 - t, 3 + 2 * t)
ok(simplify(pl(dd) - (11 + 3 * t)) == 0, "992 Q5 équation")
ok(dd.subs(t, R(-11, 3)) == V(R(-8, 3), R(17, 3), R(-13, 3)), "992 Q5 I")

# 1110 : pyramide
A, B, C, D, S = V(0, 0, 0), V(3, 0, 0), V(3, 2, 0), V(0, 2, 0), V(1, 1, 3)
ok(B - A == C - D and (B - A).dot(D - A) == 0, "1110 Q1a")
ok((B - A).norm() * (D - A).norm() == 6, "1110 Q1b")
ok(D - S == V(-1, 1, -3) and S - A == V(1, 1, 3), "1110 Q2")
P = S + R(1, 4) * (D - S)
ok(P == V(R(3, 4), R(5, 4), R(9, 4)), "1110 Q3")
ok(B - P == V(R(9, 4), R(-5, 4), R(-9, 4)) and C - P == V(R(9, 4), R(3, 4), R(-9, 4)), "1110 Q4 vecteurs")
ok(not colineaires(B - P, C - P), "1110 Q4a")
plan = lambda X: X[0] + X[2] - 3
ok(plan(P) == 0 and plan(B) == 0 and plan(C) == 0, "1110 Q4b")
nn = V(1, 0, 1)
ok(nn.dot(B - P) == 0 and nn.dot(C - P) == 0, "1110 Q4b normal")
uu = solve(plan(u * V(1, 1, 3)), u)
ok(uu == [R(3, 4)] and R(3, 4) * V(1, 1, 3) == V(R(3, 4), R(3, 4), R(9, 4)), "1110 Q5")
ok(V(1, 1, 3).dot(nn) == 4, "1110 Q5 u.n")
tt = solve(plan(S + t * nn), t)
ok(tt == [R(-1, 2)], "1110 Q6 t")
H = S - R(1, 2) * nn
ok(H == V(R(1, 2), 1, R(5, 2)), "1110 Q6 H")
SH = (H - S).norm()
ok(simplify(SH - sqrt(2) / 2) == 0, "1110 Q7a")
mm = solve((V(3, m, 0) - P).dot(V(0, 1, 0)), m)
ok(mm == [R(5, 4)], "1110 Q7b K")
K = V(3, R(5, 4), 0)
PK = (K - P).norm()
ok(simplify(PK - 9 * sqrt(2) / 4) == 0, "1110 Q7b PK")
aire = R(1, 2) * (C - B).norm() * PK
ok(simplify(aire - 9 * sqrt(2) / 4) == 0, "1110 Q7b aire")
ok(simplify(R(1, 2) * (B - P).cross(C - P).norm() - 9 * sqrt(2) / 4) == 0, "1110 Q7b aire (produit vectoriel)")
vol = R(1, 3) * aire * SH
ok(simplify(vol - R(3, 4)) == 0, "1110 Q7c")
ok(abs(Matrix.hstack(B - P, C - P, S - P).det()) / 6 == R(3, 4), "1110 Q7c déterminant")
# ancienne méthode (cosinus) : vérification des valeurs intermédiaires
ok((B - P).dot(C - P) == R(147, 16), "1110 ancien produit scalaire")

if ERREURS:
    print("ERREURS :")
    for e in ERREURS:
        print("  -", e)
else:
    print(f"TOUT EST JUSTE (angles : {a989:.4f}° et {a990:.4f}°)")
