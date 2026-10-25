"""Vérification du chapitre 4 (Avancement et bilan de matière) et du défi D04.

Conservation des éléments dans les équations publiées, sorties exactes des programmes Python, puis valeurs numériques.
Lancer : python -I -X utf8 verifications/chapitre_04.py
"""
import io
import re
from contextlib import redirect_stdout

ECHECS = []
VM = 24.0
M = {'H': 1.0, 'C': 12.0, 'N': 14.0, 'O': 16.0, 'Na': 23.0, 'Al': 27.0, 'S': 32.1, 'Cl': 35.5, 'K': 39.1,
     'Ca': 40.1, 'Fe': 55.8, 'Cu': 63.5, 'Zn': 65.4, 'Ag': 107.9}


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def compo(formule):
    """Composition d'une formule simple, avec une parenthèse éventuelle : Ca(OH)2, CH3COOH, Fe3O4."""
    res = {}
    for groupe, mult, reste in re.findall(r'\(([^)]*)\)(\d*)|([A-Z][a-z]?\d*)', formule):
        if groupe:
            for el, nb in compo(groupe).items():
                res[el] = res.get(el, 0) + nb * (int(mult) if mult else 1)
        else:
            el, nb = re.match(r'([A-Z][a-z]?)(\d*)', reste).groups()
            res[el] = res.get(el, 0) + (int(nb) if nb else 1)
    return res


def masse_molaire(formule):
    return sum(M[el] * nb for el, nb in compo(formule).items())


def espece(formule):
    charge = 0
    m = re.match(r'^(.*?)\^(\d+)([+-])$', formule)
    if m:
        formule, n, signe = m.groups()
        charge = int(n) * (1 if signe == '+' else -1)
    elif formule[-1] in '+-':
        charge = 1 if formule[-1] == '+' else -1
        formule = formule[:-1]
    return compo(formule), charge


def cote(texte):
    atomes, charge = {}, 0
    for terme in texte.split(' + '):
        m = re.match(r'^(\d*)\s*(.+)$', terme.strip())
        coef = int(m.group(1)) if m.group(1) else 1
        c, z = espece(m.group(2))
        charge += coef * z
        for el, nb in c.items():
            atomes[el] = atomes.get(el, 0) + coef * nb
    return atomes, charge


def equilibree(nom, equation):
    gauche, droite = re.split(r'\s*->\s*', equation)
    ok = cote(gauche) == cote(droite)
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} {equation}")
    if not ok:
        ECHECS.append(nom)


EQUATIONS = {
    'cours combustion du méthane': 'CH4 + 2 O2 -> CO2 + 2 H2O',
    'cours estérification': 'CH3COOH + C2H6O -> C4H8O2 + H2O',
    'ex1 synthèse de l eau': '2 H2 + O2 -> 2 H2O',
    'ex2 fer et soufre': 'Fe + S -> FeS',
    'cours magnésium et acide (expérience)': 'Mg + 2 H+ -> Mg^2+ + H2',
    'ex3 combustion du magnésium': '2 Mg + O2 -> 2 MgO',
    'ex13 synthèse de l ammoniac': 'N2 + 3 H2 -> 2 NH3',
    'ex4 combustion du propane': 'C3H8 + 5 O2 -> 3 CO2 + 4 H2O',
    'ex7 airbag': '2 NaN3 -> 2 Na + 3 N2',
    'ex7 airbag, seconde réaction': '10 Na + 2 KNO3 -> K2O + 5 Na2O + N2',
    'ex8 aluminothermie': '2 Al + Fe2O3 -> Al2O3 + 2 Fe',
    'ex9 vinaigre et bicarbonate': 'CH3COOH + HCO3- -> CH3COO- + CO2 + H2O',
    'ex10 chlorure d argent': 'Ag+ + Cl- -> AgCl',
    'ex11 zinc et ions cuivre': 'Zn + Cu^2+ -> Zn^2+ + Cu',
    'ex12 combustion du butane': '2 C4H10 + 13 O2 -> 8 CO2 + 10 H2O',
    'ex14 carbure de calcium': 'CaC2 + 2 H2O -> C2H2 + Ca(OH)2',
    'ex14 combustion de l acétylène': '2 C2H2 + 5 O2 -> 4 CO2 + 2 H2O',
    'ex15 combustion du fer': '3 Fe + 2 O2 -> Fe3O4',
    'D04 combustion de l octane': '2 C8H18 + 25 O2 -> 16 CO2 + 18 H2O',
}
for nom, eq in EQUATIONS.items():
    equilibree(nom, eq)


def sortie_de(fonction):
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        fonction()
    return tampon.getvalue().strip()


def etat_final(reactifs, produits):
    """Programme du cours (capacité numérique), recopié à l'identique."""
    candidats = [n0 / a for a, n0 in reactifs.values()]
    xmax = min(candidats)
    print('xmax =', round(xmax, 4), 'mol')
    for espece_, (a, n0) in reactifs.items():
        print(espece_, round(n0 - a * xmax, 4), 'mol')
    for espece_, (c, n0) in produits.items():
        print(espece_, round(n0 + c * xmax, 4), 'mol')


def compare(nom, obtenu, attendu):
    ok = obtenu == attendu
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} {obtenu.replace(chr(10), ' | ')}")
    if not ok:
        print('      attendu :', attendu.replace('\n', ' | '))
        ECHECS.append(nom)


compare('cours programme état final', sortie_de(lambda: etat_final(
    {'CH4': [1, 0.040], 'O2': [2, 0.100]}, {'CO2': [1, 0.0], 'H2O': [2, 0.0]})),
    'xmax = 0.04 mol\nCH4 0.0 mol\nO2 0.02 mol\nCO2 0.04 mol\nH2O 0.08 mol')
compare('ex6 candidats', str([n0 / a for a, n0 in {'CH4': [1, 0.040], 'O2': [2, 0.100]}.values()]), '[0.04, 0.05]')
compare('ex6 dioxygène 0,060 mol', sortie_de(lambda: etat_final(
    {'CH4': [1, 0.040], 'O2': [2, 0.060]}, {'CO2': [1, 0.0], 'H2O': [2, 0.0]})),
    'xmax = 0.03 mol\nCH4 0.01 mol\nO2 0.0 mol\nCO2 0.03 mol\nH2O 0.06 mol')
compare('ex6 fer et soufre', sortie_de(lambda: etat_final(
    {'Fe': [1, 0.100], 'S': [1, 0.080]}, {'FeS': [1, 0.0]})),
    'xmax = 0.08 mol\nFe 0.02 mol\nS 0.0 mol\nFeS 0.08 mol')
compare('D04 lambda 0,90', sortie_de(lambda: etat_final(
    {'C8H18': [2, 1.0], 'O2': [25, 11.25]}, {'CO2': [16, 0.0], 'H2O': [18, 0.0]})),
    'xmax = 0.45 mol\nC8H18 0.1 mol\nO2 0.0 mol\nCO2 7.2 mol\nH2O 8.1 mol')
compare('D04 lambda 1,10', sortie_de(lambda: etat_final(
    {'C8H18': [2, 1.0], 'O2': [25, 13.75]}, {'CO2': [16, 0.0], 'H2O': [18, 0.0]})),
    'xmax = 0.5 mol\nC8H18 0.0 mol\nO2 1.25 mol\nCO2 8.0 mol\nH2O 9.0 mol')

# Masses molaires utilisées
for f, v in (('C3H8', 44.0), ('NaN3', 65.0), ('KNO3', 101.1), ('Fe2O3', 159.6), ('Al2O3', 102.0), ('NaHCO3', 84.0),
             ('CH3COOH', 60.0), ('CO2', 44.0), ('AgCl', 143.4), ('C4H10', 58.0), ('CaC2', 64.1), ('Fe3O4', 231.4),
             ('C8H18', 114.0), ('FeS', 87.9), ('C4H8O2', 88.0), ('H2O', 18.0)):
    verifie(f'M({f})', masse_molaire(f), v, 1e-9)

# Cours : combustion du méthane
verifie("cours xmax (mol)", min(0.040 / 1, 0.100 / 2), 0.040, 1e-12)
verifie("cours dioxygène restant (mol)", 0.100 - 2 * 0.040, 0.020, 1e-12)
verifie("cours mélange stœchiométrique, dioxygène (mol)", 2 * 0.040, 0.080, 1e-12)
# Expérience des ballons : Mg + 2 H+ -> Mg2+ + H2, 50 mL d'acide à 0,20 mol/L
nH = 0.050 * 0.20
for m, v in ((0.05, 50), (0.10, 100), (0.15, 120), (0.20, 120)):
    x = min(m / 24.3, nH / 2)
    verifie(f"expérience ballon {m} g de magnésium (mL)", x * VM * 1000, v, 1.5)
verifie("expérience masse de magnésium stœchiométrique (g)", nH / 2 * 24.3, 0.12, 0.005)
# Exercice 1 (en nombre de molécules)
verifie("ex1 xmax (molécules)", min(6 / 2, 4 / 1), 3, 0)
verifie("ex1 dioxygène restant (molécules)", 4 - 3, 1, 0)
verifie("ex1 eau formée (molécules)", 2 * 3, 6, 0)
# Exercice 2
verifie("ex2 masse de fer (g)", 0.100 * 55.8, 5.58, 1e-9)
verifie("ex2 masse de soufre (g)", 0.080 * 32.1, 2.57, 0.005)
verifie("ex2 fer restant (g)", 0.020 * 55.8, 1.12, 0.005)
verifie("ex2 sulfure de fer (g)", 0.080 * 87.9, 7.03, 0.005)
verifie("ex2 conservation de la masse (g)", 0.100 * 55.8 + 0.080 * 32.1 - 0.020 * 55.8 - 0.080 * 87.9, 0, 1e-9)
# Exercice 3 : 2 Mg + O2 -> 2 MgO
for nom, (mg, o2), (xm, lim) in (('A', (0.20, 0.10), (0.10, 'stœchiométrique')), ('B', (0.20, 0.20), (0.10, 'Mg')),
                                  ('C', (0.30, 0.10), (0.10, 'O2'))):
    verifie(f"ex3 mélange {nom} xmax (mol) [{lim}]", min(mg / 2, o2), xm, 1e-12)
    obtenu = 'stœchiométrique' if abs(mg / 2 - o2) < 1e-12 else ('Mg' if mg / 2 < o2 else 'O2')
    if obtenu != lim:
        ECHECS.append(f'ex3 limitant {nom}')
verifie("ex3 mélange B dioxygène restant (mol)", 0.20 - 0.10, 0.10, 1e-12)
verifie("ex3 mélange B oxyde formé (mol)", 2 * 0.10, 0.20, 1e-12)
verifie("ex3 mélange C magnésium restant (mol)", 0.30 - 2 * 0.10, 0.10, 1e-12)
# Exercice 4
n4 = 8.8 / 44.0
verifie("ex4 n propane (mol)", n4, 0.20, 1e-12)
verifie("ex4 n dioxygène (mol)", 5 * n4, 1.00, 1e-12)
verifie("ex4 volume de dioxygène (L)", 5 * n4 * VM, 24.0, 1e-9)
verifie("ex4 volume d'air (L)", 5 * n4 * VM / 0.21, 114, 0.5)
verifie("ex4 masse de dioxyde de carbone (g)", 3 * n4 * 44.0, 26.4, 1e-9)
# Exercice 5
verifie("ex5 masse d'ester (g)", 0.67 * 88.0, 59, 0.05)
# Exercice 7
n7 = 130 / 65.0
verifie("ex7 n azoture (mol)", n7, 2.00, 1e-12)
verifie("ex7 xmax (mol)", n7 / 2, 1.00, 1e-12)
verifie("ex7 n diazote (mol)", 3 * n7 / 2, 3.00, 1e-12)
verifie("ex7 volume de diazote (L)", 3 * n7 / 2 * VM, 72.0, 1e-9)
verifie("ex7 masse de sodium (g)", n7 * 23.0, 46.0, 1e-9)
verifie("ex7 n nitrate de potassium (mol)", n7 * 2 / 10, 0.400, 1e-12)
verifie("ex7 masse de nitrate de potassium (g)", n7 * 2 / 10 * 101.1, 40.4, 0.05)
# Exercice 8
verifie("ex8 n aluminium (mol)", 2700 / 27.0, 100, 1e-9)
verifie("ex8 n oxyde de fer (mol)", 7980 / 159.6, 50.0, 1e-9)
verifie("ex8 masse de fer (kg)", 100 * 55.8 / 1000, 5.58, 1e-9)
verifie("ex8 masse d'alumine (kg)", 50 * 102.0 / 1000, 5.10, 1e-9)
verifie("ex8 conservation de la masse (kg)", 2.70 + 7.98 - 5.58 - 5.10, 0, 1e-9)
# Exercice 9
n9b = 2.10 / 84.0
n9a = 50 / 60.0 * 0.0500
verifie("ex9 n hydrogénocarbonate (mol)", n9b, 0.0250, 1e-12)
verifie("ex9 c acide éthanoïque (mol/L)", 50 / 60.0, 0.833, 0.0005)
verifie("ex9 n acide éthanoïque (mol)", n9a, 4.17e-2, 0.005e-2)
verifie("ex9 masse maximale de CO2 (g)", n9b * 44.0, 1.10, 1e-9)
verifie("ex9 xf (mol)", 1.07 / 44.0, 0.0243, 0.00005)
verifie("ex9 xf / xmax", 1.07 / 44.0 / n9b, 0.97, 0.005)
# Exercice 10
verifie("ex10 n argent (mmol)", 20.0 * 0.050, 1.00, 1e-12)
verifie("ex10 n chlorure (mmol)", 10.0 * 0.080, 0.80, 1e-12)
verifie("ex10 masse de chlorure d'argent (g)", 0.80e-3 * 143.4, 0.115, 0.0005)
verifie("ex10 [Ag+] finale (mol/L)", 0.20e-3 / 0.0300, 6.7e-3, 0.05e-3)
verifie("ex10 [NO3-] finale (mol/L)", 1.00e-3 / 0.0300, 3.33e-2, 0.005e-2)
verifie("ex10 [Na+] finale (mol/L)", 0.80e-3 / 0.0300, 2.67e-2, 0.005e-2)
# Exercice 11
n11 = 0.0500 * 0.100
verifie("ex11 n0 ions cuivre (mmol)", n11 * 1000, 5.00, 1e-9)
verifie("ex11 nf ions cuivre (mmol)", 0.0500 * 0.040 * 1000, 2.00, 1e-9)
verifie("ex11 xf (mmol)", (n11 - 0.0500 * 0.040) * 1000, 3.00, 1e-9)
verifie("ex11 masse de zinc (g)", 3.00e-3 * 65.4, 0.196, 0.0005)
verifie("ex11 [Zn2+] finale (mol/L)", 3.00e-3 / 0.0500, 0.060, 1e-12)
# Exercice 12
n12 = 190 / 58.0
verifie("ex12 n butane (mol)", n12, 3.28, 0.005)
verifie("ex12 xmax (mol)", n12 / 2, 1.64, 0.005)
verifie("ex12 n dioxygène (mol)", 13 / 2 * n12, 21.3, 0.05)
verifie("ex12 volume de dioxygène (L)", 13 / 2 * n12 * VM, 511, 0.5)
verifie("ex12 volume d'air (m3)", 13 / 2 * n12 * VM / 0.21 / 1000, 2.43, 0.005)
verifie("ex12 masse de CO2 (g)", 4 * n12 * 44.0, 577, 0.5)
verifie("ex12 masse d'eau (g)", 5 * n12 * 18.0, 295, 0.5)
verifie("ex12 part du dioxygène de la tente consommée", 13 / 2 * n12 * VM / 1000 / 0.6, 0.85, 0.005)
verifie("ex12 dioxygène d'une tente de 3 m3 (m3)", 3 * 0.21, 0.6, 0.05)
# Exercice 13
verifie("ex13 xf (mol)", 0.30 / 2, 0.15, 1e-12)
verifie("ex13 diazote final (mol)", 1.00 - 0.15, 0.85, 1e-12)
verifie("ex13 dihydrogène final (mol)", 3.00 - 3 * 0.15, 2.55, 1e-12)
verifie("ex13 quantité totale de gaz (mol)", 0.85 + 2.55 + 0.30, 3.70, 1e-12)
k = 0
while 0.85 ** k > 0.10:
    k += 1
verifie("ex13 nombre de passages pour 90 %", k, 15, 0)
verifie("ex13 reste après 14 passages", 0.85 ** 14, 0.103, 0.0005)
verifie("ex13 reste après 15 passages", 0.85 ** 15, 0.087, 0.0005)
# Exercice 14
n14 = 100 / 64.1
verifie("ex14 n carbure (mol)", n14, 1.56, 0.005)
verifie("ex14 volume d'acétylène (L)", n14 * VM, 37.4, 0.05)
verifie("ex14 masse d'eau (g)", 2 * n14 * 18.0, 56.2, 0.05)
verifie("ex14 n dioxygène (mol)", 5 / 2 * n14, 3.90, 0.005)
verifie("ex14 volume de dioxygène (L)", 5 / 2 * n14 * VM, 93.6, 0.05)
verifie("ex14 autonomie (h)", n14 * VM / 12, 3.1, 0.05)
# Exercice 15
verifie("ex15 xmax (mol)", min(0.30 / 3, 0.25 / 2), 0.10, 1e-12)
verifie("ex15 dioxygène restant (mol)", 0.25 - 2 * 0.10, 0.05, 1e-12)
verifie("ex15 masse d'oxyde (g)", 0.10 * 231.4, 23.1, 0.05)
verifie("ex15 masse de fer initiale (g)", 0.30 * 55.8, 16.7, 0.05)
verifie("ex15 volume de dioxygène initial (L)", 0.25 * VM, 6.0, 1e-9)
# Défi D04
n_air = 12.5 / 0.21
verifie("D04 n dioxygène pour 1 mol d'octane", 25 / 2, 12.5, 0)
verifie("D04 n air (mol)", n_air, 59.5, 0.05)
verifie("D04 masse d'air (g)", n_air * 29.0, 1726, 0.5)
verifie("D04 rapport air/essence", n_air * 29.0 / 114.0, 15.1, 0.05)
verifie("D04 masse d'essence par km (g)", 0.060 * 750, 45.0, 1e-9)
verifie("D04 n octane par km (mol)", 45.0 / 114.0, 0.395, 0.0005)
verifie("D04 n CO2 par km (mol)", 8 * 45.0 / 114.0, 3.16, 0.005)
verifie("D04 masse de CO2 par km (g)", 8 * 45.0 / 114.0 * 44.0, 139, 0.5)
verifie("D04 CO2 par litre d'essence (kg)", 8 * 750 / 114.0 * 44.0 / 1000, 2.32, 0.005)
verifie("D04 octane imbrûlé à lambda 0,90", 1 - 0.90, 0.10, 1e-12)
verifie("D04 fraction de dioxygène en excès à lambda 1,10", 1.25 / 13.75, 0.091, 0.0005)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les équations, sorties de programmes et valeurs du chapitre 4 et du défi D04 sont vérifiées.")
