# -*- coding: utf-8 -*-
"""Vérification de tous les résultats de la notion 92 (produit scalaire et orthogonalité).

    python verif_produit_scalaire.py

Chaque contrôle lève une AssertionError en cas d'écart ; sinon « OK » est affiché.
"""
import sympy as sp

V = sp.Matrix
x, t, k, a = sp.symbols("x t k a", real=True)
ok = 0


def egal(u, v, msg):
    global ok
    d = sp.simplify(sp.nsimplify(u) - sp.nsimplify(v)) if not isinstance(u, sp.MatrixBase) else sp.simplify(u - v)
    assert (d == 0 if not isinstance(d, sp.MatrixBase) else d == sp.zeros(*d.shape)), f"{msg} : {u} ≠ {v}"
    ok += 1


def ps(u, v):
    return (u.T * v)[0]


def norme(u):
    return sp.sqrt(ps(u, u))


def det2(u, v):
    return u[0] * v[1] - u[1] * v[0]


def deg(val):
    return float(sp.N(val * 180 / sp.pi))


# ====================================================================== COURS
u, v = V([1, 2, -1]), V([3, -1, 1])
egal(ps(u, v), 0, "cours ex. u.v")
egal(norme(u), sp.sqrt(6), "cours ex. ||u||")
# cube d'arête 1, repère (A ; AB, AD, AE)
A, B, C, D = V([0, 0, 0]), V([1, 0, 0]), V([1, 1, 0]), V([0, 1, 0])
E, F, G, H = V([0, 0, 1]), V([1, 0, 1]), V([1, 1, 1]), V([0, 1, 1])
AG, BD, BE = G - A, D - B, E - B
egal(ps(AG, BD), 0, "AG.BD")
egal(ps(AG, BE), 0, "AG.BE")
assert BD.cross(BE) != sp.zeros(3, 1), "BD, BE non colinéaires"
# angle CAG
cosCAG = ps(C - A, G - A) / (norme(C - A) * norme(G - A))
egal(cosCAG, sp.sqrt(6) / 3, "cos CAG")
assert abs(deg(sp.acos(cosCAG)) - 35.26) < 0.01
# (AE) et (HG) orthogonales non sécantes
egal(ps(E - A, G - H), 0, "AE.HG")
s1, s2 = sp.symbols("s1 s2")
assert sp.solve(list(A + s1 * (E - A) - (H + s2 * (G - H))), [s1, s2]) == []
# plan passant par (1;2;0) de normal (2;-1;3)
n = V([2, -1, 3]); P0 = V([1, 2, 0])
d = -ps(n, P0)
egal(d, 0, "d du plan 2x-y+3z")
# (BDE) : x + y + z - 1 = 0
for P in (B, D, E):
    egal(ps(V([1, 1, 1]), P) - 1, 0, "B, D, E dans x+y+z-1=0")
# projeté de A sur (BDE)
tt = sp.solve(ps(V([1, 1, 1]), A + t * V([1, 1, 1])) - 1, t)[0]
egal(tt, sp.Rational(1, 3), "t projeté")
Hp = A + tt * V([1, 1, 1])
egal(norme(Hp - A), sp.sqrt(3) / 3, "distance A-(BDE)")
# H est le centre de gravité de BDE
egal(Hp, (B + D + E) / 3, "H centre de gravité")
# projeté de M(3;1;4) sur la droite (B'(0;1;1), u(1;2;2))
M = V([3, 1, 4]); B2 = V([0, 1, 1]); ud = V([1, 2, 2])
tt = sp.solve(ps(B2 + t * ud - M, ud), t)[0]
egal(tt, 1, "t projeté droite")
Hd = B2 + tt * ud
egal(Hd, V([1, 3, 3]), "H projeté droite")
egal(norme(Hd - M), 3, "distance M-d")
# plan médiateur : MA² - MB² = 2 IM.BA... identité
Pa, Pb, Pm = V(sp.symbols("a1 a2 a3")), V(sp.symbols("b1 b2 b3")), V(sp.symbols("m1 m2 m3"))
I = (Pa + Pb) / 2
egal(sp.expand(ps(Pa - Pm, Pa - Pm) - ps(Pb - Pm, Pb - Pm)), sp.expand(2 * ps(Pm - I, Pb - Pa)), "plan médiateur")
# démonstration : MQ² = MH² + HQ² quand MH ⟂ HQ
egal(ps(V([0, 0, 2]) + V([3, 1, 0]), V([0, 0, 2]) + V([3, 1, 0])), 4 + 10, "Pythagore")

# ================================================================= EXERCICES
# --- exercices réécrits le 2026-11-02 (géométrie plane de Première → espace) ---
# 974 : pavé 4 × 2 × 3, repère orthonormé (A ; AB/4, AD/2, AE/3)
P4 = {"A": V([0, 0, 0]), "B": V([4, 0, 0]), "D": V([0, 2, 0]), "E": V([0, 0, 3])}
P4["F"] = P4["B"] + P4["E"]; P4["H"] = P4["D"] + P4["E"]
egal(P4["F"], V([4, 0, 3]), "974 F"); egal(P4["H"], V([0, 2, 3]), "974 H")
AF4, AH4 = P4["F"] - P4["A"], P4["H"] - P4["A"]
egal(ps(AF4, AH4), 9, "974 Q2"); egal(norme(AF4), 5, "974 AF"); egal(norme(AH4), sp.sqrt(13), "974 AH")
c4 = ps(AF4, AH4) / (norme(AF4) * norme(AH4)); egal(c4, 9 / (5 * sp.sqrt(13)), "974 cos")
assert abs(float(c4) - 0.4992) < 5e-5 and round(deg(sp.acos(c4)), 1) == 60.1, deg(sp.acos(c4))
egal(ps(P4["E"] - P4["A"], P4["D"] - P4["B"]), 0, "974 AE.BD")
assert sp.solve(list(P4["A"] + s1 * (P4["E"] - P4["A"]) - (P4["B"] + s2 * (P4["D"] - P4["B"]))), [s1, s2]) == [], "974 (AE), (BD) non sécantes"

# 978 : projeté de A(4;3;-1) sur d (B(1;0;2), u(1;2;2))
B78, u78, A78 = V([1, 0, 2]), V([1, 2, 2]), V([4, 3, -1])
egal(norme(u78), 3, "978 ||u||"); egal(ps(A78 - B78, u78), 3, "978 BA.u")
H78 = B78 + t * u78
egal(H78 - A78, V([t - 3, 2 * t - 3, 2 * t + 3]), "978 AH(t)")
egal(sp.expand(ps(H78 - A78, u78)), 9 * t - 3, "978 AH.u")
t78 = sp.solve(ps(H78 - A78, u78), t)[0]; egal(t78, sp.Rational(1, 3), "978 t")
H78 = H78.subs(t, t78); egal(H78, V([sp.Rational(4, 3), sp.Rational(2, 3), sp.Rational(8, 3)]), "978 H")
egal(H78 - A78, V([sp.Rational(-8, 3), sp.Rational(-7, 3), sp.Rational(11, 3)]), "978 AH")
egal(ps(H78 - A78, H78 - A78), 26, "978 AH²"); assert abs(float(sp.sqrt(26)) - 5.10) < 0.005
egal(ps(A78 - B78, A78 - B78), 27, "978 BA²"); egal(norme(H78 - B78), 1, "978 BH")

# 981 : AB = 3, AC = 2, AB.AC = -2 (modèle : A origine, C sur l'axe des abscisses)
A81, C81 = V([0, 0, 0]), V([2, 0, 0])
B81 = V([-1, 2 * sp.sqrt(2), 0])
egal(norme(B81 - A81), 3, "981 AB"); egal(ps(B81 - A81, C81 - A81), -2, "981 AB.AC")
egal(ps(C81 - B81, C81 - B81), 17, "981 BC²"); egal(4 - 2 * (-2) + 9, 17, "981 développement")
c81 = sp.Rational(-2, 6); egal(ps(B81 - A81, C81 - A81) / 6, c81, "981 cos")
assert round(deg(sp.acos(c81)), 1) == 109.5
I81 = (B81 + C81) / 2; egal(norme(I81 - A81), sp.Rational(3, 2), "981 AI")
H81 = V([-1, 0, 0]); egal(ps(B81 - H81, C81 - A81), 0, "981 H projeté")
egal(H81 - A81, sp.Rational(-1, 2) * (C81 - A81), "981 k = -1/2")
egal(norme(B81 - H81), 2 * sp.sqrt(2), "981 BH"); egal(norme(H81 - A81), 1, "981 AH")
egal(norme(C81 - A81) * norme(B81 - H81) / 2, 2 * sp.sqrt(2), "981 aire")
assert abs(float(2 * sp.sqrt(2)) - 2.83) < 0.005 and abs(float(sp.sqrt(17)) - 4.12) < 0.005

# 979 : A(1;0;2), B(3;2;3), C(3;-4;6)
A79, B79, C79 = V([1, 0, 2]), V([3, 2, 3]), V([3, -4, 6])
egal(B79 - A79, V([2, 2, 1]), "979 AB"); egal(C79 - A79, V([2, -4, 4]), "979 AC")
egal(ps(B79 - A79, C79 - A79), 0, "979 Q1")
egal(norme(B79 - A79), 3, "979 AB"); egal(norme(C79 - A79), 6, "979 AC"); egal(norme(C79 - B79), 3 * sp.sqrt(5), "979 BC")
egal(C79 - B79, V([0, -6, 3]), "979 vecteur BC")
egal(norme(B79 - A79) * norme(C79 - A79) / 2, 9, "979 aire")
D79 = C79 + (B79 - A79); egal(D79, V([5, -2, 7]), "979 D")
egal(D79 - A79, V([4, -2, 5]), "979 AD"); egal(ps(D79 - A79, C79 - B79), 27, "979 AD.BC")
egal(norme(C79 - A79) ** 2 - norme(B79 - A79) ** 2, 27, "979 AC² - AB²")

# 1107 (espace)
A7, B7, C7, n7 = V([2, 1, -1]), V([0, 3, 2]), V([-1, 0, 1]), V([7, -5, 8])
egal(B7 - A7, V([-2, 2, 3]), "1107 AB"); egal(C7 - A7, V([-3, -1, 2]), "1107 AC")
egal(ps(n7, B7 - A7), 0, "1107 n.AB"); egal(ps(n7, C7 - A7), 0, "1107 n.AC")
assert (B7 - A7).cross(C7 - A7) != sp.zeros(3, 1)
d7 = -ps(n7, A7); egal(d7, -1, "1107 d")
for P in (A7, B7, C7):
    egal(ps(n7, P) + d7, 0, "1107 équation")
aa, bb, cc = sp.symbols("aa bb cc")
sol = sp.solve([ps(V([aa, bb, cc]), B7 - A7), ps(V([aa, bb, cc]), C7 - A7)], [aa, bb], dict=True)[0]
egal(sol[aa].subs(cc, 8), 7, "1107 système a"); egal(sol[bb].subs(cc, 8), -5, "1107 système b")

# 976 : plan P (A(1;0;1), n(2;-1;2)), B(2;4;2), M(5;1;8)
A76, n76, B76, M76 = V([1, 0, 1]), V([2, -1, 2]), V([2, 4, 2]), V([5, 1, 8])
egal(ps(B76 - A76, n76), 0, "976 B dans P")
H76 = M76 + t * n76; egal(H76, V([5 + 2 * t, 1 - t, 8 + 2 * t]), "976 H(t)")
egal(sp.expand(ps(H76 - A76, n76)), 21 + 9 * t, "976 AH.n")
t76 = sp.solve(ps(H76 - A76, n76), t)[0]; egal(t76, sp.Rational(-7, 3), "976 t")
H76 = H76.subs(t, t76); egal(H76, V([sp.Rational(1, 3), sp.Rational(10, 3), sp.Rational(10, 3)]), "976 H")
egal(norme(M76 - H76), 7, "976 MH"); egal(norme(n76), 3, "976 ||n||")
egal(B76 - M76, V([-3, 3, -6]), "976 MB"); egal(ps(B76 - M76, B76 - M76), 54, "976 MB²")
egal(norme(B76 - M76), 3 * sp.sqrt(6), "976 MB"); assert abs(float(3 * sp.sqrt(6)) - 7.35) < 0.005
egal(B76 - H76, V([sp.Rational(5, 3), sp.Rational(2, 3), sp.Rational(-4, 3)]), "976 HB")
egal(ps(B76 - H76, B76 - H76), 5, "976 HB²"); egal(ps(M76 - H76, B76 - H76), 0, "976 MHB rectangle")
for P in (A76, B76, H76):
    egal(2 * P[0] - P[1] + 2 * P[2] - 4, 0, "976 équation 2x - y + 2z - 4 = 0")

# 975 : u(1;2;-2), v(2;1;2), w(1;0;1)
u75, v75, w75 = V([1, 2, -2]), V([2, 1, 2]), V([1, 0, 1])
egal(ps(u75, v75), 0, "975 Q1")
c75 = ps(u75, w75) / (norme(u75) * norme(w75)); egal(c75, -sp.sqrt(2) / 6, "975 cos")
assert abs(float(c75) + 0.236) < 5e-4 and round(deg(sp.acos(c75)), 1) == 103.6
egal(sp.solve(ps(V([k, 1, 2]), V([3, -k, 1])), k)[0], -1, "975 Q3")
egal(ps(V([-1, 1, 2]), V([3, 1, 1])), 0, "975 Q3 vérification")
aa75, bb75 = sp.symbols("aa75 bb75")
s75 = sp.solve([ps(V([aa75, bb75, 1]), u75), ps(V([aa75, bb75, 1]), v75)], [aa75, bb75], dict=True)[0]
n75 = V([s75[aa75], s75[bb75], 1]); egal(n75, V([-2, 2, 1]), "975 n")
egal(ps(n75, V([0, 0, 0])), 0, "975 P passe par O")
assert n75.cross(w75) != sp.zeros(3, 1), "975 w non colinéaire à n"
egal(ps(w75, v75), 4, "975 w.v")

# 982 : plan médiateur de [AB], A(1;-1;2), B(3;3;0)
A82, B82 = V([1, -1, 2]), V([3, 3, 0])
I82 = (A82 + B82) / 2; egal(I82, V([2, 1, 1]), "982 I"); egal(B82 - A82, V([2, 4, -2]), "982 AB")
X82 = V(sp.symbols("x82 y82 z82"))
egal(sp.expand(ps(X82 - I82, B82 - A82)), sp.expand(2 * (X82[0] + 2 * X82[1] - X82[2] - 3)), "982 équation")
egal(sp.expand(ps(X82 - A82, X82 - A82) - ps(X82 - B82, X82 - B82)), sp.expand(2 * ps(X82 - I82, B82 - A82)), "982 MA² - MB²")
C82 = V([4, 0, 1]); egal(C82[0] + 2 * C82[1] - C82[2] - 3, 0, "982 C dans P")
egal(ps(A82 - C82, A82 - C82), 11, "982 CA²"); egal(ps(B82 - C82, B82 - C82), 11, "982 CB²")
D82 = V([0, 0, -3]); egal(D82[0] + 2 * D82[1] - D82[2] - 3, 0, "982 D dans P")
egal(norme(A82 - D82), 3 * sp.sqrt(3), "982 DA"); egal(norme(B82 - D82), 3 * sp.sqrt(3), "982 DB")
egal(ps(A82 - D82, B82 - D82), 15, "982 DA.DB")
c82 = ps(A82 - D82, B82 - D82) / 27; egal(c82, sp.Rational(5, 9), "982 cos")
assert round(deg(sp.acos(c82)), 1) == 56.3
egal(I82 - D82, V([2, 1, 4]), "982 DI"); egal(norme(I82 - D82), sp.sqrt(21), "982 |DI|")
egal(ps(I82 - D82, B82 - A82), 0, "982 DI ⟂ AB"); egal(norme(B82 - A82), 2 * sp.sqrt(6), "982 AB")
egal(norme(B82 - A82) * norme(I82 - D82) / 2, 3 * sp.sqrt(14), "982 aire")
egal(sp.sqrt(126), 3 * sp.sqrt(14), "982 racine"); assert abs(float(3 * sp.sqrt(14)) - 11.22) < 0.005

# 1105 (cube)
egal(ps(C - A, G - A), 2, "1105 AC.AG"); egal(norme(C - A) ** 2, 2, "1105 AC²")
egal(ps(C - A, E - A), 0, "1105 AC.AE")
egal(ps(G - C, C - A), 0, "1105 C projeté de G sur (AC)")

# 1106 (tétraèdre régulier d'arête a)
s3, s6 = sp.sqrt(3), sp.sqrt(6)
TA, TB, TC = V([0, 0, 0]), V([a, 0, 0]), V([a / 2, a * s3 / 2, 0])
TD = V([a / 2, a * s3 / 6, a * s6 / 3])
for P, Q in ((TA, TB), (TA, TC), (TA, TD), (TB, TC), (TB, TD), (TC, TD)):
    egal(sp.simplify(norme(Q - P) - a).subs(a, 1), 0, "1106 arêtes")
TI, TJ, TK = (TA + TB) / 2, (TA + TC) / 2, (TA + TD) / 2
egal(sp.simplify(ps(TB - TA, TC - TA)), a ** 2 / 2, "1106 Q1")
egal(sp.simplify(ps(TI - TB, TJ - TA)), -a ** 2 / 8, "1106 Q2")
egal(sp.simplify(ps(TJ - TI, TD - TA)), 0, "1106 Q3")
egal(sp.simplify(ps(TC - TB, TD - TA)), 0, "1106 BC.AD")
egal(sp.simplify(ps(TK - TI, TK - TJ)), a ** 2 / 8, "1106 Q4")
# (IJ) et (AD) non coplanaires (donc orthogonales, pas perpendiculaires)
assert sp.simplify((TJ - TI).cross(TD - TA).dot(TA - TI)) != 0, "1106 (IJ),(AD) non coplanaires"

# 1108 (tétraèdre trirectangle)
O8, A8b, B8b, C8b = V([0, 0, 0]), V([1, 0, 0]), V([0, 1, 0]), V([0, 0, 1])
M8 = B8b + x * (C8b - B8b); egal(M8, V([0, 1 - x, x]), "1108 Q1")
MA, MO, MB = A8b - M8, O8 - M8, B8b - M8
egal(MA, V([1, x - 1, -x]), "1108 MA"); egal(MO, V([0, x - 1, -x]), "1108 MO")
egal(sp.expand(ps(MA, MO)), 2 * x ** 2 - 2 * x + 1, "1108 MA.MO")
egal(sp.expand(ps(MA, MA)), 2 * x ** 2 - 2 * x + 2, "1108 MA²")
egal(sp.expand(ps(MO, MO)), 2 * x ** 2 - 2 * x + 1, "1108 MO²")
f = (2 * x ** 2 - 2 * x + 1) / (2 * x ** 2 - 2 * x + 2)
egal(sp.simplify(ps(MA, MO) ** 2 / (ps(MA, MA) * ps(MO, MO)) - f), 0, "1108 cos²")
assert sp.discriminant(2 * x ** 2 - 2 * x + 1, x) == -4  # MA.MO > 0 : angle aigu
egal(f.subs(x, 0), sp.Rational(1, 2), "1108 f(0)"); egal(f.subs(x, 1), sp.Rational(1, 2), "1108 f(1)")
egal(f.subs(x, sp.Rational(1, 2)), sp.Rational(1, 3), "1108 f(1/2)")
egal(sp.simplify(sp.diff(f, x) - (4 * x - 2) / (2 * x ** 2 - 2 * x + 2) ** 2), 0, "1108 f'")
th = sp.acos(sp.sqrt(sp.Rational(1, 3)))
egal(sp.cos(th), sp.sqrt(3) / 3, "1108 cos θmax")
assert abs(deg(th) - 54.74) < 0.005 and abs(float(th) - 0.955) < 0.0005
egal(sp.acos(sp.sqrt(sp.Rational(1, 2))), sp.pi / 4, "1108 θ(0)")
egal(sp.factor(ps(MA, MB)), x * (2 * x - 1), "1108 Q5")
egal(M8.subs(x, sp.Rational(1, 2)), (B8b + C8b) / 2, "1108 M milieu de [BC]")
# θ(x) est bien maximal en 1/2 (contrôle numérique)
import numpy as np
xx = np.linspace(0, 1, 2001)
thx = np.degrees(np.arccos(np.sqrt((2 * xx ** 2 - 2 * xx + 1) / (2 * xx ** 2 - 2 * xx + 2))))
assert abs(xx[thx.argmax()] - 0.5) < 1e-9 and abs(thx.max() - 54.7356) < 1e-3 and abs(thx[0] - 45) < 1e-9

print(f"OK : {ok} égalités vérifiées, toutes les assertions passent.")
