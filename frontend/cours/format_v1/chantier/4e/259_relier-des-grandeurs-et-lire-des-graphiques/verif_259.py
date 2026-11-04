# -*- coding: utf-8 -*-
"""Vérification (sympy) de la notion 259 : cours, fiche, 21 exercices et données des figures.

python verif_259.py  →  nombre de contrôles, tous justes, sinon arrêt sur le premier faux.
Les données des figures sont importées de figures/figures.py (DONNEES) : on vérifie
qu'elles correspondent aux valeurs annoncées dans les énoncés et les corrigés.
"""
import importlib.util
from pathlib import Path
from sympy import Rational as Q, symbols, solve, Eq, sqrt, nsimplify, cos, pi, Integer

ICI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("fig259", ICI / "figures" / "figures.py")
F = importlib.util.module_from_spec(spec)
spec.loader.exec_module(F)
D = F.DONNEES

n = 0


def ok(cond, msg):
    global n
    assert cond, msg
    n += 1


def egal(a, b, msg, tol=None):
    a, b = nsimplify(a), nsimplify(b)
    if tol is None:
        ok(a == b, f"{msg} : {a} ≠ {b}")
    else:
        ok(abs(float(a) - float(b)) <= tol, f"{msg} : {float(a)} ≉ {float(b)}")


def interp(pts, x):
    """Lecture sur une ligne brisée."""
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1 and x1 != x0:
            return Q(y0) + (Q(y1) - Q(y0)) * (Q(x) - x0) / (x1 - x0)
    raise ValueError(x)


x, t, c, d, v, h = symbols("x t c d v h")

# ======================================================== COURS / FICHE
# marée h = 3 - 2 cos(pi t / 6)
H = lambda tt: 3 - 2 * cos(pi * Q(tt) / 6)
egal(H(2), 2, "marée 2 h"); egal(H(4), 4, "marée 4 h"); egal(H(8), 4, "marée 8 h")
egal(H(6), 5, "marée max"); egal(H(0), 1, "marée 0 h"); egal(H(12), 1, "marée 12 h")
for tt in range(0, 13):   # 4 m atteint exactement à 4 h et à 8 h ; maximum 5 m seulement à 6 h
    ok((H(tt) == 4) == (tt in (4, 8)) and (H(tt) == 5) == (tt == 6), f"marée {tt} h")
for tt in range(0, 13):
    egal(D["maree"][tt], float(H(tt)), f"données marée {tt}", 1e-9)
# piscine V = 5 + 2t
for tt, vv in zip(range(6), [5, 7, 9, 11, 13, 15]):
    egal(5 + 2 * tt, vv, f"piscine t={tt}")
    egal(dict(D["piscine"])[tt], vv, f"données piscine {tt}")
egal(5 + 2 * 3, 11, "piscine test 3 h")
# carré : 16 = 4c = c²
ok(solve(Eq(c ** 2, 4 * c), c) == [0, 4], "c² = 4c")

# ======================================================== 2663 température
T = D["temperature"]
egal(interp(T, 9), 6, "T(9)"); egal(max(y for _, y in T), 14, "max"); egal(min(y for _, y in T), 1, "min")
ok([xx for xx, y in T if y == 14] == [15] and [xx for xx, y in T if y == 1] == [6], "heures max/min")
egal(interp(T, 11), 10, "T(11)"); egal(interp(T, 18), 10, "T(18)"); egal(interp(T, 10), 8, "T(10)")
# 10 °C atteint exactement deux fois
cnt = sum(1 for (x0, y0), (x1, y1) in zip(T, T[1:]) if (y0 - 10) * (y1 - 10) < 0 or y1 == 10)
ok(cnt == 2, f"10 °C : {cnt} fois")
egal(14 - 1, 13, "hausse 6-15"); egal(18 - 11, 7, "durée ≥ 10")
for (x0, y0), (x1, y1) in zip(T, T[1:]):
    sens = "+" if y1 > y0 else "-"
    ok((sens == "+") == (6 <= x0 < 15), f"variations {x0}-{x1}")

# ======================================================== 2664 carré
for cc, p, a in D["carre"]:
    egal(p, 4 * cc, f"P({cc})"); egal(a, cc ** 2, f"A({cc})")
egal(Q(8, 2), 4, "P/c"); ok(Q(4, 2) != Q(1, 1), "A non prop")

# ======================================================== 2665 plante
P = D["plante"]
croiss = [P[k + 1][1] - P[k][1] for k in range(8)]
ok(croiss == [1, 2, 3, 4, 3, 2, 1, 0.5], f"croissances {croiss}")
egal(P[0][1], 2, "départ"); egal(P[4][1], 12, "4 sem."); egal(P[5][1], 15, "5 sem.")
egal(Q(37, 2) - 2, Q(33, 2), "total 16,5"); ok(croiss.index(max(croiss)) == 3, "semaine 3-4")

# ======================================================== 2666 baignoire
B = D["baignoire"]
egal(30 / 10, 3, "remplissage 3 cm/min"); egal(38 - 30, 8, "saut")
egal(24 - 12, 12, "bain"); egal(40 - 28, 12, "vidange"); egal(Q(30, 12), Q(5, 2), "2,5 cm/min")
egal(interp(B[:2], 5), 15, "15 cm à 5 min"); egal(interp(B[-2:], 34), 15, "15 cm à 34 min")
egal(interp(B[:2], 10), 30, "30 cm à 10 min")

# ======================================================== 2667 taxi
prix = lambda dd: Q(5, 2) + Q(6, 5) * dd
for dd, pp in zip((0, 5, 10, 15, 20), ("2.5", "8.5", "14.5", "20.5", "26.5")):
    egal(prix(dd), Q(pp), f"taxi {dd}")
    egal(dict(D["taxi"])[dd], float(Q(pp)), f"données taxi {dd}", 1e-9)
egal(Q("8.5") / 5, Q("1.7"), "8,5/5"); egal(Q("14.5") / 10, Q("1.45"), "14,5/10")
egal(prix(7), Q("10.9"), "7 km"); egal(solve(Eq(prix(d), Q("20.5")), d)[0], 15, "20,50 €")

# ======================================================== 2668 associer
egal(Q(12, 6), 2, "bougie 2 cm/h"); egal(Q(60, 3), 20, "cycliste 20 km/h"); egal(1200 - 400, 800, "dénivelé")

# ======================================================== 2669 vitesse
V = D["vitesse"]
egal(interp(V, 5), 25, "25 km/h à 5 s"); egal(interp(V, 45), 25, "25 km/h à 45 s")
dist = Q(50000, 3600) * 30
egal(dist, Q(1250, 3), "distance"); ok(round(float(dist)) == 417, "≈ 417 m"); ok(abs(float(Q(50000, 3600)) - 13.89) < 0.005, "13,89 m/s")

# ======================================================== 2670 récipients
A, Bc = D["recipients"]["A"], D["recipients"]["B"]
egal(A(800), 10, "A 800"); egal(A(1200), 15, "A 1200"); egal(A(1600), 20, "A plein")
egal(float(Bc(1600)), 20, "B plein", 1e-9); egal(float(Bc(200)), 10, "B 200 → 10", 1e-9)
ok(abs(Bc(800) - 15.874) < 0.001 and round(Bc(800)) == 16, "B 800 ≈ 16")
egal(Q(10, 8), Q(5, 4), "1,25 cm / 100 cm³"); egal(Q(200, 1600), Q(1, 8), "un huitième")

# ======================================================== 2671 course
ana, ben = D["ana"], D["ben"]
egal(ana(50), 200, "Ana 50 s"); egal(Q(200, 50), 4, "4 m/s"); egal(ben(20), 0, "départ Ben")
egal(ben(60), 200, "Ben 60 s"); egal(Q(200, 40), 5, "5 m/s")
egal(solve(Eq(4 * t, 5 * (t - 20)), t)[0], 100, "rencontre"); egal(ana(100), 400, "400 m")
egal(Q(600, 4), 150, "Ana arrivée"); egal(20 + Q(600, 5), 140, "Ben arrivée"); egal(600 - ana(140), 40, "écart")

# ======================================================== 2672 population
Pp = dict(D["population"])
egal(Pp[30], 15, "1980"); egal(Pp[50], 16, "2000")
var = [Pp[k + 10] - Pp[k] for k in range(0, 70, 10)]
ok(var == [1, 2, 4, 2, -1, 2, 3], f"variations {var}")
egal(Q(21 - 8, 8) * 100, Q(325, 2), "162,5 %"); egal(interp(D["population"], 25), 13, "1975")

# ======================================================== 2673 rectangle
R = D["rectangle"]
for xx, aa in zip(range(1, 6), (9, 16, 21, 24, 25)):
    egal(R[xx], aa, f"aire {xx}"); egal(xx * (10 - xx), aa, f"x(10-x) {xx}")
ok(sorted(solve(Eq(x * (10 - x), 16), x)) == [2, 8], "aire 16")
ok(max(R.values()) == 25 and R[5] == 25, "max 25")
ok(solve(Eq((x * (10 - x)).diff(x), 0), x) == [5], "sommet x = 5")

# ======================================================== 2674 vélo
egal(3 * 2, 6, "A 2h"); egal(10 + 2, 12, "B 2h"); egal(3 * 8, 24, "A 8h"); egal(10 + 8, 18, "B 8h")
egal(solve(Eq(3 * h, 10 + h), h)[0], 5, "intersection"); egal(3 * 5, 15, "15 €")
ok(abs(20 / 3 - 6.67) < 0.005, "6,67 h"); egal(Q(2, 3) * 60, 40, "40 min"); egal(20 - 10, 10, "B 10 h")

# ======================================================== 2675 ballon
hb = lambda tt: -5 * Q(tt) ** 2 + 20 * Q(tt)
egal(hb(1), 15, "h(1)"); egal(hb("2.5"), Q("18.75"), "h(2,5)"); egal(hb(2), 20, "h(2)"); egal(hb(3), 15, "h(3)")
egal(hb(4), 0, "h(4)"); ok(sorted(solve(Eq(-5 * t ** 2 + 20 * t, 15), t)) == [1, 3], "15 m")
ok(sorted(solve(Eq(-5 * t ** 2 + 20 * t, 0), t)) == [0, 4], "sol")
ok(solve(Eq((-5 * t ** 2 + 20 * t).diff(t), 0), t) == [2], "sommet")
for tt in (0, 1, 2.5, 4):
    egal(D["ballon"](tt), float(hb(str(tt))), f"données ballon {tt}", 1e-9)

# ======================================================== 2676 freinage
fr = lambda vv: Q(vv) ** 2 / 200
egal(fr(50), Q("12.5"), "50 km/h"); egal(fr(130), Q("84.5"), "130 km/h"); egal(fr(60), 18, "60 km/h")
for vv, dd in zip(range(0, 121, 20), (0, 2, 8, 18, 32, 50, 72)):
    egal(fr(vv), dd, f"freinage {vv}"); egal(dict(D["freinage"])[vv], dd, f"données freinage {vv}")
egal(Q(2, 20), Q(1, 10), "2/20"); egal(Q(8, 40), Q(1, 5), "8/40")
vs = [s for s in solve(Eq(v ** 2 / 200, 40), v) if s > 0][0]
egal(vs, 40 * sqrt(5), "v pour 40 m"); ok(abs(float(vs) - 89.44) < 0.01 and round(float(vs), -1) == 90, "≈ 90 km/h")
egal(fr(90), Q("40.5"), "90 km/h"); egal(fr(80), 4 * fr(40), "×4"); egal(fr(120), 4 * fr(60), "×4 bis")

# ======================================================== 2677 Léa
L = D["lea"]
egal(max(y for _, y in L), 9, "max 9 km")
egal(4 / Q(1, 4), 16, "16 km/h"); egal(5 / Q(1, 3), 15, "15 km/h"); egal(9 / Q(1, 2), 18, "18 km/h")
egal(18 / Q(3, 2), 12, "12 km/h")
egal(solve(Eq(interp(L, t) if False else 4 + Q(5, 20) * (t - 25), 6), t)[0], 33, "6 km aller")
egal(solve(Eq(9 - Q(9, 30) * (t - 60), 6), t)[0], 70, "6 km retour")
egal(interp(L, 33), 6, "lecture 33"); egal(interp(L, 70), 6, "lecture 70")

# ======================================================== 2678 plongée
pl = lambda dd: 1 + Q(dd) / 10
egal(pl(10), 2, "10 m"); egal(pl(20), 3, "20 m"); egal(pl(30), 4, "30 m"); egal(pl(25), Q(7, 2), "25 m")
egal(solve(Eq(1 + d / 10, Q(7, 2)), d)[0], 25, "3,5 bar"); egal(solve(Eq(1 + d / 10, Q(11, 5)), d)[0], 12, "2,2 bar")
egal(pl(22), Q(16, 5), "22 m → 3,2 bar"); ok(pl(20) != 2 * pl(10), "non prop")
for dd in (0, 12, 25, 40):
    egal(D["plongee"](dd), float(pl(dd)), f"données plongée {dd}", 1e-9)

# ======================================================== 2679 four
fo = D["four"]
egal(fo(0), 20, "allumage"); egal(fo(10), 200, "10 min"); egal(Q(180, 10), 18, "18 °C/min")
egal(fo(55), 110, "55 min", 1e-9); egal(fo(70), 65, "70 min", 1e-9)
import math
t100 = 40 + 15 * math.log2(180 / 80)
ok(57 < t100 < 58, f"passage sous 100 °C : {t100}")
egal(200 - 110, 90, "baisse 1"); egal(110 - 65, 45, "baisse 2")

# ======================================================== 2680 boîte
Vb = lambda xx: Q(xx) * (20 - 2 * Q(xx)) ** 2
for xx, cc, vv in ((1, 18, 324), (2, 16, 512), (3, 14, 588), (4, 12, 576), (5, 10, 500)):
    egal(20 - 2 * xx, cc, f"côté {xx}"); egal(Vb(xx), vv, f"V({xx})")
crit = solve(Eq((x * (20 - 2 * x) ** 2).diff(x), 0), x)
ok(Q(10, 3) in crit, f"maximum {crit}"); egal(Vb(Q(10, 3)), Q(16000, 27), "V max")
ok(round(float(Vb(Q(10, 3)))) == 593, "≈ 593 cm³")
r500 = sorted(solve(Eq(x * (20 - 2 * x) ** 2, 500), x), key=lambda s: float(s))
ok(len(r500) == 3 and r500[1] == 5 and abs(float(r500[0]) - 1.91) < 0.01 and float(r500[2]) > 10, f"V = 500 : {r500}")
egal(Vb("1.9"), Q("498.636"), "V(1,9)"); egal(Q("16.2") ** 2, Q("262.44"), "16,2²")
egal(D["boite"](5), 500, "données boîte 5"); egal(D["boite"](3), 588, "données boîte 3")

# ======================================================== 2681 rentabilité
cout = lambda n_: 200 + 5 * n_
rec = lambda n_: 9 * n_
egal(cout(30), 350, "coût 30"); egal(rec(30), 270, "recette 30"); egal(rec(30) - cout(30), -80, "bénéfice 30")
for n_, cc, rr in ((0, 200, 0), (10, 250, 90), (20, 300, 180)):
    egal(cout(n_), cc, f"tableur coût {n_}"); egal(rec(n_), rr, f"tableur recette {n_}"); egal(rr - cc, rec(n_) - cout(n_), "")
egal(solve(Eq(9 * x, 200 + 5 * x), x)[0], 50, "seuil"); egal(cout(50), 450, "450 €")
egal((9 * x - (200 + 5 * x)).expand(), 4 * x - 200, "bénéfice"); egal(solve(Eq(4 * x - 200, 300), x)[0], 125, "300 €")

# ======================================================== 2682 cardiaque
C = D["cardiaque"]
egal(C[0][1], 70, "repos"); ok(max(C, key=lambda p: p[1]) == (35, 180), "max")
egal(220 - 14, 206, "FCmax"); ok(round(180 / 206 * 100, 1) == 87.4, "87,4 %")
egal(Q(60, 100) * 206, Q("123.6"), "60 %"); egal(Q(75, 100) * 206, Q("154.5"), "75 %")
tz = solve(Eq(150 + Q(8, 20) * (t - 10), Q("154.5")), t)[0]
egal(tz, Q(85, 4), "sortie de zone 21,25 min"); egal(interp(C, tz), Q("154.5"), "lecture zone")
egal(Q(180 - 90, 10), 9, "récupération")

# ======================================================== 2683 basket
hk = lambda xx: -Q(1, 5) * Q(xx) ** 2 + Q(8, 5) * Q(xx) + 2
egal(hk(0), 2, "départ"); egal(hk(1), Q(17, 5), "x=1"); egal(hk(4), Q(26, 5), "x=4"); egal(hk(7), Q(17, 5), "x=7")
ok(solve(Eq((-x ** 2 / 5 + 8 * x / 5 + 2).diff(x), 0), x) == [4], "sommet")
egal(Q("7.25") ** 2, Q("52.5625"), "7,25²"); egal(hk("7.25"), Q("3.0875"), "panier"); ok(round(float(hk("7.25")), 2) == 3.09, "3,09")
egal(hk(9), Q(1, 5), "x=9"); egal(hk("9.1"), Q("-0.002"), "x=9,1")
racine = [s for s in solve(Eq(-x ** 2 / 5 + 8 * x / 5 + 2, 0), x) if s > 0][0]
egal(racine, 4 + sqrt(26), "racine"); ok(9 < float(racine) < 9.1, "entre 9 et 9,1")
for xx in (0, 4, 7.25):
    egal(D["basket"](xx), float(hk(str(xx))), f"données basket {xx}", 1e-9)

print(f"verif_259 : {n} contrôles, tous justes.")
