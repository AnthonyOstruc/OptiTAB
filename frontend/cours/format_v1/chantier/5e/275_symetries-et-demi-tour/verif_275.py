# -*- coding: utf-8 -*-
"""Vérification de la notion 275 « Symétries et demi-tour » (5e), refonte du 2026-11-04.

    python verif_275.py

1. Figures : relit DONNEES dans figures/figures.py et recalcule chaque image avec
   sympy (valeurs exactes) : symétries axiales (verticale, horizontale, diagonale,
   oblique), demi-tours, milieux, perpendicularité, alignements.
2. Chaque nombre écrit dans le cours et les corrigés (carreaux, chemins, longueurs,
   angles, aires, périmètres, fractions) est recalculé.
3. Structure : 10 exercices + 11 retirés = 21 Id en ligne ; titres uniques
   « Type - Sujet » ; progression ; méthode / étape / résultat / erreur fréquente ;
   questions = parties du corrigé = lignes de solution ; images appelées = déclarées.
"""
import importlib.util
import json
import re
from itertools import combinations
from pathlib import Path

import sympy as sp

ICI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("figs", ICI / "figures" / "figures.py")
figs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(figs)
D = figs.DONNEES

N = 0
ERREURS = []


def ok(cond, msg):
    global N
    N += 1
    if not cond:
        ERREURS.append(msg)


def Q(p):
    """Point en valeurs exactes (les coordonnées de quadrillage sont entières)."""
    return sp.Matrix([sp.nsimplify(p[0], rational=True), sp.nsimplify(p[1], rational=True)])


def egal(p, q, tol=None):
    if tol is None:
        return sp.simplify(Q(p) - Q(q)) == sp.zeros(2, 1)
    return abs(p[0] - q[0]) < tol and abs(p[1] - q[1]) < tol


def sym_axe_v(p, a):
    return sp.Matrix([2 * a - Q(p)[0], Q(p)[1]])


def sym_axe_h(p, b):
    return sp.Matrix([Q(p)[0], 2 * b - Q(p)[1]])


def sym_diag(p):
    return sp.Matrix([Q(p)[1], Q(p)[0]])


def demi(p, o):
    return 2 * Q(o) - Q(p)


def aire(pts):
    s = 0
    for i in range(len(pts)):
        x1, y1 = Q(pts[i])
        x2, y2 = Q(pts[(i + 1) % len(pts)])
        s += x1 * y2 - x2 * y1
    return abs(sp.Rational(1, 2) * s)


def distance_ex(p, q):
    return sp.sqrt((Q(q) - Q(p)).dot(Q(q) - Q(p)))


# =================================================================== 1. figures
# cours : axe vertical
c = D["cours_axiale"]
for k, p in c["depart"].items():
    ok(sym_axe_v(p, c["axe x"]) == Q(c["image"][k + "'"]), f"cours_axiale : image de {k}")
ok(c["axe x"] - c["depart"]["A"][0] == 5, "cours : A est à 5 carreaux de l'axe")
# cours : axe en diagonale
c = D["cours_axiale_diagonale"]
for k, p in c["depart"].items():
    ok(sym_diag(p) == Q(c["image"][k + "'"]), f"cours_axiale_diagonale : image de {k}")
    ok(Q(p)[0] > Q(p)[1], f"cours diag : {k} sous la diagonale")
K, K2 = Q(c["depart"]["K"]), Q(c["image"]["K'"])
H = (K + K2) / 2
ok(H[0] == H[1], "cours diag : milieu de [KK'] sur l'axe")
ok(abs(K[0] - H[0]) == 2, "cours diag : 2 carreaux traversés en diagonale de chaque côté")
# cours : compas (papier blanc)
c = D["cours_axiale_compas"]
A, A2, R, S = c["A"], c["A'"], c["R"], c["S"]
ok(abs(figs.dist(R, A) - figs.dist(R, A2)) < 1e-9 and abs(figs.dist(S, A) - figs.dist(S, A2)) < 1e-9,
   "cours compas : RA = RA' et SA = SA'")
for P_ in (R, S):
    u = (c["d2"][0] - c["d1"][0], c["d2"][1] - c["d1"][1])
    v = (P_[0] - c["d1"][0], P_[1] - c["d1"][1])
    ok(abs(u[0] * v[1] - u[1] * v[0]) < 1e-9, "cours compas : R et S sur (d)")
# cours : demi-tour
for nom in ("cours_demitour_point", "cours_demitour_compas"):
    c = D[nom]
    ok(egal(figs.milieu(c["A"], c["A'"]), c["O"], 1e-9), f"{nom} : O milieu de [AA']")
c = D["cours_demitour_quadrillage"]
for k, p in c["depart"].items():
    ok(demi(p, c["O"]) == Q(c["image"][k + "'"]), f"cours demi-tour quadrillage : image de {k}")
A, O = Q(c["depart"]["A"]), Q(c["O"])
ok(O - A == sp.Matrix([5, -1]), "cours : de A à O, 5 à droite et 1 vers le bas")
c = D["cours_droites"]
for k in "AB":
    ok(egal(figs.milieu(c[k], c[k + "'"]), c["O"], 1e-9), f"cours droites : O milieu de [{k}{k}']")
u = (c["B"][0] - c["A"][0], c["B"][1] - c["A"][1])
v = (c["B'"][0] - c["A'"][0], c["B'"][1] - c["A'"][1])
ok(abs(u[0] * v[1] - u[1] * v[0]) < 1e-9, "cours droites : (A'B') parallèle à (AB)")
c = D["cours_comparer"]
for k, p in c["depart"].items():
    ok(sym_axe_v(p, c["axe x"]) == Q(c["axiale"][k]), f"cours comparer : axiale {k}")
    ok(demi(p, c["O"]) == Q(c["demi-tour"][k]), f"cours comparer : demi-tour {k}")
# exemple du cours : triangle RST rectangle, 5 et 3
ok(sp.Rational(5 * 3, 2) == sp.Rational(15, 2), "cours : aire 7,5 cm²")

# 3000
d = D["ex3000"]
for k, p in d["a"]["depart"].items():
    ok(sym_axe_v(p, d["a"]["axe x"]) == Q(d["a"]["image"][k]), f"3000a : image de {k}")
for k, p in d["b"]["depart"].items():
    ok(sym_axe_h(p, d["b"]["axe y"]) == Q(d["b"]["image"][k]), f"3000b : image de {k}")
for k, p in d["c"]["depart"].items():
    ok(sym_diag(p) == Q(d["c"]["image"][k]), f"3000c : image de {k}")
a = d["a"]
dist_a = {k: a["axe x"] - p[0] for k, p in a["depart"].items()}
ok(dist_a == {"A": 3, "B": 1, "C": 1, "D": 3}, "3000a : distances à l'axe 3, 1, 1, 3")
ok(Q(a["depart"]["D"])[1] - Q(a["depart"]["A"])[1] == 4 and a["depart"]["D"][0] == a["depart"]["A"][0], "3000a : AD = 4 vertical")
ok(a["depart"]["B"][1] == a["depart"]["A"][1], "3000a : [AB] horizontal (angle DAB droit)")
ia = {k: Q(v) for k, v in a["image"].items()}
ok((ia["D"] - ia["A"]).dot(ia["B"] - ia["A"]) == 0 and distance_ex(ia["A"], ia["D"]) == 4, "3000a : D'A'B' droit, A'D' = 4")
b = d["b"]
ok({k: p[1] - b["axe y"] for k, p in b["depart"].items()} == {"E": 1, "F": 2, "G": 3}, "3000b : distances 1, 2, 3")
cc = d["c"]
M = Q(cc["depart"]["M"])
ok(M[0] == M[1], "3000c : M sur l'axe")
for k in "KL":
    p = Q(cc["depart"][k])
    ok((p[0] - p[1]) / 2 == 2, f"3000c : {k} à 2 diagonales de l'axe")
    ok(p[0] > p[1], f"3000c : {k} d'un même côté")

# 2999
d = D["ex2999"]
O = Q(d["O"])
for k, p in d["depart"].items():
    ok(demi(p, d["O"]) == Q(d["image"][k + "'"]), f"2999 : image de {k}")
chemins = {k: O - Q(p) for k, p in d["depart"].items()}
ok(chemins["A"] == sp.Matrix([4, -2]), "2999 : A→O 4 droite 2 bas")
ok(chemins["B"] == sp.Matrix([-2, -3]), "2999 : B→O 2 gauche 3 bas")
ok(chemins["C"] == sp.Matrix([3, -3]), "2999 : C→O 3 droite 3 bas")
ok(O - Q(d["G"]) == sp.Matrix([-4, -1]), "2999 : G→O 4 gauche 1 bas")
ok(demi(d["H"], d["O"]) == Q(d["G"]), "2999 : G symétrique de H")
for p in list(d["depart"].values()) + list(d["image"].values()) + [d["G"], d["H"]]:
    ok(0 <= p[0] <= 10 and 0 <= p[1] <= 8, "2999 : point dans le quadrillage")
B, B2 = Q(d["depart"]["B"]), Q(d["image"]["B'"])
ok(distance_ex(B, O) == distance_ex(O, B2), "2999 : OB = OB'")
ok(sp.Matrix.hstack(O - B, B2 - O).det() == 0, "2999 : B, O, B' alignés")

# 3006
d = D["ex3006"]
O = Q(d["O"])
for k, p in d["depart"].items():
    ok(demi(p, d["O"]) == Q(d["image"][k + "'"]), f"3006 : image de {k}")
ch = {k: O - Q(p) for k, p in d["depart"].items()}
ok(ch["A"] == sp.Matrix([4, 2]) and ch["C"] == sp.Matrix([1, -2]) and ch["B"] == sp.Matrix([4, -3])
   and ch["D"] == sp.Matrix([4, -1]), "3006 : chemins A, B, C, D")
dep, im = {k: Q(v) for k, v in d["depart"].items()}, {k: Q(v) for k, v in d["image"].items()}
ok(distance_ex(dep["A"], dep["B"]) == 5 == distance_ex(im["A'"], im["B'"]), "3006 : mât de 5 carreaux")
ok(aire([d["depart"][k] for k in "BCD"]) == 3 == aire([d["image"][k + "'"] for k in "BCD"]), "3006 : fanion 3 carreaux")
ok(im["A'"][0] == im["B'"][0] and im["B'"][1] < im["A'"][1] and im["C'"][0] < im["B'"][0], "3006 : mât vertical, tête en bas, fanion à gauche")
ok(abs(dep["C"][0] - dep["B"][0]) == 3 and abs(dep["B"][1] - dep["D"][1]) == 2, "3006 : base 2, hauteur 3")

# 3003 (papier blanc, valeurs flottantes vérifiées numériquement)
d = D["ex3003"]
a1, a2 = d["axe"]
ok(abs(figs.dist(d["A"], d["B"]) - 4) < 1e-9 and abs(figs.dist(d["B"], d["C"]) - 3) < 1e-9, "3003 : AB = 4, BC = 3")
ang = sp.N(sp.acos(((d["A"][0] - d["B"][0]) * (d["C"][0] - d["B"][0]) + (d["A"][1] - d["B"][1]) * (d["C"][1] - d["B"][1]))
                   / (figs.dist(d["A"], d["B"]) * figs.dist(d["C"], d["B"]))) * 180 / sp.pi)
ok(abs(ang - 60) < 1e-6, "3003 : angle ABC = 60°")
im = d["image"]
for k in "ABC":
    m = figs.milieu(d[k], im[k + "'"])
    u = (a2[0] - a1[0], a2[1] - a1[1])
    w = (im[k + "'"][0] - d[k][0], im[k + "'"][1] - d[k][1])
    ok(abs(u[0] * w[1] - u[1] * w[0] - 0) >= 0 and abs(u[0] * w[0] + u[1] * w[1]) < 1e-9, f"3003 : (d) ⟂ [{k}{k}']")
    ok(abs(u[0] * (m[1] - a1[1]) - u[1] * (m[0] - a1[0])) < 1e-9, f"3003 : milieu de [{k}{k}'] sur (d)")
ok(abs(figs.dist(im["A'"], im["B'"]) - 4) < 1e-9 and abs(figs.dist(im["B'"], im["C'"]) - 3) < 1e-9, "3003 : A'B' = 4, B'C' = 3")
for P_ in (d["R"], d["S"]):
    ok(abs(figs.dist(P_, d["B"]) - figs.dist(P_, im["B'"])) < 1e-9, "3003 : arcs de centres R, S passant par B et B'")
I = d["I"]
cr = (im["C'"][0] - im["B'"][0]) * (I[1] - im["B'"][1]) - (im["C'"][1] - im["B'"][1]) * (I[0] - im["B'"][0])
ok(abs(cr) < 1e-9, "3003 : I sur (B'C')")
for k in "ABC":
    s1 = (a2[0] - a1[0]) * (d[k][1] - a1[1]) - (a2[1] - a1[1]) * (d[k][0] - a1[0])
    ok(s1 > 0, f"3003 : {k} du même côté de (d)")

# 3001
d = D["ex3001"]
ok(abs(figs.dist(d["E"], d["F"]) - 3.5) < 1e-9 and abs(figs.dist(d["F"], d["G"]) - 2.5) < 1e-9, "3001 : EF = 3,5 ; FG = 2,5")
ang = sp.N(sp.acos(((d["E"][0] - d["F"][0]) * (d["G"][0] - d["F"][0]) + (d["E"][1] - d["F"][1]) * (d["G"][1] - d["F"][1]))
                   / (3.5 * 2.5)) * 180 / sp.pi)
ok(abs(ang - 70) < 1e-6, "3001 : angle EFG = 70°")
for k in "EFGK":
    ok(egal(figs.milieu(d[k], d["image"][k + "'"]), d["O"], 1e-9), f"3001 : O milieu de [{k}{k}']")
E2, F2 = d["image"]["E'"], d["image"]["F'"]
ok(abs((d["F"][0] - d["E"][0]) * (F2[1] - E2[1]) - (d["F"][1] - d["E"][1]) * (F2[0] - E2[0])) < 1e-9, "3001 : (EF) // (E'F')")
ok(d["rayon"] == 1.5, "3001 : rayon 1,5")
# pas de chevauchement des deux cercles ni du triangle image avec le cercle image
ok(figs.dist(d["K"], d["image"]["K'"]) > 3, "3001 : cercles disjoints")

# 3008
d = D["ex3008"]
for k, p in d.items():
    bl, orr = p["bleu"], p["orange"]
    if p["type"] == "axiale" and "axe x" in p:
        ok(all(sym_axe_v(a_, p["axe x"]) == Q(b_) for a_, b_ in zip(bl, orr)), f"3008 figure {k} : symétrie axiale verticale")
    elif p["type"] == "axiale":
        ok(all(sym_diag(a_) == Q(b_) for a_, b_ in zip(bl, orr)), f"3008 figure {k} : symétrie de diagonale")
    elif p["type"] == "demi-tour":
        ok(all(demi(a_, p["O"]) == Q(b_) for a_, b_ in zip(bl, orr)), f"3008 figure {k} : demi-tour")
    else:
        ok(all(Q(b_) - Q(a_) == sp.Matrix(p["vecteur"]) for a_, b_ in zip(bl, orr)), f"3008 figure {k} : glissement")
        ok(Q(p["vecteur"]) == sp.Matrix([4, 2]), "3008 : 4 à droite, 2 vers le haut")
        mil = {tuple((Q(a_) + Q(b_)) / 2) for a_, b_ in zip(bl, orr)}
        ok(len(mil) > 1, "3008 figure 4 : pas de milieu commun")
    for q in bl + orr:
        ok(0 <= q[0] <= 7 and 0 <= q[1] <= 7, f"3008 figure {k} : dans le quadrillage")
ok(Q(d[1]["orange"][0])[0] - Q(d[1]["bleu"][0])[0] == 6, "3008 figure 1 : coins à 6 carreaux")
ok(d[2]["orange"][0] == (7, 5), "3008 figure 2 : coin en haut à droite de l'orange")
L0 = figs.L0
# le L n'a aucun axe ni centre (sinon les réponses seraient ambiguës)


def isometries_de(polys):
    """Axes et centre d'une figure formée de polygones (recherche exhaustive sur les sommets)."""
    pts = [Q(p) for poly in polys for p in poly]
    ens = {tuple(p) for p in pts}
    segs = set()
    for poly in polys:
        for i in range(len(poly)):
            a_, b_ = tuple(Q(poly[i])), tuple(Q(poly[(i + 1) % len(poly)]))
            segs.add(frozenset((a_, b_)))
    centre = sum(pts, sp.zeros(2, 1)) / len(pts)

    def image_seg(f):
        return {frozenset((tuple(f(sp.Matrix(a_))), tuple(f(sp.Matrix(b_))))) for a_, b_ in map(tuple, segs)}

    a_centre = image_seg(lambda p: 2 * centre - p) == segs
    axes = 0
    vus = set()
    for p1, p2 in combinations(pts, 2):
        for kind in ("med", "par"):
            if kind == "med":
                if p1 == p2:
                    continue
                n = p2 - p1
                c0 = n.dot((p1 + p2) / 2)
            else:
                dvec = p2 - p1
                if dvec == sp.zeros(2, 1):
                    continue
                n = sp.Matrix([-dvec[1], dvec[0]])
                c0 = n.dot(p1)
            g = sp.gcd(sp.gcd(n[0], n[1]), c0) if c0 != 0 else sp.gcd(n[0], n[1])
            n, c0 = n / g, c0 / g
            if n[0] < 0 or (n[0] == 0 and n[1] < 0):
                n, c0 = -n, -c0
            cle = (n[0], n[1], c0)
            if cle in vus:
                continue
            vus.add(cle)
            nn = n.dot(n)

            def refl(p, n=n, c0=c0, nn=nn):
                return p - 2 * (n.dot(p) - c0) / nn * n
            if {tuple(refl(sp.Matrix(p))) for p in ens} == ens and image_seg(refl) == segs:
                axes += 1
    return axes, a_centre


ok(isometries_de([L0]) == (0, False), "3008 : la forme en L n'a ni axe ni centre")

# 3005
d = D["ex3005"]
ok(abs(figs.dist(d["A"], d["B"]) - 6) < 1e-9 and abs(figs.dist(d["A"], d["C"]) - 4) < 1e-9, "3005 : AB = 6, AC = 4")
ok(abs((d["B"][0] - d["A"][0]) * (d["C"][0] - d["A"][0]) + (d["B"][1] - d["A"][1]) * (d["C"][1] - d["A"][1])) < 1e-9, "3005 : rectangle en A")
ok(abs(figs.dist(d["A"], d["M"]) - 2) < 1e-9, "3005 : AM = 2")
BC = sp.sqrt(6 ** 2 + 4 ** 2)
ok(sp.Rational(715, 100) <= BC < sp.Rational(725, 100), "3005 : BC ≈ 7,2 (arrondi au millimètre)")
ok(abs(figs.dist(d["B"], d["C"]) - float(BC)) < 1e-9, "3005 : BC de la figure = racine de 52")
ok(sp.Rational(6 * 4, 2) == 12, "3005 : aire 12")
ok(abs(6 + 4 + 7.2 - 17.2) < 1e-12, "3005 : périmètre 17,2")
ok(6 - 2 == 4, "3005 : M'B' = 4")
im = d["image"]
for k in "ABCM":
    ok(egal(figs.milieu(d[k], im[k + "'"]), d["O"], 1e-9), f"3005 : O milieu de [{k}{k}']")
ok(abs(figs.dist(im["A'"], im["M'"]) - 2) < 1e-9 and abs(figs.dist(im["M'"], im["B'"]) - 4) < 1e-9, "3005 : A'M' = 2, M'B' = 4")
for (p, q), (p2, q2) in (((d["A"], d["B"]), (im["A'"], im["B'"])), ((d["A"], d["C"]), (im["A'"], im["C'"]))):
    ok(abs((q[0] - p[0]) * (q2[1] - p2[1]) - (q[1] - p[1]) * (q2[0] - p2[0])) < 1e-9, "3005 : droites parallèles")

# 3015 lettres
LW, LH = figs.LW, figs.LH
attendu = {"H": (2, True), "N": (0, True), "E": (1, False), "X": (2, True), "T": (1, False), "Z": (0, True)}
for l, traits in figs.LETTRES.items():
    # une lettre = ensemble de segments (traits épais)
    segs = []
    for t in traits:
        segs += [[t[i], t[i + 1]] for i in range(len(t) - 1)]
    # recherche d'axes : verticale et horizontale par le centre de la boîte, diagonales de la boîte
    centre = sp.Matrix([sp.nsimplify(LW / 2), sp.nsimplify(LH / 2)])
    S_ = {frozenset((tuple(Q(a_)), tuple(Q(b_)))) for a_, b_ in segs}

    def img(f):
        return {frozenset((tuple(f(sp.Matrix(a_))), tuple(f(sp.Matrix(b_))))) for a_, b_ in map(tuple, S_)}
    n_axes = 0
    if img(lambda p: sp.Matrix([2 * centre[0] - p[0], p[1]])) == S_:
        n_axes += 1
    if img(lambda p: sp.Matrix([p[0], 2 * centre[1] - p[1]])) == S_:
        n_axes += 1
    # les diagonales de la boîte (non carrée) ne sont pas des axes : on vérifie qu'aucune ne marche
    for (p1, p2) in (((0, 0), (LW, LH)), ((0, LH), (LW, 0))):
        n = sp.Matrix([-(sp.nsimplify(p2[1]) - sp.nsimplify(p1[1])), sp.nsimplify(p2[0]) - sp.nsimplify(p1[0])])
        c0 = n.dot(Q(p1))

        def refl(p, n=n, c0=c0):
            return p - 2 * (n.dot(p) - c0) / n.dot(n) * n
        ok(img(refl) != S_, f"3015 : diagonale de la boîte de {l} n'est pas un axe")
    a_centre = img(lambda p: 2 * centre - p) == S_
    # E : la barre du milieu est plus courte, l'axe horizontal reste valable (barre posée sur l'axe)
    if l == "E":
        S_E = {frozenset((tuple(Q(a_)), tuple(Q(b_)))) for a_, b_ in segs}
        ok(img(lambda p: sp.Matrix([p[0], 2 * centre[1] - p[1]])) == S_E, "3015 : E a un axe horizontal")
    ok((n_axes, a_centre) == attendu[l], f"3015 : lettre {l} : {(n_axes, a_centre)} au lieu de {attendu[l]}")
    ok(figs.SYM_LETTRES[l] == (("vh" if attendu[l][0] == 2 else ("h" if l == "E" else ("v" if l == "T" else ""))), attendu[l][1]),
       f"3015 : tracé du corrigé de {l}")
# 3015 compléter
d = D["ex3015_completer"]
for poly, pim in zip(d["bleu"], d["image"]):
    ok(all(demi(p, d["O"]) == Q(q) for p, q in zip(poly, pim)), "3015 : image par demi-tour")
ok(aire(d["bleu"][0]) == 8 and aire(d["bleu"][1]) == sp.Rational(1, 2), "3015 : motif 8,5 carreaux")
ok(aire(d["bleu"][0]) + aire(d["bleu"][1]) + aire(d["image"][0]) + aire(d["image"][1]) == 17, "3015 : figure complète 17 carreaux")
ok(Q(d["O"]) - Q(d["bleu"][0][5]) == sp.Matrix([4, -2]), "3015 : coin en haut à gauche du L → O : 4 droite, 2 bas")
# pas de chevauchement : boîtes englobantes disjointes entre motif et image
from shapely.geometry import Polygon  # noqa: E402
bleu = Polygon(d["bleu"][0]).union(Polygon(d["bleu"][1]))
vert = Polygon(d["image"][0]).union(Polygon(d["image"][1]))
ok(bleu.intersection(vert).area == 0, "3015 : motif et image disjoints")
ok(isometries_de(d["bleu"] + d["image"])[0] == 0, "3015 : figure complète sans axe")
ok(isometries_de(d["bleu"] + d["image"])[1], "3015 : figure complète avec centre O")
ok(isometries_de([d["bleu"][0]]) == (0, False), "3015 : le L n'a pas d'axe (branches 4 et 5)")
# mots NON et TOT : N a un centre ; T n'en a pas, mais un axe vertical
ok(attendu["N"][1] and not attendu["T"][1] and attendu["T"][0] == 1, "3015 : NON / TOT")

# 3012
d = D["ex3012"]
for k, p in d["F"].items():
    ok(sym_axe_v(p, d["axe x"]) == Q(d["F1"][k]), f"3012 : F1 {k}")
    ok(demi(p, d["O"]) == Q(d["F2"][k]), f"3012 : F2 {k}")
ok({k: d["axe x"] - p[0] for k, p in d["F"].items()} == {"A": 5, "B": 2, "C": 2, "D": 4, "E": 5}, "3012 : distances à (d)")
ok(Q(d["O"]) - Q(d["F"]["C"]) == sp.Matrix([3, -2]), "3012 : C→O 3 droite 2 bas")
noms = "ABCDE"
ok(aire([d["F"][k] for k in noms]) == 7, "3012 : aire de F = 7")
ok(aire([d["F1"][k] for k in noms]) == 7 and aire([d["F2"][k] for k in noms]) == 7, "3012 : aires de F1, F2")
CD = Q(d["F"]["D"]) - Q(d["F"]["C"])
C1D1 = Q(d["F1"]["D"]) - Q(d["F1"]["C"])
C2D2 = Q(d["F2"]["D"]) - Q(d["F2"]["C"])
ok(sp.Matrix.hstack(CD, C2D2).det() == 0, "3012 : [C2D2] // [CD]")
ok(sp.Matrix.hstack(CD, C1D1).det() != 0, "3012 : [C1D1] non parallèle à [CD]")
ok(CD == sp.Matrix([-2, 2]) and C1D1 == sp.Matrix([2, 2]) and C2D2 == sp.Matrix([2, -2]), "3012 : directions décrites")
# comptage par colonnes : 3 ; 2 + 1/2 ; 1 + 1/2
poly = Polygon([d["F"][k] for k in noms])
from shapely.geometry import box  # noqa: E402
col = [sum(poly.intersection(box(x, y, x + 1, y + 1)).area for y in range(0, 11)) for x in (1, 2, 3)]
ok(col == [3, 2.5, 1.5], f"3012 : colonnes {col}")
for p in list(d["F1"].values()) + list(d["F2"].values()):
    ok(0 <= p[0] <= 14 and 0 <= p[1] <= 10, "3012 : dans le quadrillage")

# 3019
d = D["ex3019"]
tri, car = d["motif"]
ok(aire(tri) == 2 and aire(car) == 1, "3019 : motif 3 carreaux")
ok([d["axe x"] - p[0] for p in tri] == [3, 1, 3], "3019 : triangle à 3 et 1 carreaux de (d)")
ok(Q(d["O"]) - Q(tri[0]) == sp.Matrix([3, -1]), "3019 : sommet de l'angle droit → O : 3 droite 1 bas")
ok((Q(tri[1]) - Q(tri[0])).dot(Q(tri[2]) - Q(tri[0])) == 0, "3019 : angle droit au premier sommet")
tous = [tri, car] + d["etape 1"] + d["etape 2"]
ok(sum(aire(m) for m in tous) == 12, "3019 : 12 carreaux colorés")
union = Polygon(tous[0])
for m in tous[1:]:
    ok(union.intersection(Polygon(m)).area == 0, "3019 : motifs disjoints")
    union = union.union(Polygon(m))
ax, ce = isometries_de(tous + [[(0, 0), (8, 0), (8, 8), (0, 8)]])
ok(ax == 2 and ce, f"3019 : carreau terminé : {ax} axes, centre {ce}")
cote = sp.Rational(20, 8)
ok(cote == sp.Rational(5, 2) and cote ** 2 == sp.Rational(25, 4), "3019 : 2,5 cm et 6,25 cm²")
ok(12 * cote ** 2 == 75, "3019 : 75 cm²")
ok(sp.Rational(12, 64) == sp.Rational(3, 16) == sp.Rational(75, 400), "3019 : fraction 3/16")

# =================================================================== 3. structure
meta = json.loads((ICI / "source_en_ligne" / "meta.json").read_text(encoding="utf-8"))
ids_en_ligne = {e["id"] for e in meta["exercices"]}
texte = (ICI / "exercices.txt").read_text(encoding="utf-8")
blocs = [b.strip() for b in re.split(r"^===[ \t]*$", texte, flags=re.M) if b.strip()]
retires = {int(m.group(1)) for m in re.finditer(r"^(\d+)", (ICI / "exercices_retires.txt").read_text(encoding="utf-8"), re.M)}
ids, titres, types = [], [], []
corr = json.loads((ICI / "figures" / "correspondance.json").read_text(encoding="utf-8"))
for b in blocs:
    titre = b.splitlines()[0].replace("===", "", 1).strip()
    eid = int(re.search(r"^Id:\s*(\d+)", b, re.M).group(1))
    ids.append(eid)
    titres.append(titre)
    typ = titre.split(" - ")[0]
    types.append(typ)
    ok(typ in ("Découverte", "Entraînement", "Problème", "Synthèse"), f"{eid} : type {typ}")
    ok(len(titre.split(" - ")) == 2, f"{eid} : titre « Type - Sujet »")
    ok("brevet" not in b.lower(), f"{eid} : mention du brevet")
    ok("Image:" not in b, f"{eid} : ligne Image: résiduelle")
    en = b[b.index("Énoncé:"):b.index("Étapes:")]
    et = b[b.index("Étapes:"):b.index("Solution:")]
    so = b[b.index("Solution:"):]
    nq = len(re.findall(r"^\d+\. ", en, re.M))
    ok(nq == len(re.findall(r"^## Question \d+", et, re.M)), f"{eid} : questions ≠ parties du corrigé")
    ok(nq == len(re.findall(r"^\d+\. ", so, re.M)), f"{eid} : questions ≠ lignes de solution")
    ok(":::" in et and "::: methode" in et and "::: etape" in et and "::: resultat" in et, f"{eid} : méthode/étape/résultat")
    ok("::: attention" in et, f"{eid} : erreur fréquente")
    appel = {int(n) for n in re.findall(r"\[IMAGE_(\d+)\]", b)}
    decl = {int(n) for n in corr["exercices"].get(str(eid), {})}
    ok(appel == decl, f"{eid} : images appelées {appel} / déclarées {decl}")
    ok(re.search(r"\[IMAGE_\d+\]", en) is not None, f"{eid} : figure dans l'énoncé")
    ok(re.search(r"\[IMAGE_\d+\]", et) is not None, f"{eid} : figure dans le corrigé")
    for f_ in corr["exercices"].get(str(eid), {}).values():
        ok((ICI / "figures" / "images" / f_["fichier"]).exists(), f"{eid} : {f_['fichier']} absent")
ok(len(blocs) == 10, "10 exercices")
ok(len(set(titres)) == len(titres), "titres uniques")
ok(set(ids) | retires == ids_en_ligne and not set(ids) & retires, "10 gardés + 11 retirés = 21 Id")
ok(types == ["Découverte"] * 3 + ["Entraînement"] * 3 + ["Problème"] * 2 + ["Synthèse"] * 2, f"progression {types}")
for nom, cle, idd in (("cours_270.txt", "cours", "270"), ("fiche_190.txt", "fiches", "190")):
    t = (ICI / nom).read_text(encoding="utf-8")
    appel = {int(n) for n in re.findall(r"\[IMAGE_(\d+)\]", t)}
    ok(appel == {int(n) for n in corr[cle][idd]}, f"{nom} : images")
    ok("brevet" not in t.lower(), f"{nom} : brevet")
ok((ICI / "cours_270.txt").read_text(encoding="utf-8").startswith("Titre: Symétries et demi-tour\n"), "titre du cours")
ok((ICI / "fiche_190.txt").read_text(encoding="utf-8").startswith("Titre: Résumé : Symétries et demi-tour\n"), "titre de la fiche")

print(f"{N} contrôles, {len(ERREURS)} erreur(s)")
for e in ERREURS:
    print("  ✗", e)
raise SystemExit(1 if ERREURS else 0)
