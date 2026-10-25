"""Vérification du chapitre 12 (Description d'un fluide au repos) et du défi D12.

Lancer : python -I -X utf8 verifications/chapitre_12.py
"""
import io
import math
from contextlib import redirect_stdout

ECHECS = []
G, PATM = 9.81, 1.013e5
RHO_EAU, RHO_MER, RHO_HG, RHO_AIR = 1.00e3, 1.03e3, 13.6e3, 1.2


def verifie(nom, calcule, publie, tol_rel=0.006):
    ok = abs(calcule - publie) <= tol_rel * abs(publie) + 1e-300
    print(f"{'ok ' if ok else 'ÉCHEC'} {nom:60s} calculé {calcule:.6g}  publié {publie}")
    if not ok:
        ECHECS.append(nom)


def sortie_de(fonction):
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        fonction()
    return tampon.getvalue().strip()


# Cours
verifie("cours force sur 1 m2 à Patm (N)", PATM * 1.0, 1.0e5, 0.02)
verifie("cours masse de poids 1,0e5 N (t)", 1.0e5 / G / 1000, 10, 0.02)
verifie("cours seringue 60 -> 20 mL (hPa)", 1013 * 60 / 20, 3039)
verifie("cours eau douce, 10 m : surpression (Pa)", RHO_EAU * G * 10, 9.81e4)
verifie("cours eau douce, 10 m : pression (Pa)", PATM + RHO_EAU * G * 10, 2.0e5, 0.01)


def programme():
    P1, V1 = 1013, 60
    for V in [60, 50, 40, 30, 20]:
        P = P1 * V1 / V
        print(V, 'mL :', round(P), 'hPa')


s = sortie_de(programme)
print('   cours programme :', s.replace('\n', ' | '))
if s != '60 mL : 1013 hPa\n50 mL : 1216 hPa\n40 mL : 1520 hPa\n30 mL : 2026 hPa\n20 mL : 3039 hPa':
    ECHECS.append('cours programme')
# Exercice 1
verifie("ex1 masse d'air d'une pièce de 50 m3 (kg)", RHO_AIR * 5 * 4 * 2.5, 60)
verifie("ex1 rapport des masses volumiques eau / air", RHO_EAU / RHO_AIR, 830, 0.01)
# Exercice 2 : fenêtre
S2 = 1.20 * 0.80
verifie("ex2 aire de la fenêtre (m2)", S2, 0.96)
verifie("ex2 force pressante (N)", PATM * S2, 9.72e4)
verifie("ex2 masse équivalente (kg)", PATM * S2 / G, 9.9e3, 0.01)
verifie("ex2 force nette, écart de 30 hPa (N)", 3000 * S2, 2.88e3)
# Exercice 3 : seringue bouchée
P3 = 1013e2 * 60 / 20
verifie("ex3 pression finale (Pa)", P3, 3.04e5)
verifie("ex3 force de l'opérateur (N)", (P3 - PATM) * 6.0e-4, 122, 0.01)
verifie("ex3 volume pour 2,0e5 Pa (mL)", 1013e2 * 60 / 2.0e5, 30.4)
# Exercice 4 : sous l'eau
verifie("ex4 piscine 2,0 m : surpression (Pa)", RHO_EAU * G * 2.0, 1.96e4)
verifie("ex4 piscine 2,0 m : pression (Pa)", PATM + RHO_EAU * G * 2.0, 1.21e5)
verifie("ex4 mer 10 m : pression (Pa)", PATM + RHO_MER * G * 10, 2.02e5)
verifie("ex4 profondeur pour 3,0e5 Pa (m)", (3.0e5 - PATM) / (RHO_MER * G), 19.7)
# Exercice 5 : vases communicants (surface à 3,0 m, A à 2,0 m, C à 0,3 m)
verifie("ex5 pression en A (Pa)", PATM + RHO_EAU * G * (3.0 - 2.0), 1.11e5)
verifie("ex5 pression en C (Pa)", PATM + RHO_EAU * G * (3.0 - 0.3), 1.28e5)


# Exercice 6 : programme pression-profondeur
def programme6():
    rho, g, P0 = 1030, 9.81, 1.013e5
    for h in range(0, 50, 10):
        P = P0 + rho * g * h
        print(h, 'm :', round(P / 1e5, 2), 'bar')


s6 = sortie_de(programme6)
print('   ex6 programme :', s6.replace('\n', ' | '))
if s6 != '0 m : 1.01 bar\n10 m : 2.02 bar\n20 m : 3.03 bar\n30 m : 4.04 bar\n40 m : 5.05 bar':
    ECHECS.append('ex6 programme')
verifie("ex6 augmentation tous les 10 m (bar)", RHO_MER * G * 10 / 1e5, 1.01)
verifie("ex6 profondeur pression triple (m)", 2 * PATM / (RHO_MER * G), 20.1)
verifie("ex6 lac : 20 m (bar)", (0.80e5 + 1000 * 9.81 * 20) / 1e5, 2.76, 0.002)
# Exercice 7 : poumons du plongeur
P7 = PATM + RHO_MER * G * 20
verifie("ex7 pression à 20 m (Pa)", P7, 3.03e5)
verifie("ex7 volume des poumons à 20 m (L)", 6.0 * PATM / P7, 2.0)
verifie("ex7 volume à la surface d'un air pris à 20 m (L)", 6.0 * P7 / PATM, 18, 0.01)
for h, v in [(10, 3.0), (30, 1.5), (40, 1.2)]:
    verifie(f"ex7 volume à {h} m (L)", 6.0 * PATM / (PATM + RHO_MER * G * h), v, 0.02)
# Exercice 8 : Torricelli
verifie("ex8 pression de 760 mm de mercure (Pa)", RHO_HG * G * 0.760, 1.01e5, 0.005)
verifie("ex8 hauteur d'eau équivalente (m)", PATM / (RHO_EAU * G), 10.3)
verifie("ex8 760 mm de mercure, en hPa", RHO_HG * G * 0.760 / 100, 1014, 0.001)
# Exercice 9 : altitude
verifie("ex9 écart pour 100 m (Pa)", RHO_AIR * G * 100, 1.18e3, 0.01)
verifie("ex9 tour de 300 m (hPa)", RHO_AIR * G * 300 / 100, 35, 0.01)
verifie("ex9 un étage de 3 m (hPa)", RHO_AIR * G * 3 / 100, 0.35, 0.01)
verifie("ex9 Mont Blanc avec rho constant (hPa)", 1013 - RHO_AIR * G * 4807 / 100, 447)
# Exercice 10 : tube en U
verifie("ex10 masse volumique de l'huile (kg/m3)", RHO_EAU * 10.8 / 12.0, 900)
verifie("ex10 pression à l'interface (Pa)", PATM + 900 * G * 0.120, 1.024e5, 0.001)
# Exercice 11 : test de la loi de Mariotte
V11 = [60, 50, 40, 30, 24, 20]
P11 = [1012, 1218, 1515, 2031, 2526, 3046]
PV = [p * v for p, v in zip(P11, V11)]
print('   ex11 produits P x V :', PV)
moy = sum(PV) / len(PV)
verifie("ex11 produit moyen (hPa.mL)", moy, 6.08e4)
verifie("ex11 écart relatif maximal (%)", max(abs(x - moy) / moy for x in PV) * 100, 0.3, 0.2)
verifie("ex11 pression prévue pour 15 mL (hPa)", 6.08e4 / 15, 4053)
# Exercice 12 : plongée en bouteille
P12 = 1.0e5 + RHO_MER * G * 20
verifie("ex12 pression à 20 m (bar)", P12 / 1e5, 3.02)
verifie("ex12 volume d'air à 1,0 bar (L)", 12 * 200 / 1.0, 2400)
verifie("ex12 volume utilisable (L)", 12 * (200 - 50) / 1.0, 1800)
verifie("ex12 consommation à 20 m (L/min)", 20 * 3.02, 60.4)
verifie("ex12 autonomie (min)", 1800 / 60.4, 29.8)
verifie("ex12 autonomie en surface (min)", 1800 / 20, 90)
# Exercice 13 : ballon-sonde
V13 = 1.5 * 1013 / 30
verifie("ex13 volume à 30 hPa (m3)", V13, 50.7)
verifie("ex13 rapport des volumes", V13 / 1.5, 34, 0.01)
verifie("ex13 rayon au sol (m)", (3 * 1.5 / (4 * math.pi)) ** (1 / 3), 0.71)
verifie("ex13 rayon à 30 hPa (m)", (3 * V13 / (4 * math.pi)) ** (1 / 3), 2.30)
verifie("ex13 diamètre au sol (m)", 2 * (3 * 1.5 / (4 * math.pi)) ** (1 / 3), 1.42)
verifie("ex13 diamètre à 30 hPa (m)", 2 * (3 * V13 / (4 * math.pi)) ** (1 / 3), 4.59)
Vmax = 4 / 3 * math.pi * 3.0 ** 3
verifie("ex13 volume à l'éclatement (m3)", Vmax, 113)
verifie("ex13 pression à l'éclatement (hPa)", 1013 * 1.5 / Vmax, 13.4)
# Exercice 14 : château d'eau
verifie("ex14 surpression au rez-de-chaussée, 50 m (Pa)", RHO_EAU * G * 50, 4.9e5, 0.002)
verifie("ex14 surpression au dernier étage, 27 m (Pa)", RHO_EAU * G * 27, 2.65e5)
verifie("ex14 hauteur d'eau pour 3,0 bar (m)", 3.0e5 / (RHO_EAU * G), 30.6)
verifie("ex14 altitude minimale de la surface (m)", 25 + 3.0e5 / (RHO_EAU * G), 55.6)
verifie("ex14 surpression au fond de la cuve (Pa)", RHO_EAU * G * 8.0, 7.85e4)
verifie("ex14 force sur la trappe (N)", RHO_EAU * G * 8.0 * 0.50, 3.92e4)
# Exercice 15 : barrage
verifie("ex15 surpression au pied (Pa)", RHO_EAU * G * 60, 5.89e5)
verifie("ex15 surpression à mi-hauteur (Pa)", RHO_EAU * G * 30, 2.94e5)
verifie("ex15 force sur une vanne de 1 m2 au pied (N)", RHO_EAU * G * 60 * 1.0, 5.89e5)
verifie("ex15 force sur une bande de 1 m de large (N)", RHO_EAU * G * 60 / 2 * 60 * 1.0, 1.77e7)
verifie("ex15 masse équivalente (t)", RHO_EAU * G * 60 / 2 * 60 / G / 1000, 1800)
# Défi D12 : hémisphères de Magdebourg
S = math.pi * 0.25 ** 2
verifie("D12 aire du disque (m2)", S, 0.196)
verifie("D12 force, vide parfait (N)", PATM * S, 1.99e4)
verifie("D12 force par cheval, 8 chevaux (N)", PATM * S / 8, 2.5e3, 0.01)
verifie("D12 volume des hémisphères (L)", 4 / 3 * math.pi * 2.5 ** 3, 65.4)


def programme_d12():
    V, v = 65.4, 2.0
    P, n = 1.013, 0
    while P > 0.10:
        P = P * V / (V + v)
        n = n + 1
    print(n, 'coups :', round(P, 4), 'bar')


s12 = sortie_de(programme_d12)
print('   D12 programme :', s12)
if s12 != '77 coups : 0.0996 bar':
    ECHECS.append('D12 programme')
verifie("D12 pression après 1 coup (bar)", 1.013 * 65.4 / 67.4, 0.983)
verifie("D12 nombre de coups par logarithme", math.log(0.10 / 1.013) / math.log(65.4 / 67.4), 76.9, 0.002)
verifie("D12 force avec 0,10 bar résiduel (N)", (1.013 - 0.10) * 1e5 * S, 1.79e4)
verifie("D12 ventouse r = 5,0 cm (N)", PATM * math.pi * 0.05 ** 2, 796)
verifie("D12 masse équivalente, vide parfait (t)", PATM * S / G / 1000, 2.0, 0.02)
verifie("D12 masse équivalente, ventouse (kg)", PATM * math.pi * 0.05 ** 2 / G, 80, 0.02)
verifie("D12 baisse relative avec 0,10 bar (%)", 0.10 / 1.013 * 100, 10, 0.02)
verifie("D12 hauteur d'eau donnant 1,013e5 Pa (m)", PATM / (RHO_EAU * G), 10.3)

if ECHECS:
    raise SystemExit(f"{len(ECHECS)} vérification(s) en échec : {ECHECS}")
print("\nToutes les valeurs et sorties du chapitre 12 et du défi D12 sont vérifiées.")
