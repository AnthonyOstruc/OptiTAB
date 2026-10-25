"""Vérification des résultats numériques du chapitre 9 (force des acides et des bases) et du défi D09.

Lancer : python -I -X utf8 verifications/chapitre_09.py
"""
import io
from contextlib import redirect_stdout
from math import log10, sqrt

ECHECS = []
KE = 1.0e-14


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def h_acide_faible(ka, c):
    """Racine positive de h² + Ka h − Ka c = 0."""
    return (-ka + sqrt(ka * ka + 4 * ka * c)) / 2


# L'essentiel
verifie("essentiel pH acide fort 2,0e-3", -log10(2.0e-3), 2.70, 0.005)
verifie("essentiel pH base forte 1,0e-3", 14.0 + log10(1.0e-3), 11.0, 1e-9)
h = h_acide_faible(1.7e-5, 1.0e-2)
verifie("essentiel h éthanoïque 1,0e-2 (mol/L)", h, 4.0e-4, 0.05e-4)
verifie("essentiel pH éthanoïque 1,0e-2", -log10(h), 3.39, 0.005)
for pka, ka in ((3.75, 1.8e-4), (4.20, 10 ** -4.20), (4.76, 1.7e-5), (7.5, 3.2e-8), (9.2, 6.3e-10)):
    verifie(f"tableau Ka pour pKa = {pka}", 10 ** -pka, ka, ka * 0.03)
# Exercice 1
verifie("ex1 [HO-] à pH 2,0", KE / 10 ** -2.0, 1.0e-12, 1e-15)
verifie("ex1 [HO-] à pH 11,0", KE / 10 ** -11.0, 1.0e-3, 1e-9)
verifie("ex1 pKe à 60 °C", -log10(9.6e-14), 13.0, 0.05)
verifie("ex1 pH neutre à 60 °C", -log10(9.6e-14) / 2, 6.51, 0.005)
# Exercice 2
verifie("ex2 tau HCl", 10 ** -2.0 / 1.0e-2, 1, 1e-9)
verifie("ex2 tau éthanoïque", 10 ** -3.4 / 1.0e-2, 0.040, 0.0005)
verifie("ex2 pourcentage non dissocié (%)", 100 * (1 - 10 ** -3.4 / 1.0e-2), 96, 0.5)
# Exercice 3
verifie("ex3 Ka HCOOH", 10 ** -3.75, 1.8e-4, 0.05e-4)
verifie("ex3 Ka HClO", 10 ** -7.5, 3.2e-8, 0.05e-8)
verifie("ex3 Ka NH4+", 10 ** -9.2, 6.3e-10, 0.05e-10)
# Exercice 4
verifie("ex4 rapport AH/A- à pH 2,5", 10 ** (4.2 - 2.5), 50, 0.5)
verifie("ex4 part de la forme basique (%)", 100 / (1 + 10 ** 1.7), 2, 0.3)
# Exercice 5
verifie("ex5 pH acide nitrique", -log10(2.0e-3), 2.70, 0.005)
verifie("ex5 pH soude", 14.0 + log10(1.0e-3), 11.0, 1e-9)
verifie("ex5 c du déboucheur (mol/L)", 10 ** (10.4 - 14), 2.5e-4, 0.05e-4)
verifie("ex5 volume d'eau à ajouter (mL)", 10 * 10 - 10, 90, 1e-9)
# Exercice 6
h6 = h_acide_faible(1.8e-4, 1.0e-2)
verifie("ex6 h méthanoïque (mol/L)", h6, 1.25e-3, 0.005e-3)
verifie("ex6 pH méthanoïque", -log10(h6), 2.90, 0.005)
verifie("ex6 tau méthanoïque (%)", 100 * h6 / 1.0e-2, 12.5, 0.1)
verifie("ex6 tau éthanoïque (%)", 100 * 10 ** -3.39 / 1.0e-2, 4.1, 0.05)
# Exercice 7
verifie("ex7 alpha(A-) à pH 3,8 (%)", 100 / (1 + 10 ** (4.76 - 3.8)), 10, 0.5)
verifie("ex7 rapport A-/AH à pH 3,8", 10 ** (3.8 - 4.76), 0.11, 0.005)
verifie("ex7 alpha(A-) à pH 2,8 (%)", 100 / (1 + 10 ** (4.76 - 2.8)), 1, 0.1)
# Exercice 8
h8 = h_acide_faible(1.8e-4, 5.0e-3)
verifie("ex8 h (mol/L)", h8, 8.6e-4, 0.05e-4)
verifie("ex8 pH", -log10(h8), 3.06, 0.005)
verifie("ex8 tau (%)", 100 * h8 / 5.0e-3, 17.3, 0.1)
verifie("ex8 h approché (mol/L)", sqrt(1.8e-4 * 5.0e-3), 9.5e-4, 0.02e-4)
verifie("ex8 pH approché", -log10(sqrt(1.8e-4 * 5.0e-3)), 3.02, 0.005)
# Exercice 9
verifie("ex9 rapport In-/HIn à pH 7,4", 10 ** (7.4 - 7.1), 2.0, 0.005)
# Exercice 10
verifie("ex10 pH après ajout", 4.76 + log10(0.099 / 0.101), 4.75, 0.005)
verifie("ex10 pH dans l'eau pure", -log10(1.0e-3), 3.00, 1e-9)
# Exercice 11 : sorties du programme
tampon = io.StringIO()
with redirect_stdout(tampon):
    pKa = 4.76

    def alpha(pH):
        return 1 / (1 + 10 ** (pKa - pH))

    for pH in (3.76, 4.76, 5.76):
        print(round(alpha(pH), 3))
sortie = tampon.getvalue().strip().splitlines()
print('   ex11 sorties :', sortie)
if sortie != ['0.091', '0.5', '0.909']:
    ECHECS.append('ex11 sorties du programme')
verifie("ex11 forme acide à pH 7,4 (pKa 6,1)", round(1 - 1 / (1 + 10 ** (6.1 - 7.4)), 3), 0.048, 1e-9)
# Exercice 12
verifie("ex12 rapport HCO3-/CO2", 10 ** (7.4 - 6.1), 20, 0.5)
verifie("ex12 [CO2,H2O] (mmol/L)", 24 / 10 ** 1.3, 1.2, 0.05)
verifie("ex12 hausse de pH pour CO2 divisé par 2", log10(2), 0.30, 0.005)
# Exercice 13
c13 = 1.6 / 90.1
verifie("ex13 c acide lactique (mol/L)", c13, 1.8e-2, 0.05e-2)
h13 = h_acide_faible(1.4e-4, c13)
verifie("ex13 h (mol/L)", h13, 1.5e-3, 0.05e-3)
verifie("ex13 pH", -log10(h13), 2.82, 0.005)
verifie("ex13 tau (%)", 100 * h13 / c13, 8.5, 0.1)
verifie("ex13 rapport lactate/acide à pH 4,5", 10 ** (4.5 - 3.86), 4.4, 0.05)
verifie("ex13 part de la forme acide dans le yaourt (%)", 100 / (1 + 10 ** 0.64), 19, 0.5)
# Exercice 14
verifie("ex14 c max (mol/L)", 0.150 / 122.1, 1.23e-3, 0.005e-3)
verifie("ex14 fraction active à pH 3,2", 1 / (1 + 10 ** (3.2 - 4.2)), 0.91, 0.005)
verifie("ex14 fraction active à pH 5,5", 1 / (1 + 10 ** (5.5 - 4.2)), 0.048, 0.0005)
verifie("ex14 rapport des efficacités", 0.909 / 0.0477, 19, 0.5)
verifie("ex14 fraction active à pH 6,0", 1 / (1 + 10 ** (6.0 - 4.2)), 0.016, 0.0005)
# Exercice 15
verifie("ex15 fraction HClO à pH 7,2", 1 / (1 + 10 ** (7.2 - 7.5)), 0.67, 0.005)
verifie("ex15 fraction HClO à pH 7,4", 1 / (1 + 10 ** (7.4 - 7.5)), 0.56, 0.005)
verifie("ex15 fraction HClO à pH 8,2", 1 / (1 + 10 ** (8.2 - 7.5)), 0.17, 0.005)

# Défi D09 : acide fort très dilué
tampon = io.StringIO()
with redirect_stdout(tampon):
    Ke = 1.0e-14
    for c in (1.0e-2, 1.0e-6, 1.0e-8, 1.0e-10):
        h = (c + sqrt(c ** 2 + 4 * Ke)) / 2
        print(c, round(-log10(h), 2))
sortie = tampon.getvalue().strip().splitlines()
print('   D09 sorties :', sortie)
if sortie != ['0.01 2.0', '1e-06 6.0', '1e-08 6.98', '1e-10 7.0']:
    ECHECS.append('D09 sorties du programme')
hd = (1.0e-8 + sqrt(1.0e-16 + 4 * KE)) / 2
verifie("D09 h pour c = 1e-8 (mol/L)", hd, 1.05e-7, 0.005e-7)
verifie("D09 pH pour c = 1e-8", -log10(hd), 6.98, 0.005)
verifie("D09 racine de Ke (mol/L)", sqrt(KE), 1.0e-7, 1e-12)
verifie("D09 écart à la droite pour c = 1e-6", abs(-log10((1e-6 + sqrt(1e-12 + 4 * KE)) / 2) - 6.0), 0.004, 0.001)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 9 et du défi D09 sont vérifiées.")
