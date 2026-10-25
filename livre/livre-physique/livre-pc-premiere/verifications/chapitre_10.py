"""Vérification du chapitre 10 (Combustions et énergie chimique) et du défi D10.

Équations de combustion ajustées, énergies de réaction à partir des énergies de liaison, pouvoirs calorifiques,
bilans d'énergie et de dioxyde de carbone, sorties exactes des programmes Python.
Lancer : python -I -X utf8 verifications/chapitre_10.py
"""
import io
import re
from contextlib import redirect_stdout

ECHECS = []
M = {'H': 1.0, 'C': 12.0, 'O': 16.0}
D = {'C-H': 415, 'C-C': 345, 'C-O': 358, 'C=O': 804, 'O=O': 498, 'O-H': 463, 'H-H': 436}
ER = {'CH4': -802, 'C3H8': -2043, 'C4H10': -2657, 'C8H18': -5074, 'C2H6O': -1235, 'CH4O': -638, 'H2': -242}


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
    'méthane': 'CH4 + 2 O2 -> CO2 + 2 H2O',
    'propane': 'C3H8 + 5 O2 -> 3 CO2 + 4 H2O',
    'butane': '2 C4H10 + 13 O2 -> 8 CO2 + 10 H2O',
    'éthanol': 'C2H6O + 3 O2 -> 2 CO2 + 3 H2O',
    'méthanol': '2 CH4O + 3 O2 -> 2 CO2 + 4 H2O',
    'octane': '2 C8H18 + 25 O2 -> 16 CO2 + 18 H2O',
    'dihydrogène': '2 H2 + O2 -> 2 H2O',
    'combustion incomplète du méthane (CO)': '2 CH4 + 3 O2 -> 2 CO + 4 H2O',
    'combustion incomplète du méthane (C)': 'CH4 + O2 -> C + 2 H2O',
    'carbone': 'C + O2 -> CO2',
    'paraffine': 'C25H52 + 38 O2 -> 25 CO2 + 26 H2O',
    'kérosène': '2 C12H26 + 37 O2 -> 24 CO2 + 26 H2O',
}
for nom, eq in EQUATIONS.items():
    equilibree(nom, eq)
# formules générales : alcane n = 1 à 8 et alcool n = 1 à 4
for n in range(1, 9):
    if (3 * n + 1) % 2 == 0:
        equilibree(f'alcane n = {n}', f'C{n}H{2*n+2} + {(3*n+1)//2} O2 -> {n} CO2 + {n+1} H2O')
for n in range(2, 5, 2):
    equilibree(f'alcool n = {n}', f'C{n}H{2*n+2}O + {3*n//2} O2 -> {n} CO2 + {n+1} H2O')
equilibree('ex2 demi-équation CO2/CH4', 'CO2 + 8 H -> CH4 + 2 H2O')

# Masses molaires et pouvoirs calorifiques (MJ/kg = kJ/g)
for f, v in (('CH4', 16.0), ('C3H8', 44.0), ('C4H10', 58.0), ('C8H18', 114.0), ('C2H6O', 46.0), ('CH4O', 32.0),
             ('H2', 2.0), ('CO2', 44.0), ('C25H52', 352.0), ('C12H26', 170.0)):
    verifie(f'M({f})', mm(f), v, 1e-9)
PC = {'CH4': 50.1, 'C3H8': 46.4, 'C4H10': 45.8, 'C8H18': 44.5, 'C2H6O': 26.8, 'CH4O': 19.9, 'H2': 121}
for f, v in PC.items():
    verifie(f'PC {f} (MJ/kg)', -ER[f] / mm(f), v, 0.05 if f != 'H2' else 0.5)


def sortie_de(fonction):
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        fonction()
    return tampon.getvalue().strip()


def programme(rompues, formees):
    Er = sum(D[l] * n for l, n in rompues.items()) - sum(D[l] * n for l, n in formees.items())
    print('Er =', Er, 'kJ/mol')


s = sortie_de(lambda: programme({'C-H': 4, 'O=O': 2}, {'C=O': 2, 'O-H': 4}))
print('   cours programme :', s)
if s != 'Er = -804 kJ/mol':
    ECHECS.append('cours programme')
s6 = sortie_de(lambda: programme({'C-C': 2, 'C-H': 8, 'O=O': 5}, {'C=O': 6, 'O-H': 8}))
s6b = sortie_de(lambda: programme({'C-C': 6, 'C-H': 20, 'O=O': 13}, {'C=O': 16, 'O-H': 20}))
print('   ex6 :', s6, '|', s6b)
if s6 != 'Er = -2028 kJ/mol' or s6b != 'Er = -5280 kJ/mol':
    ECHECS.append('ex6 programme')
verifie("ex6 écart propane / tables (%)", (2043 - 2028) / 2043 * 100, 0.7, 0.05)
verifie("ex6 butane par mole (kJ/mol)", -5280 / 2, -2640, 0)
verifie("ex6 écart butane / tables (%)", (2657 - 2640) / 2657 * 100, 0.6, 0.05)
# Cours : bilan d'énergie du méthane
verifie("cours énergie de rupture (kJ)", 4 * 415 + 2 * 498, 2656, 0)
verifie("cours énergie de formation (kJ)", 2 * 804 + 4 * 463, 3460, 0)
verifie("cours écart avec la valeur des tables (%)", (804 - 802) / 802 * 100, 0.25, 0.01)
verifie("cours énergie libérée par 1,0 kg de méthane (MJ)", 1000 / 16.0 * 802 / 1000, 50.1, 0.05)
# Exercice 4 : chauffer de l'eau
Q4 = 1.0 * 4.18 * 80
verifie("ex4 énergie pour chauffer 1,0 L de 20 à 100 °C (kJ)", Q4, 334, 0.5)
verifie("ex4 masse de butane, rendement 100 % (g)", Q4 / 45.8, 7.3, 0.05)
verifie("ex4 masse de butane, rendement 50 % (g)", Q4 / 45.8 / 0.50, 14.6, 0.05)
# Exercice 5 : dihydrogène
verifie("ex5 énergie de rupture (kJ)", 2 * 436 + 498, 1370, 0)
verifie("ex5 énergie de formation (kJ)", 4 * 463, 1852, 0)
verifie("ex5 Er pour l'équation (kJ)", 1370 - 1852, -482, 0)
verifie("ex5 Er par mole de H2 (kJ/mol)", (1370 - 1852) / 2, -241, 0)
# Exercice 7 : mesurer un pouvoir calorifique
Q7 = 0.200 * 4180 * 20.0
verifie("ex7 énergie reçue par l'eau (kJ)", Q7 / 1000, 16.7, 0.05)
verifie("ex7 PC expérimental (kJ/g)", Q7 / 1000 / 1.20, 13.9, 0.05)
verifie("ex7 rapport à la valeur des tables (%)", Q7 / 1000 / 1.20 / 26.8 * 100, 52, 0.5)
# Exercice 8 : chauffage au gaz
E8 = 15000 * 3.6
verifie("ex8 énergie (MJ)", E8, 54000, 0)
m8 = E8 / 50.1
verifie("ex8 masse de méthane (kg)", m8, 1078, 0.5)
n8 = m8 * 1000 / 16.0
verifie("ex8 n méthane (mol)", n8, 6.74e4, 0.005e4)
verifie("ex8 volume de méthane à 20 °C (m3)", n8 * 24.0 / 1000, 1620, 5)
verifie("ex8 masse de CO2 (t)", n8 * 44.0 / 1e6, 2.96, 0.005)
# Exercice 10 : bois et fioul pour 10 000 kWh
E10 = 10000 * 3.6
verifie("ex10 masse de bois à 15 MJ/kg (kg)", E10 / 15, 2400, 0)
verifie("ex10 masse de fioul à 42,6 MJ/kg (kg)", E10 / 42.6, 845, 0.5)
verifie("ex10 volume de fioul (L)", E10 / 42.6 / 0.84, 1006, 1)
# Exercice 11 : dihydrogène
verifie("ex11 masse d'octane équivalente à 1 kg de H2 (kg)", 121 / 44.5, 2.72, 0.005)
verifie("ex11 volume de 1 kg de H2 à 20 °C sous 1 bar (m3)", 1000 / 2.0 * 24.0 / 1000, 12.0, 1e-9)
verifie("ex11 volume de 1 kg de H2 à 700 bar (L)", 1000 / 40, 25, 0)
# Exercice 12 : éthanol et butane
verifie("ex12 CO2 de l'éthanol (g/MJ)", 2 * 44.0 / 1235 * 1000, 71.3, 0.05)
verifie("ex12 CO2 du butane (g/MJ)", 4 * 44.0 / 2657 * 1000, 66.2, 0.05)
verifie("ex12 masse d'éthanol pour 1 MJ (g)", 1000 / 26.8, 37.3, 0.05)
verifie("ex12 masse de butane pour 1 MJ (g)", 1000 / 45.8, 21.8, 0.05)
# Exercice 13 : voiture
n13 = 0.060 * 750 / 114.0
verifie("ex13 masse d'essence par km (g)", 0.060 * 750, 45.0, 1e-9)
verifie("ex13 énergie par km (MJ)", n13 * 5074 / 1000, 2.00, 0.005)
verifie("ex13 énergie utile à 35 % (MJ)", n13 * 5074 / 1000 * 0.35, 0.70, 0.005)
verifie("ex13 CO2 par km (g)", 8 * n13 * 44.0, 139, 0.5)
verifie("ex13 énergie pour 100 km (MJ)", n13 * 5074 / 1000 * 100, 200, 0.5)
verifie("ex13 voiture électrique, 15 kWh (MJ)", 15 * 3.6, 54, 1e-9)
verifie("ex13 rapport essence / électrique", n13 * 5074 / 1000 * 100 / 54, 3.7, 0.05)
# Exercice 14 : biogaz
n14 = 0.60 * 1000 / 24.0
verifie("ex14 n méthane dans 1 m3 de biogaz (mol)", n14, 25.0, 1e-9)
verifie("ex14 énergie de 1 m3 (kJ)", n14 * 802, 2.005e4, 1e-9)
verifie("ex14 énergie de 1 m3 (MJ, environ 20)", n14 * 802 / 1000, 20, 0.06)
verifie("ex14 énergie de 1 m3 (kWh)", n14 * 802 / 1000 / 3.6, 5.6, 0.05)
verifie("ex14 énergie par jour (kWh)", 300 * n14 * 802 / 1000 / 3.6, 1671, 0.5)
verifie("ex14 énergie par an (MWh)", 300 * n14 * 802 / 1000 / 3.6 * 365 / 1000, 610, 0.5)
verifie("ex14 nombre de foyers à 15 MWh", 300 * n14 * 802 / 1000 / 3.6 * 365 / 1000 / 15, 40.7, 0.05)
# Exercice 15 : bougie
verifie("ex15 énergie par heure (kJ)", 5.0 * 42, 210, 1e-9)
verifie("ex15 puissance (W)", 5.0 * 42 * 1000 / 3600, 58, 0.5)
verifie("ex15 n paraffine par heure (mol)", 5.0 / 352.0, 1.42e-2, 0.005e-2)
verifie("ex15 CO2 par heure (g)", 25 * 5.0 / 352.0 * 44.0, 15.6, 0.05)

# Figure 10-co2 et défi D10 : g de CO2 par MJ
CO2 = {'méthane': 44.0 / 802, 'butane': 4 * 44.0 / 2657, 'octane': 8 * 44.0 / 5074, 'éthanol': 2 * 44.0 / 1235,
       'carbone': 44.0 / 393.5}
for nom, v in (('méthane', 54.9), ('butane', 66.2), ('octane', 69.4), ('éthanol', 71.3), ('carbone', 112)):
    verifie(f"CO2 {nom} (g/MJ)", CO2[nom] * 1000, v, 0.05 if nom != 'carbone' else 0.5)
# Défi D10
dens = {'H2': (121, 0.071), 'CH4': (50.1, 0.42), 'kérosène': (43.0, 0.80), 'éthanol': (26.8, 0.789)}
for nom, v in (('H2', 8.6), ('CH4', 21.0), ('kérosène', 34.4), ('éthanol', 21.1)):
    verifie(f"D10 densité d'énergie {nom} (MJ/L)", dens[nom][0] * dens[nom][1], v, 0.05)
verifie("D10 Er kérosène (kJ/mol)", 43.0 * 170.0, 7310, 0)
verifie("D10 CO2 kérosène (g/MJ)", 12 * 44.0 / (43.0 * 170.0) * 1000, 72.2, 0.05)
verifie("D10 volume de réservoir H2 pour 1 GJ (L)", 1000 / (121 * 0.071), 116, 0.5)
verifie("D10 volume de réservoir kérosène pour 1 GJ (L)", 1000 / (43.0 * 0.80), 29.1, 0.05)
verifie("D10 masse de H2 pour 1 GJ (kg)", 1000 / 121, 8.3, 0.05)
verifie("D10 masse de kérosène pour 1 GJ (kg)", 1000 / 43.0, 23.3, 0.05)


def programme_defi():
    carburants = {'H2': [121, 0.071], 'CH4': [50.1, 0.42], 'kerosene': [43.0, 0.80], 'ethanol': [26.8, 0.789]}
    par_litre = {nom: round(pc * rho, 1) for nom, (pc, rho) in carburants.items()}
    print(sorted(par_litre, key=par_litre.get, reverse=True))
    print(par_litre)


sd = sortie_de(programme_defi)
print('   D10 programme :', sd.replace('\n', ' | '))
if sd != ("['kerosene', 'ethanol', 'CH4', 'H2']\n"
          "{'H2': 8.6, 'CH4': 21.0, 'kerosene': 34.4, 'ethanol': 21.1}"):
    ECHECS.append('D10 programme')

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les équations, énergies, sorties de programmes et valeurs du chapitre 10 et du défi D10 sont vérifiées.")
