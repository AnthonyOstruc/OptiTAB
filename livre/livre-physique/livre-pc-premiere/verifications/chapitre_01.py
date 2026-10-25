"""Vérification des résultats numériques du chapitre 1 (composition d'un système chimique) et du défi D01.

Lancer : python -I -X utf8 verifications/chapitre_01.py
"""
import io
from contextlib import redirect_stdout

ECHECS = []
NA = 6.02e23          # mol^-1
VM = 24.0             # L/mol à 20 °C et 1013 hPa
MA = {'H': 1.0, 'He': 4.0, 'C': 12.0, 'N': 14.0, 'O': 16.0, 'Na': 23.0, 'Mg': 24.3, 'S': 32.1, 'Cl': 35.5,
      'K': 39.1, 'Ca': 40.1, 'Cu': 63.5, 'Ag': 107.9, 'Au': 197.0}


def M(**formule):
    return sum(MA[el] * nb for el, nb in formule.items())


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


# L'essentiel
verifie("cours M(H2O)", M(H=2, O=1), 18.0, 1e-9)
verifie("cours M(CO2)", M(C=1, O=2), 44.0, 1e-9)
verifie("cours M(saccharose)", M(C=12, H=22, O=11), 342.0, 1e-9)
verifie("cours n saccharose 10,0 g (mol)", 10.0 / 342.0, 0.0292, 0.00005)
verifie("cours N saccharose", 10.0 / 342.0 * NA, 1.76e22, 0.005e22)
verifie("cours n eau 100 g (mol)", 100 / 18.0, 5.56, 0.005)
verifie("cours N eau 100 g", 100 / 18.0 * NA, 3.34e24, 0.005e24)
verifie("cours n dioxygène 1,0 L (mol)", 1.0 / VM, 0.0417, 0.00005)
verifie("cours m dioxygène 1,0 L (g)", 1.0 / VM * 32.0, 1.33, 0.005)
verifie("cours M(NaCl)", M(Na=1, Cl=1), 58.5, 1e-9)
verifie("cours n NaCl 5,85 g (mol)", 5.85 / 58.5, 0.100, 1e-9)
verifie("cours c NaCl (mol/L)", 0.100 / 0.5000, 0.200, 1e-9)
verifie("cours t NaCl (g/L)", 0.200 * 58.5, 11.7, 1e-9)
verifie("cours facteur de dilution", 0.200 / 0.0200, 10, 1e-9)
verifie("cours volume prélevé (mL)", 100.0 / 10, 10.0, 1e-9)


def programme_cours():
    M_atome = {'H': 1.0, 'C': 12.0, 'N': 14.0, 'O': 16.0}
    formule = {'C': 8, 'H': 10, 'N': 4, 'O': 2}      # caféine
    Mm = 0
    for element in formule:
        Mm = Mm + formule[element] * M_atome[element]
    m = 0.080                                         # g
    n = m / Mm
    print(Mm, f"{n:.3e}", f"{n * 6.02e23:.3e}")


s = sortie_de(programme_cours)
print('   cours programme :', s)
if s != '194.0 4.124e-04 2.482e+20':
    ECHECS.append('cours programme')
# Exercice 1
verifie("ex1 M caféine", M(C=8, H=10, N=4, O=2), 194.0, 1e-9)
verifie("ex1 M glucose", M(C=6, H=12, O=6), 180.0, 1e-9)
verifie("ex1 M aspirine", M(C=9, H=8, O=4), 180.0, 1e-9)
verifie("ex1 M ion sulfate", M(S=1, O=4), 96.1, 1e-9)
verifie("ex1 M ammoniac", M(N=1, H=3), 17.0, 1e-9)
# Exercice 2
verifie("ex2 n carbone 0,200 g (mol)", 0.200 / 12.0, 0.0167, 0.00005)
verifie("ex2 N carbone", 0.200 / 12.0 * NA, 1.00e22, 0.005e22)
verifie("ex2 n or 5,0 g (mol)", 5.0 / 197.0, 0.0254, 0.00005)
verifie("ex2 N or", 5.0 / 197.0 * NA, 1.53e22, 0.005e22)
verifie("ex2 masse d'un atome de carbone (g)", 12.0 / NA, 1.99e-23, 0.005e-23)
# Exercice 3
m3 = 25.0 * 0.789
verifie("ex3 masse d'éthanol (g)", m3, 19.7, 0.05)
verifie("ex3 M éthanol", M(C=2, H=6, O=1), 46.0, 1e-9)
verifie("ex3 n éthanol (mol)", m3 / 46.0, 0.429, 0.0005)
verifie("ex3 N éthanol", m3 / 46.0 * NA, 2.58e23, 0.005e23)
verifie("ex3 volume d'une mole (mL)", 46.0 / 0.789, 58.3, 0.05)
# Exercice 4
verifie("ex4 n gaz 4,8 L (mol)", 4.8 / VM, 0.20, 1e-9)
verifie("ex4 m hélium (g)", 0.20 * 4.0, 0.80, 1e-9)
verifie("ex4 m dioxyde de carbone (g)", 0.20 * 44.0, 8.8, 1e-9)
verifie("ex4 m air (g)", 0.20 * 29.0, 5.8, 1e-9)
# Exercice 5
verifie("ex5 concentration en masse (g/L)", 0.9 / 0.100, 9.0, 1e-9)
verifie("ex5 c NaCl (mol/L)", 9.0 / 58.5, 0.154, 0.0005)
verifie("ex5 m dans 500 mL (g)", 9.0 * 0.500, 4.5, 1e-9)
verifie("ex5 n dans 500 mL (mol)", 4.5 / 58.5, 0.0769, 0.00005)
verifie("ex5 N ions sodium", 4.5 / 58.5 * NA, 4.63e22, 0.005e22)
# Exercice 6
M6 = M(Cu=1, S=1, O=4) + 5 * M(H=2, O=1)
verifie("ex6 M sulfate de cuivre pentahydraté", M6, 249.6, 1e-9)
verifie("ex6 n (mol)", 0.0400 * 0.2500, 1.00e-2, 1e-12)
verifie("ex6 m à peser (g)", 0.0400 * 0.2500 * M6, 2.50, 0.005)
verifie("ex6 concentration en masse (g/L)", 0.0400 * M6, 9.98, 0.005)
# Exercice 7
verifie("ex7 facteur de dilution", 0.0400 / 2.00e-3, 20, 1e-9)
verifie("ex7 volume prélevé (mL)", 100.0 / 20, 5.00, 1e-9)
verifie("ex7 concentration en masse de S1 (g/L)", 2.00e-3 * M6, 0.499, 0.0005)
# Exercice 8
m8 = 125 * 0.789
verifie("ex8 masse d'éthanol par litre (g)", m8, 98.6, 0.05)
verifie("ex8 c éthanol (mol/L)", m8 / 46.0, 2.14, 0.005)
verifie("ex8 verre de vin 10 cL (g)", 100 * 0.125 * 0.789, 9.9, 0.05)
verifie("ex8 bière 5 % 25 cL (g)", 250 * 0.05 * 0.789, 9.9, 0.05)
verifie("ex8 whisky 40 % 3 cL (g)", 30 * 0.40 * 0.789, 9.5, 0.05)
# Exercice 9
verifie("ex9 c magnésium (mol/L)", 0.119 / 24.3, 4.90e-3, 0.005e-3)
verifie("ex9 c calcium (mol/L)", 0.549 / 40.1, 1.37e-2, 0.005e-2)
verifie("ex9 n magnésium dans 20 cL (mol)", 0.119 * 0.20 / 24.3, 9.79e-4, 0.005e-4)
verifie("ex9 N ions magnésium dans 20 cL", 0.119 * 0.20 / 24.3 * NA, 5.90e20, 0.005e20)
verifie("ex9 volume pour 300 mg (L)", 300 / 119, 2.5, 0.05)
# Exercice 10
V10 = 8.0 * 7.0 * 3.0
verifie("ex10 volume de la salle (m3)", V10, 168, 1e-9)
n10 = V10 * 1000 / VM
verifie("ex10 n air (mol)", n10, 7.00e3, 0.005e3)
verifie("ex10 n dioxygène (mol)", 0.21 * n10, 1.47e3, 0.005e3)
verifie("ex10 m dioxygène (kg)", 0.21 * n10 * 32.0 / 1000, 47.0, 0.05)
verifie("ex10 n diazote (mol)", 0.78 * n10, 5.46e3, 0.005e3)
verifie("ex10 m diazote (kg)", 0.78 * n10 * 28.0 / 1000, 153, 0.5)
verifie("ex10 volume de CO2 produit en 1 h (L)", 30 * 12, 360, 1e-9)
verifie("ex10 n CO2 (mol)", 360 / VM, 15, 1e-9)
verifie("ex10 part de CO2 ajoutée (%)", 100 * 360 / (V10 * 1000), 0.21, 0.005)
verifie("ex10 part de CO2 ajoutée (ppm)", 1e6 * 360 / (V10 * 1000), 2.1e3, 0.05e3)
# Exercice 11
verifie("ex11 M glucose", M(C=6, H=12, O=6), 180.0, 1e-9)
verifie("ex11 M paracétamol", M(C=8, H=9, N=1, O=2), 151.0, 1e-9)
verifie("ex11 n caféine (mol)", 0.080 / 194.0, 4.12e-4, 0.005e-4)
verifie("ex11 paracétamol sans l'azote", M(C=8, H=9, O=2), 137.0, 1e-9)
verifie("ex2 rapport des nombres d'atomes", (5.0 / 197.0) / (0.200 / 12.0), 1.5, 0.05)
verifie("ex2 rapport des masses", 5.0 / 0.200, 25, 1e-9)
verifie("ex14 deux ampoules (mmol/L)", 2 * 13.4 / 0.520, 51.5, 0.05)
verifie("ex14 nombre maximal d'ampoules", 20 / (13.4 - 0.4), 1.5, 0.05)
verifie("ex15 part des atomes d'or avec valeurs arrondies (%)", 100 * 1.52 / 2.77, 55, 0.5)
# Exercice 12
verifie("ex12 glycémie (g/L)", 7.8e-3 * 180.0, 1.40, 0.005)
verifie("ex12 borne basse (mmol/L)", 0.70 / 180.0 * 1000, 3.9, 0.05)
verifie("ex12 borne haute (mmol/L)", 1.10 / 180.0 * 1000, 6.1, 0.05)
verifie("ex12 seuil du diabète (mmol/L)", 1.26 / 180.0 * 1000, 7.0, 0.05)
verifie("ex12 glucose dans 5,0 L (g)", 1.40 * 5.0, 7.0, 1e-9)
verifie("ex12 glucose à 1,10 g/L (g)", 1.10 * 5.0, 5.5, 1e-9)
verifie("ex12 excès de glucose (g)", 1.40 * 5.0 - 1.10 * 5.0, 1.5, 1e-9)
verifie("ex12 fraction d'un morceau de sucre", 1.5 / 6, 0.25, 1e-9)
# Exercice 13
n13 = 5600 / 2.0
verifie("ex13 n dihydrogène (mol)", n13, 2800, 1e-9)
verifie("ex13 volume à 20 °C et 1013 hPa (L)", n13 * VM, 67200, 1e-9)
verifie("ex13 rapport des volumes", n13 * VM / 142, 473, 0.5)
verifie("ex13 N molécules", n13 * NA, 1.69e27, 0.005e27)
verifie("ex13 n pour 100 km (mol)", 800 / 2.0, 400, 1e-9)
verifie("ex13 volume pour 100 km (L)", 800 / 2.0 * VM, 9600, 1e-9)
verifie("ex13 autonomie (km)", 5.6 / 0.8 * 100, 700, 1e-9)
# Exercice 14
verifie("ex14 masse de glucose (g)", 50 * 0.500, 25, 1e-9)
verifie("ex14 n glucose (mol)", 25 / 180.0, 0.139, 0.0005)
verifie("ex14 M KCl", M(K=1, Cl=1), 74.6, 1e-9)
verifie("ex14 n KCl (mmol)", 1000 * 1.0 / 74.6, 13.4, 0.05)
verifie("ex14 c ions potassium (mol/L)", 1.0 / 74.6 / 0.510, 0.0263, 0.00005)
verifie("ex14 concentration en masse du glucose après ajout (g/L)", 25 / 0.510, 49.0, 0.05)
# Exercice 15
mAu, mAg, mCu = 0.75 * 4.0, 0.125 * 4.0, 0.125 * 4.0
nAu, nAg, nCu = mAu / 197.0, mAg / 107.9, mCu / 63.5
nt = nAu + nAg + nCu
verifie("ex15 masse d'or (g)", mAu, 3.0, 1e-9)
verifie("ex15 n or (mol)", nAu, 1.52e-2, 0.005e-2)
verifie("ex15 n argent (mol)", nAg, 4.63e-3, 0.005e-3)
verifie("ex15 n cuivre (mol)", nCu, 7.87e-3, 0.005e-3)
verifie("ex15 n total (mol)", nt, 2.77e-2, 0.005e-2)
verifie("ex15 part des atomes d'or (%)", 100 * nAu / nt, 55, 0.5)
verifie("ex15 part des atomes d'argent (%)", 100 * nAg / nt, 17, 0.5)
verifie("ex15 part des atomes de cuivre (%)", 100 * nCu / nt, 28, 0.5)
verifie("ex15 or 18 carats", 24 * 0.75, 18, 1e-9)
# Défi D01
n_atm = 5.1e21 / 29
verifie("D01 n air de l'atmosphère (mol)", n_atm, 1.76e20, 0.005e20)
verifie("D01 N molécules de l'atmosphère", n_atm * NA, 1.06e44, 0.005e44)
n_souffle = 0.50 / VM
verifie("D01 n d'une inspiration (mol)", n_souffle, 2.08e-2, 0.005e-2)
verifie("D01 N d'une inspiration", n_souffle * NA, 1.25e22, 0.005e22)
verifie("D01 nombre d'inspirations dans l'atmosphère", n_atm / n_souffle, 8.4e21, 0.05e21)
verifie("D01 fraction de l'atmosphère", n_souffle / n_atm, 1.18e-22, 0.005e-22)
verifie("D01 molécules du dernier souffle par inspiration", n_souffle * NA * n_souffle / n_atm, 1.5, 0.05)
verifie("D01 inspirations en une heure", 15 * 60, 900, 1e-9)
verifie("D01 molécules de César en une heure", 1.5 * 900, 1.3e3, 0.05e3)
verifie("D01 molécules de diazote seules", 0.78 * 1.5, 1.2, 0.05)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 1 et du défi D01 sont vérifiées.")
