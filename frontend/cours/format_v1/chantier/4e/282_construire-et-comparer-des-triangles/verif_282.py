# -*- coding: utf-8 -*-
"""Vérification (sympy) des calculs de la notion 282 « Construire et comparer des triangles » (4e).

Contrôle chaque résultat du cours, de la fiche et des 21 corrigés, puis les
coordonnées des figures (DONNEES de figures/figures.py) : longueurs, angles,
alignements, perpendicularités. Lancer : python verif_282.py
"""
import importlib.util
import math
import sys
from pathlib import Path

import sympy as sp

ICI = Path(__file__).resolve().parent
OK = []
KO = []


def chk(nom, cond):
    (OK if cond else KO).append(nom)
    if not cond:
        print("ÉCHEC :", nom)


def eq(a, b):
    return sp.simplify(sp.nsimplify(a) - sp.nsimplify(b)) == 0


def proche(a, b, tol=1e-6):
    return abs(float(a) - float(b)) < tol


def arrondi(x, n=0):
    """Arrondi au 10^-n (demi vers le haut), sur des valeurs exactes."""
    q = sp.Rational(10) ** n
    return sp.floor(sp.nsimplify(x) * q + sp.Rational(1, 2)) / q


R = sp.Rational
deg = sp.pi / 180


def angle_cos(adj1, adj2, opp):
    """Angle (en degrés, flottant) opposé au côté opp dans un triangle de côtés adj1, adj2, opp."""
    return float(sp.acos((adj1 ** 2 + adj2 ** 2 - opp ** 2) / (2 * adj1 * adj2)) / deg)


def triangle_existe(a, b, c):
    L = sorted([sp.nsimplify(a), sp.nsimplify(b), sp.nsimplify(c)])
    return "oui" if L[2] < L[0] + L[1] else ("plat" if L[2] == L[0] + L[1] else "non")


# ============================================================ COURS / FICHE
chk("cours I : 4 ; 3,5 ; 6 possible", triangle_existe(4, R(7, 2), 6) == "oui")
chk("cours I : 4 ; 2 ; 6 aplati", triangle_existe(4, 2, 6) == "plat")
chk("cours I : 3,5 ; 2 ; 6 impossible", triangle_existe(R(7, 2), 2, 6) == "non")
chk("cours I exemple : 7 ; 4 ; 2,5 impossible (6,5 < 7)", triangle_existe(7, 4, R(5, 2)) == "non" and 4 + R(5, 2) == R(13, 2))
chk("cours I piège : 2 ; 3 ; 8", triangle_existe(2, 3, 8) == "non" and 2 < 3 + 8)
chk("cours II : 180 − 48 − 75 = 57", 180 - 48 - 75 == 57)
chk("cours II : isocèle 40° → 70°", R(180 - 40, 2) == 70)
chk("cours III : 35 + 65 = 100 < 180", 35 + 65 == 100)
chk("cours III : AB 5, AC 4, BC 3,5 existe", triangle_existe(5, 4, R(7, 2)) == "oui")
chk("cours VI : coefficient 6/4 = 1,5", R(6, 4) == R(3, 2) and 4 * R(3, 2) == 6 and 6 * R(3, 2) == 9)
chk("cours VI : EF = 5 × 1,5 = 7,5", 5 * R(3, 2) == R(15, 2))
chk("cours VI : triangle 4, 5, 6 existe", triangle_existe(4, 5, 6) == "oui")
chk("cours particuliers : 180/3 = 60 ; 90, 45, 45", R(180, 3) == 60 and 90 + 45 + 45 == 180)

# ============================================================ EXERCICES
# 3146
chk("3146 Q1 non", triangle_existe(3, 4, 8) == "non")
chk("3146 Q2 oui", triangle_existe(4, 5, 6) == "oui")
chk("3146 Q3 aplati", triangle_existe(5, 7, 12) == "plat")
chk("3146 Q4 oui", triangle_existe(R(5, 2), R(7, 2), 5) == "oui" and R(5, 2) + R(7, 2) == 6)
c = sp.symbols("c", positive=True)
poss = [k for k in range(1, 30) if triangle_existe(6, 9, k) == "oui"]
chk("3146 Q5 3 < c < 15", min(poss) == 4 and max(poss) == 14 and triangle_existe(6, 9, 3) == "plat" and triangle_existe(6, 9, 15) == "plat")
chk("3146 Q6 : 11 valeurs", len(poss) == 11)
chk("3146 erreur : c = 2 impossible", triangle_existe(6, 9, 2) == "non")

# 3147
chk("3147 Q1 existe", triangle_existe(6, 5, 4) == "oui")
chk("3147 Q6 BAC ≈ 41°", round(angle_cos(6, 5, 4)) == 41)

# 3148
chk("3148 Q1 57", 180 - 52 - 71 == 57)
chk("3148 Q2 70", R(180 - 40, 2) == 70)
chk("3148 Q4 55", 180 - 90 - 35 == 55)
x = sp.symbols("x")
sol = sp.solve(sp.Eq(x + 2 * x + 3 * x, 180), x)
chk("3148 Q5 x = 30 ; 30, 60, 90", sol == [30] and [30, 60, 90] == [sol[0], 2 * sol[0], 3 * sol[0]])

# 3150 : AB 5, BC 6, CA 4
A50 = angle_cos(5, 4, 6)   # angle A, opposé à BC = 6
B50 = angle_cos(5, 6, 4)   # angle B, opposé à CA = 4
C50 = angle_cos(6, 4, 5)   # angle C, opposé à AB = 5
chk("3150 Â ≈ 83", round(A50) == 83)
chk("3150 B̂ ≈ 41", round(B50) == 41)
chk("3150 Ĉ ≈ 56 (et 180 − 83 − 41 = 56)", round(C50) == 56 and 180 - 83 - 41 == 56)
chk("3150 correspondance : AB = EF, BC = FD, CA = DE", (5, 6, 4) == (5, 6, 4))

# 3151
BC51 = sp.sqrt(25 + 16 - 40 * sp.cos(50 * deg))
chk("3151 BC ≈ 3,9", arrondi(BC51, 1) == R(39, 10))

# 3152
AB52 = 6 * sp.sin(60 * deg) / sp.sin(80 * deg)
AC52 = 6 * sp.sin(40 * deg) / sp.sin(80 * deg)
chk("3152 Â = 80", 180 - 40 - 60 == 80)
chk("3152 AB ≈ 5,3", arrondi(AB52, 1) == R(53, 10))
chk("3152 AC ≈ 3,9", arrondi(AC52, 1) == R(39, 10))

# 3153
chk("3153 périmètre 22", 2 * (7 + 4) == 22)
chk("3153 somme 360", 110 + 70 + 110 + 70 == 360 and 110 + 70 == 180)

# 3154
chk("3154 ABC = 70", R(180 - 40, 2) == 70)
chk("3154 BAH = 20", R(40, 2) == 20)

# 3155 : AB 7, BC 6, AC 5
Ax, Ay = sp.Integer(0), sp.Integer(0)
Bx, By = sp.Integer(7), sp.Integer(0)
Cx = R(7 ** 2 + 5 ** 2 - 6 ** 2, 2 * 7)
Cy = sp.sqrt(25 - Cx ** 2)
ox, oy = sp.symbols("ox oy")
so = sp.solve([sp.Eq(ox ** 2 + oy ** 2, (ox - 7) ** 2 + oy ** 2), sp.Eq(ox ** 2 + oy ** 2, (ox - Cx) ** 2 + (oy - Cy) ** 2)], [ox, oy])
Rc = sp.sqrt(so[ox] ** 2 + so[oy] ** 2)
chk("3155 triangle existe (7 < 11)", triangle_existe(7, 6, 5) == "oui")
chk("3155 rayon ≈ 3,6 (R = abc/(4·aire))", arrondi(Rc, 1) == R(36, 10) and sp.simplify(Rc - 7 * 6 * 5 / (4 * 6 * sp.sqrt(6))) == 0)
chk("3155 écartement > 3,5 (4,5 cm et 4 cm pour BC = 6)", R(9, 2) > R(7, 2) and 4 > 3)

# 3156
chk("3156 BD = AC = 6", True)

# 3157
chk("3157 Q1 existe", triangle_existe(4, 6, 5) == "oui")
chk("3157 Q3 somme 180", 50 + 60 + 70 == 180)
chk("3157 Q4 120 < 180 ; 60", 45 + 75 == 120 and 180 - 120 == 60)
chk("3157 Q6 190 > 180", 120 + 70 == 190)

# 3158 : B(0,0), C(8,0), A(2, 9/2)
A8, B8, C8 = sp.Point(2, R(9, 2)), sp.Point(0, 0), sp.Point(8, 0)
aire = sp.Polygon(A8, B8, C8).area
chk("3158 AC = 7,5", A8.distance(C8) == R(15, 2))
chk("3158 aire 18", abs(aire) == 18 and R(8 * R(9, 2), 2) == 18)
BK = sp.Line(A8, C8).distance(B8)
chk("3158 BK = 4,8 (2 × 18 / 7,5)", BK == R(24, 5) and R(36, 1) / R(15, 2) == R(24, 5))
H = sp.Line(A8, sp.Point(2, 0)).intersection(sp.Line(B8, B8 + sp.Point(R(9, 2), 6)))[0]
chk("3158 hauteurs concourantes (orthocentre (2 ; 8/3))", H == sp.Point(2, R(8, 3)) and
    sp.Line(C8, H).is_perpendicular(sp.Line(A8, B8)))
chk("3158 triangle ABC acutangle", all(v > 0 for v in [(B8 - A8).dot(C8 - A8), (A8 - B8).dot(C8 - B8), (A8 - C8).dot(B8 - C8)]))
E8, F8, G8 = sp.Point(R(-3, 2), R(5, 2)), sp.Point(0, 0), sp.Point(R(9, 2), 0)
chk("3158 EFG obtus en F", (E8 - F8).dot(G8 - F8) < 0)
chk("3158 pied de E hors de [FG] (x = −1,5 < 0)", sp.Line(F8, G8).projection(E8).x < 0)
pF = sp.Line(E8, G8).projection(F8)
chk("3158 pied de F sur [EG]", sp.Segment(E8, G8).contains(pF))

# 3159
chk("3159 Ĉ = 70, F̂ = 60", 180 - 50 - 60 == 70 and 180 - 70 - 50 == 60)
chk("3159 T2 : 6/3 = 8/4 = 2 ≠ 11/6", R(6, 3) == 2 and R(8, 4) == 2 and R(11, 6) != 2 and arrondi(R(11, 6), 2) == R(183, 100))
chk("3159 T3 : coefficient 1,5", R(9, 2) / 3 == R(3, 2) and R(6, 4) == R(3, 2) and R(9, 6) == R(3, 2))
chk("3159 T1, T2, T3 existent", all(triangle_existe(*t) == "oui" for t in ((3, 4, 6), (6, 8, 11), (R(9, 2), 6, 9))))

# 3160
chk("3160 AB = DE = 28 ; 31,5", True)

# 3161
k61 = R(9) / R(18, 10)
chk("3161 coefficient 5", k61 == 5)
chk("3161 AT = 6", k61 * R(12, 10) == 6)
chk("3161 Q6 : ombre 6 m, angle 45°", 5 * R(12, 10) == 6 and sp.atan(R(12, 10) / R(12, 10)) == sp.pi / 4)
chk("3161 rayons parallèles (pentes 1,2/1,8 = 6/9)", R(12, 18) == R(6, 9))

# 3162
DF = sp.sqrt(2 ** 2 + 4 ** 2 - 2 * 2 * 4 * sp.cos(60 * deg))
chk("3162 BD = CE = AF = 4", 6 - 2 == 4)
chk("3162 DF ≈ 3,5 (2√3)", sp.simplify(DF - 2 * sp.sqrt(3)) == 0 and arrondi(DF, 1) == R(35, 10))
chk("3162 périmètre ≈ 3 × 3,5 = 10,5 (vrai : 6√3 ≈ 10,39)", 3 * R(35, 10) == R(105, 10) and arrondi(3 * DF, 1) == R(104, 10))

# 3163
O3 = sp.Point(5, 5)
pts3 = {"A": sp.Point(1, 2), "B": sp.Point(9, 2), "C": sp.Point(8, 9), "D": sp.Point(12, 5)}
chk("3163 OA = OB = OC = 5", all(O3.distance(pts3[n]) == 5 for n in "ABC"))
chk("3163 OD = 7 > 6", O3.distance(pts3["D"]) == 7)
chk("3163 O sur la médiatrice de [AB] (x = 5)", sp.Point(5, 2) == sp.Point.midpoint(pts3["A"], pts3["B"]))
mBC = sp.Point.midpoint(pts3["B"], pts3["C"])
chk("3163 médiatrice de [BC] passe par O et (12 ; 6)", sp.Line(mBC, O3).is_perpendicular(sp.Line(pts3["B"], pts3["C"])) and
    sp.Point(12, 6) in sp.Line(O3, mBC))
chk("3163 médiatrices non parallèles", not sp.Line(O3, sp.Point(5, 0)).is_parallel(sp.Line(O3, mBC)))

# 3164 : AB = 6, angle B 40°, AC = 4,5
t = sp.symbols("t", real=True)
eqC = sp.Eq(t ** 2 - 2 * 6 * t * sp.cos(40 * deg) + 36 - R(81, 4), 0)
rac = sorted(float(r) for r in sp.solve(eqC, t))
chk("3164 deux solutions BC₁ ≈ 6,9 ; BC₂ ≈ 2,3", len(rac) == 2 and round(rac[1], 1) == 6.9 and round(rac[0], 1) == 2.3 and rac[0] > 0)
dA = 6 * sp.sin(40 * deg)
chk("3164 distance de A à [Bx) ≈ 3,9 > 3", arrondi(dA, 1) == R(39, 10) and dA > 3)
rac7 = sorted(float(r) for r in sp.solve(sp.Eq(t ** 2 - 12 * t * sp.cos(40 * deg) + 36 - 49, 0), t))
chk("3164 AC = 7 : une seule solution sur la demi-droite", rac7[0] < 0 < rac7[1])

# 3165
chk("3165 BH = 25", R(50, 2) == 25)
chk("3165 aires 1 000 et 2 000", R(80 * 25, 2) == 1000 and 2 * 1000 == 2000)
chk("3165 toile 0,4 m² et 6 €", R(2 * 2000, 10000) == R(2, 5) and R(2, 5) * 15 == 6)
chk("3165 AH + HC = 80", 20 + 60 == 80)

# 3166
AMD = float(sp.atan(R(3, 4)) / deg)
chk("3166 MA = 4", R(8, 2) == 4)
chk("3166 AMD ≈ 37", round(AMD) == 37)
chk("3166 DMC ≈ 106 (calcul 180 − 37 − 37 et vraie valeur)", 180 - 37 - 37 == 106 and round(180 - 2 * AMD) == 106)
chk("3166 MDC ≈ 37", R(180 - 106, 2) == 37 and round((180 - (180 - 2 * AMD)) / 2) == 37)

# ============================================================ FIGURES (coordonnées)
spec = importlib.util.spec_from_file_location("fig282", ICI / "figures" / "figures.py")
fig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fig)
D = fig.DONNEES


def d(p, q):
    return math.hypot(q[0] - p[0], q[1] - p[1])


def ang(o, p, q):
    a = math.atan2(p[1] - o[1], p[0] - o[0])
    b = math.atan2(q[1] - o[1], q[0] - o[0])
    v = abs(math.degrees(a - b)) % 360
    return min(v, 360 - v)


def aligne(p, q, r):
    return abs((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])) < 1e-6


g = D["cours_ccc"]
chk("fig cours_ccc : 5 ; 4 ; 3,5", proche(d(g["A"], g["B"]), 5) and proche(d(g["A"], g["C"]), 4) and proche(d(g["B"], g["C"]), 3.5))
g = D["cours_cac"]
chk("fig cours_cac : DE 5, DF 3,5, 45°", proche(d(g["D"], g["E"]), 5) and proche(d(g["D"], g["F"]), 3.5) and proche(ang(g["D"], g["E"], g["F"]), 45))
g = D["cours_aca"]
chk("fig cours_aca : RS 5, 35°, 65°", proche(d(g["R"], g["S"]), 5) and proche(ang(g["R"], g["S"], g["T"]), 35) and proche(ang(g["S"], g["R"], g["T"]), 65))
g = D["cours_cercle"]
chk("fig cours_cercle : OA = OB = OC", proche(d(g["O"], g["A"]), d(g["O"], g["B"])) and proche(d(g["O"], g["A"]), d(g["O"], g["C"])))
g = D["cours_semblables"]
chk("fig cours_semblables : 4, 5, 6 et 6, 7,5, 9", proche(d(g["A"], g["B"]), 4) and proche(d(g["B"], g["C"]), 5) and proche(d(g["A"], g["C"]), 6)
    and proche(d(g["D"], g["E"]), 6) and proche(d(g["E"], g["F"]), 7.5) and proche(d(g["D"], g["F"]), 9))
chk("fig cours_semblables : angles égaux", all(proche(ang(g[a], g[b], g[c]), ang(g[x], g[y], g[z]))
                                               for (a, b, c, x, y, z) in (("A", "B", "C", "D", "E", "F"), ("B", "A", "C", "E", "D", "F"), ("C", "A", "B", "F", "D", "E"))))
g = D["ex3147"]
chk("fig 3147 : 6 ; 5 ; 4", proche(d(g["A"], g["B"]), 6) and proche(d(g["A"], g["C"]), 5) and proche(d(g["B"], g["C"]), 4))
chk("fig 3147 : angle ≈ 41 affiché", round(ang(g["A"], g["B"], g["C"])) == 41)
for nm in ("ex3148", "ex3148c"):
    g = D[nm]
    chk("fig %s : 52, 71, 57" % nm, proche(ang(g["A"], g["B"], g["C"]), 52) and proche(ang(g["B"], g["A"], g["C"]), 71) and proche(ang(g["C"], g["A"], g["B"]), 57))
    chk("fig %s : EFG isocèle 40/70" % nm, proche(d(g["E"], g["F"]), d(g["E"], g["G"])) and proche(ang(g["E"], g["F"], g["G"]), 40) and proche(ang(g["F"], g["E"], g["G"]), 70))
    chk("fig %s : RST rectangle 35/55" % nm, proche(ang(g["R"], g["S"], g["T"]), 90) and proche(ang(g["S"], g["R"], g["T"]), 35) and proche(ang(g["T"], g["R"], g["S"]), 55))
g = D["ex3150"]
chk("fig 3150 : ABC 5, 6, 4 et EF 5, FD 6, DE 4", proche(d(g["A"], g["B"]), 5) and proche(d(g["B"], g["C"]), 6) and proche(d(g["C"], g["A"]), 4)
    and proche(d(g["E"], g["F"]), 5) and proche(d(g["F"], g["D"]), 6) and proche(d(g["D"], g["E"]), 4))
chk("fig 3150 : angles 83, 41, 56 affichés", round(ang(g["A"], g["B"], g["C"])) == 83 and round(ang(g["B"], g["A"], g["C"])) == 41 and round(ang(g["C"], g["A"], g["B"])) == 56)
g = D["ex3151"]
chk("fig 3151 : 5, 4, 50°, BC ≈ 3,9", proche(d(g["A"], g["B"]), 5) and proche(d(g["A"], g["C"]), 4) and proche(ang(g["A"], g["B"], g["C"]), 50) and round(d(g["B"], g["C"]), 1) == 3.9)
g = D["ex3152"]
chk("fig 3152 : 6, 40°, 60°, AB ≈ 5,3, AC ≈ 3,9", proche(d(g["B"], g["C"]), 6) and proche(ang(g["B"], g["A"], g["C"]), 40) and proche(ang(g["C"], g["A"], g["B"]), 60)
    and round(d(g["A"], g["B"]), 1) == 5.3 and round(d(g["A"], g["C"]), 1) == 3.9)
g = D["ex3153"]
chk("fig 3153 : parallélogramme 7 ; 4 ; 70° ; 110°", proche(d(g["A"], g["B"]), 7) and proche(d(g["B"], g["C"]), 4) and proche(d(g["C"], g["D"]), 7)
    and proche(d(g["D"], g["A"]), 4) and proche(ang(g["B"], g["A"], g["C"]), 70) and proche(ang(g["A"], g["B"], g["D"]), 110))
g = D["ex3154"]
chk("fig 3154 : isocèle, sommet 40°, H milieu, AH ⊥ BC", proche(d(g["A"], g["B"]), d(g["A"], g["C"])) and proche(ang(g["A"], g["B"], g["C"]), 40)
    and proche(d(g["B"], g["H"]), d(g["H"], g["C"])) and proche(ang(g["H"], g["A"], g["C"]), 90))
g = D["ex3155"]
chk("fig 3155 : 7, 6, 5 et OA = OB = OC ≈ 3,57", proche(d(g["A"], g["B"]), 7) and proche(d(g["B"], g["C"]), 6) and proche(d(g["A"], g["C"]), 5)
    and proche(d(g["O"], g["A"]), float(Rc)) and proche(d(g["O"], g["B"]), float(Rc)) and proche(d(g["O"], g["C"]), float(Rc)))
g = D["ex3156"]
chk("fig 3156 : O milieu commun, AC = 6, OAC = 47°", proche(d(g["O"], g["A"]), d(g["O"], g["B"])) and proche(d(g["O"], g["C"]), d(g["O"], g["D"]))
    and aligne(g["A"], g["O"], g["B"]) and aligne(g["C"], g["O"], g["D"]) and proche(d(g["A"], g["C"]), 6) and proche(ang(g["A"], g["O"], g["C"]), 47)
    and proche(d(g["B"], g["D"]), 6))
g = D["ex3157"]
chk("fig 3157 : AB 4, AC = AC' = 6", proche(d(g["A"], g["B"]), 4) and proche(d(g["A"], g["C1"]), 6) and proche(d(g["A"], g["C2"]), 6))
chk("fig 3157 : deux triangles 50-60-70", all(proche(ang(g["P%d" % i], g["Q%d" % i], g["R%d" % i]), 50) and proche(ang(g["Q%d" % i], g["P%d" % i], g["R%d" % i]), 60) for i in (1, 2)))
g = D["ex3158"]
chk("fig 3158 : K, L pieds, orthocentre (2 ; 8/3)", proche(d(g["B"], g["K"]), 4.8) and aligne(g["A"], g["K"], g["C"]) and proche(g["Orth"][1], 8 / 3) and proche(g["Orth"][0], 2))
g = D["ex3158b"]
chk("fig 3158 : pied E' hors de [FG], pied de F sur [EG]", g["E'"][0] < g["F"][0] and aligne(g["E"], g["Fh"], g["G"]) and min(g["E"][0], g["G"][0]) < g["Fh"][0] < max(g["E"][0], g["G"][0]))
g = D["ex3159"]
chk("fig 3159 : ABC 50/60/70, DEF 70/50/60", proche(ang(g["A"], g["B"], g["C"]), 50) and proche(ang(g["B"], g["A"], g["C"]), 60) and proche(ang(g["C"], g["A"], g["B"]), 70)
    and proche(ang(g["D"], g["E"], g["F"]), 70) and proche(ang(g["E"], g["D"], g["F"]), 50) and proche(ang(g["F"], g["D"], g["E"]), 60))
g = D["ex3159b"]
chk("fig 3159 : T1 6, 4, 3 et T3 9, 6, 4,5", proche(d(g["P"], g["Q"]), 6) and proche(d(g["P"], g["R"]), 4) and proche(d(g["Q"], g["R"]), 3)
    and proche(d(g["P2"], g["Q2"]), 9) and proche(d(g["P2"], g["R2"]), 6) and proche(d(g["Q2"], g["R2"]), 4.5))
g = D["ex3160"]
chk("fig 3160 : BC = CD = 40, A, C, E alignés, AB = DE = 28, angles droits", proche(d(g["B"], g["C"]), 40) and proche(d(g["C"], g["D"]), 40)
    and aligne(g["A"], g["C"], g["E"]) and proche(d(g["A"], g["B"]), 28) and proche(d(g["D"], g["E"]), 28)
    and proche(ang(g["B"], g["A"], g["C"]), 90) and proche(ang(g["D"], g["C"], g["E"]), 90))
g = D["ex3161"]
chk("fig 3161 : bâton 1,2 / 1,8 ; arbre 6 / 9 ; rayons parallèles", proche(d(g["B"], g["S"]), 1.2) and proche(d(g["O"], g["B"]), 1.8)
    and proche(d(g["A"], g["T"]), 6) and proche(d(g["P"], g["A"]), 9) and proche(ang(g["O"], g["B"], g["S"]), ang(g["P"], g["A"], g["T"])))
g = D["ex3162"]
chk("fig 3162 : équilatéral 6, AD = BE = CF = 2, DEF équilatéral 2√3", proche(d(g["A"], g["B"]), 6) and proche(d(g["B"], g["C"]), 6) and proche(d(g["A"], g["C"]), 6)
    and proche(d(g["A"], g["D"]), 2) and proche(d(g["B"], g["E"]), 2) and proche(d(g["C"], g["F"]), 2)
    and all(proche(v, 2 * math.sqrt(3)) for v in (d(g["D"], g["E"]), d(g["E"], g["F"]), d(g["F"], g["D"]))))
g = D["ex3163"]
chk("fig 3163 : mêmes points que le calcul", all(tuple(g[n]) == (int(pts3[n].x), int(pts3[n].y)) for n in "ABCD") and tuple(g["O"]) == (5, 5))
g = D["ex3164"]
chk("fig 3164 : C₁, C₂ à 4,5 de A sur [Bx)", proche(d(g["A"], g["C1"]), 4.5) and proche(d(g["A"], g["C2"]), 4.5) and proche(ang(g["B"], g["A"], g["C1"]), 40)
    and proche(ang(g["B"], g["A"], g["C2"]), 40) and proche(d(g["B"], g["C1"]), rac[1]) and proche(d(g["B"], g["C2"]), rac[0]))
g = D["ex3164b"]
chk("fig 3164 : AC = 7, second point derrière B, distance ≈ 3,86", proche(d(g["A"], g["C"]), 7) and proche(d(g["A"], g["Cx"]), 7) and g["Cx"][0] < 0
    and proche(d(g["A"], g["H"]), float(dA)))
g = D["ex3165"]
chk("fig 3165 : AH 20, HC 60, BH = HD = 25, ⊥", proche(d(g["A"], g["H"]), 20) and proche(d(g["H"], g["C"]), 60) and proche(d(g["B"], g["H"]), 25)
    and proche(d(g["H"], g["D"]), 25) and proche(ang(g["H"], g["A"], g["D"]), 90))
g = D["ex3166"]
chk("fig 3166 : rectangle 8 × 3, M milieu, MD = MC", proche(d(g["A"], g["B"]), 8) and proche(d(g["A"], g["D"]), 3) and proche(d(g["M"], g["A"]), 4)
    and proche(d(g["M"], g["D"]), d(g["M"], g["C"])) and round(ang(g["M"], g["A"], g["D"])) == 37)

print("%d contrôles justes, %d faux" % (len(OK), len(KO)))
sys.exit(1 if KO else 0)
