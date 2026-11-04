# -*- coding: utf-8 -*-
"""Vérification sympy de tous les calculs de la notion 254 (4e : carrés et racines carrées).

    python verif_254.py      -> affiche le nombre de contrôles, s'arrête à la première erreur
"""
from sympy import Rational as R, sqrt, pi, Integer, solve, symbols, floor, ceiling, N, isprime

n_ok = 0


def ok(cond, msg):
    global n_ok
    if not bool(cond):
        raise SystemExit("ÉCHEC : " + msg)
    n_ok += 1


def D(s):
    """Décimal exact à partir d'une chaîne « 4,47 »."""
    return R(s.replace(",", "."))


def arr(x, k):
    """Arrondi de x (sympy) à k décimales, rendu exact."""
    v = N(x, 30)
    return R(round(float(v) * 10 ** k)) / 10 ** k if abs(float(v)) < 1e12 else None


def arrondi(x, k):
    from decimal import Decimal, ROUND_HALF_UP
    d = Decimal(str(N(x, 40)))
    q = Decimal(1).scaleb(-k)
    return R(str(d.quantize(q, rounding=ROUND_HALF_UP)))


def encadre(a, lo, hi):
    return lo ** 2 < a < hi ** 2 and lo < sqrt(a) < hi


x = symbols("x")

# ------------------------------------------------------------------ cours
ok(7 ** 2 == 49, "7²")
ok(D("0,3") ** 2 == D("0,09"), "0,3²")
ok(R(2, 3) ** 2 == R(4, 9), "(2/3)²")
ok((-6) ** 2 == 36 and -(6 ** 2) == -36, "(-6)² / -6²")
ok(2 * 3 ** 2 == 18 and (2 * 3) ** 2 == 36, "2×3²")
ok(3 ** 2 + 4 ** 2 == 25 and (3 + 4) ** 2 == 49, "3²+4²")
ok([k * k for k in range(1, 13)] == [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144], "carrés parfaits 1-12")
ok((13 ** 2, 14 ** 2, 15 ** 2) == (169, 196, 225), "13² 14² 15²")
ok(sqrt(49) == 7 and sqrt(0) == 0 and sqrt(1) == 1, "racines simples")
ok(sqrt(D("0,25")) == D("0,5"), "√0,25")
ok(sqrt(R(9, 16)) == R(3, 4), "√(9/16)")
ok(sqrt(13 ** 2) == 13 and sqrt(5) ** 2 == 5, "√13², (√5)²")
ok(sqrt(25) == 5, "√25")
ok(arrondi(sqrt(20), 2) == D("4,47") and arrondi(sqrt(20), 1) == D("4,5"), "√20 arrondis")
ok(str(N(sqrt(20), 10)).startswith("4.472135"), "√20 affichage")
ok(sqrt(16) == 4 and sqrt(36) == 6, "√16 √36")
ok(sqrt(9 + 16) == 5 and sqrt(9) + sqrt(16) == 7, "√(9+16)")
ok(encadre(20, 4, 5), "4<√20<5")
ok(D("4,4") ** 2 == D("19,36") and D("4,5") ** 2 == D("20,25") and encadre(20, D("4,4"), D("4,5")), "√20 au dixième")
ok(D("4,47") ** 2 == D("19,9809"), "4,47²")
ok(D("5,5") ** 2 == D("30,25") and sqrt(30) < D("5,5"), "√30 < 5,5")
ok(set(solve(x ** 2 - 49, x)) == {7, -7}, "x²=49")
ok(set(solve(x ** 2 - 7, x)) == {sqrt(7), -sqrt(7)} and arrondi(sqrt(7), 2) == D("2,65"), "x²=7")
ok(solve(x ** 2 + 3, x) == [] or all(not s.is_real for s in solve(x ** 2 + 3, x)), "x²=-3")
ok(set(solve(3 * x ** 2 - 75, x)) == {5, -5} and R(75, 3) == 25, "3x²=75")
ok(set(solve(x ** 2 - 64, x)) == {8, -8}, "c²=64")
ok(9 + 16 == 25 and 3 ** 2 == 9 and 4 ** 2 == 16 and 5 ** 2 == 25, "triangle 3-4-5")

# ------------------------------------------------------------------ fiche
ok(sqrt(144) == 12 and sqrt(D("0,09")) == D("0,3"), "fiche racines")
ok(encadre(20, 4, 5) and encadre(20, D("4,4"), D("4,5")), "fiche encadrement")
ok(sqrt(36) == 6 and 5 ** 2 == 25, "fiche pièges")

# ------------------------------------------------------------------ 2558
ok([k * k for k in (1, 2, 3, 4)] == [1, 4, 9, 16], "2558 Q1 quadrillage")
ok([k * k for k in (3, 6, 9, 11, 13, 15)] == [9, 36, 81, 121, 169, 225], "2558 Q2")
ok([k * k for k in (1, 2, 4, 5, 7, 8, 10, 12, 14)] == [1, 4, 16, 25, 49, 64, 100, 144, 196], "2558 Q2 cases données")
ok([k * k for k in range(1, 20) if 50 < k * k < 150] == [64, 81, 100, 121, 144], "2558 Q3")
ok(7 ** 2 == 49 and 13 ** 2 == 169, "2558 Q3 bornes")
ok(14 ** 2 == 196 and 196 < 200 < 225 and not any(k * k == 200 for k in range(300)), "2558 Q4")
ok([(k * k) % 10 for k in range(10)] == [0, 1, 4, 9, 6, 5, 6, 9, 4, 1], "2558 Q5 unités")
ok(sorted({(k * k) % 10 for k in range(1000)}) == [0, 1, 4, 5, 6, 9], "2558 Q5 général")
ok(not any(k * k == 2027 for k in range(100)), "2558 Q6")

# ------------------------------------------------------------------ 2559
ok(7 * 7 == 49 and sqrt(49) == 7, "2559 Q1")
ok((sqrt(81), sqrt(144), sqrt(1), sqrt(0)) == (9, 12, 1, 0), "2559 Q2")
ok(sqrt(D("0,25")) == D("0,5") and sqrt(D("0,01")) == D("0,1") and sqrt(R(4, 9)) == R(2, 3), "2559 Q3")
ok(D("0,05") ** 2 == D("0,0025") and D("0,5") > D("0,25"), "2559 erreur fréquente")
ok(not sqrt(-4).is_real, "2559 Q4")
ok(sqrt(7) ** 2 == 7 and sqrt(7 ** 2) == 7 and sqrt((-7) ** 2) == 7, "2559 Q5")
ok((-5) ** 2 == 25 and sqrt(25) == 5, "2559 Q6")

# ------------------------------------------------------------------ 2560
ok(sqrt(64) == 8, "2560 Q1")
ok(D("1,5") ** 2 == D("2,25") and sqrt(D("2,25")) == D("1,5"), "2560 Q2")
ok(encadre(30, 5, 6), "2560 Q3")
ok(arrondi(sqrt(30), 2) == D("5,48") and str(N(sqrt(30), 6)).startswith("5.4772"), "2560 Q4")
ok(D("5,48") ** 2 == D("30,0304"), "2560 vérification")
ok(4 * 8 == 32 and 4 * D("1,5") == 6, "2560 Q5 A B")
ok(arrondi(4 * sqrt(30), 3) == D("21,909") and arrondi(4 * sqrt(30), 1) == D("21,9"), "2560 Q5 C")
ok(64 / 4 == 16 and 16 * 16 == 256, "2560 erreur fréquente")

# ------------------------------------------------------------------ 2561
ok(encadre(20, 4, 5) and encadre(50, 7, 8) and encadre(90, 9, 10), "2561 Q1-3")
ok(D("4,4") ** 2 == D("19,36") and D("4,5") ** 2 == D("20,25"), "2561 Q4")
ok(str(N(sqrt(20), 5)).startswith("4.4721") and arrondi(sqrt(20), 2) == D("4,47"), "2561 Q5")
ok(arrondi(sqrt(50), 2) == D("7,07") and arrondi(sqrt(90), 2) == D("9,49"), "2561 Q6")

# ------------------------------------------------------------------ 2562
ok(sqrt(9) + sqrt(16) == 7 and sqrt(9 + 16) == 5, "2562 Q1")
ok(sqrt(100) - sqrt(64) == 2 and sqrt(100 - 64) == 6, "2562 Q2")
ok(sqrt(3 ** 2 + 4 ** 2) == 5 and 3 + 4 == 7, "2562 Q3")
ok(sqrt(6 ** 2 + 8 ** 2) == 10 and 36 + 64 == 100, "2562 Q4")
ok(sqrt(25 + 0) == sqrt(25) + sqrt(0), "2562 Q6")
ok(solve(sqrt(25 + x) - 5 - sqrt(x), x) == [0], "2562 Q6 unique")

# ------------------------------------------------------------------ 2563
ok(set(solve(x ** 2 - 49, x)) == {7, -7}, "2563 Q1")
ok(set(solve(x ** 2 - D("0,36"), x)) == {D("0,6"), -D("0,6")}, "2563 Q2")
ok(solve(x ** 2, x) == [0], "2563 Q3")
ok(all(not s.is_real for s in solve(x ** 2 + 9, x)), "2563 Q4")
ok(set(solve(x ** 2 - 121, x)) == {11, -11}, "2563 Q5")
ok(arrondi(sqrt(2), 3) == D("1,414") and str(N(sqrt(2), 5)).startswith("1.4142"), "2563 Q6")

# ------------------------------------------------------------------ 2564
ok(3 ** 2 + 4 ** 2 == 25 and (3 + 4) ** 2 == 49, "2564 Q1")
ok(2 * 3 ** 2 == 18 and (2 * 3) ** 2 == 36, "2564 Q2")
ok((-5) ** 2 == 25 and -5 ** 2 == -25, "2564 Q3")
ok(D("0,3") ** 2 == D("0,09") and D("1,2") ** 2 == D("1,44") and 12 * 12 == 144, "2564 Q4")
ok(R(2, 3) ** 2 == R(4, 9) and R(-1, 2) ** 2 == R(1, 4), "2564 Q5")
ok(10 ** 2 - 2 * 6 ** 2 == 28 and 2 * 36 == 72, "2564 Q6")

# ------------------------------------------------------------------ 2565
ok(sqrt(196) == 14 and 4 * 14 == 56 and 56 * D("12,5") == 700, "2565 Q1-3")
ok(encadre(200, 14, 15) and arrondi(sqrt(200), 2) == D("14,14") and str(N(sqrt(200), 6)).startswith("14.1421"), "2565 Q4")
ok(arrondi(4 * sqrt(200), 2) == D("56,57") and ceiling(4 * sqrt(200)) == 57, "2565 Q5")
ok(57 * D("12,5") == D("712,5"), "2565 Q6")

# ------------------------------------------------------------------ 2566
ok(18 * 8 == 144 and sqrt(144) == 12, "2566 Q1-2")
ok(2 * (18 + 8) == 52 and 4 * 12 == 48, "2566 Q3")
ok(5 * 20 == 100 and sqrt(100) == 10 and 2 * (5 + 20) == 50 and 4 * 10 == 40, "2566 Q4")
ok(6 * 15 == 90 and 81 < 90 < 100 and arrondi(sqrt(90), 2) == D("9,49"), "2566 Q5 côté")
ok(2 * (6 + 15) == 42 and arrondi(4 * sqrt(90), 2) == D("37,95"), "2566 Q5 périmètres")
ok((18 + 8) / 2 == 13 and 13 ** 2 == 169, "2566 erreur fréquente")

# ------------------------------------------------------------------ 2567
d = lambda t: D("4,9") * t ** 2
ok(d(1) == D("4,9") and d(2) == D("19,6") and d(3) == D("44,1"), "2567 Q1")
ok(D("44,1") / D("4,9") == 9 and sqrt(9) == 3, "2567 Q2")
ok(D("122,5") / D("4,9") == 25 and sqrt(25) == 5, "2567 Q3")
ok(arrondi(100 / D("4,9"), 2) == D("20,41") and arrondi(sqrt(100 / D("4,9")), 4) == D("4,5175")
   and arrondi(sqrt(100 / D("4,9")), 2) == D("4,52"), "2567 Q4")
ok(arrondi(324 / D("4,9"), 2) == D("66,12") and arrondi(sqrt(324 / D("4,9")), 4) == D("8,1316")
   and arrondi(sqrt(324 / D("4,9")), 2) == D("8,13"), "2567 Q5")
ok(D("88,2") / D("4,9") == 18 and arrondi(sqrt(18), 2) == D("4,24")
   and arrondi(D("4,24") / 3, 2) == D("1,41") and sqrt(18) / 3 == sqrt(2), "2567 Q6")

# ------------------------------------------------------------------ 2568
ok(D("6,7") ** 2 == D("44,89") and D("6,7") < sqrt(45), "2568 Q1")
ok(7 < sqrt(50), "2568 Q2")
ok(D("3,2") ** 2 == D("10,24"), "2568 Q3 carré")
vals = [sqrt(10), Integer(3), sqrt(8), D("3,2"), sqrt(12)]
ok(sorted(vals, key=lambda v: N(v, 30)) == [sqrt(8), 3, sqrt(10), D("3,2"), sqrt(12)], "2568 Q3 rangement")
ok((arrondi(sqrt(8), 2), arrondi(sqrt(10), 2), arrondi(sqrt(12), 2)) == (D("2,83"), D("3,16"), D("3,46")), "2568 Q4")
ok([k for k in range(0, 20) if sqrt(20) < k < sqrt(70)] == [5, 6, 7, 8], "2568 Q5")
ok(4 ** 2 < 20 and 9 ** 2 > 70, "2568 Q5 bornes")
ok(sqrt(D("0,36")) == D("0,6") and D("0,36") < D("0,6"), "2568 Q6")

# ------------------------------------------------------------------ 2569
ok(encadre(2, 1, 2), "2569 Q1")
ok(D("1,4") ** 2 == D("1,96") and D("1,5") ** 2 == D("2,25") and encadre(2, D("1,4"), D("1,5")), "2569 Q2")
ok(D("1,41") ** 2 == D("1,9881") and D("1,42") ** 2 == D("2,0164") and encadre(2, D("1,41"), D("1,42")), "2569 Q3")
ok(D("1,414") ** 2 == D("1,999396") and D("1,415") ** 2 == D("2,002225") and encadre(2, D("1,414"), D("1,415")), "2569 Q4")
ok(str(N(sqrt(2), 9)).startswith("1.41421356"), "2569 Q5")
ok(D("1,6") ** 2 == D("2,56") and D("1,7") ** 2 == D("2,89") and D("1,8") ** 2 == D("3,24")
   and encadre(3, D("1,7"), D("1,8")) and D("1,5") ** 2 == D("2,25"), "2569 Q6")

# ------------------------------------------------------------------ 2570 (A(0,0) B(4,0) C(4,4) D(0,4), E(4,8) F(8,4))
ok(4 ** 2 == 16 and 8 ** 2 == 64 and 64 == 4 * 16, "2570 Q1-2")
ok(2 * 16 == 32 and encadre(32, 5, 6) and arrondi(sqrt(32), 2) == D("5,66"), "2570 Q3-4")
B, Dp, E, F, C = (4, 0), (0, 4), (4, 8), (8, 4), (4, 4)
dist2 = lambda P, Q: (P[0] - Q[0]) ** 2 + (P[1] - Q[1]) ** 2
ok(dist2(B, Dp) == dist2(Dp, E) == dist2(E, F) == dist2(F, B) == 32 and dist2(B, E) == dist2(Dp, F) == 64, "2570 BDEF carré")
ok(((B[0] + E[0]) / 2, (B[1] + E[1]) / 2) == C and ((Dp[0] + F[0]) / 2, (Dp[1] + F[1]) / 2) == C, "2570 diagonales en C")
aire_tri = lambda P, Q, S: abs((Q[0] - P[0]) * (S[1] - P[1]) - (S[0] - P[0]) * (Q[1] - P[1])) / 2
ok(aire_tri(B, C, Dp) == aire_tri(Dp, C, E) == aire_tri(E, C, F) == aire_tri(F, C, B) == 8, "2570 triangles 8 cm²")
ok(4 * 8 == 32 and sqrt(dist2(B, Dp)) == sqrt(32), "2570 Q5-6")

# ------------------------------------------------------------------ 2571
ok(sqrt(D("2,25")) == D("1,5"), "2571 Q1")
ok(sqrt(86 - 5) == 9 and 9 ** 2 + 5 == 86, "2571 Q2")
ok(sqrt(R(72, 2)) == 6 and 2 * 6 ** 2 == 72, "2571 Q3")
ok(sqrt(64) - 1 == 7, "2571 Q4")
ok(17 ** 2 == 289 and 18 ** 2 == 324 and 17 ** 2 < 300 < 18 ** 2, "2571 Q5")
ok(100 ** 2 == 10000 and 101 ** 2 == 10201 and min(k for k in range(200) if k * k > 10000) == 101, "2571 Q6")

# ------------------------------------------------------------------ 2572
ok(sqrt(2025) == 45 and 40 ** 2 == 1600 and 50 ** 2 == 2500, "2572 Q1")
ok(4 * 45 == 180, "2572 Q2")
ok(45 - 2 == 43 and 43 ** 2 == 1849, "2572 Q3")
ok(2025 - 1849 == 176, "2572 Q4")
ok(176 * D("0,05") == D("8,8") and D("8,8") * 35 == 308, "2572 Q5-6")
ok(4 * 44 * 1 == 176, "2572 Q7")

# ------------------------------------------------------------------ 2573
ok(sqrt(36) == 6 and 12 ** 2 == 144 and 144 / 36 == 4, "2573 Q1-2")
ok(encadre(72, 8, 9) and arrondi(sqrt(72), 2) == D("8,49") and str(N(sqrt(72), 5)).startswith("8.4853"), "2573 Q3")
ok((sqrt(72) / 6) ** 2 == 2 and sqrt(72) / 6 == sqrt(2) and arrondi(sqrt(2), 3) == D("1,414"), "2573 Q4")
ok(6 * sqrt(9) == 18 and 18 ** 2 == 324 == 9 * 36, "2573 Q5")
ok(100 * 100 == 10000 and sqrt(10000) == 100, "2573 Q6 côté")
ok(arrondi(R(10000, 36), 1) == D("277,8") and arrondi(R(100, 6), 1) == D("16,7")
   and arrondi(D("16,7") ** 2, 1) == D("278,9") and R(100, 6) ** 2 == R(10000, 36), "2573 Q6 coefficients")

# ------------------------------------------------------------------ 2574
ok(5 ** 2 == 25 and 12 ** 2 == 144, "2574 Q1")
ok(sqrt(324) == 18 and 17 ** 2 == 289, "2574 Q2")
ok(max(k for k in range(100) if k * k <= 500) == 22 and 22 ** 2 == 484 and 500 - 484 == 16, "2574 Q3")
ok(23 ** 2 == 529 and 529 - 500 == 29, "2574 Q4")
ok(4 + 4 + 1 == 9 == 5 ** 2 - 4 ** 2 and all((k + 1) ** 2 - k ** 2 == 2 * k + 1 for k in range(100)), "2574 Q5")
ok(2 * 22 + 1 == 45 == 529 - 484, "2574 Q5 vérification")
ok(6 ** 2 - 4 ** 2 == 20 == 4 * 6 - 4, "2574 Q6 exemple côté 6")
ok(22 ** 2 - 20 ** 2 == 84 == 4 * 22 - 4 and 484 - 400 == 84, "2574 Q6")

# ------------------------------------------------------------------ 2575
ok(sqrt(9) == 3 and sqrt(16) == 4 and sqrt(9 + 16) == 5, "2575 Q1-2")
ok(sqrt(6 ** 2 + 8 ** 2) == 10 and sqrt(5 ** 2 + 12 ** 2) == 13 and 25 + 144 == 169, "2575 Q4-5")
ok(sqrt(1 + 4) == sqrt(5) and encadre(5, 2, 3) and arrondi(sqrt(5), 3) == D("2,236") and arrondi(sqrt(5), 2) == D("2,24"), "2575 Q6")
ok(3 ** 2 + 4 ** 2 == 5 ** 2 and 6 ** 2 + 8 ** 2 == 10 ** 2 and 5 ** 2 + 12 ** 2 == 13 ** 2, "2575 Q7 triplets")

# ------------------------------------------------------------------ 2576
ok(sqrt(D("0,09")) == D("0,3"), "2576 Q1")
ok(sqrt(D("20,25")) == D("4,5") and 16 < D("20,25") < 25, "2576 Q2")
ok(D("4,5") / D("0,3") == 15 and 15 ** 2 == 225, "2576 Q3")
ok(D("20,25") / D("0,09") == 225 and R(2025, 9) == 225, "2576 Q4")
ok(225 * D("1,1") == D("247,5") and ceiling(D("247,5")) == 248, "2576 Q5")
ok(arrondi(R(248, 12), 2) == D("20,67") and 20 * 12 == 240 and 21 * 12 == 252 and 248 - 240 == 8, "2576 Q6 boîtes")
ok(21 * D("18,9") == D("396,9"), "2576 Q6 prix")

# ------------------------------------------------------------------ 2577
v = lambda h: sqrt(D("9,8") * h)
ok(D("9,8") * 4000 == 39200 and arrondi(v(4000), 2) == D("197,99") and 198 ** 2 == 39204 and arrondi(v(4000), 0) == 198, "2577 Q1")
ok(198 * D("3,6") == D("712,8") and arrondi(v(4000) * D("3,6"), 0) == 713, "2577 Q2")
ok(v(10) == sqrt(98) and arrondi(sqrt(98), 1) == D("9,9") and arrondi(sqrt(98) * D("3,6"), 1) == D("35,6"), "2577 Q3")
ok(49 ** 2 == 2401 and R(2401) / D("9,8") == 245 and v(245) == 49, "2577 Q4")
ok(arrondi(R(3000, 713), 3) == D("4,208") and arrondi(R(3000, 713) * 60, 2) == D("252,45")
   and arrondi(R(3000, 713) * 60 - 240, 2) == D("12,45") and floor(R(3000, 713) * 60 - 240 + R(1, 2)) == 12, "2577 Q5")
ok(R(4000, 10) == 400 and sqrt(400) == 20 and D("198") / 20 == D("9,9"), "2577 retenir")

# ------------------------------------------------------------------ 2578
ok(pi * 15 ** 2 == 225 * pi and arrondi(225 * pi, 2) == D("706,86") and arrondi(225 * pi, 1) == D("706,9"), "2578 Q1")
ok(2 * pi * 10 ** 2 == 200 * pi and arrondi(200 * pi, 2) == D("628,32") and arrondi(200 * pi, 1) == D("628,3"), "2578 Q2")
ok(225 * pi > 200 * pi, "2578 Q3")
ok(arrondi(14 / (225 * pi), 3) == D("0,02") and arrondi(18 / (200 * pi), 3) == D("0,029")
   and arrondi(14 / D("706,86"), 3) == D("0,02") and arrondi(18 / D("628,32"), 3) == D("0,029"), "2578 Q4")
ok(arrondi(sqrt(200), 2) == D("14,14") and arrondi(2 * sqrt(200), 2) == D("28,28") and arrondi(2 * sqrt(200), 1) == D("28,3"), "2578 Q5")
ok(arrondi(1000 / pi, 2) == D("318,31") and arrondi(sqrt(1000 / pi), 2) == D("17,84")
   and arrondi(2 * sqrt(1000 / pi), 2) == D("35,68") and arrondi(2 * sqrt(1000 / pi), 1) == D("35,7"), "2578 Q6")

print(f"verif_254 : {n_ok} contrôles, tout est juste.")
