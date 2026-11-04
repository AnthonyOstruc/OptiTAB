# -*- coding: utf-8 -*-
"""Vérification des calculs de la notion 267 (5e : carrés et cubes).

Cours, fiche, 10 exercices et figures : chaque résultat est recalculé en
nombres exacts (sympy.Rational, sympy.Integer, sympy.symbols).
Contrôles de structure : 10 exercices, progression, aucune mention du brevet,
10 gardés + 11 retirés = 21, figures appelées = figures déclarées.
Lancer : python verif_267.py
"""
import json
import re
from pathlib import Path

from sympy import Rational as R, Integer as I, symbols, expand, solve, integer_nthroot, pi

ICI = Path(__file__).resolve().parent
n_ok = 0
x = symbols("x")


def ok(cond, msg):
    global n_ok
    assert cond, msg
    n_ok += 1


def d(s):
    """Décimal écrit à la française -> rationnel exact : '2,25' -> 9/4."""
    return R(s.replace(",", ".").replace(" ", ""))


def carre_parfait(n):
    return integer_nthroot(int(n), 2)[1]


def cube_parfait(n):
    return integer_nthroot(int(n), 3)[1]


# ================================================================== COURS
ok(I(5) ** 2 == 25 and 5 * 5 == 25, "carré de 5 carreaux")
ok(4 * 4 == 16 and I(4) ** 3 == 64 and 4 * 16 == 64, "cube de 4 : 4 couches de 16")
ok(I(6) ** 2 == 36 and d("0,7") ** 2 == d("0,49") and d("1,1") ** 2 == d("1,21"), "exemples de carrés")
ok(I(2) ** 3 == 8 and I(10) ** 3 == 1000, "2³ et 10³")
ok(d("0,2") ** 2 == d("0,04") and d("0,04") * d("0,2") == d("0,008") == d("0,2") ** 3, "0,2³")
ok(I(2) ** 4 == 2 * 2 * 2 * 2, "2⁴ (remarque)")
ok(I(5) ** 2 != 5 * 2 and I(2) ** 3 != 2 * 3 and d("0,7") ** 2 not in (2 * d("0,7"), d("4,9")), "erreurs exposant")
ok([a ** 2 for a in range(13)] == [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144], "table des carrés 0..12")
ok([a ** 3 for a in (0, 1, 2, 3, 4, 5, 10)] == [0, 1, 8, 27, 64, 125, 1000], "table des cubes")
ok(7 * 7 == 49 and 10 ** 3 == 1000 and 1 ** 2 == 1 ** 3 == 1, "écrire comme carré / cube")
ok(36 < 40 < 49 and not carre_parfait(40), "40 n'est pas un carré parfait")
ok(cube_parfait(27) and not carre_parfait(27) and 25 < 27 < 36, "27 cube, pas carré")
ok(4 * 3 ** 2 - 5 == 31 and 4 * 9 == 36, "4 × 3² − 5 = 31")
ok((4 * 3) ** 2 - 5 == 139 and 12 ** 2 == 144, "(4 × 3)² − 5 = 139")
ok(2 + 3 * 2 ** 3 == 26 and 3 * 8 == 24, "2 + 3 × 2³ = 26")
ok((1 + 2) ** 2 == 9 and 1 ** 2 + 2 ** 2 == 5, "(1 + 2)² ≠ 1² + 2²")
ok((2 * x ** 2 - 5).subs(x, 4) == 27 and ((2 * x) ** 2 - 5).subs(x, 4) == 59, "2x² − 5 et (2x)² − 5 pour x = 4")
ok(expand((2 * x) ** 2) == 4 * x ** 2 and expand((2 * x) ** 2) != 2 * x ** 2, "(2x)² ≠ 2x²")
ok((x ** 3).subs(x, 2) == (4 * x).subs(x, 2) == 8, "x³ = 4x vraie pour 2")
ok((x ** 3).subs(x, 1) == 1 and (4 * x).subs(x, 1) == 4, "x³ = 4x fausse pour 1")
ok(sorted(solve(x ** 3 - 4 * x, x)) == [-2, 0, 2], "x³ = 4x : seules solutions −2, 0, 2")
ok(I(7) ** 2 == 49 and I(7) ** 3 == 343 and 7 * 7 * 7 == 343, "carré et cube de 7 cm")
ok(d("3,14") * 3 ** 2 == d("28,26") and abs(pi * 9 - d("28,26")) < 1, "aire du disque r = 3")
ok(10 ** 3 == 1000 and 10 * 10 * 10 == 1000, "1 dm³ = 1 000 cm³")
ok(10 ** 2 == 100 and 10 ** 3 == 1000, "1 m² = 100 dm² ; 1 m³ = 1 000 dm³")
ok((10 * 3) ** 2 == 100 * 3 ** 2 and (10 * 3) ** 3 == 1000 * 3 ** 3, "côté × 10 : aire × 100, volume × 1 000")

# ================================================================== FICHE
ok(36 < 40 < 49 and 4 * 3 ** 2 - 5 == 31 and (4 * 3) ** 2 - 5 == 139, "fiche : encadrement et priorités")
ok(I(3) ** 2 != 6 and I(4) ** 3 != 12 and I(4) ** 3 == 64, "fiche : erreurs 1")
ok(d("0,7") ** 2 == d("0,49") != d("1,4") and d("0,2") ** 3 == d("0,008"), "fiche : décimaux")
ok((1 + 2) ** 2 == 9 and 1 + 4 == 5 and 4 * 3 ** 2 != 12 ** 2, "fiche : erreurs 3 et 4")
ok((2 * 5) ** 2 == 4 * 5 ** 2 and (2 * 5) ** 3 == 8 * 5 ** 3, "fiche : côté doublé")

# ================================================================== 2831
ok([n * n for n in (1, 2, 3, 4)] == [1, 4, 9, 16], "carrés de 1 à 4")
ok(7 ** 2 == 49 and 10 ** 2 == 100, "côtés 7 et 10")
ok(3 * 3 == 9 and 9 * 3 == 27 == 3 ** 3, "cube d'arête 3")
ok(3 ** 3 - 2 ** 3 == 19, "19 petits cubes visibles (erreur fréquente)")
ok(1 ** 3 == 1 and 2 * 2 == 4 and 2 * 4 == 8 == 2 ** 3, "arêtes 1 et 2")
ok(10 * 10 == 100 and 10 * 100 == 1000 == 10 ** 3, "arête 10")
ok(4 ** 2 == 16 and 3 ** 3 == 27, "16 cm² et 27 cm³")

# ================================================================== 2833
ok(11 * 11 == I(11) ** 2 and d("2,3") * d("2,3") == d("2,3") ** 2 and d("0,4") ** 3 == d("0,064"), "écrire avec un exposant")
ok(9 ** 2 == 81 and 5 ** 3 == 125 and 25 * 5 == 125 and 10 ** 3 == 1000, "entiers")
ok(d("0,3") ** 2 == d("0,09") and 3 * 3 == 9 and d("0,3") ** 2 != d("0,9"), "0,3² = 0,09")
ok(d("1,2") ** 2 == d("1,44") and 12 * 12 == 144, "1,2² = 1,44")
ok(d("0,3") ** 2 < d("0,3"), "0,3² < 0,3")
ok(7 ** 2 == 49 and 2 * 7 == 14 and 3 ** 3 == 27 and 3 * 3 == 9, "carré/double, cube/triple")
ok(3 * 2 == 6 and 4 * 3 == 12 and 3 ** 2 == 9 and 4 ** 3 == 64 and 16 * 4 == 64, "erreur de Tom")
ok(len([(a, b, c) for a in range(10) for b in range(10) for c in range(10)]) == 1000 == 10 ** 3, "cadenas : 1 000 codes")
ok(len([(a, b) for a in range(10) for b in range(10)]) == 100, "cadenas : 100 débuts")

# ================================================================== 2835
ok([n ** 2 for n in range(1, 5)] == [1, 4, 9, 16], "étapes 1 à 4")
ok(5 ** 2 == 25 and 25 - 16 == 9 == 4 + 4 + 1, "étape 5 et points ajoutés")
ok(sum(1 for i in range(5) for j in range(5) if i == 4 or j == 4) == 9, "figure : 9 points verts")
ok([n ** 2 for n in range(6, 13)] == [36, 49, 64, 81, 100, 121, 144], "tableau 6 à 12")
ok(9 ** 2 == 81 and 11 ** 2 == 121, "étapes 9 et 11")
ok(7 ** 2 == 49 < 50 < 64 == 8 ** 2 and not carre_parfait(50), "50 n'est pas un carré")
ok(10 ** 2 == 100 and 2 * 5 ** 2 == 50 and 10 ** 2 == 4 * 5 ** 2, "erreur : étape 10")

# ================================================================== 2842
for n, a in [(25, 5), (49, 7), (100, 10), (144, 12)]:
    ok(a * a == n and carre_parfait(n), f"{n} = {a}²")
ok(25 < 30 < 36 and not carre_parfait(30) and 64 < 80 < 81 and not carre_parfait(80), "30 et 80")
ok(9 ** 2 == 81 and 3 ** 3 == 27 and 9 * 3 == 27 and 10 ** 3 == 1000 and d("0,5") ** 2 == d("0,25") and 5 ** 3 == 125, "compléter")
cubes = [n ** 3 for n in range(2, 6) if 2 <= n ** 3 <= 100]
ok(cubes == [8, 27, 64] and 5 ** 3 > 100, "cubes entre 2 et 100")
ok([c for c in cubes if carre_parfait(c)] == [64] and 4 < 8 < 9 and 25 < 27 < 36, "64 seul carré et cube")
ok(8 ** 2 == 64 == 4 ** 3, "64 = 8² = 4³")
ok(9 + 16 == 25 == 5 ** 2 and 4 + 9 == 13 and 9 < 13 < 16 and not carre_parfait(13), "Lina : contre-exemple")
vals = {"3^2": 9, "2^3": 8, "10^2": 100, "5^3": 125, "1^3": 1}
ok([k for k, v in sorted(vals.items(), key=lambda kv: kv[1])] == ["1^3", "2^3", "3^2", "10^2", "5^3"], "ordre croissant")
ok(10 > 5 and 10 ** 2 < 5 ** 3, "10² < 5³ malgré 10 > 5")

# ================================================================== 2838
A = 2 * 6 ** 2 - 9
B = (2 * 6) ** 2 - 9
ok(A == 63 and 2 * 36 == 72 and B == 135 and 12 ** 2 == 144, "A = 63 ; B = 135")
C, D, E = 2 + 4 ** 2, (2 + 4) ** 2, 2 ** 2 + 4 ** 2
ok((C, D, E) == (18, 36, 20), "C, D, E")
F = 10 ** 3 - 4 * 3 ** 3
G = 2 * 3 ** 2 + 5 * 2 ** 3
ok(F == 892 and 4 * 27 == 108 and G == 58 and 18 + 40 == 58, "F = 892 ; G = 58")
H = (7 - 2) ** 3 - 5 ** 2
ok(H == 100 and 125 - 25 == 100, "H = 100")
ok(D != E, "Sacha a tort")

# ================================================================== 2840
eA, eB = 5 * x ** 2 - 4, (5 * x) ** 2 - 4
ok(eA.subs(x, 2) == 16 and eB.subs(x, 2) == 96 and 5 * 4 - 4 == 16 and 10 ** 2 - 4 == 96, "A = 16 ; B = 96")
v = d("1,5")
ok(v ** 2 == d("2,25") and 15 * 15 == 225, "1,5² = 2,25")
ok(v ** 3 == d("3,375") and d("2,25") * v == d("3,375"), "1,5³ = 3,375")
ok((2 * x ** 2 + 3).subs(x, v) == d("7,5") and 2 * d("2,25") == d("4,5"), "2x² + 3 = 7,5")
ok([(x ** 2).subs(x, t) == (2 * x).subs(x, t) for t in (3, 2, 0)] == [False, True, True], "x² = 2x : tests")
ok(sorted(solve(x ** 2 - 2 * x, x)) == [0, 2], "x² = 2x seulement pour 0 et 2")
ok(d("3,14") * 5 ** 2 == d("78,5") and abs(pi * 25 - d("78,5")) < 1, "aire du disque r = 5")
ok(d("3,14") * 5 * 2 != d("78,5"), "erreur 3,14 × 5 × 2")

# ================================================================== 2845
cote, dalle = d("4,5"), d("0,5")
ok(cote / dalle == 9 and 9 * dalle == cote, "9 dalles par côté")
ok(9 ** 2 == 81, "81 dalles")
ok(cote ** 2 == d("20,25") and dalle ** 2 == d("0,25") and 81 * d("0,25") == d("20,25"), "aires")
ok(d("20,25") / d("0,25") == 81 and d("20,25") / d("0,5") == d("40,5"), "aire ÷ aire ; erreur aire ÷ longueur")
ok(4 * 20 == 80 < 81 <= 5 * 20 and 100 - 81 == 19, "5 boîtes ; 19 restantes")
ok(5 / dalle == 10 and 10 ** 2 == 100, "agrandissement : 100 dalles")
ok(I(5) ** 2 == 25 and 25 - d("20,25") == d("4,75"), "+4,75 m²")
ok(100 - 81 == 19 and 19 * d("0,25") == d("4,75"), "19 dalles suffisent tout juste")

# ================================================================== 2851
ok(30 / 5 == 6, "6 cubes par arête")
ok(6 ** 2 == 36 and 6 ** 3 == 216 and 36 * 6 == 216, "36 et 216")
ok(30 ** 3 == 27000 and 30 * 30 == 900 and 900 * 30 == 27000 and 27000 / 1000 == 27, "27 000 cm³ = 27 L")
ok(3 ** 3 == 27, "3 dm : 27 dm³")
ok(5 ** 3 == 125 and 216 * 125 == 27000, "contrôle du remplissage")
ok(216 - 36 == 180 == 5 * 36 and 180 * 125 == 22500 and R(22500, 1000) == d("22,5"), "180 cubes ; 22,5 L")
ok(6 * 3 == 18, "erreur 6 × 3")

# ================================================================== 2849
ok(3 ** 2 == 9 and 2 ** 3 == 8, "départ")
ok(6 ** 2 == 36 and 36 / 9 == 4 == 2 ** 2, "carré doublé : × 4")
ok(4 ** 3 == 64 and 16 * 4 == 64 and 64 / 8 == 8 == 2 ** 3, "cube doublé : × 8")
ok((3 * 3) ** 2 == 81 and 81 / 9 == 9 == 3 ** 2, "carré triplé : × 9")
ok((3 * 2) ** 3 == 216 and 216 / 8 == 27 == 3 ** 3, "cube triplé : × 27")
ok(12 ** 2 == 144 and 10 ** 3 == 1000, "côté 12 cm ; arête 10 cm")
ok((6 // 3) ** 2 == 4 and (4 // 2) ** 3 == 8, "figures : 4 carrés, 8 cubes")

# ================================================================== 2847
progA = lambda t: 3 * t ** 2 - 7
progB = lambda t: (3 * t) ** 2 - 7
ok(5 ** 2 == 25 and 25 * 3 == 75 and 75 - 7 == 68 == progA(5), "A(5) = 68")
ok(5 * 3 == 15 and 15 ** 2 == 225 and 225 - 7 == 218 == progB(5), "B(5) = 218")
t = d("2,5")
ok(t ** 2 == d("6,25") and d("6,25") * 3 == d("18,75") and progA(t) == d("11,75"), "A(2,5) = 11,75")
ok(t * 3 == d("7,5") and d("7,5") ** 2 == d("56,25") and progB(t) == d("49,25"), "B(2,5) = 49,25")
ok(progA(x) == 3 * x ** 2 - 7 and expand(progB(x)) == 9 * x ** 2 - 7, "expressions littérales")
ok(progA(0) == progB(0) == -7, "contre-exemple 0")
ok(solve(progA(x) - progB(x), x) == [0], "0 est le seul nombre commun")
ok(293 + 7 == 300 and 300 / 3 == 100 and 10 ** 2 == 100 and progA(10) == 293, "A : 293 depuis 10")
ok(893 + 7 == 900 and 30 ** 2 == 900 and 30 / 3 == 10 and progB(10) == 893, "B : 893 depuis 10")
ok([s for s in solve(progA(x) - 293, x) if s > 0] == [10] and [s for s in solve(progB(x) - 893, x) if s > 0] == [10], "solutions positives")
ok(100 / 2 == 50 and 50 ** 2 == 2500, "erreur : diviser par 2")

# ================================================================== contrôle des textes
TYPES = ("Découverte - ", "Entraînement - ", "Problème - ", "Synthèse - ")
ex = (ICI / "exercices.txt").read_text(encoding="utf-8")
titres = re.findall(r"^=== (.+)$", ex, re.M)
ok(len(titres) == 10 and len(set(titres)) == 10, "10 titres uniques")
ok(all(t.startswith(TYPES) for t in titres), "types de titres")
ok([t.split(" - ")[0] for t in titres] == ["Découverte"] * 3 + ["Entraînement"] * 3 + ["Problème"] * 3 + ["Synthèse"],
   "progression 3 / 3 / 3 / 1")
ok(all("Carrés et cubes" not in t for t in titres), "titres sans le nom du chapitre")
for nom in ("cours_262.txt", "fiche_182.txt", "exercices.txt"):
    txt = (ICI / nom).read_text(encoding="utf-8")
    ok("brevet" not in txt.lower(), f"pas de « brevet » dans {nom}")
    ok("\\sqrt" not in txt and "racine" not in txt.lower(), f"pas de racine carrée (4e) dans {nom}")
    ok("(-" not in txt.replace(" ", ""), f"pas de carré de relatif (4e) dans {nom}")
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
    ok("::: attention" in bloc or "::: retenir" in bloc, f"{tid} : erreur fréquente ou à retenir")
    ok(bloc.count("::: resultat") >= len(re.findall(r"^## Question", bloc, re.M)), f"{tid} : un résultat par question")
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
for nom, cle, idd in (("cours_262.txt", "cours", "262"), ("fiche_182.txt", "fiches", "182")):
    appels = sorted(set(re.findall(r"\[IMAGE_(\d+)\]", (ICI / nom).read_text(encoding="utf-8"))))
    ok(appels == sorted(corr[cle][idd].keys()), f"{nom} : images")
for cle in corr:
    for idd in corr[cle]:
        for pos, e in corr[cle][idd].items():
            ok((images / e["fichier"]).exists() and len(e["alt"]) >= 15, f"{cle} {idd} {pos} : fichier et alt")

print(f"verif_267 : {n_ok} contrôles, tous justes.")
