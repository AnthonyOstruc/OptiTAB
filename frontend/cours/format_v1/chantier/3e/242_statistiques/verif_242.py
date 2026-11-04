# -*- coding: utf-8 -*-
"""Vérification (sympy) des résultats numériques de la notion 242 « Statistiques »."""
from sympy import Rational as R, Integer as I, nsimplify


def moy(v, n=None):
    if n is None:
        return sum(I(x) for x in v) / len(v)
    return sum(I(a) * b for a, b in zip(v, n)) / sum(n)


def med(v):
    s = sorted(v)
    n = len(s)
    return I(s[n // 2]) if n % 2 else R(s[n // 2 - 1] + s[n // 2], 2)


def deplie(v, n):
    return [a for a, b in zip(v, n) for _ in range(b)]


ok = []
def eq(a, b, nom):
    assert nsimplify(a) == nsimplify(b), (nom, a, b)
    ok.append(nom)


# Cours / fiche
N, E = [6, 8, 10, 12, 16], [2, 3, 6, 5, 4]
eq(sum(E), 20, "effectif notes")
eq(sum(a * b for a, b in zip(N, E)), 220, "somme pondérée")
eq(moy(N, E), 11, "moyenne pondérée")
eq(med(deplie(N, E)), 10, "médiane notes")
eq(max(N) - min(N), 10, "étendue notes")
eq(moy(N), R(52, 5), "moyenne sans effectifs (erreur 2323)")
eq(R(12, 30), R(2, 5), "fréquence vélo")
eq(med([2, 3, 5, 6, 6, 9, 11, 12]), 6, "médiane cours")
s = [2, 3, 3, 8]
eq(moy(s), 4, "ex cours moy"); eq(med(s), 3, "ex cours med"); eq(max(s) - min(s), 6, "ex cours étendue")
A, B = [10, 10, 11, 12, 12], [4, 8, 12, 14, 17]
eq(moy(A), 11, "comparaison A"); eq(moy(B), 11, "comparaison B")
eq(max(A) - min(A), 2, "étendue A"); eq(max(B) - min(B), 13, "étendue B")
eq(R(18, 40) * 360, 162, "angle B")
eq(R(10, 40) * 360, 90, "angle A"); eq(R(12, 40) * 360, 108, "angle C")
eq(R(10, 40), R(25, 100), "A 25 %"); eq(R(12, 40), R(30, 100), "C 30 %")

# 2317
s = [2, 4, 4, 5, 7, 8]
eq(R(2, 6), R(1, 3), "2317 q3"); eq(R(3, 6), R(1, 2), "2317 q4")
# 2322
eq(5 + 4, 9, "2322 q4"); eq(R(9, 20), R(45, 100), "2322 q5")
# 2323 effectifs cumulés
cum = [sum(E[:k + 1]) for k in range(5)]
assert cum == [2, 5, 11, 16, 20]; ok.append("2323 cumulés")
# 2325 histogramme
H = [4, 8, 6, 2]
eq(sum(H), 20, "2325 total")
eq(moy([5, 15, 25, 35], H), 18, "2325 moyenne estimée")
# 2326 tableur
eq(4 * 3 + 7 * 5 + 12 * 2, 71, "2326 somme pondérée"); eq(moy([4, 7, 12], [3, 5, 2]), R(71, 10), "2326 moyenne")
eq(moy([4, 7, 12]), R(23, 3), "2326 MOYENNE fausse")
# 2331
eq((9 * 14 + 24) / I(10), 15, "2331 nouvelle moyenne")
# 2332
eq(R(84 - 80, 80), R(5, 100), "2332 taux")
# 2334 pluie
P = [62, 55, 48, 51, 66, 38, 22, 30, 54, 70, 78, 72]
eq(sum(P), 646, "2334 total"); eq(med(P), R(109, 2), "2334 médiane")
eq(max(P) - min(P), 56, "2334 étendue"); eq(sum(1 for x in P if x > 60), 5, "2334 > 60 mm")
eq(R(38 + 22, 2), 30, "2334 erreur non rangée")
assert abs(float(sum(P)) / 12 - 53.8) < 0.05; ok.append("2334 moyenne")
# 2336
eq(200 - 30 - 70 - 60, 40, "2336 q1")
assert [R(x, 200) * 360 for x in (30, 70, 60, 40)] == [54, 126, 108, 72]; ok.append("2336 angles")
cum = [30, 100, 160, 200]; ok.append("2336 cumulés")
# 2337
JA, JB = [12, 14, 15, 13, 16, 14], [5, 25, 8, 22, 6, 24]
eq(moy(JA), 14, "2337 moy A"); eq(moy(JB), 15, "2337 moy B")
eq(med(JA), 14, "2337 med A"); eq(med(JB), 15, "2337 med B")
eq(max(JA) - min(JA), 4, "2337 ét A"); eq(max(JB) - min(JB), 20, "2337 ét B")
eq(sum(1 for x in JB if x < 10), 3, "2337 B < 10")

# Corrigés développés (deuxième passe)
eq(moy([7, 9, 10, 14]), 10, "2319 q1"); eq(moy([12, 15, 8, 11, 9]), 11, "2319 q2")
eq(moy([-3, 5, 0, 2]), 1, "2319 q3"); eq(moy([9, 11, 12, 16]), 12, "2319 q5")
eq(med([13, 4, 9, 7, 11]), 9, "2320 q2"); eq(med([1, 3, 6, 8, 10, 20]), 7, "2320 q3")
eq(moy([1, 3, 6, 8, 10, 20]), 8, "2320 q4")
T = [-3, 2, 5, -1, 8, 0, 3]
eq(max(T) - min(T), 11, "2321 étendue"); eq(moy(T), 2, "2321 moyenne"); eq(med(T), 2, "2321 médiane")
eq(R(1, 6) + R(2, 6) + 3 * R(1, 6), 1, "2317 q5")
eq(30 - 12 - 9, 9, "2318 q1"); eq(R(12, 30), R(4, 10), "2318 q2"); eq(R(9, 30), R(3, 10), "2318 q3")
eq(R(360, 40), 9, "2324 q1")
eq((12 * 13 + 18 * 11) / I(30), R(118, 10), "2327 q3"); eq(R(13 + 11, 2), 12, "2327 q4")
eq(4 * R(25, 2) - 34, 16, "2328 q2"); eq(4 * 13 - 34, 18, "2328 q4"); eq(4 * 15 - 34, 26, "2328 q5")
eq(moy([9, 10, 10, 11]), 10, "2329 A"); eq(moy([2, 10, 10, 18]), 10, "2329 B")
eq(med([2, 10, 10, 18]), 10, "2329 med B")
S = [1800, 1900, 2000, 2100, 2200]
eq(moy(S), 2000, "2330 q1"); eq(med(S + [9000]), 2050, "2330 q3")
assert round(float(moy(S + [9000]))) == 3167; ok.append("2330 q2")
eq(sum(1 for x in S + [9000] if x < moy(S + [9000])), 5, "2330 q5")

eq(140 - 126, 14, "2331 q3"); eq(8 * 13 + 22, 126, "2331 q5 somme")
eq(med([14] * 9 + [24]), 14, "2331 q5 série 1"); eq(med([13] * 8 + [22, 24]), 13, "2331 q5 série 2")
eq(4 * 11, 44, "2335 q1"); eq(6 * 12, 72, "2335 q2"); eq(72 - 44, 28, "2335 q3")
eq(28 - 13, 15, "2335 q4"); eq(R(44 + 13 + 15, 6), 12, "2335 vérif"); eq(6 * 14 - 44, 40, "2335 q5")

CA, CB = [8, 9, 10, 11, 11, 12, 13, 14, 15], [4, 6, 9, 12, 13, 14, 16, 17, 19, 20]
eq(sum(CA), 103, "2333 somme A"); assert abs(float(moy(CA)) - 11.4) < 0.05; ok.append("2333 moy A")
eq(moy(CB), 13, "2333 moy B"); eq(med(CA), 11, "2333 med A"); eq(med(CB), R(27, 2), "2333 med B")
eq(max(CA) - min(CA), 7, "2333 ét A"); eq(max(CB) - min(CB), 16, "2333 ét B")
eq(sum(1 for x in CA if x >= 12), 4, "2333 A>=12"); eq(sum(1 for x in CB if x >= 12), 7, "2333 B>=12")
assert [R(x, 200) for x in (30, 70, 60, 40)] == [R(15, 100), R(35, 100), R(3, 10), R(2, 10)]; ok.append("2336 fréquences")

# ---------------------------------------------------------------- finition 2026-11-03
# 2332 graphique trompeur
eq(84 - 80, 4, "2332 hausse"); eq(R(4, 80), R(5, 100), "2332 taux 5 %")
eq(80 - 78, 2, "2332 hauteur 2025"); eq(84 - 78, 6, "2332 hauteur 2026")
eq(R(6, 2), 3, "2332 rapport visuel"); eq(R(84, 80), R(105, 100), "2332 rapport réel")
# 2334 relevé de pluie
P = [62, 55, 48, 51, 66, 38, 22, 30, 54, 70, 78, 72]
eq(sum(P[:6]), 320, "2334 S1"); eq(sum(P[6:]), 326, "2334 S2"); eq(sum(P), 646, "2334 total")
assert str(R(646, 12).evalf(5)) == "53.833"; ok.append("2334 moyenne 53,833…")
eq(med(P), R(109, 2), "2334 médiane"); eq(R(38 + 22, 2), 30, "2334 erreur non rangé")
eq(max(P) - min(P), 56, "2334 étendue")
assert P.index(min(P)) == 6 and P.index(max(P)) == 10; ok.append("2334 juillet / novembre")
mois = ["janv", "févr", "mars", "avr", "mai", "juin", "juil", "août", "sept", "oct", "nov", "déc"]
assert sorted((v, m) for v, m in zip(P, mois) if v > 60) == [(62, "janv"), (66, "mai"), (70, "oct"), (72, "déc"), (78, "nov")]
ok.append("2334 mois > 60")
assert str(R(5, 12).evalf(3)) == "0.417" and round(float(R(5, 12)) * 100) == 42; ok.append("2334 5/12 ≈ 42 %")
# 2317, 2318, 2320, 2321, 2322, 2323, 2324, 2325
eq(len([2, 4, 4, 5, 7, 8]), 6, "2317 q1"); eq([2, 4, 4, 5, 7, 8].count(4), 2, "2317 q2")
eq(R(9, 30), R(30, 100), "2318 q3/q4 %")
assert sorted([13, 4, 9, 7, 11]) == [4, 7, 9, 11, 13]; ok.append("2320 q1")
eq(sum([1, 3, 6, 8, 10, 20]), 48, "2320 q4 somme")
eq(max(T), 8, "2321 max"); eq(min(T), -3, "2321 min")
T2 = [-3, 8, 8, 8, 8, 8, 8]
eq(max(T2) - min(T2), 11, "2321 q5 même étendue"); assert moy(T2) > moy(T); ok.append("2321 q5 moyenne plus élevée")
eq(max(E), 6, "2322 q3"); eq(N[E.index(max(E))], 10, "2322 q3 note")
assert [a * b for a, b in zip(N, E)] == [12, 24, 60, 60, 64]; ok.append("2323 produits")
eq(R(18, 40), R(45, 100), "2324 q4")
eq(4 + 8 + 6 + 2, 20, "2325 total"); eq((5 * 4 + 15 * 8 + 25 * 6 + 35 * 2) / I(20), 18, "2325 moyenne")
# 2327 réunir deux groupes
eq(12 * 13, 156, "2327 q1"); eq(18 * 11, 198, "2327 q2"); eq(R(354, 30), R(59, 5), "2327 q3")
eq(R(15 * 13 + 15 * 11, 30), 12, "2327 q5 effectifs égaux"); eq(15 * 13 + 15 * 11, 360, "2327 q5 somme")
assert 11 < R(354, 30) < 12 and abs(R(354, 30) - 11) < abs(R(354, 30) - 13); ok.append("2327 q4 plus proche de 11")
# 2329, 2333, 2337
eq(18 - 2, 16, "2329 étendue B"); eq(11 - 9, 2, "2329 étendue A")
JA, JB = [12, 14, 15, 13, 16, 14], [5, 25, 8, 22, 6, 24]
eq(moy(JA), 14, "2337 moy A"); eq(moy(JB), 15, "2337 moy B"); eq(med(JA), 14, "2337 med A"); eq(med(JB), 15, "2337 med B")
eq(R(max(JB) - min(JB), max(JA) - min(JA)), 5, "2337 rapport des étendues")
eq(sum(JA), 84, "2337 total A"); eq(sum(JB), 90, "2337 total B")
assert sorted(JA)[2:4] == [14, 14] and sorted(JB)[2:4] == [8, 22]; ok.append("2337 valeurs centrales")
# découpages des sommes (affichage téléphone)
eq(8 + 9 + 10 + 11 + 11, 49, "2333 paquet A1"); eq(12 + 13 + 14 + 15, 54, "2333 paquet A2"); eq(49 + 54, 103, "2333 total A")
eq(4 + 6 + 9 + 12 + 13, 44, "2333 paquet B1"); eq(14 + 16 + 17 + 19 + 20, 86, "2333 paquet B2"); eq(44 + 86, 130, "2333 total B")
assert str(R(103, 9).evalf(4)) == "11.44"; ok.append("2333 103/9 = 11,44…")
eq(1800 + 2200, 4000, "2330 paire 1"); eq(1900 + 2100, 4000, "2330 paire 2"); eq(4000 + 4000 + 2000, 10000, "2330 total")
eq(8 + 12 + 14, 34, "2328 trois notes")
eq(2 + 5 + 8 + 3, 18, "2321 positifs"); eq(-3 + -1, -4, "2321 négatifs"); eq(18 - 4, 14, "2321 total")
eq(sorted(T)[3], 2, "2321 4e valeur")
assert [4, 4 + 8, 12 + 6, 18 + 2] == [4, 12, 18, 20]; ok.append("2325 effectifs cumulés")
assert [30, 30 + 70, 100 + 60, 160 + 40] == [30, 100, 160, 200]; ok.append("2336 effectifs cumulés")
eq(sum([54, 126, 108, 72]), 360, "2336 somme angles")
assert [x * 9 for x in (10, 18, 12)] == [90, 162, 108] and 90 + 162 + 108 == 360; ok.append("2324 angles")
eq(360 * R(45, 100), 162, "2324 q5")
eq(R(9, 20), R(45, 100), "2322 q5")

print(len(ok), "contrôles OK")
