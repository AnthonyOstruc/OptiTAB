# -*- coding: utf-8 -*-
"""Vérification sympy de toutes les valeurs numériques de la notion 245 (trigonométrie, 3e)."""
from sympy import Rational as R, sqrt, cos, sin, tan, acos, asin, atan, pi, N

deg = pi / 180
ok = 0


def d(x):
    return N(x * deg)


def angle(x):
    return N(x / deg)


def chk(nom, val, attendu, tol):
    global ok
    v = float(N(val))
    assert abs(v - attendu) <= tol, (nom, v, attendu)
    ok += 1
    print("OK %-38s %.5f ~ %s" % (nom, v, attendu))


C = lambda a: cos(a * deg)
S = lambda a: sin(a * deg)
T = lambda a: tan(a * deg)

# ---------------- cours
chk("cours cos60", C(60), 0.5, 1e-12)
chk("cours ex longueur 10 sin35", 10 * S(35), 5.74, 0.005)
chk("cours ex hyp 7/cos50", 7 / C(50), 10.9, 0.05)
chk("cours ex angle acos 0,6", acos(R(6, 10)) / deg, 53.1, 0.05)
chk("cours complementaire", 90 - acos(R(6, 10)) / deg, 36.9, 0.05)
chk("cours elevation 20 tan40 + 1,5", 20 * T(40) + R(3, 2), 18.3, 0.05)
chk("cours tan 6/8", atan(R(6, 8)) / deg, 36.9, 0.05)
# ---------------- exercices
chk("2381 cos D", R(8, 10), 0.8, 0)
chk("2381 sin D", R(6, 10), 0.6, 0)
chk("2381 tan D", R(6, 8), 0.75, 0)
chk("2381 angle D", acos(R(8, 10)) / deg, 36.87, 0.005)
chk("2381 Pythagore 8 6 10", sqrt(8**2 + 6**2), 10, 0)
chk("2382 AC = 8 sin40", 8 * S(40), 5.14, 0.005)
chk("2382 AB = 8 cos40", 8 * C(40), 6.13, 0.005)
chk("2383 EF = 7,5 cos52", R(15, 2) * C(52), 4.62, 0.005)
chk("2383 FG = 7,5 sin52", R(15, 2) * S(52), 5.91, 0.005)
chk("2384 LM = 6/cos34", 6 / C(34), 7.24, 0.005)
chk("2384 KM = 6 tan34", 6 * T(34), 4.05, 0.005)
chk("2385 angle I = acos(5/8)", acos(R(5, 8)) / deg, 51.32, 0.005)
chk("2385 angle K", 90 - acos(R(5, 8)) / deg, 38.68, 0.005)
chk("2385 sin K = 5/8 => K", asin(R(5, 8)) / deg, 38.68, 0.005)
chk("2386 a ST = 9 sin28", 9 * S(28), 4.23, 0.005)
chk("2386 b ST = 7 tan28", 7 * T(28), 3.72, 0.005)
chk("2386 c RT = 7/cos28", 7 / C(28), 7.93, 0.005)
chk("2387 B = atan(4,5/7)", atan(R(45, 70)) / deg, 32.74, 0.005)
chk("2387 C", 90 - atan(R(45, 70)) / deg, 57.26, 0.005)
chk("2387 BC Pythagore", sqrt(7**2 + R(45, 10)**2), 8.32, 0.005)
chk("2388 BC = 5/sin25", 5 / S(25), 11.83, 0.005)
chk("2388 AC = 5/tan25", 5 / T(25), 10.72, 0.005)
chk("2388 B = 65", 90 - 25, 65, 0)
chk("2388 controle cos65 = AB/BC", 5 / (5 / S(25)) - C(65), 0, 1e-12)
chk("2389 hauteur 6 sin70", 6 * S(70), 5.638, 0.0005)
chk("2389 pied 6 cos70", 6 * C(70), 2.052, 0.0005)
chk("2389 angle acos(1,5/6)", acos(R(15, 60)) / deg, 75.52, 0.005)
chk("2390 BC juste 6/cos40", 6 / C(40), 7.83, 0.005)
chk("2390 BC faux 6/sin40", 6 / S(40), 9.33, 0.005)
chk("2390 cos(40 rad)", cos(40), -0.667, 0.0005)
chk("2391 hauteur 4 tan3", 4 * T(3), 0.2096, 0.00005)
chk("2391 longueur 4/cos3", 4 / C(3), 4.0055, 0.00005)
chk("2391 angle atan(0,5/8)", atan(R(5, 80)) / deg, 3.58, 0.005)
chk("2392 35 sin48", 35 * S(48), 26.01, 0.005)
chk("2392 hauteur totale", 35 * S(48) + R(12, 10), 27.21, 0.005)
chk("2392 horizontale 35 cos48", 35 * C(48), 23.42, 0.005)
chk("2393 asin(2,1/4,2)", asin(R(21, 42)) / deg, 30, 1e-9)
chk("2393 horizontale 4,2 cos30", R(42, 10) * C(30), 3.637, 0.0005)
chk("2394 30 tan38", 30 * T(38), 23.44, 0.005)
chk("2394 hauteur", 30 * T(38) + R(16, 10), 25.04, 0.005)
chk("2394 nouvel angle", atan(30 * T(38) / 20) / deg, 49.53, 0.005)
chk("2395 hauteur 5 tan35", 5 * T(35), 3.501, 0.0005)
chk("2395 chevron 5/cos35", 5 / C(35), 6.104, 0.0005)
chk("2395 angle au sommet", 180 - 2 * 35, 110, 0)
chk("2396 AB = 25 tan58", 25 * T(58), 40.01, 0.005)
chk("2396 BC = 25/cos58", 25 / C(58), 47.18, 0.005)
chk("2397 altitude 3000 tan12", 3000 * T(12), 637.7, 0.05)
chk("2397 trajet 3000/cos12", 3000 / C(12), 3067.0, 0.05)
chk("2397 angle atan(1000/3000)", atan(R(1, 3)) / deg, 18.43, 0.005)
chk("2398 45/tan8", 45 / T(8), 320.2, 0.05)
chk("2398 45/tan12", 45 / T(12), 211.7, 0.05)
chk("2398 deplacement", 45 / T(8) - 45 / T(12), 108.5, 0.05)
chk("2399 angle atan(0,1)", atan(R(1, 10)) / deg, 5.71, 0.005)
chk("2399 denivele 2500 x 0,1", 2500 * R(1, 10), 250, 0)
chk("2399 route Pythagore", sqrt(2500**2 + 250**2), 2512.5, 0.05)
chk("2399 route 2500/cos(atan 0,1)", 2500 / cos(atan(R(1, 10))), 2512.5, 0.05)
chk("2399 sin(5,7) x 2512,5", 2500 / cos(atan(R(1, 10))) * sin(atan(R(1, 10))), 250, 1e-9)
chk("2400 AC Pythagore", sqrt(8**2 + 6**2), 10, 0)
chk("2400 angle A atan(6/8)", atan(R(6, 8)) / deg, 36.87, 0.005)
chk("2400 EF Thales", R(5, 8) * 6, 3.75, 0)
chk("2400 AF Thales", R(5, 8) * 10, 6.25, 0)
chk("2400 controle 5 tan A", 5 * tan(atan(R(6, 8))), 3.75, 1e-12)
chk("2400 controle AF = 5/cos A", 5 / cos(atan(R(6, 8))), 6.25, 1e-12)
print("\n%d contrôles OK" % ok)

# compléments (valeurs citées dans les corrigés)
chk("2382 mode radians 8 sin(40 rad)", 8 * sin(40), 5.96, 0.005)
chk("2384 erreur 6 cos34", 6 * C(34), 4.97, 0.005)
chk("2390 Tom 6/cos(40 rad)", 6 / cos(40), -9.00, 0.005)
chk("2387 BC^2", 7**2 + R(45, 10)**2, 69.25, 0)
chk("2387 erreur atan(7/4,5)", atan(R(70, 45)) / deg, 57.26, 0.005)
chk("2391 tan alpha 0,5/8", R(5, 10) / 8, 0.0625, 0)
chk("2394 tan nouvel angle", 30 * T(38) / 20, 1.172, 0.0005)
chk("2396 AB^2", (25 * T(58))**2, 1600.7, 0.05)
chk("2396 AC^2+AB^2", 625 + (25 * T(58))**2, 2225.7, 0.05)
chk("2396 BC^2", (25 / C(58))**2, 2225.7, 0.05)
chk("2398 angle en S", 90 - 8, 82, 0)
chk("2399 L^2", 2500**2 + 250**2, 6312500, 0)
chk("cours 20 tan40", 20 * T(40), 16.8, 0.05)
print("\n%d contrôles OK (avec compléments)" % ok)
