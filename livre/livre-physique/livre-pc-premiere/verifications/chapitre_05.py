"""Vérification du chapitre 5 (Titrages colorimétriques) et du défi D05.

Conservation des éléments et des charges dans les équations publiées, sortie exacte du programme Python, valeurs numériques.
Lancer : python -I -X utf8 verifications/chapitre_05.py
"""
import io
import re
from contextlib import redirect_stdout

ECHECS = []
M = {'H': 1.0, 'C': 12.0, 'O': 16.0, 'Na': 23.0, 'S': 32.1, 'Cl': 35.5, 'K': 39.1, 'Mn': 54.9, 'Fe': 55.8,
     'I': 126.9}


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def compo(formule):
    res = {}
    for el, nb in re.findall(r'([A-Z][a-z]?)(\d*)', formule):
        res[el] = res.get(el, 0) + (int(nb) if nb else 1)
    return res


def masse_molaire(formule):
    return sum(M[el] * nb for el, nb in compo(formule).items())


def espece(formule):
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
    gauche, droite = re.split(r'\s*(?:->|=)\s*', equation)
    ok = cote(gauche) == cote(droite)
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} {equation}")
    if not ok:
        ECHECS.append(nom)


EQUATIONS = {
    'cours permanganate et fer(II)': 'MnO4- + 8 H+ + 5 Fe^2+ -> Mn^2+ + 5 Fe^3+ + 4 H2O',
    'cours diiode et thiosulfate': 'I2 + 2 S2O3^2- -> 2 I- + S4O6^2-',
    'cours vitamine C et diiode': 'C6H8O6 + I2 -> C6H6O6 + 2 I- + 2 H+',
    'ex9 demi-équation acide oxalique': '2 CO2 + 2 H+ + 2 e- = H2C2O4',
    'ex9 permanganate et acide oxalique': '2 MnO4- + 5 H2C2O4 + 6 H+ -> 2 Mn^2+ + 10 CO2 + 8 H2O',
    'ex11 permanganate et eau oxygénée': '2 MnO4- + 5 H2O2 + 6 H+ -> 2 Mn^2+ + 5 O2 + 8 H2O',
    'ex13 demi-équation sulfate': 'SO4^2- + 4 H+ + 2 e- = SO2 + 2 H2O',
    'ex13 dioxyde de soufre et diiode': 'SO2 + I2 + 2 H2O -> SO4^2- + 4 H+ + 2 I-',
    'D05 hypochlorite et iodure': 'ClO- + 2 I- + 2 H+ -> I2 + Cl- + H2O',
    'D05 demi-équation hypochlorite/chlorure': 'ClO- + 2 H+ + 2 e- = Cl- + H2O',
    'D05 hypochlorite et chlorure (chlore actif)': 'ClO- + Cl- + 2 H+ -> Cl2 + H2O',
}
for nom, eq in EQUATIONS.items():
    equilibree(nom, eq)


def sortie_de(fonction):
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        fonction()
    return tampon.getvalue().rstrip()


def programme_cours(volumes):
    c2 = 2.00e-2      # mol/L : ions permanganate
    n1 = 1.20e-3      # mol : ions fer(II)
    for V in volumes:          # mL
        n2 = c2 * V * 1e-3
        x = min(n2 / 1, n1 / 5)
        nFe = n1 - 5 * x
        nMn = n2 - x
        print(f"V = {V:2d} mL : Fe2+ {nFe * 1e3:.2f} mmol ; MnO4- {nMn * 1e3:.2f} mmol")


ATTENDU = """V =  0 mL : Fe2+ 1.20 mmol ; MnO4- 0.00 mmol
V =  4 mL : Fe2+ 0.80 mmol ; MnO4- 0.00 mmol
V =  8 mL : Fe2+ 0.40 mmol ; MnO4- 0.00 mmol
V = 12 mL : Fe2+ 0.00 mmol ; MnO4- 0.00 mmol
V = 16 mL : Fe2+ 0.00 mmol ; MnO4- 0.08 mmol"""
s = sortie_de(lambda: programme_cours([0, 4, 8, 12, 16]))
print('   cours programme :', s.replace('\n', ' | '))
if s != ATTENDU:
    ECHECS.append('cours programme')
s6 = sortie_de(lambda: programme_cours([6]))
if s6 != "V =  6 mL : Fe2+ 0.60 mmol ; MnO4- 0.00 mmol":
    ECHECS.append('ex6 V = 6 mL')
s20 = sortie_de(lambda: programme_cours([20]))
if s20 != "V = 20 mL : Fe2+ 0.00 mmol ; MnO4- 0.16 mmol":
    ECHECS.append('ex6 V = 20 mL')
print('   ex6 :', s6, '|', s20)


# Exercice 6, question 4 : programme adapté au titrage du diiode par le thiosulfate
def programme_diiode():
    c2 = 5.00e-2
    n1 = 4.00e-4
    for V in [0, 8, 16, 20]:
        n2 = c2 * V * 1e-3
        x = min(n2 / 2, n1 / 1)
        print(f"V = {V:2d} mL : I2 {(n1 - x) * 1e3:.2f} mmol ; S2O3 {(n2 - 2 * x) * 1e3:.2f} mmol")


s4 = sortie_de(programme_diiode)
print('   ex6 diiode :', s4.replace('\n', ' | '))
if s4 != ("V =  0 mL : I2 0.40 mmol ; S2O3 0.00 mmol\nV =  8 mL : I2 0.20 mmol ; S2O3 0.00 mmol\n"
          "V = 16 mL : I2 0.00 mmol ; S2O3 0.00 mmol\nV = 20 mL : I2 0.00 mmol ; S2O3 0.20 mmol"):
    ECHECS.append('ex6 diiode')

for f, v in (('C6H8O6', 176.0), ('I2', 253.8), ('H2C2O4', 90.0), ('SO2', 64.1), ('KMnO4', 158.0), ('KI', 166.0)):
    verifie(f'M({f})', masse_molaire(f), v, 1e-9)
verifie('M(H2C2O4, 2 H2O)', masse_molaire('H2C2O4') + 2 * 18.0, 126.0, 1e-9)

# Cours
verifie("cours n(Fe2+) (mol)", 5 * 2.00e-2 * 12.0e-3, 1.20e-3, 1e-15)
verifie("cours c(Fe2+) (mol/L)", 5 * 2.00e-2 * 12.0e-3 / 10.0e-3, 0.120, 1e-12)
# Expérience : comprimé de vitamine C
n_vc = 1.00e-2 * 14.2e-3
verifie("expérience n vitamine C dans 10 mL (mol)", n_vc, 1.42e-4, 1e-12)
verifie("expérience n vitamine C du comprimé (mol)", n_vc * 20, 2.84e-3, 1e-12)
verifie("expérience masse de vitamine C (mg)", n_vc * 20 * 176.0 * 1000, 500, 0.5)
# Exercice 2
verifie("ex2 n diiode (mol)", 0.100 * 12.4e-3 / 2, 6.20e-4, 1e-12)
verifie("ex2 c diiode (mol/L)", 0.100 * 12.4e-3 / 2 / 20.0e-3, 3.10e-2, 1e-12)
# Exercice 5
verifie("ex5 n fer(II) (mol)", 5 * 0.0200 * 13.6e-3, 1.36e-3, 1e-12)
verifie("ex5 c fer(II) (mol/L)", 5 * 0.0200 * 13.6e-3 / 20.0e-3, 6.80e-2, 1e-12)
# Exercice 7 : médicament contre l'anémie
n7 = 5 * 2.00e-3 * 14.3e-3
verifie("ex7 n fer(II) dans 10 mL (mol)", n7, 1.43e-4, 1e-12)
verifie("ex7 n fer du comprimé (mol)", 10 * n7, 1.43e-3, 1e-12)
verifie("ex7 masse de fer (mg)", 10 * n7 * 55.8 * 1000, 79.8, 0.05)
verifie("ex7 écart relatif (%)", abs(10 * n7 * 55.8 * 1000 - 80) / 80 * 100, 0.25, 0.01)
verifie("ex7 volume attendu pour 80 mg (mL)", 0.080 / 55.8 / 10 / 5 / 2.00e-3 * 1000, 14.3, 0.05)
# Exercice 8 : antiseptique iodé
n8 = 1.00e-2 * 7.90e-3 / 2
verifie("ex8 n diiode (mol)", n8, 3.95e-5, 1e-12)
verifie("ex8 c solution diluée (mol/L)", n8 / 10.0e-3, 3.95e-3, 1e-12)
verifie("ex8 c antiseptique (mol/L)", 10 * n8 / 10.0e-3, 3.95e-2, 1e-12)
verifie("ex8 concentration en masse (g/L)", 10 * n8 / 10.0e-3 * 253.8, 10.0, 0.05)
# Exercice 9 : acide oxalique
n9 = 5 / 2 * 0.0200 * 15.6e-3
verifie("ex9 n acide oxalique dans 10 mL (mol)", n9, 7.80e-4, 1e-12)
verifie("ex9 masse dans 100 mL (g)", 10 * n9 * 126.0, 0.983, 0.0005)
verifie("ex9 pureté (%)", 10 * n9 * 126.0 / 1.00 * 100, 98.3, 0.05)
verifie("ex9 volume attendu pour un produit pur (mL)", 1.00 / 126.0 / 10 * 2 / 5 / 0.0200 * 1000, 15.9, 0.05)
# Exercice 10 : choisir le titrant
for c, v, inc in ((1.00e-1, 1.0, 10), (1.00e-2, 10.0, 1.0), (5.00e-3, 20.0, 0.5)):
    vE = 0.050 * 10.0e-3 / 5 / c * 1000
    verifie(f"ex10 VE pour c = {c} (mL)", vE, v, 1e-9)
    verifie(f"ex10 incertitude relative 0,1 mL pour c = {c} (%)", 0.1 / vE * 100, inc, 1e-9)
# Exercice 11 : eau oxygénée
n11 = 5 / 2 * 0.0200 * 17.6e-3
verifie("ex11 n eau oxygénée dans 10 mL (mol)", n11, 8.80e-4, 1e-12)
verifie("ex11 c solution diluée (mol/L)", n11 / 10.0e-3, 8.80e-2, 1e-12)
verifie("ex11 c eau oxygénée (mol/L)", 10 * n11 / 10.0e-3, 0.880, 1e-12)
verifie("ex11 titre en volumes", 10 * n11 / 10.0e-3 / 2 * 22.4, 9.9, 0.05)
verifie("ex11 volume attendu pour 10 volumes (mL)", 10 / 22.4 * 2 / 10 * 10.0e-3 * 2 / 5 / 0.0200 * 1000, 17.9, 0.05)
# Exercice 12 : jus de citron
for VE, t in ((14.2, 0.500), (11.4, 0.401)):
    verifie(f"ex12 c, VE = {VE} mL (mol/L)", 2.00e-3 * VE / 10.0, round(2.00e-3 * VE / 10.0, 7), 1e-12)
    verifie(f"ex12 concentration en masse, VE = {VE} mL (g/L)", 2.00e-3 * VE / 10.0 * 176.0, t, 0.0005)
verifie("ex12 perte de vitamine C (%)", (1 - 11.4 / 14.2) * 100, 20, 0.5)
verifie("ex12 volume de jus frais pour 110 mg (mL)", 110 / 0.500, 220, 1e-9)
verifie("ex12 vitamine C d'un verre de 200 mL de jus frais (mg)", 0.500 * 200, 100, 1e-9)
# Exercice 13 : dioxyde de soufre du vin
n13 = 5.00e-3 * 11.8e-3
verifie("ex13 n dioxyde de soufre (mol)", n13, 5.90e-5, 1e-12)
verifie("ex13 c (mol/L)", n13 / 25.0e-3, 2.36e-3, 1e-12)
verifie("ex13 concentration en masse (mg/L)", n13 / 25.0e-3 * 64.1 * 1000, 151, 0.5)
verifie("ex13 VE pour 200 mg/L (mL)", 0.200 / 64.1 * 25.0e-3 / 5.00e-3 * 1000, 15.6, 0.05)
# Exercice 14 : bain de permanganate
t14 = 0.500 / 4.0
verifie("ex14 concentration en masse attendue (g/L)", t14, 0.125, 1e-12)
verifie("ex14 dilution au 1/8000 (g/L)", 1000 / 8000, 0.125, 1e-12)
verifie("ex14 VE attendu (mL)", t14 / 158.0 * 20.0e-3 * 5 / 5.00e-3 * 1000, 15.8, 0.05)
n14 = 5.00e-3 * 15.4e-3 / 5
verifie("ex14 n permanganate (mol)", n14, 1.54e-5, 1e-12)
verifie("ex14 c permanganate (mol/L)", n14 / 20.0e-3, 7.70e-4, 1e-12)
verifie("ex14 concentration en masse mesurée (g/L)", n14 / 20.0e-3 * 158.0, 0.122, 0.0005)
verifie("ex14 écart relatif (%)", (n14 / 20.0e-3 * 158.0 - 0.125) / 0.125 * 100, -2.7, 0.05)
# Exercice 15 : graphique
verifie("ex15 n diiode (mmol)", 0.0500 * 16.0 / 2, 0.400, 1e-12)
verifie("ex15 c diiode (mol/L)", 0.0500 * 16.0e-3 / 2 / 20.0e-3, 2.00e-2, 1e-12)
verifie("ex15 thiosulfate en excès à 20 mL (mmol)", 0.0500 * (20 - 16.0), 0.20, 1e-12)
# Défi D05 : eau de Javel
for VE, c, t, pct in ((14.6, 0.365, 25.9, 2.6), (11.2, 0.280, 19.9, 2.0)):
    n_thio = 0.0500 * VE * 1e-3
    n_clo = n_thio / 2
    verifie(f"D05 VE = {VE} mL : n thiosulfate (mol)", n_thio, 0.0500 * VE * 1e-3, 0)
    verifie(f"D05 VE = {VE} mL : c hypochlorite (mol/L)", 10 * n_clo / 10.0e-3, c, 0.0005)
    verifie(f"D05 VE = {VE} mL : chlore actif (g/L)", 10 * n_clo / 10.0e-3 * 71.0, t, 0.05)
    verifie(f"D05 VE = {VE} mL : pourcentage (g pour 100 mL)", 10 * n_clo / 10.0e-3 * 71.0 / 10, pct, 0.05)
verifie("D05 n thiosulfate, flacon neuf (mol)", 0.0500 * 14.6e-3, 7.30e-4, 1e-12)
verifie("D05 n diiode, flacon neuf (mol)", 0.0500 * 14.6e-3 / 2, 3.65e-4, 1e-12)
verifie("D05 perte du vieux flacon (%)", (1 - 11.2 / 14.6) * 100, 23, 0.5)
verifie("D05 n iodure nécessaire (mol)", 2 * 3.65e-4, 7.30e-4, 1e-12)
verifie("D05 n iodure dans 1,0 g de KI (mol)", 1.0 / 166.0, 6.0e-3, 0.05e-3)
verifie("D05 VE attendu pour 0,37 mol/L (mL)", 0.37 * 1.0e-3 * 2 / 0.0500 * 1000, 14.8, 0.05)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les équations, sorties de programmes et valeurs du chapitre 5 et du défi D05 sont vérifiées.")
