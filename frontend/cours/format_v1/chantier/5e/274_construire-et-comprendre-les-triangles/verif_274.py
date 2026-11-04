# -*- coding: utf-8 -*-
"""Vérification exacte (sympy) de la notion 274 (5e) : Construire et comprendre les triangles.

    python verif_274.py

Contrôle chaque résultat du cours, de la fiche et des 10 exercices, les valeurs
arrondies annoncées, les coordonnées des figures (figures/figures.py, DONNEES),
puis la structure (questions = étapes = solutions, images appelées = déclarées,
10 gardés + 11 retirés = 21 Id en ligne, aucune mention du brevet).
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

import sympy as sp

ICI = Path(__file__).resolve().parent
OK, KO = [], []


def ctrl(nom, cond):
    (OK if bool(cond) else KO).append(nom)


R = sp.Rational
deg = sp.pi / 180


def angle_deg(o, p, q):
    """Angle saillant en o (degrés, flottant) entre o→p et o→q."""
    u = sp.Matrix([p[0] - o[0], p[1] - o[1]])
    v = sp.Matrix([q[0] - o[0], q[1] - o[1]])
    c = u.dot(v) / (u.norm() * v.norm())
    return float(sp.acos(sp.nsimplify(c, rational=False)) * 180 / sp.pi)


def d(p, q):
    return float(sp.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2))


def proche(a, b, tol=1e-6):
    return abs(float(a) - float(b)) < tol


def arrondi(x, n=1):
    """Arrondi au dixième (n=1) ou à l'unité (n=0), comme les mesures de l'élève."""
    return round(float(x) + 1e-12, n)


def inegalite(a, b, c):
    a, b, c = sorted([sp.nsimplify(a), sp.nsimplify(b), sp.nsimplify(c)])
    if c < a + b:
        return "ok"
    if c == a + b:
        return "plat"
    return "non"


def aire(base, h):
    return sp.nsimplify(base) * sp.nsimplify(h) / 2


# ============================================================ COURS
ctrl("cours inégalité 3,5 ; 2,5 ; 5", inegalite(R(7, 2), R(5, 2), 5) == "ok")
ctrl("cours inégalité 3 ; 2 ; 5", inegalite(3, 2, 5) == "plat")
ctrl("cours inégalité 2,5 ; 2 ; 5", inegalite(R(5, 2), 2, 5) == "non")
ctrl("cours exemple 6 ; 3,5 ; 2 impossible", inegalite(6, R(7, 2), 2) == "non" and R(7, 2) + 2 == R(11, 2))
ctrl("cours exemple 4,5 ; 3 ; 2 possible", inegalite(R(9, 2), 3, 2) == "ok" and 3 + 2 == 5)
ctrl("cours erreur 2 ; 3 ; 8", inegalite(2, 3, 8) == "non" and 2 < 3 + 8)
ctrl("cours 180 - 38 - 85 = 57", 180 - (38 + 85) == 57 and 38 + 85 == 123)
ctrl("cours équilatéral 60", sp.Rational(180, 3) == 60)
ctrl("cours isocèle 36 -> 72", 180 - 36 == 144 and R(144, 2) == 72)
ctrl("cours isocèle 25 -> 130", 180 - 2 * 25 == 130)
ctrl("cours LMN existe", inegalite(R(11, 2), R(9, 2), 3) == "ok" and R(9, 2) + 3 == R(15, 2))
ctrl("cours IJK 35 + 70 = 105", 35 + 70 == 105 and 105 < 180)
ctrl("cours XYZ angle Y = 70", 180 - (50 + 60) == 70)
ctrl("cours FG = 7 rayon 3,5", R(7, 2) == sp.nsimplify(3.5))
ctrl("cours aire 9 x 4 / 2 = 18", aire(9, 4) == 18 and 9 * 4 == 36)
ctrl("cours hauteur 21 cm2 base 6 -> 7", sp.solve(sp.Eq(6 * sp.Symbol("h") / 2, 21))[0] == 7 and 2 * 21 == 42)
ctrl("cours médiane 30 / 2 = 15", R(30, 2) == 15)

# ============================================================ EXERCICES
# 2980
ctrl("2980 a) 4,5,7", inegalite(4, 5, 7) == "ok" and 4 + 5 == 9)
ctrl("2980 b) 3,4,8", inegalite(3, 4, 8) == "non" and 3 + 4 == 7)
ctrl("2980 c) 2,5 ; 3,5 ; 6", inegalite(R(5, 2), R(7, 2), 6) == "plat")
ctrl("2980 d) 6,6,6", inegalite(6, 6, 6) == "ok" and 6 + 6 == 12)
ctrl("2980 Q2 ABC 6,4,5", inegalite(6, 4, 5) == "ok" and 4 + 5 == 9)
ctrl("2980 Q5 4 cm aplati", inegalite(3, 7, 4) == "plat")
ctrl("2980 Q5 9 cm possible", inegalite(3, 7, 9) == "ok" and 3 + 7 == 10)
ctrl("2980 Q5 11 cm impossible", inegalite(3, 7, 11) == "non")
# 2984
ctrl("2984 Q1 65", 180 - (47 + 68) == 65 and 47 + 68 == 115)
ctrl("2984 Q2 56", 180 - (90 + 34) == 56 and 90 + 34 == 124 and 34 + 56 == 90)
ctrl("2984 Q3 70", 180 - 40 == 140 and R(140, 2) == 70)
ctrl("2984 Q4 52 et 76", 180 - (52 + 52) == 76 and 52 + 52 == 104)
ctrl("2984 Q5 60", R(180, 3) == 60)
ctrl("2984 Q6 a) 90+90", 90 + 90 == 180)
ctrl("2984 Q6 b) 185", 100 + 85 == 185 and 185 > 180)
ctrl("2984 Q6 c) 150", 3 * 50 == 150 and 150 != 180)
# 2981 : DE = 5,5 ; DF = 4 ; angle D = 50
DE, DF = R(11, 2), 4
EF = sp.sqrt(DE ** 2 + DF ** 2 - 2 * DE * DF * sp.cos(50 * deg))
ctrl("2981 Q3 EF ≈ 4,2", arrondi(EF.evalf()) == 4.2)
angE = sp.asin(DF * sp.sin(50 * deg) / EF) * 180 / sp.pi
angF = 180 - 50 - angE
ctrl("2981 Q4 DEF ≈ 46", round(float(angE)) == 46)
ctrl("2981 Q4 DFE ≈ 84", round(float(angF)) == 84)
ctrl("2981 Q4 50 + 46 + 84 = 180", 50 + 46 + 84 == 180)
ctrl("2981 Q4 angle en F aigu (asin valable)", float(DE ** 2) < float(DF ** 2 + EF ** 2))
ctrl("2981 Q5 isocèle 30 -> 75", 180 - 30 == 150 and R(150, 2) == 75)
# 2978
ctrl("2978 Q1 AUG = 65", 180 - (40 + 75) == 65 and 40 + 75 == 115)
AG = 5 * sp.sin(65 * deg) / sp.sin(75 * deg)
UG = 5 * sp.sin(40 * deg) / sp.sin(75 * deg)
ctrl("2978 Q3 AG ≈ 4,7", arrondi(AG.evalf()) == 4.7)
ctrl("2978 Q3 UG ≈ 3,3", arrondi(UG.evalf()) == 3.3)
ctrl("2978 Q4 EFG = 55", 180 - 70 == 110 and R(110, 2) == 55)
EFiso = R(5, 2) / sp.cos(55 * deg)
ctrl("2978 Q5 EF ≈ 4,4", arrondi(EFiso.evalf()) == 4.4)
ctrl("2978 Q6 185 > 180", 100 + 85 == 185)
# 2991 : B(0,0), C(7,0), A(4,4)
A, B, C = (4, 4), (0, 0), (7, 0)
ctrl("2991 BC = 7", sp.sqrt((C[0] - B[0]) ** 2 + (C[1] - B[1]) ** 2) == 7)
ctrl("2991 AC = 5", sp.sqrt((C[0] - A[0]) ** 2 + (C[1] - A[1]) ** 2) == 5)
ctrl("2991 AH = 4", A[1] == 4)
ctrl("2991 Q2 aire 14", aire(7, 4) == 14)
BK = sp.solve(sp.Eq(5 * sp.Symbol("x") / 2, 14))[0]
ctrl("2991 Q3 BK = 5,6", BK == R(28, 5) and 5 * BK == 28)
t = R((B[0] - A[0]) * 3 + (B[1] - A[1]) * (-4), 25)
K = (A[0] + 3 * t, A[1] - 4 * t)
ctrl("2991 Q3 K sur [AC]", 0 < t < 1)
ctrl("2991 Q3 BK exact (coordonnées)", sp.sqrt(K[0] ** 2 + K[1] ** 2) == R(28, 5))
# orthocentre : x = 4 (hauteur de A), y = 3x/4 (hauteur de B) ; hauteur de C : perpendiculaire à (AB) (y = x) par C
Ho = (4, 3)
ctrl("2991 Q4 orthocentre sur la hauteur issue de C", (Ho[0] - C[0]) * 4 + (Ho[1] - C[1]) * 4 == 0)
ctrl("2991 Q4 triangle acutangle", all(angle_deg(*x) < 90 for x in ((A, B, C), (B, C, A), (C, A, B))))
D, E, Fp = (R(-3, 2), 3), (0, 0), (4, 0)
ctrl("2991 Q5 angle en E obtus", angle_deg(E, D, Fp) > 90)
Kd = (D[0], 0)
ctrl("2991 Q5 K hors de [EF]", Kd[0] < E[0])
ctrl("2991 Q6 DK = 3 et aire 6", D[1] == 3 and aire(4, 3) == 6)
ctrl("2991 Q6 erreur KF : 8,25 > 6", aire(Fp[0] - Kd[0], 3) == R(33, 4) and R(33, 4) > 6)
# 2987 : ABC 7, 5, 6
ctrl("2987 Q1 existe", inegalite(7, 5, 6) == "ok" and 5 + 6 == 11)
a, b, c = 6, 5, 7          # BC, AC, AB
s = R(a + b + c, 2)
S = sp.sqrt(s * (s - a) * (s - b) * (s - c))
Rc = sp.nsimplify(a * b * c / (4 * S))
ctrl("2987 Q3 rayon ≈ 3,6", arrondi(Rc.evalf()) == 3.6)
ctrl("2987 Q5 ST = 5", sp.sqrt(3 ** 2 + 4 ** 2) == 5)
ctrl("2987 Q5 rayon 2,5", R(5, 2) == sp.nsimplify(2.5))
# 2982 : B(0,0), C(90,0), A(30,40), H(30,0), M(45,0)
ctrl("2982 Q1 1800", aire(90, 40) == 1800)
ctrl("2982 Q2 600 et 1200", aire(30, 40) == 600 and aire(60, 40) == 1200 and 90 - 30 == 60 and 600 + 1200 == 1800)
ctrl("2982 Q3 900", aire(45, 40) == 900 and 2 * 900 == 1800)
ctrl("2982 Q4 HM = 15", 45 - 30 == 15)
ctrl("2982 Q5 3 x 600", R(90, 3) == 30 and aire(30, 40) == 600 and 3 * 600 == 1800)
# 2994
ctrl("2994 Q2 48", aire(12, 8) == 48)
ctrl("2994 Q3 48 aussi", aire(12, 8) == 48)
ctrl("2994 Q4 moitié de 96", 12 * 8 == 96 and R(96, 2) == 48)
ctrl("2994 Q5 16 et 32", aire(4, 8) == 16 and 12 - 4 == 8 and aire(8, 8) == 32 and 16 + 32 == 48)
BN = sp.solve(sp.Eq(12 * sp.Symbol("x") / 2, 18))[0]
ctrl("2994 Q6 BN = 3", BN == 3 and 12 * BN == 36)
ctrl("2994 erreur sans /2 : 1,5 m et 9 m2", R(18, 12) == R(3, 2) and aire(12, R(3, 2)) == 9)
# 2998
ctrl("2998 Q1 56", 180 - 124 == 56)
ctrl("2998 Q3 68", 180 - (56 + 56) == 68 and 56 + 56 == 112)
ctrl("2998 Q4 124", 68 + 56 == 124)
ctrl("2998 Q5 120", 180 - 60 == 120 and 180 - 120 == 60)
ctrl("2998 Q6 135", R(180 - 90, 2) == 45 and 180 - 45 == 135)
# 2996 : rectangle en A, AB = 4,5 ; AC = 6
AB_, AC_ = R(9, 2), 6
BC_ = sp.sqrt(AB_ ** 2 + AC_ ** 2)
ctrl("2996 Q2 BC = 7,5", BC_ == R(15, 2))
angB = sp.atan(AC_ / AB_) * 180 / sp.pi
ctrl("2996 Q2 ABC ≈ 53", round(float(angB)) == 53)
ctrl("2996 Q2 ACB ≈ 37", round(float(90 - angB)) == 37 and 90 - 53 == 37)
ctrl("2996 Q3 rayon 3,75", BC_ / 2 == R(15, 4))
ctrl("2996 Q4 aire 13,5", aire(AB_, AC_) == R(27, 2))
AH_ = sp.solve(sp.Eq(BC_ * sp.Symbol("x") / 2, R(27, 2)))[0]
ctrl("2996 Q5 AH = 3,6", AH_ == R(18, 5) and BC_ * AH_ == 27)
ctrl("2996 Q6 6,75", aire(R(15, 4), R(18, 5)) == R(27, 4) and 2 * R(27, 4) == R(27, 2))

# ============================================================ FIGURES (coordonnées réelles)
spec = importlib.util.spec_from_file_location("fig274", ICI / "figures" / "figures.py")
fig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fig)
DON = fig.DONNEES


def L(nom, p, q, v, tol=1e-6):
    ctrl(f"figure {nom} : longueur {v}", proche(d(p, q), v, tol))


def ANG(nom, o, p, q, v, tol=1e-4):
    ctrl(f"figure {nom} : angle {v}", proche(angle_deg(o, p, q), v, tol))


g = DON["cours_ccc"]
L("cours_ccc LM", g["L"], g["M"], 5.5); L("cours_ccc LN", g["L"], g["N"], 4.5); L("cours_ccc MN", g["M"], g["N"], 3)
g = DON["cours_cac"]
L("cours_cac RS", g["R"], g["S"], 5); L("cours_cac RT", g["R"], g["T"], 3.5); ANG("cours_cac SRT", g["R"], g["S"], g["T"], 40)
g = DON["cours_aca"]
L("cours_aca IJ", g["I"], g["J"], 5); ANG("cours_aca KIJ", g["I"], g["K"], g["J"], 35)
ANG("cours_aca IJK", g["J"], g["I"], g["K"], 70); ANG("cours_aca IKJ", g["K"], g["I"], g["J"], 75)
g = DON["cours_cercle"]
ctrl("figure cours_cercle : OA = OB = OC", proche(d(g["O"], g["A"]), d(g["O"], g["B"])) and proche(d(g["O"], g["A"]), d(g["O"], g["C"])))
g = DON["cours_cercle_rect"]
ANG("cours_cercle_rect angle droit en E", g["E"], g["F"], g["G"], 90)
ctrl("figure cours_cercle_rect : O milieu de [FG]", proche(g["O"][0], (g["F"][0] + g["G"][0]) / 2) and proche(g["O"][1], 0))
g = DON["cours_hauteurs"]
for (s, p, q) in (("A", "B", "C"), ("B", "C", "A"), ("C", "A", "B")):
    # l'orthocentre H est sur la hauteur issue de s : (H - s) perpendiculaire à (q - p)
    v = (g["H"][0] - g[s][0], g["H"][1] - g[s][1])
    w = (g[q][0] - g[p][0], g[q][1] - g[p][1])
    ctrl(f"figure cours_hauteurs : orthocentre sur la hauteur issue de {s}", proche(v[0] * w[0] + v[1] * w[1], 0))
ctrl("figure cours_hauteurs : angle obtus en E", angle_deg(g["E"], g["D"], g["F"]) > 90)
ctrl("figure cours_hauteurs : K pied extérieur", proche(g["K"][0], g["D"][0]) and g["K"][0] < g["E"][0])
g = DON["cours_aire"]
ctrl("figure cours_aire : H pied de la hauteur", proche(g["H"][0], g["A"][0]) and proche(g["H"][1], 0))
g = DON["cours_mediane_aire"]
ctrl("figure cours_mediane_aire : M milieu, H pied, M ≠ H", proche(g["M"][0], (g["B"][0] + g["C"][0]) / 2)
     and proche(g["H"][0], g["A"][0]) and abs(g["M"][0] - g["H"][0]) > 0.5)
g = DON["cours_medianes_G"]
for (s, p, q) in (("D", "E", "F"), ("E", "F", "D"), ("F", "D", "E")):
    m = ((g[p][0] + g[q][0]) / 2, (g[p][1] + g[q][1]) / 2)
    cr = (m[0] - g[s][0]) * (g["G"][1] - g[s][1]) - (m[1] - g[s][1]) * (g["G"][0] - g[s][0])
    ctrl(f"figure cours_medianes_G : G sur la médiane issue de {s}", proche(cr, 0))
g = DON["cours_inegalite"]
L("cours_inegalite AC", g["A"], g["C"], 3.5); L("cours_inegalite BC", g["B"], g["C"], 2.5)

g = DON["ex2980"]
L("ex2980 AB", g["A"], g["B"], 6); L("ex2980 AC", g["A"], g["C"], 4); L("ex2980 BC", g["B"], g["C"], 5)
L("ex2980 AC'", g["A"], g["C'"], 4); L("ex2980 BC'", g["B"], g["C'"], 5)
g = DON["ex2984"]
for (cle, angs) in (("a", (47, 68, 65)), ("b", (90, 34, 56)), ("c", (40, 70, 70)), ("d", (76, 52, 52))):
    X, Y, Z = g[cle]
    ANG(f"ex2984 {cle} sommet", X, Y, Z, angs[0]); ANG(f"ex2984 {cle} gauche", Y, X, Z, angs[1]); ANG(f"ex2984 {cle} droite", Z, X, Y, angs[2])
g = DON["ex2981"]
L("ex2981 DE", g["D"], g["E"], 5.5); L("ex2981 DF", g["D"], g["F"], 4); ANG("ex2981 EDF", g["D"], g["E"], g["F"], 50)
ctrl("figure ex2981 : EF ≈ 4,2", arrondi(d(g["E"], g["F"])) == 4.2)
g = DON["ex2981_iso"]
L("ex2981_iso AB", g["A"], g["B"], 4); L("ex2981_iso AC", g["A"], g["C"], 4); ANG("ex2981_iso BAC", g["A"], g["B"], g["C"], 30)
ANG("ex2981_iso ABC", g["B"], g["A"], g["C"], 75); ANG("ex2981_iso ACB", g["C"], g["A"], g["B"], 75)
g = DON["ex2978_AUG"]
L("ex2978 AU", g["A"], g["U"], 5); ANG("ex2978 UAG", g["A"], g["U"], g["G"], 40)
ANG("ex2978 AUG", g["U"], g["A"], g["G"], 65); ANG("ex2978 AGU", g["G"], g["A"], g["U"], 75)
ctrl("figure ex2978 : AG ≈ 4,7 et UG ≈ 3,3", arrondi(d(g["A"], g["G"])) == 4.7 and arrondi(d(g["U"], g["G"])) == 3.3)
g = DON["ex2978_EFG"]
L("ex2978 FG", g["F"], g["G"], 5); ANG("ex2978 FEG", g["E"], g["F"], g["G"], 70)
ctrl("figure ex2978 : EF = EG ≈ 4,4", proche(d(g["E"], g["F"]), d(g["E"], g["G"])) and arrondi(d(g["E"], g["F"])) == 4.4)
g = DON["ex2991"]
L("ex2991 BC", g["B"], g["C"], 7); L("ex2991 AC", g["A"], g["C"], 5); L("ex2991 AH", g["A"], g["H"], 4)
L("ex2991 BK", g["B"], g["K"], 5.6)
for (s, p, q, pied) in (("A", "B", "C", "H"), ("B", "A", "C", "K"), ("C", "A", "B", "L")):
    v = (g[pied][0] - g[s][0], g[pied][1] - g[s][1])
    w = (g[q][0] - g[p][0], g[q][1] - g[p][1])
    ctrl(f"figure ex2991 : ({s}{pied}) perpendiculaire", proche(v[0] * w[0] + v[1] * w[1], 0))
    o = (g["Orth"][0] - g[s][0], g["Orth"][1] - g[s][1])
    ctrl(f"figure ex2991 : orthocentre sur la hauteur issue de {s}", proche(o[0] * w[0] + o[1] * w[1], 0))
g = DON["ex2991b"]
L("ex2991b EF", g["E"], g["F"], 4); L("ex2991b DK", g["D"], g["K"], 3)
g = DON["ex2987"]
L("ex2987 AB", g["A"], g["B"], 7); L("ex2987 AC", g["A"], g["C"], 5); L("ex2987 BC", g["B"], g["C"], 6)
ctrl("figure ex2987 : OA = OB = OC = R", all(proche(d(g["O"], g[x]), g["R"]) for x in "ABC"))
ctrl("figure ex2987 : R = rayon exact", proche(g["R"], float(Rc)))
g = DON["ex2987_RST"]
L("ex2987 RS", g["R"], g["S"], 3); L("ex2987 RT", g["R"], g["T"], 4); L("ex2987 ST", g["S"], g["T"], 5)
ctrl("figure ex2987 : OR = OS = OT = 2,5", all(proche(d(g["O"], g[x]), 2.5) for x in "RST"))
g = DON["ex2982"]
L("ex2982 BC", g["B"], g["C"], 90); L("ex2982 AH", g["A"], g["H"], 40); L("ex2982 BH", g["B"], g["H"], 30)
L("ex2982 BM", g["B"], g["M"], 45)
g = DON["ex2994"]
L("ex2994 AB", g["A"], g["B"], 12); L("ex2994 BC", g["B"], g["C"], 8); L("ex2994 DM", g["D"], g["M"], 4)
L("ex2994 DM'", g["D"], g["M'"], 9); L("ex2994 MK", g["M"], g["K"], 8); L("ex2994 BN", g["B"], g["N"], 3)
g = DON["ex2998"]
ANG("ex2998 ACD", g["C"], g["A"], g["D"], 124); ANG("ex2998 ABC", g["B"], g["A"], g["C"], 56)
ANG("ex2998 BAC", g["A"], g["B"], g["C"], 68)
ctrl("figure ex2998 : AB = AC", proche(d(g["A"], g["B"]), d(g["A"], g["C"])))
g = DON["ex2996_constr"]
L("ex2996 AB", g["A"], g["B"], 4.5); L("ex2996 AC", g["A"], g["C"], 6); ANG("ex2996 angle droit", g["A"], g["B"], g["C"], 90)
ctrl("figure ex2996 : OA = OB = OC = 3,75", all(proche(d(g["O"], g[x]), 3.75) for x in "ABC"))
ctrl("figure ex2996 : arcs de la médiatrice équidistants de B et C",
     all(proche(d(g[P], g["B"]), d(g[P], g["C"])) for P in ("P1", "P2")))
g = DON["ex2996_aires"]
L("ex2996b BC", g["B"], g["C"], 7.5); L("ex2996b BA", g["B"], g["A"], 4.5); L("ex2996b CA", g["C"], g["A"], 6)
L("ex2996b AH", g["A"], g["H"], 3.6); L("ex2996b BO", g["B"], g["O"], 3.75)

# ============================================================ STRUCTURE
meta = json.loads((ICI / "source_en_ligne" / "meta.json").read_text(encoding="utf-8"))
ex_txt = (ICI / "exercices.txt").read_text(encoding="utf-8")
blocs = [b.strip() for b in re.split(r"^===[ \t]*$", ex_txt, flags=re.M) if b.strip()]
ids = [int(re.search(r"^Id:\s*(\d+)", b, re.M).group(1)) for b in blocs]
retires = [int(m.group(1)) for m in re.finditer(r"^(\d+)\s", (ICI / "exercices_retires.txt").read_text(encoding="utf-8"), re.M)]
ids_ligne = {e["id"] for e in meta["exercices"]}
ctrl("structure : 10 exercices gardés", len(ids) == 10 and len(set(ids)) == 10)
ctrl("structure : 11 retirés", len(retires) == 11 and len(set(retires)) == 11)
ctrl("structure : gardés + retirés = 21 Id en ligne", set(ids) | set(retires) == ids_ligne and not set(ids) & set(retires))
corr = json.loads((ICI / "figures" / "correspondance.json").read_text(encoding="utf-8"))
titres = []
types = []
for b in blocs:
    titre = b.splitlines()[0].replace("===", "", 1).strip()
    titres.append(titre)
    types.append(titre.split(" - ")[0])
    eid = re.search(r"^Id:\s*(\d+)", b, re.M).group(1)
    en = b.split("Énoncé:")[1].split("Étapes:")[0]
    et = b.split("Étapes:")[1].split("Solution:")[0]
    so = b.split("Solution:")[1]
    nq = len(re.findall(r"^\d+\. ", en, re.M))
    ne = len(re.findall(r"^## Question \d+ ", et, re.M))
    ns = len(re.findall(r"^\d+\. ", so, re.M))
    ctrl(f"structure {eid} : questions = étapes = solutions ({nq})", nq == ne == ns and nq >= 5)
    ctrl(f"structure {eid} : un résultat par question", et.count("::: resultat") >= ne)
    ctrl(f"structure {eid} : erreur fréquente ou à retenir", "::: attention" in et or "::: retenir" in et)
    ctrl(f"structure {eid} : une méthode au moins", "::: methode" in et)
    imgs = set(re.findall(r"\[IMAGE_(\d+)\]", b))
    ctrl(f"structure {eid} : images appelées = déclarées", imgs == set(corr["exercices"].get(eid, {}).keys()))
    for n, v in corr["exercices"].get(eid, {}).items():
        ctrl(f"structure {eid} : fichier {v['fichier']} présent", (ICI / "figures" / "images" / v["fichier"]).exists())
ctrl("structure : titres uniques", len(set(titres)) == len(titres))
ctrl("structure : progression 3 D / 3 E / 3 P / 1 S",
     types == ["Découverte"] * 3 + ["Entraînement"] * 3 + ["Problème"] * 3 + ["Synthèse"])
for nom in ("cours_269.txt", "fiche_189.txt"):
    t = (ICI / nom).read_text(encoding="utf-8")
    genre, cle = ("cours", "269") if nom.startswith("cours") else ("fiches", "189")
    imgs = set(re.findall(r"\[IMAGE_(\d+)\]", t))
    ctrl(f"structure {nom} : images appelées = déclarées", imgs == set(corr[genre][cle].keys()))
tout = ex_txt + (ICI / "cours_269.txt").read_text(encoding="utf-8") + (ICI / "fiche_189.txt").read_text(encoding="utf-8")
ctrl("aucune mention du brevet", "brevet" not in tout.lower())
ctrl("aucun nom de chapitre dans les titres", all("Construire et comprendre" not in t for t in titres))

print(f"{len(OK)} contrôles justes, {len(KO)} faux")
for k in KO:
    print("  FAUX :", k)
sys.exit(1 if KO else 0)
