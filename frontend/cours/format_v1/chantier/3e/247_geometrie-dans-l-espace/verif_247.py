# -*- coding: utf-8 -*-
"""Vérification sympy de tous les calculs de la notion 247 (géométrie dans l'espace, 3e)."""
from sympy import Rational as R, pi, sqrt, N, floor, nsimplify

ok = 0
def chk(nom, val, attendu, tol=None):
    global ok
    if isinstance(attendu, bool):
        assert bool(val) is attendu, (nom, val)
    elif tol is None:
        assert nom and (nsimplify(val) - nsimplify(attendu)) == 0, (nom, val, attendu)
    else:
        assert abs(N(val) - attendu) < tol, (nom, N(val), attendu)
    ok += 1

boule = lambda r: R(4, 3) * pi * r**3
cone = lambda r, h: pi * r**2 * h / 3
cyl = lambda r, h: pi * r**2 * h

# ---- cours
chk("cours cône 4/9", cone(4, 9), 48 * pi); chk("cours cône approx", cone(4, 9), 150.8, 0.05)
chk("cours sphère r", sqrt(5**2 - 3**2), 4)
chk("cours mi-hauteur", R(1, 2)**3, R(1, 8))
chk("cours cylindre patron", 2 * pi * 2, 4 * pi); chk("4pi", 4 * pi, 12.6, 0.05)
chk("cours pyramide 6x6x4", R(36 * 4, 3), 48)
chk("cours maquette k3", 2**3 * 30, 240)                 # aquarium de 30 L agrandi de rapport 2
# ---- 2422
chk("2422 V", 8 * 5 * 3, 120); chk("2422 aires", 8 * 3 + 8 * 5 + 5 * 3, 79); chk("2422 tot", 2 * 79, 158)
chk("2422 L", R(120, 1000), R(12, 100))
# ---- 2423
chk("2423 base", pi * 9, 28.3, 0.05); chk("2423 V", cyl(3, 10), 90 * pi); chk("2423 arr", cyl(3, 10), 283, 0.5)
chk("2423 2h", cyl(3, 20) / cyl(3, 10), 2); chk("2423 2r", cyl(6, 10) / cyl(3, 10), 4)
# ---- 2424
chk("2424 B", 36, 36); chk("2424 V", R(36 * 9, 3), 108); chk("2424 pave", 36 * 9, 324); chk("2424 h", R(144 * 3, 36), 12)
# ---- 2425
chk("2425 V", cone(4, 9), 48 * pi); chk("2425 arr", cone(4, 9), 151, 0.5); chk("2425 cyl", cyl(4, 9), 144 * pi)
# ---- 2426
chk("2426 V", boule(3), 36 * pi); chk("2426 arr", boule(3), 113.1, 0.05); chk("2426 A", 4 * pi * 9, 36 * pi)
chk("2426 V6", boule(6), 288 * pi); chk("2426 k3", boule(6) / boule(3), 8); chk("2426 A6", 4 * pi * 36, 144 * pi)
# ---- 2427
chk("2427 A", 6 * 4, 24); chk("2427 V", 2**3, 8)
# ---- 2428 (patron du cylindre r = 2, h = 5)
chk("2428 L", 2 * pi * 2, 12.6, 0.05); chk("2428 Alat", 4 * pi * 5, 20 * pi); chk("2428 Alat arr", 20 * pi, 62.8, 0.05)
chk("2428 Atot", 20 * pi + 2 * pi * 4, 28 * pi); chk("2428 Atot arr", 28 * pi, 88.0, 0.05)
chk("2428 V", cyl(2, 5), 20 * pi); chk("2428 section", 4 * 5, 20)
# ---- 2429
chk("2429 S", 8 * 5, 40); chk("2429 V", 8 * 5 * 6, 240); chk("2429 m1", 40 * 2, 80); chk("2429 m2", 40 * 4, 160)
chk("2429 S2", 8 * 6, 48)
# ---- 2430
chk("2430 centre", (R(6, 2), R(4, 2), R(3, 2)) == (3, 2, R(3, 2)), True)
# ---- 2431
chk("2431 lon", 20 + 50, 70); chk("2431 lat", 35 + 35, 70)
# ---- 2432
chk("2432 HM", sqrt(25 - 9), 4); chk("2432 A", pi * 16, 50.3, 0.05); chk("2432 d", sqrt(25 - 9), 4)
# ---- 2433
Vr = cyl(1, 2) + boule(1) / 2
chk("2433 cyl", cyl(1, 2), 2 * pi); chk("2433 demi", boule(1) / 2, R(2, 3) * pi); chk("2433 tot", Vr, R(8, 3) * pi)
chk("2433 L", Vr * 1000, 8378, 0.5); chk("2433 min", Vr * 1000 / 20, 418.9, 0.05)
# ---- 2434
chk("2434 B", boule(5), R(500, 3) * pi); chk("2434 cav", boule(2), R(32, 3) * pi); chk("2434 m", boule(5) - boule(2), 156 * pi)
chk("2434 arr", 156 * pi, 490, 0.5); chk("2434 masse", 156 * pi * R(78, 10), 3823, 0.5)
# ---- 2435
chk("2435 V", cone(6, 12), 144 * pi); chk("2435 S", pi * 9, 9 * pi); chk("2435 petit", cone(3, 6), 18 * pi)
chk("2435 petit k3", 144 * pi * R(1, 8), 18 * pi); chk("2435 tronc", 126 * pi, 396, 0.5); chk("2435 frac", R(126, 144), R(7, 8))
# ---- 2436
Vs = cyl(3, 8) + cone(3, 2)
chk("2436 cyl", cyl(3, 8), 72 * pi); chk("2436 cone", cone(3, 2), 6 * pi); chk("2436 tot", Vs, 78 * pi)
chk("2436 arr", Vs, 245, 0.5); chk("2436 ble", Vs * R(8, 10) * R(75, 100), 147, 0.5)
chk("2436 camions", floor(N(Vs * R(6, 10) / 25)) + 1, 6)
# ---- 2437
chk("2437 AF", sqrt(36 + 36), 6 * sqrt(2)); chk("2437 AF arr", 6 * sqrt(2), 8.49, 0.005)
chk("2437 AG", sqrt(72 + 36), 6 * sqrt(3)); chk("2437 AG arr", 6 * sqrt(3), 10.39, 0.005)
chk("2437 V", 6**3, 216); chk("2437 boule", boule(3), 36 * pi); chk("2437 %", boule(3) / 216 * 100, 52.4, 0.05)
chk("2437 frac", boule(3) / 216, pi / 6)
# ---- 2438
chk("2438 cone", cone(3, 10), 30 * pi); chk("2438 demi", boule(3) / 2, 18 * pi); chk("2438 tot", 48 * pi, 150.8, 0.05)
chk("2438 n", floor(2000 / N(48 * pi)), 13); chk("2438 benef", R(13 * 25, 10) - 12, R(205, 10))
# ---- 2439
SI = sqrt(R(216, 10)**2 + R(175, 10)**2)
chk("2439 V", R(35**2) * R(216, 10) / 3, 8820); chk("2439 OI", R(35, 2), R(175, 10)); chk("2439 SI", SI, 27.8, 0.05)
chk("2439 SI2", R(216, 10)**2 + R(175, 10)**2, R(77281, 100))
chk("2439 aire", 35 * SI / 2, 486.5, 0.05); chk("2439 4 faces", 4 * 35 * SI / 2, 1946, 0.5)
chk("2439 4 faces arrondi", 4 * R(4865, 10), 1946)
# ---- 2440
chk("2440 eq", 2 * pi * 6371, 40030, 0.5); chk("2440 1deg", 2 * pi * 6371 / 360, 111.2, 0.05)
chk("2440 30deg", 2 * pi * 6371 * 30 / 360, 3336, 0.5); chk("2440 A", 4 * pi * 6371**2 / 10**8, 5.10, 0.005)
chk("2440 V", boule(6371) / 10**12, 1.08, 0.005)
# ---- 2441
chk("2441 V", cone(4, 12), 64 * pi); chk("2441 arr", 64 * pi, 201, 0.5); chk("2441 k", R(10, 12), R(5, 6))
chk("2441 r", 4 * R(5, 6), R(10, 3)); chk("2441 Vl", 64 * pi * R(5, 6)**3, R(1000, 27) * pi)
chk("2441 Vl direct", cone(R(10, 3), 10), R(1000, 27) * pi); chk("2441 Vl arr", R(1000, 27) * pi, 116.4, 0.05)
chk("2441 %", R(125, 216) * 100, 57.9, 0.05)
# ---- 2442
chk("2442 cont", 80 * 40 * 50, 160000); chk("2442 eau", 80 * 40 * 45, 144000); chk("2442 min", R(144, 6), 24)
chk("2442 boule", boule(6), 288 * pi); chk("2442 arr", 288 * pi, 905, 0.5)
chk("2442 h", 288 * pi / (80 * 40), 0.28, 0.005); chk("2442 niveau", 45 + 288 * pi / 3200 < 50, True)
# ---- nouveau-1 (pyramide 9 × 9, hauteur 12, coupée à SO' = 4)
chk("n1 V", R(81 * 12, 3), 324); chk("n1 k", R(4, 12), R(1, 3)); chk("n1 cote", 9 * R(1, 3), 3)
chk("n1 aire", 81 * R(1, 3)**2, 9); chk("n1 petit", 324 * R(1, 27), 12); chk("n1 petit direct", R(9 * 4, 3), 12)
chk("n1 tronc", 324 - 12, 312); chk("n1 frac", R(312, 324), R(26, 27)); chk("n1 aire base/section", R(81, 9), 9)

# ---- valeurs intermédiaires écrites dans les corrigés
chk("2433 V num", R(8, 3) * pi, 8.37758, 0.000005); chk("2433 h min", Vr * 1000 / 20 - 6 * 60, 58.9, 0.05)
chk("2436 ble vol", R(624, 10) * pi, 196.04, 0.005); chk("2436 masse", R(468, 10) * pi, 147.03, 0.005)
chk("2436 div", R(468, 10) * pi / 25, 5.88, 0.005)
chk("2438 div", 2000 / (48 * pi), 13.26, 0.005)
chk("2439 SI num", SI, 27.80, 0.005); chk("2439 aire arr", R(35 * 278, 20), R(4865, 10))
chk("2440 eq num", 12742 * pi, 40030.2, 0.05); chk("2440 1deg num", 12742 * pi / 360, 111.19, 0.005)
chk("2440 30 num", 12742 * pi * 30 / 360, 3335.8, 0.05); chk("2440 A num", 4 * pi * 6371**2, 510064472, 0.5)
chk("2440 V num", boule(6371) / 10**12, 1.083, 0.0005); chk("2440 erreur", R(1112, 10) * 30, 3336)
chk("2441 r num", R(10, 3), 3.33, 0.005); chk("2441 Vl num", R(1000, 27) * pi, 116.36, 0.005)
chk("2441 k3 num", R(125, 216), 0.579, 0.0005)
chk("2442 h num", 288 * pi / 3200, 0.283, 0.0005)
chk("2437 % num", pi / 6 * 100, 52.36, 0.005); chk("2437 AF num", sqrt(72), 8.485, 0.0005); chk("2437 AG num", sqrt(108), 10.392, 0.0005)
chk("2434 masse num", 156 * pi * R(78, 10), 3822.7, 0.05); chk("2434 V num", 156 * pi, 490.09, 0.005)
chk("2435 tronc num", 126 * pi, 395.84, 0.005); chk("2425 num", 48 * pi, 150.80, 0.005)
chk("2423 num", 90 * pi, 282.74, 0.005); chk("2428 num", 4 * pi, 12.57, 0.005); chk("2428 lat num", 20 * pi, 62.83, 0.005)
chk("2428 tot num", 28 * pi, 87.96, 0.005); chk("2426 num", 36 * pi, 113.10, 0.005)
chk("2441 V num", 64 * pi, 201.06, 0.005); chk("2442 boule num", 288 * pi, 904.78, 0.005)
chk("n1 V", R(972, 3), 324)

print(f"verif_247 : {ok} contrôles, tout est juste.")
