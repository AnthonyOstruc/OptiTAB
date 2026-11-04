# -*- coding: utf-8 -*-
"""Vérification des calculs de la notion 261 (5e : opérations et priorités) avec sympy.

Tous les décimaux sont des fractions exactes (sympy.Rational) : aucun arrondi.
Les expressions sont évaluées par sympy à partir de leur écriture (priorités de Python
= priorités opératoires), et les arbres de calcul des figures sont recalculés.
"""
import importlib.util
from pathlib import Path

from sympy import Rational as R, sympify, Integer

n_ok = 0


def ok(cond, msg):
    global n_ok
    assert bool(cond), msg
    n_ok += 1


def d(s):
    """Nombre écrit à la française -> Rational exact."""
    return R(s.replace(",", ".").replace(" ", ""))


def ev(expr):
    """Évalue une expression écrite avec ×, ÷, [ ], virgules décimales."""
    e = expr.replace("×", "*").replace("÷", "/").replace("[", "(").replace("]", ")").replace("−", "-")
    e = e.replace(" ", "")
    # décimaux à la française -> Rational
    import re
    e = re.sub(r"(\d+),(\d+)", lambda m: "Rational('%s.%s')" % (m.group(1), m.group(2)), e)
    e = re.sub(r"(?<![\w.'])(\d+)(?![\w.'])", r"Integer(\1)", e)
    return sympify(e, locals={"Rational": R, "Integer": Integer}, rational=True)


def eq(expr, attendu, msg):
    v = ev(expr) if isinstance(expr, str) else expr
    a = d(attendu) if isinstance(attendu, str) else attendu
    ok(v == a, f"{msg} : {expr} = {v} au lieu de {a}")


# ====================================================================== cours
eq("14 + 6", 20, "cours tableau somme"); eq("14 - 6", 8, "cours tableau diff")
eq("14 × 6", 84, "cours tableau produit"); eq("84 ÷ 6", 14, "cours tableau quotient")
eq("9 + 5 × 3", 24, "cours nature somme"); eq("(9 + 5) × 3", 42, "cours nature produit")
eq("18 - 6 ÷ 3 + 2 × 4", 24, "cours A"); eq("18 - 2 + 8", 24, "cours A l1"); eq("16 + 8", 24, "cours A l2")
eq("24 ÷ 3 × 2", 16, "cours gauche-droite 1"); eq("24 ÷ (3 × 2)", 4, "cours mauvais ordre 1")
eq("12 - 5 + 2", 9, "cours gauche-droite 2"); eq("12 - (5 + 2)", 5, "cours mauvais ordre 2")
eq("(18 - 6) ÷ (3 + 1) × 5", 15, "cours B"); eq("12 ÷ 4 × 5", 15, "cours B l1"); eq("3 × 5", 15, "cours B l2")
eq("18 - 6 ÷ 3 + 1 × 5", 21, "cours B sans parenthèses")
eq("50 - [4 × (7 - 2) + 3]", 27, "cours C"); eq("50 - [4 × 5 + 3]", 27, "cours C l1"); eq("50 - [20 + 3]", 27, "cours C l2")
eq("2 × (9 - 4) + 6", 16, "cours D arbre"); eq("9 - 4", 5, "cours D 1"); eq("2 × 5", 10, "cours D 2")
eq("4 × (2 + 9)", 44, "cours traduire 1"); eq("30 - 12 ÷ 4", 27, "cours traduire 2"); eq("8 × (5 - 3)", 16, "cours traduire 3")
eq("17 + 48 + 3", 68, "cours regrouper +"); eq("(17 + 3) + 48", 68, "cours regrouper + b")
eq("25 × 7 × 4", 700, "cours regrouper ×")
eq("7 × 102", 714, "cours 7×102"); eq("7 × 100 + 7 × 2", 714, "cours 7×102 dév")
eq("13 × 99", 1287, "cours 13×99"); eq("13 × 100 - 13 × 1", 1287, "cours 13×99 dév"); eq("13 × 100 - 1", 1299, "cours 13×99 piège")
eq("6 × 4,5 + 4 × 4,5", 45, "cours factoriser"); eq("(6 + 4) × 4,5", 45, "cours factoriser b")
eq("19,8 × 5,1", "100,98", "cours ordre de grandeur"); eq("20 × 5", 100, "cours ordre de grandeur estim")
eq("(45 + 27) ÷ (3,5 + 2,5)", 12, "cours calculatrice")
ok(ev("45 + 27 ÷ 3,5 + 2,5") != 12, "cours calculatrice sans parenthèses")
eq("7,56 ÷ 0,6", "12,6", "cours division"); eq("75,6 ÷ 6", "12,6", "cours division b"); eq("12,6 × 0,6", "7,56", "cours division contrôle")
eq("3 ÷ 0,5", 6, "cours diviser par 0,5")
eq("3 × 9,5 + 4 × 6 + 2", "54,5", "cours cinéma"); eq("28,5 + 24 + 2", "54,5", "cours cinéma l1")
eq("3 × 10 + 4 × 6 + 2", 56, "cours cinéma estimation")
# division posée du cours : 75,6 ÷ 6
eq("7 - 1 × 6", 1, "posée cours 1"); eq("15 - 2 × 6", 3, "posée cours 2"); eq("36 - 6 × 6", 0, "posée cours 3")

# ====================================================================== fiche
eq("4 × (2 + 9)", 44, "fiche traduire"); eq("50 - [4 × (7 - 2) + 3]", 27, "fiche crochets")
eq("24 ÷ 3 × 2", 16, "fiche gauche-droite")
eq("12 + 3 × 5", 27, "fiche erreur 1"); eq("(12 + 3) × 5", 75, "fiche erreur 1 faux")
eq("40 ÷ 4 × 2", 20, "fiche erreur 2"); eq("40 ÷ (4 × 2)", 5, "fiche erreur 2 faux")
eq("23 ÷ 4", "5,75", "fiche boîtes"); ok(5 * 4 < 23 <= 6 * 4, "fiche 6 boîtes")

# ====================================================================== 2709
eq("15 + 5 × 4", 35, "2709 A"); eq("(15 + 5) × 4", 80, "2709 A faux")
eq("40 - 12 ÷ 4 × 2", 34, "2709 B"); eq("12 ÷ 4", 3, "2709 B1"); eq("40 - 6", 34, "2709 B2")
eq("30 ÷ 5 × 3", 18, "2709 C"); eq("30 ÷ (5 × 3)", 2, "2709 C Léa")
eq("50 - 20 - 8 + 3", 25, "2709 D"); eq("50 - 20 - (8 + 3)", 19, "2709 D faux")
eq("7 × 8 - 6 × 9 + 4", 6, "2709 E"); eq("7 × 8", 56, "2709 E1"); eq("6 × 9", 54, "2709 E2"); eq("56 - 54", 2, "2709 E3")

# ====================================================================== 2710
eq("3 × (8 + 2)", 30, "2710 A"); eq("3 × 8 + 2", 26, "2710 B")
eq("(25 - 5) ÷ (6 - 2)", 5, "2710 C")
eq("2 × [15 - (4 + 3)]", 16, "2710 D"); eq("2 × [15 - 7]", 16, "2710 D l1")
eq("[(9 - 3) × 4 + 6] ÷ 5", 6, "2710 E"); eq("[24 + 6] ÷ 5", 6, "2710 E l2")
eq("(20 - 2 × 3) ÷ 7", 2, "2710 arbre"); ok(ev("20 - 2 × 3 ÷ 7") != 2, "2710 arbre sans parenthèses")
eq("4 + 6 × 5 - 2", 32, "2710 sans parenthèses"); eq("(4 + 6) × 5 - 2", 48, "2710 a"); eq("(4 + 6) × (5 - 2)", 30, "2710 b")
# aucune autre façon simple d'obtenir 48 ou 30 n'est demandée ; on vérifie que les autres placements diffèrent
autres = ["4 + 6 × (5 - 2)", "(4 + 6 × 5) - 2", "4 + (6 × 5 - 2)"]
ok(all(ev(a) not in (48, 30) for a in autres), "2710 placements uniques")

# ====================================================================== 2716
eq("12 + 30", 42, "2716 1a"); eq("8 × 7", 56, "2716 1b"); eq("45 - 18", 27, "2716 1c"); eq("36 ÷ 4", 9, "2716 1d")
eq("5 + 3 × 6", 23, "2716 F"); eq("(5 + 3) × 6", 48, "2716 G"); eq("40 - 20 ÷ 4", 35, "2716 H"); eq("(40 - 20) ÷ 4", 5, "2716 K")
eq("6 × (4 + 5)", 54, "2716 3a"); eq("6 + 4 × 5", 26, "2716 3b"); eq("100 - 36 ÷ 4", 91, "2716 3c"); eq("(50 - 14) ÷ 4", 9, "2716 3d")
eq("3 × (12 - 7)", 15, "2716 L"); eq("20 ÷ 4 + 6", 11, "2716 M")
eq("8 + 2 × 5", 18, "2716 Tom 1"); eq("(8 + 2) × 5", 50, "2716 Tom 2")

# ====================================================================== 2717
eq("4 × 17 × 25", 1700, "2717 1a"); eq("37 + 48 + 63 + 52", 200, "2717 1b"); eq("2,5 × 13 × 4", 130, "2717 1c")
eq("8 × 105", 840, "2717 2"); eq("8 × 100 + 8 × 5", 840, "2717 2 dév")
eq("23 × 101", 2323, "2717 3a"); eq("34 × 99", 3366, "2717 3b"); eq("15 × 12", 180, "2717 3c")
eq("23 × 100 + 23", 2323, "2717 3a dév"); eq("3400 - 34", 3366, "2717 3b dév"); eq("150 + 30", 180, "2717 3c dév")
eq("37 × 8 + 37 × 2", 370, "2717 4a"); eq("4,7 × 13 - 4,7 × 3", 47, "2717 4b")
eq("18 × 0,5", 9, "2717 5a"); eq("46 × 0,25", "11,5", "2717 5b"); eq("46 ÷ 4", "11,5", "2717 5b bis")
eq("46 × 99", 4554, "2717 6"); eq("46 × 100 - 1", 4599, "2717 6 Inès")

# ====================================================================== 2706
eq("8,4 ÷ 0,7", 12, "2706 1"); eq("84 ÷ 7", 12, "2706 1b"); eq("12 × 0,7", "8,4", "2706 1 contrôle")
eq("9,12 ÷ 2,4", "3,8", "2706 2"); eq("91,2 ÷ 24", "3,8", "2706 2b"); eq("3,8 × 2,4", "9,12", "2706 2 contrôle")
eq("3 × 24", 72, "2706 posée 1"); eq("91 - 72", 19, "2706 posée 2"); eq("8 × 24", 192, "2706 posée 3")
eq("5,4 ÷ 0,45", 12, "2706 3"); eq("540 ÷ 45", 12, "2706 3b"); eq("450 + 90", 540, "2706 3 contrôle")
eq("2,35 ÷ 0,25", "9,4", "2706 4"); eq("235 ÷ 25", "9,4", "2706 4b"); eq("9 × 25", 225, "2706 4c")
eq("9 × 0,25", "2,25", "2706 5"); eq("2,35 - 2,25", "0,1", "2706 5 reste"); ok(9 * d("0,25") <= d("2,35") < 10 * d("0,25"), "2706 9 pleines")

# ====================================================================== 2714
eq("49,7 × 3,1", "154,07", "2714 1a"); eq("50 × 3", 150, "2714 1a estim")
eq("798 ÷ 3,8", 210, "2714 1b"); eq("800 ÷ 4", 200, "2714 1b estim")
eq("19,8 + 0,98 × 102", "119,76", "2714 1c"); eq("(19,8 + 0,98) × 102", "2119,56", "2714 1c faux")
eq("3 × 4,95 + 2 × 12,1", "39,05", "2714 2"); eq("3 × 5 + 2 × 12", 39, "2714 2 estim")
eq("36 + 24 ÷ 4 + 2", 44, "2714 3 Hugo"); eq("(36 + 24) ÷ (4 + 2)", 10, "2714 3")
eq("(12,6 + 5,4) ÷ (3 × 1,5)", 4, "2714 4"); eq("(12,6 + 5,4) ÷ 3 × 1,5", 9, "2714 4 faux")
eq("7,6 × 5,2", "39,52", "2714 5"); eq("76 × 52", 3952, "2714 5b")

# ====================================================================== 2705
eq("4 × (3 + 2)", 20, "2705 1"); eq("(3 + 2) × 2,5 + 4,6", "17,1", "2705 2")
eq("4 × [(3 + 2) × 2,5 + 4,6] + 6", "74,4", "2705 3"); eq("4 × 17,1 + 6", "74,4", "2705 3b")
eq("20 × 2,5 + 4 × 5 + 6", 76, "2705 4 estim")
eq("4 × (3 + 2) × 2,5 + 4,6 + 6", "60,6", "2705 5"); eq("74,4 - 60,6", "13,8", "2705 5 écart"); eq("3 × 4,6", "13,8", "2705 5 écart b")
eq("4 × [5 × 2,5 + 4,6] + 6", "74,4", "2705 3 l1"); eq("4 × [12,5 + 4,6] + 6", "74,4", "2705 3 l2"); eq("68,4 + 6", "74,4", "2705 3 l4")
eq("4 × 5 × 2,5 + 4,6 + 6", "60,6", "2705 5 l1"); eq("50 + 4,6 + 6", "60,6", "2705 5 l2")
eq("6 × 1 + 6 × 0,75", "10,5", "2724 1 dist"); eq("1 + 0,75", "1,75", "2724 1 décomposition")
eq("82 × 6 + 82 × 0,5", 533, "2707 repas dist"); eq("420 + 950 + 533", 1903, "2707 T l1")
eq("74,4 + 17,1", "91,5", "2705 6"); eq("91,5 - 80", "11,5", "2705 6 manque"); eq("80 - 74,4", "5,6", "2705 6 reste")

# ====================================================================== 2723
A = lambda n: 28 + n * d("3,5")
B = lambda n: 15 + n * d("4,2")
for n, a, b in ((17, "87,5", "86,4"), (18, "91", "90,6"), (19, "94,5", "94,8"), (20, "98", "99")):
    eq(A(n), a, f"2723 A({n})"); eq(B(n), b, f"2723 B({n})")
eq(A(18) - B(18), "0,4", "2723 écart 18"); eq(B(20) - A(20), 1, "2723 écart 20")
ok(all(B(n) < A(n) for n in range(1, 19)) and all(A(n) < B(n) for n in range(19, 200)), "2723 seuil 19")
eq("18 × 0,7", "12,6", "2723 4a"); eq("19 × 0,7", "13,3", "2723 4b")
eq("95 - 28", 67, "2723 5"); ok(A(19) <= 95 < A(20), "2723 max 19")
eq(A(10), 63, "2723 attention 10"); eq("2 × 63", 126, "2723 attention double")

# ====================================================================== 2724
eq("6 × 1,75", "10,5", "2724 1"); eq("6 + 4,5", "10,5", "2724 1b")
eq("4 × 6 × 1,75 - 3 + 5", 44, "2724 2"); eq("24 × 1,75", 42, "2724 2b")
eq("24 × 2 - 3 + 5", 50, "2724 2 estim")
eq("4 × (6 × 1,75 - 3) + 5", 35, "2724 4"); eq("4 × 7,5", 30, "2724 4b"); eq("44 - 35", 9, "2724 4 écart"); eq("4 × 3 - 3", 9, "2724 4 écart b")
eq("5 × 6 × 1,75 - 3 + 5", "54,5", "2724 5"); eq("54,5 - 50", "4,5", "2724 5 manque")
eq("50 - 5 + 3", 48, "2724 6"); eq("48 ÷ 30", "1,6", "2724 6b"); eq("30 × 1,6 - 3 + 5", 50, "2724 6 contrôle")

# ====================================================================== 2707
eq("2 × 26 + 24", 76, "2707 1"); eq("76 + 6", 82, "2707 1b")
eq("80 × 12,5", 1000, "2707 2 estim"); eq("76 × 12,5", 950, "2707 2"); eq("76 × 12 + 76 × 0,5", 950, "2707 2b"); eq("912 + 38", 950, "2707 2c")
eq("420 + 76 × 12,5 + 82 × 6,5", 1903, "2707 3"); eq("82 × 6,5", 533, "2707 3b"); eq("492 + 41", 533, "2707 3c")
eq("76 × 12,5 + 82 × 6,5", 1483, "2707 4")
eq("(1903 - 725) ÷ 76", "15,5", "2707 5"); eq("76 × 15,5", 1178, "2707 5 contrôle")
eq("(420 + 76 × 12,5 + 82 × 6,5 - 725) ÷ 76", "15,5", "2707 6")
z = ev("420 + 76 × 12,5 + 82 × 6,5 - 725 ÷ 76")
ok(1893 < z < 1894, "2707 6 Zoé environ 1 893"); ok(9 < R(725, 76) < 10, "2707 6 environ 10")

# ====================================================================== figures (valeurs dessinées)
spec = importlib.util.spec_from_file_location("figs261", Path(__file__).parent / "figures" / "figures.py")
F = importlib.util.module_from_spec(spec)
spec.loader.exec_module(F)
ok(F.evalue(F.COURS_ARBRE) == 16, "figure arbre cours")
ok(F.evalue(F.E_2709) == 6, "figure arbre 2709")
ok(F.evalue(F.A_2710) == 2, "figure arbre 2710")
ok(F.evalue(F.F_2724) == 44, "figure arbre 2724")
for nom in ("ex_ordre_arbre_corrige", "ex_parentheses_arbre_corrige", "ex_facture_arbre_corrige", "cours_arbre"):
    ok("resVide" not in F.FIGURES[nom], f"{nom} : toutes les cases remplies")
for nom in ("ex_ordre_arbre_enonce", "ex_parentheses_arbre_enonce"):
    ok("resVert" not in F.FIGURES[nom] and "resDonne" not in F.FIGURES[nom], f"{nom} : aucune réponse dans l'énoncé")
ok(F.FIGURES["ex_facture_arbre_enonce"].count("resDonne]") == 1, "2724 énoncé : seule la case 24 est donnée")
for attendu in ("$56$", "$54$", "$2$", "$6$"):
    ok(attendu in F.FIGURES["ex_ordre_arbre_corrige"], f"2709 figure contient {attendu}")
for attendu in ("$24$", "$42$", "$39$", "$44$"):
    ok(attendu in F.FIGURES["ex_facture_arbre_corrige"], f"2724 figure contient {attendu}")
ok("17{,}10" in F.FIGURES["ex_ateliers_corrige"] and "74{,}40" in F.FIGURES["ex_ateliers_corrige"], "2705 figure valeurs")
ok("54{,}50" in F.FIGURES["cours_probleme"], "cours figure cinéma")
ok("1\\,178 \\div 76 = 15{,}50" in F.FIGURES["ex_sortie_corrige"], "2707 figure valeurs")
ok("= 840" in F.FIGURES["ex_mental_aire_corrige"] and "= 714" in F.FIGURES["cours_aire"], "figures d'aire")
ok("2{,}25" in F.FIGURES["ex_bouteilles_corrige"] and "0{,}1" in F.FIGURES["ex_bouteilles_corrige"], "2706 figure bouteilles")
ok(F.fr(1903) == r"1\,903" and F.fr(F.num("17,1")) == "17{,}1", "format des nombres")

print(f"verif_261 : {n_ok} contrôles, tous justes.")
