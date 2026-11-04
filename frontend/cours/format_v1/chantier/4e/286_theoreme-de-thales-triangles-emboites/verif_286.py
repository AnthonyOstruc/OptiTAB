# -*- coding: utf-8 -*-
"""Vérification (sympy, valeurs exactes) de tous les calculs de la notion 286
« Théorème de Thalès (triangles emboîtés) » (4e) : cours, fiche, 21 exercices,
et coordonnées des figures (parallélisme, rapports, longueurs dessinées).

Lancer : python verif_286.py  (depuis ce dossier)
"""
import importlib.util
import pathlib

from sympy import Rational as R, sqrt, nsimplify, symbols, solve, Eq, Point, Line, Segment

ICI = pathlib.Path(__file__).resolve().parent
OK = 0
ERREURS = []


def eg(nom, a, b):
    global OK
    if not isinstance(a, bool):
        a, b = nsimplify(a), nsimplify(b)
    if a == b:
        OK += 1
    else:
        ERREURS.append(f"{nom} : {a} != {b}")


def vrai(nom, cond):
    eg(nom, bool(cond), True)


def arr(x, n):
    """Arrondi décimal au 10^-n d'une valeur exacte (renvoyé exact)."""
    return R(round(float(x) * 10 ** n), 10 ** n)


def num(a, b, c):
    """Quatrième proportionnelle, inconnue au numérateur : a/b = x/c  ->  x = a*c/b."""
    return nsimplify(a) * nsimplify(c) / nsimplify(b)


def den(a, b, c):
    """Quatrième proportionnelle, inconnue au dénominateur : a/b = c/x  ->  x = b*c/a."""
    return nsimplify(b) * nsimplify(c) / nsimplify(a)


def triangle_ok(a, b, c):
    a, b, c = sorted(map(nsimplify, (a, b, c)))
    return a + b > c


x = symbols("x")

# ------------------------------------------------------------------ cours
eg("cours AN", num(4, 6, 9), 6)
eg("cours MN", num(4, 6, R(15, 2)), 5)
vrai("cours triangle", triangle_ok(6, 9, R(15, 2)))
eg("cours AB = AM + MB", R(5, 2) + R(3, 2), 4)
eg("cours rapports 4/6", R(4, 6), R(2, 3))
eg("cours 6/9", R(6, 9), R(2, 3))
eg("cours 5/7,5", 5 / R(15, 2), R(2, 3))
eg("cours réduc AN", R(2, 3) * 9, 6)
eg("cours réduc MN", R(2, 3) * R(15, 2), 5)
eg("cours agrand", R(6, 4), R(3, 2))
eg("cours agrand 6x1,5", 6 * R(3, 2), 9)
eg("cours agrand 5x1,5", 5 * R(3, 2), R(15, 2))
eg("cours périm ABC", 6 + 9 + R(15, 2), R(45, 2))
eg("cours périm AMN", 4 + 6 + 5, 15)
eg("cours périm k", R(45, 2) * R(2, 3), 15)
eg("cours ombre", den(R(8, 10), 6, 1), R(15, 2))
eg("fiche AN", num(4, 6, 9), 6)

# ------------------------------------------------------------------ 3630
eg("3630 RT", den(2, 5, 3), R(15, 2))
eg("3630 VT", R(15, 2) - 3, R(9, 2))
eg("3630 erreur", R(2 * 3, 5), R(12, 10))

# ------------------------------------------------------------------ 3631
eg("3631 AN", num(3, 5, 10), 6)
eg("3631 MN", num(3, 5, 8), R(24, 5))
eg("3631 NC", 10 - 6, 4)
eg("3631 AN/AC", R(6, 10), R(3, 5))
eg("3631 MN/BC", R(24, 5) / 8, R(3, 5))
vrai("3631 triangle", triangle_ok(5, 10, 8))

# ------------------------------------------------------------------ 3632
k = R(4, 10)
eg("3632 k", k, R(2, 5))
eg("3632 AN", k * 12, R(24, 5))
eg("3632 MN", k * 15, 6)
eg("3632 P ABC", 10 + 12 + 15, 37)
eg("3632 P AMN", 4 + R(24, 5) + 6, R(74, 5))
eg("3632 P k", k * 37, R(74, 5))
eg("3632 agrand", R(10, 4), R(5, 2))
eg("3632 4,8x2,5", R(24, 5) * R(5, 2), 12)
eg("3632 6x2,5", 6 * R(5, 2), 15)
vrai("3632 triangle", triangle_ok(10, 12, 15))

# ------------------------------------------------------------------ 3633
eg("3633 AB", 4 + 6, 10)
eg("3633 AC", den(4, 10, 6), 15)
eg("3633 NC", 15 - 6, 9)
eg("3633 BC", den(4, 10, 5), R(25, 2))
eg("3633 Léo", den(4, 6, 5), R(15, 2))
vrai("3633 triangle", triangle_ok(10, 15, R(25, 2)))

# ------------------------------------------------------------------ 3634
eg("3634 k", R(2, 8), R(1, 4))
eg("3634 AN", R(1, 4) * 6, R(3, 2))
eg("3634 MN", R(1, 4) * 9, R(9, 4))
eg("3634 inverse", R(8, 2), 4)
eg("3634 vérif", R(3, 2) * 4, 6)
eg("3634 k'", R(6, 8), R(3, 4))
eg("3634 AN'", R(3, 4) * 6, R(9, 2))
eg("3634 MN'", R(3, 4) * 9, R(27, 4))
vrai("3634 triangle", triangle_ok(8, 6, 9))

# ------------------------------------------------------------------ 3635
eg("3635 HK", num(3, 5, 6), R(18, 5))
eg("3635 EK", num(3, 5, 7), R(21, 5))
vrai("3635 b fausse", R(3, 2) != R(18, 5) / 6)
vrai("3635 f fausse", R(3, 5) != R(5, 3))
vrai("3635 triangle", triangle_ok(5, 7, 6))

# ------------------------------------------------------------------ 3636
eg("3636 CN", den(2, 12, R(3, 2)), 9)
eg("3636 erreur (arbre en haut)", R(2, 12) * R(3, 2), R(1, 4))
eg("3636 SM", sqrt(2 ** 2 + R(3, 2) ** 2), R(5, 2))
eg("3636 SM²", 4 + R(9, 4), R(25, 4))
eg("3636 SN", den(2, 12, R(5, 2)), 15)
eg("3636 vérif", 12 ** 2 + 9 ** 2, 15 ** 2)

# ------------------------------------------------------------------ 3637
eg("3637 k", R(24, 10) / 6, R(2, 5))
eg("3637 AC", den(R(24, 10), 6, 3), R(15, 2))
eg("3637 18/2,4", 18 / R(24, 10), R(15, 2))
eg("3637 vérif AC", R(2, 5) * R(15, 2), 3)
eg("3637 BC", den(R(24, 10), 6, R(32, 10)), 8)
eg("3637 19,2", 6 * R(32, 10), R(192, 10))
eg("3637 erreur", R(2, 5) * R(32, 10), R(128, 100))
eg("3637 MB", 6 - R(24, 10), R(36, 10))
eg("3637 NC", R(15, 2) - 3, R(9, 2))
eg("3637 périmètre", R(36, 10) + 8 + R(9, 2) + R(32, 10), R(193, 10))
vrai("3637 triangle", triangle_ok(6, R(15, 2), 8))

# ------------------------------------------------------------------ 3638
eg("3638 AP", 2 + 3, 5)
eg("3638 AB", 5 + 3, 8)
eg("3638 AC", den(2, 8, 3), 12)
eg("3638 BC", den(2, 8, R(5, 2)), 10)
eg("3638 AQ", num(5, 8, 12), R(15, 2))
eg("3638 PQ", num(5, 8, 10), R(25, 4))
eg("3638 NQ", R(15, 2) - 3, R(9, 2))
eg("3638 QC", 12 - R(15, 2), R(9, 2))
vrai("3638 triangle", triangle_ok(8, 12, 10))

# ------------------------------------------------------------------ 3639
eg("3639 MN", num(2, 6, 9), 3)
eg("3639 AN", num(2, 6, 6), 2)
eg("3639 MB", 6 - 2, 4)
AH = sqrt(6 ** 2 - R(9, 2) ** 2)
eg("3639 AH²", 36 - R(81, 4), R(63, 4))
eg("3639 AH arrondi", arr(AH, 2), R(397, 100))
eg("3639 AK arrondi", arr(AH / 3, 2), R(132, 100))
eg("3639 KH arrondi", arr(AH - AH / 3, 2), R(265, 100))

# ------------------------------------------------------------------ 3640
sol = solve(Eq(x / (x + 4), R(3, 9)), x)
eg("3640 x", sol[0], 2)
eg("3640 développement", (9 * x - 3 * (x + 4)).expand(), 6 * x - 12)
eg("3640 AC", 3 + 6, 9)
eg("3640 BC", den(2, 6, R(5, 2)), R(15, 2))
vrai("3640 triangle", triangle_ok(6, 9, R(15, 2)))

# ------------------------------------------------------------------ 3641
eg("3641 AB", 3 + 2, 5)
eg("3641 Zoé", R(3, 1) * R(15, 2) / 5, R(9, 2))
eg("3641 MN", num(3, 5, 8), R(24, 5))
eg("3641 Sami", 5 * R(15, 2) / 3, R(25, 2))
eg("3641 AN", num(3, 5, R(15, 2)), R(9, 2))
eg("3641 22,5/5", R(45, 2) / 5, R(9, 2))
eg("3641 NC", R(15, 2) - R(9, 2), 3)
eg("3641 AN/AC", R(9, 2) / R(15, 2), R(3, 5))
eg("3641 MN/BC", R(24, 5) / 8, R(3, 5))
vrai("3641 triangle", triangle_ok(5, R(15, 2), 8))

# ------------------------------------------------------------------ 3642
eg("3642 AC", sqrt(8 ** 2 + 6 ** 2), 10)
eg("3642 MN", num(2, 8, 6), R(3, 2))
eg("3642 AN", num(2, 8, 10), R(5, 2))
eg("3642 Pythagore", 2 ** 2 + R(3, 2) ** 2, R(5, 2) ** 2)

# ------------------------------------------------------------------ 3643
eg("3643 BS", den(4, 20, R(18, 10)), 9)
eg("3643 OT²", 16 + R(324, 100), R(1924, 100))
eg("3643 OT", arr(sqrt(R(1924, 100)), 2), R(439, 100))
eg("3643 sœur", 20 * R(135, 100) / 9, 3)
eg("3643 autre arbre", den(5, 30, R(18, 10)), R(108, 10))
eg("3643 erreur", R(5, 30) * R(18, 10), R(3, 10))

# ------------------------------------------------------------------ 3644 (échelle 1/1000 : 1 cm -> 10 m)
eg("3644 AB plan", 3 + R(9, 2), R(15, 2))
eg("3644 AB réel", R(15, 2) * 10, 75)
eg("3644 AC réel", 9 * 10, 90)
eg("3644 BC réel", 6 * 10, 60)
eg("3644 AN plan", num(3, R(15, 2), 9), R(18, 5))
eg("3644 MN plan", num(3, R(15, 2), 6), R(12, 5))
eg("3644 MN réel", R(12, 5) * 10, 24)
eg("3644 MN réel direct", num(30, 75, 60), 24)
eg("3644 prix", 24 * R(25, 2), 300)
eg("3644 AM 36 m", 75 * R(36, 60), 45)
eg("3644 2700/60", R(2700, 60), 45)
eg("3644 AM plan", R(4500, 1000), R(9, 2))
vrai("3644 triangle", triangle_ok(R(15, 2), 9, 6))

# ------------------------------------------------------------------ 3645
eg("3645 AB", 12 + 36, 48)
eg("3645 BC", den(12, 48, 15), 60)
eg("3645 erreur MB", den(12, 36, 15), 45)
eg("3645 AC", den(12, 48, 13), 52)
eg("3645 NC", 52 - 13, 39)
eg("3645 canard", 60 / R(1, 2), 120)
eg("3645 promeneur", 48 + 52 - 60, 40)
vrai("3645 triangle", triangle_ok(48, 52, 60))
vrai("3645 petit triangle", triangle_ok(12, 13, 15))

# ------------------------------------------------------------------ 3646
eg("3646 AK", 8 - 3, 5)
eg("3646 MN x=3", R(5, 8) * 12, R(15, 2))
eg("3646 aire x=3", R(15, 2) * 3, R(45, 2))
MNx = 12 * (8 - x) / 8
eg("3646 MN(x)", (MNx - (12 - R(3, 2) * x)).simplify(), 0)
for xv, mn, aire in ((2, 9, 18), (4, 6, 24), (6, 3, 18)):
    eg(f"3646 MN({xv})", MNx.subs(x, xv), mn)
    eg(f"3646 aire({xv})", MNx.subs(x, xv) * xv, aire)
eg("3646 carré", solve(Eq(12 - R(3, 2) * x, x), x)[0], R(24, 5))
eg("3646 vérif carré", 12 - R(3, 2) * R(24, 5), R(24, 5))

# ------------------------------------------------------------------ 3647
eg("3647 BC", den(R(1, 2), 2, R(2, 5)), R(8, 5))
eg("3647 AH²", 4 - R(64, 100), R(336, 100))
eg("3647 AH", arr(sqrt(R(336, 100)), 2), R(183, 100))
eg("3647 chaîne basse", R(8, 10) * R(16, 10) / 2, R(64, 100))
eg("3647 chaîne 0,35", den(R(1, 2), 2, R(35, 100)), R(14, 10))
eg("3647 minimale", R(1, 2) * R(3, 2) / 2, R(375, 1000))

# ------------------------------------------------------------------ 3648
eg("3648 DR", R(3, 12) * R(6, 10), R(15, 100))
eg("3648 ES", R(6, 12) * R(6, 10), R(3, 10))
eg("3648 FT", R(9, 12) * R(6, 10), R(45, 100))
eg("3648 tube", R(15, 100) + R(3, 10) + R(45, 100), R(9, 10))
eg("3648 AB²", 144 + R(36, 100), R(14436, 100))
eg("3648 AB", arr(sqrt(R(14436, 100)), 2), R(1201, 100))
eg("3648 pente", R(6, 10) / 12, R(5, 100))
eg("3648 pente support", R(15, 100) / 3, R(5, 100))
eg("3648 autre porte", R(8, 10) / R(5, 100), 16)

# ------------------------------------------------------------------ 3649
eg("3649 x", solve(Eq(x / (x + 8), R(15, 20)), x)[0], 24)
eg("3649 développement", (15 * (x + 8)).expand(), 15 * x + 120)
eg("3649 vérif", R(24, 32), R(3, 4))
eg("3649 x'", solve(Eq(x / (x + 8), R(15, 25)), x)[0], 12)
eg("3649 vérif'", R(12, 20), R(3, 5))
eg("3649 passerelle", 24 + 3 + 3, 30)

# ------------------------------------------------------------------ figures : coordonnées
spec = importlib.util.spec_from_file_location("fig286", ICI / "figures" / "figures.py")
FIG = importlib.util.module_from_spec(spec)
spec.loader.exec_module(FIG)
for nom, (A, B, C, M, N, cotes) in FIG.CONTROLES.items():
    A, B, C, M, N = (Point(nsimplify(round(p[0], 6)), nsimplify(round(p[1], 6))) for p in (A, B, C, M, N))
    vrai(f"fig {nom} : M sur [AB]", Segment(A, B).contains(M) or Segment(A, B).distance(M) < R(1, 10 ** 4))
    vrai(f"fig {nom} : N sur [AC]", Segment(A, C).contains(N) or Segment(A, C).distance(N) < R(1, 10 ** 4))
    d1, d2 = N - M, C - B
    vrai(f"fig {nom} : (MN) // (BC)", abs(float(d1.x * d2.y - d1.y * d2.x)) < 1e-4)
    # rapports dessinés = rapports de l'énoncé (à 1 % près)
    r_des = float(A.distance(M) / A.distance(B))
    vrai(f"fig {nom} : AM/AB dessiné {r_des:.3f}", abs(r_des - float(cotes["r"])) < 0.01)
    if "forme" in cotes:  # côtés du grand triangle proportionnels aux vraies longueurs
        ab, ac, bc = (float(v) for v in cotes["forme"])
        u = float(A.distance(B)) / ab
        vrai(f"fig {nom} : AC proportionnel", abs(float(A.distance(C)) / u - ac) < 0.02 * ac)
        vrai(f"fig {nom} : BC proportionnel", abs(float(B.distance(C)) / u - bc) < 0.02 * bc)

print(f"{OK} contrôles justes, {len(ERREURS)} erreur(s)")
for e in ERREURS:
    print("  ✗", e)
