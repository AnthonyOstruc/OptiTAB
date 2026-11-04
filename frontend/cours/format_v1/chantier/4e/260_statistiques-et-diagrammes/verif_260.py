# -*- coding: utf-8 -*-
"""Vérification (sympy, valeurs exactes) de tous les calculs de la notion 260
« Statistiques et diagrammes » (4e) : cours, fiche, 21 exercices et données des figures.

Lancer : python verif_260.py  (depuis ce dossier)
"""
import importlib.util
import pathlib
from sympy import Rational as R, nsimplify

ICI = pathlib.Path(__file__).resolve().parent
OK = 0
ERREURS = []


def eg(nom, a, b):
    global OK
    if isinstance(a, (list, tuple)):
        a, b = tuple(nsimplify(x) for x in a), tuple(nsimplify(x) for x in b)
    elif not isinstance(a, bool):
        a, b = nsimplify(a), nsimplify(b)
    if a == b:
        OK += 1
    else:
        ERREURS.append(f"{nom} : {a} != {b}")


def arr(x, n):
    """Arrondi décimal (au 10^-n) d'une valeur exacte, renvoyé exact."""
    return R(round(float(x) * 10 ** n), 10 ** n)


def moyenne(v):
    return R(sum(v), len(v))


def moy_pond(vals, eff):
    return R(sum(a * b for a, b in zip(vals, eff)), sum(eff))


def mediane(v):
    s = sorted(v)
    n = len(s)
    return R(s[n // 2]) if n % 2 else R(s[n // 2 - 1] + s[n // 2], 2)


def deplie(vals, eff):
    out = []
    for a, b in zip(vals, eff):
        out += [a] * b
    return out


def etendue(v):
    return max(v) - min(v)


spec = importlib.util.spec_from_file_location("fig260", ICI / "figures" / "figures.py")
FIG = importlib.util.module_from_spec(spec)
spec.loader.exec_module(FIG)
D = FIG.DONNEES

# ======================================================================== COURS / FICHE
liv_v, liv_e = D["cours_livres"]
eg("cours effectif total livres", sum(liv_e), 25)
for e, p in zip(liv_e, [8, 24, 36, 20, 12]):
    eg(f"cours fréquence {e}/25", R(e, 25) * 100, p)
eg("cours somme fréquences", 8 + 24 + 36 + 20 + 12, 100)
eg("cours somme pondérée livres", sum(a * b for a, b in zip(liv_v, liv_e)), 51)
eg("cours moyenne livres", moy_pond(liv_v, liv_e), R("2.04"))
eg("cours moyenne non pondérée (erreur)", moyenne(liv_v), 2)
eg("cours médiane livres", mediane(deplie(liv_v, liv_e)), 2)
eg("cours rangs livres", [sum(liv_e[:k]) for k in range(1, 4)], [2, 8, 17])
eg("cours étendue livres", etendue(liv_v), 4)
eg("cours moyenne simple notes", moyenne([11, 15, 8, 14, 12]), 12)
eg("cours moyenne coef", moy_pond([12, 15, 9], [2, 1, 3]), 11)
eg("cours somme coef produits", 24 + 15 + 27, 66)
MI = [13, 8, 17, 10, 12, 8, 15]
eg("cours série impair rangée", sorted(MI), D["cours_mediane_impair"])
eg("cours médiane impair", mediane(MI), 12)
MP = D["cours_mediane_pair"]
eg("cours médiane pair", mediane(MP), R("10.5"))
eg("cours étendue pair", etendue(MP), 16)
eg("cours somme pair", sum(MP), 88)
eg("cours moyenne pair", moyenne(MP), 11)
MP2 = MP[:-1] + [60]
eg("cours somme 60", sum(MP2), 128)
eg("cours moyenne 60", moyenne(MP2), 16)
eg("cours médiane 60", mediane(MP2), R("10.5"))
act = D["cours_activites"]
eg("cours total activités", sum(e for _, e in act), 36)
for n, e in act:
    eg(f"cours angle {n}", R(e, 36) * 360, e * 10)
eg("cours somme angles", sum(e * 10 for _, e in act), 360)
eg("cours 1 % en degrés", R(360, 100), R("3.6"))
eg("cours effectif histogramme", sum(D["cours_tailles"][1]), 25)
TX, TY = D["cours_temperatures"]
eg("cours max température", max(TY), 21)
eg("cours heure du max", TX[TY.index(21)], 14)
eg("cours min température", min(TY), 8)
eg("cours heure du min", TX[TY.index(8)], 6)
eg("cours étendue températures", etendue(TY), 13)
eg("cours croissance 6 h -> 14 h", all(TY[i] < TY[i + 1] for i in range(4)), True)
eg("cours décroissance 14 h -> 20 h", all(TY[i] > TY[i + 1] for i in range(4, 7)), True)
CA, CB = D["cours_comparaison"]
eg("cours moyenne A", moyenne(CA), 10)
eg("cours moyenne B", moyenne(CB), 10)
eg("cours somme A", sum(CA), 50)
eg("cours étendue A", etendue(CA), 2)
eg("cours étendue B", etendue(CB), 15)

# ======================================================================== 2684
SP = [e for _, e in D["2684"]]
eg("2684 total", sum(SP), 25)
for e, p in zip(SP, [32, 20, 16, 24, 8]):
    eg(f"2684 fréquence {e}", R(e, 25) * 100, p)
eg("2684 collectifs", R(8 + 5, 25) * 100, 52)
eg("2684 tennis 7/30", arr(R(7, 30) * 100, 1), R("23.3"))
eg("2684 football 8/30", arr(R(8, 30) * 100, 1), R("26.7"))
eg("2684 7/30 décimal", arr(R(7, 30), 4), R("0.2333"))
eg("2684 8/30 décimal", arr(R(8, 30), 4), R("0.2667"))

# ======================================================================== 2685
fv, fe = D["2685"]
eg("2685 total", sum(fe), 25)
eg("2685 ni frère", R(fe[0], 25), R("0.16"))
eg("2685 au moins 2", fe[2] + fe[3] + fe[4], 12)
eg("2685 au moins 2 %", R(12, 25), R("0.48"))
eg("2685 total frères", sum(a * b for a, b in zip(fv, fe)), 40)
eg("2685 moyenne", moy_pond(fv, fe), R("1.6"))

# ======================================================================== 2686
L = [12, 15, 8, 17, 13]
eg("2686 somme", sum(L), 65)
eg("2686 moyenne", moyenne(L), 13)
eg("2686 moyenne 6 notes", arr(moyenne(L + [9]), 2), R("12.33"))
eg("2686 note pour 14", 14 * 6 - 65, 19)
eg("2686 vérif 14", moyenne(L + [19]), 14)
eg("2686 note pour 16", 16 * 6 - 65, 31)
eg("2686 étendue", etendue(L), 9)
eg("2686 médiane", mediane(L), 13)
eg("2686 série rangée figure", sorted(L), D["2686"])

# ======================================================================== 2687
S = [12, 5, 9, 15, 7, 11, 9]
eg("2687 rangée", sorted(S), D["2687"][0])
eg("2687 médiane", mediane(S), 9)
S8 = S + [20]
eg("2687 rangée 8", sorted(S8), D["2687"][1])
eg("2687 médiane 8", mediane(S8), 10)
eg("2687 étendue", etendue(S8), 15)
eg("2687 somme", sum(S8), 88)
eg("2687 moyenne", moyenne(S8), 11)
S100 = S + [100]
eg("2687 somme 100", sum(S100), 168)
eg("2687 moyenne 100", moyenne(S100), 21)
eg("2687 médiane 100", mediane(S100), 10)

# ======================================================================== 2688
N, C = [14, 12, 15, 18], [4, 3, 2, 1]
eg("2688 moyenne simple", moyenne(N), R("14.75"))
eg("2688 somme pondérée", sum(a * b for a, b in zip(N, C)), 140)
eg("2688 moyenne pondérée", moy_pond(N, C), 14)
eg("2688 erreur /4", R(140, 4), 35)
eg("2688 maths 10", moy_pond([10, 12, 15, 18], C), R("12.4"))
eg("2688 somme maths 10", 40 + 36 + 30 + 18, 124)
eg("2688 +1 maths", moy_pond([15, 12, 15, 18], C) - 14, R("0.4"))
eg("2688 +1 sport", moy_pond([14, 12, 15, 19], C) - 14, R("0.1"))
eg("2688 note pour 15", R(15 * 10 - 84, 4), R("16.5"))
eg("2688 vérif 15", moy_pond([R("16.5"), 12, 15, 18], C), 15)

# ======================================================================== 2689
TR = D["2689"]
eg("2689 voiture", 100 - (30 + 15 + 40), 15)
eg("2689 pourcentages figure", [p for _, p in TR], [30, 15, 40, 15])
for (n, p), e in zip(TR, [72, 36, 96, 36]):
    eg(f"2689 effectif {n}", R(p, 100) * 240, e)
for (n, p), a in zip(TR, [108, 54, 144, 54]):
    eg(f"2689 angle {n}", R(p, 100) * 360, a)
eg("2689 somme effectifs", 72 + 36 + 96 + 36, 240)
eg("2689 somme angles", 108 + 54 + 144 + 54, 360)
eg("2689 bus ou vélo", 40 + 15, 55)
eg("2689 angle bus ou vélo", R(55, 100) * 360, 198)
eg("2689 erreur 1 %", R(360, 100), R("3.6"))

# ======================================================================== 2690
pv, pe = D["2690"]
eg("2690 total", sum(pe), 25)
eg("2690 produits", [a * b for a, b in zip(pv, pe)], [108, 185, 304, 234, 120])
eg("2690 somme", sum(a * b for a, b in zip(pv, pe)), 951)
eg("2690 moyenne", moy_pond(pv, pe), R("38.04"))
eg("2690 erreur", moyenne(pv), 38)
eg("2690 médiane", mediane(deplie(pv, pe)), 38)
eg("2690 rang médian", deplie(pv, pe)[12], 38)
eg("2690 cumul", [sum(pe[:k]) for k in range(1, 4)], [3, 8, 16])
eg("2690 étendue", etendue(pv), 4)
eg("2690 mode", pv[pe.index(max(pe))], 38)
eg("2690 39 ou plus", R(pe[3] + pe[4], 25), R("0.36"))

# ======================================================================== 2691
_, A, B = D["2691"]
eg("2691 somme A", sum(A), 98)
eg("2691 somme B", sum(B), 98)
eg("2691 moyenne A", moyenne(A), 14)
eg("2691 moyenne B", moyenne(B), 14)
eg("2691 étendue A", etendue(A), 4)
eg("2691 étendue B", etendue(B), 16)
eg("2691 rangée A", sorted(A), [12, 13, 14, 14, 14, 15, 16])
eg("2691 rangée B", sorted(B), [6, 10, 10, 12, 18, 20, 22])
eg("2691 médiane A", mediane(A), 14)
eg("2691 médiane B", mediane(B), 12)
eg("2691 rapport étendues", R(16, 4), 4)

# ======================================================================== 2692
brut = [12, 8, 14, 10, 16, 12, 6, 10, 18, 12, 14, 8, 10, 12, 16, 14, 6, 12, 10, 18, 8, 14, 12, 16, 10]
nv, ne = D["2692"]
eg("2692 nombre de notes", len(brut), 25)
eg("2692 effectifs comptés", [brut.count(v) for v in nv], ne)
eg("2692 somme effectifs", sum(ne), 25)
eg("2692 produits", [a * b for a, b in zip(nv, ne)], [12, 24, 50, 72, 56, 48, 36])
eg("2692 somme", sum(brut), 298)
eg("2692 moyenne", moyenne(brut), R("11.92"))
eg("2692 médiane", mediane(brut), 12)
eg("2692 cumul", [sum(ne[:k]) for k in range(1, 5)], [2, 5, 10, 16])
eg("2692 au moins 10", sum(1 for x in brut if x >= 10), 20)
eg("2692 fréquence", R(20, 25), R("0.8"))
b1 = [x + 1 for x in brut]
eg("2692 moyenne +1", moyenne(b1), R("12.92"))
eg("2692 somme +1", sum(b1), 323)
eg("2692 médiane +1", mediane(b1), 13)
eg("2692 étendue", etendue(brut), 12)
eg("2692 étendue +1", etendue(b1), 12)

# ======================================================================== 2693
G = [45, 52, 38, 61, 70, 84, 57]
eg("2693 total", sum(G), 407)
eg("2693 moyenne", arr(moyenne(G), 2), R("58.14"))
eg("2693 rangée", sorted(G), D["2693"])
eg("2693 médiane", mediane(G), 57)
eg("2693 étendue", etendue(G), 46)
eg("2693 week-end", 84 + 57, 141)
eg("2693 week-end %", arr(R(141, 407) * 100, 1), R("34.6"))
eg("2693 week-end décimal", arr(R(141, 407), 3), R("0.346"))
eg("2693 total 60", 60 * 7, 420)
eg("2693 manque", 420 - 407, 13)
eg("2693 dimanche", 57 + 13, 70)
eg("2693 vérif", moyenne(G[:-1] + [70]), 60)

# ======================================================================== 2694
eg("2694 somme A", R("12.5") * 24, 300)
eg("2694 somme B", R("11.5") * 26, 299)
eg("2694 moyenne", R(599, 50), R("11.98"))
eg("2694 nouvel élève", arr(R(299 + 18, 27), 2), R("11.74"))
eg("2694 exemple 25", R("12.5") * 25 + R("11.5") * 25, 600)
eg("2694 exemple moyenne", R(600, 50), 12)

# ======================================================================== 2695
SA = D["2695"]
eg("2695 somme", sum(SA), 22300)
eg("2695 moyenne", arr(moyenne(SA), 2), R("2477.78"))
eg("2695 médiane", mediane(SA), 1800)
eg("2695 sous la moyenne", sum(1 for x in SA if x < moyenne(SA)), 7)
eg("2695 %", arr(R(7, 9) * 100, 1), R("77.8"))
SA8 = SA[:-1]
eg("2695 somme sans", sum(SA8), 14300)
eg("2695 moyenne sans", moyenne(SA8), R("1787.5"))
eg("2695 médiane sans", mediane(SA8), 1650)
eg("2695 étendue avec", etendue(SA), 6500)
eg("2695 étendue sans", etendue(SA8), 1100)

# ======================================================================== 2696
eg("2696 somme", 11 * 5, 55)
eg("2696 x", 55 - (8 + 11 + 14 + 9), 13)
X = [8, 11, 13, 14, 9]
eg("2696 moyenne", moyenne(X), 11)
eg("2696 médiane", mediane(X), 11)
eg("2696 étendue", etendue(X), 6)
eg("2696 y", 12 * 6 - 55, 17)
eg("2696 moyenne y", moyenne(X + [17]), 12)
eg("2696 erreur y = 12", arr(moyenne(X + [12]), 2), R("11.17"))
eg("2696 médiane 6", mediane(X + [17]), 12)

# ======================================================================== 2697
bo, ee = D["2697"]
eg("2697 total", sum(ee), 100)
eg("2697 classe max", bo[ee.index(max(ee))], 2)
eg("2697 au moins 3 h", ee[3] + ee[4], 33)
eg("2697 moins de 2 h", ee[0] + ee[1], 37)
eg("2697 cumul", [sum(ee[:k]) for k in range(1, 6)], [12, 37, 67, 85, 100])
centres = [R(1, 2) + k for k in range(5)]
eg("2697 produits", [c * e for c, e in zip(centres, ee)], [6, R("37.5"), 75, 63, R("67.5")])
eg("2697 moyenne", moy_pond(centres, ee), R("2.49"))
eg("2697 minutes", R("0.49") * 60, R("29.4"))

# ======================================================================== 2698
JM, PA = [117, 54, 189, 90], [96, 45, 96, 63]
eg("2698 total JM", sum(JM), 450)
eg("2698 total PA", sum(PA), 300)
eg("2698 fréquences JM", [R(e, 450) * 100 for e in JM], D["2698"][1])
eg("2698 fréquences PA", [R(e, 300) * 100 for e in PA], D["2698"][2])
eg("2698 somme JM", sum(D["2698"][1]), 100)
eg("2698 somme PA", sum(D["2698"][2]), 100)
eg("2698 angle bus", R(42, 100) * 360, R("151.2"))
eg("2698 vélo réunis", R(54 + 45, 750), R("0.132"))
eg("2698 moyenne fréquences", R(12 + 15, 2), R("13.5"))

# ======================================================================== 2699
for n, t, a, p, e in D["2699"]:
    eg(f"2699 angle texte {n}", R(t.replace(",", ".")), nsimplify(a))
    eg(f"2699 fréquence {n}", nsimplify(a) / 360 * 100, p)
    eg(f"2699 effectif {n}", R(p, 100) * 200, e)
eg("2699 somme angles", sum(nsimplify(a) for _, _, a, _, _ in D["2699"]), 360)
eg("2699 somme effectifs", 86 + 48 + 36 + 30, 200)
eg("2699 extrapolation", R(43, 100) * 15000, 6450)
eg("2699 montagne ou campagne", 48 + 36, 84)
eg("2699 42 %", R(42, 100) * 200, 84)

# ======================================================================== 2700
H, HC = [11, 9, 13, 10], [1, 2, 1, 2]
eg("2700 moyenne simple", moyenne(H), R("10.75"))
eg("2700 somme pondérée", sum(a * b for a, b in zip(H, HC)), 62)
eg("2700 moyenne pondérée", arr(moy_pond(H, HC), 2), R("10.33"))
eg("2700 somme visée", 12 * 9, 108)
eg("2700 x exact", R(108 - 62, 3), R(46, 3))
eg("2700 x arrondi", arr(R(46, 3), 2), R("15.33"))
eg("2700 avec 15", 62 + 3 * 15, 107)
eg("2700 avec 15,5", 62 + 3 * R("15.5"), R("108.5"))
eg("2700 moyenne 15,5", arr(R("108.5") / 9, 2), R("12.06"))
eg("2700 max", arr(R(62 + 60, 9), 2), R("13.56"))

# ======================================================================== 2701
v1, v2 = D["2701"]
eg("2701 hausse", v2 - v1, 4)
eg("2701 taux", arr(R(4, 102) * 100, 1), R("3.9"))
eg("2701 taux décimal", arr(R(4, 102), 3), R("0.039"))
eg("2701 rapport visuel", R(v2 - 100, v1 - 100), 3)
eg("2701 rapport réel", arr(R(v2, v1), 2), R("1.04"))

# ======================================================================== 2702
_, PL = D["2702"]
eg("2702 premier semestre", sum(PL[:6]), 318)
eg("2702 second semestre", sum(PL[6:]), 335)
eg("2702 total", sum(PL), 653)
eg("2702 moyenne", arr(moyenne(PL), 2), R("54.42"))
eg("2702 max novembre", (max(PL), PL.index(max(PL))), (80, 10))
eg("2702 min août", (min(PL), PL.index(min(PL))), (30, 7))
eg("2702 étendue", etendue(PL), 50)
eg("2702 rangée", sorted(PL), [30, 35, 45, 48, 50, 52, 55, 55, 65, 68, 70, 80])
eg("2702 médiane", mediane(PL), R("53.5"))
eg("2702 moins de 55", sum(1 for x in PL if x < 55), 6)
eg("2702 au-dessus moyenne", [i for i, x in enumerate(PL) if x > moyenne(PL)], [3, 4, 8, 9, 10, 11])
eg("2702 automne", sum(PL[8:11]), 205)
eg("2702 automne %", arr(R(205, 653) * 100, 1), R("31.4"))
eg("2702 automne décimal", arr(R(205, 653), 3), R("0.314"))

# ======================================================================== 2703
IA, IB = D["2703"]
eg("2703 A jours 1-5", sum(IA[:5]), 125)
eg("2703 A jours 6-10", sum(IA[5:]), 125)
eg("2703 B jours 1-5", sum(IB[:5]), 110)
eg("2703 B jours 6-10", sum(IB[5:]), 120)
eg("2703 moyenne A", moyenne(IA), 25)
eg("2703 moyenne B", moyenne(IB), 23)
eg("2703 étendue A", etendue(IA), 2)
eg("2703 étendue B", etendue(IB), 22)
eg("2703 rangée A", sorted(IA), [24, 24, 25, 25, 25, 25, 25, 25, 26, 26])
eg("2703 rangée B", sorted(IB), [18, 18, 18, 19, 19, 20, 21, 22, 35, 40])
eg("2703 médiane A", mediane(IA), 25)
eg("2703 médiane B", mediane(IB), R("19.5"))
eg("2703 retards A", sum(1 for x in IA if x > 30), 0)
eg("2703 retards B jours", [i + 1 for i, x in enumerate(IB) if x > 30], [3, 6])
eg("2703 % retards", R(2, 10), R("0.2"))

# ======================================================================== 2704
av, ae = D["2704"]
eg("2704 total", sum(ae), 40)
eg("2704 produits", [a * b for a, b in zip(av, ae)], [60, 104, 140, 105, 96, 68])
eg("2704 somme", sum(a * b for a, b in zip(av, ae)), 573)
eg("2704 moyenne", moy_pond(av, ae), R("14.325"))
eg("2704 moyenne arrondie", arr(moy_pond(av, ae), 1), R("14.3"))
eg("2704 médiane", mediane(deplie(av, ae)), 14)
eg("2704 cumul", [sum(ae[:k]) for k in range(1, 4)], [5, 13, 23])
eg("2704 étendue", etendue(av), 5)
eg("2704 moins de 14", R(ae[0] + ae[1], 40), R("0.325"))
eg("2704 Étoile somme", 15 * 30, 450)
eg("2704 fusion", arr(R(573 + 450, 70), 2), R("14.61"))
eg("2704 somme fusion", 573 + 450, 1023)
eg("2704 moyenne des moyennes", arr((R("14.325") + 15) / 2, 2), R("14.66"))
eg("2704 fusion différente", R(1023, 70) != (R("14.325") + 15) / 2, True)
nouv = deplie(av, ae) + [18] * 5
eg("2704 nouvelle somme", sum(nouv), 663)
eg("2704 nouvelle moyenne", arr(moyenne(nouv), 1), R("14.7"))
eg("2704 nouvelle médiane", mediane(nouv), 14)
eg("2704 23e valeur", sorted(nouv)[22], 14)
eg("2704 nouvelle étendue", etendue(nouv), 6)

print(f"{OK} contrôles justes, {len(ERREURS)} erreur(s)")
for e in ERREURS:
    print("  ✗", e)
