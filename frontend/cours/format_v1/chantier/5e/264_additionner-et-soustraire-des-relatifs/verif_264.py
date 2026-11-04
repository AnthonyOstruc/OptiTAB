# -*- coding: utf-8 -*-
"""Vérification des calculs de la notion 264 (5e : additionner et soustraire des relatifs).

Tous les décimaux sont des fractions exactes (sympy.Rational) : aucun arrondi.
Les expressions sont évaluées par sympy à partir de leur écriture à la française
(virgule décimale, signe moins typographique accepté). Les valeurs dessinées dans les
figures (figures/figures.py) sont recalculées, et les résultats écrits dans
exercices.txt / cours / fiche sont recherchés dans les fichiers.
"""
import importlib.util
import re
from pathlib import Path

from sympy import Integer, Rational as R, sympify

ICI = Path(__file__).parent
n_ok = 0


def ok(cond, msg):
    global n_ok
    assert bool(cond), msg
    n_ok += 1


def d(s):
    return R(str(s).replace(",", ".").replace(" ", "").replace("−", "-"))


def ev(expr):
    e = expr.replace("−", "-").replace(" ", "")
    e = re.sub(r"(\d+),(\d+)", lambda m: "Rational('%s.%s')" % (m.group(1), m.group(2)), e)
    e = re.sub(r"(?<![\w.'])(\d+)(?![\w.'])", r"Integer(\1)", e)
    return sympify(e, locals={"Rational": R, "Integer": Integer}, rational=True)


def eq(expr, attendu, msg):
    v = ev(expr)
    a = d(attendu) if isinstance(attendu, str) else attendu
    ok(v == a, f"{msg} : {expr} = {v} au lieu de {a}")


def dist0(x):
    return abs(x)


def somme_regle(a, b):
    """Addition par la règle des signes (même signe / signes contraires), comparée à a + b."""
    a, b = d(a), d(b)
    if a == 0 or b == 0:
        return a + b
    if (a > 0) == (b > 0):
        r = dist0(a) + dist0(b)
        return r if a > 0 else -r
    r = abs(dist0(a) - dist0(b))
    plus_loin = a if dist0(a) > dist0(b) else b
    return r if plus_loin > 0 else -r


def regle(a, b, attendu, msg):
    v = somme_regle(a, b)
    ok(v == d(a) + d(b), f"{msg} : règle ≠ somme")
    ok(v == d(attendu), f"{msg} : ({a}) + ({b}) = {v} au lieu de {attendu}")


COURS = (ICI / "cours_259.txt").read_text(encoding="utf-8")
FICHE = (ICI / "fiche_179.txt").read_text(encoding="utf-8")
EXOS = (ICI / "exercices.txt").read_text(encoding="utf-8")


def present(texte, morceau, msg):
    ok(morceau in texte, f"{msg} : « {morceau} » absent")


# ====================================================================== cours
regle(-2, 5, 3, "cours droite 1"); regle(1, -4, -3, "cours droite 2")
regle(-6, -3, -9, "cours même signe -"); regle("2,5", 4, "6,5", "cours même signe +")
regle(-9, 4, -5, "cours contraires 1"); regle(7, -2, 5, "cours contraires 2")
regle("-1,8", "0,6", "-1,2", "cours contraires décimaux")
regle(-3, 3, 0, "cours opposés"); eq("(-4) + 0", -4, "cours zéro")
regle(-5, -3, -8, "cours erreur fréquente"); ok(d(-8) not in (8, -2), "cours erreur : ni 8 ni -2")
eq("2 - (-3)", 5, "cours soustraction 1"); eq("2 + 3", 5, "cours soustraction 1b")
eq("-1 - (+4)", -5, "cours soustraction 2"); eq("-1 + (-4)", -5, "cours soustraction 2b")
eq("6 - 10", -4, "cours autres 1"); eq("-5 - (-2)", -3, "cours autres 2"); eq("0 - (-7)", 7, "cours autres 3")
eq("-2,4 - 1,6", -4, "cours autres 4")
eq("3 - (-4)", 7, "cours terme manquant"); eq("7 + (-4)", 3, "cours terme manquant vérif")
eq("(-2) + (+7) - (-5) - (+4)", 6, "cours somme algébrique"); eq("-2 + 7 + 5 - 4", 6, "cours écriture simplifiée")
for s_, r_ in (("+(+5)", 5), ("+(-5)", -5), ("-(+5)", -5), ("-(-5)", 5)):
    eq("0" + s_, r_, f"cours tableau {s_}")
eq("9 - 4 - 7 + 3", 1, "cours regrouper 1"); eq("(9 + 3) + (-4 - 7)", 1, "cours regrouper 1b"); eq("12 + (-11)", 1, "cours regrouper 1c")
eq("-5 + 8 - 3 + 5 - 6", -1, "cours regrouper 2"); eq("(-5 + 5) + 8 - 3 - 6", -1, "cours regrouper 2b"); eq("0 + 8 - 9", -1, "cours regrouper 2c")
eq("10 - (2 - 6)", 14, "cours parenthèses"); eq("10 - (-4)", 14, "cours parenthèses b")
eq("10 - 4 - 3", 3, "cours attention 1"); eq("10 - (4 - 3)", 9, "cours attention 2")
eq("5 - (-7)", 12, "cours variation 1"); eq("-1 - 5", -6, "cours variation 2")
eq("12 - (-9)", 21, "cours écart altitudes"); eq("2 - (-3,5)", "5,5", "cours distance droite")
for m in ("$(-6) + (-3) = -9$", "$(+2{,}5) + (+4) = +6{,}5$", "$(-9) + (+4) = -5$", "$(+7) + (-2) = +5$",
          "$(-1{,}8) + (+0{,}6) = -1{,}2$", "$(-3) + (+3) = 0$", "$(-5) + (-3) = -8$", "$6 - 10 = 6 + (-10) = -4$",
          "$-5 - (-2) = -5 + 2 = -3$", "$0 - (-7) = 0 + 7 = 7$", "$-2{,}4 - 1{,}6 = -2{,}4 + (-1{,}6) = -4$",
          "$3 - (-4) = 3 + 4 = 7$", "$5 - (-7) = 5 + 7 = 12$", "$-1 - 5 = -6$", "$12 - (-9) = 12 + 9 = 21$",
          "$2 - (-3{,}5) = 5{,}5$", "$10 - 4 - 3 = 3$", "$10 - (4 - 3) = 10 - 1 = 9$"):
    present(COURS, m, "cours écrit")

# ====================================================================== fiche
for m in ("$(-6) + (-3) = -9$", "$(-9) + (+4) = -5$", "$(-3) + (+3) = 0$", "$2 - (-3) = 2 + 3 = 5$",
          "$-1 - (+4) = -1 + (-4) = -5$", "$3 - (-4) = 7$", "$10 - (2 - 6) = 10 - (-4) = 14$",
          "$5 - (-7) = +12$", "$(-5) + (-3) = -8$", "$10 - (4 - 3) = 9$"):
    present(FICHE, m, "fiche écrit")
eq("3 - (-4)", 7, "fiche terme manquant")

# ====================================================================== 2772
regle(-3, 5, 2, "2772 1a"); regle(2, -6, -4, "2772 1b"); regle(-1, -4, -5, "2772 1c")
regle(-7, 7, 0, "2772 2"); regle(-12, -9, -21, "2772 3a"); regle(15, -23, -8, "2772 3b")
regle("-3,5", "8,2", "4,7", "2772 3c"); regle(-6, -4, -10, "2772 4")
eq("12 + 9", 21, "2772 3a dist"); eq("23 - 15", 8, "2772 3b dist"); eq("8,2 - 3,5", "4,7", "2772 3c dist"); eq("6 + 4", 10, "2772 4 dist")
ok([-3 + k for k in range(1, 6)] == [-2, -1, 0, 1, 2], "2772 1a graduations parcourues")
ok(2 - 2 == 0 and 0 - 4 == -4, "2772 1b passage par 0")

# ====================================================================== 2773
ok(-(-4) == 4 and -(9) == -9, "2773 1a opposés")
eq("7 - (-4)", 11, "2773 1b"); eq("7 + 4", 11, "2773 1b'"); eq("-6 - (+2)", -8, "2773 1c"); eq("-6 + (-2)", -8, "2773 1c'")
eq("-3 - (-8)", 5, "2773 2a"); eq("2,5 - (+6)", "-3,5", "2773 2b"); eq("-1,2 - (-1,2)", 0, "2773 2c"); eq("0 - (+5)", -5, "2773 2d")
eq("8 - 3", 5, "2773 2a dist"); eq("6 - 2,5", "3,5", "2773 2b dist")
ok(ev("-3 - 8") != 5 and ev("-3 + (-8)") != 5, "2773 attention : écritures fausses")
eq("1 - (-4)", 5, "2773 3a"); eq("1 - (+4)", -3, "2773 3b")
eq("4 - 9", -5, "2773 4a"); eq("9 - 4", 5, "2773 4b"); ok(ev("4 - 9") == -ev("9 - 4"), "2773 4 opposés")

# ====================================================================== 2768
t6, h, b, nuit = -4, 7, -5, -6
midi = t6 + h; t18 = midi + b
ok(midi == 3 and t18 == -2, "2768 3")
eq("(-4) + (+7)", 3, "2768 midi"); eq("3 + (-5)", -2, "2768 18 h")
eq("(-2) - (-4)", 2, "2768 4"); eq("(+7) + (-5)", 2, "2768 4 contrôle")
eq("(-6) - (-2)", -4, "2768 5"); eq("3 - (-6)", 9, "2768 6")
ok(max(t6, midi, t18, nuit) == 3 and min(t6, midi, t18, nuit) == -6, "2768 6 extrêmes")

# ====================================================================== 2779
eq("(+5) + (-8) - (-3)", 0, "2779 A"); eq("5 - 8 + 3", 0, "2779 A simpl"); eq("-3 + 3", 0, "2779 A l2")
eq("(-4) - (+6) + (-2) - (-9)", -3, "2779 B"); eq("-4 - 6 - 2 + 9", -3, "2779 B simpl")
eq("-10 - 2 + 9", -3, "2779 B l2"); eq("-12 + 9", -3, "2779 B l3")
eq("(+2,5) - (+4) + (-1,5) - (-7)", 4, "2779 C"); eq("2,5 - 4 - 1,5 + 7", 4, "2779 C simpl")
eq("-1,5 - 1,5 + 7", 4, "2779 C l2"); eq("-3 + 7", 4, "2779 C l3")
eq("-7 + 4 - 9 + 12 - 3 + 1", -2, "2779 D"); eq("4 + 12 + 1", 17, "2779 D +"); eq("-7 - 9 - 3", -19, "2779 D -"); eq("17 + (-19)", -2, "2779 D fin")
eq("13,6 - 8 + 5 - 13,6 + 8 - 11", -6, "2779 E"); eq("(13,6 - 13,6) + (-8 + 8) + 5 - 11", -6, "2779 E regroupé")
eq("(-3) - (-5)", 2, "2779 Mila juste"); eq("-3 - 5", -8, "2779 Mila faux")

# ====================================================================== 2780
eq("8 - (3 - 5)", 10, "2780 F"); eq("3 - 5", -2, "2780 F par"); eq("8 + 2", 10, "2780 F l2")
eq("(-4 + 9) - (2 - 10)", 13, "2780 G"); eq("-4 + 9", 5, "2780 G p1"); eq("2 - 10", -8, "2780 G p2"); eq("5 - (-8)", 13, "2780 G l1")
eq("-6,5 + (1,5 - 4) - (-3)", -6, "2780 H"); eq("1,5 - 4", "-2,5", "2780 H par"); eq("4 - 1,5", "2,5", "2780 H dist")
eq("-6,5 + (-2,5) - (-3)", -6, "2780 H l1"); eq("-6,5 - 2,5 + 3", -6, "2780 H l2"); eq("-9 + 3", -6, "2780 H l3")
eq("15 - 7 - 3", 5, "2780 K"); eq("8 - 3", 5, "2780 K l1"); eq("15 - (7 - 3)", 11, "2780 L"); eq("15 - 4", 11, "2780 L l1")
eq("8 - 3 - 5", 0, "2780 Lucas faux")

# ====================================================================== 2769
spec = importlib.util.spec_from_file_location("figs264", ICI / "figures" / "figures.py")
F = importlib.util.module_from_spec(spec)
spec.loader.exec_module(F)

r1 = F.etages(F.P1_BASE)
ok(r1 == [[-3, 5, -8, 2], [2, -3, -6], [-1, -9], [-10]], f"2769 pyramide 1 : {r1}")
eq("(-3) + 5", 2, "2769 p1 a"); eq("5 + (-8)", -3, "2769 p1 b"); eq("(-8) + 2", -6, "2769 p1 c")
eq("2 + (-3)", -1, "2769 p1 d"); eq("(-3) + (-6)", -9, "2769 p1 e"); eq("(-1) + (-9)", -10, "2769 p1 sommet")
r2 = F.p2_complete()
ok(r2 == [[4, -6, -7], [-2, -13], [-15]], f"2769 pyramide 2 : {r2}")
eq("-2 - 4", -6, "2769 p2 case"); eq("4 + (-6)", -2, "2769 p2 vérif"); eq("(-6) + (-7)", -13, "2769 p2 b"); eq("(-2) + (-13)", -15, "2769 p2 sommet")
r3 = F.etages(F.P1_MODIF)
ok(r3 == [[-3, 5, -8, -2], [2, -3, -10], [-1, -13], [-14]], f"2769 pyramide modifiée : {r3}")
eq("(-8) + (-2)", -10, "2769 3 a"); eq("(-3) + (-10)", -13, "2769 3 b"); eq("(-1) + (-13)", -14, "2769 3 sommet")
eq("-14 - (-10)", -4, "2769 3 variation")
eq("2 - (-5)", 7, "2769 4a"); eq("(-5) + 7", 2, "2769 4a vérif")
eq("-3 - (-8)", 5, "2769 4b"); eq("5 + (-8)", -3, "2769 4b vérif")
eq("-10 - (-6)", -4, "2769 4c"); eq("-4 - 6", -10, "2769 4c vérif")

# ====================================================================== 2787
alt = F.sm_altitudes()
ok(alt == [-15, -27, -20, -38], f"2787 altitudes : {alt}")
eq("(-15) + (-12)", -27, "2787 2a"); eq("(-27) + (+7)", -20, "2787 2b"); eq("(-20) + (-18)", -38, "2787 2c")
eq("(-38) - (-15)", -23, "2787 3 a"); eq("-38 + 15", -23, "2787 3 a'"); eq("-12 + 7 - 18", -23, "2787 3 b"); eq("-5 - 18", -23, "2787 3 b'")
eq("12 + 7 + 18", 37, "2787 4"); eq("8 - (-38)", 46, "2787 5"); eq("0 - (-38)", 38, "2787 6")
ok(F.SM_GOELAND - alt[-1] == 46, "2787 figure écart")

# ====================================================================== 2786
s0 = d("-12,50"); ops = [d("18,75"), d("-9,40"), d("-14,60"), d("6,25")]
soldes = []
s = s0
for o in ops:
    s += o
    soldes.append(s)
ok(soldes == [d("6,25"), d("-3,15"), d("-17,75"), d("-11,50")], f"2786 soldes : {soldes}")
eq("(-12,50) + (+18,75)", "6,25", "2786 3 mars"); eq("6,25 + (-9,40)", "-3,15", "2786 5 mars")
eq("(-3,15) + (-14,60)", "-17,75", "2786 9 mars"); eq("(-17,75) + (+6,25)", "-11,50", "2786 12 mars")
ok(min(soldes + [s0]) == d("-17,75") and sorted([d("-17,75"), d("-12,50"), d("-11,50"), d("-3,15")]) == [d("-17,75"), d("-12,50"), d("-11,50"), d("-3,15")], "2786 3 ordre")
eq("(-11,50) - (-12,50)", 1, "2786 4"); eq("18,75 - 9,40 - 14,60 + 6,25", 1, "2786 4 vérif")
eq("(18,75 + 6,25) - (9,40 + 14,60)", 1, "2786 4 regroupé"); eq("18,75 + 6,25", 25, "2786 4 +"); eq("9,40 + 14,60", 24, "2786 4 -")
eq("0 - (-11,50)", "11,50", "2786 5"); eq("20 - (-11,50)", "31,50", "2786 6"); eq("-11,50 + 31,50", 20, "2786 6 vérif")
eq("20 - 11,50", "8,50", "2786 erreur"); eq("-11,50 + 8,50", -3, "2786 erreur conséquence")

# ====================================================================== 2770
mins = [d(-8), d("-11,5"), d(-5), d("-2,5"), d(F.V_MIN)]
maxs = [d(3), d(-1), d("4,5"), d(6), d(F.V_MAX)]
ok(F.V_MIN == -6 and F.V_MAX == 2, "2770 vendredi")
amp = [M - m for M, m in zip(maxs, mins)]
ok(amp == [11, d("10,5"), d("9,5"), d("8,5"), 8], f"2770 amplitudes : {amp}")
eq("3 - (-8)", 11, "2770 lundi"); eq("-1 - (-11,5)", "10,5", "2770 mardi"); eq("4,5 - (-5)", "9,5", "2770 mercredi")
eq("6 - (-2,5)", "8,5", "2770 jeudi"); eq("2 - (-6)", 8, "2770 vendredi")
ok(amp.index(max(amp)) == 0, "2770 3 lundi")
eq("-11,5 - (-8)", "-3,5", "2770 4a"); eq("-5 - (-11,5)", "6,5", "2770 4b")
ok(maxs[1] < 0, "2770 5 gel mardi")
eq("-6 + (-4,5)", "-10,5", "2770 6 min"); eq("-10,5 + 9", "-1,5", "2770 6 max"); eq("-1,5 - (-10,5)", 9, "2770 6 vérif")
eq("2 - 6", -4, "2770 erreur")

# ====================================================================== 2771
ca = F.cases(F.CARTES_A)
ok(ca == [0, 4, -3, -5, 1], f"2771 Anaïs : {ca}")
eq("0 + (+4)", 4, "2771 a1"); eq("4 + (-7)", -3, "2771 a2"); eq("(-3) + (-2)", -5, "2771 a3"); eq("(-5) + (+6)", 1, "2771 a4")
eq("(-3) + (+5) + (-8)", -6, "2771 2"); eq("2 - 8", -6, "2771 2 l2")
ok(F.CARTE_B4 == 4, "2771 3 carte"); eq("-2 - (-6)", 4, "2771 3"); eq("-6 + 4", -2, "2771 3 vérif")
cb = F.cases(F.CARTES_B3 + [F.CARTE_B4])
ok(cb == [0, -3, 2, -6, -2], f"2771 Bastien : {cb}")
eq("1 - (-2)", 3, "2771 4"); ok(abs(1) < abs(-2), "2771 5 Anaïs gagne")
eq("-7 - 2 + 4 + 6", 1, "2771 6"); eq("-9 + 10", 1, "2771 6 l2")
from itertools import permutations
ok({sum(p) for p in permutations(F.CARTES_A)} == {1}, "2771 6 tout ordre")
ok(all(-7 <= c <= 7 for c in ca + cb), "2771 la piste dessinée (-7 à 7) contient tous les parcours")

# ====================================================================== figures : valeurs dessinées
ok("$(-2) + (+5) = 3$" in F.FIGURES["cours_addition"] and "$(+1) + (-4) = -3$" in F.FIGURES["cours_addition"], "fig cours addition")
ok("$2 - (-3) = 2 + (+3) = 5$" in F.FIGURES["cours_soustraction"] and "$-1 - (+4) = -1 + (-4) = -5$" in F.FIGURES["cours_soustraction"], "fig cours soustraction")
ok("$+12$ °C" in F.FIGURES["cours_thermometre"] and "$-6$ °C" in F.FIGURES["cours_thermometre"], "fig cours thermomètre")
ok("$12 - (-9)$" in F.FIGURES["cours_altitudes"] and "$= 21$ m" in F.FIGURES["cours_altitudes"], "fig cours altitudes")
for lettre, a, b in F.EX_ADD:
    ok(f"$({F.sg(a)}) + ({F.sg(b)}) = {F.nb(a + b)}$" in F.FIGURES["ex_addition_corrige"], f"fig 2772 {lettre}")
    ok(f"= {F.nb(a + b)}$" not in F.FIGURES["ex_addition_enonce"], f"fig 2772 énoncé sans réponse {lettre}")
ok([a + b for _, a, b in F.EX_ADD] == [2, -4, -5], "fig 2772 valeurs")
ok("= 5$" in F.FIGURES["ex_soustraction_corrige"] and "= -3$" in F.FIGURES["ex_soustraction_corrige"], "fig 2773")
ok("= " not in F.FIGURES["ex_soustraction_enonce"], "fig 2773 énoncé sans réponse")
ok("VERT" not in F.FIGURES["ex_journee_enonce"] and "otGreenDark" not in F.FIGURES["ex_journee_enonce"], "fig 2768 énoncé sans réponse")
for v in ("$+7$", "$-5$", "$-4$", "midi : $3$", "18 h : $-2$", "nuit : $-6$"):
    ok(v in F.FIGURES["ex_journee_corrige"], f"fig 2768 corrigé {v}")
for nom in ("ex_pyramides_enonce", "ex_station_enonce", "ex_sousmarin_enonce", "ex_piste_enonce", "ex_addition_enonce", "ex_soustraction_enonce"):
    ok("otGreenDark" not in F.FIGURES[nom], f"{nom} : aucune réponse (vert) dans l'énoncé")
ok("$-10$" not in F.FIGURES["ex_pyramides_enonce"] and "$-15$" not in F.FIGURES["ex_pyramides_enonce"], "fig 2769 énoncé sans sommets")
ok("-6" not in F.FIGURES["ex_station_enonce"].split("vendredi")[1], "fig 2770 énoncé : valeur non écrite")
ok("$2 - (-6) = 8$" in F.FIGURES["ex_station_corrige"], "fig 2770 corrigé")
ok("{$-38$ m}" in F.FIGURES["ex_sousmarin_corrige"] and "$46$ m" in F.FIGURES["ex_sousmarin_corrige"], "fig 2787 corrigé")

# ====================================================================== textes : solutions écrites
for m in ("1. a) $2$ ; b) $-4$ ; c) $-5$.", "c) $4{,}7$ (signes contraires)", "2. a) $5$ ; b) $-3{,}5$ ; c) $0$ ; d) $-5$.",
          "6. $3 - (-6) = 9$", "$A = 5 - 8 + 3 = 0$", "$B = -4 - 6 - 2 + 9 = -3$", "$C = 2{,}5 - 4 - 1{,}5 + 7 = 4$",
          "$D = 17 + (-19) = -2$", "3. $E = -6$.", "1. $F = 8 - (-2) = 10$.", "2. $G = 5 - (-8) = 13$.", "$K = 5$ et $L = 11$",
          "sommet $-10$", "sommet $-15$", "Nouveau sommet $-14$ : variation $-4$.", "4. a) $7$ ; b) $5$ ; c) $-4$.",
          "$-27$ m ; $-20$ m ; $-38$ m", "$8 - (-38) = 46$ m", "$0 - (-38) = +38$ m",
          "$6{,}25$ € ; $-3{,}15$ € ; $-17{,}75$ € ; $-11{,}50$ €", "6. $31{,}50$ €.",
          "2. $11$ ; $10{,}5$ ; $9{,}5$ ; $8{,}5$ ; $8$", "6. Minimale $-10{,}5$ °C ; maximale $-1{,}5$ °C.",
          "1. $4$ ; $-3$ ; $-5$ ; $1$.", "3. $-2 - (-6) = +4$.", "4. $1 - (-2) = 3$ cases."):
    present(EXOS, m, "solution écrite")
ok("brevet" not in (EXOS + COURS + FICHE).lower(), "aucune mention du brevet")
titres = re.findall(r"^=== (.+)$", EXOS, re.M)
ok(len(titres) == 10 and len(set(titres)) == 10, "10 titres uniques")
ok([t.split(" - ")[0] for t in titres] == ["Découverte"] * 3 + ["Entraînement"] * 3 + ["Problème"] * 2 + ["Synthèse"] * 2,
   "progression Découverte / Entraînement / Problème / Synthèse")

print(f"verif_264 : {n_ok} contrôles, tous justes.")
