"""Vérification des résultats numériques du chapitre 3 (titrages) et du défi D03.

Les volumes équivalents lus sur les figures sont recalculés à partir des données générées
(generer_donnees.py) par la méthode des tangentes et par l'intersection des droites.
Lancer : python -I -X utf8 verifications/chapitre_03.py
"""
from math import log10
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tangentes import tangentes  # noqa: E402
from droites_conductimetrie import segments  # noqa: E402

ECHECS = []


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


# Exercice 1 : solution commerciale d'acide chlorhydrique
c1 = 0.23 * 1110 / 36.5
verifie("ex1 c solution commerciale (mol/L)", c1, 7.0, 0.05)
verifie("ex1 masse de 1 L (g)", 1.11 * 1000, 1110, 1e-9)
verifie("ex1 volume à prélever (mL)", 0.100 * 500.0 / c1, 7.1, 0.05)
# Exercice 2
verifie("ex2 a) c_A", 0.100 * 12.6 / 20.0, 0.0630, 1e-9)
verifie("ex2 b) c(NH3)", 0.0500 * 14.2 / 10.0, 0.0710, 1e-9)
# Exercice 3
s, b1, b2, bm, ve3, phe3 = tangentes('03-hcl-naoh-ph', 0.20, 20.0)
verifie("ex3 VE (mL)", ve3, 20.0, 0.05)
verifie("ex3 pH_E", phe3, 7.0, 0.05)
verifie("ex3 c_A", 1.00e-2 * 20.0 / 20.0, 1.00e-2, 1e-12)
# Exercice 4
_, (ve4,) = segments('03-naoh-hcl-sigma', [(0, 7), (9, 16)])
verifie("ex4 VE (mL)", ve4, 7.9, 0.05)
verifie("ex4 c(NaOH)", 0.0500 * 7.9 / 20.0, 2.0e-2, 0.05e-2)
# Exercice 6 : composition au cours du titrage
n0 = 1.0e-2 * 20.0e-3
for v, (h, na, oh) in {10.0: (1.0e-4, 1.0e-4, 0.0), 20.0: (0.0, 2.0e-4, 0.0), 30.0: (0.0, 3.0e-4, 1.0e-4)}.items():
    nb = 1.0e-2 * v * 1e-3
    verifie(f"ex6 n(H3O+) à {v} mL", max(n0 - nb, 0), h, 1e-12)
    verifie(f"ex6 n(Na+) à {v} mL", nb, na, 1e-12)
    verifie(f"ex6 n(HO-) à {v} mL", max(nb - n0, 0), oh, 1e-12)
verifie("ex6 pH à 10,0 mL", -log10(1.0e-4 / 30.0e-3), 2.48, 0.005)
verifie("ex6 pH à 30,0 mL", 14 + log10(1.0e-4 / 50.0e-3), 11.30, 0.005)
# Exercice 7 : contributions à la conductivité
verifie("ex7 avant E (HCl)", 5.01 - 35.0, -30.0, 0.05)
verifie("ex7 après E", 5.01 + 19.9, 24.9, 0.05)
verifie("ex7 avant E (acide éthanoïque)", 5.01 + 4.09, 9.1, 0.05)
verifie("ex7 rapport des pentes", (5.01 + 19.9) / (5.01 + 4.09), 2.7, 0.05)
# Exercice 8 : vinaigre
s, b1, b2, bm, ve8, phe8 = tangentes('03-vinaigre-ph', 0.30, 10.1)
verifie("ex8 VE (mL)", ve8, 10.1, 0.05)
verifie("ex8 pH_E", phe8, 8.7, 0.05)
c8 = 10 * 0.100 * 10.1 / 10.0
verifie("ex8 c(vinaigre)", c8, 1.01, 0.005)
verifie("ex8 degré d'acidité", c8 * 60.05 * 100 / 1010, 6.0, 0.05)
# Exercice 9 : ions chlorure
_, (ve9,) = segments('03-chlorure-sigma', [(0, 5.5), (7, 12)])
verifie("ex9 VE (mL)", ve9, 6.1, 0.05)
c9 = 10 * 0.0500 * 6.1 / 20.0
verifie("ex9 c(Cl-) dans le sérum", c9, 0.15, 0.005)
verifie("ex9 concentration en masse (g/L)", c9 * 58.44, 8.9, 0.05)
# Exercice 10
verifie("ex10 VE (mL)", 1.00e-3 / 0.100 * 1000, 10.0, 1e-9)
# Exercice 11 : degré Dornic
m11 = 1.6e-3 * (1 / 9) * 90.08
verifie("ex11 masse d'acide lactique dans 10 mL (g)", m11, 0.0160, 0.00005)
verifie("ex11 degré Dornic", m11 / 0.010 / 0.1, 16, 0.05)
verifie("ex11 coefficient : °D par mL de soude", (1e-3 / 9 * 90.08) / 0.010 / 0.1, 10.0, 0.01)
# Exercice 12 : déboucheur
s, b1, b2, bm, ve12, phe12 = tangentes('03-deboucheur-ph', 0.25, 21.6)
verifie("ex12 VE (mL)", ve12, 21.6, 0.05)
c12 = 25 * 0.100 * 21.6 / 20.0
verifie("ex12 c(soude commerciale)", c12, 2.70, 0.005)
verifie("ex12 titre massique (%)", c12 * 40.0 / 1100 * 100, 9.8, 0.05)
verifie("ex12 VE attendu pour 10 %", 0.10 * 1100 / 40.0 / 25 * 20.0 / 0.100, 22.0, 0.05)
# Exercice 13 : aspirine
s, b1, b2, bm, ve13, phe13 = tangentes('03-aspirine-ph', 0.20, 13.8)
verifie("ex13 VE (mL)", ve13, 13.8, 0.05)
m13 = 0.0500 * 13.8e-3 * 4 * 180.16
verifie("ex13 masse d'aspirine (mg)", m13 * 1000, 497, 0.5)
verifie("ex13 écart relatif (%)", (500 - m13 * 1000) / 500 * 100, 0.6, 0.05)
# Exercice 14 : mélange
_, (ve14a, ve14b) = segments('03-melange-sigma', [(0, 2.5), (6, 13), (15, 20)])
verifie("ex14 VE1 (mL)", ve14a, 4.1, 0.05)
verifie("ex14 VE2 (mL)", ve14b, 13.9, 0.05)
verifie("ex14 c(HCl)", 0.100 * 4.1 / 20.0, 0.020, 0.0005)
verifie("ex14 c(acide éthanoïque)", 0.100 * (13.9 - 4.1) / 20.0, 0.049, 0.0005)
verifie("ex14 c(HCl) dans le vinaigre", 20 * 0.100 * 4.1 / 20.0, 0.41, 0.005)
verifie("ex14 c(acide éthanoïque) dans le vinaigre", 20 * 0.100 * 9.8 / 20.0, 0.98, 0.005)
# Exercice 15 : correction de dilution
_, (ve15,) = segments('03-dilution-sigma', [(0, 9), (11, 20)], colonne=2)
verifie("ex15 VE avec la conductivité corrigée", ve15, 10.0, 0.05)
_, (ve15b,) = segments('03-dilution-sigma', [(0, 4), (16, 20)], colonne=1)
verifie("ex15 VE avec la conductivité brute", ve15b, 7.9, 0.05)
verifie("ex15 erreur relative (%)", (10.0 - ve15b) / 10.0 * 100, 21, 0.5)
verifie("ex15 c(HCl)", 0.100 * 10.0 / 20.0, 0.0500, 1e-12)

# Défi D03 : identifier un acide inconnu
s, b1, b2, bm, ved, phed = tangentes('03-succinique-ph', 0.15, 25.4)
verifie("D03 VE (mL)", ved, 25.4, 0.05)
n_ho = 0.100 * 25.4e-3
verifie("D03 n(HO-) à l'équivalence (mmol)", n_ho * 1000, 2.54, 0.005)
verifie("D03 M si monoacide (g/mol)", 0.150 / n_ho, 59.1, 0.05)
M = 4 * 12.01 + 6 * 1.008 + 4 * 16.00
verifie("D03 M(C4H6O4)", M, 118.1, 0.05)
verifie("D03 %C", 4 * 12.01 / M * 100, 40.7, 0.05)
verifie("D03 %H", 6 * 1.008 / M * 100, 5.1, 0.05)
verifie("D03 %O", 4 * 16.00 / M * 100, 54.2, 0.05)
verifie("D03 n(acide) (mmol)", 0.150 / M * 1000, 1.27, 0.005)
verifie("D03 rapport n(HO-) / n(acide)", n_ho / (0.150 / M), 2.0, 0.01)
for nom, (c, h, o) in {'C2H3O2': (2, 3, 2)}.items():
    m = c * 12.01 + h * 1.008 + o * 16.00
    verifie(f"D03 M({nom})", m, 59.0, 0.05)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 3 et du défi D03 sont vérifiées.")
