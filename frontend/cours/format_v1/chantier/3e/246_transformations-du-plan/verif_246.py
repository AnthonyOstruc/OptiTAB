# -*- coding: utf-8 -*-
"""Vérifications sympy de la notion 246 « Transformations du plan » (3e).

Chaque coordonnée des figures (figures/figures.py) et chaque résultat des
exercices est recalculé ici. Lancer : python verif_246.py
"""
from sympy import Rational as R, sqrt, Point, Polygon, Line, Segment, nsimplify, Abs, Integer, sympify
import math

n_ok = 0


def ok(cond, msg):
    global n_ok
    if not cond:
        raise AssertionError(msg)
    n_ok += 1


def sym_axe(p, axe):
    return Line(*axe).reflect if False else Point(p).reflect(Line(*axe))


def sym_centre(p, o):
    return Point(2 * o[0] - p[0], 2 * o[1] - p[1])


def rot(p, o, deg):
    return Point(p).rotate(sympify(deg) * __import__("sympy").pi / 180, Point(o))


def homot(p, o, k):
    return Point(o[0] + k * (p[0] - o[0]), o[1] + k * (p[1] - o[1]))


def aire(*pts):
    return Abs(Polygon(*[Point(p) for p in pts]).area)


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


# ------------------------------------------------------------------ 2401 symétrie axiale, axe x = 6
A, B, C = (1, 1), (4, 1), (2, 4)
axe = (Point(6, 0), Point(6, 1))
Ai, Bi, Ci = [sym_axe(p, axe) for p in (A, B, C)]
ok((Ai, Bi, Ci) == (Point(11, 1), Point(8, 1), Point(10, 4)), "2401 images")
ok(6 - C[0] == 4 and Ci.x - C[0] == 8, "2401 Q1 4 carreaux, 8 au total")
ok(6 - A[0] == 5 and 6 - B[0] == 2, "2401 Q2 distances à l'axe")
ok(Point(A).distance(Point(B)) == 3 and Ai.distance(Bi) == 3, "2401 Q4")
ok(orient(A, B, C) > 0 and orient(Ai, Bi, Ci) < 0, "2401 Q5 orientation inversée")

# ------------------------------------------------------------------ 2402 symétrie centrale, O(6 ; 4)
O = (6, 4)
A, B, C = (2, 5), (5, 5), (2, 7)
Ai, Bi, Ci = [sym_centre(p, O) for p in (A, B, C)]
ok((Ai, Bi, Ci) == (Point(10, 3), Point(7, 3), Point(10, 1)), "2402 images")
ok((O[0] - A[0], O[1] - A[1]) == (4, -1), "2402 Q1 déplacement A→O")
ok(Point(A).midpoint(Ai) == Point(O) and Point(B).midpoint(Bi) == Point(O), "2402 milieux")
ok(Point(A).distance(Point(C)) == 2 and Ai.distance(Ci) == 2, "2402 AC = A'C' = 2")
ok(Line(Point(A), Point(C)).is_parallel(Line(Ai, Ci)), "2402 parallèles")
ok(orient(A, B, C) * orient(Ai, Bi, Ci) > 0, "2402 même orientation")

# ------------------------------------------------------------------ 2403 translation P(1;5) → Q(5;7)
u = (4, 2)
A, B, C = (1, 1), (4, 1), (2, 3)
img = [Point(p[0] + u[0], p[1] + u[1]) for p in (A, B, C)]
ok(img == [Point(5, 3), Point(8, 3), Point(6, 5)], "2403 images")
ok(Point(A).midpoint(img[1]) == Point(B).midpoint(img[0]), "2403 ABB'A' parallélogramme (diagonales)")
ok(img[0].distance(img[1]) == 3, "2403 A'B' = 3")

# ------------------------------------------------------------------ 2404 quart de tour direct, O(5 ; 4)
O = (5, 4)
A, B, C = (7, 4), (9, 4), (8, 6)
img = [rot(p, O, 90) for p in (A, B, C)]
ok(img == [Point(5, 6), Point(5, 8), Point(3, 7)], "2404 images")
ok(Point(O).distance(img[0]) == Point(O).distance(Point(A)) == 2, "2404 OA = OA'")
ok(rot(A, O, 180) == sym_centre(A, O), "2404 deux quarts de tour = symétrie centrale")
ok(rot(A, O, 360) == Point(A), "2404 quatre quarts de tour")

# ------------------------------------------------------------------ 2405 grandeurs conservées
a, b, c = 4, 6, 7
s = R(a + b + c, 2)
ok(abs(float(sqrt(s * (s - a) * (s - b) * (s - c))) - 12) < .05, "2405 aire ≈ 12 (Héron)")
ok(a + b + c == 17 and 3 * 17 == 51 and 3 ** 2 * 12 == 108, "2405 périmètres et aire")

# ------------------------------------------------------------------ 2406 reconnaître
G = [(1, 4), (2, 4), (2, 6), (3, 6), (3, 7), (1, 7)]
F1 = [(x, y - 4) for x, y in G]
F2 = [sym_axe(p, (Point(R(9, 2), 0), Point(R(9, 2), 1))) for p in G]
F3 = [sym_centre(p, (5, R(7, 2))) for p in G]
F4 = [(y + 7, 6 - x) for x, y in G]
F4r = [rot(p, (R(13, 2), R(-1, 2)), -90) for p in G]
F5 = [homot(p, (21, -3), R(1, 2)) for p in G]
ok(F2 == [Point(9 - x, y) for x, y in G], "2406 F2 symétrie axiale")
ok([Point(p) for p in F4] == F4r, "2406 F4 quart de tour horaire de centre (6,5 ; -0,5)")
ok(F5 == [Point(R(1, 2) * x + R(21, 2), R(1, 2) * y - R(3, 2)) for x, y in G], "2406 F5 homothétie de rapport 1/2")
ok(sym_centre((1, 4), (5, R(7, 2))) == Point(9, 3), "2406 segment de construction de F3")
ok(aire(*F5) == aire(*G) / 4, "2406 aire de F5")

# ------------------------------------------------------------------ 2407 rapports
for k, oap, agr, cote in ((4, 16, True, 1), (R(1, 2), 2, False, 1), (-2, 8, True, -1), (R(-1, 4), 1, False, -1), (-1, 4, None, -1)):
    ok(Abs(k) * 4 == oap, "2407 OA' pour k = %s" % k)

# ------------------------------------------------------------------ 2408 homothétie k = 2, O(1 ; 1)
O = (1, 1)
A, B, C = (4, 2), (6, 2), (5, 4)
img = [homot(p, O, 2) for p in (A, B, C)]
ok(img == [Point(7, 3), Point(11, 3), Point(9, 7)], "2408 images")
ok(aire(A, B, C) == 2 and aire(*img) == 8, "2408 aires")
ok(Point(A).distance(Point(B)) == 2 and img[0].distance(img[1]) == 4, "2408 longueurs")

# ------------------------------------------------------------------ 2409 homothétie k = -1/2, O(7 ; 4)
O = (7, 4)
A, B, C = (1, 2), (5, 2), (3, 6)
img = [homot(p, O, R(-1, 2)) for p in (A, B, C)]
ok(img == [Point(10, 5), Point(8, 5), Point(9, 3)], "2409 images")
ok(aire(A, B, C) == 8 and aire(*img) == 2, "2409 aires")
ok(Point(A).distance(Point(B)) == 4 and img[0].distance(img[1]) == 2, "2409 longueurs")

# ------------------------------------------------------------------ 2410
k = R(10, 4)
ok(k == R(5, 2) and 3 * k == R(15, 2) and 6 * k ** 2 == R(75, 2), "2410")

# ------------------------------------------------------------------ 2411
ok(18 * 3 == 54 and 20 * 9 == 180 and 18 * R(1, 2) == 9 and 20 * R(1, 4) == 5, "2411 Q1-Q3")
ok(50 * 8 == 400 and 50 * R(1, 5) ** 3 == R(2, 5), "2411 Q4-Q5")

# ------------------------------------------------------------------ 2412 maquette 1/100
k = R(1, 100)
ok(3000 * k == 30, "2412 façade 30 cm")
ok(450 * 10 ** 4 * k ** 2 == 450, "2412 surface 450 cm²")
ok(6000 * 10 ** 6 * k ** 3 == 6000 and R(6000, 1000) == 6, "2412 volume 6 000 cm³ = 6 L")

# ------------------------------------------------------------------ 2413 frise
CH = [(R(1, 2), R(1, 2)), (R(5, 2), R(1, 2)), (R(7, 2), R(3, 2)), (R(5, 2), R(5, 2)), (R(1, 2), R(5, 2)), (R(3, 2), R(3, 2))]
ok(aire(*CH) == 4, "2413 aire du motif 4 cm²")
ok(5 * 4 == 20 and 3 * 4 == 12 and 100 // 4 == 25 and 6 * 4 == 24, "2413 distances et nombre de motifs")

# ------------------------------------------------------------------ 2414 rosace
ok(R(360, 8) == 45 and 3 * 45 == 135 and R(180, 45) == 4 and R(360, 12) == 30, "2414")
ok(round(360 / 7, 1) == 51.4, "2414 sept pétales")

# ------------------------------------------------------------------ 2415 centre Ω(1 ; 1), k = 2
W = (1, 1)
pts = [(3, 3), (5, 3), (3, 4)]
img = [homot(p, W, 2) for p in pts]
ok(img == [Point(5, 5), Point(9, 5), Point(5, 7)], "2415 images")
L1 = Line(Point(pts[0]), img[0])
L2 = Line(Point(pts[1]), img[1])
ok(L1.intersection(L2) == [Point(W)], "2415 (AA') et (BB') se coupent en Ω")
ok(Line(Point(pts[2]), img[2]).contains(Point(W)), "2415 (CC') passe par Ω")
ok(aire(*pts) == 1 and aire(*img) == 4, "2415 aires")

# ------------------------------------------------------------------ 2416
ok(R(75, 12) == R(25, 4) and sqrt(R(25, 4)) == R(5, 2) and 4 * R(5, 2) == 10, "2416")

# ------------------------------------------------------------------ 2417 pavage
T1 = [(0, 0), (2, 0), (2, 2)]
T2 = {Point(0, 0), Point(2, 2), Point(0, 2)}
T3 = {Point(4, 0), Point(6, 0), Point(6, 2)}
T4 = {Point(2, 2), Point(4, 2), Point(4, 4)}
T5 = {Point(2, 0), Point(4, 2), Point(2, 2)}
ok({Point(x + 4, y) for x, y in T1} == T3, "2417 T1 → T3")
ok({Point(x + 2, y + 2) for x, y in T1} == T4, "2417 T1 → T4")
ok({sym_centre(p, (1, 1)) for p in T1} == T2, "2417 T1 → T2 symétrie centrale")
ok({sym_axe(p, (Point(0, 0), Point(1, 1))) for p in T1} == T2, "2417 T1 → T2 symétrie axiale")
ok({sym_centre(p, (2, 1)) for p in T1} == T5, "2417 T1 → T5")
ok(all({Point(x + a, y + b) for x, y in T1} != T5 for a in range(-4, 5) for b in range(-4, 5)), "2417 pas de translation")
ok(aire(*T1) == 2 and R(8 * 4, 2) == 16, "2417 aires et nombre de pièces")

# ------------------------------------------------------------------ 2418 logo
ok(5 ** 2 == 3 ** 2 + 4 ** 2 and R(3 * 4, 2) == 6, "2418 Q1-Q2")
ok((3 * 8, 4 * 8, 5 * 8) == (24, 32, 40) and R(24 * 32, 2) == 384 and 6 * 64 == 384, "2418 Q3-Q4")
ok(384 * R(2, 100) == R(768, 100), "2418 Q5 7,68 €")

# ------------------------------------------------------------------ 2419 projecteur
k = R(400, 5)
ok(k == 80 and R(36, 10) * k == 288, "2419 Q2-Q3")
ok(R(36, 10) * R(24, 10) == R(864, 100), "2419 diapositive 3,6 × 2,4")
ok(R(864, 100) * k ** 2 == 55296 and abs(55296 / 10 ** 4 - 5.53) < .005, "2419 Q4")
ok(R(216, 1) / R(36, 10) == 60 and 60 * 5 == 300, "2419 Q5")

# ------------------------------------------------------------------ 2420 parallélogramme
A, B, C = Point(1, 1), Point(5, 2), Point(6, 5)
D = C + (A - B)
ok(D == Point(2, 4), "2420 D")
ok(A.midpoint(C) == B.midpoint(D) == Point(R(7, 2), 3), "2420 milieu commun I")
ok(sym_centre(A, (R(7, 2), 3)) == C and sym_centre(B, (R(7, 2), 3)) == D, "2420 symétrie de centre I")
ok(A.distance(B) == sqrt(17) == C.distance(D) and abs(float(sqrt(17)) - 4.12) < .005, "2420 AB = CD = √17")

# ------------------------------------------------------------------ 2421 pyramide
h = R(3 * 1350, 225)
ok(h == 18 and h / 3 == 6 and sqrt(225) == 15 and R(15, 3) == 5, "2421 hauteur et côtés")
ok(225 * R(1, 9) == 25 and 1350 * R(1, 27) == 50 and R(25 * 6, 3) == 50, "2421 section et petit volume")
ok(1350 - 50 == 1300 and R(1300, 1350) == R(26, 27) and round(float(R(2600, 27)), 1) == 96.3, "2421 tronc")

# ------------------------------------------------------------------ cours
O = (4, 2)
ok(rot((2, 3), O, -90) == Point(5, 4), "cours rotation horaire A'")
ok([homot(p, (0, 1), 3) for p in ((2, 2), (3, 2), (2, 3))] == [Point(6, 4), Point(9, 4), Point(6, 7)], "cours k = 3")
ok([homot(p, (5, 4), -2) for p in ((7, 3), (8, 5), (6, 6))] == [Point(1, 6), Point(-1, 2), Point(3, 0)], "cours k = -2")
ok([sym_axe(p, (Point(0, 0), Point(1, 1))) for p in ((1, 3), (2, 6), (4, 6))] == [Point(3, 1), Point(6, 2), Point(6, 4)], "cours axe y = x")
ok([sym_centre(p, (5, 3)) for p in ((1, 4), (4, 4), (3, 6))] == [Point(9, 2), Point(6, 2), Point(7, 0)], "cours symétrie centrale")
ok(R(1, 2) ** 2 == R(1, 4) and R(1, 2) ** 3 == R(1, 8) and R(360, 6) == 60, "cours exemples")
ok(Abs(R(-1, 2)) * 6 == 3, "cours exemple k = -0,5")

print("verif_246 : %d contrôles OK" % n_ok)
