# -*- coding: utf-8 -*-
"""Vérification des calculs de la notion 270 (5e : inconnues et équations simples).

Cours, fiche, 10 exercices et figures : chaque équation est résolue avec sympy
(solve en nombres exacts), chaque vérification et chaque calcul intermédiaire
est recalculé. Contrôles de structure : 10 exercices, progression 3/3/3/1,
aucune mention du brevet, 10 gardés + 11 retirés = 21 Id en ligne, figures
appelées = figures déclarées, valeurs des figures = valeurs du texte.
Lancer : python verif_270.py
"""
import json
import re
from pathlib import Path

from sympy import Rational as R, Integer as I, symbols, solve, Eq, floor

ICI = Path(__file__).resolve().parent
n_ok = 0
x, n, t, m, d, l, p, s, e, r = symbols("x n t m d l p s e r")


def ok(cond, msg):
    global n_ok
    assert cond, msg
    n_ok += 1


def D(c):
    """Décimal écrit à la française -> rationnel exact : '2,25' -> 9/4."""
    return R(str(c).replace(",", ".").replace(" ", ""))


def sol(eq, var=x):
    """Solution unique d'une équation du premier degré."""
    s_ = solve(eq, var)
    assert len(s_) == 1, (eq, s_)
    return s_[0]


def est_solution(gauche, droite, val, var=x):
    return gauche.subs(var, val) == droite.subs(var, val)


# ================================================================== COURS
ok(sol(Eq(x + 8, 20)) == 12, "je pense à un nombre : x + 8 = 20")
ok(est_solution(5 * x - 3, 2 * x + 9, 4) and 5 * 4 - 3 == 17 and 2 * 4 + 9 == 17, "4 solution de 5x − 3 = 2x + 9")
ok(not est_solution(5 * x - 3, 2 * x + 9, 2) and 5 * 2 - 3 == 7 and 2 * 2 + 9 == 13, "2 non solution")
ok(sol(Eq(5 * x - 3, 2 * x + 9)) == 4, "4 est la seule solution (contrôle)")
ok(5 * 4 == 20, "5x pour x = 4 vaut 20")
ok(sol(Eq(x + 5, 12)) == 7 and 7 + 5 == 12, "x + 5 = 12")
ok(sol(Eq(x + D("3,6"), 10)) == D("6,4"), "x + 3,6 = 10")
ok(sol(Eq(x + 9, 4)) == -5 and -5 + 9 == 4, "x + 9 = 4")
ok(sol(Eq(x + R(1, 3), 1)) == R(2, 3) and R(3, 3) - R(1, 3) == R(2, 3), "x + 1/3 = 1")
ok(sol(Eq(x - 6, 11)) == 17, "x − 6 = 11")
ok(sol(Eq(3 * x, 12)) == 4, "3x = 12")
ok(sol(Eq(4 * x, 7)) == D("1,75") and 4 * D("1,75") == 7, "4x = 7")
ok(sol(Eq(D("0,5") * x, 4)) == 8 and D("0,5") * 8 == 4, "0,5x = 4")
ok(sol(Eq(3 * x, 2)) == R(2, 3) and 3 * R(2, 3) == 2, "3x = 2")
ok(sol(Eq(x / 3, 1)) == 3, "x/3 = 1")
ok(sol(Eq(x / 4, D("2,5"))) == 10 and R(10, 4) == D("2,5"), "x/4 = 2,5")
ok(sol(Eq(2 * x, 0)) == 0 and sol(Eq(x / 2, 0)) == 0, "2x = 0 et x/2 = 0")
ok(12 + 5 == 17 and 17 + 5 == 22, "erreur : ajouter au lieu de soustraire")
ok(12 - 3 == 9 and 3 * 9 == 27, "erreur : soustraire au lieu de diviser")
ok(R(3, 2) != R(2, 3), "erreur : quotient inversé")
ok(sol(Eq(x + D("12,50"), 40)) == D("27,50"), "prix du livre")
ok(sol(Eq(7 * n, 168), n) == 24 and 7 * 24 == 168, "étagères")
ok(sol(Eq(3 * x + 2, 11)) == 3 and 11 - 2 == 9 and 9 / I(3) == 3, "cahiers et règle")
ok(3 * 2 + 2 == 8 and 3 * 3 + 2 == 11, "cahiers : essais")

# ================================================================== FICHE
ok(sol(Eq(x + 8, 20)) == 12 and sol(Eq(3 * n, 21), n) == 7, "fiche : exemples d'équations")
ok(sol(Eq(x + 9, 4)) == -5 and sol(Eq(4 * x, 7)) == D("1,75") and sol(Eq(3 * x, 2)) == R(2, 3), "fiche : exemples")
ok(sol(Eq(x / 3, 1)) == 3, "fiche : x/3 = 1")
ok(sol(Eq(x + 5, 12)) == 7 and sol(Eq(3 * x, 12)) == 4, "fiche : erreurs 1 et 2")

# ================================================================== 2897 tester
ok(est_solution(x + 9, I(15), 6) and not est_solution(x + 9, I(15), 24) and 24 + 9 == 33, "2897 q1")
ok([k for k in (3, 4, 5) if 7 * k == 28] == [4] and (7 * 3, 7 * 5) == (21, 35), "2897 q2")
ok(est_solution(4 * x - 1, I(9), D("2,5")) and 4 * D("2,5") == 10, "2897 q3")
ok((3 * 2 + 4, 5 * 2 - 2) == (10, 8) and (3 * 3 + 4, 5 * 3 - 2) == (13, 13), "2897 q4")
ok(sol(Eq(3 * x + 4, 5 * x - 2)) == 3, "2897 q4 : 3 est bien la solution (contrôle)")
ok(est_solution(6 * x, I(0), 0) and not est_solution(x + 6, I(0), 0) and sol(Eq(x + 6, 0)) == -6, "2897 q5")
ok(7 * 4 == 28, "2897 erreur 7x = 74")

# ================================================================== 2896 additions et balances
ok(sol(Eq(x + 8, 23)) == 15 and 15 + 8 == 23, "2896 balance A")
ok(sol(Eq(x + D("4,5"), 12)) == D("7,5"), "2896 balance B")
ok(sol(Eq(x + 13, 41)) == 28 and sol(Eq(x + D("0,7"), 2)) == D("1,3") and sol(Eq(27 + x, 50)) == 23, "2896 q3")
ok(sol(Eq(x + 11, 4)) == -7, "2896 q4")
ok(sol(Eq(x - 8, 15)) == 23, "2896 q5")
ok(41 + 13 == 54 and 54 + 13 == 67, "2896 erreur fréquente")

# ================================================================== 2898 multiplications et divisions
ok(sol(Eq(4 * x, 18)) == D("4,5"), "2898 balance")
ok(sol(Eq(6 * x, 42)) == 7 and sol(Eq(5 * x, 13)) == D("2,6") and sol(Eq(8 * x, 6)) == D("0,75"), "2898 q2 a-c")
ok(sol(Eq(7 * x, 3)) == R(3, 7) and 7 * R(3, 7) == 3, "2898 q2 d")
ok(sol(Eq(x / 6, 1)) == 6 and sol(Eq(x / 5, D("2,4"))) == 12 and sol(Eq(x / 10, D("0,7"))) == 7, "2898 q3")
ok(sol(Eq(9 * x, 0)) == 0 and sol(Eq(x / 7, 0)) == 0, "2898 q4")
ok(12 - 3 == 9 and 3 * 9 == 27 and sol(Eq(3 * x, 12)) == 4, "2898 q5 Tom")

# ================================================================== 2903 décimaux, relatifs, fractions
ok(sol(Eq(x + D("2,75"), 5)) == D("2,25"), "2903 1a")
ok(sol(Eq(x + D("1,8"), D("0,5"))) == D("-1,3"), "2903 1b")
ok(sol(Eq(x + 7, -3)) == -10, "2903 1c")
ok(sol(Eq(x - D("4,5"), -1)) == D("3,5"), "2903 1d")
ok(sol(Eq(D("2,5") * x, 10)) == 4 and R(100, 25) == 4, "2903 2a")
ok(sol(Eq(D("0,4") * x, 3)) == D("7,5") and R(30, 4) == D("7,5"), "2903 2b")
ok(sol(Eq(D("1,2") * x, D("0,6"))) == D("0,5") and R(6, 12) == D("0,5"), "2903 2c")
ok(sol(Eq(x + R(2, 5), 1)) == R(3, 5), "2903 3a")
ok(sol(Eq(x + R(1, 4), R(5, 6))) == R(7, 12) and R(10, 12) == R(5, 6) and R(3, 12) == R(1, 4), "2903 3b")
ok(sol(Eq(3 * x, 7)) == R(7, 3), "2903 3c")
ok(2 < R(7, 3) < 3 and floor(R(7, 3) * 100) == 233 and abs(R(7, 3) - D("2,33")) < D("0,005"), "2903 q4")
ok(D("1,8") - D("0,5") == D("1,3") and 3 * D("0,4") == D("1,2") and D("0,4") * D("1,2") == D("0,48"), "2903 erreurs")

# ================================================================== 2901 mettre en équation
ok(sol(Eq(D("7,8") + d, D("12,5")), d) == D("4,7"), "2901 randonnée")
ok(sol(Eq(8 * l, 18), l) == D("2,25"), "2901 ruban")
ok(sol(Eq(5 * p, D("7,50")), p) == D("1,50"), "2901 stylos")
ok(sol(Eq(t + 9, 4), t) == -5, "2901 température")
ok(sol(Eq(s / 4, D("12,50")), s) == 50 and sol(Eq(4 * s, D("12,50")), s) != 50, "2901 partage")

# ================================================================== 2908 vérifier et corriger
ok(56 + 15 == 71 and sol(Eq(x + 15, 41)) == 26, "2908 Ana")
ok(sol(Eq(6 * x, 33)) == D("5,5") and 33 % 6 != 0, "2908 Bilal")
ok(R(5, 3) > 1 and 5 * R(5, 3) > 5 and sol(Eq(5 * x, 3)) == R(3, 5) == D("0,6"), "2908 Chloé")
ok(D("0,75") / 4 == D("0,1875") and sol(Eq(x / 4, 3)) == 12, "2908 Dylan")
ok(sol(Eq(x + 7, 5)) == -2, "2908 Emma")
ok(D("1,5") - D("2,5") == -1 and sol(Eq(x - D("2,5"), 4)) == D("6,5"), "2908 Farid")

# ================================================================== 2914 flacons
ok(sol(Eq(m + D("1,2"), D("4,8")), m) == D("3,6"), "2914 q1")
ok(sol(Eq(8 * x, D("3,6"))) == D("0,45"), "2914 q2")
ok(D("0,45") * 1000 == 450 and 450 + 50 == 500, "2914 q3 q4")
ok(10 * D("0,45") == D("4,5") and D("4,5") - D("3,6") == D("0,9") and D("3,6") < D("4,5"), "2914 q5")

# ================================================================== 2904 billes et ruban
ok(sol(Eq(t + 3 * t, 64), t) == 16 and 3 * 16 == 48 and 16 + 48 == 64, "2904 billes")
ok(D("2,4") - D("0,6") == D("1,8") and sol(Eq(2 * x + D("0,6"), D("2,4"))) == D("0,9"), "2904 ruban")
ok(D("0,9") + D("0,6") == D("1,5") and D("0,9") + D("1,5") == D("2,4") and D("1,5") - D("0,9") == D("0,6"), "2904 vérif ruban")
ok(D("2,4") / 2 == D("1,2"), "2904 erreur moitiés")

# ================================================================== 2900 programmes
ok(sol(Eq(6 * x, 45)) == D("7,5"), "2900 q1")
ok(sol(Eq(x + D("2,5"), 1)) == D("-1,5"), "2900 q2")
C = lambda v: 4 * v + 7
ok(C(5) == 27 and [C(k) for k in (8, 9, 10)] == [39, 43, 47], "2900 q3 a b")
ok(sol(Eq(C(x), 43)) == 9 and 43 - 7 == 36 and 36 / I(4) == 9, "2900 q3 c")
ok(sol(Eq(C(x), 9)) == D("0,5") and C(D("0,5")) == 9 and C(0) == 7 and C(1) == 11, "2900 q4")
ok(sol(Eq(C(x), 7)) == 0, "2900 q5")
ok(D("43") / 4 == D("10,75") and D("10,75") - 7 == D("3,75") and C(D("3,75")) == 22, "2900 erreur ordre")

# ================================================================== 2902 synthèse
ok(sol(Eq(18 * n, 540), n) == 30, "2902 q1")
ok(15 * 36 == 540 and sol(Eq(15 * n, 540), n) == 36, "2902 q2")
ok(sol(Eq(30 * e, 165), e) == D("5,5"), "2902 q3")
ok(18 + D("5,5") == D("23,5") and sol(Eq(r + 20, D("23,5")), r) == D("3,5"), "2902 q4")
ok(2 * 30 == 60 and sol(Eq(8 * p, 60), p) == D("7,5") and 7 * 8 == 56 and 8 * 8 == 64 and 64 - 60 == 4, "2902 q5")

# ================================================================== figures : valeurs écrites = valeurs du texte
fig = (ICI / "figures" / "figures.py").read_text(encoding="utf-8")
for frag in ('(1, "5"), (0, "12")', '(0, "7")', '(3, None), (0, "12")', '(0, "4")',
             '(1, "8"), (0, "23")', '(0, "15")', '(1, "4{,}5"), (0, "12")', '(0, "7{,}5")',
             '(4, None), (0, "18")', '(0, "4{,}5")',
             r'$12{,}50$ €', r'$40$ €', r'$168$ livres', r'$11$ €', r'$11 - 2 = 9$ €, puis $9 \div 3 = 3$ €',
             r'$7{,}8$ km', r'$12{,}5$ km', r'$12{,}5 - 7{,}8 = 4{,}7$ km', r'$18$ m', r'$\ell = 18 \div 8 = 2{,}25$ m',
             r'$1{,}2$ kg', r'$4{,}8$ kg', r'$m = 4{,}8 - 1{,}2 = 3{,}6$ kg', r'$0{,}45$', r'$x = 3{,}6 \div 8 = 0{,}45$ kg',
             r'$64$ billes', r'$3 \times 16 = 48$', r'$4t = 64$, donc $t = 64 \div 4 = 16$',
             r'$2{,}4$ m', r'$0{,}6$', r'$2{,}4 - 0{,}6 = 1{,}8$ m', r'$x = 1{,}8 \div 2 = 0{,}9$ m', r'$0{,}9 + 0{,}6 = 1{,}5$ m', r'$16$ billes',
             r'$\times 4$', r'$+ 7$', r'$\div 4$', r'$- 7$', r'$43$', r'$36$', r'$9$'):
    ok(frag in fig, f"figure : « {frag} » présent")
ok(4 * 9 == 36 and 36 + 7 == 43, "figure programme : 9 → 36 → 43")
ok(8 * D("2,25") == 18 and 8 * D("0,45") == D("3,6") and 4 * 16 == 64, "figures : cases vertes")

# ================================================================== contrôle des textes
TYPES = ("Découverte - ", "Entraînement - ", "Problème - ", "Synthèse - ")
ex = (ICI / "exercices.txt").read_text(encoding="utf-8")
titres = re.findall(r"^=== (.+)$", ex, re.M)
ok(len(titres) == 10 and len(set(titres)) == 10, "10 titres uniques")
ok(all(t_.startswith(TYPES) for t_ in titres), "types de titres")
ok([t_.split(" - ")[0] for t_ in titres] == ["Découverte"] * 3 + ["Entraînement"] * 3 + ["Problème"] * 3 + ["Synthèse"],
   "progression 3 / 3 / 3 / 1")
ok(all("Inconnues" not in t_ and "équations simples" not in t_ for t_ in titres), "titres sans le nom du chapitre")
for nom in ("cours_265.txt", "fiche_185.txt", "exercices.txt"):
    txt = (ICI / nom).read_text(encoding="utf-8")
    ok("brevet" not in txt.lower(), f"pas de « brevet » dans {nom}")
    ok("\\sqrt" not in txt and "racine" not in txt.lower(), f"pas de racine carrée (4e) dans {nom}")
    ok(not re.search(r"x\^2|x²", txt), f"pas d'équation du second degré dans {nom}")
ids = [int(k) for k in re.findall(r"^Id:\s*(\d+)", ex, re.M)]
retires = [int(k) for k in re.findall(r"^(\d+)", (ICI / "exercices_retires.txt").read_text(encoding="utf-8"), re.M)]
src = (ICI / "source_en_ligne" / "exercices.txt").read_text(encoding="utf-8")
ids_src = [int(k) for k in re.findall(r"^Id:\s*(\d+)", src, re.M)]
ok(len(ids) == 10 and len(retires) == 11 and not set(ids) & set(retires), "10 gardés, 11 retirés, disjoints")
ok(sorted(ids + retires) == sorted(ids_src) and len(ids_src) == 21, "gardés + retirés = les 21 Id en ligne")
for bloc in ex.split("\n===\n"):
    if not bloc.strip():
        continue
    tid = re.search(r"^Id:\s*(\d+)", bloc, re.M).group(1)
    ok("::: attention" in bloc or "::: retenir" in bloc, f"{tid} : erreur fréquente ou à retenir")
    ok(bloc.count("::: resultat") >= len(re.findall(r"^## Question", bloc, re.M)), f"{tid} : un résultat par question")
    ok("Solution:" in bloc and "Étapes:" in bloc and "Énoncé:" in bloc, f"{tid} : rubriques")
    nq_enonce = len(re.findall(r"^\d+\. ", bloc.split("Étapes:")[0], re.M))
    nq_etapes = len(re.findall(r"^## Question", bloc, re.M))
    nq_sol = len(re.findall(r"^\d+\. ", bloc.split("Solution:")[1], re.M))
    ok(nq_enonce == nq_etapes == nq_sol, f"{tid} : {nq_enonce} questions = {nq_etapes} étapes = {nq_sol} solutions")

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
for nom, cle, idd in (("cours_265.txt", "cours", "265"), ("fiche_185.txt", "fiches", "185")):
    appels = sorted(set(re.findall(r"\[IMAGE_(\d+)\]", (ICI / nom).read_text(encoding="utf-8"))))
    ok(appels == sorted(corr[cle][idd].keys()), f"{nom} : images")
for cle in corr:
    for idd in corr[cle]:
        for pos, e_ in corr[cle][idd].items():
            ok((images / e_["fichier"]).exists() and len(e_["alt"]) >= 15, f"{cle} {idd} {pos} : fichier et alt")

print(f"verif_270 : {n_ok} contrôles, tous justes.")
