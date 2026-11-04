# -*- coding: utf-8 -*-
"""Vérification exacte (sympy) de la notion 279 (5e) : Hasard et probabilités.

    python verif_279.py

Chaque probabilité est recalculée par dénombrement exhaustif des issues, en
fractions exactes (sympy.Rational), puis comparée aux valeurs écrites dans le cours,
la fiche et les 10 corrigés (écritures décimales et pourcentages compris). Les
données des figures (figures/figures.py, DONNEES) et les simulations des courbes
sont relues. Enfin la structure : questions = étapes = solutions, un résultat par
question, images appelées = déclarées, 10 gardés + 11 retirés = 21 Id en ligne,
progression, aucune mention du brevet, pas d'événement contraire (programme de 4e).
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

import sympy as sp

ICI = Path(__file__).resolve().parent
OK, KO = [], []
R = sp.Rational


def ctrl(nom, cond):
    (OK if bool(cond) else KO).append(nom)


def proba(issues, favorable):
    """Probabilité exacte en situation d'équiprobabilité, par dénombrement."""
    issues = list(issues)
    return R(sum(1 for i in issues if favorable(i)), len(issues))


def dec_fr(x, n=None):
    """Écriture décimale française exacte (ou arrondie à n chiffres) d'un rationnel."""
    x = sp.nsimplify(x)
    if n is not None:
        v = sp.Float(x, 30)
        q = sp.Rational(10) ** n
        v = sp.floor(v * q + R(1, 2)) / q
        s = f"{float(v):.{n}f}"
    else:
        s = str(sp.Float(x, 15)).rstrip("0").rstrip(".")
    return s.replace(".", "{,}")


def pct(x):
    """Pourcentage exact « 37{,}5\\ \\% »."""
    v = sp.nsimplify(x * 100)
    s = str(sp.Float(v, 15)).rstrip("0").rstrip(".") if v.q != 1 else str(v)
    return s.replace(".", "{,}") + r"\ \%"


def frac(x):
    x = sp.nsimplify(x)
    return rf"\dfrac{{{x.p}}}{{{x.q}}}" if x.q != 1 else str(x.p)


# ---------------------------------------------------------------- textes
cours = (ICI / "cours_274.txt").read_text(encoding="utf-8")
fiche = (ICI / "fiche_194.txt").read_text(encoding="utf-8")
ex_txt = (ICI / "exercices.txt").read_text(encoding="utf-8")
blocs = [b.strip() for b in re.split(r"^===[ \t]*$", ex_txt, flags=re.M) if b.strip()]
EX = {re.search(r"^Id:\s*(\d+)", b, re.M).group(1): b for b in blocs}


def dans(eid, *morceaux):
    for m in morceaux:
        ctrl(f"ex{eid} : « {m} » écrit", m in EX[eid])


def dans_cours(*morceaux):
    for m in morceaux:
        ctrl(f"cours : « {m} » écrit", m in cours)


# ---------------------------------------------------------------- figures
spec = importlib.util.spec_from_file_location("fig279", ICI / "figures" / "figures.py")
FIG = importlib.util.module_from_spec(spec)
spec.loader.exec_module(FIG)
DON = FIG.DONNEES

DE = range(1, 7)

# ============================================================ COURS
sac = dict(DON["sac_cours"])
ctrl("cours : sac 5 rouges, 2 bleus, 1 vert", sac == {"rouge": 5, "bleu": 2, "vert": 1})
jetons = [c for c, n in DON["sac_cours"] for _ in range(n)]
pr = proba(jetons, lambda c: c == "rouge")
pb = proba(jetons, lambda c: c == "bleu")
pv = proba(jetons, lambda c: c == "vert")
ctrl("cours : P(rouge) = 5/8 = 0,625 = 62,5 %", pr == R(5, 8) and dec_fr(pr) == "0{,}625" and pct(pr) == r"62{,}5\ \%")
ctrl("cours : P(bleu) = 1/4 = 25 %", pb == R(1, 4) and pct(pb) == r"25\ \%")
ctrl("cours : P(vert) = 1/8 = 0,125 = 12,5 %", pv == R(1, 8) and dec_fr(pv) == "0{,}125")
ctrl("cours : P(jaune) = 0", proba(jetons, lambda c: c == "jaune") == 0)
dans_cours(r"\dfrac{5}{8} = 0{,}625 = 62{,}5\ \%", r"\dfrac{2}{8} = \dfrac{1}{4} = 25\ \%", r"\dfrac{1}{8} = 0{,}125 = 12{,}5\ \%")
ctrl("cours : P(au moins 5) = 2/6 = 1/3", proba(DE, lambda k: k >= 5) == R(1, 3))
dans_cours(r"\frac{2}{6} = \frac{1}{3}")
ctrl("cours : 1/6 ≈ 0,17", dec_fr(R(1, 6), 2) == "0{,}17")
ctrl("cours : tableau des écritures", all(dec_fr(R(a, b)) == d for a, b, d in
                                           [(1, 2, "0{,}5"), (1, 4, "0{,}25"), (3, 4, "0{,}75"), (1, 5, "0{,}2"), (1, 10, "0{,}1")]))
ctrl("cours : pourcentages du tableau", [pct(R(a, b)) for a, b in [(1, 2), (1, 4), (3, 4), (1, 5), (1, 10)]] ==
     [r"50\ \%", r"25\ \%", r"75\ \%", r"20\ \%", r"10\ \%"])
# roue du cours : partage en secteurs de 60°
roue = DON["roue_cours"]
ctrl("cours : roue 180 + 120 + 60 = 360", sum(a for _, a in roue) == 360)
petits = [c for c, a in roue for _ in range(a // 60)]
ctrl("cours : 6 secteurs de 60°", len(petits) == 6 and 360 // 6 == 60)
ctrl("cours : roue bleu 1/2, jaune 1/3, rouge 1/6",
     [proba(petits, lambda c, n=n: c == n) for n in ("bleu", "jaune", "rouge")] == [R(1, 2), R(1, 3), R(1, 6)])
ctrl("figure roue_cours : rayons en pointillés aux bons angles (30°, -30°, -150°)",
     "(30.00:" in FIG.FIGURES["roue_cours"] and "(-30.00:" in FIG.FIGURES["roue_cours"] and "(-150.00:" in FIG.FIGURES["roue_cours"])
# échelle du sac
ctrl("figure echelle_sac : probabilités du sac", DON["echelle_sac"] == {"jaune": 0, "vert": pv, "bleu": pb, "rouge": pr, "certain": 1})
# 40 tirages
eff = {"rouge": 27, "bleu": 9, "vert": 4}
ctrl("cours : 27 + 9 + 4 = 40", sum(eff.values()) == 40)
ctrl("cours : fréquences 0,675 ; 0,225 ; 0,1", [dec_fr(R(v, 40)) for v in eff.values()] == ["0{,}675", "0{,}225", "0{,}1"])
ctrl("cours : 27/40 = 67,5 %", pct(R(27, 40)) == r"67{,}5\ \%")
dans_cours(r"\dfrac{27}{40} = 0{,}675", r"$67{,}5\ \%$")
sim = DON["sim_cours"]
ctrl("figure frequences_cours : 1 000 tirages", len(sim) == 1000)
ctrl("figure frequences_cours : fréquence finale proche de 0,625 (écart < 0,005)", abs(sim[-1][1] - 0.625) < 0.005)
ctrl("figure frequences_cours : forte variation au début (> 0,7 avant 20 tirages)", max(y for x, y in sim[:20]) > 0.7)
ctrl("figure frequences_cours : stabilisée après 400 tirages (écart < 0,03)", all(abs(y - 0.625) < 0.03 for x, y in sim[399:]))
ctrl("figure frequences_cours : fenêtre 0,4 → 1,05 contient la courbe", all(0.4 <= y <= 1.05 for x, y in sim))
ctrl("fiche : 1/4 = 0,25 = 25 %", r"\dfrac{1}{4} = 0{,}25 = 25\ \%" in fiche)
ctrl("fiche : 1/6 ≈ 0,17 ≈ 17 %", r"\dfrac{1}{6} \approx 0{,}17 \approx 17\ \%" in fiche)
ctrl("cartes du cours : impairs 1, 3, 5, 7, 9", [k for k in range(1, 11) if k % 2] == [1, 3, 5, 7, 9])

# ============================================================ 3084
ev = DON["evenements_3084"]
ctrl("ex3084 : A pairs", tuple(k for k in DE if k % 2 == 0) == ev["A"])
ctrl("ex3084 : B multiples de 3", tuple(k for k in DE if k % 3 == 0) == ev["B"])
ctrl("ex3084 : C strictement < 3", tuple(k for k in DE if k < 3) == ev["C"])
ctrl("ex3084 : D certain, E impossible", proba(DE, lambda k: k <= 6) == 1 and proba(DE, lambda k: k == 7) == 0)
real6 = [n for n, f in [("A", lambda k: k % 2 == 0), ("B", lambda k: k % 3 == 0), ("C", lambda k: k < 3),
                        ("D", lambda k: k <= 6), ("E", lambda k: k == 7)] if f(6)]
ctrl("ex3084 : avec 6, A, B, D réalisés", real6 == ["A", "B", "D"])
ctrl("ex3084 : A (3 issues) > C (2 issues)", len(ev["A"]) == 3 and len(ev["C"]) == 2)
ctrl("ex3084 : 25 × 4 = 100", 25 * 4 == 100)

# ============================================================ 3087
urne = [c for c, n in DON["urne_3087"] for _ in range(n)]
pA, pB, pC = R(1, 2), proba(DE, lambda k: k == 3), proba(urne, lambda c: c == "rouge")
ctrl("ex3087 : P(A) = 1/2, P(B) = 1/6, P(C) = 3/4", (pA, pB, pC) == (R(1, 2), R(1, 6), R(3, 4)))
ctrl("ex3087 : D impossible, E certain", proba(DE, lambda k: k == 0) == 0 and proba(urne, lambda c: c in ("rouge", "bleue")) == 1)
ctrl("ex3087 : boule bleue 1/4", proba(urne, lambda c: c == "bleue") == R(1, 4))
ctrl("ex3087 : écritures", dec_fr(pA) == "0{,}5" and pct(pA) == r"50\ \%" and dec_fr(pC) == "0{,}75" and pct(pC) == r"75\ \%"
     and dec_fr(pB, 2) == "0{,}17" and round(float(pB) * 100) == 17)
ctrl("figure echelle_3087_placee : positions", DON["echelle_3087"] == {"D": 0, "B": pB, "A": pA, "C": pC, "E": 1})
ctrl("ex3087 : G = (1/6)^10 très proche de 0", R(1, 6) ** 10 < R(1, 10 ** 7))
ctrl("ex3087 : 0,75 au milieu de 0,7 et 0,8", (R(7, 10) + R(8, 10)) / 2 == pC)
dans("3087", r"P(B) \approx 0{,}17", r"\frac{3}{4} &= \frac{75}{100} = 0{,}75 = 75\ \%", r"\frac{1}{2} &= \frac{50}{100} = 0{,}5 = 50\ \%")

# ============================================================ 3083
urne = [c for c, n in DON["urne_3083"] for _ in range(n)]
ctrl("ex3083 : 10 boules", len(urne) == 10)
p = {c: proba(urne, lambda x, c=c: x == c) for c in ("rouge", "bleue", "jaune", "verte")}
ctrl("ex3083 : rouge 3/5 = 0,6 = 60 %", p["rouge"] == R(3, 5) and dec_fr(p["rouge"]) == "0{,}6" and pct(p["rouge"]) == r"60\ \%")
ctrl("ex3083 : bleue 3/10 = 0,3 = 30 %", p["bleue"] == R(3, 10) and pct(p["bleue"]) == r"30\ \%")
ctrl("ex3083 : jaune 1/10 = 10 %", p["jaune"] == R(1, 10) and pct(p["jaune"]) == r"10\ \%")
ctrl("ex3083 : verte 0", p["verte"] == 0)
ctrl("ex3083 : pas jaune 9/10 = 90 %", proba(urne, lambda x: x != "jaune") == R(9, 10))
ctrl("ex3083 : rouge > 1/2, tom faux", p["rouge"] > R(1, 2) and p["rouge"] != R(1, 3))
ctrl("ex3083 : ordre jaune < bleue < rouge", p["jaune"] < p["bleue"] < p["rouge"])
dans("3083", r"P(\text{rouge}) &= \frac{6}{10} = \frac{3}{5} \\" + "\n" + r"&= 0{,}6 = 60\ \%", r"\frac{9}{10} = 0{,}9 = 90\ \%")

# ============================================================ 3096
C12 = range(1, 13)
evs = {"A": lambda k: k % 2 == 0, "B": lambda k: k % 3 == 0, "C": lambda k: 12 % k == 0, "D": lambda k: k >= 10}
P = {n: proba(C12, f) for n, f in evs.items()}
ctrl("ex3096 : P(7) = 1/12", proba(C12, lambda k: k == 7) == R(1, 12))
ctrl("ex3096 : A 1/2, B 1/3, C 1/2, D 1/4", (P["A"], P["B"], P["C"], P["D"]) == (R(1, 2), R(1, 3), R(1, 2), R(1, 4)))
ctrl("ex3096 : listes A et C", tuple(k for k in C12 if evs["A"](k)) == DON["cartes_3096"]["A"]
     and tuple(k for k in C12 if evs["C"](k)) == DON["cartes_3096"]["C"])
ctrl("ex3096 : B = 3, 6, 9, 12 ; D = 10, 11, 12", [k for k in C12 if evs["B"](k)] == [3, 6, 9, 12] and [k for k in C12 if evs["D"](k)] == [10, 11, 12])
ctrl("ex3096 : D < B < A = C", P["D"] < P["B"] < P["A"] == P["C"])
ctrl("ex3096 : douzièmes 3, 4, 6", [P[n] * 12 for n in "DBA"] == [3, 4, 6])
ctrl("ex3096 : A ≠ C (8 dans A, 3 dans C)", evs["A"](8) and not evs["C"](8) and evs["C"](3) and not evs["A"](3))
p11 = proba(range(1, 12), lambda k: k % 2 == 0)
ctrl("ex3096 : sans la carte 12, P(pair) = 5/11 < 1/2", p11 == R(5, 11) and p11 < R(1, 2))
dans("3096", r"P(\text{pair}) = \frac{5}{11}", r"P(D) = \frac{3}{12} = \frac{1}{4}")

# ============================================================ 3103
r1 = DON["roue1_3103"]
ctrl("ex3103 : roue 1 = 3 rouges, 2 bleus, 2 jaunes, 1 blanc",
     (r1.count("rouge"), r1.count("bleu"), r1.count("jaune"), r1.count("blanc")) == (3, 2, 2, 1))
ctrl("ex3103 : 360 / 8 = 45", R(360, 8) == 45)
q1 = {c: proba(r1, lambda x, c=c: x == c) for c in ("rouge", "bleu", "jaune", "blanc")}
ctrl("ex3103 : roue 1 probabilités", (q1["rouge"], q1["bleu"], q1["jaune"], q1["blanc"]) == (R(3, 8), R(1, 4), R(1, 4), R(1, 8)))
ctrl("ex3103 : 3/8 = 0,375 = 37,5 %", dec_fr(q1["rouge"]) == "0{,}375" and pct(q1["rouge"]) == r"37{,}5\ \%")
autre = proba(r1, lambda x: x != "rouge")
ctrl("ex3103 : autre que rouge 5/8 = 0,625", autre == R(5, 8) and dec_fr(autre) == "0{,}625")
r2 = DON["roue2_3103"]
ctrl("ex3103 : roue 2 = 180 + 90 + 90 = 360", sum(a for _, a in r2) == 360)
quarts = [c for c, a in r2 for _ in range(a // 90)]
q2 = {c: proba(quarts, lambda x, c=c: x == c) for c in ("rouge", "bleu", "jaune")}
ctrl("ex3103 : roue 2 en quarts 1/2, 1/4, 1/4", (q2["rouge"], q2["bleu"], q2["jaune"]) == (R(1, 2), R(1, 4), R(1, 4)))
ctrl("ex3103 : rouge meilleur avec roue 2 (4/8 > 3/8)", q2["rouge"] > q1["rouge"] and q2["rouge"] == R(4, 8))
ctrl("ex3103 : bleu à égalité", q1["bleu"] == q2["bleu"])
ctrl("ex3103 : Léo faux (1/3 ≠ 1/2)", q2["rouge"] != R(1, 3))

# ============================================================ 3089
lignes = re.findall(r"^\*\*([PF ]+)\*\*$", EX["3089"], re.M)
seq = "".join(lignes).replace(" ", "")
ctrl("ex3089 : 20 lancers écrits", len(seq) == 20)
ctrl("ex3089 : 8 piles, 12 faces", seq.count("P") == 8 and seq.count("F") == 12)
ctrl("ex3089 : 4 P par ligne", all(l.replace(" ", "").count("P") == 4 for l in lignes))
ctrl("ex3089 : se termine par deux F", seq.endswith("FF") and seq[-3] == "P")
fp, ff = R(8, 20), R(12, 20)
ctrl("ex3089 : 2/5 = 0,4 = 40 % ; 3/5 = 60 %", fp == R(2, 5) and pct(fp) == r"40\ \%" and ff == R(3, 5) and pct(ff) == r"60\ \%")
fc = R(243, 500)
ctrl("ex3089 : 243/500 = 0,486 = 48,6 %", dec_fr(fc) == "0{,}486" and pct(fc) == r"48{,}6\ \%")
ctrl("ex3089 : 25 × 20 = 500", 25 * 20 == 500)
ctrl("ex3089 : écarts 0,1 et 0,014", R(1, 2) - fp == R(1, 10) and R(1, 2) - fc == R(14, 1000))
ctrl("figure barres_3089 : données", DON["barres_3089"] == [("Inès", 20, 8), ("classe", 500, 243)])

# ============================================================ 3101
S = DON["sacs_3101"]
PS = {n: R(j, j + b) for n, (j, b) in S.items()}
ctrl("ex3101 : 3/8, 7/16, 1/2", (PS["A"], PS["B"], PS["C"]) == (R(3, 8), R(7, 16), R(1, 2)))
ctrl("ex3101 : seizièmes 6, 7, 8", [PS[n] * 16 for n in "ABC"] == [6, 7, 8])
ctrl("ex3101 : B a le plus de jaunes mais C meilleur", max(S, key=lambda n: S[n][0]) == "B" and PS["C"] > PS["B"])
ctrl("ex3101 : pourcentages 37,5 / 43,75 / 50", [pct(PS[n]) for n in "ABC"] == [r"37{,}5\ \%", r"43{,}75\ \%", r"50\ \%"])
ctrl("ex3101 : 7 ÷ 16 = 0,4375", dec_fr(PS["B"]) == "0{,}4375")
x = sp.symbols("x", integer=True, nonnegative=True)
ctrl("ex3101 : ajouter 2 jaunes au sac A", sp.solve(sp.Eq(R(1, 2) * (8 + x), 3 + x), x) == [2])
ctrl("ex3101 : retirer 2 bleus du sac B", sp.solve(sp.Eq(R(1, 2) * (16 - x), 7), x) == [2])
ctrl("ex3101 : vérifications 5/10 et 7/14", R(5, 10) == R(1, 2) and R(7, 14) == R(1, 2))
ctrl("ex3101 : erreur jaunes/bleus = 3/5", R(3, 5) != PS["A"])

# ============================================================ 3094
lm, ln = DON["lancers_Malik"], DON["lancers_Nora"]
tab = re.findall(r"^\| \$(\d)\$ \| \$(\d+)\$ \| \$(\d+)\$ \|$", EX["3094"], re.M)
ctrl("ex3094 : tableau de 6 lignes", len(tab) == 6)
ctrl("ex3094 : tableau = simulation de Malik", [int(m) for _, m, _ in tab] == [lm.count(k) for k in DE])
ctrl("ex3094 : tableau = simulation de Nora", [int(n) for _, _, n in tab] == [ln.count(k) for k in DE])
ctrl("ex3094 : totaux 600", len(lm) == 600 == len(ln) and sum(int(m) for _, m, _ in tab) == 600 and sum(int(n) for _, _, n in tab) == 600)
ctrl("ex3094 : Malik, 4 six dans les 12 premiers lancers", lm[:12].count(6) == 4)
f6m, f6n = R(lm.count(6), 600), R(ln.count(6), 600)
ctrl("ex3094 : Malik 101/600 ≈ 0,168 ≈ 0,17 ≈ 17 %", lm.count(6) == 101 and dec_fr(f6m, 3) == "0{,}168"
     and dec_fr(f6m, 2) == "0{,}17" and round(float(f6m) * 100) == 17)
ctrl("ex3094 : Nora 181/600 ≈ 0,302 ≈ 0,30 ≈ 30 %", ln.count(6) == 181 and dec_fr(f6n, 3) == "0{,}302"
     and dec_fr(f6n, 2) == "0{,}30" and round(float(f6n) * 100) == 30)
ctrl("ex3094 : 600 / 6 = 100", R(600, 6) == 100)
ctrl("ex3094 : Malik entre 93 et 111", min(lm.count(k) for k in DE) == 93 and max(lm.count(k) for k in DE) == 111)
ctrl("ex3094 : Nora, faces 1 à 5 sous 100", all(ln.count(k) < 100 for k in range(1, 6)))
ctrl("ex3094 : 4/12 = 1/3 ≈ 0,33", R(4, 12) == R(1, 3) and dec_fr(R(1, 3), 2) == "0{,}33")
fm = FIG.freq_six(lm)
fn = FIG.freq_six(ln)
ctrl("figure frequences_3094 : Malik à 12 lancers = 1/3", abs(fm[11][1] - 1 / 3) < 1e-12)
ctrl("figure frequences_3094 : Malik stabilisé vers 1/6 après 200 lancers (écart < 0,015)", all(abs(y - 1 / 6) < 0.015 for x, y in fm[199:]))
ctrl("figure frequences_3094 : Nora stabilisée vers 0,3 après 200 lancers (écart < 0,025)", all(abs(y - 0.3) < 0.025 for x, y in fn[199:]))
ctrl("figure frequences_3094 : courbes dans la fenêtre 0 → 0,6 (à partir de 2 lancers)", all(0 <= y <= 0.6 for x, y in fm[1:] + fn[1:]))
ctrl("figure frequences_3094 : « dé de Malik » sous la courbe de Malik vers 420 lancers", all(y > 0.13 for x, y in fm[380:460]))
ctrl("figure frequences_3094 : « dé de Nora » au-dessus de sa courbe vers 420 lancers", all(y < 0.355 for x, y in fn[380:460]))
dans("3094", r"\frac{101}{600} \approx 0{,}168 \approx 0{,}17", r"\frac{181}{600} \approx 0{,}302 \approx 0{,}30")

# ============================================================ 3092
roue12 = range(1, 13)
pa = proba(roue12, lambda k: k % 4 == 0)
ctrl("ex3092 : multiples de 4 = 4, 8, 12", tuple(k for k in roue12 if k % 4 == 0) == DON["gagnants_3092"])
ctrl("ex3092 : stand A 3/12 = 1/4 = 25 %", pa == R(1, 4) and pct(pa) == r"25\ \%")
urneB = ["dorée"] * 3 + ["blanche"] * 17
pb = proba(urneB, lambda c: c == "dorée")
ctrl("ex3092 : stand B 3/20 = 0,15 = 15 %", pb == R(3, 20) and dec_fr(pb) == "0{,}15" and pct(pb) == r"15\ \%")
pc = proba(DE, lambda k: k in (5, 6))
ctrl("ex3092 : stand C 2/6 = 1/3 ≈ 0,33", pc == R(1, 3) and dec_fr(pc, 2) == "0{,}33")
ctrl("ex3092 : B < A < C", pb < pa < pc)
ctrl("figure echelle_3092", DON["echelle_3092"] == {"B": pb, "A": pa, "C": pc})
f = R(57, 240)
ctrl("ex3092 : 57/240 = 19/80 = 0,2375 = 23,75 %", f == R(19, 80) and dec_fr(f) == "0{,}2375" and pct(f) == r"23{,}75\ \%")
ctrl("ex3092 : 23,75 % ≈ 24 %", round(float(f) * 100) == 24)
dans("3092", r"f &= \frac{57}{240} = \frac{19}{80} \\" + "\n" + r"&= 0{,}2375 = 23{,}75\ \%",
     r"&= \frac{3}{20} = \frac{15}{100} \\" + "\n" + r"&= 0{,}15 = 15\ \%")
dans("3089", r"f(\text{pile}) &= \frac{8}{20} = \frac{2}{5} \\" + "\n" + r"&= \frac{40}{100} = 0{,}4 = 40\ \%",
     r"f &= \frac{243}{500} = \frac{486}{1\,000} \\" + "\n" + r"&= 0{,}486 = 48{,}6\ \%")
dans("3101", r"\frac{3}{8} &= \frac{3 \times 2}{8 \times 2} = \frac{6}{16}", r"\frac{1}{2} &= \frac{1 \times 8}{2 \times 8} = \frac{8}{16}")
dans("3103", r"P(\text{autre que rouge}) &= \frac{5}{8} \\" + "\n" + r"&= 0{,}625 = 62{,}5\ \%")
dans("3102", r"P(\text{Yanis gagne}) &= \frac{4}{6} = \frac{2}{3}", r"P(\text{Zoé gagne}) &= \frac{3}{6} = \frac{1}{2}")

# ============================================================ 3102
z1, y1 = proba(DE, lambda k: k in (1, 2)), proba(DE, lambda k: k not in (1, 2))
ctrl("ex3102 : règle 1 : 1/3 et 2/3", (z1, y1) == (R(1, 3), R(2, 3)) and y1 == 2 * z1)
div10 = tuple(k for k in DE if 10 % k == 0)
ctrl("ex3102 : diviseurs de 10 sur le dé = 1, 2, 5", div10 == DON["regle2_3102"]["Zoé"] == (1, 2, 5))
ctrl("ex3102 : diviseurs de 10 = 1, 2, 5, 10", [d for d in range(1, 11) if 10 % d == 0] == [1, 2, 5, 10])
ctrl("ex3102 : Yanis 3, 4, 6", tuple(k for k in DE if k not in div10) == DON["regle2_3102"]["Yanis"])
z2 = proba(DE, lambda k: k in div10)
ctrl("ex3102 : règle 2 équitable 1/2", z2 == R(1, 2) == 1 - z2)
ctrl("ex3102 : échelle 0,33 / 0,67 / 0,5", dec_fr(z1, 2) == "0{,}33" and dec_fr(y1, 2) == "0{,}67"
     and DON["echelle_3102"] == {"Zoé1": z1, "Yanis1": y1, "regle2": z2})
f = R(23, 40)
ctrl("ex3102 : 23/40 = 0,575 = 57,5 %", dec_fr(f) == "0{,}575" and pct(f) == r"57{,}5\ \%")
ctrl("ex3102 : écart 0,075", f - R(1, 2) == R(75, 1000))
z3, y3 = proba(DE, lambda k: k % 3 == 0), proba(DE, lambda k: k <= 2)
ctrl("ex3102 : règle 3 : 1/3 chacun, 4 et 5 sans gagnant", z3 == y3 == R(1, 3)
     and [k for k in DE if not (k % 3 == 0 or k <= 2)] == [4, 5])

# ============================================================ STRUCTURE
meta = json.loads((ICI / "source_en_ligne" / "meta.json").read_text(encoding="utf-8"))
ids = [int(e) for e in EX]
retires = [int(m.group(1)) for m in re.finditer(r"^(\d+)\s", (ICI / "exercices_retires.txt").read_text(encoding="utf-8"), re.M)]
ids_ligne = {e["id"] for e in meta["exercices"]}
ctrl("structure : 10 exercices gardés", len(ids) == 10 and len(set(ids)) == 10)
ctrl("structure : 11 retirés", len(retires) == 11 and len(set(retires)) == 11)
ctrl("structure : gardés + retirés = 21 Id en ligne", set(ids) | set(retires) == ids_ligne and not set(ids) & set(retires))
corr = json.loads((ICI / "figures" / "correspondance.json").read_text(encoding="utf-8"))
titres, types = [], []
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
    ctrl(f"structure {eid} : un résultat par question", et.count("::: resultat") == ne)
    ctrl(f"structure {eid} : erreur fréquente ou à retenir", "::: attention" in et or "::: retenir" in et)
    ctrl(f"structure {eid} : une méthode par question", et.count("::: methode") == ne)
    imgs = set(re.findall(r"\[IMAGE_(\d+)\]", b))
    ctrl(f"structure {eid} : images appelées = déclarées", imgs == set(corr["exercices"].get(eid, {}).keys()))
    ctrl(f"structure {eid} : au moins une figure dans l'énoncé ou le corrigé", len(imgs) >= 1)
    for n, v in corr["exercices"].get(eid, {}).items():
        ctrl(f"structure {eid} : fichier {v['fichier']} présent", (ICI / "figures" / "images" / v["fichier"]).exists())
    ctrl(f"structure {eid} : encadrés équilibrés", len(re.findall(r"^::: \w", b, re.M)) == len(re.findall(r"^:::\s*$", b, re.M)))
ctrl("structure : titres uniques", len(set(titres)) == len(titres))
ctrl("structure : progression 3 D / 3 E / 2 P / 2 S",
     types == ["Découverte"] * 3 + ["Entraînement"] * 3 + ["Problème"] * 2 + ["Synthèse"] * 2)
for nom, genre, cle in (("cours_274.txt", "cours", "274"), ("fiche_194.txt", "fiches", "194")):
    t = (ICI / nom).read_text(encoding="utf-8")
    imgs = set(re.findall(r"\[IMAGE_(\d+)\]", t))
    ctrl(f"structure {nom} : images appelées = déclarées", imgs == set(corr[genre][cle].keys()))
    ctrl(f"structure {nom} : encadrés équilibrés", len(re.findall(r"^::: \w", t, re.M)) == len(re.findall(r"^:::\s*$", t, re.M)))
tout = ex_txt + cours + fiche
ctrl("aucune mention du brevet", "brevet" not in tout.lower())
ctrl("pas d'événement contraire (programme de 4e)", "contraire" not in tout.lower())
ctrl("pas de nombre premier (prolongement seulement en 5e)", "premier" not in tout.lower())
ctrl("aucun nom de chapitre dans les titres", all("Hasard et probabilités" not in t for t in titres))

print(f"{len(OK)} contrôles justes, {len(KO)} faux")
for k in KO:
    print("  FAUX :", k)
sys.exit(1 if KO else 0)
