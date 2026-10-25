"""Vérification du chapitre 9 (Synthèses organiques) et du défi D09.

Équations ajustées, masses molaires, quantités, rendements, sorties exactes des programmes Python.
Lancer : python -I -X utf8 verifications/chapitre_09.py
"""
import io
import math
import re
from contextlib import redirect_stdout

ECHECS = []
M = {'H': 1.0, 'C': 12.0, 'N': 14.0, 'O': 16.0, 'Na': 23.0}


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:62s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def compo(formule):
    res = {}
    for el, nb in re.findall(r'([A-Z][a-z]?)(\d*)', formule):
        res[el] = res.get(el, 0) + (int(nb) if nb else 1)
    return res


def mm(formule):
    return sum(M[el] * nb for el, nb in compo(formule).items())


def cote(texte):
    atomes = {}
    for terme in texte.split(' + '):
        m = re.match(r'^(\d*)\s*(.+)$', terme.strip())
        coef = int(m.group(1)) if m.group(1) else 1
        for el, nb in compo(m.group(2)).items():
            atomes[el] = atomes.get(el, 0) + coef * nb
    return atomes


def equilibree(nom, equation):
    g, d = re.split(r'\s*->\s*', equation)
    ok = cote(g) == cote(d)
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:62s} {equation}")
    if not ok:
        ECHECS.append(nom)


EQUATIONS = {
    'cours et ex7 aspirine': 'C7H6O3 + C4H6O3 -> C9H8O4 + C2H4O2',
    'ex5 et ex12 acétate d isoamyle': 'C2H4O2 + C5H12O -> C7H14O2 + H2O',
    'ex11 paracétamol': 'C6H7NO + C4H6O3 -> C8H9NO2 + C2H4O2',
    'ex13 saponification de l oléine': 'C57H104O6 + 3 NaOH -> 3 C18H33O2Na + C3H8O3',
    'ex14 estérification': 'C2H4O2 + C2H6O -> C4H8O2 + H2O',
}
for nom, eq in EQUATIONS.items():
    equilibree(nom, eq)
# l'oxydation de l'alcool benzylique se vérifie avec ses demi-équations
equilibree('ex9 demi-équation (bilan atomique)', 'C7H6O2 + 4 H -> C7H8O + H2O')

for f, v in (('C7H6O3', 138.0), ('C4H6O3', 102.0), ('C9H8O4', 180.0), ('C7H14O2', 130.0), ('C5H12O', 88.0),
             ('C2H4O2', 60.0), ('C7H8O', 108.0), ('C7H6O2', 122.0), ('C6H7NO', 109.0), ('C8H9NO2', 151.0),
             ('C57H104O6', 884.0), ('C18H33O2Na', 304.0), ('NaOH', 40.0), ('C13H18O2', 206.0), ('C10H14', 134.0)):
    verifie(f'M({f})', mm(f), v, 1e-9)


def sortie_de(fonction):
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        fonction()
    return tampon.getvalue().strip()


def programme(reactifs, M_produit, m_obtenue):
    xmax = min(m / Mr / a for a, m, Mr in reactifs.values())
    m_max = xmax * M_produit
    print('xmax =', round(xmax, 5), 'mol ; m_max =', round(m_max, 2), 'g')
    print('rendement =', round(100 * m_obtenue / m_max, 1), '%')


ASPIRINE = {'acide salicylique': [1, 2.00, 138.0], 'anhydride ethanoique': [1, 5.40, 102.0]}
s = sortie_de(lambda: programme(ASPIRINE, 180.0, 2.15))
print('   cours programme :', s.replace('\n', ' | '))
if s != 'xmax = 0.01449 mol ; m_max = 2.61 g\nrendement = 82.4 %':
    ECHECS.append('cours programme')
s6 = sortie_de(lambda: programme(ASPIRINE, 180.0, 2.40))
print('   ex6 2,40 g :', s6.replace('\n', ' | '))
if s6 != 'xmax = 0.01449 mol ; m_max = 2.61 g\nrendement = 92.0 %':
    ECHECS.append('ex6 programme 2,40 g')
s6b = sortie_de(lambda: programme({'acide': [1, 21.0, 60.0], 'alcool': [1, 12.15, 88.0]}, 130.0, 10.9))
print('   ex6 ester :', s6b.replace('\n', ' | '))
if s6b != 'xmax = 0.13807 mol ; m_max = 17.95 g\nrendement = 60.7 %':
    ECHECS.append('ex6 programme ester')

# Cours : aspirine
n_sal = 2.00 / 138.0
verifie("cours n acide salicylique (mol)", n_sal, 1.45e-2, 0.005e-2)
verifie("cours n anhydride (mol)", 5.40 / 102.0, 5.29e-2, 0.005e-2)
verifie("cours masse d'anhydride (g) = 5,0 mL x 1,08", 5.0 * 1.08, 5.40, 1e-9)
verifie("cours m_max aspirine (g)", n_sal * 180.0, 2.61, 0.005)
verifie("cours rendement (%)", 2.15 / (n_sal * 180.0) * 100, 82, 0.5)
# Exercice 4 : CCM
verifie("ex4 Rf du produit", 3.0 / 6.0, 0.50, 1e-12)
verifie("ex4 Rf de l'impureté", 4.8 / 6.0, 0.80, 1e-12)
# Exercice 5 : ester
verifie("ex5 n ester (mol)", 9.1 / 130.0, 0.0700, 1e-12)
verifie("ex5 rendement (%)", 9.1 / 130.0 / 0.100 * 100, 70, 1e-9)
# Exercice 7 : aspirine et Kofler
verifie("ex7 masse de comprimés possibles (500 mg)", n_sal * 180.0 * 0.824 / 0.500, 4.3, 0.05)
# Exercice 8 : recristallisation
verifie("ex8 masse dissoute à 95 °C dans 100 mL (g)", 60 * 0.100, 6.0, 1e-12)
verifie("ex8 masse restant dissoute à 20 °C (g)", 3.0 * 0.100, 0.30, 1e-12)
verifie("ex8 masse maximale récupérée (g)", 5.0 - 0.30, 4.7, 1e-12)
verifie("ex8 volume minimal d'eau chaude (mL)", 5.0 / 60 * 1000, 83, 0.5)
# Exercice 9 : acide benzoïque
n9 = 2.0 * 1.04 / 108.0
verifie("ex9 masse d'alcool benzylique (g)", 2.0 * 1.04, 2.08, 1e-12)
verifie("ex9 n alcool benzylique (mol)", n9, 1.93e-2, 0.005e-2)
verifie("ex9 m_max acide benzoïque (g)", n9 * 122.0, 2.35, 0.005)
verifie("ex9 rendement (%)", 1.80 / (n9 * 122.0) * 100, 77, 0.5)
# Exercice 10 : distillation (températures d'ébullition publiées)
teb = {'propanone': 56, 'éthanol': 78, 'eau': 100}
if not teb['propanone'] < teb['éthanol'] < teb['eau']:
    ECHECS.append('ex10 ordre')
# Exercice 11 : paracétamol
n11 = 3.00 / 109.0
verifie("ex11 n 4-aminophénol (mol)", n11, 2.75e-2, 0.005e-2)
verifie("ex11 m_max paracétamol (g)", n11 * 151.0, 4.16, 0.005)
verifie("ex11 rendement (%)", 3.20 / (n11 * 151.0) * 100, 77, 0.5)
# Exercice 12 : acétate d'isoamyle
n_alc = 15.0 * 0.81 / 88.0
n_ac = 20.0 * 1.05 / 60.0
verifie("ex12 masse d'alcool (g)", 15.0 * 0.81, 12.15, 1e-9)
verifie("ex12 n alcool (mol)", n_alc, 0.138, 0.0005)
verifie("ex12 n acide (mol)", n_ac, 0.350, 1e-9)
verifie("ex12 m_max ester (g)", n_alc * 130.0, 17.9, 0.05)
verifie("ex12 masse d'ester obtenue (g)", 12.5 * 0.87, 10.9, 0.05)
verifie("ex12 rendement (%)", 12.5 * 0.87 / (n_alc * 130.0) * 100, 61, 0.5)
# Exercice 13 : savon à froid
n_huile = 500 / 884.0
verifie("ex13 n oléine (mol)", n_huile, 0.566, 0.0005)
verifie("ex13 masse de soude stœchiométrique (g)", 3 * n_huile * 40.0, 67.9, 0.05)
verifie("ex13 masse de soude avec 5 % de surgras (g)", 3 * n_huile * 40.0 * 0.95, 64.5, 0.05)
verifie("ex13 masse de savon maximale (g)", 3 * n_huile * 304.0, 516, 0.5)
verifie("ex13 masse de glycérol (g)", n_huile * 92.0, 52.0, 0.05)
verifie("ex13 M(C3H8O3)", mm('C3H8O3'), 92.0, 1e-9)


# Exercice 14 : estérification, K = 4 (données publiées : rendements)
def x_eq(r):
    a, b, c = 3, -4 * (1 + r), 4 * r
    return (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)


verifie("ex14 rendement 1 : 1 (%)", 100 * x_eq(1), 67, 0.5)
verifie("ex14 rendement 2 : 1 (%)", 100 * x_eq(2), 85, 0.5)
verifie("ex14 rendement 3 : 1 (%)", 100 * x_eq(3), 90, 0.5)
# Exercice 15 : comprimés
n_asp = 20 * 0.500 / 180.0
verifie("ex15 n aspirine pour 20 comprimés (mol)", n_asp, 0.0556, 0.00005)
verifie("ex15 n acide salicylique à 80 % (mol)", n_asp / 0.80, 0.0694, 0.00005)
verifie("ex15 masse d'acide salicylique (g)", n_asp / 0.80 * 138.0, 9.58, 0.005)

# Défi D09 : ibuprofène
for n_et, r, pub in ((6, 0.90, 53), (3, 0.90, 73), (6, 0.95, 74), (3, 0.95, 86)):
    verifie(f"D09 rendement global {n_et} étapes à {r}", 100 * r ** n_et, pub, 0.5)
verifie("D09 économie d'atomes BHC (%)", 100 * 206.0 / (134.0 + 102.0 + 2.0 + 28.0), 77, 0.5)
verifie("D09 masse des réactifs BHC (g/mol)", 134.0 + 102.0 + 2.0 + 28.0, 266.0, 1e-9)
verifie("D09 déchets théoriques Boots par kg (kg)", 1 / 0.40 - 1, 1.5, 1e-12)
verifie("D09 déchets théoriques BHC par kg (kg)", 266.0 / 206.0 - 1, 0.29, 0.005)
verifie("D09 masse de réactifs Boots pour 1 kg avec 6 x 90 % (kg)", 1 / 0.40 / 0.9 ** 6, 4.7, 0.05)
verifie("D09 masse de réactifs BHC pour 1 kg avec 3 x 90 % (kg)", 266.0 / 206.0 / 0.9 ** 3, 1.77, 0.005)


def programme_defi():
    for etapes in [3, 6, 10]:
        print(etapes, round(0.90 ** etapes * 100), '%')


sd = sortie_de(programme_defi)
print('   D09 programme :', sd.replace('\n', ' | '))
if sd != '3 73 %\n6 53 %\n10 35 %':
    ECHECS.append('D09 programme')

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les équations, sorties de programmes et valeurs du chapitre 9 et du défi D09 sont vérifiées.")
