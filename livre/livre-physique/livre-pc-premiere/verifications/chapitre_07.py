"""Vérification du chapitre 7 (Cohésion, dissolution et extraction) et du défi D07.

Équations de dissolution (éléments et charges), sorties exactes des programmes Python, valeurs numériques.
Lancer : python -I -X utf8 verifications/chapitre_07.py
"""
import io
import re
from contextlib import redirect_stdout

ECHECS = []
M = {'H': 1.0, 'C': 12.0, 'N': 14.0, 'O': 16.0, 'Na': 23.0, 'Mg': 24.3, 'Al': 27.0, 'P': 31.0, 'S': 32.1,
     'Cl': 35.5, 'K': 39.1, 'Ca': 40.1, 'Cu': 63.5, 'I': 126.9}


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:60s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def compo(formule):
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
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:60s} {equation}")
    if not ok:
        ECHECS.append(nom)


EQUATIONS = {
    'cours chlorure de sodium': 'NaCl -> Na+ + Cl-',
    'cours chlorure de calcium': 'CaCl2 -> Ca^2+ + 2 Cl-',
    'ex2 chlorure de potassium': 'KCl -> K+ + Cl-',
    'ex2 sulfate de sodium': 'Na2SO4 -> 2 Na+ + SO4^2-',
    'ex2 sulfate d aluminium': 'Al2(SO4)3 -> 2 Al^3+ + 3 SO4^2-',
    'ex2 phosphate de potassium': 'K3PO4 -> 3 K+ + PO4^3-',
    'ex2 nitrate de magnésium': 'Mg(NO3)2 -> Mg^2+ + 2 NO3-',
    'ex6 sulfate de potassium': 'K2SO4 -> 2 K+ + SO4^2-',
    'ex6 phosphate de sodium': 'Na3PO4 -> 3 Na+ + PO4^3-',
    'ex7 sulfate de cuivre': 'CuSO4 -> Cu^2+ + SO4^2-',
    'ex11 et ex14 eau dure et savon': '2 C17H35COO- + Ca^2+ -> (C17H35COO)2Ca',
}
for nom, eq in EQUATIONS.items():
    equilibree(nom, eq)

for f, v in (('NaCl', 58.5), ('CaCl2', 111.1), ('CuSO4', 159.6), ('Na2SO4', 142.1), ('Al2(SO4)3', 342.3),
             ('C17H35COONa', 306.0), ('KCl', 74.6), ('I2', 253.8)):
    verifie(f'M({f})', masse_molaire(f), v, 1e-9)
verifie('M(CuSO4, 5 H2O)', masse_molaire('CuSO4') + 5 * 18.0, 249.6, 1e-9)


def sortie_de(fonction):
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        fonction()
    return tampon.getvalue().strip()


def programme(solides, c):
    for nom, ions in solides.items():
        print(nom, {ion: round(nb * c, 3) for ion, nb in ions.items()})


SOLIDES = {'NaCl': {'Na+': 1, 'Cl-': 1},
           'CaCl2': {'Ca2+': 1, 'Cl-': 2},
           'Al2(SO4)3': {'Al3+': 2, 'SO42-': 3}}
s = sortie_de(lambda: programme(SOLIDES, 0.100))
print('   cours programme :', s.replace('\n', ' | '))
if s != ("NaCl {'Na+': 0.1, 'Cl-': 0.1}\nCaCl2 {'Ca2+': 0.1, 'Cl-': 0.2}\n"
         "Al2(SO4)3 {'Al3+': 0.2, 'SO42-': 0.3}"):
    ECHECS.append('cours programme')
s6 = sortie_de(lambda: programme({'K2SO4': {'K+': 2, 'SO42-': 1}, 'Na3PO4': {'Na+': 3, 'PO43-': 1}}, 0.100))
print('   ex6 :', s6.replace('\n', ' | '))
if s6 != "K2SO4 {'K+': 0.2, 'SO42-': 0.1}\nNa3PO4 {'Na+': 0.3, 'PO43-': 0.1}":
    ECHECS.append('ex6 programme')
s6b = sortie_de(lambda: programme(SOLIDES, 0.050))
print('   ex6 c = 0,050 :', s6b.replace('\n', ' | '))
if s6b != ("NaCl {'Na+': 0.05, 'Cl-': 0.05}\nCaCl2 {'Ca2+': 0.05, 'Cl-': 0.1}\n"
           "Al2(SO4)3 {'Al3+': 0.1, 'SO42-': 0.15}"):
    ECHECS.append('ex6 programme c = 0,050')

# Cours : chlorure de calcium
n = 2.22 / 111.1
verifie("cours n chlorure de calcium (mol)", n, 2.00e-2, 0.005e-2)
verifie("cours c (mol/L)", n / 0.2000, 0.100, 0.0005)
# Exercice 2 : c = 0,050 mol/L
for nom, cat, an, vc, va in (('KCl', 1, 1, 0.050, 0.050), ('CaCl2', 1, 2, 0.050, 0.100), ('Na2SO4', 2, 1, 0.100, 0.050),
                             ('Al2(SO4)3', 2, 3, 0.100, 0.150), ('K3PO4', 3, 1, 0.150, 0.050),
                             ('Mg(NO3)2', 1, 2, 0.050, 0.100)):
    verifie(f"ex2 {nom} cation (mol/L)", cat * 0.050, vc, 1e-12)
    verifie(f"ex2 {nom} anion (mol/L)", an * 0.050, va, 1e-12)
# Exercice 7 : sulfate de cuivre pentahydraté
n7 = 2.50 / 249.6
verifie("ex7 n (mol)", n7, 1.00e-2, 0.005e-2)
verifie("ex7 c (mol/L)", n7 / 0.1000, 0.100, 0.0005)
verifie("ex7 masse pour 250,0 mL à 0,0500 mol/L (g)", 0.0500 * 0.2500 * 249.6, 3.12, 0.005)
verifie("ex7 concentration en masse de Cu2+ (g/L)", 0.100 * 63.5, 6.35, 1e-9)
# Exercice 8 : sels de déneigement
verifie("ex8 n NaCl dans 1 kg (mol)", 1000 / 58.5, 17.1, 0.05)
verifie("ex8 n ions NaCl (mol)", 2 * 1000 / 58.5, 34.2, 0.05)
verifie("ex8 n CaCl2 dans 1 kg (mol)", 1000 / 111.1, 9.00, 0.005)
verifie("ex8 n ions CaCl2 (mol)", 3 * 1000 / 111.1, 27.0, 0.05)
# Exercice 9 : caféine
verifie("ex9 masse de caféine dissoute dans 50 mL d'eau (g)", 22 * 0.050, 1.1, 1e-9)
verifie("ex9 masse dissoute dans 50 mL de dichlorométhane (g)", 100 * 0.050, 5.0, 1e-9)
# Exercice 12 : diiode
verifie("ex12 masse de diiode dans 20 mL (mg)", 0.25 * 20, 5.0, 1e-12)
verifie("ex12 concentration dans 10 mL de cyclohexane (g/L)", 0.25 * 20 / 10, 0.50, 1e-12)
# Exercice 13 : températures d'ébullition (données publiées, ordre)
teb = {'CH4': -161, 'NH3': -33, 'H2O': 100, 'HF': 20, 'H2S': -60, 'éthanol': 78, 'méthoxyméthane': -24}
if not (teb['H2O'] > teb['HF'] > teb['NH3'] > teb['CH4'] and teb['H2O'] > teb['H2S']
        and teb['éthanol'] > teb['méthoxyméthane']):
    ECHECS.append('ex13 ordre des températures')
verifie("ex13 écart éthanol / méthoxyméthane (°C)", teb['éthanol'] - teb['méthoxyméthane'], 102, 0)
verifie("ex13 écart eau / sulfure d'hydrogène (°C)", teb['H2O'] - teb['H2S'], 160, 0)
# Exercice 14 : eau dure et savon
nCa = 30 * 1e-4 * 5.0
verifie("ex14 [Ca2+] pour 30 °f (mol/L)", 30 * 1e-4, 3.0e-3, 1e-15)
verifie("ex14 n Ca2+ dans 5,0 L (mol)", nCa, 1.5e-2, 1e-15)
verifie("ex14 n ions stéarate précipités (mol)", 2 * nCa, 3.0e-2, 1e-15)
verifie("ex14 masse de savon perdue (g)", 2 * nCa * 306.0, 9.2, 0.05)
verifie("ex14 masse pour une eau douce à 5 °f (g)", 2 * 5 * 1e-4 * 5.0 * 306.0, 1.5, 0.05)


# Exercice 15 : extractions successives, c_org = K c_aq avec K = 5
def fraction_extraite(K, Vaq, Vorg):
    return K * Vorg / (Vaq + K * Vorg)


verifie("ex15 une extraction de 40 mL : fraction extraite", fraction_extraite(5, 100, 40), 0.67, 0.005)
verifie("ex15 une extraction de 20 mL : fraction extraite", fraction_extraite(5, 100, 20), 0.50, 1e-12)
deux = 1 - (1 - fraction_extraite(5, 100, 20)) ** 2
verifie("ex15 deux extractions de 20 mL : fraction extraite", deux, 0.75, 1e-12)
verifie("ex15 masse extraite, une extraction (g)", 1.0 * fraction_extraite(5, 100, 40), 0.67, 0.005)
verifie("ex15 masse extraite, deux extractions (g)", 1.0 * deux, 0.75, 1e-12)
verifie("ex15 quatre extractions de 10 mL", 1 - (1 - fraction_extraite(5, 100, 10)) ** 4, 0.80, 0.005)

# Défi D07 : étiquette d'une eau minérale (mg/L)
cations = {'Ca2+': (486, 40.1, 2), 'Mg2+': (84, 24.3, 2), 'Na+': (14.2, 23.0, 1), 'K+': (4.1, 39.1, 1)}
anions = {'SO42-': (1187, 96.1, 2), 'HCO3-': (403, 61.0, 1), 'Cl-': (14, 35.5, 1), 'NO3-': (4.3, 62.0, 1)}
publies_c = {'Ca2+': (12.1, 24.2), 'Mg2+': (3.46, 6.91), 'Na+': (0.617, 0.617), 'K+': (0.105, 0.105)}
publies_a = {'SO42-': (12.4, 24.7), 'HCO3-': (6.61, 6.61), 'Cl-': (0.394, 0.394), 'NO3-': (0.069, 0.069)}
for dico, pub in ((cations, publies_c), (anions, publies_a)):
    for ion, (t, Mi, z) in dico.items():
        c = t / Mi
        verifie(f"D07 {ion} concentration (mmol/L)", c, pub[ion][0], 0.0051 * pub[ion][0] + 0.0005)
        verifie(f"D07 {ion} charges (mmol/L)", z * c, pub[ion][1], 0.0051 * pub[ion][1] + 0.0005)
plus = sum(z * t / Mi for t, Mi, z in cations.values())
moins = sum(z * t / Mi for t, Mi, z in anions.values())
verifie("D07 charges positives (mmol/L)", plus, 31.9, 0.05)
verifie("D07 charges négatives (mmol/L)", moins, 31.8, 0.05)
verifie("D07 écart relatif (%)", (plus - moins) / plus * 100, 0.3, 0.1)
verifie("D07 masse totale des ions (mg/L)", sum(t for t, _, _ in cations.values()) + sum(t for t, _, _ in anions.values()),
        2197, 0.5)
def programme_defi():
    def charges(ions):
        total = 0
        for t, Mi, z in ions.values():
            total = total + z * t / Mi
        return total
    p, m = charges(cations), charges(anions)
    print(round(p, 1), round(m, 1), round(100 * (p - m) / p, 1))


sd = sortie_de(programme_defi)
print('   D07 programme :', sd)
if sd != '31.9 31.8 0.3':
    ECHECS.append('D07 programme')
verifie("D07 M(SO4)", 32.1 + 4 * 16.0, 96.1, 1e-9)
verifie("D07 M(HCO3)", 1.0 + 12.0 + 48.0, 61.0, 1e-9)
verifie("D07 M(NO3)", 14.0 + 48.0, 62.0, 1e-9)
verifie("D07 rapport Ca2+ / SO42- (quantités)", (486 / 40.1) / (1187 / 96.1), 0.98, 0.005)
verifie("D07 masse de gypse CaSO4,2H2O dissoute par litre (g)", 486 / 40.1 * (40.1 + 96.1 + 36.0) / 1000, 2.09, 0.005)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les équations, sorties de programmes et valeurs du chapitre 7 et du défi D07 sont vérifiées.")
