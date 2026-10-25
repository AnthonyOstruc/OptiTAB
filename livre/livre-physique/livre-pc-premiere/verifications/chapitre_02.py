"""Vérification des résultats numériques du chapitre 2 (absorbance et dosage par étalonnage) et du défi D02.

Lancer : python -I -X utf8 verifications/chapitre_02.py
"""
import io
from contextlib import redirect_stdout

ECHECS = []


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def sortie_de(fonction):
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        fonction()
    return tampon.getvalue().strip()


K_BLEU = 0.106          # L/µmol, bleu patenté à 638 nm, cuve de 1,00 cm
# L'essentiel
for c, a in ((1.0, 0.106), (2.0, 0.212), (4.0, 0.424), (6.0, 0.636), (8.0, 0.848)):
    verifie(f"cours gamme : A pour {c} µmol/L", K_BLEU * c, a, 0.0005)
verifie("cours concentration inconnue (µmol/L)", 0.45 / K_BLEU, 4.25, 0.005)
verifie("cours coefficient d'absorption molaire (L/mol/cm)", K_BLEU * 1e6, 1.06e5, 1)
verifie("cours permanganate : A", 2.4e3 * 1.00 * 1.0e-4, 0.24, 1e-9)


def programme_cours():
    c = [1.0, 2.0, 4.0, 6.0, 8.0]
    A = [0.106, 0.212, 0.424, 0.636, 0.848]
    num, den = 0, 0
    for i in range(len(c)):
        num = num + c[i] * A[i]
        den = den + c[i] ** 2
    k = num / den
    print(round(k, 3), round(0.45 / k, 2))


s = sortie_de(programme_cours)
print('   cours programme :', s)
if s != '0.106 4.25':
    ECHECS.append('cours programme')
# Exercice 3
verifie("ex3 A pour 2,0e-4 mol/L", 2.4e3 * 1.00 * 2.0e-4, 0.48, 1e-9)
verifie("ex3 c pour A = 0,30 (mol/L)", 0.30 / 2.4e3, 1.25e-4, 1e-12)
verifie("ex3 A avec une cuve de 2,00 cm", 2.4e3 * 2.00 * 2.0e-4, 0.96, 1e-9)
verifie("ex3 M(KMnO4)", 39.1 + 54.9 + 4 * 16.0, 158.0, 1e-9)
verifie("ex3 concentration en masse (mg/L)", 1.25e-4 * 158.0 * 1000, 19.8, 0.051)
# Exercice 4
for c, a in ((10, 0.12), (20, 0.24), (40, 0.48), (60, 0.72), (80, 0.96)):
    verifie(f"ex4 A pour {c} mmol/L", 0.012 * c, a, 1e-9)
verifie("ex4 c inconnue (mmol/L)", 0.54 / 0.012, 45, 1e-9)
verifie("ex4 coefficient d'absorption molaire (L/mol/cm)", 0.012 * 1000, 12, 1e-9)
verifie("ex4 concentration en masse de CuSO4 (g/L)", 0.045 * 159.6, 7.18, 0.005)
# Exercice 5
verifie("ex5 c de la solution diluée (µmol/L)", 0.42 / K_BLEU, 3.96, 0.005)
verifie("ex5 c du sirop (µmol/L)", 10 * 0.42 / K_BLEU, 39.6, 0.05)
# Exercice 6
for c, v in ((1.0, 2.5), (2.0, 5.0), (4.0, 10.0), (6.0, 15.0), (8.0, 20.0)):
    verifie(f"ex6 volume de mère pour {c} µmol/L (mL)", c * 25.0 / 10.0, v, 1e-9)
# Exercice 7
c7 = 0.150 / 2.4e3
verifie("ex7 c permanganate (mol/L)", c7, 6.25e-5, 1e-12)
verifie("ex7 concentration en masse (mg/L)", c7 * 158.0 * 1000, 9.9, 0.05)
verifie("ex7 0,0010 % en masse/volume (mg/L)", 0.0010 / 100 * 1e6, 10, 1e-9)
verifie("ex7 absorbance attendue pour 10 mg/L", 10e-3 / 158.0 * 2.4e3, 0.152, 0.0005)
# Exercice 8
c8 = 0.37 / 0.012
verifie("ex8 c ions cuivre (mmol/L)", c8, 30.8, 0.05)
verifie("ex8 masse de cuivre (g)", c8 * 1e-3 * 0.100 * 63.5, 0.196, 0.0005)
verifie("ex8 pourcentage de cuivre (%)", 100 * c8 * 1e-3 * 0.100 * 63.5 / 1.00, 19.6, 0.05)
# Exercice 9


def programme_ex9():
    c = [1.0, 2.0, 4.0, 6.0, 8.0]
    A = [0.107, 0.210, 0.425, 0.634, 0.851]
    num = 0
    den = 0
    for i in range(len(c)):
        num = num + c[i] * A[i]
        den = den + c[i] ** 2
    k = num / den
    print(round(k, 4))
    for i in range(len(c)):
        print(c[i], round(100 * (A[i] - k * c[i]) / (k * c[i]), 1))


s = sortie_de(programme_ex9).replace('\n', ' | ')
print('   ex9 programme :', s)
if s != '0.1061 | 1.0 0.8 | 2.0 -1.0 | 4.0 0.1 | 6.0 -0.4 | 8.0 0.3':
    ECHECS.append('ex9 programme')
verifie("ex9 concentration pour A = 0,50 (µmol/L)", 0.50 / 0.1061, 4.71, 0.005)
# Exercice 10
verifie("ex10 coefficient sur la partie linéaire (L/µmol)", 0.53 / 5, 0.106, 1e-9)
verifie("ex10 A attendue à 25 µmol/L sans saturation", 0.106 * 25, 2.65, 1e-9)
verifie("ex10 dilution pour A = 2,4 vers 0,6", 2.4 / 0.6, 4, 1e-9)
# Exercice 11
verifie("ex11 c bleu patenté (µmol/L)", 0.53 / K_BLEU, 5.0, 1e-9)
# Exercice 12
c12 = 0.53 / K_BLEU * 20
verifie("ex12 c dans la solution diluée (µmol/L)", 0.53 / K_BLEU, 5.0, 1e-9)
verifie("ex12 c dans le sirop (µmol/L)", c12, 100, 1e-9)
verifie("ex12 concentration en masse (mg/L)", c12 * 1e-6 * 582.7 * 1000, 58, 0.5)
verifie("ex12 masse par verre de 20 mL de sirop (mg)", c12 * 1e-6 * 582.7 * 20, 1.2, 0.05)
verifie("ex8 quantité de cuivre (mol)", 0.37 / 0.012 * 1e-3 * 0.100, 3.08e-3, 0.005e-3)
verifie("ex14 c de la boisson mesurée (mol/L)", 0.318 / 9.7e3 * 50, 1.64e-3, 0.005e-3)
verifie("ex15 c dans la fiole de 1 L (mol/L)", 0.108 / 1.11e4 * 25, 2.43e-4, 0.005e-4)
verifie("ex15 c attendue diluée (mol/L)", 0.014 / 55.8 / 25, 1.00e-5, 0.005e-5)
verifie("ex13 nitrates du puits B arrondi (mg/L)", 0.48 / 0.0085, 56, 0.5)
verifie("ex12 DJA d'un enfant de 30 kg (mg)", 5 * 30, 150, 1e-9)
verifie("ex12 nombre de verres", 150 / (c12 * 1e-6 * 582.7 * 20), 130, 2)
# Exercice 13
for t, a in ((10, 0.085), (20, 0.170), (30, 0.255), (40, 0.340), (50, 0.425)):
    verifie(f"ex13 A pour {t} mg/L", 0.0085 * t, a, 1e-9)
verifie("ex13 nitrates du puits A (mg/L)", 0.392 / 0.0085, 46.1, 0.05)
verifie("ex13 nitrates du puits B (mg/L)", 0.48 / 0.0085, 56.5, 0.05)
verifie("ex13 c nitrates du puits A (mol/L)", 0.392 / 0.0085 / 1000 / 62.0, 7.44e-4, 0.005e-4)
verifie("ex13 M(NO3-)", 14.0 + 3 * 16.0, 62.0, 1e-9)
# Exercice 14
c14 = 0.32 / 194.2
verifie("ex14 c caféine de la boisson (mol/L)", c14, 1.65e-3, 0.005e-3)
verifie("ex14 A sans dilution", c14 * 9.7e3, 16, 0.5)
verifie("ex14 A après dilution par 50", c14 / 50 * 9.7e3, 0.32, 0.005)
verifie("ex14 c mesurée diluée (mol/L)", 0.318 / 9.7e3, 3.28e-5, 0.005e-5)
verifie("ex14 concentration en masse (g/L)", 0.318 / 9.7e3 * 50 * 194.2, 0.318, 0.0005)
verifie("ex14 caféine par canette de 250 mL (mg)", 0.318 * 250, 80, 0.5)
verifie("ex14 limite pour 60 kg (mg)", 3 * 60, 180, 1e-9)
verifie("ex14 canettes", 180 / 80, 2.25, 1e-9)
# Exercice 15
c15 = 0.014 / 55.8
verifie("ex15 c attendue dans la fiole (mol/L)", c15, 2.51e-4, 0.005e-4)
verifie("ex15 A attendue", c15 / 25 * 1.11e4, 0.111, 0.0005)
m15 = 0.108 / 1.11e4 * 25 * 55.8 * 1000
verifie("ex15 masse de fer mesurée (mg)", m15, 13.6, 0.05)
verifie("ex15 part de l'indication (%)", 100 * m15 / 14, 97, 0.5)
verifie("ex15 c diluée mesurée (mol/L)", 0.108 / 1.11e4, 9.73e-6, 0.005e-6)
# Défi D02
cB = 0.53 / 0.106
cJ = (0.62 - 0.0060 * cB) / 0.0270
verifie("D02 c bleu patenté (µmol/L)", cB, 5.0, 1e-9)
verifie("D02 c tartrazine (µmol/L)", cJ, 21.9, 0.05)
verifie("D02 c tartrazine en négligeant le bleu (µmol/L)", 0.62 / 0.0270, 23.0, 0.05)
verifie("D02 erreur relative (%)", 100 * (0.62 / 0.0270 - cJ) / cJ, 5.1, 0.05)
verifie("D02 part du bleu dans A(427)", 0.0060 * cB / 0.62 * 100, 4.8, 0.05)
verifie("D02 coefficients molaires tartrazine (L/mol/cm)", 0.0270e6, 2.70e4, 1e-6)
verifie("D02 tartrazine dans le sirop (µmol/L)", 20 * 21.9, 438, 1e-9)
verifie("D02 bleu patenté dans le sirop (µmol/L)", 20 * cB, 100, 1e-9)
verifie("D02 contribution du bleu à 427 nm", 0.0060 * cB, 0.030, 1e-9)
verifie("D02 erreur avec valeurs arrondies (%)", 100 * (23.0 - 21.9) / 21.9, 5, 0.1)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 2 et du défi D02 sont vérifiées.")
