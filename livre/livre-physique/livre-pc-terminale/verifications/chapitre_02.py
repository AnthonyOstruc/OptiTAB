"""Vérification des résultats numériques du chapitre 2 (méthodes physiques d'analyse) et du défi D02.

Lancer : python -I -X utf8 verifications/chapitre_02.py
"""
import numpy as np

ECHECS = []
R = 8.314


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


# Exercice 1 : loi de Beer-Lambert, epsilon = 12 L/mol/cm
verifie("ex1 A pour c = 5,0e-2", 12 * 1.00 * 5.0e-2, 0.60, 1e-9)
verifie("ex1 c pour A = 0,42", 0.42 / 12, 3.5e-2, 0.05e-2)
verifie("ex1 A avec l = 2,00 cm", 12 * 2.00 * 5.0e-2, 1.2, 1e-9)
# Exercice 2 : loi de Kohlrausch
s_nacl = (5.01 + 7.63) * 2.0  # mS/m
verifie("ex2 sigma NaCl 2,0 mmol/L (mS/m)", s_nacl, 25.3, 0.05)
verifie("ex2 sigma NaCl en mS/cm", s_nacl / 100, 0.253, 0.0005)
verifie("ex2 sigma KNO3 (mS/m)", (7.35 + 7.14) * 2.0, 29.0, 0.05)
# Exercice 3 : gaz parfait
n_he = 1.05e5 * 4.2e-3 / (R * 293.15)
verifie("ex3 n(He)", n_he, 0.18, 0.005)
verifie("ex3 m(He) en g", n_he * 4.0, 0.72, 0.005)
verifie("ex3 bouteille 200 bar (mol)", 2.00e7 * 0.012 / (R * 293.15), 98, 0.6)
# Exercice 6 : colorant E133
c6 = np.array([1.0, 2.0, 4.0, 6.0, 8.0])
a6 = np.array([0.13, 0.26, 0.52, 0.79, 1.04])
k6 = (c6 * a6).sum() / (c6 ** 2).sum()
verifie("ex6 k (L/umol)", k6, 0.1305, 0.00005)
c_dil = 0.62 / k6
verifie("ex6 c solution diluée (umol/L)", c_dil, 4.75, 0.005)
verifie("ex6 c boisson (umol/L)", 2 * c_dil, 9.50, 0.005)
t6 = 2 * c_dil * 1e-6 * 792.8 * 1000
verifie("ex6 concentration en masse (mg/L)", t6, 7.5, 0.05)
verifie("ex6 volume pour la DJA d'un adolescent de 60 kg (L)", 6 * 60 / t6, 48, 0.5)
# Exercice 7 : sérum physiologique
c7 = np.array([2.0, 4.0, 6.0, 8.0, 10.0])
s7 = np.array([0.246, 0.488, 0.727, 0.962, 1.195])
k7 = (c7 * s7).sum() / (c7 ** 2).sum()
verifie("ex7 k (mS.cm-1 par mmol/L)", k7, 0.1202, 0.00005)
c_dil7 = 0.928 / k7
verifie("ex7 c sérum dilué (mmol/L)", c_dil7, 7.72, 0.005)
verifie("ex7 c sérum (mmol/L)", 20 * c_dil7, 154, 0.5)
verifie("ex7 concentration en masse NaCl (g/L)", 20 * c_dil7 * 1e-3 * 58.44, 9.0, 0.05)
# Exercice 8 : deux colorants
c_b = 0.53 / 1.06e5
verifie("ex8 c(bleu) dans le sirop dilué", c_b, 5.0e-6, 1e-9)
c_j = (0.51 - 3.0e3 * c_b) / 2.70e4
verifie("ex8 c(jaune) dans le sirop dilué", c_j, 1.83e-5, 0.005e-5)
verifie("ex8 c(jaune) sans additivité", 0.51 / 2.70e4, 1.89e-5, 0.005e-5)
verifie("ex8 erreur relative sans additivité (%)", (0.51 / 2.70e4 / c_j - 1) * 100, 3.0, 0.05)
# Exercice 10 : comprimé effervescent
n10 = 337e2 * 1.10e-3 / (R * 293.15)
verifie("ex10 n(CO2) (mol)", n10, 1.52e-2, 0.005e-2)
verifie("ex10 m(NaHCO3) (g)", n10 * 84.0, 1.28, 0.005)
verifie("ex10 écart relatif à 1,30 g (%)", (1.30 - n10 * 84.0) / 1.30 * 100, 1.7, 0.05)
# Exercice 11 : eau minérale (mg/L, g/mol, lambda en mS.m2/mol, charge)
ions = {'Ca': (80, 40.08, 11.9, 2), 'Mg': (26, 24.31, 10.6, 2), 'Na': (6.5, 22.99, 5.01, 1), 'K': (1.0, 39.10, 7.35, 1),
        'HCO3': (360, 61.02, 4.45, -1), 'SO4': (14, 96.06, 16.0, -2), 'Cl': (10, 35.45, 7.63, -1),
        'NO3': (3.8, 62.00, 7.14, -1)}
conc = {k: v[0] / v[1] for k, v in ions.items()}  # mmol/L = mol/m3
sigma11 = sum(ions[k][2] * conc[k] for k in ions) / 100  # mS/cm
verifie("ex11 c(HCO3-) (mmol/L)", conc['HCO3'], 5.90, 0.005)
verifie("ex11 c(Ca2+) (mmol/L)", conc['Ca'], 2.00, 0.005)
verifie("ex11 sigma calculée (mS/cm)", sigma11, 0.68, 0.005)
plus = sum(conc[k] * ions[k][3] for k in ions if ions[k][3] > 0)
moins = -sum(conc[k] * ions[k][3] for k in ions if ions[k][3] < 0)
verifie("ex11 charges positives (mmol/L)", plus, 6.44, 0.005)
verifie("ex11 charges négatives (mmol/L)", moins, 6.53, 0.005)
verifie("ex11 rapport mesure / calcul", 0.58 / sigma11, 0.85, 0.005)
# Exercice 12 : soluté antiseptique (permanganate)
c12 = np.array([20, 40, 60, 80, 100])
a12 = np.array([0.049, 0.095, 0.145, 0.191, 0.241])
k12 = (c12 * a12).sum() / (c12 ** 2).sum()
verifie("ex12 k (L/umol)", k12, 2.40e-3, 0.005e-3)
c_d = 0.150 / k12
verifie("ex12 c (umol/L)", c_d, 62.4, 0.05)
M_kmno4 = 39.10 + 54.94 + 4 * 16.00
t12 = c_d * 1e-6 * M_kmno4
verifie("ex12 M(KMnO4)", M_kmno4, 158.0, 0.05)
verifie("ex12 masse pour 100 mL (mg)", t12 * 100, 0.99, 0.005)
verifie("ex12 écart relatif à l'étiquette (%)", (1.0 - t12 * 100) / 1.0 * 100, 1.3, 0.05)
verifie("ex12 c attendue (umol/L)", 0.010 / M_kmno4 * 1e6, 63.3, 0.05)
# Exercice 13 : coussin de sécurité
n_n2 = 1.20e5 * 0.060 / (R * 353.15)
verifie("ex13 n(N2) (mol)", n_n2, 2.45, 0.005)
M_nan3 = 22.99 + 3 * 14.01
verifie("ex13 M(NaN3)", M_nan3, 65.0, 0.05)
verifie("ex13 m(NaN3) (g)", 2 / 3 * n_n2 * M_nan3, 106, 0.5)
verifie("ex13 pression après refroidissement à 20 °C (Pa)", 1.20e5 * 293.15 / 353.15, 1.0e5, 0.005e5)
# Exercice 15 : salinité de l'eau de mer
a15, b15 = np.polyfit(c7, s7, 1)
verifie("ex15 pente a", a15, 0.1186, 0.00005)
verifie("ex15 ordonnée b", b15, 0.012, 0.0005)
c15 = (0.712 - b15) / a15
verifie("ex15 c eau de mer diluée (mmol/L)", c15, 5.90, 0.005)
verifie("ex15 c eau de mer (mol/L)", c15 * 100 / 1000, 0.590, 0.0005)
verifie("ex15 salinité équivalente NaCl (g/L)", c15 * 100 / 1000 * 58.44, 34.5, 0.05)
verifie("ex15 sigma attendue sans dilution (mS/cm)", 0.590e3 * (5.01 + 7.63) / 100, 74.6, 0.05)

# Défi D02 : méthode des ajouts dosés
vs = np.array([0.0, 2.0, 4.0, 6.0, 8.0])
ad = np.array([0.209, 0.311, 0.417, 0.520, 0.623])
pente, origine = np.polyfit(vs, ad, 1)
verifie("D02 pente (par mL)", pente, 0.0519, 0.00006)
verifie("D02 ordonnée à l'origine", origine, 0.209, 0.0005)
c0 = origine / pente * 1.00e-4 / 10.0
verifie("D02 c0 (mol/L)", c0, 4.0e-5, 0.05e-5)
verifie("D02 k = epsilon x l (L/mol)", pente * 50.0 / 1.00e-4, 2.6e4, 0.05e4)
c0_vrai = (origine - 0.020) / pente * 1.00e-4 / 10.0
verifie("D02 b corrigée de l'absorbance parasite", origine - 0.020, 0.1886, 0.00005)
verifie("D02 c0 corrigée (mol/L)", c0_vrai, 3.6e-5, 0.05e-5)
verifie("D02 surestimation sans correction (%)", (c0 / c0_vrai - 1) * 100, 11, 0.5)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 2 et du défi D02 sont vérifiées.")
