# -*- coding: utf-8 -*-
"""Vérification (sympy) des calculs du cours, de la fiche, des 21 exercices
et des coordonnées des figures de la notion 288 (4e)."""
import importlib.util
import math
from pathlib import Path

import sympy as sp
from sympy import Rational as R, sqrt, Point, Polygon, pi, Matrix

ICI = Path(__file__).resolve().parent
n_ok = 0
erreurs = []


def ok(cond, msg):
    global n_ok
    if bool(cond):
        n_ok += 1
    else:
        erreurs.append(msg)


def eg(a, b, msg):
    ok(sp.simplify(sp.nsimplify(a) - sp.nsimplify(b)) == 0, f"{msg} : {a} ≠ {b}")


def arr(x, n):
    """Arrondi décimal à n chiffres (exact)."""
    return sp.Float(round(float(x), n), 15)


def proche(x, v, n, msg):
    ok(abs(float(x) - v) < 10 ** (-n) / 2 + 1e-12, f"{msg} : {float(x)} ≉ {v}")


# ------------------------------------------------------------------ figures
spec = importlib.util.spec_from_file_location("fig288", ICI / "figures" / "figures.py")
fig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fig)
D = fig.DONNEES


def T(v):
    return lambda p: (p[0] + v[0], p[1] + v[1])


def sym_axe_vertical(a):
    return lambda p: (2 * a - p[0], p[1])


def sym_centre(o):
    return lambda p: (2 * o[0] - p[0], 2 * o[1] - p[1])


def homothetie(k, o, dest):
    return lambda p: (dest[0] + k * (p[0] - o[0]), dest[1] + k * (p[1] - o[1]))


def meme(l1, l2, msg):
    ok(all(abs(a[0] - b[0]) < 1e-9 and abs(a[1] - b[1]) < 1e-9 for a, b in zip(l1, l2)) and len(l1) == len(l2), msg)


def aire(pts):
    return abs(Polygon(*[Point(sp.nsimplify(x), sp.nsimplify(y)) for x, y in pts]).area)


def dist(p, q):
    return sqrt((sp.nsimplify(p[0]) - sp.nsimplify(q[0])) ** 2 + (sp.nsimplify(p[1]) - sp.nsimplify(q[1])) ** 2)


# cours : translation (7 ; 2)
c = D["cours_translation"]
meme(c["A'B'C'"], [T((7, 2))(p) for p in c["ABC"]], "cours : image A'B'C'")
eg(aire(c["ABC"]), aire(c["A'B'C'"]), "cours : aire conservée")
# cours : parallélogramme AA'M'M
p = D["cours_parallelogramme"]
ok(abs(p["M'"][0] - p["M"][0] - (p["A'"][0] - p["A"][0])) < 1e-9 and abs(p["M'"][1] - p["M"][1] - (p["A'"][1] - p["A"][1])) < 1e-9,
   "cours : MM' = AA'")
eg(dist(p["A'"], p["M'"]), dist(p["A"], p["M"]), "cours : A'M' = AM")
# cours : trois transformations
t3 = D["cours_trois"]
meme(t3["axiale (x=4)"], [sym_axe_vertical(4)(q) for q in t3["depart"]], "cours : symétrie axiale")
meme(t3["centrale (3,5 ; 2,5)"], [sym_centre((3.5, 2.5))(q) for q in t3["depart"]], "cours : symétrie centrale")
meme(t3["translation (+4 ; 0)"], [T((4, 0))(q) for q in t3["depart"]], "cours : translation du panneau")
# cours : agrandissement
ca = D["cours_agrandissement"]
for k, key in ((R(1, 2), "k=0,5"), (2, "k=2")):
    for a, b in zip(ca["depart"], ca[key]):
        ok(abs(b[0] - float(k) * a[0]) < 1e-9 and abs(b[1] - float(k) * a[1]) < 1e-9, f"cours : {key}")
    eg(aire(ca[key]), k ** 2 * aire(ca["depart"]), f"cours : aire × k² ({key})")
# cours : pavage de chevrons (2 ; 0) et (0 ; 2) sans trou : aire d'un chevron = 4 = 2 × 2
eg(aire(fig.CHEVRON), 4, "cours : aire du chevron = aire de la maille 2 × 2")
# cours : textes
eg(R(8, 4), 2, "cours : k = 8/4")
eg(3 * 2, 6, "cours : 3 × 2")
eg(5 * 2, 10, "cours : 5 × 2")
eg((3 + 4 + 5) * 2, 24, "cours : périmètre 24")
eg(8 * 50, 400, "cours : 8 × 50")
eg(R(120, 50), R(12, 5), "cours : 120 ÷ 50 = 2,4")
eg(R(10, 400), R(1, 40), "cours : échelle 1/40")
eg(6 * 4, 24, "cours : rectangle 6 × 4")
eg(R(1, 2), sp.Float(0.5), "cours : 1/2 = 0,5")
eg(3 + 1, 4, "cours : enchaînement 3 + 1")

# ------------------------------------------------------------------ 3671
e = D["ex3671"]
S = e["S"]
meme(e["a"], [T((5, 1))(q) for q in S], "3671 a : translation (5 ; 1)")
meme(e["b"], [sym_axe_vertical(5)(q) for q in S], "3671 b : symétrie d'axe x = 5")
meme(e["c"], [sym_centre((5, 2.5))(q) for q in S], "3671 c : symétrie de centre (5 ; 2,5)")
meme(e["d"], [homothetie(2, (1, 1), (5, 1))(q) for q in S], "3671 d : agrandissement × 2")
ok(max(x for x, _ in S) - min(x for x, _ in S) == 2 and max(y for _, y in S) - min(y for _, y in S) == 3, "3671 : 2 × 3 carreaux")
xs = [x for x, _ in e["d"]]
ys = [y for _, y in e["d"]]
ok(max(xs) - min(xs) == 4 and max(ys) - min(ys) == 6, "3671 d : 4 × 6 carreaux")
ok(all(0 <= x <= 10 and 0 <= y <= 8 for k in "abcd" for x, y in e[k]), "3671 : dans le quadrillage")

# ------------------------------------------------------------------ 3672
e = D["ex3672"]
v = (e["A'"][0] - e["A"][0], e["A'"][1] - e["A"][1])
ok(v == (3, 2), "3672 : déplacement (3 ; 2)")
ok(e["B'"] == (5, 6) and e["C'"] == (1, 5) and e["D'"] == (2, 0), "3672 : B', C', D'")
ok(e["E"] == (-2, -1) and T(v)(e["E"]) == e["A"], "3672 : E")
eg(dist(e["A"], e["A'"]), sqrt(13), "3672 : AA' = √13")
proche(sqrt(13), 3.6, 1, "3672 : √13 ≈ 3,6")

# ------------------------------------------------------------------ 3673
e = D["ex3673"]
meme(e["A'B'C'"], [T((5, 2))(q) for q in e["ABC"]], "3673 : image")
A, B, C = e["ABC"]
eg(dist(A, B), 4, "3673 : AB = 4")
eg(C[1] - A[1], 3, "3673 : hauteur 3")
eg(aire(e["ABC"]), 6, "3673 : aire 6")
eg(aire(e["A'B'C'"]), 6, "3673 : aire image 6")

# ------------------------------------------------------------------ 3674
e = D["ex3674"]
eg(dist(e["A"], e["B"]), 5, "3674 : AB = 5")
eg(dist(e["A"], e["M"]), 3, "3674 : AM = 3")
eg(dist(e["M"], e["M'"]), 5, "3674 : MM' = 5")
eg(dist(e["B"], e["M'"]), 3, "3674 : BM' = 3")
eg(dist(e["A"], e["C"]), 10, "3674 : AC = 10")
ok(Point(*map(sp.nsimplify, e["A"])).is_collinear(Point(*map(sp.nsimplify, e["B"])), Point(*map(sp.nsimplify, e["C"]))), "3674 : A, B, C alignés")
ok(not Point(*map(sp.nsimplify, e["A"])).is_collinear(Point(*map(sp.nsimplify, e["B"])), Point(*map(sp.nsimplify, e["M"]))), "3674 : M hors de (AB)")
eg(5 + 3 + 5 + 3, 16, "3674 : périmètre")

# ------------------------------------------------------------------ 3675
eg(3 * 2, 6, "3675 : 3 × 2")
eg(2 * 2, 4, "3675 : 2 × 2")
eg(2 * (3 + 2), 10, "3675 : périmètre petit")
eg(2 * (6 + 4), 20, "3675 : périmètre grand")
eg(6 * 4, 24, "3675 : aire grand")
eg(R(24, 6), 4, "3675 : aire × 4")
eg(R(3, 6), R(1, 2), "3675 : k retour 0,5")
eg(R(75, 10) / 3, R(5, 2), "3675 : k = 2,5")
eg(2 * R(5, 2), 5, "3675 : largeur 5")

# ------------------------------------------------------------------ 3676
e = D["ex3676"]
eg(dist(e["R"], e["T"]), 6, "3676 : RT")
eg(dist(e["S"], e["T"]), 8, "3676 : ST")
eg(dist(e["R"], e["S"]), 10, "3676 : RS")
eg(dist(e["R'"], e["S'"]), 5, "3676 : R'S'")
eg(dist(e["S'"], e["T'"]), 4, "3676 : S'T'")
eg(dist(e["R'"], e["T'"]), 3, "3676 : R'T'")
eg(5 ** 2, 4 ** 2 + 3 ** 2, "3676 : réciproque de Pythagore")
eg(10 + 8 + 6, 24, "3676 : périmètre 24")
eg(5 + 4 + 3, 12, "3676 : périmètre 12")
eg(R(75, 10) / 10, R(3, 4), "3676 : k = 0,75")
eg(8 * R(3, 4), 6, "3676 : 8 × 0,75")
eg(6 * R(3, 4), R(9, 2), "3676 : 6 × 0,75")
eg(10 / R(75, 10), R(4, 3), "3676 : 10/7,5 = 4/3")
proche(R(4, 3), 1.33, 2, "3676 : 4/3 ≈ 1,33")

# ------------------------------------------------------------------ 3677
eg(4 * R(3, 2), 6, "3677 : 4 × 1,5")
eg(R(36, 9), 4, "3677 : 36/9")

# ------------------------------------------------------------------ 3678
largeur = max(x for x, _ in fig.MOTIF78) - min(x for x, _ in fig.MOTIF78)
ok(largeur < 3, "3678 : motifs séparés (largeur < 3)")
for de, a, att in ((1, 2, 3), (1, 4, 9), (1, 8, 21), (1, 20, 57)):
    eg((a - de) * 3, att, f"3678 : motif {de} → {a}")
eg((5 - 2) * 3, 9, "3678 : motif 5 → 2")
eg(100 / R(5, 2), 40, "3678 : 40 motifs")
eg(39 * R(5, 2), R(195, 2), "3678 : 97,5 cm")

# ------------------------------------------------------------------ 3679
e = D["ex3679"]
F, ax, O, E = e["F"], e["axe x"], e["O"], e["E"]
for k in F:
    ok(e["F1"][k] == sym_axe_vertical(ax)(F[k]), f"3679 : F1 {k}")
    ok(e["F2"][k] == sym_centre(O)(F[k]), f"3679 : F2 {k}")
    ok(e["F3"][k] == T((E[0] - F["A"][0], E[1] - F["A"][1]))(F[k]), f"3679 : F3 {k}")
ok(ax - F["C"][0] == 2, "3679 : C à 2 carreaux de (d)")
ok(ax - F["A"][0] == 5 and ax - F["B"][0] == 5 and ax - F["D"][0] == 5, "3679 : A, B, D à 5 carreaux")
ok((O[0] - F["C"][0], O[1] - F["C"][1]) == (-1, -3), "3679 : de C à O, 1 à gauche, 3 en bas")
ok(e["F2"]["C"] == (O[0] - 1, O[1] - 3), "3679 : C2")
ok((O[0] - F["A"][0], O[1] - F["A"][1]) == (2, 0), "3679 : de A à O, 2 à droite")
ok((E[0] - F["A"][0], E[1] - F["A"][1]) == (8, -5), "3679 : de A à E, 8 à droite, 5 en bas")
eg(aire([F["B"], F["C"], F["D"]]), 3, "3679 : aire du fanion 3")
for cle in ("F1", "F2", "F3"):
    d = e[cle]
    eg(aire([d["B"], d["C"], d["D"]]), 3, f"3679 : aire du fanion de {cle}")
ok(e["F1"]["B"][1] > e["F1"]["A"][1] and e["F1"]["C"][0] < e["F1"]["B"][0], "3679 : F1 mât en haut, fanion à gauche")
ok(e["F2"]["B"][1] < e["F2"]["A"][1] and e["F2"]["C"][0] < e["F2"]["B"][0], "3679 : F2 mât en bas, fanion à gauche")
ok(e["F3"]["B"][1] > e["F3"]["A"][1] and e["F3"]["C"][0] > e["F3"]["B"][0], "3679 : F3 mât en haut, fanion à droite")
ok(all(0 <= x <= 13 and 0 <= y <= 11 for cle in ("F1", "F2", "F3") for x, y in e[cle].values()), "3679 : dans le quadrillage")

# ------------------------------------------------------------------ 3680
e = D["ex3680"]
eg(dist(e["E"], e["F"]), 4, "3680 : EF")
eg(dist(e["E"], e["G"]), 3, "3680 : EG")
eg(dist(e["F"], e["G"]), 5, "3680 : FG")
eg(dist(e["E'"], e["F'"]), 4, "3680 : E'F'")
eg(dist(e["E'"], e["G'"]), 3, "3680 : E'G'")
eg(dist(e["F'"], e["G'"]), 5, "3680 : F'G'")
eg(dist(e["F"], e["F'"]), dist(e["E"], e["E'"]), "3680 : FF' = EE'")
eg(4 ** 2 + 3 ** 2, 5 ** 2, "3680 : Pythagore")
eg(R(4 * 3, 2), 6, "3680 : aire 6")
v1 = Matrix([e["F"][0] - e["E"][0], e["F"][1] - e["E"][1]])
v2 = Matrix([e["G"][0] - e["E"][0], e["G"][1] - e["E"][1]])
eg(v1.dot(v2), 0, "3680 : angle droit en E")

# ------------------------------------------------------------------ 3681
eg(9 * 50, 450, "3681 : 450")
eg(7 * 50, 350, "3681 : 350")
eg(R(18, 10) * 50, 90, "3681 : porte 90")
eg(R(45, 10) * R(35, 10), R(1575, 100), "3681 : 15,75 m²")
eg(R(200, 50), 4, "3681 : lit 4")
eg(R(160, 50), R(32, 10), "3681 : lit 3,2")
eg(9 * 7, 63, "3681 : 63 cm²")
eg(450 * 350, 157500, "3681 : 157 500 cm²")
eg(R(157500, 63), 2500, "3681 : × 2 500")
eg(63 * 50, 3150, "3681 : 3 150")
eg(R(157500, 10000), R(1575, 100), "3681 : conversion m²")

# ------------------------------------------------------------------ 3682
eg(R(20, 10), 2, "3682 : 20/10")
eg(R(30, 15), 2, "3682 : 30/15")
eg(R(13, 10), R(13, 10), "3682 : 13/10")
eg(R(18, 15), R(6, 5), "3682 : 18/15 = 1,2")
eg(15 * R(13, 10), R(195, 10), "3682 : 19,5")
eg(R(50, 10) * 15, 75, "3682 : 75")
eg(R(6, 10) * 15, 9, "3682 : 9")
proche(R(18, 13), 1.38, 2, "3682 : 18/13 ≈ 1,38")
ok(R(15, 10) == R(30, 20), "3682 : même rapport")

# ------------------------------------------------------------------ 3683
e = D["ex3683"]
M, M1, M2 = e["M"], e["M1"], e["M2"]
eg(aire(M), 20, "3683 : aire M")
eg(aire(M1), 5, "3683 : aire M1")
eg(aire(M2), 45, "3683 : aire M2")
eg(R(5, 20), R(1, 4), "3683 : × 0,25")
eg(R(45, 20), R(9, 4), "3683 : × 2,25")
toit = dist(M[4], M[3])
eg(toit, sqrt(8), "3683 : côté du toit √8")
proche(toit, 2.8, 1, "3683 : ≈ 2,8")
proche(toit / 2, 1.4, 1, "3683 : M1 ≈ 1,4")
proche(toit * R(3, 2), 4.2, 1, "3683 : M2 ≈ 4,2")
eg(R(28, 10) * R(1, 2), R(14, 10), "3683 : 2,8 × 0,5")
eg(R(28, 10) * R(3, 2), R(42, 10), "3683 : 2,8 × 1,5")
for maison, nom in ((M, "M"), (M1, "M1"), (M2, "M2")):
    s, g, d = maison[3], maison[4], maison[2]
    eg((g[0] - s[0]) * (d[0] - s[0]) + (g[1] - s[1]) * (d[1] - s[1]), 0, f"3683 : angle droit du toit {nom}")
ok(max(x for x, _ in M2) <= 18 and max(y for _, y in M2) <= 11, "3683 : M2 dans le quadrillage")
for a, b in zip(fig.MAISON, M2):
    ok(abs(b[0] - 11 - 1.5 * a[0]) < 1e-9 and abs(b[1] - 1 - 1.5 * a[1]) < 1e-9, "3683 : M2 = 1,5 × M")

# ------------------------------------------------------------------ 3684
e = D["ex3684"]
eg(dist(e["D"], e["E"]), 6, "3684 : DE")
eg(dist(e["E"], e["F"]), 8, "3684 : EF")
eg(dist(e["D"], e["F"]), 5, "3684 : DF")
eg(dist(e["D'"], e["E'"]), 9, "3684 : D'E'")
eg(dist(e["E'"], e["F'"]), 12, "3684 : E'F'")
eg(dist(e["D'"], e["F'"]), R(15, 2), "3684 : D'F'")
angE = sp.acos(R(6 ** 2 + 8 ** 2 - 5 ** 2, 2 * 6 * 8)) * 180 / pi
ok(round(float(angE)) == 39, f"3684 : angle E ≈ 39° ({float(angE):.2f})")
eg(R(9, 6), R(3, 2), "3684 : k = 1,5")
eg(6 + 8 + 5, 19, "3684 : périmètre 19")
eg(9 + 12 + R(15, 2), R(57, 2), "3684 : périmètre 28,5")
eg(19 * R(3, 2), R(57, 2), "3684 : 19 × 1,5")
ok(R(12, 6) == R(16, 8) and R(11, 5) != 2, "3684 : GHI non")
eg(R(11, 5), R(22, 10), "3684 : 11/5 = 2,2")
ok(R(3, 6) == R(4, 8) == R(5, 2) / 5 == R(1, 2), "3684 : JKL réduction 0,5")
ok(6 + 5 > 8 and 12 + 11 > 16 and 3 + R(5, 2) > 4, "3684 : triangles constructibles")

# ------------------------------------------------------------------ 3685
e = D["ex3685"]
base = e["1"]
ok(base[1][0] - base[0][0] == 3 and base[3][1] - base[0][1] == 2, "3685 : base 3, hauteur 2")
for n, v in (("2", (3, 0)), ("3", (1, 2)), ("4", (4, 2)), ("5", (11, 4))):
    meme(e[n], [T(v)(q) for q in base], f"3685 : carreau 1 → {n}")
eg(3 * 3 + 2 * 1, 11, "3685 : 11")
eg(3 * 0 + 2 * 2, 4, "3685 : 4")
eg(aire(base), 6, "3685 : aire 6")
eg(R(96, 6), 16, "3685 : 16 carreaux")

# ------------------------------------------------------------------ 3686
e = D["ex3686"]
ok(e["R_1"] == T((3, 2))(e["R"]), "3686 : R1")
ok(e["R_2"] == T((2, -4))(e["R_1"]), "3686 : R2")
ok(e["P"] == T((2, -4))(e["R"]) and T((3, 2))(e["P"]) == e["R_2"], "3686 : ordre inverse")
ok((e["R_2"][0] - e["R"][0], e["R_2"][1] - e["R"][1]) == (5, -2), "3686 : translation unique")
proche(sqrt(13), 3.61, 2, "3686 : √13")
proche(sqrt(20), 4.47, 2, "3686 : √20")
proche(sqrt(29), 5.39, 2, "3686 : √29")
proche(sqrt(13) + sqrt(20), 8.08, 2, "3686 : 8,08")
proche(sqrt(13) + sqrt(20) - sqrt(29), 2.69, 2, "3686 : 2,69")
eg(R(808, 100) - R(539, 100), R(269, 100), "3686 : 8,08 − 5,39")

# ------------------------------------------------------------------ 3687
e = D["ex3687"]
eg(aire(e["depart"]), 12, "3687 : aire 12")
eg(aire(e["agrandi"]), 27, "3687 : aire 27")
cotes = [dist(e["depart"][i], e["depart"][(i + 1) % 6]) for i in range(6)]
ok(cotes == [4, 2, 2, 2, 2, 4], f"3687 : côtés {cotes}")
cotes2 = [dist(e["agrandi"][i], e["agrandi"][(i + 1) % 6]) for i in range(6)]
ok(cotes2 == [6, 3, 3, 3, 3, 6], f"3687 : côtés agrandis {cotes2}")
eg(sum(cotes), 16, "3687 : périmètre 16")
eg(sum(cotes2), 24, "3687 : périmètre 24")
eg(R(27, 12), R(9, 4), "3687 : × 2,25")
eg(12 * R(3, 2), 18, "3687 : erreur 18")
eg(R(75, 12), R(25, 4), "3687 : 6,25")
eg(sqrt(R(25, 4)), R(5, 2), "3687 : k = 2,5")
eg(10 * 10 - 5 * 5, 75, "3687 : vérification 75")

# ------------------------------------------------------------------ 3688
eg(15 * 200, 3000, "3688 : 3 000")
eg(8 * 200, 1600, "3688 : 1 600")
eg(2 * 200, 400, "3688 : bassin 400")
eg(2 * (30 + 16), 92, "3688 : clôture")
eg(2 * (15 + 8) * 200, 9200, "3688 : vérification")
eg(30 * 16, 480, "3688 : aire 480")
proche(4 * pi, 12.57, 2, "3688 : bassin ≈ 12,57")
proche(480 - 4 * pi, 467.4, 1, "3688 : pelouse ≈ 467,4")
proche(R(4674, 10) * 35, 16359, 0, "3688 : graines ≈ 16 359 g")
proche((480 - 4 * pi) * 35, 16360, -1, "3688 : ≈ 16 360 g")
ok(3 * 5000 < (480 - 4 * pi) * 35 <= 4 * 5000, "3688 : 4 sacs")
eg(15 * 8, 120, "3688 : 120 cm²")
eg(480 * 10000, 4800000, "3688 : 4 800 000")
eg(120 * 200 * 200, 4800000, "3688 : 120 × 40 000")

# ------------------------------------------------------------------ 3689
eg(R(33000, 1000), 33, "3689 : 33 cm")
eg(R(12500, 1000), R(25, 2), "3689 : 12,5 cm")
eg(R(165, 10) / 33000, R(1, 2000), "3689 : 1/2000")
eg(R(11500, 2000), R(23, 4), "3689 : 5,75")
eg(R(165, 330), R(1, 2), "3689 : 0,5")
eg(16500 / R(165, 10), 1000, "3689 : 1 000")
eg(R(165, 10) / 330, R(1, 20), "3689 : erreur 1/20")

# ------------------------------------------------------------------ 3690
w5, h5 = map(sp.nsimplify, D["ex3690"]["A5"])
w4, h4 = map(sp.nsimplify, D["ex3690"]["A4"])
w3, h3 = map(sp.nsimplify, D["ex3690"]["A3"])
eg(h4 / 2, w5, "3690 : A5 = 29,7/2")
eg(2 * w4, h3, "3690 : A3 = 2 × 21")
proche(w5 / w4, 0.707, 3, "3690 : 14,85/21")
proche(w4 / h4, 0.707, 3, "3690 : 21/29,7")
proche(h4 / w4, 1.414, 3, "3690 : 29,7/21")
proche(h3 / h4, 1.414, 3, "3690 : 42/29,7")
eg(R(707, 1000) * R(1414, 1000), R(999698, 1000000), "3690 : produit")
eg(w5 * h5, R(31185, 100), "3690 : aire A5")
eg(w4 * h4, R(6237, 10), "3690 : aire A4")
eg(w3 * h3, R(12474, 10), "3690 : aire A3")
eg(2 * w5 * h5, w4 * h4, "3690 : aire double A5 → A4")
eg(2 * w4 * h4, w3 * h3, "3690 : aire double A4 → A3")
proche(R(707, 1000) ** 2, 0.5, 3, "3690 : 0,707² ≈ 0,5")

# ------------------------------------------------------------------ 3691
e = D["ex3691"]
eg(R(200 * 10, 50), 40, "3691 : A'B' = 40")
ok(e["B'"][1] * 10 == 40 and e["A'"][0] * 10 == 200 and e["A"][0] * 10 == 50 and e["B"][1] * 10 == 10, "3691 : figure à l'échelle")
ok(Point(*e["L"]).is_collinear(Point(*e["B"]), Point(*e["B'"])), "3691 : L, B, B' alignés")
eg(R(40, 10), 4, "3691 : k = 4")
eg(R(200, 50), 4, "3691 : LA'/LA = 4")
eg(6 * 4, 24, "3691 : largeur 24")
eg(R(100, 10), 10, "3691 : k = 10")
eg(R(200, 10), 20, "3691 : LA = 20")
eg(R(300, 50), 6, "3691 : k = 6")
eg(10 * 6, 60, "3691 : 60 cm")

print(f"{n_ok} contrôles justes, {len(erreurs)} erreur(s)")
for m in erreurs:
    print("  ERREUR :", m)
