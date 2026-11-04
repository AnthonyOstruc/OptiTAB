# -*- coding: utf-8 -*-
"""Vérification des calculs de la notion 269 (5e : développer, réduire et démontrer).

Cours, fiche, 10 exercices et figures : chaque développement, réduction,
factorisation, test d'égalité, calcul mental et démonstration est recalculé en
nombres exacts (sympy). Programmes de calcul exécutés étape par étape.
Contrôles de structure : 10 exercices, progression 3/3/3/1, aucune mention du
brevet, pas de double distributivité (4e), 10 gardés + 11 retirés = 21 Id,
figures appelées = figures déclarées.
Lancer : python verif_269.py
"""
import json
import re
from pathlib import Path

from sympy import Rational as R, symbols, expand, solve, factor, simplify, Integer as I

ICI = Path(__file__).resolve().parent
n_ok = 0
x, a, b, k, y, n, p, q = symbols("x a b k y n p q")


def ok(cond, msg):
    global n_ok
    assert cond, msg
    n_ok += 1


def d(s):
    """Décimal écrit à la française -> rationnel exact : '2,5' -> 5/2."""
    return R(s.replace(",", ".").replace(" ", ""))


def egal(e1, e2):
    """Égalité de deux expressions pour toutes les valeurs."""
    return simplify(expand(e1) - expand(e2)) == 0


def programme(depart, etapes):
    """Exécute un programme de calcul : liste de (opération, nombre). Renvoie les résultats successifs."""
    v, res = depart, [depart]
    for op, c in etapes:
        v = {"+": v + c, "-": v - c, "*": v * c, "/": v / c}[op]
        res.append(v)
    return res


# ================================================================== COURS
ok(egal(4 * x + 2, 4 * x + 2) and egal(4 * (x + 2), 4 * x + 8), "nature : 4x + 2 et 4(x + 2)")
ok(egal(k * (a + b), k * a + k * b) and egal(k * (a - b), k * a - k * b), "distributivité simple")
ok(6 * (10 + 3) == 78 == 6 * 10 + 6 * 3 and 6 * 13 == 78 and 60 + 18 == 78, "6 × (10 + 3) = 78")
ok(egal(3 * (x + 5), 3 * x + 15), "3(x + 5) = 3x + 15")
ok(egal(2 * (4 * a - 3), 8 * a - 6), "2(4a − 3) = 8a − 6")
ok(egal(d("0,5") * (x + 8), d("0,5") * x + 4), "0,5(x + 8) = 0,5x + 4")
ok(not egal(3 * (x + 5), 3 * x + 5), "3(x + 5) ≠ 3x + 5")
ok(egal(5 * x + 20, 5 * (x + 4)) and egal(7 * a - 7 * b, 7 * (a - b)) and egal(4 * x + 4, 4 * (x + 1)), "factorisations du cours")
ok(not egal(4 * x + 4, 4 * x), "4x + 4 ≠ 4x")
ok(8 * 103 == 824 == 800 + 24 and 12 * 99 == 1188 == 1200 - 12, "8 × 103 ; 12 × 99")
ok(45 * 7 + 45 * 3 == 450 == 45 * 10, "45 × 7 + 45 × 3")
ok(d("2,6") * 15 - d("2,6") * 5 == 26 == d("2,6") * 10, "2,6 × 15 − 2,6 × 5")
ok(egal(3 * x + 5 * x, 8 * x) and egal(7 * x - 2 * x, 5 * x), "3x + 5x ; 7x − 2x")
ok(egal(a * x + b * x, (a + b) * x), "ax + bx = (a + b)x")
ok(egal(2 * a + 3 + 4 * a, 6 * a + 3) and egal(x + x + x, 3 * x) and egal(4 * x + 9 + x - 2, 5 * x + 7), "réductions du cours")
ok(egal(d("2,5") * y + 4 + y + 1, d("3,5") * y + 5), "réduction décimale du cours")
ok(egal(2 * (x + 4) + 3 * x, 5 * x + 8) and egal(2 * x + 8 + 3 * x, 5 * x + 8), "2(x + 4) + 3x = 5x + 8")
ok(not egal(3 * x + 5, 8 * x) and egal(x + x, 2 * x) and egal(x * x, x ** 2) and not egal(2 * x, x ** 2), "erreurs de réduction")
e1, e2 = 2 * x + 3, 5 * x
ok(e1.subs(x, 1) == e2.subs(x, 1) == 5, "2x + 3 = 5x vraie pour 1")
ok(e1.subs(x, 2) == 7 and e2.subs(x, 2) == 10, "2x + 3 = 5x fausse pour 2 (7 et 10)")
ok(solve(e1 - e2, x) == [1], "2x + 3 = 5x : seule solution 1")
prog = programme(x, [("+", 5), ("*", 3), ("-", 15)])
ok(prog[1] == x + 5 and egal(prog[2], 3 * (x + 5)) and egal(prog[3], 3 * x), "programme du cours : le triple")
ok(all(programme(I(t), [("+", 5), ("*", 3), ("-", 15)])[-1] == 3 * t for t in range(0, 30)), "programme du cours exécuté")
ok(egal(2 * p + 2 * q, 2 * (p + q)), "somme de deux pairs")

# ================================================================== FICHE (mêmes exemples que le cours)
ok(egal(3 * (x + 5), 3 * x + 15) and egal(2 * (4 * a - 3), 8 * a - 6), "fiche : développer")
ok(egal(5 * x + 20, 5 * (x + 4)) and egal(4 * x + 4, 4 * (x + 1)), "fiche : factoriser")
ok(8 * 103 == 824 and 45 * 7 + 45 * 3 == 450, "fiche : calcul mental")
ok(egal(3 * x + 5 * x, 8 * x) and egal(7 * x - 2 * x, 5 * x) and egal(x + x + x, 3 * x), "fiche : réduire")
ok(egal(2 * a + 3 + 4 * a, 6 * a + 3) and egal(2 * (x + 4) + 3 * x, 5 * x + 8), "fiche : réduire 2")
ok(e1.subs(x, 2) == 7 and e2.subs(x, 2) == 10, "fiche : contre-exemple")

# ================================================================== 2875
ok(4 * (6 + 3) == 36 == 4 * 9, "quadrillage : 36")
ok(4 * 6 == 24 and 4 * 3 == 12 and 24 + 12 == 36, "24 + 12 = 36")
ok(7 * (10 + 2) == 84 == 7 * 12 and 7 * 10 + 7 * 2 == 84 and 70 + 14 == 84, "7 × (10 + 2)")
ok(5 * (8 - 3) == 25 == 5 * 5 and 5 * 8 - 5 * 3 == 25 and 40 - 15 == 25, "5 × (8 − 3)")
ok(egal(3 * x + 2, 3 * x + 2) and not egal(3 * x + 2, 3 * (x + 2)), "D ≠ E")

# ================================================================== 2873
ok(egal(4 * (x + 3), 4 * x + 12) and 4 * 3 == 12, "4(x + 3) = 4x + 12")
ok(4 * (5 + 3) == 32 and 4 * 8 == 32 and 4 * 5 + 12 == 32 and 20 + 12 == 32, "aire pour x = 5")
ok((4 * x + 3).subs(x, 5) == 23 and 23 != 32, "contre-exemple de Tom")
ok(egal(5 * (x + 2), 5 * x + 10) and egal(2 * (x + 7), 2 * x + 14), "5(x + 2) ; 2(x + 7)")

# ================================================================== 2877
ok(egal(3 * x + 5 * x, 8 * x) and egal(6 * a + a, 7 * a) and egal(9 * y - 4 * y, 5 * y) and egal(x + x + x + x, 4 * x), "Q1")
ok(egal(2 * a + 3 + 4 * a, 6 * a + 3) and egal(5 * x + 1 + 2 * x + 6, 7 * x + 7) and egal(8 + 3 * x - 2 + x, 4 * x + 6), "Q2")
ok(egal(d("1,5") * x + 2 + d("0,5") * x + d("0,4"), 2 * x + d("2,4")) and d("1,5") + d("0,5") == 2, "Q2 d) décimaux")
ok(egal(x + x, 2 * x) and egal(x * x, x ** 2), "Q3")
P = x + 2 * x + (x + 3)
ok(egal(P, 4 * x + 3) and P.subs(x, 4) == 19 and 4 + 8 + 7 == 19 and 4 * 4 + 3 == 19, "périmètre du triangle")
ok(4 + 7 > 8 and 4 + 8 > 7 and 8 + 7 > 4, "triangle de côtés 4, 8, 7 constructible")
ok(egal((x + 3 + x) - 2 * x, 3), "triangle constructible pour tout x > 0 : x + (x + 3) − 2x = 3 > 0")
ok((4 * x + 3).subs(x, 1) == (7 * x).subs(x, 1) == 7, "Lina : 7 et 7 pour x = 1")
ok((4 * x + 3).subs(x, 2) == 11 and (7 * x).subs(x, 2) == 14, "contre-exemple x = 2")

# ================================================================== 2880
ok(egal(5 * (x + 4), 5 * x + 20) and egal(3 * (2 * x - 1), 6 * x - 3) and egal(d("2,5") * (x + 4), d("2,5") * x + 10), "Q1 a-c")
ok(egal(4 * (3 + 2 * a), 12 + 8 * a) and egal(6 * (7 - y), 42 - 6 * y), "Q1 d-e")
ok(egal(3 * (2 * x + 1) + x, 7 * x + 3) and egal(6 * (3 + x) - 2 * x, 4 * x + 18), "Q2 a-b")
ok(egal(2 * (x + 5) + 3 * (x + 1), 5 * x + 13) and egal(4 * (2 * x + 3) - 5, 8 * x + 7), "Q2 c-d")
ok(egal(5 * (x + 3) + 2 * x, 7 * x + 15) and not egal(5 * (x + 3) + 2 * x, 7 * x + 3), "copie de Sami")
ok((3 * (2 * x + 1) + x).subs(x, 10) == 73 == 3 * 21 + 10 and 7 * 10 + 3 == 73, "contrôle x = 10")

# ================================================================== 2882
ok(egal(6 * x + 18, 6 * (x + 3)) and 6 * 3 == 18, "figure : 6(x + 3)")
ok(egal(5 * x + 15, 5 * (x + 3)) and egal(9 * a + 9 * b, 9 * (a + b)) and egal(15 * x - 10, 5 * (3 * x - 2)), "Q2 a-c")
ok(egal(8 * x + 8, 8 * (x + 1)) and egal(12 + 4 * y, 4 * (3 + y)), "Q2 d-e")
ok((15 * x - 10).as_content_primitive() == (5, 3 * x - 2) and (5 * x + 15).as_content_primitive() == (5, x + 3)
   and (8 * x + 8).as_content_primitive() == (8, x + 1) and (10 * x + 5).as_content_primitive() == (5, 2 * x + 1)
   and (6 * x + 18).as_content_primitive() == (6, x + 3) and (4 * x + 16).as_content_primitive() == (4, x + 4),
   "facteurs communs maximaux")
ok(egal(4 * x + 12 + 2 * x + 6, 6 * x + 18) and egal(6 * x + 18, 6 * (x + 3)), "Q3")
ok(not egal(5 * 2 * x, 10 * x + 5) and egal(10 * x + 5, 5 * (2 * x + 1)), "Hugo")

# ================================================================== 2881
ok(7 * 102 == 714 == 700 + 14, "7 × 102")
ok(15 * 99 == 1485 == 1500 - 15, "15 × 99")
ok(9 * 21 == 189 == 180 + 9 and 13 * 11 == 143 == 130 + 13, "9 × 21 ; 13 × 11")
ok(37 * 6 + 37 * 4 == 370, "37 × 6 + 37 × 4")
ok(d("8,5") * 13 - d("8,5") * 3 == 85 and d("1,7") * 58 + d("1,7") * 42 == 170, "8,5 et 1,7")
ok(99 * 5 + 5 == 500 == 5 * 100, "99 × 5 + 5")
ok(12 * 19 + 12 * 11 == 360 == 12 * 30, "maillots et shorts")
ok(6 * 14 == 84 == 60 + 24 and 60 + 4 == 64, "Léo")

# ================================================================== 2874
EG = {1: (2 * (x + 3), 2 * x + 6), 2: (3 * (x + 4), 3 * x + 4), 3: (x + x + x, 3 * x),
      4: (2 * x + 4, x + 6), 5: (5 * x - x, I(5))}
val2 = {i: (g.subs(x, 2), dr.subs(x, 2)) for i, (g, dr) in EG.items()}
ok(val2 == {1: (10, 10), 2: (18, 10), 3: (6, 6), 4: (8, 8), 5: (8, 5)}, "tests pour x = 2")
val5 = {i: (EG[i][0].subs(x, 5), EG[i][1].subs(x, 5)) for i in (1, 3, 4)}
ok(val5 == {1: (16, 16), 3: (15, 15), 4: (14, 11)}, "tests pour x = 5")
ok(egal(*EG[1]) and egal(*EG[3]), "(1) et (3) toujours vraies")
ok(not egal(*EG[2]) and not egal(*EG[4]) and not egal(*EG[5]), "(2), (4), (5) pas toujours vraies")
ok(solve(EG[4][0] - EG[4][1], x) == [2], "(4) vraie seulement pour x = 2")
ok(egal(3 * (x + 4), 3 * x + 12) and egal(5 * x - x, 4 * x), "corrections de (2) et (5)")

# ================================================================== 2893
A = [("*", 3), ("+", 4), ("*", 2)]
B = [("+", 1), ("*", 6), ("+", 2)]
C = [("+", 4), ("*", 6)]
ok(programme(2, A) == [2, 6, 10, 20] and programme(2, B) == [2, 3, 18, 20], "avec 2")
ok(programme(5, A) == [5, 15, 19, 38] and programme(5, B) == [5, 6, 36, 38], "avec 5")
ok(egal(programme(x, A)[-1], 2 * (3 * x + 4)) and egal(programme(x, B)[-1], 6 * (x + 1) + 2), "expressions A et B")
ok(egal(2 * (3 * x + 4), 6 * x + 8) and egal(6 * (x + 1) + 2, 6 * x + 8), "A = B = 6x + 8")
ok(programme(0, A)[-1] == 8 and programme(0, C) == [0, 4, 24], "contre-exemple 0 pour C")
ok(egal(programme(x, C)[-1], 6 * x + 24) and egal(programme(x, C)[-1] - programme(x, A)[-1], 16), "C − A = 16")
ok(R(50, 2) == 25 and 25 - 4 == 21 and R(21, 3) == 7 and programme(7, A)[-1] == 50 and 6 * 7 + 8 == 50, "remonter : 7")
ok(solve(6 * x + 8 - 50, x) == [7], "6x + 8 = 50 pour x = 7 seulement")

# ================================================================== 2887
ok(7 + 8 + 9 == 24 == 3 * 8 and 12 + 13 + 14 == 39 == 3 * 13 and 30 + 31 + 32 == 93 == 3 * 31, "trois exemples")
S = n + (n + 1) + (n + 2)
ok(egal(S, 3 * n + 3) and egal(S, 3 * (n + 1)), "3n + 3 = 3(n + 1)")
ok(R(141, 3) == 47 and 46 + 47 + 48 == 141, "141 = 46 + 47 + 48")
ok(3 * 33 == 99 and 3 * 34 == 102 and 100 % 3 != 0, "100 n'est pas un multiple de 3")
ok(1 + 2 + 3 + 4 == 10 and 10 % 4 != 0 and 4 * 2 == 8 and 4 * 3 == 12, "contre-exemple de Zoé")
ok(egal(n + (n + 1) + (n + 2) + (n + 3), 4 * n + 6), "4 consécutifs : 4n + 6 (pas toujours multiple de 4)")

# ================================================================== 2888
L_ = x + x + 3
ok(egal(L_, 2 * x + 3), "longueur 2x + 3")
ok(egal(5 * (2 * x + 3), 10 * x + 15) and egal(5 * x + 5 * x + 15, 10 * x + 15), "aire 10x + 15")
Pj = (2 * x + 3) + 5 + (2 * x + 3) + 5
ok(egal(Pj, 4 * x + 16) and egal(4 * x + 16, 4 * (x + 4)), "périmètre 4x + 16 = 4(x + 4)")
ok((10 * x + 15).subs(x, 4) == 55 == 5 * 11 and (2 * x + 3).subs(x, 4) == 11, "aire 55 pour x = 4")
ok(Pj.subs(x, 4) == 32 == 11 + 5 + 11 + 5 and 4 * 4 + 16 == 32, "périmètre 32 pour x = 4")
ok((10 * x + 15).subs(x, 8) == 95 and 2 * 55 == 110 and 95 != 110, "doubler x : 95 ≠ 110")
ok((2 * (2 * x + 3) + 5).subs(x, 4) != 32, "erreur fréquente détectée par le contrôle")

# ================================================================== contrôle des textes
TYPES = ("Découverte - ", "Entraînement - ", "Problème - ", "Synthèse - ")
ex = (ICI / "exercices.txt").read_text(encoding="utf-8")
titres = re.findall(r"^=== (.+)$", ex, re.M)
ok(len(titres) == 10 and len(set(titres)) == 10, "10 titres uniques")
ok(all(t.startswith(TYPES) for t in titres), "types de titres")
ok([t.split(" - ")[0] for t in titres] == ["Découverte"] * 3 + ["Entraînement"] * 3 + ["Problème"] * 3 + ["Synthèse"],
   "progression 3 / 3 / 3 / 1")
ok(all("Développer, réduire" not in t and "Calcul littéral" not in t for t in titres), "titres sans le nom du chapitre")
diffs = re.findall(r"^Difficulté:\s*(\w+)", ex, re.M)
ok(diffs == ["easy"] * 3 + ["medium"] * 3 + ["hard"] * 4, "difficultés cohérentes")
for nom in ("cours_264.txt", "fiche_184.txt", "exercices.txt"):
    txt = (ICI / nom).read_text(encoding="utf-8")
    ok("brevet" not in txt.lower(), f"pas de « brevet » dans {nom}")
    ok("double distributivit" not in txt.lower() and not re.search(r"\)\s*\(", txt), f"pas de double distributivité (4e) dans {nom}")
    ok("\\sqrt" not in txt, f"pas de racine carrée dans {nom}")
    ok(not re.search(r"(?<![\w)])-\s*\d+\s*\(|\(\s*-\s*\d", txt), f"pas de produit par un relatif (4e) dans {nom}")
ids = [int(m) for m in re.findall(r"^Id:\s*(\d+)", ex, re.M)]
retires = [int(m) for m in re.findall(r"^(\d+)", (ICI / "exercices_retires.txt").read_text(encoding="utf-8"), re.M)]
src = (ICI / "source_en_ligne" / "exercices.txt").read_text(encoding="utf-8")
ids_src = [int(m) for m in re.findall(r"^Id:\s*(\d+)", src, re.M)]
ok(len(ids) == 10 and len(retires) == 11 and not set(ids) & set(retires), "10 gardés, 11 retirés, disjoints")
ok(sorted(ids + retires) == sorted(ids_src) and len(ids_src) == 21, "gardés + retirés = les 21 Id en ligne")
for bloc in ex.split("\n===\n"):
    if not bloc.strip():
        continue
    tid = re.search(r"^Id:\s*(\d+)", bloc, re.M).group(1)
    nq_enonce = len(re.findall(r"^\d+\. ", bloc.split("Étapes:")[0], re.M))
    nq_etapes = len(re.findall(r"^## Question", bloc, re.M))
    nq_sol = len(re.findall(r"^\d+\. ", bloc.split("Solution:")[1], re.M))
    ok(nq_enonce == nq_etapes == nq_sol, f"{tid} : questions énoncé {nq_enonce} = corrigé {nq_etapes} = solution {nq_sol}")
    ok("::: attention" in bloc or "::: retenir" in bloc, f"{tid} : erreur fréquente ou à retenir")
    ok(bloc.count("::: resultat") >= nq_etapes, f"{tid} : un résultat par question")
    ok("Solution:" in bloc and "Étapes:" in bloc and "Énoncé:" in bloc, f"{tid} : rubriques")

# figures : chaque [IMAGE_N] appelé est déclaré, et chaque figure déclarée existe
corr = json.loads((ICI / "figures" / "correspondance.json").read_text(encoding="utf-8"))
images = ICI / "figures" / "images"
for bloc in ex.split("\n===\n"):
    if not bloc.strip():
        continue
    tid = re.search(r"^Id:\s*(\d+)", bloc, re.M).group(1)
    appels = sorted(set(re.findall(r"\[IMAGE_(\d+)\]", bloc)))
    decl = sorted(corr["exercices"].get(tid, {}).keys())
    ok(appels == decl, f"{tid} : images appelées {appels} = déclarées {decl}")
for nom, cle, idd in (("cours_264.txt", "cours", "264"), ("fiche_184.txt", "fiches", "184")):
    appels = sorted(set(re.findall(r"\[IMAGE_(\d+)\]", (ICI / nom).read_text(encoding="utf-8"))))
    ok(appels == sorted(corr[cle][idd].keys()), f"{nom} : images")
for cle in corr:
    for idd in corr[cle]:
        for pos, e in corr[cle][idd].items():
            ok((images / e["fichier"]).exists() and len(e["alt"]) >= 15, f"{cle} {idd} {pos} : fichier et alt")

# textes des figures = valeurs du texte (figures.py)
fig = (ICI / "figures" / "figures.py").read_text(encoding="utf-8")
for frag in ('"$4x$", "$12$"', '"$6x$", "$18$"', '"$700$", "$14$"', '"$5x$", "$5x$", "$15$"', '"$3x$", "$15$"',
             "$4 \\times 6 = 24$", "$4 \\times 3 = 12$", "$P = x + 2x + x + 3 = 4x + 3$", "$2(3x + 4)$", "$6(x + 1) + 2$"):
    ok(frag in fig, f"figure : {frag}")

print(f"verif_269 : {n_ok} contrôles, tous justes.")
