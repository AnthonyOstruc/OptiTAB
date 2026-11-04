# -*- coding: utf-8 -*-
"""Vérification des résultats de la notion 281 (4e, probabilités) : python verif_281.py

Fractions exactes (sympy Rational), dénombrements exhaustifs, équations résolues par sympy,
données des figures relues dans figures/figures.py, script Scratch exécuté.
"""
import math
import sys
from itertools import product
from pathlib import Path

from sympy import Eq, Rational as R, pi, solve, symbols, N as num

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI / "figures"))
import figures as FG  # noqa: E402
from scratch import executer  # noqa: E402

D = FG.DONNEES
ok = 0


def v(nom, a, b):
    global ok
    assert a == b, (nom, a, b)
    ok += 1


def proche(nom, a, b, tol):
    global ok
    assert abs(float(a) - float(b)) <= tol, (nom, float(a), float(b))
    ok += 1


def P(fav, tot):
    return R(fav, tot)


DE = range(1, 7)

# ------------------------------------------------------------------ cours
u = dict(D["urne_cours"])
v("cours urne données", u, {"rouge": 5, "bleue": 3, "jaune": 2})
v("cours rouge", P(5, 10), R(1, 2)); v("cours bleue", P(3, 10), R(3, 10)); v("cours jaune", P(2, 10), R(1, 5))
v("cours somme", P(5, 10) + P(3, 10) + P(2, 10), 1)
v("cours roue angles", D["roue_cours"], [180, 120, 60]); v("cours roue 360", sum(D["roue_cours"]), 360)
v("cours roue P", [R(a, 360) for a in D["roue_cours"]], [R(1, 2), R(1, 3), R(1, 6)])
v("cours roue somme", R(3, 6) + R(2, 6) + R(1, 6), 1)
v("cours non 6", 1 - R(1, 6), R(5, 6)); v("cours non as", 1 - R(4, 32), R(7, 8)); v("cours 28/32", R(28, 32), R(7, 8))
v("cours 1/4", R(1, 4), R(25, 100))
pieces = list(product("PF", repeat=2))
v("cours deux pièces", len(pieces), 4)
v("cours un pile", P(sum(i.count("P") == 1 for i in pieces), 4), R(1, 2))
fin = D["sim_cours"][-1][1]
proche("cours simulation finale proche de 1/6", fin, 1 / 6, 0.005)
v("cours simulation dans le cadre", max(y for _, y in D["sim_cours"]) <= 0.42, True)
proche("cours 1/6 ≈ 0,17", 1 / 6, 0.17, 0.005)

# ------------------------------------------------------------------ 3125
u = dict(D["urne_3125"]); n = sum(u.values())
v("3125 total", n, 12)
v("3125 rouge", P(u["rouge"], n), R(1, 2)); v("3125 bleue", P(u["bleue"], n), R(1, 3)); v("3125 jaune", P(u["jaune"], n), R(1, 6))
v("3125 somme", sum(P(k, n) for k in u.values()), 1)
v("3125 non rouge", 1 - R(1, 2), P(u["bleue"] + u["jaune"], n))
v("3125 +3 jaunes", P(u["jaune"] + 3, n + 3), R(1, 3))

# ------------------------------------------------------------------ 3126
A = [k for k in DE if k % 2 == 0]; B = [k for k in DE if k % 3 == 0]; C = [k for k in DE if k >= 5]
v("3126 A", A, [2, 4, 6]); v("3126 B", B, [3, 6]); v("3126 C", C, [5, 6])
v("3126 P", [P(len(A), 6), P(len(B), 6), P(len(C), 6)], [R(1, 2), R(1, 3), R(1, 3)])
prem = [k for k in DE if k > 1 and all(k % d for d in range(2, k))]
v("3126 premiers", prem, [2, 3, 5]); v("3126 P premier", P(len(prem), 6), R(1, 2))
v("3126 non C", P(len([k for k in DE if k <= 4]), 6), 1 - R(1, 3)); v("3126 non C val", 1 - R(1, 3), R(2, 3))
v("3126 obtenir 0", P(0, 6), 0); v("3126 < 10", P(len([k for k in DE if k < 10]), 6), 1)

# ------------------------------------------------------------------ 3127
roue = D["roue_3127"]
v("3127 angle", R(360, 8), 45)
cnt = lambda c: sum(1 for k in roue if roue[k] == c)
v("3127 rouge", P(cnt("rouge"), 8), R(3, 8)); v("3127 bleu", P(cnt("bleu"), 8), R(1, 4))
v("3127 jaune", P(cnt("jaune"), 8), R(1, 4)); v("3127 blanc", P(cnt("blanc"), 8), R(1, 8))
v("3127 somme", sum(P(cnt(c), 8) for c in ("rouge", "bleu", "jaune", "blanc")), 1)
v("3127 non jaune", 1 - R(1, 4), R(3, 4)); v("3127 pair", P(len([k for k in roue if k % 2 == 0]), 8), R(1, 2))
v("3127 rouge et pair", P(len([k for k in roue if roue[k] == "rouge" and k % 2 == 0]), 8), R(1, 8))
rp = [k for k in roue if roue[k] == "rouge" or k % 2 == 0]
v("3127 rouge ou pair liste", rp, [1, 2, 3, 4, 6, 8]); v("3127 rouge ou pair", P(len(rp), 8), R(3, 4))
v("3127 piège 7/8", R(3, 8) + R(4, 8), R(7, 8))

# ------------------------------------------------------------------ 3128 et cours (32 cartes)
jeu = list(product(FG.VALEURS, [s for _, _, s in FG.SUITS]))
v("3128 32 cartes", len(jeu), 32)
v("3128 coeur", P(sum(s == "cœur" for _, s in jeu), 32), R(1, 4))
v("3128 as", P(sum(x == "A" for x, _ in jeu), 32), R(1, 8)); v("3128 as de coeur", P(1, 32), R(1, 32))
v("3128 rouge", P(sum(s in ("cœur", "carreau") for _, s in jeu), 32), R(1, 2))
fig_ = sum(x in ("V", "D", "R") for x, _ in jeu)
v("3128 figures", fig_, 12); v("3128 P figure", P(fig_, 32), R(3, 8)); v("3128 non figure", 1 - R(3, 8), P(32 - fig_, 32))

# ------------------------------------------------------------------ 3129
e = D["echelle_3129"]
v("3129 A", e["A"], R(1, 2)); v("3129 B", e["B"], R(1, 6)); v("3129 C", e["C"], 0); v("3129 D", e["D"], 1)
v("3129 E", e["E"], 1 - R(1, 6)); v("3129 F", e["F"], R(3, 4))
v("3129 ordre", sorted(e, key=lambda k: e[k]), ["C", "B", "A", "F", "E", "D"])
v("3129 arrondis", [round(float(e[k]), 2) for k in "BE"], [0.17, 0.83])
v("3129 rouge du sac F", R(1, 4), 1 - e["F"])

# ------------------------------------------------------------------ 3130
v("3130 pluie", R(100) - 35, 65); v("3130 non as", 1 - R(4, 32), R(7, 8))
v("3130 nul", 100 - 45 - 30, 25); v("3130 ne perd pas", 100 - 30, 45 + 25); v("3130 ne gagne pas", 100 - 45, 30 + 25)
v("3130 affirmation", R(4, 10) + R(5, 10) != 1, True)

# ------------------------------------------------------------------ 3131
v("3131 PP", P(sum(i == ("P", "P") for i in pieces), 4), R(1, 4))
v("3131 au moins un", P(sum("P" in i for i in pieces), 4), R(3, 4)); v("3131 contraire", 1 - R(1, 4), R(3, 4))
v("3131 Léo", [P(sum(i.count("P") == k for i in pieces), 4) for k in range(3)], [R(1, 4), R(1, 2), R(1, 4)])
v("3131 400", 400 * R(1, 2), 200)

# ------------------------------------------------------------------ 3132 (script exécuté)
v("3132 attendu", 600 * R(1, 6), 100); v("3132 93", R(155, 1000) * 600, 93)
for f in ("0.155", "0.175", "0.16", "0.18"):
    v("3132 fréquence possible " + f, (R(f) * 600).q, 1)
fr = []
for g in range(15):
    r = executer({"Lutin": [FG.SCRIPTS["3132"]]}, graine=g)
    fr.append(r.dits[0])
v("3132 script : fréquences entre 0 et 1", all(0 <= x <= 1 for x in fr), True)
proche("3132 script : moyenne des fréquences proche de 1/6", sum(fr) / len(fr), 1 / 6, 0.02)
v("3132 script : résultats différents", len(set(fr)) > 1, True)
r = executer({"Lutin": [FG.SCRIPTS["cours"]]}, graine=3)
proche("cours script 1000 lancers", r.dits[0], 1 / 6, 0.06)
proche("cours 1/6 = 0,167", 1 / 6, 0.167, 0.0005)

# ------------------------------------------------------------------ 3133
pil = D["pile_3133"]
fq = [R(s, n) for n, s in pil]
v("3133 fréquences", fq, [R(7, 10), R(56, 100), R(512, 1000), R(4985, 10000)])
v("3133 écarts", [abs(f - R(1, 2)) for f in fq], [R(2, 10), R(6, 100), R(12, 1000), R(15, 10000)])
v("3133 écarts décroissants", all(abs(fq[k] - R(1, 2)) > abs(fq[k + 1] - R(1, 2)) for k in range(3)), True)

# ------------------------------------------------------------------ 3134
f, c, m = 6, 4, 8; n = f + c + m
v("3134 total", n, 18); v("3134 P", [P(f, n), P(c, n), P(m, n)], [R(1, 3), R(2, 9), R(4, 9)])
v("3134 somme", R(3, 9) + R(2, 9) + R(4, 9), 1); v("3134 non menthe", 1 - R(4, 9), P(f + c, n))
v("3134 -2 fraises", P(f - 2, n - 2), R(1, 4))
y = symbols("y")
v("3134 citron", solve(Eq((c + y) / (n + y), R(1, 2)), y), [10]); v("3134 contrôle", R(14, 28), R(1, 2))

# ------------------------------------------------------------------ 3135
a = D["roue_3135"]
v("3135 360", sum(a), 360)
v("3135 P", [R(x, 360) for x in a], [R(1, 2), R(1, 4), R(1, 6), R(1, 12)])
v("3135 somme", R(6, 12) + R(3, 12) + R(2, 12) + R(1, 12), 1)
v("3135 pair", R(a[1] + a[3], 360), R(1, 3)); v("3135 1200", 1200 * R(1, 12), 100); v("3135 angle 1/4", R(1, 4) * 360, 90)

# ------------------------------------------------------------------ 3136
C20 = range(1, 21)
prem20 = [k for k in C20 if k > 1 and all(k % d for d in range(2, k))]
v("3136 premiers figure", prem20, FG.PREMIERS_20)
v("3136 mult 5", P(sum(k % 5 == 0 for k in C20), 20), R(1, 5))
v("3136 premiers", (len(prem20), P(len(prem20), 20)), (8, R(2, 5)))
div = [k for k in C20 if 20 % k == 0]
v("3136 diviseurs", div, [1, 2, 4, 5, 10, 20]); v("3136 P div", P(len(div), 20), R(3, 10))
car = [k for k in C20 if math.isqrt(k) ** 2 == k]
v("3136 carrés", car, [1, 4, 9, 16]); v("3136 P carré", P(len(car), 20), R(1, 5))
v("3136 premier et pair", [k for k in prem20 if k % 2 == 0], [2])
po = [k for k in C20 if k % 2 == 0 or k % 5 == 0]
v("3136 pair ou mult 5", (len(po), P(len(po), 20)), (12, R(3, 5)))
v("3136 non premier", 1 - R(2, 5), P(20 - len(prem20), 20)); v("3136 > 20", P(sum(k > 20 for k in C20), 20), 0)

# ------------------------------------------------------------------ 3137
pu = D["punaise_3137"]
fq = [R(s, n) for n, s in pu]
v("3137 fréquences", fq, [R(7, 10), R(54, 100), R(63, 100), R(59, 100), R(618, 1000), R(612, 1000)])
v("3137 cumul croissant", all(pu[k][1] <= pu[k + 1][1] and pu[k + 1][1] - pu[k][1] <= pu[k + 1][0] - pu[k][0] for k in range(5)), True)
v("3137 stabilisé dès 200", all(R(59, 100) <= q <= R(62, 100) for q in fq[3:]), True)
v("3137 côté", 1 - R(612, 1000), R(388, 1000)); v("3137 5000", 5000 * R(612, 1000), 3060)

# ------------------------------------------------------------------ 3138
v("3138 jeu1", (P(2, 6), P(4, 6)), (R(1, 3), R(2, 3))); v("3138 jeu1 équitable", P(3, 6), R(1, 2))
v("3138 jeu2", (P(4, 10), P(6, 10)), (R(2, 5), R(3, 5)))
x = symbols("x")
v("3138 rouges à ajouter", solve(Eq(4 + x, 6), x), [2])
r8 = range(1, 9)
v("3138 jeu3", (P(sum(k % 3 == 0 for k in r8), 8), P(sum(k % 4 == 0 for k in r8), 8)), (R(1, 4), R(1, 4)))
v("3138 jeu3 disjoints", [k for k in r8 if k % 3 == 0 and k % 4 == 0], [])
v("3138 60 parties", 60 * R(1, 3), 20)

# ------------------------------------------------------------------ 3139
g = D["roue_3139"]
v("3139 secteurs", (sum(1 for k in g if g[k] == 5), sum(1 for k in g if g[k] == 2)), (1, 3))
p5, p2 = R(1, 12), R(3, 12); p0 = R(12 - len(g), 12)
v("3139 P", (p5, p2, p0), (R(1, 12), R(1, 4), R(2, 3))); v("3139 gagner", p5 + p2, 1 - p0); v("3139 gagner val", p5 + p2, R(1, 3))
v("3139 600", (600 * p5, 600 * p2), (50, 150)); v("3139 bilan", 600 - (50 * 5 + 150 * 2), 50)
v("3139 fréquence", round(46 / 600, 3), 0.077); v("3139 1/12", round(1 / 12, 3), 0.083)
v("3139 modifiée", 600 - (600 * R(1, 12) * 5 + 600 * R(2, 12) * 2), 150)

# ------------------------------------------------------------------ 3140
U = D["urnes_3140"]
pA, pB, pC = (R(r_, r_ + n_) for r_, n_ in (U["A"], U["B"], U["C"]))
v("3140 P", (pA, pB, pC), (R(3, 5), R(5, 9), R(8, 15)))
v("3140 /45", (pA * 45, pB * 45, pC * 45), (27, 25, 24)); v("3140 ordre", pA > pB > pC, True)
v("3140 A+B", R(3 + 5, 5 + 9), R(4, 7)); v("3140 moyenne", (pA + pB) / 2, R(26, 45)); v("3140 différent", R(4, 7) != R(26, 45), True)
proche("3140 4/7", R(4, 7), 0.571, 0.0005); proche("3140 26/45", R(26, 45), 0.578, 0.0005)
r_ = symbols("r")
v("3140 rouges B", solve(Eq((5 + r_) / (9 + r_), R(3, 5)), r_), [1])
v("3140 noires A", solve(Eq(R(3) / (5 + r_), R(1, 2)), r_), [1])

# ------------------------------------------------------------------ 3141
pj = 1 - R(1, 4) - R(1, 3)
v("3141 jaune", pj, R(5, 12))
t = symbols("t")
tot = solve(Eq(pj * t, 10), t)[0]
v("3141 total", tot, 24); v("3141 rouges bleues", (tot / 4, tot / 3), (6, 8))
v("3141 bande", D["bande_3141"], {"rouges": 3, "bleues": 4, "jaunes": 5}); v("3141 part", R(10, 5), 2)
v("3141 rouges 1/2", solve(Eq((6 + x) / (24 + x), R(1, 2)), x), [12]); v("3141 piège", R(12, 30), R(2, 5))
v("3141 25 boules", R(25, 3).q != 1, True)

# ------------------------------------------------------------------ 3142
ef = D["de_3142"]
v("3142 total", sum(ef), 500)
v("3142 fréquences", [R(k, 500) for k in ef], [R(12, 100), R(13, 100), R(14, 100), R(15, 100), R(16, 100), R(3, 10)])
proche("3142 attendu", R(500, 6), 83, 0.5)
v("3142 pair", R(ef[1] + ef[3] + ef[5], 500), R(58, 100)); v("3142 pair 290", ef[1] + ef[3] + ef[5], 290)
v("3142 victoires", 200 * R(3, 10), 60); proche("3142 33", 200 * R(1, 6), 33.3, 0.05)

# ------------------------------------------------------------------ 3143
Fdp, Fext, Ftot, Gdp, Gext, Gtot, dp, ext, T = 40, 24, 64, 35, 21, 56, 75, 45, 120
v("3143 tableau", (Ftot - Fdp, dp - Fdp, T - Ftot, Fext + Gext, T - dp, Gdp + Gext), (Fext, Gdp, Gtot, ext, ext, Gtot))
v("3143 P", (P(Ftot, T), P(dp, T), P(Fdp, T), P(Gext, T)), (R(8, 15), R(5, 8), R(1, 3), R(7, 40)))
v("3143 62,5 %", R(5, 8) * 100, R(125, 2))
v("3143 fille ou dp", P(Ftot + Gdp, T), 1 - R(7, 40)); v("3143 33/40", 1 - R(7, 40), R(33, 40))
v("3143 double comptage", Ftot + dp, 139)

# ------------------------------------------------------------------ 3144
dis = dict(D["distributeur_3144"]); n = sum(dis.values())
v("3144 total", n, 30)
v("3144 rouge", P(dis["rouge"], n), R(2, 5)); v("3144 non bleue", 1 - P(dis["bleue"], n), R(4, 5))
v("3144 Tom", P(dis["jaune"], n), P(dis["bleue"] + dis["blanche"], n)); v("3144 3/10", P(9, 30), R(3, 10))
v("3144 après Lucie", P(dis["rouge"] - 1, n - 1), R(11, 29)); v("3144 plus petite", R(11, 29) < R(2, 5), True)
proche("3144 0,379", R(11, 29), 0.379, 0.0005)
v("3144 blanches", solve(Eq(4 * (3 + x), 30 + x), x), [6]); v("3144 9/36", R(9, 36), R(1, 4))
v("3144 fréquence", R(95, 250), R(38, 100))

# ------------------------------------------------------------------ 3145
car_, pd, gd = 40 ** 2, pi * 10 ** 2, pi * 20 ** 2
v("3145 carré", car_, 1600); proche("3145 314", pd, 314.16, 0.005)
v("3145 P petit", pd / car_, pi / 16); proche("3145 0,196", num(pi / 16), 0.196, 0.0005)
v("3145 P grand", gd / car_, pi / 4); proche("3145 0,785", num(pi / 4), 0.785, 0.0005)
v("3145 couronne", pi / 4 - pi / 16, 3 * pi / 16); proche("3145 0,589", num(3 * pi / 16), 0.589, 0.0005)
proche("3145 hors", num(1 - pi / 4), 0.215, 0.0005); proche("3145 200", num(200 * pi / 16), 39.3, 0.05)
v("3145 rapport 4", (pi / 4) / (pi / 16), 4)

print(f"verif_281 : {ok} contrôles, tous justes")
