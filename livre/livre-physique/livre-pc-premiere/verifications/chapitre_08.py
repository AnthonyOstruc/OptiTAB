"""Vérification du chapitre 8 (Molécules organiques et spectroscopie infrarouge) et du défi D08.

Pour chaque molécule publiée : formule brute déduite de la formule semi-développée, cohérence du nom (nombre d'atomes de
carbone, famille) ; bandes des spectres dans les intervalles de la table ; sortie du programme ; énumération du défi.
Lancer : python -I -X utf8 verifications/chapitre_08.py
"""
import io
import re
from contextlib import redirect_stdout

ECHECS = []
M = {'H': 1.0, 'C': 12.0, 'O': 16.0}


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def brute(semi):
    """Formule brute d'une formule semi-développée écrite sans multiplicateur de groupe : CH3-CH(CH3)-CHO."""
    compte = {}
    for el, nb in re.findall(r'([A-Z][a-z]?)(\d*)', semi):
        compte[el] = compte.get(el, 0) + (int(nb) if nb else 1)
    return compte


def ecrit(compte):
    return ''.join(f"{el}{compte[el] if compte[el] > 1 else ''}" for el in ('C', 'H', 'O') if el in compte)


def famille_formule(semi):
    if 'COOH' in semi:
        return 'acide'
    if semi.endswith('CHO') or semi.startswith('OHC') or semi == 'HCHO':
        return 'aldéhyde'
    if re.search(r'-CO-', semi):
        return 'cétone'
    if 'OH' in semi:
        return 'alcool'
    return 'alcane'


RACINES = {'méth': 1, 'éth': 2, 'prop': 3, 'but': 4, 'pent': 5, 'hex': 6, 'hept': 7, 'oct': 8}
MULT = {'': 1, 'di': 2, 'tri': 3}


def lit_nom(nom):
    """Nombre d'atomes de carbone et famille d'un nom à un seul groupe caractéristique."""
    famille = 'alcane'
    n = nom
    if n.startswith('acide '):
        famille, n = 'acide', n[6:].replace('oïque', '')
    elif n.endswith('ol'):
        famille = 'alcool'
    elif n.endswith('one'):
        famille = 'cétone'
    elif n.endswith('al'):
        famille = 'aldéhyde'
    carbones = 0
    for mult, sub in re.findall(r'(?:[\d,]+-)(di|tri|)(méthyl|éthyl)', n):
        carbones += MULT[mult] * (1 if sub == 'méthyl' else 2)
    principal = re.sub(r'^(?:[\d,]+-(?:di|tri|)(?:méthyl|éthyl))+', '', n)
    for racine in sorted(RACINES, key=len, reverse=True):
        if principal.startswith(racine):
            carbones += RACINES[racine]
            break
    else:
        raise ValueError(nom)
    return carbones, famille


MOLECULES = [
    # (nom, formule semi-développée, formule brute publiée)
    ('éthanol', 'CH3-CH2-OH', 'C2H6O'),
    ('propanone', 'CH3-CO-CH3', 'C3H6O'),
    ('acide méthanoïque', 'HCOOH', 'CH2O2'),
    ('butane', 'CH3-CH2-CH2-CH3', 'C4H10'),
    ('propanal', 'CH3-CH2-CHO', 'C3H6O'),
    ('butanone', 'CH3-CO-CH2-CH3', 'C4H8O'),
    ('propan-2-ol', 'CH3-CH(OH)-CH3', 'C3H8O'),
    ('acide propanoïque', 'CH3-CH2-COOH', 'C3H6O2'),
    ('butan-1-ol', 'CH3-CH2-CH2-CH2-OH', 'C4H10O'),
    ('méthanal', 'HCHO', 'CH2O'),
    ('propan-1-ol', 'CH3-CH2-CH2-OH', 'C3H8O'),
    ('2-méthylpropan-1-ol', 'CH3-CH(CH3)-CH2-OH', 'C4H10O'),
    ('pentan-3-one', 'CH3-CH2-CO-CH2-CH3', 'C5H10O'),
    ('2-méthylpropanal', 'CH3-CH(CH3)-CHO', 'C4H8O'),
    ('acide butanoïque', 'CH3-CH2-CH2-COOH', 'C4H8O2'),
    ('hexan-2-one', 'CH3-CO-CH2-CH2-CH2-CH3', 'C6H12O'),
    ('3-méthylbutan-1-ol', 'CH3-CH(CH3)-CH2-CH2-OH', 'C5H12O'),
    ('butanal', 'CH3-CH2-CH2-CHO', 'C4H8O'),
    ('butan-2-ol', 'CH3-CH(OH)-CH2-CH3', 'C4H10O'),
    ('2-méthylpropan-2-ol', 'CH3-C(CH3)(OH)-CH3', 'C4H10O'),
    ('acide éthanoïque', 'CH3-COOH', 'C2H4O2'),
    ('hexanal', 'CH3-CH2-CH2-CH2-CH2-CHO', 'C6H12O'),
    ('heptan-2-one', 'CH3-CO-CH2-CH2-CH2-CH2-CH3', 'C7H14O'),
    ('pentanal', 'CH3-CH2-CH2-CH2-CHO', 'C5H10O'),
    ('2-méthylbutanal', 'CH3-CH2-CH(CH3)-CHO', 'C5H10O'),
    ('3-méthylbutanal', 'CH3-CH(CH3)-CH2-CHO', 'C5H10O'),
    ('2,2-diméthylpropanal', 'CH3-C(CH3)(CH3)-CHO', 'C5H10O'),
    ('pentan-2-one', 'CH3-CO-CH2-CH2-CH3', 'C5H10O'),
    ('3-méthylbutan-2-one', 'CH3-CO-CH(CH3)-CH3', 'C5H10O'),
]
for nom, semi, publie in MOLECULES:
    b = ecrit(brute(semi))
    nc, fam = lit_nom(nom)
    ok = b == publie and nc == brute(semi)['C'] and fam == famille_formule(semi)
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:24s} {semi:28s} {b:8s} {fam}")
    if not ok:
        ECHECS.append(nom)

# Table des bandes (cours) et bandes des spectres publiés
TABLE = {'O-H alcool libre': (3580, 3670), 'O-H alcool lié': (3200, 3400), 'O-H acide': (2500, 3200),
         'C-H': (2800, 3000), 'C-H aldéhyde': (2650, 2850), 'C=O': (1650, 1750)}
SPECTRES = {
    'éthanol': [('O-H alcool lié', 3340), ('C-H', 2975)],
    'propanal': [('C-H', 2980), ('C-H aldéhyde', 2820), ('C-H aldéhyde', 2720), ('C=O', 1730)],
    'propanone': [('C-H', 2995), ('C=O', 1715)],
    'acide éthanoïque': [('O-H acide', 3000), ('C=O', 1715)],
    'ex5 propan-1-ol': [('O-H alcool lié', 3330), ('C-H', 2960), ('C-H', 2880)],
    'ex12 A propanal': [('C-H aldéhyde', 2820), ('C-H aldéhyde', 2720), ('C=O', 1730)],
    'ex12 B acide propanoïque': [('O-H acide', 2980), ('C=O', 1712)],
    'ex14 butanone': [('C-H', 2980), ('C=O', 1718)],
    'ex15 propan-2-ol': [('O-H alcool lié', 3350), ('C-H', 2970)],
    'ex15 mélange final': [('O-H alcool lié', 3400), ('C=O', 1715)],
    'D08 3-méthylbutanal': [('C-H', 2960), ('C-H aldéhyde', 2810), ('C-H aldéhyde', 2715), ('C=O', 1728)],
}
for spectre, bandes in SPECTRES.items():
    for liaison, sigma in bandes:
        mini, maxi = TABLE[liaison]
        ok = mini <= sigma <= maxi
        if not ok:
            ECHECS.append(f'{spectre} {liaison} {sigma}')
        print(f"{'ok ' if ok else 'ÉCHEC'} bande {spectre:26s} {liaison:16s} {sigma}")


def sortie_de(fonction):
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        fonction()
    return tampon.getvalue().strip()


def programme(table, pics):
    for pic in pics:
        liaisons = [nom for nom, (mini, maxi) in table.items() if mini <= pic <= maxi]
        print(pic, liaisons)


T = {'O-H alcool': (3200, 3400), 'O-H acide': (2500, 3200), 'C-H': (2800, 3000), 'C=O': (1650, 1750)}
s = sortie_de(lambda: programme(T, [3340, 2970, 1715]))
print('   cours programme :', s.replace('\n', ' | '))
if s != "3340 ['O-H alcool']\n2970 ['O-H acide', 'C-H']\n1715 ['C=O']":
    ECHECS.append('cours programme')
s6 = sortie_de(lambda: programme(T, [3000, 2720, 1730]))
print('   ex6 :', s6.replace('\n', ' | '))
if s6 != "3000 ['O-H acide', 'C-H']\n2720 ['O-H acide']\n1730 ['C=O']":
    ECHECS.append('ex6 programme')
T2 = dict(T)
T2['C-H aldehyde'] = (2650, 2850)
s6b = sortie_de(lambda: programme(T2, [2720]))
print('   ex6 avec aldéhyde :', s6b)
if s6b != "2720 ['O-H acide', 'C-H aldehyde']":
    ECHECS.append('ex6 programme aldéhyde')

# Exercice 13 : gel hydroalcoolique
verifie("ex13 masse d'éthanol dans 80 mL (g)", 80 * 0.789, 63.1, 0.05)
verifie("ex13 n éthanol (mol)", 80 * 0.789 / 46.0, 1.37, 0.005)
verifie("ex13 M(C2H6O)", 2 * 12.0 + 6 * 1.0 + 16.0, 46.0, 1e-9)
verifie("ex13 M(C3H8O)", 3 * 12.0 + 8 * 1.0 + 16.0, 60.0, 1e-9)
verifie("ex13 masse de propan-2-ol dans 75 mL (g)", 75 * 0.786, 59.0, 0.05)
verifie("ex13 n propan-2-ol (mol)", 75 * 0.786 / 60.0, 0.983, 0.0005)

# Défi D08 : les sept composés carbonylés saturés de formule C5H10O
ISOMERES = {'pentanal': 'CH3-CH2-CH2-CH2-CHO', '2-méthylbutanal': 'CH3-CH2-CH(CH3)-CHO',
            '3-méthylbutanal': 'CH3-CH(CH3)-CH2-CHO', '2,2-diméthylpropanal': 'CH3-C(CH3)(CH3)-CHO',
            'pentan-2-one': 'CH3-CO-CH2-CH2-CH3', 'pentan-3-one': 'CH3-CH2-CO-CH2-CH3',
            '3-méthylbutan-2-one': 'CH3-CO-CH(CH3)-CH3'}
verifie("D08 nombre d'isomères", len(ISOMERES), 7, 0)
for nom, semi in ISOMERES.items():
    if ecrit(brute(semi)) != 'C5H10O':
        ECHECS.append(f'D08 formule {nom}')
aldehydes = [n for n, s_ in ISOMERES.items() if famille_formule(s_) == 'aldéhyde']
verifie("D08 aldéhydes", len(aldehydes), 4, 0)
ramifies = [n for n in aldehydes if 'méthyl' in n]
verifie("D08 aldéhydes ramifiés", len(ramifies), 3, 0)
# indice 3 : la ramification n'est pas portée par le carbone voisin du groupe CHO
reste = [n for n in ramifies if not n.startswith('2-') and not n.startswith('2,2-')]
if reste != ['3-méthylbutanal']:
    ECHECS.append('D08 conclusion')
print('   D08 conclusion :', reste)
verifie("D08 M(C5H10O)", 5 * 12.0 + 10 * 1.0 + 16.0, 86.0, 1e-9)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les formules, noms, bandes, sorties et énumérations du chapitre 8 et du défi D08 sont vérifiées.")
