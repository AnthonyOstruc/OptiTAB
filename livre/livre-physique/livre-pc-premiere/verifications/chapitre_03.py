"""Vérification des résultats du chapitre 3 (réactions d'oxydoréduction) et du défi D03.

Conservation des éléments et des charges de toutes les équations publiées, puis valeurs numériques.
Lancer : python -I -X utf8 verifications/chapitre_03.py
"""
import io
import re
from contextlib import redirect_stdout

ECHECS = []
VM = 24.0


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


def espece(formule):
    """Composition et charge d'une espèce : MnO4-, Fe^2+, Cr2O7^2-, e-, CH3CH2OH (charge multiple après ^)."""
    charge = 0
    if formule == 'e-':
        return {}, -1
    m = re.match(r'^(.*?)\^(\d+)([+-])$', formule)
    if m:
        formule, n, signe = m.groups()
        charge = int(n) * (1 if signe == '+' else -1)
    elif formule[-1] in '+-':
        charge = 1 if formule[-1] == '+' else -1
        formule = formule[:-1]
    compo = {}
    for el, nb in re.findall(r'([A-Z][a-z]?)(\d*)', formule):
        compo[el] = compo.get(el, 0) + (int(nb) if nb else 1)
    return compo, charge


def cote(texte):
    atomes, charge = {}, 0
    for terme in texte.split(' + '):
        m = re.match(r'^(\d*)\s*(.+)$', terme.strip())
        coef = int(m.group(1)) if m.group(1) else 1
        compo, z = espece(m.group(2))
        charge += coef * z
        for el, nb in compo.items():
            atomes[el] = atomes.get(el, 0) + coef * nb
    return atomes, charge


def equilibree(nom, equation):
    gauche, droite = re.split(r'\s*(?:->|=)\s*', equation)
    ag, cg = cote(gauche)
    ad, cd = cote(droite)
    ok = ag == ad and cg == cd
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} {equation}")
    if not ok:
        ECHECS.append(nom)


EQUATIONS = {
    'cours demi-équation cuivre': 'Cu^2+ + 2 e- = Cu',
    'cours demi-équation permanganate': 'MnO4- + 8 H+ + 5 e- = Mn^2+ + 4 H2O',
    'cours zinc et ions cuivre': 'Zn + Cu^2+ -> Zn^2+ + Cu',
    'cours permanganate et ions fer(II)': 'MnO4- + 8 H+ + 5 Fe^2+ -> Mn^2+ + 5 Fe^3+ + 4 H2O',
    'ex1 argent': 'Ag+ + e- = Ag',
    'ex1 fer(III)/fer(II)': 'Fe^3+ + e- = Fe^2+',
    'ex1 aluminium': 'Al^3+ + 3 e- = Al',
    'ex1 diiode': 'I2 + 2 e- = 2 I-',
    'ex1 dichlore': 'Cl2 + 2 e- = 2 Cl-',
    'ex2 dichromate': 'Cr2O7^2- + 14 H+ + 6 e- = 2 Cr^3+ + 7 H2O',
    'ex2 dioxygène/eau': 'O2 + 4 H+ + 4 e- = 2 H2O',
    'ex2 eau oxygénée/eau': 'H2O2 + 2 H+ + 2 e- = 2 H2O',
    'ex2 nitrate/monoxyde d azote': 'NO3- + 4 H+ + 3 e- = NO + 2 H2O',
    'ex2 dioxygène/eau oxygénée': 'O2 + 2 H+ + 2 e- = H2O2',
    'ex3 arbre de Diane': 'Cu + 2 Ag+ -> Cu^2+ + 2 Ag',
    'ex4 zinc et acide': 'Zn + 2 H+ -> Zn^2+ + H2',
    'ex5 fer et ions cuivre': 'Fe + Cu^2+ -> Fe^2+ + Cu',
    'ex6a permanganate et fer(II)': 'MnO4- + 8 H+ + 5 Fe^2+ -> Mn^2+ + 5 Fe^3+ + 4 H2O',
    'ex6b tétrathionate': 'S4O6^2- + 2 e- = 2 S2O3^2-',
    'ex6b diiode et thiosulfate': 'I2 + 2 S2O3^2- -> 2 I- + S4O6^2-',
    'ex6c eau oxygénée et iodure': 'H2O2 + 2 I- + 2 H+ -> I2 + 2 H2O',
    'ex7 acide éthanoïque/éthanol': 'CH3COOH + 4 H+ + 4 e- = CH3CH2OH + H2O',
    'ex7 alcootest': '2 Cr2O7^2- + 3 CH3CH2OH + 16 H+ -> 4 Cr^3+ + 3 CH3COOH + 11 H2O',
    'ex8 sulfure d argent': 'Ag2S + 2 e- = 2 Ag + S^2-',
    'ex8 argenterie': '3 Ag2S + 2 Al -> 6 Ag + 2 Al^3+ + 3 S^2-',
    'ex10 vitamine C': 'C6H6O6 + 2 H+ + 2 e- = C6H8O6',
    'ex10 vitamine C et diiode': 'C6H8O6 + I2 -> C6H6O6 + 2 I- + 2 H+',
    'ex10 vitamine C et dioxygène': '2 C6H8O6 + O2 -> 2 C6H6O6 + 2 H2O',
    'ex11 hypochlorite/dichlore': '2 ClO- + 4 H+ + 2 e- = Cl2 + 2 H2O',
    'ex11 javel et acide': 'ClO- + Cl- + 2 H+ -> Cl2 + H2O',
    'ex12 dioxygène et fer': '2 Fe + O2 + 4 H+ -> 2 Fe^2+ + 2 H2O',
    'ex12 dioxygène et zinc': '2 Zn + O2 + 4 H+ -> 2 Zn^2+ + 2 H2O',
    'ex13 dismutation': '2 H2O2 -> 2 H2O + O2',
    'ex14 zinc et ions argent': 'Zn + 2 Ag+ -> Zn^2+ + 2 Ag',
    'ex15 métal et acide': 'Zn + 2 H+ -> Zn^2+ + H2',
}
for nom, eq in EQUATIONS.items():
    equilibree(nom, eq)


def programme_cours():
    especes = {'MnO4-': ({'Mn': 1, 'O': 4}, -1), 'H+': ({'H': 1}, 1),
               'Fe2+': ({'Fe': 1}, 2), 'Mn2+': ({'Mn': 1}, 2),
               'Fe3+': ({'Fe': 1}, 3), 'H2O': ({'H': 2, 'O': 1}, 0)}
    reactifs = {'MnO4-': 1, 'H+': 8, 'Fe2+': 5}
    produits = {'Mn2+': 1, 'Fe3+': 5, 'H2O': 4}

    def bilan(cote_):
        atomes, charge = {}, 0
        for nom, coef in cote_.items():
            composition, z = especes[nom]
            charge = charge + coef * z
            for el, nb in composition.items():
                atomes[el] = atomes.get(el, 0) + coef * nb
        return atomes, charge

    print(bilan(reactifs))
    print(bilan(produits))


s = sortie_de(programme_cours).replace('\n', ' | ')
print('   cours programme :', s)
if s != "({'Mn': 1, 'O': 4, 'H': 8, 'Fe': 5}, 17) | ({'Mn': 1, 'Fe': 5, 'H': 8, 'O': 4}, 17)":
    ECHECS.append('cours programme')


# Exercice 9 : même fonction bilan, dictionnaires modifiés
def bilan_avec(especes, cote_):
    atomes, charge = {}, 0
    for nom, coef in cote_.items():
        composition, z = especes[nom]
        charge = charge + coef * z
        for el, nb in composition.items():
            atomes[el] = atomes.get(el, 0) + coef * nb
    return atomes, charge


esp9 = {'MnO4-': ({'Mn': 1, 'O': 4}, -1), 'H+': ({'H': 1}, 1), 'Fe2+': ({'Fe': 1}, 2)}
s9 = str(bilan_avec(esp9, {'MnO4-': 1, 'H+': 4, 'Fe2+': 5}))
print('   ex9 H+ = 4 :', s9)
if s9 != "({'Mn': 1, 'O': 4, 'H': 4, 'Fe': 5}, 13)":
    ECHECS.append('ex9 H+ = 4')
esp9 = {'Zn': ({'Zn': 1}, 0), 'Cu2+': ({'Cu': 1}, 2), 'Zn2+': ({'Zn': 1}, 2), 'Cu': ({'Cu': 1}, 0)}
r9, p9 = str(bilan_avec(esp9, {'Zn': 1, 'Cu2+': 1})), str(bilan_avec(esp9, {'Zn2+': 1, 'Cu': 1}))
print('   ex9 zinc et cuivre :', r9, '|', p9)
if r9 != p9 or r9 != "({'Zn': 1, 'Cu': 1}, 2)":
    ECHECS.append('ex9 zinc et cuivre')
ga, ca = cote('Fe^3+ + Cu')
da, cda = cote('Fe^2+ + Cu^2+')
if not (ga == da and ca == 3 and cda == 4):
    ECHECS.append('ex9 contre-exemple')
equilibree('ex9 fer(III) et cuivre corrigée', '2 Fe^3+ + Cu -> 2 Fe^2+ + Cu^2+')
# Exercice 7 : décompte publié dans le corrigé
a7, c7 = cote('2 Cr2O7^2- + 3 CH3CH2OH + 16 H+')
if a7 != {'Cr': 4, 'O': 17, 'C': 6, 'H': 34} or c7 != 12:
    ECHECS.append('ex7 décompte')
print('   ex7 décompte :', a7, c7)
# Exercice 4
verifie("ex4 n zinc (mol)", 0.654 / 65.4, 1.00e-2, 1e-12)
verifie("ex4 volume de dihydrogène (L)", 0.654 / 65.4 * VM, 0.240, 1e-9)
# Exercice 8
M_Ag2S = 2 * 107.9 + 32.1
verifie("ex8 M(Ag2S)", M_Ag2S, 247.9, 1e-9)
n8 = 0.100 / M_Ag2S
verifie("ex8 n Ag2S (mol)", n8, 4.03e-4, 0.005e-4)
verifie("ex8 masse d'argent récupérée (g)", 2 * n8 * 107.9, 0.0871, 0.00005)
verifie("ex8 n aluminium (mol)", 2 / 3 * n8, 2.69e-4, 0.005e-4)
verifie("ex8 masse d'aluminium (mg)", 2 / 3 * n8 * 27.0 * 1000, 7.3, 0.05)
# Exercice 11
verifie("ex11 n ions hypochlorite (mol)", 0.37 * 0.100, 0.037, 1e-12)
verifie("ex11 volume de dichlore (L)", 0.037 * VM, 0.89, 0.005)
verifie("ex11 masse de dichlore (g)", 0.037 * 71.0, 2.6, 0.05)
verifie("ex11 chlore actif 2,6 % (mol/L)", 26 / 71.0, 0.37, 0.005)
# Exercice 12
n12 = 2000 / 65.4
verifie("ex12 n zinc (mol)", n12, 30.6, 0.05)
verifie("ex12 n électrons (mol)", 2 * n12, 61.2, 0.05)
verifie("ex12 masse de fer protégée (kg)", n12 * 55.8 / 1000, 1.71, 0.005)
# Exercice 13
nO2 = 10 / 22.4
verifie("ex13 n dioxygène par litre (mol)", nO2, 0.446, 0.0005)
verifie("ex13 c eau oxygénée (mol/L)", 2 * nO2, 0.893, 0.0005)
verifie("ex13 volume de dioxygène, flacon de 250 mL, 0 °C (L)", 10 * 0.250, 2.5, 1e-9)
verifie("ex13 volume de dioxygène à 20 °C (L)", nO2 * 0.250 * VM, 2.68, 0.005)
# Exercice 14
m14 = 5.0 * 2.0
verifie("ex14 masse d'argent dans le bain (g)", m14, 10, 1e-9)
verifie("ex14 n ions argent (mol)", m14 / 107.9, 0.0927, 0.00005)
verifie("ex14 n zinc (mol)", m14 / 107.9 / 2, 0.0463, 0.00005)
verifie("ex14 masse de zinc (g)", m14 / 107.9 / 2 * 65.4, 3.03, 0.005)
# Exercice 15
n15 = 0.096 / VM
verifie("ex15 n dihydrogène (mol)", n15, 4.0e-3, 1e-12)
verifie("ex15 masse molaire du métal (g/mol)", 0.262 / n15, 65.5, 0.05)
# Défi D03
nAg = 0.100 * 0.100
verifie("D03 n ions argent (mol)", nAg, 0.0100, 1e-12)
verifie("D03 n cuivre consommé (mol)", nAg / 2, 5.00e-3, 1e-12)
verifie("D03 masse de cuivre consommée (g)", nAg / 2 * 63.5, 0.318, 0.0005)
verifie("D03 masse d'argent déposée (g)", nAg * 107.9, 1.08, 0.005)
verifie("D03 prise de masse (g)", nAg * 107.9 - nAg / 2 * 63.5, 0.76, 0.005)
verifie("D03 masse de la tige à la fin (g)", 5.00 + nAg * 107.9 - nAg / 2 * 63.5, 5.76, 0.005)
verifie("D03 masse molaire équivalente (g/mol)", 2 * 107.9 - 63.5, 152.3, 1e-9)
verifie("D03 x à partir de la prise de masse 0,38 g (mol)", 0.38 / 152.3, 2.5e-3, 0.05e-3)
verifie("D03 c ions cuivre à la pesée de 5,38 g (mol/L)", 0.38 / 152.3 / 0.100, 0.025, 0.0005)
verifie("D03 c ions cuivre finale (mol/L)", nAg / 2 / 0.100, 0.0500, 1e-12)
verifie("D03 n ions argent pour tout le fil (mol)", 2 * 5.00 / 63.5, 0.157, 0.0005)
verifie("D03 n cuivre de la tige (mol)", 5.00 / 63.5, 0.0787, 0.00005)
verifie("D03 volume pour tout dissoudre (L)", 2 * 5.00 / 63.5 / 0.100, 1.57, 0.005)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les équations et valeurs du chapitre 3 et du défi D03 sont vérifiées.")
