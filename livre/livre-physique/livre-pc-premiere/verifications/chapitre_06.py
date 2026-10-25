"""Vérification du chapitre 6 (Schémas de Lewis, géométrie et polarité) et du défi D06.

Pour chaque schéma de Lewis publié : nombre total d'électrons de valence, règle du duet ou de l'octet pour chaque atome
(sauf lacune annoncée). Puis écarts d'électronégativité, sortie du programme Python et calculs du défi.
Lancer : python -I -X utf8 verifications/chapitre_06.py
"""
import io
import math
from contextlib import redirect_stdout

ECHECS = []
VALENCE = {'H': 1, 'B': 3, 'C': 4, 'N': 5, 'O': 6, 'F': 7, 'Na': 1, 'Al': 3, 'S': 6, 'Cl': 7}
CHI = {'H': 2.20, 'Li': 0.98, 'Be': 1.57, 'B': 2.04, 'C': 2.55, 'N': 3.04, 'O': 3.44, 'F': 3.98,
       'Na': 0.93, 'Mg': 1.31, 'Al': 1.61, 'Si': 1.90, 'P': 2.19, 'S': 2.58, 'Cl': 3.16}


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def lewis(nom, atomes, liaisons, charge=0, lacunes=(), doublets_publies=None):
    """atomes : liste (symbole, doublets non liants) ; liaisons : liste (i, j, multiplicité)."""
    entourage = [0] * len(atomes)
    nl = 0
    for i, j, mult in liaisons:
        entourage[i] += 2 * mult
        entourage[j] += 2 * mult
        nl += mult
    nnl = sum(d for _, d in atomes)
    for k, (s, d) in enumerate(atomes):
        entourage[k] += 2 * d
    e_valence = sum(VALENCE[s] for s, _ in atomes) - charge
    ok = e_valence == 2 * (nl + nnl)
    for k, (s, d) in enumerate(atomes):
        cible = 2 if s == 'H' else 8
        if k in lacunes:
            ok = ok and entourage[k] < cible
        else:
            ok = ok and entourage[k] == cible
    if doublets_publies is not None:
        ok = ok and doublets_publies == (nl + nnl, nl, nnl)
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:30s} {e_valence} e- de valence ; {nl} liants, {nnl} non liants")
    if not ok:
        ECHECS.append(nom)


# Schémas du cours (liste du programme) et des exercices
lewis('H2', [('H', 0), ('H', 0)], [(0, 1, 1)])
lewis('O2', [('O', 2), ('O', 2)], [(0, 1, 2)])
lewis('N2', [('N', 1), ('N', 1)], [(0, 1, 3)])
lewis('H2O', [('O', 2), ('H', 0), ('H', 0)], [(0, 1, 1), (0, 2, 1)], doublets_publies=(4, 2, 2))
lewis('CO2', [('C', 0), ('O', 2), ('O', 2)], [(0, 1, 2), (0, 2, 2)], doublets_publies=(8, 4, 4))
lewis('NH3', [('N', 1), ('H', 0), ('H', 0), ('H', 0)], [(0, 1, 1), (0, 2, 1), (0, 3, 1)], doublets_publies=(4, 3, 1))
lewis('CH4', [('C', 0)] + [('H', 0)] * 4, [(0, k, 1) for k in range(1, 5)], doublets_publies=(4, 4, 0))
lewis('HCl', [('H', 0), ('Cl', 3)], [(0, 1, 1)])
lewis('H+', [('H', 0)], [], charge=1, lacunes=(0,))
lewis('H3O+', [('O', 1)] + [('H', 0)] * 3, [(0, k, 1) for k in range(1, 4)], charge=1, doublets_publies=(4, 3, 1))
lewis('Na+', [('Na', 0)], [], charge=1, lacunes=(0,))
lewis('NH4+', [('N', 0)] + [('H', 0)] * 4, [(0, k, 1) for k in range(1, 5)], charge=1, doublets_publies=(4, 4, 0))
lewis('Cl-', [('Cl', 4)], [], charge=-1)
lewis('OH-', [('O', 3), ('H', 0)], [(0, 1, 1)], charge=-1, doublets_publies=(4, 1, 3))
lewis('O2-', [('O', 4)], [], charge=-2)
lewis('BH3 (lacune)', [('B', 0)] + [('H', 0)] * 3, [(0, k, 1) for k in range(1, 4)], lacunes=(0,))
lewis('AlCl3 (lacune)', [('Al', 0)] + [('Cl', 3)] * 3, [(0, k, 1) for k in range(1, 4)], lacunes=(0,))
# Exercice 2 : schémas à vérifier
lewis('ex2 méthanol CH3OH', [('C', 0), ('O', 2)] + [('H', 0)] * 4,
      [(0, 1, 1), (0, 2, 1), (0, 3, 1), (0, 4, 1), (1, 5, 1)], doublets_publies=(7, 5, 2))
lewis('ex2 éthène C2H4', [('C', 0), ('C', 0)] + [('H', 0)] * 4,
      [(0, 1, 2), (0, 2, 1), (0, 3, 1), (1, 4, 1), (1, 5, 1)], doublets_publies=(6, 6, 0))
lewis('ex2 cyanure d hydrogène HCN', [('H', 0), ('C', 0), ('N', 1)], [(0, 1, 1), (1, 2, 3)], doublets_publies=(5, 4, 1))
lewis('ex2 peroxyde d hydrogène H2O2', [('H', 0), ('O', 2), ('O', 2), ('H', 0)], [(0, 1, 1), (1, 2, 1), (2, 3, 1)],
      doublets_publies=(7, 3, 4))
# Exercices 7 à 15
lewis('ex7 méthanal CH2O', [('C', 0), ('O', 2), ('H', 0), ('H', 0)], [(0, 1, 2), (0, 2, 1), (0, 3, 1)],
      doublets_publies=(6, 4, 2))
lewis('ex10 trichlorométhane CHCl3', [('C', 0), ('H', 0)] + [('Cl', 3)] * 3, [(0, k, 1) for k in range(1, 5)],
      doublets_publies=(13, 4, 9))
lewis('ex10 tétrachlorométhane CCl4', [('C', 0)] + [('Cl', 3)] * 4, [(0, k, 1) for k in range(1, 5)],
      doublets_publies=(16, 4, 12))
lewis('ex11 éthanol CH3-CH2-OH', [('C', 0), ('C', 0), ('O', 2)] + [('H', 0)] * 6,
      [(0, 1, 1), (1, 2, 1), (0, 3, 1), (0, 4, 1), (0, 5, 1), (1, 6, 1), (1, 7, 1), (2, 8, 1)], doublets_publies=(10, 8, 2))
lewis('ex11 méthoxyméthane CH3-O-CH3', [('C', 0), ('O', 2), ('C', 0)] + [('H', 0)] * 6,
      [(0, 1, 1), (1, 2, 1), (0, 3, 1), (0, 4, 1), (0, 5, 1), (2, 6, 1), (2, 7, 1), (2, 8, 1)], doublets_publies=(10, 8, 2))
lewis('ex13 dichlorodifluorométhane CCl2F2', [('C', 0), ('Cl', 3), ('Cl', 3), ('F', 3), ('F', 3)],
      [(0, k, 1) for k in range(1, 5)], doublets_publies=(16, 4, 12))
lewis('ex13 difluorométhane CH2F2', [('C', 0), ('H', 0), ('H', 0), ('F', 3), ('F', 3)], [(0, k, 1) for k in range(1, 5)],
      doublets_publies=(10, 4, 6))
lewis('ex14 monoxyde de carbone CO', [('C', 1), ('O', 1)], [(0, 1, 3)], doublets_publies=(5, 3, 2))
lewis('ex15 éthyne C2H2', [('H', 0), ('C', 0), ('C', 0), ('H', 0)], [(0, 1, 1), (1, 2, 3), (2, 3, 1)],
      doublets_publies=(5, 5, 0))
lewis('ex15 chlorométhane CH3Cl', [('C', 0), ('Cl', 3)] + [('H', 0)] * 3, [(0, k, 1) for k in range(1, 5)],
      doublets_publies=(7, 4, 3))


# Programme du cours
def sortie_de(fonction):
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        fonction()
    return tampon.getvalue().strip()


valence = {'H': 1, 'C': 4, 'N': 5, 'O': 6, 'Cl': 7}


def doublets(atomes, charge=0):
    ne = 0
    for symbole, nombre in atomes.items():
        ne = ne + nombre * valence[symbole]
    ne = ne - charge
    return ne // 2


def programme():
    print(doublets({'H': 2, 'O': 1}))
    print(doublets({'C': 1, 'O': 2}))
    print(doublets({'N': 1, 'H': 4}, charge=1))
    print(doublets({'O': 1, 'H': 1}, charge=-1))


s = sortie_de(programme)
print('   cours programme :', s.replace('\n', ' | '))
if s != '4\n8\n4\n4':
    ECHECS.append('cours programme')
for nom, args, attendu in (('ex6 NH3', ({'N': 1, 'H': 3},), 4), ('ex6 CH4', ({'C': 1, 'H': 4},), 4),
                           ('ex6 H3O+', ({'H': 3, 'O': 1}, 1), 4), ('ex6 Cl-', ({'Cl': 1}, -1), 4),
                           ('ex6 HCN', ({'H': 1, 'C': 1, 'N': 1},), 5), ('ex6 C2H6O', ({'C': 2, 'H': 6, 'O': 1},), 10)):
    verifie(f"{nom} doublets", doublets(*args), attendu, 0)
verifie("ex6 NO2 : 17 électrons, nombre impair", 5 + 2 * 6, 17, 0)

# Électronégativités et polarité des liaisons (seuil : écart supérieur ou égal à 0,4)
for a, b, d, polaire in (('H', 'Cl', 0.96, True), ('C', 'H', 0.35, False), ('O', 'H', 1.24, True), ('C', 'O', 0.89, True),
                         ('C', 'Cl', 0.61, True), ('N', 'H', 0.84, True), ('H', 'H', 0.0, False), ('C', 'F', 1.43, True),
                         ('C', 'C', 0.0, False), ('Na', 'Cl', 2.23, True)):
    ecart = abs(CHI[a] - CHI[b])
    verifie(f"écart d'électronégativité {a}-{b}", ecart, d, 0.005)
    if (ecart >= 0.4) != polaire:
        ECHECS.append(f'polarité {a}-{b}')

# Défi D06
cos_t = (3 + 3 - 8) / (2 * 3)
verifie("D06 cosinus de l'angle tétraédrique", cos_t, -1 / 3, 1e-12)
verifie("D06 angle tétraédrique (°)", math.degrees(math.acos(cos_t)), 109.5, 0.05)
verifie("D06 côté du cube : diagonale d'une face (unités)", math.sqrt(8), 2 * math.sqrt(2), 1e-12)
verifie("D06 demi-diagonale du cube (unités)", math.sqrt(3), 1.732, 0.0005)
verifie("D06 cos(52,25°)", math.cos(math.radians(104.5 / 2)), 0.612, 0.0005)
verifie("D06 moment dipolaire de l'eau (D)", 2 * 1.51 * math.cos(math.radians(104.5 / 2)), 1.85, 0.005)
verifie("D06 moment de l'eau s'il était linéaire (D)", 2 * 1.51 * math.cos(math.radians(90)), 0, 1e-12)
verifie("D06 moment de l'eau à 109,5° (D)", 2 * 1.51 * math.cos(math.radians(109.47 / 2)), 1.74, 0.005)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nTous les schémas de Lewis, électronégativités, sorties et calculs du chapitre 6 et du défi D06 sont vérifiés.")
