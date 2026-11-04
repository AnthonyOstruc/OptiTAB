# -*- coding: utf-8 -*-
"""Vérification mathématique de la notion 278 (5e : organiser et interpréter des données).

    python verif_278.py

1. Contrôles explicites (sympy, valeurs exactes) de chaque réponse du cours, de la
   fiche et des exercices ; les données des figures (figures/figures.py, DONNEES)
   sont confrontées aux énoncés : dépouillements recomptés à partir des relevés
   bruts, angles, fréquences, moyennes, lectures.
2. Contrôle automatique : toute égalité purement numérique écrite entre $…$ dans
   les trois fichiers (fractions, pourcentages, degrés, chaînes « a = b = c ») est
   recalculée exactement.
3. Structure : 10 exercices, progression 3-3-2-2, une méthode et un résultat par
   question, erreur fréquente, solution complète, Id gardés / retirés (3062 à 3082),
   aucune mention du brevet ; pas de médiane ni de moyenne pondérée (programme de 4e).
"""
import importlib.util
import re
import sys
from collections import Counter
from pathlib import Path

import sympy as sp

ICI = Path(__file__).resolve().parent
ok, ko = 0, []
R = sp.Rational


def check(cond, msg):
    global ok
    if cond:
        ok += 1
    else:
        ko.append(msg)


def d(s):
    return sp.nsimplify(s.replace(",", "."), rational=True)


def pct(n, tot):
    return R(n, tot) * 100


spec = importlib.util.spec_from_file_location("fig278", ICI / "figures" / "figures.py")
FIG = importlib.util.module_from_spec(spec)
spec.loader.exec_module(FIG)
D = FIG.DONNEES
COURS = (ICI / "cours_273.txt").read_text(encoding="utf-8")
FICHE = (ICI / "fiche_193.txt").read_text(encoding="utf-8")
EX = (ICI / "exercices.txt").read_text(encoding="utf-8")


def bloc(eid):
    for b in re.split(r"^===[ \t]*$", EX, flags=re.M):
        if re.search(r"^Id: %s\s*$" % eid, b, re.M):
            return b
    raise KeyError(eid)


def contient(eid, *morceaux):
    b = bloc(eid)
    for m in morceaux:
        check(m in b, f"{eid} : texte attendu absent « {m} »")


# ===================================================================== cours
BO = dict(D["cours_boissons"])
check(BO == {"Jus de fruits": 8, "Eau": 5, "Chocolat chaud": 4, "Lait": 3}, "cours : données des boissons")
tot = sum(BO.values())
check(tot == 20, "cours : 20 élèves")
check([pct(e, tot) for e in BO.values()] == [40, 25, 20, 15], "cours : fréquences 40/25/20/15 %")
check([R(e, tot) for e in BO.values()] == [d("0,4"), d("0,25"), d("0,2"), d("0,15")], "cours : fréquences décimales")
check(sum(R(e, tot) for e in BO.values()) == 1, "cours : somme des fréquences = 1")
check(R(360, tot) == 18 and [e * 18 for e in BO.values()] == [144, 90, 72, 54], "cours : angles 144/90/72/54")
check([R(e, tot) * 180 for e in BO.values()] == [72, 45, 36, 27], "cours : angles semi-circulaires")
check(R(8, 20) == R(2, 5) == d("0,4") == R(40, 100), "cours : 8/20 = 40 %")
check(R(3, 20) == R(15, 100) and R(3) / 20 == d("0,15"), "cours : 3/20 = 15 %")
check(R(6, 20) == R(30, 100) and R(7, 28) == R(25, 100) and R(6, 20) > R(7, 28) and 6 < 7, "cours : 6/20 > 7/28")
BV, BE = D["cours_buts"]
check(BV == [0, 1, 2, 3, 4] and BE == [4, 7, 5, 3, 1] and sum(BE) == 20, "cours : buts sur 20 matchs")
check(BE[2] == 5 and BE[3] + BE[4] == 4 and R(4, 20) == R(20, 100), "cours : lectures du diagramme en bâtons")
JX, JY = D["cours_judo"]
check(dict(zip(JX, JY))[2023] == 50 and JY[1] < JY[0] and all(JY[i + 1] > JY[i] for i in range(1, 5)),
      "cours : judo, baisse puis hausse")
hausses = [JY[i + 1] - JY[i] for i in range(5)]
check(max(hausses) == 15 and hausses.index(15) == 2 and 50 - 35 == 15, "cours : plus forte hausse 2022-2023")
colis = [d("2,5"), 3, d("1,5"), 4]
check(sum(colis) == 11 and R(11, 4) == d("2,75") and d("2,75") not in colis, "cours : masse moyenne des colis")
check(min(colis) <= d("2,75") <= max(colis) and 4 * d("2,75") == 11, "cours : interprétation de la moyenne")
check(13 * 3 == 39, "cours : Hugo 39 points")
check(R(10 + 10 + 16, 3) == 12 and R(10 + 16, 2) == 13, "cours : erreur valeur répétée")
contient_cours = ["=SOMME(B2:B5)", "=B2/B6", "=MOYENNE(B2:B6)", "=SOMME(B2:B6)/5"]
for m in contient_cours:
    check(m in COURS, f"cours : formule {m}")
check(BO["Jus de fruits"] / R(tot) == d("0,4"), "figure cours_tableur : C2 = 0,4")
check("1858" in COURS and "Nightingale" in COURS, "cours : prolongement historique (programme)")

# ===================================================================== fiche
check(R(8, 20) == R(2, 5) and 8 * 18 == 144 and 13 * 3 == 39, "fiche : exemples")

# ===================================================================== 3062 : dépouillement des fruits
brut = " ".join(D["3062_brut"]).split()
cpt = Counter(brut)
check(len(brut) == 24, "3062 : 24 réponses")
noms = {"F": "Fraise", "P": "Pomme", "B": "Banane", "O": "Orange"}
check({noms[k]: v for k, v in cpt.items()} == dict(D["3062"]), "3062 : dépouillement = tableau de la figure")
check(dict(D["3062"]) == {"Fraise": 9, "Pomme": 6, "Banane": 5, "Orange": 4}, "3062 : effectifs 9/6/5/4")
for ligne in D["3062_brut"]:
    check(", ".join(ligne.split()) in bloc(3062), f"3062 : relevé « {ligne} » dans l'énoncé")
par_ligne = {k: [Counter(l.split())[k] for l in D["3062_brut"]] for k in "FPBO"}
check(par_ligne == {"F": [3, 2, 2, 2], "P": [1, 2, 1, 2], "B": [1, 1, 2, 1], "O": [1, 1, 1, 1]},
      "3062 : comptages ligne par ligne du corrigé")
check(24 - 9 == 15 == 6 + 5 + 4 and R(24, 3) == 8 and 9 > 8, "3062 : questions 3 et 4")

# ===================================================================== 3071 : fréquences
AC = dict(D["3071"])
check(AC == {"Sport": 14, "Musique": 6, "Lecture": 8, "Écrans": 12} and sum(AC.values()) == 40, "3071 : données")
check(R(14, 40) == R(7, 20) == R(35, 100), "3071 : sport 35 %")
check([pct(e, 40) for e in AC.values()] == [35, 15, 30 - 10, 30], "3071 : fréquences")
check(sum(pct(e, 40) for e in AC.values()) == 100, "3071 : somme 100 %")
check(R(6 + 8, 40) == R(35, 100), "3071 : activités culturelles 35 %")
check(25 * R(40, 100) == 10 and 14 > 10 and R(40, 100) > R(35, 100), "3071 : 5e C")
check(sum(e * 100 // 40 for e in AC.values()) == 100, "figure 3071 : barre à 100 %")

# ===================================================================== 3066 : bibliothèque
J, E = D["3066"]
check(E == [12, 18, 15, 9, 6] and all(e % 3 == 0 for e in E), "3066 : valeurs sur les lignes de la graduation")
check(max(E) == 18 and J[E.index(18)] == "Mar" and min(E) == 6 and J[E.index(6)] == "Ven" and 18 - 6 == 12,
      "3066 : extrêmes")
check(sum(E) == 60 and R(15, 60) == R(1, 4) == d("0,25"), "3066 : total et fréquence du mercredi")
check(E[0] + E[1] == 30 == R(sum(E), 2), "3066 : lundi + mardi = exactement la moitié")

# ===================================================================== 3063 : animaux
AV, AE = D["3063"]
check(AV == [0, 1, 2, 3, 4] and AE == [7, 10, 5, 2, 1] and sum(AE) == 25, "3063 : données")
check(sum(AE[2:]) == 8 and pct(8, 25) == 32, "3063 : au moins 2 animaux")
check(pct(7, 25) == 28, "3063 : aucun animal")
check(AE[0] + AE[1] == 17 and pct(17, 25) == 68 and R(25, 2) == d("12,5") and 17 > d("12,5"), "3063 : au plus un")
for v, e in zip(AV, AE):
    check(f"| ${v}$ | ${e}$ |" in bloc(3063), f"3063 : ligne {v} du tableau")

# ===================================================================== 3073 : transports
TR = dict(D["3073"])
check(TR == {"À pied": 10, "Vélo": 18, "Bus": 12} and sum(TR.values()) == 40, "3073 : données")
check([pct(e, 40) for e in TR.values()] == [25, 45, 30], "3073 : fréquences")
check(R(360, 40) == 9 and [9 * e for e in TR.values()] == [90, 162, 108] and 90 + 162 + 108 == 360, "3073 : angles")
check(R(360, 4) == 90, "3073 : quart de disque")
check(R(180, 40) == d("4,5") and [d("4,5") * e for e in TR.values()] == [45, 81, 54] and 45 + 81 + 54 == 180,
      "3073 : angles semi-circulaires")

# ===================================================================== 3072 : moyenne
NY, NI = D["3072"]
check(NY == [12, 9, 15, 10, 14] and NI == [12, 11, 13, 12, 12], "3072 : données")
check(sum(NY) == 60 and R(60, 5) == 12, "3072 : moyenne de Yanis")
check(NY[0] == 12 and [n for n in NY if n > 12] == [15, 14] and [n for n in NY if n < 12] == [9, 10], "3072 : Q2")
check(R(sum(NI), 5) == 12 and max(NY) - min(NY) == 6 and max(NI) - min(NI) == 2, "3072 : Inès et écarts")
check(13 * 6 == 78 and 78 - 60 == 18 and R(60 + 18, 6) == 13 and 18 <= 20, "3072 : note à obtenir")
contient(3072, "=MOYENNE(B2:F2)", "=SOMME(B2:F2)/5")
for i, n in enumerate(NY, 1):
    check(f"| C{i} | ${n}$ |" in bloc(3072), f"3072 : note C{i}")

# ===================================================================== 3075 : piscine
PM, PE = D["3075"]
check(PE == [800, 1000, 1000, 1400, 2000, 2800] and all(v % 200 == 0 for v in PE), "3075 : valeurs sur la grille")
check(PE[2] == 1000 and PE[5] == 2800, "3075 : lectures mars et juin")
var = [PE[i + 1] - PE[i] for i in range(5)]
check(var == [200, 0, 400, 600, 800] and max(var) == 800 and var.index(800) == 4, "3075 : variations")
moy = R(sum(PE), 6)
check(sum(PE) == 9000 and moy == 1500, "3075 : moyenne 1 500")
check([m for m, v in zip(PM, PE) if v > moy] == ["mai", "juin"], "3075 : mois au-dessus de la moyenne")
check(3 * 800 == 2400 and 2800 > 2400 and R(2800, 800) == d("3,5"), "3075 : plus de trois fois plus")

# ===================================================================== 3065 : tableur
GJ, GV = D["3065"]
check(GV == [18, 24, 12, 30, 36] and sum(GV) == 120, "3065 : ventes et total")
check(R(18, 120) == R(3, 20) == d("0,15"), "3065 : B3 = 0,15")
check([pct(v, 120) for v in GV] == [15, 20, 10, 25, 30] and sum(pct(v, 120) for v in GV) == 100, "3065 : fréquences")
check(R(120, 5) == 24 and [j for j, v in zip(GJ, GV) if v > 24] == ["Jeu", "Ven"] and GV[1] == 24,
      "3065 : moyenne et jours au-dessus")
check(R(30, 120) == R(1, 4), "3065 : le jeudi = un quart du disque")
contient(3065, "=SOMME(B2:B6)", "=B2/B7", "=B3/B7", "=MOYENNE(B2:B6)", "=B7/5", "=B3/B8")
check("G2" not in bloc(3065) and "F2" not in bloc(3065), "3065 : plus aucune référence à l'ancienne feuille en ligne")

# ===================================================================== 3064 : vote
brut = " ".join(D["3064_brut"]).split()
cpt = Counter(brut)
noms = {"P": "Parc", "Z": "Zoo", "M": "Musée", "C": "Cinéma"}
check(len(brut) == 30 and {noms[k]: v for k, v in cpt.items()} == dict(D["3064"]), "3064 : dépouillement")
for ligne in D["3064_brut"]:
    check(", ".join(ligne.split()) in bloc(3064), f"3064 : bulletins « {ligne} » dans l'énoncé")
par_ligne = {k: [Counter(l.split())[k] for l in D["3064_brut"]] for k in "PZMC"}
check(par_ligne == {"P": [3, 2, 3, 2, 2], "Z": [1, 3, 1, 2, 2], "M": [1, 1, 1, 2, 1], "C": [1, 0, 1, 0, 1]},
      "3064 : comptages ligne par ligne du corrigé")
SA = dict(D["3064"])
check([pct(e, 30) for e in SA.values()] == [40, 30, 20, 10], "3064 : fréquences 5e A")
check(SA["Parc"] == 12 < R(30, 2) == 15, "3064 : pas de majorité")
check(R(360, 30) == 12 and [12 * e for e in SA.values()] == [144, 108, 72, 36] and 144 + 108 + 72 + 36 == 360,
      "3064 : angles")
SB = dict(D["3064_B"])
check(SB == {"Parc": 11, "Zoo": 6, "Musée": 5, "Cinéma": 3} and sum(SB.values()) == 25, "3064 : 5e B")
check([pct(e, 25) for e in SB.values()] == [44, 24, 20, 12], "3064 : fréquences 5e B")
check(12 > 11 and pct(11, 25) > pct(12, 30), "3064 : le parc plus populaire en 5e B")
contient(3064, "$11$ pour le parc, $6$ pour le zoo, $5$ pour le musée et $3$ pour le cinéma")

# ===================================================================== 3082 : cantine
CJ, CR = D["3082"]
check(CR == [280, 300, 290, 330], "3082 : valeurs")
check(330 - 280 == 50 and 6 * 280 == 1680 and 2 * 280 == 560 and 330 < 560, "3082 : le titre est faux")
check(280 - 270 == 10 and 330 - 270 == 60 and R(60, 10) == 6, "3082 : barres vues à partir de 270")
check(sum(CR) == 1200 and R(1200, 4) == 300, "3082 : moyenne 300")
check(R(330, 1200) == d("0,275") and R(330, 1200) * 100 == d("27,5"), "3082 : 27,5 %")
check(max(CR) <= 350, "3082 : axe honnête jusqu'à 350")

# ===================================================================== contrôle automatique des égalités numériques


def frac(s):
    while True:
        n = re.sub(r"\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
        if n == s:
            return s
        s = n


def tex_vers_py(s):
    s = s.replace("{,}", ".").replace(r"\times", "*").replace(r"\div", "/")
    s = s.replace(r"\,\%", "/100").replace(r"\%", "/100").replace(r"^\circ", "")
    s = s.replace(r"\left", "").replace(r"\right", "").replace(r"\,", "").replace(r"\quad", " ")
    s = frac(s)
    s = re.sub(r"\\text\{[^}]*\}", " ", s)
    return s.strip()


NUM = re.compile(r"^[\d.\s+\-*/()]+$")


def valeur(expr):
    try:
        v = sp.sympify(expr, rational=True)
        return v if v.is_Rational else None
    except Exception:
        return None


def egalites(texte, ou):
    global ok
    vus = 0
    blocs = re.findall(r"\$\$(.+?)\$\$", texte, re.S) + re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", texte)
    for m in blocs:
        for ligne in re.split(r"\\\\|\\qquad", m):
            ligne = ligne.replace("&", "")
            ligne = re.sub(r"\\begin\{aligned\}|\\end\{aligned\}", "", ligne)
            membres = [tex_vers_py(x) for x in ligne.split("=")]
            membres = [x for x in membres if x]
            if len(membres) < 2 or not all(NUM.match(x) for x in membres):
                continue
            vals = [valeur(x) for x in membres]
            if any(v is None for v in vals):
                ko.append(f"{ou} : « {ligne.strip()} » illisible")
                continue
            vus += 1
            if all(v == vals[0] for v in vals):
                ok += 1
            else:
                ko.append(f"{ou} : « {ligne.strip()} » → {[str(v) for v in vals]}")
    return vus


total_auto = 0
for nom, t in (("cours_273.txt", COURS), ("fiche_193.txt", FICHE), ("exercices.txt", EX)):
    total_auto += egalites(t, nom)
check(total_auto >= 100, f"contrôle automatique : seulement {total_auto} égalités lues")
# test du détecteur : une erreur volontaire doit être repérée
_avant = len(ko)
egalites(r"$\frac{3}{20} = 16\,\%$", "test")
check(len(ko) == _avant + 1, "le contrôle automatique ne détecte pas une erreur volontaire")
if len(ko) == _avant + 1:
    ko.pop()
    ok += 1

# ===================================================================== structure
blocs = [b.strip() for b in re.split(r"^===[ \t]*$", EX, flags=re.M) if b.strip()]
check(len(blocs) == 10, f"{len(blocs)} exercices (10 attendus)")
types = [re.match(r"=== (\w+)", b).group(1) for b in blocs]
check(types == ["Découverte"] * 3 + ["Entraînement"] * 3 + ["Problème"] * 2 + ["Synthèse"] * 2, f"progression {types}")
diffs = [re.search(r"^Difficulté: (\w+)", b, re.M).group(1) for b in blocs]
check(diffs == ["easy"] * 3 + ["medium"] * 3 + ["hard"] * 4, f"difficultés {diffs}")
titres = [b.splitlines()[0] for b in blocs]
check(len(set(titres)) == 10, "titres uniques")
retires = {int(m) for m in re.findall(r"^(\d+)", (ICI / "exercices_retires.txt").read_text(encoding="utf-8"), re.M)}
ids = [int(re.search(r"^Id: (\d+)", b, re.M).group(1)) for b in blocs]
check(len(retires) == 11 and not (retires & set(ids)) and set(ids) | retires == set(range(3062, 3083)),
      "Id gardés / retirés (3062 à 3082)")
for b in blocs:
    eid = re.search(r"^Id: (\S+)", b, re.M).group(1)
    en = b.split("Énoncé:", 1)[1].split("Étapes:", 1)[0]
    et = b.split("Étapes:", 1)[1].split("Solution:", 1)[0]
    nq = len(re.findall(r"^\d+\. ", en, re.M))
    check(len(re.findall(r"^## Question", et, re.M)) == nq, f"{eid} : {nq} questions / corrigés")
    check(et.count("::: methode") >= nq and et.count("::: resultat") >= nq, f"{eid} : méthode et résultat par question")
    check("::: attention" in et or "::: retenir" in et, f"{eid} : erreur fréquente ou à retenir")
    sol = b.split("Solution:", 1)[1]
    check(len(re.findall(r"^\d+\. ", sol, re.M)) == nq, f"{eid} : solution courte complète")
    imgs = re.findall(r"\[IMAGE_(\d+)\]", b)
    check(len(set(imgs)) == len(imgs), f"{eid} : images appelées une seule fois")
check(sum("::: attention" in b for b in blocs) >= 9, "erreur fréquente dans presque tous les exercices")
for nom, t in (("cours_273.txt", COURS), ("fiche_193.txt", FICHE), ("exercices.txt", EX)):
    tl = t.lower()
    check("brevet" not in tl, f"{nom} : mention du brevet")
    check("médiane" not in tl and "pondérée" not in tl and "étendue" not in tl and "histogramme" not in tl,
          f"{nom} : notion de 4e ou hors programme de 5e (médiane, moyenne pondérée, étendue, histogramme)")

print(f"{ok} contrôles justes, {len(ko)} erreur(s) ; {total_auto} égalités numériques recalculées automatiquement")
for e in ko:
    print("  ✗", e)
sys.exit(1 if ko else 0)
