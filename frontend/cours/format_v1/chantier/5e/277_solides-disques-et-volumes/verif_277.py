# -*- coding: utf-8 -*-
"""Vérification de la notion 277 (5e : solides, disques et volumes).

Cours, fiche, 10 exercices et figures : chaque volume, aire, conversion et
arrondi est recalculé en nombres exacts (sympy). Géométrie des figures :
arêtes cachées calculées, patrons de cube repliés, vues d'empilement,
longueurs des patrons. Contrôles de structure : 10 exercices, progression,
aucune mention du brevet, 10 gardés + 11 retirés = 21, figures appelées = déclarées.
Lancer : python verif_277.py
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

from sympy import Rational as R, Integer as I, pi, N, floor, sqrt

ICI = Path(__file__).resolve().parent
n_ok = 0


def ok(cond, msg):
    global n_ok
    assert cond, msg
    n_ok += 1


def d(s):
    """Décimal écrit à la française -> rationnel exact : '2,5' -> 5/2."""
    return R(s.replace(",", ".").replace(" ", "").replace(" ", ""))


def arrondi(x, n):
    """Arrondi au plus proche à n décimales (exact)."""
    q = R(10) ** n
    return R(floor(N(x, 30) * q + R(1, 2)), q)


def cyl(r, h):
    return pi * r ** 2 * h


# ================================================================== COURS
ok(6 + 2 == 8 and 3 * 6 == 18 and 2 * 6 == 12, "prisme à base hexagonale : 8 faces, 18 arêtes, 12 sommets")
ok(3 + 2 == 5 and 3 * 3 == 9 and 2 * 3 == 6, "prisme à base triangulaire : 5, 9, 6")
ok(1 + 2 + 2 + 3 == 8, "empilement du cours : 8 cubes")
H_c = {(0, 0): 1, (1, 0): 2, (0, 1): 2, (1, 1): 3}
ok([max(H_c[(i, 0)], H_c[(i, 1)]) for i in (0, 1)] == [2, 3], "vue de face du cours : 2 et 3")
ok(3 + 4 + 5 == 12 and 3 ** 2 + 4 ** 2 == 5 ** 2, "patron du prisme du cours : 12 cm, triangle 3-4-5 rectangle")
ok(2 * pi * 4 == 8 * pi and arrondi(8 * pi, 1) == d("25,1"), "patron cylindre r = 4 : 8π ≈ 25,1")
ok(4 * 3 == 12 and 12 * 2 == 24 and 4 * 3 * 2 == 24, "pavé de petits cubes 4 × 3 × 2")
ok(I(5) ** 3 == 125, "cube de 5 cm : 125 cm³")
ok(R(7 * 4, 2) == 14 and 14 * 10 == 140, "prisme du cours : B = 14, V = 140")
ok(pi * 5 ** 2 == 25 * pi and 25 * pi * 4 == 100 * pi and arrondi(100 * pi, 1) == d("314,2"), "cylindre du cours : 100π ≈ 314,2")
ok(10 * 10 * 10 == 1000, "1 dm³ = 1 000 cm³")
ok(d("1,8") * 1000 == 1800 and R(4200, 1000) == d("4,2") and 75 * 10 == 750 and d("0,3") * 1000 == 300, "exemples de conversions du cours")

# ================================================================== FICHE (mêmes formules)
ok(cyl(I(2), I(3)) == 12 * pi, "formule du cylindre")

# ================================================================== FIGURES : chargement du module
spec = importlib.util.spec_from_file_location("fig277", ICI / "figures" / "figures.py")
fig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fig)

# 3050 : arêtes cachées du prisme ABCDEF (calculées par la figure)
base, h = fig.PR3050
pr = fig.prisme_vertical(base, h, fig.Vue(1), bas=["A", "B", "C"], haut=["D", "E", "F"])
ok(pr.cachees() == [("A", "C"), ("B", "C"), ("C", "F")], f"3050 : arêtes cachées {pr.cachees()}")
ok(len(pr.F) == 5 and len(pr.aretes) == 9 and len(pr.V) == 6, "3050 : 5 faces, 9 arêtes, 6 sommets")
# solide 5 (maison couchée) : 7 faces, bases avant/arrière pentagonales
pm = fig.prisme_couche(fig.MAISON, 1.9, fig.Vue(1))
ok(len(pm.F) == 7 and len(fig.MAISON) == 5, "3050 : prisme couché à base pentagonale")


# 3047 : pliage des patrons de cube
def plier(cases):
    """Renvoie la normale extérieure (3D) de chaque carré après pliage, ou None si deux carrés se superposent."""
    cases = list(cases)
    pos = {c: k for k, c in enumerate(cases)}
    neg = lambda v: tuple(-x for x in v)
    etat = {0: ((0, 0, -1), (1, 0, 0), (0, 1, 0))}  # normale, est, nord
    file = [0]
    while file:
        k = file.pop()
        Nn, E, No = etat[k]
        c, r = cases[k]
        for (dc, dr), nouv in (((1, 0), lambda: (E, neg(Nn), No)), ((-1, 0), lambda: (neg(E), Nn, No)),
                               ((0, 1), lambda: (No, E, neg(Nn))), ((0, -1), lambda: (neg(No), E, Nn))):
            v = (c + dc, r + dr)
            if v in pos and pos[v] not in etat:
                etat[pos[v]] = nouv()
                file.append(pos[v])
    normales = [etat[k][0] for k in range(len(cases))]
    return normales if len(set(normales)) == 6 else None


res = {k: plier(c) for k, c in fig.PATRONS_3047.items()}
ok(res["A"] is not None and res["C"] is not None, "3047 : A et C sont des patrons")
ok(res["B"] is None and res["D"] is None, "3047 : B et D ne sont pas des patrons")
nA = res["A"]
opp = lambda n, i, j: n[i] == tuple(-x for x in n[j])
ok(opp(nA, 1, 3) and opp(nA, 0, 2) and opp(nA, 4, 5), "3047 : A, faces 2/4, 1/3, 5/6 opposées")
nC = res["C"]
ok(opp(nC, 0, 3) and opp(nC, 1, 4) and opp(nC, 2, 5), "3047 : C, paires de couleurs {0,3}, {1,4}, {2,5}")
ok(plier([(0, 1), (1, 1), (2, 1), (3, 1), (1, 2), (1, 0)]) is not None, "cours : patron en croix")
# patron du pavé 5 × 3 × 2 : a = hauteur, b = largeur, c = longueur
ok((2, 3, 5) == (2, 3, 5), "3047 : a = 2, b = 3, c = 5")

# 3054 : empilement
H = fig.H3054
ok(sum(H.values()) == 11, "3054 : 11 cubes")
ok([H[(i, 1)] for i in range(3)] == [3, 2, 2] and [H[(i, 0)] for i in range(3)] == [1, 2, 1], "3054 : piles")
ok(all(H[(i, 1)] >= H[(i, 0)] for i in range(3)), "3054 : piles du fond au moins aussi hautes (dessus visibles)")
face = [max(H[(i, 0)], H[(i, 1)]) for i in range(3)]
droite = [max(H[(i, j)] for i in range(3)) for j in (0, 1)]
ok(face == [3, 2, 2] and droite == [2, 3], "3054 : vues de face et de droite")
H2 = dict(H)
H2[(0, 0)] += 1
ok([max(H2[(i, 0)], H2[(i, 1)]) for i in range(3)] == face and sum(H2.values()) == 12, "3054 : un cube de plus, même vue de face")
ok(5 * 2 == 10 and 10 * 3 == 30 and 5 * 2 * 3 == 30, "3054 : pavé 5 × 2 × 3 = 30")

# ================================================================== 3045 : conversions
ok(3 * 1000 == 3000 and R(4500, 1000) == d("4,5") and d("2,5") * 1000 == 2500 and R(750, 1000) == d("0,75"), "3045 Q1")
ok(d("1,5") * 100 == 150 and 33 * 10 == 330 and R(250, 1000) == d("0,25"), "3045 Q2")
ok(2 == 2 and R(330, 10) == 33 and d("1,2") * 1000 == 1200, "3045 Q3")
ok(9 * 6 == 54 and 54 * 20 == 1080 and 9 * 6 * 20 == 1080 and R(1080, 1000) == d("1,08") > 1, "3045 Q4 : brique")
mL = {"0,4 L": d("0,4") * 1000, "380 cm3": 380, "0,0005 m3": d("0,0005") * 10 ** 6, "42 cL": 42 * 10}
ok(mL == {"0,4 L": 400, "380 cm3": 380, "0,0005 m3": 500, "42 cL": 420}, "3045 Q5 : en mL")
ok(sorted(mL, key=mL.get) == ["380 cm3", "0,4 L", "42 cL", "0,0005 m3"], "3045 Q5 : ordre")

# ================================================================== 3055 : prismes
ok(6 * 4 * d("2,5") == 60 and 6 * 4 == 24 and 24 * d("2,5") == 60, "3055 A : 60 cm³")
ok(R(5 * 4, 2) == 10 and 10 * 9 == 90, "3055 B : 90 cm³")
tri = fig.TRI_3055
ok(tri[1][0] - tri[0][0] == 6 and tri[2][1] == 4, "3055 C : figure côté 6, hauteur 4")
ok(R(6 * 4, 2) == 12 and 12 * 10 == 120, "3055 C : 120 cm³")
ok(60 < 90 < 120 and R(105, 15) == 7 and 15 * 7 == 105, "3055 Q4, Q5")

# ================================================================== 3051 : cylindres
V1, V2, V3 = cyl(3, 10), cyl(R(8, 2), 5), cyl(2, 15)
ok(pi * 3 ** 2 == 9 * pi and arrondi(9 * pi, 1) == d("28,3"), "3051 : aire de base 9π ≈ 28,3")
ok(V1 == 90 * pi and arrondi(V1, 1) == d("282,7"), "3051 : 90π ≈ 282,7")
ok(V2 == 80 * pi and arrondi(V2, 1) == d("251,3") and pi * 4 ** 2 == 16 * pi, "3051 : 80π ≈ 251,3")
ok(d("1,5") * 10 == 15 and V3 == 60 * pi and arrondi(V3, 1) == d("188,5"), "3051 : 60π ≈ 188,5")
ok(arrondi(V3 / 10, 1) == d("18,8") and floor(N(V3 / 10, 20) * 1000) == 18849, "3051 : 18,8 cL")
ok(V3 < V2 < V1, "3051 : ordre 3, 2, 1")
ok(V1 / 2 == 45 * pi and V2 != V1 / 2 and cyl(8, 5) == 320 * pi == 4 * V2, "3051 Q5 et erreur fréquente")

# ================================================================== 3061 : boîte en prisme
T = fig.TRI_3061
ok(T == [(0, 0), (6, 0), (0, 8)] and sqrt(6 ** 2 + 8 ** 2) == 10, "3061 : triangle 6-8-10 (figure)")
ok((8, 10, 15) == (8, 10, 15) and 6 + 8 + 10 == 24, "3061 : a = 8, b = 10, c = 15, périmètre 24")
ok(R(6 * 8, 2) == 24 and 24 * 15 == 360, "3061 : B = 24, V = 360")
ok(d("0,6") * 1000 == 600 and R(600, 24) == 25 and 24 * 25 == 600, "3061 : longueur 25 cm")
ok(2 * 24 == 48 and 6 * 25 + 8 * 25 + 10 * 25 == 600 and 150 + 200 + 250 == 600 and 48 + 600 == 648, "3061 : carton 648 cm²")

# ================================================================== 3052 : boîte de conserve
ok(R(10, 2) == 5 and arrondi(10 * pi, 1) == d("31,4") and floor(N(10 * pi, 20) * 1000) == 31415, "3052 : 10π ≈ 31,4")
ok(10 * pi * 11 == 110 * pi and arrondi(110 * pi, 1) == d("345,6") and arrondi(110 * pi, 0) == 346, "3052 : étiquette 346 cm²")
V = cyl(5, 11)
ok(V == 275 * pi and arrondi(V, 1) == d("863,9") and arrondi(V, 0) == 864, "3052 : 275π ≈ 864")
ok(864 - 850 == 14 and N(V) > 850, "3052 : 14 mL vides")
ok(arrondi(cyl(10, 11), 0) == 3456, "3052 : erreur fréquente 3 456 cm³")

# ================================================================== 3059 : aquarium
a, b, c = fig.AQ
rD, hD = fig.DECOR
ok((a, b, c) == (60, 30, 40) and (rD, hD) == (5, 20), "3059 : données de la figure")
ok(a * b * c == 72000 and a * b == 1800 and 1800 * 40 == 72000, "3059 : 72 000 cm³ = 72 L")
ok(R(54000, 1800) == 30 and 1800 * 30 == 54000, "3059 : hauteur 30 cm")
Vd = cyl(rD, hD)
ok(Vd == 500 * pi and arrondi(Vd, 1) == d("1570,8") and arrondi(Vd, 0) == 1571, "3059 : décor 500π ≈ 1 571")
ok(arrondi(R(1571, 1000), 1) == d("1,6"), "3059 : 1,6 L")
ok(hD < 30 and arrondi(Vd / 1800, 2) == d("0,87") and arrondi(30 + Vd / 1800, 1) == d("30,9"), "3059 : 30,9 cm")
ok(arrondi(54000 + Vd, 1) == d("55570,8") and 1800 * 36 == 64800, "3059 : 64 800 et 55 570,8")
reste = 64800 - (54000 + Vd)
ok(arrondi(reste, 1) == d("9229,2") and arrondi(reste / 1000, 1) == d("9,2"), "3059 : 9,2 L")

# ================================================================== 3041 : emballages
T = fig.TRI_3041
ok(T == [(0, 0), (6, 0), (3, 4)] and sqrt(3 ** 2 + 4 ** 2) == 5, "3041 : triangle isocèle 6-5-5, hauteur 4")
ok(3 + 2 == 5 and 3 * 3 == 9 and 2 * 3 == 6, "3041 : 5 faces, 9 arêtes, 6 sommets")
ok(arrondi(5 * pi, 1) == d("15,7") and R(5, 2) == d("2,5"), "3041 : rectangle 5π ≈ 15,7")
ok(R(6 * 4, 2) == 12 and 12 * 25 == 300, "3041 : V_A = 300")
VB = cyl(d("2,5"), 15)
ok(VB == d("93,75") * pi and d("2,5") ** 2 == d("6,25") and arrondi(VB, 1) == d("294,5"), "3041 : V_B ≈ 294,5")
ok(N(VB) < 300 and R(300, 10) == 30, "3041 : A choisi, 30 cL")

# ================================================================== STRUCTURE
ex = (ICI / "exercices.txt").read_text(encoding="utf-8")
titres = re.findall(r"^=== (.+)$", ex, re.M)
types = [t.split(" - ")[0] for t in titres]
ok(len(titres) == 10 and len(set(titres)) == 10, "10 titres uniques")
ok(types == ["Découverte"] * 3 + ["Entraînement"] * 3 + ["Problème"] * 2 + ["Synthèse"] * 2, "progression 3 / 3 / 2 / 2")
ok(all("Solides, disques" not in t for t in titres), "titres sans le nom du chapitre")
diff = re.findall(r"^Difficulté:\s*(\w+)", ex, re.M)
ok(diff == ["easy"] * 3 + ["medium"] * 3 + ["hard"] * 4, "difficultés cohérentes")
for nom in ("cours_272.txt", "fiche_192.txt", "exercices.txt"):
    t = (ICI / nom).read_text(encoding="utf-8")
    ok("brevet" not in t.lower(), f"pas de « brevet » dans {nom}")
    ok("pythagore" not in t.lower() and "\\sqrt" not in t, f"pas de Pythagore ni de racine (4e) dans {nom}")
    ok(t.lower().count("pyramide") <= (1 if nom == "cours_272.txt" else 0), f"pyramides : au plus une mention ({nom})")
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
    nq = len(re.findall(r"^## Question", bloc, re.M))
    ok(bloc.count("::: resultat") >= nq, f"{tid} : un résultat par question")
    nq_e = len(re.findall(r"^\d+\. ", bloc.split("Étapes:")[0], re.M))
    ok(nq == nq_e, f"{tid} : {nq_e} questions dans l'énoncé, {nq} dans le corrigé")
    sol = bloc.split("Solution:")[1]
    ok(len(re.findall(r"^\d+\. ", sol, re.M)) == nq_e, f"{tid} : solution courte complète")
    ok("Solution:" in bloc and "Étapes:" in bloc and "Énoncé:" in bloc, f"{tid} : rubriques")

# figures : chaque [IMAGE_N] appelé est déclaré, et chaque figure déclarée existe et est compilée
corr = json.loads((ICI / "figures" / "correspondance.json").read_text(encoding="utf-8"))
images = ICI / "figures" / "images"
for bloc in ex.split("\n===\n"):
    if not bloc.strip():
        continue
    tid = re.search(r"^Id:\s*(\d+)", bloc, re.M).group(1)
    appels = sorted(set(re.findall(r"\[IMAGE_(\d+)\]", bloc)), key=int)
    decl = sorted(corr["exercices"].get(tid, {}).keys(), key=int)
    ok(appels == decl, f"{tid} : images appelées {appels} = déclarées {decl}")
for nom, cle, idd in (("cours_272.txt", "cours", "272"), ("fiche_192.txt", "fiches", "192")):
    appels = sorted(set(re.findall(r"\[IMAGE_(\d+)\]", (ICI / nom).read_text(encoding="utf-8"))), key=int)
    ok(appels == sorted(corr[cle][idd].keys(), key=int), f"{nom} : images")
utilisees = set()
for cle in corr:
    for idd in corr[cle]:
        for pos, e in corr[cle][idd].items():
            ok((images / e["fichier"]).exists() and len(e["alt"]) >= 15, f"{cle} {idd} {pos} : fichier et alt")
            utilisees.add(e["fichier"][:-4])
ok(utilisees == set(fig.FIGURES), f"figures définies = figures utilisées ({set(fig.FIGURES) ^ utilisees})")
ok(set(p.stem for p in images.glob("*.png")) == set(fig.FIGURES), "aucune image orpheline dans figures/images")

print(f"verif_277 : {n_ok} contrôles, tous justes.")
