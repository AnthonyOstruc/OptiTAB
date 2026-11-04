# -*- coding: utf-8 -*-
"""Vérification exacte (sympy) de tous les résultats de la notion 180
« Vecteurs, droites et plans de l'espace » : cours, fiche, exercices, figures.

    python verif_vecteurs_espace.py      → « TOUT EST JUSTE » ou la liste des écarts
"""
from sympy import Matrix, Rational as Q, symbols, solve, simplify

ERREURS = []


def ok(cond, msg):
    if not cond:
        ERREURS.append(msg)


def V(*c):
    return Matrix([Q(x) if not isinstance(x, Q) else x for x in c])


def colineaires(u, v):
    return u.cross(v) == Matrix([0, 0, 0])


def comb2(w, u, v):
    """(a, b) tels que w = a u + b v, ou None."""
    a, b = symbols("a b")
    s = solve(list(a * u + b * v - w), [a, b], dict=True)
    return (s[0][a], s[0][b]) if s else None


def coplanaires(u, v, w):
    return Matrix.hstack(u, v, w).det() == 0


# --------------------------------------------------------------- cube unité
C = {"A": V(0, 0, 0), "B": V(1, 0, 0), "C": V(1, 1, 0), "D": V(0, 1, 0),
     "E": V(0, 0, 1), "F": V(1, 0, 1), "G": V(1, 1, 1), "H": V(0, 1, 1)}


def vec(P, R, pts=C):
    return pts[R] - pts[P]


# =============================================================== COURS
# I. Chasles dans le cube : AG = AB + BC + CG = AB + AD + AE
ok(vec("A", "G") == vec("A", "B") + vec("B", "C") + vec("C", "G"), "cours : AG = AB + BC + CG")
ok(vec("A", "G") == vec("A", "B") + vec("A", "D") + vec("A", "E"), "cours : AG = AB + AD + AE")
# II. figure du plan : AM = 2u + 1,5v (construction, rien à vérifier numériquement)
# coplanarité dans le cube : EG = EF + EH ; EF, EH, EA non coplanaires
ok(vec("E", "G") == vec("E", "F") + vec("E", "H"), "cours : EG = EF + EH")
ok(not coplanaires(vec("E", "F"), vec("E", "H"), vec("E", "A")), "cours : EF, EH, EA non coplanaires")
# exemple de coplanarité en coordonnées
u, v, w, t = V(1, 0, 1), V(0, 1, 1), V(2, 3, 5), V(1, 1, 3)
ok(comb2(w, u, v) == (2, 3), "cours : w = 2u + 3v")
ok(comb2(t, u, v) is None and not coplanaires(u, v, t), "cours : u, v, t non coplanaires")
ok(1 + 1 == 2 and 2 != 3, "cours : a + b = 2 ≠ 3")
# III. alignement A(1;0;2), B(3;1;1), C(7;3;-1)
A, B, Cc = V(1, 0, 2), V(3, 1, 1), V(7, 3, -1)
ok(B - A == V(2, 1, -1) and Cc - A == V(6, 3, -3) and Cc - A == 3 * (B - A), "cours : AC = 3AB")
# repère : M(2;3;2)
# V. section du cube par (IJG), I milieu de [AB], J milieu de [BC]
I, J = (C["A"] + C["B"]) / 2, (C["B"] + C["C"]) / 2
ok(vec("E", "G") == 2 * (J - I), "cours : EG = 2 IJ (trapèze)")
ok(coplanaires(J - I, C["G"] - I, C["E"] - I), "cours : I, J, G, E coplanaires")
ok((C["G"] - J).norm() == (C["E"] - I).norm(), "cours : trapèze isocèle (JG = IE)")

# =============================================================== EXERCICES
# 1093
u, v, w = V(2, -1, 3), V(1, 4, -2), V(0, 2, 1)
ok(u + v == V(3, 3, 1), "1093 Q1")
ok(3 * u == V(6, -3, 9) and 2 * v == V(2, 8, -4) and 3 * u - 2 * v == V(4, -11, 13), "1093 Q2")
ok(not colineaires(u, v), "1093 Q3")
ok(u + v + w == V(3, 5, 2), "1093 Q4")
ok(V(4, -1, 5) - V(1, 2, 3) == V(3, -3, 2), "1093 Q5")

# 1094
A, B, Cc = V(1, 2, 3), V(3, 4, 5), V(2, 3, 4)
ok(B - A == V(2, 2, 2) and Cc - A == V(1, 1, 1), "1094 Q1-Q2")
ok(B - A == 2 * (Cc - A), "1094 Q3 : AB = 2AC")
ok(Cc == (A + B) / 2, "1094 : C milieu de [AB]")

# 1095
u, v, w = V(1, 2, 0), V(0, 1, 1), V(2, 5, 1)
ok(comb2(w, u, v) == (2, 1), "1095 Q1 : w = 2u + v")
ok(not colineaires(u, v), "1095 Q2")
ok(coplanaires(u, v, w), "1095 Q3")
ok(comb2(V(3, 7, 2), u, v) is None and 2 * 3 + 2 == 8, "1095 Q5 : (3;7;2) pas combinaison (2a + b = 8 ≠ 7)")

# 1096
P = {"A": V(0, 0, 0), "B": V(2, 1, 0), "C": V(1, 2, 1), "D": V(3, 3, 1), "E": V(1, 0, 2)}
AB, AC, AD, AE = (P[k] - P["A"] for k in "BCDE")
ok(AB == V(2, 1, 0) and AC == V(1, 2, 1) and AD == V(3, 3, 1), "1096 Q1")
ok(not colineaires(AB, AC), "1096 Q2")
ok(comb2(AD, AB, AC) == (1, 1), "1096 Q4 : AD = AB + AC")
ok(P["D"] - P["C"] == AB, "1096 : ABDC parallélogramme (CD = AB)")
ok(comb2(AE, AB, AC) is None, "1096 Q5 : E hors du plan (ABC)")
ok(2 * Q(-1, 2) + 2 == 1 and Q(-1, 2) + 2 * 2 == Q(7, 2), "1096 Q5 : a = -1/2, a + 2b = 7/2 ≠ 0")

# 1097
ok(vec("A", "G") == V(1, 1, 1), "1097 Q2")
ok(vec("A", "C") == V(1, 1, 0), "1097 Q3")
ok(vec("E", "F") == V(1, 0, 0) and vec("E", "H") == V(0, 1, 0) and not colineaires(vec("E", "F"), vec("E", "H")), "1097 Q4")
ok(vec("E", "G") == vec("E", "F") + vec("E", "H"), "1097 Q4 : EG = EF + EH")
ok(comb2(vec("A", "H"), vec("A", "C"), vec("A", "F")) is None, "1097 Q5 : A, C, F, H non coplanaires")
ok(not coplanaires(vec("A", "C"), vec("A", "F"), vec("A", "H")), "1097 Q5 (déterminant)")
# système de Q5 : AH = a AC + b AF -> a + b = 0, a = 1, b = 1
ok(V(0, 1, 1) != 1 * V(1, 1, 0) + 1 * V(1, 0, 1), "1097 Q5 système")
# ACFH tétraèdre régulier (arêtes √2)
for X, Y in [("A", "C"), ("A", "F"), ("A", "H"), ("C", "F"), ("C", "H"), ("F", "H")]:
    ok(vec(X, Y).norm() ** 2 == 2, f"1097 : {X}{Y} = √2")

# 1098
ok(vec("B", "C") == V(0, 1, 0), "1098 Q2")
ok(vec("A", "D") == vec("B", "C") and vec("F", "G") == vec("B", "C"), "1098 : (d1) = (AD), (d2) = (FG)")
# plans (ADG) : x = z ; (BCE) : x + z = 1
def dans_plan(M, O, a, b):
    return coplanaires(a, b, M - O)
for X in "ADGF":
    ok(dans_plan(C[X], C["A"], vec("A", "D"), vec("A", "G")), f"1098 : {X} ∈ (ADG)")
for X in "BCHE":
    ok(dans_plan(C[X], C["B"], vec("B", "C"), vec("B", "E")), f"1098 : {X} ∈ (BCE)")
ok(not dans_plan(C["B"], C["A"], vec("A", "D"), vec("A", "G")), "1098 : B ∉ (ADG) (plans distincts)")
K = (C["A"] + C["F"]) / 2
ok(K == (C["B"] + C["E"]) / 2 == V(Q(1, 2), 0, Q(1, 2)), "1098 : K milieu de [AF] et de [BE]")
ok(dans_plan(K, C["A"], vec("A", "D"), vec("A", "G")) and dans_plan(K, C["B"], vec("B", "C"), vec("B", "E")), "1098 : K dans les deux plans")
L = (C["D"] + C["G"]) / 2
ok(L == (C["C"] + C["H"]) / 2 and L - K == vec("B", "C"), "1098 : L centre de DCGH, KL = BC")
ok(dans_plan(L, C["A"], vec("A", "D"), vec("A", "G")) and dans_plan(L, C["B"], vec("B", "C"), vec("B", "E")), "1098 : L dans les deux plans")
# direction de l'intersection : produit vectoriel des normales
n1 = vec("A", "D").cross(vec("A", "G"))
n2 = vec("B", "C").cross(vec("B", "E"))
ok(colineaires(n1.cross(n2), vec("B", "C")), "1098 : Δ ∥ (BC)")

# 1102 : I, J, K milieux de [AD], [AE], [FG] ; section hexagonale
I, J, K = (C["A"] + C["D"]) / 2, (C["A"] + C["E"]) / 2, (C["F"] + C["G"]) / 2
n = (J - I).cross(K - I)
def dans_IJK(M):
    return (n.T * (M - I))[0] == 0
Pp = V(0, Q(-1, 2), 1)
ok(dans_IJK(Pp) and colineaires(Pp - C["E"], vec("E", "H")), "1102 : P ∈ (IJ) ∩ (EH)")
ok(colineaires(Pp - I, J - I), "1102 : P ∈ (IJ)")
ok(C["E"] - Pp == vec("E", "H") / 2, "1102 : PE = EH/2 (P au-delà de E)")
ok(colineaires(J - I, vec("D", "E")), "1102 : (IJ) ∥ (DE)")
R = (C["E"] + C["F"]) / 2
ok(dans_IJK(R) and colineaires(R - Pp, K - Pp), "1102 : R milieu de [EF] sur (PK)")
N = (C["C"] + C["G"]) / 2
M = (C["C"] + C["D"]) / 2
ok(dans_IJK(N) and dans_IJK(M), "1102 : N, M milieux de [CG], [CD] dans (IJK)")
ok(colineaires(N - K, J - I), "1102 : (KN) ∥ (IJ)")
ok(colineaires(M - I, K - R), "1102 : (IM) ∥ (RK)")
for X, Y in [(I, J), (J, R), (R, K), (K, N), (N, M), (M, I)]:
    ok((Y - X).norm() ** 2 == Q(1, 2), "1102 : côtés √2/2")
# aucun autre sommet de la section : les arêtes coupées sont exactement 6
aretes = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("E", "F"), ("F", "G"), ("G", "H"), ("H", "E"),
          ("A", "E"), ("B", "F"), ("C", "G"), ("D", "H")]
coupees = []
for X, Y in aretes:
    fx, fy = (n.T * (C[X] - I))[0], (n.T * (C[Y] - I))[0]
    if fx * fy < 0 or fx == 0 or fy == 0:
        coupees.append(X + Y)
ok(sorted("".join(sorted(x)) for x in coupees) == sorted(["AD", "AE", "EF", "FG", "CG", "CD"]), f"1102 : arêtes coupées {coupees}")
# point S de l'ancienne rédaction : (JR) ∩ (BF) est HORS du cube (au-dessus de F)
s = symbols("s")
S = J + s * (R - J)
sol = solve([S[0] - 1, S[1] - 0], s)
ok(S.subs(s, sol[s])[2] > 1, "1102 : (JR) coupe (BF) au-dessus de F (hors de l'arête)")

# 1101 : tétraèdre quelconque, milieux
a, b, c, d = (Matrix(symbols(f"{p}1 {p}2 {p}3")) for p in "abcd")
I, J, K, L = (a + b) / 2, (a + c) / 2, (c + d) / 2, (b + d) / 2
ok(simplify(J - I - (c - b) / 2) == Matrix([0, 0, 0]), "1101 : IJ = BC/2")
ok(simplify(K - L - (c - b) / 2) == Matrix([0, 0, 0]), "1101 : LK = BC/2")
ok(simplify(K - J - (d - a) / 2) == Matrix([0, 0, 0]), "1101 : JK = AD/2")
ok(simplify(L - I - (d - a) / 2) == Matrix([0, 0, 0]), "1101 : IL = AD/2")
ok(simplify((J - I) - (K - L)) == Matrix([0, 0, 0]), "1101 : IJ = LK (parallélogramme IJKL)")

# 1103 : I milieu de [EF], J milieu de [BC]
I, J = (C["E"] + C["F"]) / 2, (C["B"] + C["C"]) / 2
ok(I == V(Q(1, 2), 0, 1) and J == V(1, Q(1, 2), 0), "1103 : I, J")
ok(J - I == V(Q(1, 2), Q(1, 2), -1), "1103 : IJ")
ok(vec("C", "E") == V(-1, -1, 1) and vec("C", "G") == V(0, 0, 1), "1103 : CE, CG")
ok(J - I == -Q(1, 2) * vec("C", "E") - Q(1, 2) * vec("C", "G"), "1103 : IJ = -CE/2 - CG/2")
ok(comb2(J - I, vec("C", "E"), vec("C", "G")) == (Q(-1, 2), Q(-1, 2)), "1103 : unicité a = b = -1/2")
# décomposition dans (AB, AD, AE)
ok(J - I == Q(1, 2) * vec("A", "B") + Q(1, 2) * vec("A", "D") - vec("A", "E"), "1103 : IJ = AB/2 + AD/2 - AE")
ok(vec("C", "E") == -vec("A", "B") - vec("A", "D") + vec("A", "E"), "1103 : CE = -AB - AD + AE")

# 1099
A, B, Cc, D = V(1, 0, 0), V(2, 1, 0), V(0, 1, 1), V(3, 2, 1)
AB, AC, AD = B - A, Cc - A, D - A
ok(AB == V(1, 1, 0) and AC == V(-1, 1, 1) and AD == V(2, 2, 1), "1099 Q1")
ok(not colineaires(AB, AC), "1099 Q2")
ok(comb2(AD, AB, AC) is None, "1099 Q4")
ok(3 + 1 == 4 and 4 != 2, "1099 Q4 : a = 3, b = 1, a + b = 4 ≠ 2")
ok(not coplanaires(AB, AC, AD), "1099 Q5")

# 1100
u1, u2, v1, v2 = V(2, 1, -1), V(1, -1, 2), V(1, 1, 0), V(0, 1, 1)
A, B, Cc = V(1, 0, 1), V(0, 2, 0), V(0, 0, 1)
ok(not colineaires(u1, u2), "1100 Q1")
ok(not colineaires(v1, v2), "1100 Q2")
ok(comb2(u1, v1, v2) == (2, -1), "1100 Q3 : u1 = 2v1 - v2")
ok(comb2(u2, v1, v2) is None, "1100 Q4")
ok(comb2(A - Cc, v1, v2) is None, "1100 Q5 : A ∉ P")
# d2 coupe P : point d'intersection
tt, x, y = symbols("tt x y")
sol = solve(list(B + tt * u2 - (Cc + x * v1 + y * v2)), [tt, x, y], dict=True)
ok(len(sol) == 1, "1100 Q6 : d2 ∩ P = un point")
Ipt = B + sol[0][tt] * u2
ok(Ipt == V(Q(3, 4), Q(5, 4), Q(3, 2)) and sol[0][tt] == Q(3, 4) and sol[0][x] == Q(3, 4) and sol[0][y] == Q(1, 2),
   f"1100 Q6 : point d'intersection {list(Ipt)}")
# d1, d2 : pas d'intersection
t1, t2 = symbols("t1 t2")
ok(solve(list(A + t1 * u1 - (B + t2 * u2)), [t1, t2], dict=True) == [], "1100 Q7 : d1 ∩ d2 = ∅")
ok(1 + 2 * Q(1, 3) == Q(5, 3) and 1 - Q(1, 3) == Q(2, 3) and 2 * Q(5, 3) == Q(10, 3), "1100 Q7 : valeurs t = 1/3, s = 5/3")

# 1104 : pavé ABCDEFGH, repère (A ; AB, AD, AE) — coordonnées « comme dans un cube »
I = (C["B"] + C["F"]) / 2
ok(I == V(1, 0, Q(1, 2)), "1104 : I")
CA, DE, DG = vec("C", "A"), vec("D", "E"), vec("D", "G")
ok(CA == V(-1, -1, 0) and DE == V(0, -1, 1) and DG == V(1, 0, 1), "1104 Q1 coordonnées")
ok(CA == DE - DG and comb2(CA, DE, DG) == (1, -1), "1104 Q1 : CA = DE - DG")
AI, DF, HE = I - C["A"], vec("D", "F"), vec("H", "E")
ok(AI == V(1, 0, Q(1, 2)) and DF == V(1, -1, 1) and HE == V(0, -1, 0), "1104 Q2 coordonnées")
ok(not colineaires(DF, HE), "1104 Q2 : DF, HE non colinéaires")
ok(comb2(AI, DF, HE) is None and not coplanaires(AI, DF, HE), "1104 Q2 : non coplanaires")
# vérité dans un pavé de dimensions quelconques (repère orthonormé)
la, lb, lc = symbols("la lb lc", positive=True)
Pv = {"A": Matrix([0, 0, 0]), "B": Matrix([la, 0, 0]), "C": Matrix([la, lb, 0]), "D": Matrix([0, lb, 0]),
      "E": Matrix([0, 0, lc]), "F": Matrix([la, 0, lc]), "G": Matrix([la, lb, lc]), "H": Matrix([0, lb, lc])}
ok(simplify(vec("C", "A", Pv) - (vec("D", "E", Pv) - vec("D", "G", Pv))) == Matrix([0, 0, 0]), "1104 : CA = DE - DG (pavé quelconque)")
Ip = (Pv["B"] + Pv["F"]) / 2
ok(simplify(Matrix.hstack(Ip - Pv["A"], vec("D", "F", Pv), vec("H", "E", Pv)).det()) != 0, "1104 : non coplanaires (pavé quelconque)")

# =============================================================== FINITION 2026-11-02
# valeurs écrites sur les nouvelles figures et dans les textes ajoutés
Af, Bf = V(1, 2, 3), V(4, -1, 5)
ok(Bf - Af == V(3, -3, 2), "fig 1093 : AB(3 ; -3 ; 2), chemin +3, -3, +2")
A4, B4, C4 = V(1, 2, 3), V(3, 4, 5), V(2, 3, 4)
ok((A4 + B4) / 2 == C4 and B4 - A4 == 2 * (C4 - A4), "fig 1094 : C milieu de [AB], AB = 2 AC")
u5, v5, w5, t5 = V(1, 2, 0), V(0, 1, 1), V(2, 5, 1), V(3, 7, 2)
ok(2 * u5 + v5 == w5, "fig 1095 : w = 2u + v")
ok(3 * u5 + 2 * v5 == V(3, 8, 2) and 3 * u5 + 2 * v5 != t5, "1095 Q5 : 3u + 2v = (3 ; 8 ; 2) ≠ t")
ok(not coplanaires(u5, v5, t5), "1095 Q5 : u, v, t non coplanaires")
A6, B6, C6, D6, E6 = V(0, 0, 0), V(2, 1, 0), V(1, 2, 1), V(3, 3, 1), V(1, 0, 2)
ok(D6 - C6 == B6 - A6 and D6 - A6 == (B6 - A6) + (C6 - A6), "fig 1096 : ABDC parallélogramme")
ok(not coplanaires(B6 - A6, C6 - A6, E6 - A6), "fig 1096 : E hors de (ABC)")
A9, B9, C9, D9 = V(1, 0, 0), V(2, 1, 0), V(0, 1, 1), V(3, 2, 1)
ok(not coplanaires(B9 - A9, C9 - A9, D9 - A9), "fig 1099 : ABCD tétraèdre")
u1_, v1_, v2_ = V(2, 1, -1), V(1, 1, 0), V(0, 1, 1)
ok(u1_ == 2 * v1_ - v2_, "fig 1100 : u1 = 2 v1 - v2")

if ERREURS:
    print("ÉCARTS :")
    for e in ERREURS:
        print(" -", e)
else:
    print("TOUT EST JUSTE")
