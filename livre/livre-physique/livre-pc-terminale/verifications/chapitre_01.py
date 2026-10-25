"""Vérification des résultats numériques du chapitre 1 (transformations acide-base) et du défi D01.

Chaque valeur publiée dans un corrigé est recalculée ici, puis comparée à la valeur imprimée
(arrondie comme dans le livre). Lancer : python -I -X utf8 verifications/chapitre_01.py
"""
from math import log10, pi, sqrt
import numpy as np

ECHECS = []


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def ph(h):
    return -log10(h)


# Exercice 3 : pH <-> concentration en ion oxonium
verifie("ex3 1a pH(1,0e-3)", ph(1.0e-3), 3.00, 0.005)
verifie("ex3 1b pH(2,5e-4)", ph(2.5e-4), 3.60, 0.005)
verifie("ex3 1c pH(6,3e-9)", ph(6.3e-9), 8.20, 0.005)
verifie("ex3 2b [H3O+] pour pH 7,40", 10 ** -7.40, 4.0e-8, 0.05e-8)
verifie("ex3 2c [H3O+] pour pH 11,3", 10 ** -11.3, 5e-12, 0.5e-12)
# Exercice 8 : éthylamine, pH 11,8
verifie("ex8 [H3O+] pour pH 11,8", 10 ** -11.8, 2e-12, 0.5e-12)
# Exercice 10 : eau minérale
M_HCO3 = 1.0 + 12.0 + 3 * 16.0
c_hco3 = 3.050 / M_HCO3
verifie("ex10 M(HCO3-)", M_HCO3, 61.0, 1e-9)
verifie("ex10 c(HCO3-)", c_hco3, 5.00e-2, 0.005e-2)
n10 = c_hco3 * 0.200
verifie("ex10 n(HCO3-) dans 200 mL", n10, 1.00e-2, 0.005e-2)
verifie("ex10 V(CO2) en L", n10 * 24.0, 0.240, 0.0005)
# Exercice 11 : facteurs de concentration
verifie("ex11 1 pluie 5,6 -> 4,3", 10 ** (5.6 - 4.3), 20, 0.5)
verifie("ex11 2 sang 7,35 -> 7,45", 10 ** 0.10, 1.26, 0.005)
verifie("ex11 3 dilution par 5 de pH 2,7", 2.7 + log10(5), 3.4, 0.05)
verifie("ex11 4 facteur pour +0,5", 10 ** 0.5, 3.2, 0.05)
# Exercice 13 : ballon (vinaigre + hydrogénocarbonate)
rho, titre, M_acide, M_nahco3, Vm = 1.01, 0.060, 60.0, 84.0, 24.0
c_acide = rho * 1000 * titre / M_acide
verifie("ex13 c(acide éthanoïque) mol/L", c_acide, 1.01, 0.005)
n_acide = c_acide * 0.0500
n_hco3 = 5.00 / M_nahco3
verifie("ex13 n(acide)", n_acide, 5.05e-2, 0.005e-2)
verifie("ex13 n(HCO3-)", n_hco3, 5.95e-2, 0.005e-2)
assert n_acide < n_hco3, "l'acide doit être limitant"
V_co2 = n_acide * Vm
verifie("ex13 V(CO2) en L", V_co2, 1.21, 0.005)
V_sphere15 = 4 / 3 * pi * 7.5 ** 3 / 1000
verifie("ex13 volume sphère D = 15 cm (L)", V_sphere15, 1.77, 0.005)
D_max = (6 * V_co2 * 1000 / pi) ** (1 / 3)
verifie("ex13 diamètre maximal (cm)", D_max, 13.2, 0.05)
n_15 = V_sphere15 / Vm
verifie("ex13 n nécessaire pour 15 cm", n_15, 7.36e-2, 0.005e-2)
verifie("ex13 V vinaigre nécessaire (mL)", n_15 / c_acide * 1000, 73, 0.5)
verifie("ex13 m NaHCO3 nécessaire (g)", n_15 * M_nahco3, 6.19, 0.005)
verifie("ex13 m NaHCO3 stoechiométrique pour 50 mL (g)", n_acide * M_nahco3, 4.24, 0.005)
# Exercice 14 : acidification des océans (données AEE 2026)
h1985, h2024 = 10 ** -8.11, 10 ** -8.04
verifie("ex14 [H3O+] 1985", h1985, 7.8e-9, 0.05e-9)
verifie("ex14 [H3O+] 2024", h2024, 9.1e-9, 0.05e-9)
verifie("ex14 augmentation relative (%)", (h2024 / h1985 - 1) * 100, 17.5, 0.05)
verifie("ex14 [H3O+] 2100 bas (pH 7,89)", 10 ** -7.89, 1.3e-8, 0.05e-8)
verifie("ex14 [H3O+] 2100 haut (pH 7,54)", 10 ** -7.54, 2.9e-8, 0.05e-8)
verifie("ex14 facteur bas", 10 ** 0.15, 1.4, 0.05)
verifie("ex14 facteur haut", 10 ** 0.5, 3.2, 0.05)
# Exercice 15 : régression linéaire sur les cinq premières mesures
c = np.array([1e-1, 1e-2, 1e-3, 1e-4, 1e-5])
mesures = np.array([1.10, 2.04, 3.02, 4.01, 4.98])
a, b = np.polyfit(-np.log10(c), mesures, 1)
verifie("ex15 pente", a, 0.973, 0.0005)
verifie("ex15 ordonnée à l'origine", b, 0.111, 0.0005)
ecarts = np.abs(mesures - (-np.log10(c)))
for ci, e, attendu in zip(c, ecarts, [0.10, 0.04, 0.02, 0.01, 0.02]):
    verifie(f"ex15 écart pour c = {ci:.0e}", e, attendu, 0.005)
verifie("ex15 écart pour c = 1e-6", abs(5.81 - 6), 0.19, 0.005)
verifie("ex15 [H3O+] mesurée pour c = 1e-6", 10 ** -5.81, 1.5e-6, 0.05e-6)

# Défi D01
h_mel = (1.0e-2 * 0.100 + 1.0e-4 * 0.100) / 0.200
verifie("D01 q1 [H3O+] du mélange", h_mel, 5.05e-3, 0.005e-3)
verifie("D01 q1 pH du mélange", ph(h_mel), 2.30, 0.005)
# q3 : volume de solution de pH 4,0 pour atteindre pH 3,0
V = (1.0e-2 * 0.100 - 1.0e-3 * 0.100) / (1.0e-3 - 1.0e-4)
verifie("D01 q3 volume de solution pH 4,0 (L)", V, 1.0, 1e-9)
V_eau = 1.0e-2 * 0.100 / 1.0e-3 - 0.100
verifie("D01 q3 volume d'eau (L)", V_eau, 0.90, 1e-9)
KE = 1.0e-14


def ph_exact(x):
    return ph((x + sqrt(x * x + 4 * KE)) / 2)


verifie("D01 q4 pH exact c = 1e-8", ph_exact(1.0e-8), 6.98, 0.005)
verifie("D01 q4 h exact c = 1e-8", (1e-8 + sqrt(1e-16 + 4e-14)) / 2, 1.05e-7, 0.005e-7)
seuil = sqrt(4 * KE / ((2 * 10 ** 0.01 - 1) ** 2 - 1))
verifie("D01 q5 seuil de concentration", seuil, 6.5e-7, 0.05e-7)
verifie("D01 q5 écart au seuil", -log10(seuil) - ph_exact(seuil), 0.01, 1e-9)
verifie("D01 q5 écart pour 1e-6", -log10(1e-6) - ph_exact(1e-6), 0.0043, 0.00005)
# Monotonie : l'écart décroît quand c augmente
grille = np.logspace(-10, -3, 400)
ecart = np.array([-log10(x) - ph_exact(x) for x in grille])
assert np.all(np.diff(ecart) < 0), "l'écart doit décroître avec c"
print("ok  D01 q5 écart strictement décroissant sur [1e-10 ; 1e-3]")

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 1 et du défi D01 sont vérifiées.")
