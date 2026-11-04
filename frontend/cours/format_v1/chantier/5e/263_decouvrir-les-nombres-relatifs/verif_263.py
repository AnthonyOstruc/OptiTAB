# -*- coding: utf-8 -*-
"""Vérification (sympy, valeurs exactes) de tous les résultats de la notion 263.

    python verif_263.py
"""
import re
from itertools import product
from pathlib import Path

from sympy import Rational as R, Abs, nsimplify

N = 0
ECHECS = []


def ok(cond, msg):
    global N
    N += 1
    if not cond:
        ECHECS.append(msg)


def q(s):
    """'-4,5' -> Rational exact."""
    return nsimplify(s.replace(",", "."), rational=True)


def croissant(vals):
    return sorted(vals)


ICI = Path(__file__).resolve().parent

# ------------------------------------------------------------------ cours
ok(q("-4,7") < q("-4,15"), "cours -4,7 < -4,15")
ok(croissant([q(x) for x in "1,8 -5 0 -0,5 -5,2 2".split()]) == [q(x) for x in "-5,2 -5 -0,5 0 1,8 2".split()], "cours rangement")
ok(-4 < q("-3,6") < -3, "cours encadrement -3,6")
ok(Abs(q("-6,5")) == q("6,5") and Abs(9) == 9 and Abs(0) == 0, "cours distances")
ok(-8 < -3 and -15 < 2 and q("3,7") < 5 and -9 < -2, "cours comparaisons")
ok(3 * R(1, 2) == R(3, 2), "cours F à 3 intervalles de 0,5")
ok(-q("3,5") == q("-3,5") and -(-12) == 12, "cours opposés")

# ------------------------------------------------------------------ 2747
ok(q("-3") < 0 < 5, "2747 Q1")
dates = {"Rome": -753, "Empire": 476, "Alesia": -52, "Charlemagne": 800}
ok(sorted(dates, key=dates.get) == ["Rome", "Alesia", "Empire", "Charlemagne"], "2747 Q4 ordre")
nbs = [q(x) for x in "-7 12 0 -0,5 3,2 -15 8".split()]
ok([x for x in nbs if x < 0] == [-7, q("-0,5"), -15], "2747 Q3a")
ok([x for x in nbs if x > 0] == [12, q("3,2"), 8], "2747 Q3b")

# ------------------------------------------------------------------ 2752
pas = R(1, 2)
ok(R(1) / 2 == pas, "2752 Q1")
lus = {"A": -5 * pas, "B": -1 * pas, "C": 3 * pas}
ok(lus == {"A": q("-2,5"), "B": q("-0,5"), "C": q("1,5")}, "2752 Q2")
ok(Abs(-3) / pas == 6 and 2 / pas == 4 and q("1,5") / pas == 3, "2752 Q3 intervalles")
tous = dict(lus, E=-3, F=2, G=q("-1,5"))
d = {k: Abs(v) for k, v in tous.items()}
ok(min(d, key=d.get) == "B" and max(d, key=d.get) == "E", "2752 Q4")
ok(list(d.values()).count(max(d.values())) == 1 and list(d.values()).count(min(d.values())) == 1, "2752 Q4 unicité")

# ------------------------------------------------------------------ 2748
tab = [q(x) for x in "-6 4,5 -0,8 13 -2,75".split()]
ok([Abs(x) for x in tab] == [6, q("4,5"), q("0,8"), 13, q("2,75")], "2748 Q1 distances")
ok([-x for x in tab] == [6, q("-4,5"), q("0,8"), -13, q("2,75")], "2748 Q1 opposés")
ok(-(-5) == 5 and -(2) == -2, "2748 Q2")
ok(Abs(-9) != -9 and Abs(5) == Abs(-5) and 5 != -5, "2748 Q3")

# ------------------------------------------------------------------ 2749
pts = {"A": (3, 2), "B": (-4, 3), "C": (-2, -3), "D": (4, -1), "E": (0, 3), "F": (-3, 0)}
ok([k for k, (x, y) in pts.items() if x < 0] == ["B", "C", "F"], "2749 Q3a")
ok([k for k, (x, y) in pts.items() if y < 0] == ["C", "D"], "2749 Q3b")
ok(pts["E"][0] == 0 and pts["F"][1] == 0, "2749 Q4")
ok((-pts["A"][0], pts["A"][1]) == (-3, 2), "2749 Q5")
# points placés dans la fenêtre du repère (-5..5 ; -4..4) et tous distincts
places = [(-1, 4), (2, -4), (-5, -2), (-3, 2)]
ok(all(-5 <= x <= 5 and -4 <= y <= 4 for x, y in list(pts.values()) + places), "2749 fenêtre")
ok(len(set(list(pts.values()) + places)) == 10, "2749 points distincts")

# ------------------------------------------------------------------ 2751
villes = {"Paris": q("2,5"), "Oslo": q("-4,5"), "Montreal": -12, "Rome": 5, "Moscou": q("-9,5"),
          "Berlin": -1, "Helsinki": -7}
ok(q("-4,3") > q("-4,7") and q("-0,8") < q("0,2") and q("-9,5") > -12 and q("-1,05") > q("-1,5"), "2751 Q1")
ordre = sorted(villes, key=villes.get)
ok(ordre == ["Montreal", "Moscou", "Helsinki", "Oslo", "Berlin", "Paris", "Rome"], "2751 Q2")
neg = sorted([v for v in villes.values() if v < 0], reverse=True)
ok(neg == [-1, q("-4,5"), -7, q("-9,5"), -12], "2751 Q3")
ok(villes["Helsinki"] < villes["Oslo"], "2751 Q4")
ok(-10 < q("-9,5") < -9 and q("-4,7") < q("-4,4") < q("-4,3") and q("-4,7") < q("-4,6") < q("-4,3"), "2751 Q5")

# ------------------------------------------------------------------ 2759
P = {"A": q("-4,5"), "B": q("3,2"), "C": q("-3,2"), "D": q("0,7")}
ok(sorted(P, key=P.get) == ["A", "C", "D", "B"], "2759 Q1")
ok(Abs(P["A"]) > Abs(P["B"]) == Abs(P["C"]) > Abs(P["D"]), "2759 Q2")
opp = [(a, b) for a, b in product(P, P) if a < b and P[a] == -P[b]]
ok(opp == [("B", "C")], "2759 Q3")
E = -P["D"]
ok(E == q("-0,7") and E > P["C"], "2759 Q4")
l5 = [q(x) for x in "-3,25 -3,2 -3,52 -0,7 -3".split()]
ok(sorted(l5, reverse=True) == [q(x) for x in "-0,7 -3 -3,2 -3,25 -3,52".split()], "2759 Q5")

# ------------------------------------------------------------------ 2750
arrets = [5, -2, 0, 3, -3, 7]
ok([a for a in arrets if a < 0] == [-2, -3], "2750 Q1")
ok(sorted(arrets) == [-3, -2, 0, 3, 5, 7], "2750 Q2")
ok(Abs(-2) + Abs(3) == 5 and 3 - (-2) == 5, "2750 Q3")
ok(-3 < -2, "2750 Q4")
ok(Abs(-2) < Abs(4), "2750 Q5")
ok(-3 == -(3) and 3 - (-3) == 6, "2750 Q6")
ok(-3 >= -3 and 8 <= 8, "2750 étages existants")

# ------------------------------------------------------------------ 2753
alt = {"falaise": 70, "mouette": 40, "bateau": 0, "plongeuse": -30, "epave": -50, "sousmarin": -70}
ok(sorted(alt.values()) == [-70, -50, -30, 0, 40, 70], "2753 Q2")
ok([k for k, v in alt.items() if Abs(v) == 70 and k != "falaise"] == ["sousmarin"], "2753 Q3")
ok(Abs(alt["plongeuse"]) == 30, "2753 Q4")
ok(alt["mouette"] - alt["plongeuse"] == 70 == 40 + 30, "2753 Q5")
milieu = R(alt["epave"] + alt["plongeuse"], 2)
ok(milieu == -40 and -50 < -45 < -40 and Abs(-45 - (-50)) < Abs(-45 - (-30)), "2753 Q6")
ok(all(v % 10 == 0 for v in alt.values()), "2753 lisible au pas de 10 m")

# ------------------------------------------------------------------ 2765
# indices 1-3 : -2,6 < x < -2,4 puis -2,5 < x < -2,4
for x in (q("-2,45"), q("-2,42"), q("-2,48")):
    ok(x < 0 and q("2,4") < Abs(x) < q("2,6") and x > q("-2,5"), f"2765 Q3 {x}")
# indice 4 : tous les décimaux à 2 chiffres après la virgule, chiffre des centièmes 5
cands = [R(-k, 100) for k in range(1, 1000) if k % 10 == 5]
sol = [x for x in cands if x < 0 and q("2,4") < Abs(x) < q("2,6") and x > q("-2,5")]
ok(sol == [q("-2,45")], "2765 Q4 unicité")
# l'indice 3 est plus exigeant
ok(q("-2,5") > q("-2,6"), "2765 Q2")

# ------------------------------------------------------------------ 2754
T = {"6 h": -7, "9 h": q("-4,5"), "12 h": q("1,5"), "15 h": 3, "18 h": -2, "21 h": q("-5,5")}
ok([h for h, v in T.items() if v < 0] == ["6 h", "9 h", "18 h", "21 h"], "2754 Q1")
ok(sorted(T.values()) == [-7, q("-5,5"), q("-4,5"), -2, q("1,5"), 3] and min(T, key=T.get) == "6 h", "2754 Q2")
ok(T["21 h"] < T["9 h"], "2754 Q3")
dist = {h: Abs(v) for h, v in T.items()}
ok(min(dist, key=dist.get) == "12 h" and sorted(dist.values())[0] < sorted(dist.values())[1], "2754 Q4")
plan = {"C": (-3, 2), "T": (2, 4), "R": (4, -1), "P": (-4, -3), "S": (-2, -1)}
plan["F"] = (-plan["R"][0], plan["R"][1])
ok(plan["F"] == (-4, -1), "2754 Q7")
ok(sorted(k for k, (x, y) in plan.items() if y < 0) == ["F", "P", "R", "S"], "2754 Q8")
ok(len(set(plan.values())) == 6, "2754 lieux distincts")

# ------------------------------------------------------------------ figures : valeurs dessinées = valeurs du texte
fig = (ICI / "figures" / "figures.py").read_text(encoding="utf-8")
ok('(-12, "Montréal"' in fig and '(-9.5, "Moscou"' in fig and '(-7, "Helsinki"' in fig and '(-4.5, "Oslo"' in fig
   and '(-1, "Berlin"' in fig and '(2.5, "Paris"' in fig and '(5, "Rome"' in fig, "figure 2751 = tableau")
ok('(-2.5, "A"), (-.5, "B"), (1.5, "C")' in fig and '((-3, "E"), (2, "F"), (-1.5, "G"))' in fig, "figure 2752")
ok('((-5, "M"), (2, "N"))' in fig and '((5, "P"), (-2, "Q"))' in fig, "figure 2748")
ok('(5, r"14 h' in fig and '(-3, r"7 h' in fig, "figure 2747")
ok('(70, "falaise"' in fig and '(40, "oiseau"' in fig and '(-30, "plongeur"' in fig and '(-50, "epave"' in fig
   and '(-70, "sousmarin"' in fig, "figure 2753")
ok("for k in (-3, -2, 0, 3, 5, 7)" in fig, "figure 2750 arrêts")
ok('(-7, "6 h"), (-5.5, "21 h"), (-4.5, "9 h"), (-2, "18 h"), (1.5, "12 h"), (3, "15 h")' in fig, "figure 2754 températures")

# ------------------------------------------------------------------ cohérence Solution / Étapes et aucun « brevet »
ex = (ICI / "exercices.txt").read_text(encoding="utf-8")
for fichier in ("exercices.txt", "cours_258.txt", "fiche_178.txt"):
    t = (ICI / fichier).read_text(encoding="utf-8").lower()
    ok("brevet" not in t, f"pas de « brevet » dans {fichier}")
titres = re.findall(r"^=== (.+)$", ex, re.M)
ok(len(titres) == 10 and len(set(titres)) == 10, "10 titres uniques")
ok(all(t.split(" - ")[0] in ("Découverte", "Entraînement", "Problème", "Synthèse") for t in titres), "types de titres")
for bloc in re.split(r"^===\s*$", ex, flags=re.M):
    if "Id:" in bloc:
        eid = re.search(r"Id:\s*(\S+)", bloc).group(1)
        et = bloc.split("Étapes:")[1].split("Solution:")[0]
        for champ in ("::: methode", "::: etape", "::: resultat"):
            ok(champ in et, f"{eid} : {champ} présent")
        ok("::: attention" in et or "::: retenir" in et, f"{eid} : erreur fréquente / à retenir")

print(f"{N} contrôles, {len(ECHECS)} échec(s)")
for e in ECHECS:
    print("  ✗", e)
raise SystemExit(1 if ECHECS else 0)
