"""Vérification des résultats numériques du chapitre 8 (piles et oxydoréduction) et du défi D08.

Lancer : python -I -X utf8 verifications/chapitre_08.py
"""
import io
import re
from contextlib import redirect_stdout
from math import log10

ECHECS = []
F = 96500
NA = 6.02e23
AN = 3.156e7


def verifie(nom, calcule, publie, tol):
    ok = abs(calcule - publie) <= tol
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def composition(formule):
    """Nombre d'atomes de chaque élément d'une formule simple, par exemple C6H8O6, MnO4 ou Ag2O."""
    atomes = {}
    for symbole, nombre in re.findall(r'([A-Z][a-z]?)(\d*)', formule):
        atomes[symbole] = atomes.get(symbole, 0) + int(nombre or 1)
    return atomes


def bilan(nom, reactifs, produits):
    """reactifs, produits : listes de (coefficient, formule, charge) ; l'électron s'écrit (n, 'e', -1)."""
    def total(cote):
        atomes, charge = {}, 0
        for coef, formule, q in cote:
            charge += coef * q
            if formule != 'e':
                for symbole, nombre in composition(formule).items():
                    atomes[symbole] = atomes.get(symbole, 0) + coef * nombre
        return atomes, charge
    ok = total(reactifs) == total(produits)
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:58s} conservation des éléments et des charges")
    if not ok:
        ECHECS.append(nom)


def nernst(e0, n, c):
    """Potentiel d'une électrode métallique (hors programme), pour contrôler les tensions à vide publiées."""
    return e0 + 0.05916 / n * log10(c)


# Demi-équations et équations publiées
bilan("ex1 Ag+/Ag", [(1, 'Ag', 1), (1, 'e', -1)], [(1, 'Ag', 0)])
bilan("ex1 Fe3+/Fe2+", [(1, 'Fe', 3), (1, 'e', -1)], [(1, 'Fe', 2)])
bilan("ex1 I2/I-", [(1, 'I2', 0), (2, 'e', -1)], [(2, 'I', -1)])
bilan("ex1 O2/H2O", [(1, 'O2', 0), (4, 'H', 1), (4, 'e', -1)], [(2, 'H2O', 0)])
bilan("ex1 H+/H2", [(2, 'H', 1), (2, 'e', -1)], [(1, 'H2', 0)])
bilan("ex1 MnO4-/Mn2+", [(1, 'MnO4', -1), (8, 'H', 1), (5, 'e', -1)], [(1, 'Mn', 2), (4, 'H2O', 0)])
bilan("ex1 fer(II) + dioxygène", [(4, 'Fe', 2), (1, 'O2', 0), (4, 'H', 1)], [(4, 'Fe', 3), (2, 'H2O', 0)])
bilan("ex1 permanganate + fer(II)", [(1, 'MnO4', -1), (5, 'Fe', 2), (8, 'H', 1)], [(1, 'Mn', 2), (5, 'Fe', 3), (4, 'H2O', 0)])
bilan("ex1-2-3 cuivre + ions argent", [(1, 'Cu', 0), (2, 'Ag', 1)], [(1, 'Cu', 2), (2, 'Ag', 0)])
bilan("cours acide ascorbique (oxydation)", [(1, 'C6H8O6', 0)], [(1, 'C6H6O6', 0), (2, 'H', 1), (2, 'e', -1)])
bilan("cours diiode + acide ascorbique", [(1, 'I2', 0), (1, 'C6H8O6', 0)], [(2, 'I', -1), (1, 'C6H6O6', 0), (2, 'H', 1)])
bilan("cours ClO-/Cl-", [(1, 'ClO', -1), (2, 'H', 1), (2, 'e', -1)], [(1, 'Cl', -1), (1, 'H2O', 0)])
bilan("cours sodium + eau", [(2, 'Na', 0), (2, 'H2O', 0)], [(2, 'Na', 1), (2, 'HO', -1), (1, 'H2', 0)])
bilan("cours Daniell", [(1, 'Cu', 2), (1, 'Zn', 0)], [(1, 'Cu', 0), (1, 'Zn', 2)])
bilan("ex5 eau de Javel acidifiée", [(1, 'ClO', -1), (1, 'Cl', -1), (2, 'H', 1)], [(1, 'Cl2', 0), (1, 'H2O', 0)])
bilan("ex7 anode Zn/ZnO", [(1, 'Zn', 0), (2, 'HO', -1)], [(1, 'ZnO', 0), (1, 'H2O', 0), (2, 'e', -1)])
bilan("ex7 cathode Ag2O/Ag", [(1, 'Ag2O', 0), (1, 'H2O', 0), (2, 'e', -1)], [(2, 'Ag', 0), (2, 'HO', -1)])
bilan("ex7 bilan", [(1, 'Zn', 0), (1, 'Ag2O', 0)], [(1, 'ZnO', 0), (2, 'Ag', 0)])
bilan("ex9 cathode O2/HO-", [(1, 'O2', 0), (2, 'H2O', 0), (4, 'e', -1)], [(4, 'HO', -1)])
bilan("ex9 bilan zinc-air", [(2, 'Zn', 0), (1, 'O2', 0)], [(2, 'ZnO', 0)])
bilan("ex10 H2O/H2", [(2, 'H2O', 0), (2, 'e', -1)], [(1, 'H2', 0), (2, 'HO', -1)])
bilan("ex10 Mg2+/Mg", [(1, 'Mg', 2), (2, 'e', -1)], [(1, 'Mg', 0)])
bilan("ex12 lithium-iode", [(2, 'Li', 0), (1, 'I2', 0)], [(2, 'LiI', 0)])
bilan("ex13 anode H2", [(1, 'H2', 0)], [(2, 'H', 1), (2, 'e', -1)])
bilan("ex13 bilan", [(2, 'H2', 0), (1, 'O2', 0)], [(2, 'H2O', 0)])
bilan("ex15 fer + ions cuivre(II)", [(1, 'Fe', 0), (1, 'Cu', 2)], [(1, 'Fe', 2), (1, 'Cu', 0)])

# Constantes et tensions à vide (contrôle avec les potentiels standard, hors programme)
verifie("K(Cu2+ + Zn) : 10^(2 x 1,103 / 0,05916)", 10 ** (2 * 1.103 / 0.05916) / 1e37, 1.9, 0.05)
verifie("ex2-3 K(Cu + 2 Ag+) (en 1e15)", 10 ** (2 * (0.7996 - 0.34) / 0.05916) / 1e15, 4, 0.6)
e_zn, e_fe = nernst(-0.76, 2, 0.10), nernst(-0.44, 2, 0.10)
e_cu, e_ag = nernst(0.34, 2, 0.10), nernst(0.7996, 1, 0.10)
verifie("cours Daniell : tension à vide (V)", e_cu - e_zn, 1.10, 0.005)
verifie("ex3-15 cuivre-argent : tension à vide (V)", e_ag - e_cu, 0.43, 0.005)
verifie("ex15 fer-cuivre : tension à vide (V)", e_cu - e_fe, 0.78, 0.005)
verifie("ex15 zinc-argent prévu : 1,10 + 0,43 (V)", 1.10 + 0.43, 1.53, 1e-9)
verifie("ex15 zinc-argent avec les potentiels (V)", e_ag - e_zn, 1.53, 0.005)
verifie("ex15 zinc-fer prévu : 1,10 - 0,78 (V)", 1.10 - 0.78, 0.32, 1e-9)
verifie("ex15 zinc-fer avec les potentiels (V)", e_fe - e_zn, 0.32, 0.005)
verifie("ex14 tension de la pile de concentration (V)", nernst(0.34, 2, 0.10) - nernst(0.34, 2, 0.010), 0.030, 0.0005)

# L'essentiel : exemple de capacité et programme
nzn = 2.0 / 65.4
verifie("cours n(Zn) pour 2,0 g (mol)", nzn, 3.1e-2, 0.05e-2)
q = 2 * 5.0e-3 * F
verifie("cours capacité (C)", q, 965, 0.5)
verifie("cours capacité (A.h)", q / 3600, 0.27, 0.005)
verifie("cours durée à 20 mA (s)", q / 0.020, 4.8e4, 0.05e4)
verifie("cours durée à 20 mA (h)", q / 0.020 / 3600, 13, 0.5)
F_PROG = 96500


def capacite(reactifs, n):
    x_max = min(qte / a for qte, a in reactifs)
    return n * x_max * F_PROG


tampon = io.StringIO()
with redirect_stdout(tampon):
    Q = capacite([(5.0e-3, 1), (3.1e-2, 1)], 2)
    print(round(Q), "C")
    print(round(Q / 3600, 2), "A.h")
    print(round(Q / 0.020 / 3600, 1), "h")
sortie = tampon.getvalue().strip().splitlines()
print('   cours programme :', sortie)
if sortie != ['965 C', '0.27 A.h', '13.4 h']:
    ECHECS.append('cours programme de capacité')
verifie("cours figure : durée de fonctionnement (h)", 965 / 0.020 / 3600, 13.40, 0.005)

# Exercice 2 : arbre de Diane
nag = 0.0500 * 0.100
verifie("ex2 m(Ag) (g)", nag * 107.9, 0.540, 0.0005)
verifie("ex2 m(Cu) (g)", nag / 2 * 63.5, 0.159, 0.0005)
# Exercice 3
verifie("ex3 Qr,i", 0.10 / 0.10 ** 2, 10, 1e-9)
# Exercice 6 : pile Daniell
verifie("ex6 n(Zn) (mol)", 5.0 / 65.4, 7.6e-2, 0.05e-2)
q6 = 2 * 0.100 * 0.10 * F
verifie("ex6 capacité (C)", q6, 1.93e3, 0.005e3)
verifie("ex6 capacité (mA.h)", q6 / 3.6, 536, 0.5)
verifie("ex6 durée à 50 mA (s)", q6 / 0.050, 3.86e4, 0.005e4)
verifie("ex6 durée à 50 mA (h)", q6 / 0.050 / 3600, 10.7, 0.05)
verifie("ex6 masse de cuivre déposée, 0,635 arrondi à 0,64 (g)", 0.010 * 63.5, 0.64, 0.0051)
# Exercice 7 : pile bouton à l'oxyde d'argent
nzn7, nag2o = 0.034 / 65.4, 0.15 / 231.7
verifie("ex7 n(Zn) (mol)", nzn7, 5.2e-4, 0.05e-4)
verifie("ex7 n(Ag2O) (mol)", nag2o, 6.5e-4, 0.05e-4)
q7 = 2 * nzn7 * F
verifie("ex7 capacité (C)", q7, 100, 1)
verifie("ex7 capacité (mA.h)", q7 / 3.6, 28, 0.5)
verifie("ex7 durée (s)", q7 / 1.5e-6, 6.7e7, 0.05e7)
verifie("ex7 durée (ans)", q7 / 1.5e-6 / AN, 2, 0.15)
# Exercice 8 : suivi de l'usure (données calculées pour I = 0,100 A, arrondies au millième)
pente_th = -0.100 * 3600 / (2 * F * 0.100)
t8 = [0, 1, 2, 3, 4]
c8 = [0.100, 0.081, 0.063, 0.044, 0.025]
for t, c in zip(t8, c8):
    verifie(f"ex8 donnée à t = {t} h (mol/L)", 0.100 + pente_th * t, c, 0.0005)
tm, cm = sum(t8) / 5, sum(c8) / 5
pente = sum((t - tm) * (c - cm) for t, c in zip(t8, c8)) / sum((t - tm) ** 2 for t in t8)
verifie("ex8 pente de la droite moyenne (mol/L/h)", pente, -0.0187, 0.00005)
verifie("ex8 ordonnée à l'origine (mol/L)", cm - pente * tm, 0.1000, 0.0005)
i8 = 2 * F * 0.100 * abs(pente) / 3600
verifie("ex8 intensité (A)", i8, 0.10, 0.005)
verifie("ex8 date d'épuisement (h)", 0.100 / abs(pente), 5.3, 0.05)
verifie("ex8 capacité (C)", 2 * F * 1.00e-2, 1.9e3, 0.05e3)
verifie("ex8 capacité (A.h)", 2 * F * 1.00e-2 / 3600, 0.54, 0.005)
verifie("ex8 [Cu2+] pour Qr = K (1e-38 mol/L)", 0.200 / 1.9e37 / 1e-38, 1, 0.1)
# Exercice 9 : pile zinc-air
q9 = 620 * 3.6
verifie("ex9 capacité (C)", q9, 2232, 1e-9)
verifie("ex9 n(e-) (mol)", q9 / F, 2.31e-2, 0.005e-2)
verifie("ex9 n(Zn) (mol)", q9 / F / 2, 1.16e-2, 0.005e-2)
verifie("ex9 m(Zn) (g)", q9 / F / 2 * 65.4, 0.76, 0.005)
verifie("ex9 durée (h)", 620 / 1.6, 388, 0.5)
verifie("ex9 durée (jours)", 620 / 1.6 / 16, 24, 0.5)
# Exercice 10 : sodium
verifie("ex10 n(Na) (mol)", 0.23 / 23.0, 1.0e-2, 1e-9)
verifie("ex10 V(H2) (L)", 0.23 / 23.0 / 2 * 24, 0.12, 1e-9)
# Exercice 11 : simulation (sortie publiée)
tampon = io.StringIO()
with redirect_stdout(tampon):
    F11, I11, dt = 96500, 0.050, 60
    n_cu, n_zn = 5.0e-3, 5.0e-3
    t = 0
    while n_cu > 0:
        dx = I11 * dt / (2 * F11)
        n_cu = n_cu - dx
        n_zn = n_zn + dx
        t = t + dt
    print(t, round(t / 3600, 2), round(n_zn, 4))
sortie = tampon.getvalue().strip()
print('   ex11 sortie :', sortie)
if sortie != '19320 5.37 0.01':
    ECHECS.append('ex11 sortie du programme')
verifie("ex11 capacité (C)", 2 * F * 5.0e-3, 965, 0.5)
verifie("ex11 durée exacte (s)", 2 * F * 5.0e-3 / 0.050, 19300, 1e-6)
# Exercice 12 : stimulateur cardiaque
q12 = 1.0 * 3600
verifie("ex12 durée (s)", q12 / 10e-6, 3.6e8, 1)
verifie("ex12 durée (ans)", q12 / 10e-6 / AN, 11, 0.5)
ne12 = q12 / F
verifie("ex12 n(e-) (mol)", ne12, 3.73e-2, 0.005e-2)
verifie("ex12 m(Li) (g)", ne12 * 6.94, 0.26, 0.005)
verifie("ex12 m(I2) (g)", ne12 / 2 * 2 * 126.9, 4.7, 0.05)
verifie("ex12 m(Zn) (g)", ne12 / 2 * 65.4, 1.2, 0.05)
verifie("ex12 rapport des masses zinc/lithium (près de 5)", (ne12 / 2 * 65.4) / (ne12 * 6.94), 4.7, 0.05)
# Exercice 13 : voiture à hydrogène
nh2 = 5600 / 2.0
verifie("ex13 n(H2) (mol)", nh2, 2.8e3, 1e-9)
q13 = 2 * nh2 * F
verifie("ex13 charge (C)", q13, 5.4e8, 0.05e8)
e13 = q13 * 0.70
verifie("ex13 énergie (J)", e13, 3.8e8, 0.05e8)
verifie("ex13 énergie (kW.h)", e13 / 3.6e6, 105, 0.5)
verifie("ex13 consommation (kW.h/100 km)", e13 / 3.6e6 / 6.5, 16, 0.5)
verifie("ex13 masse d'eau (kg)", nh2 * 18.0 / 1000, 50, 0.5)
# Exercice 14 : pile de concentration
verifie("ex14 Qr,i", 1.0e-2 / 0.10, 0.10, 1e-12)
x14 = (0.10 - 0.010) / 2
verifie("ex14 avancement volumique final (mol/L)", x14, 0.045, 1e-12)
verifie("ex14 concentration finale (mol/L)", 0.010 + x14, 0.055, 1e-12)
verifie("ex14 n(e-) (mol)", 2 * x14 * 0.100, 9.0e-3, 1e-12)
verifie("ex14 capacité (C)", 2 * x14 * 0.100 * F, 8.7e2, 0.05e2)
verifie("ex14 masse de cuivre perdue (g)", x14 * 0.100 * 63.5, 0.29, 0.005)

# Défi D08 : tension à vide au cours de la décharge (relation admise U = 1,10 - 0,0296 log Qr)
tampon = io.StringIO()
with redirect_stdout(tampon):
    Fd, V, c = 96500, 0.100, 0.10
    Qmax = 2 * Fd * c * V
    for f in (0.5, 0.9, 0.99, 0.9999):
        qd = f * Qmax
        cu = c - qd / (2 * Fd * V)
        zn = c + qd / (2 * Fd * V)
        print(f, round(1.10 - 0.0296 * log10(zn / cu), 3))
sortie = tampon.getvalue().strip().splitlines()
print('   D08 sorties :', sortie)
if sortie != ['0.5 1.086', '0.9 1.062', '0.99 1.032', '0.9999 0.973']:
    ECHECS.append('D08 sorties du programme')
verifie("D08 log K = 1,10/0,0296", 1.10 / 0.0296, 37.2, 0.05)
kd = 10 ** (1.10 / 0.0296)
verifie("D08 K (en 1e37)", kd / 1e37, 1.5, 0.05)
verifie("D08 tension redonnant K = 1,9e37 (V)", 0.0296 * log10(1.9e37), 1.103, 0.0005)
verifie("D08 capacité (C)", 2 * F * 0.10 * 0.100, 1930, 1e-6)
verifie("D08 capacité (A.h)", 2 * F * 0.10 * 0.100 / 3600, 0.54, 0.005)
verifie("D08 Qr à mi-décharge", 0.15 / 0.05, 3, 1e-9)
cu0 = 0.20 / kd
verifie("D08 [Cu2+] pour U = 0 (1e-38 mol/L)", cu0 / 1e-38, 1, 0.5)
verifie("D08 nombre d'ions dans 100 mL (1e-16)", cu0 * 0.100 * NA / 1e-16, 8, 0.5)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs du chapitre 8 et du défi D08 sont vérifiées.")
