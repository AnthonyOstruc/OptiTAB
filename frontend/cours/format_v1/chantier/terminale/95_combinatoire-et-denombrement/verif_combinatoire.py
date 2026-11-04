# -*- coding: utf-8 -*-
"""Vérification de tous les dénombrements de la notion « Combinatoire et dénombrement ».

    python verif_combinatoire.py

Chaque résultat publié (cours, fiche, exercices) est recalculé par la formule
(math.comb, math.perm, factorielles) ET, quand c'est raisonnable, par
énumération exhaustive (itertools). Le script s'arrête à la première erreur.
"""
from itertools import combinations, permutations, product
from math import comb, factorial as f, perm

N_OK = 0


def ok(nom, calcule, attendu):
    global N_OK
    assert calcule == attendu, f"{nom} : calculé {calcule}, attendu {attendu}"
    N_OK += 1
    print(f"  ✓ {nom} = {attendu}")


def compte(iterable, cond=lambda x: True):
    return sum(1 for x in iterable if cond(x))


LETTRES = [chr(65 + i) for i in range(26)]
CHIFFRES = list(range(10))

print("COURS")
ok("menus 3 x 4 x 2", compte(product(range(3), range(4), range(2))), 24)
ok("menus de l'arbre 2 x 3", compte(product("SP", "VFG")), 6)
ok("codes 4 chiffres", compte(product(CHIFFRES, repeat=4)), 10_000)
ok("parties de {a,b,c}", compte(product([0, 1], repeat=3)), 8)
ok("couples distincts de {A,B,C}", compte(permutations("ABC", 2)), 6)
ok("podium parmi 10", compte(permutations(range(10), 3)), 720)
ok("anagrammes MATHS", len(set(permutations("MATHS"))), 120)
ok("mains de 5 cartes parmi 32", comb(32, 5), 201_376)
ok("mains avec exactement 2 as", compte(combinations(range(32), 5), lambda m: sum(c < 4 for c in m) == 2), 19_656)
ok("C(4,2) x C(28,3)", comb(4, 2) * comb(28, 3), 19_656)
ok("C(28,3)", comb(28, 3), 3_276)
ok("chemins O(0;0) -> A(4;3)", len(set(permutations("DDDDHHH"))), 35)
ok("C(7,3)", comb(7, 3), 35)
ok("chemins passant par B(2;1) (cours)", comb(3, 1) * comb(4, 2), 18)
# triangle de Pascal (figure) : lignes 0 à 6 et relation mise en évidence
for n in range(7):
    ligne = [comb(n, k) for k in range(n + 1)]
    if n:
        prec = [comb(n - 1, k) for k in range(n)]
        assert ligne == [1] + [prec[k - 1] + prec[k] for k in range(1, n)] + [1]
ok("Pascal 4 + 6 = 10", comb(4, 1) + comb(4, 2), comb(5, 2))
ok("somme ligne 6", sum(comb(6, k) for k in range(7)), 2 ** 6)
for n in range(1, 12):
    for k in range(1, n):
        assert comb(n, k) == comb(n - 1, k - 1) + comb(n - 1, k)
        assert comb(n, k) == comb(n, n - k)
        assert comb(n, k) == perm(n, k) // f(k)
    assert sum(comb(n, k) for k in range(n + 1)) == 2 ** n
    assert comb(n, 2) == n * (n - 1) // 2
print("  ✓ Pascal, symétrie, formule, somme 2^n vérifiées pour n ≤ 11")
# exemple du cours « probabilité » : 2 rouges parmi 4 tirées dans 5R+3B
ok("C(5,2)C(3,2) / C(8,4) : numérateur", comb(5, 2) * comb(3, 2), 30)
ok("C(8,4)", comb(8, 4), 70)
from fractions import Fraction
ok("probabilité exactement 2 rouges", Fraction(comb(5, 2) * comb(3, 2), comb(8, 4)), Fraction(3, 7))
ok("rangements 2 rouges + 3 bleues", len(set(permutations("RRBBB"))), comb(5, 2))
ok("comités 3 parmi 5H+4F avec au moins une femme",
   compte(combinations(range(9), 3), lambda c: any(i >= 5 for i in c)), comb(9, 3) - comb(5, 3))
ok("C(9,3) - C(5,3)", comb(9, 3) - comb(5, 3), 74)
ok("tableau : équipe 3 parmi 8", comb(8, 3), 56)

print("EXERCICE 1263 — principes")
ok("Q1 menus 3x5x4", compte(product(range(3), range(5), range(4))), 60)
ok("Q2 deux dés", compte(product(range(1, 7), repeat=2)), 36)
ok("Q3 codes 4 chiffres", compte(product(CHIFFRES, repeat=4)), 10_000)
ok("Q4 sport ou musique", 12 + 8, 20)
ok("Q5 26^6", 26 ** 6, 308_915_776)

print("EXERCICE 1264 — permutations")
ok("Q1 5!", compte(permutations(range(5))), 120)
ok("Q2 8!", compte(permutations(range(8))), 40_320)
ok("Q3 6!", f(6), 720)
ok("Q3 7!", f(7), 5_040)
ok("Q4 8!/6!", f(8) // f(6), 56)


def classe_rotation(p):
    n = len(p)
    return min(tuple(p[(i + r) % n] for i in range(n)) for r in range(n))


ok("Q5 table ronde (classes de rotations)", len({classe_rotation(p) for p in permutations("ABCD")}), 6)
ok("Q5 4!/4", f(4) // 4, 6)

print("EXERCICE 1265 — arrangements")
ok("Q1 podium 10", compte(permutations(range(10), 3)), 720)
ok("Q2 A(12,3)", perm(12, 3), 1_320)
ok("Q3 codes chiffres distincts", compte(permutations(CHIFFRES, 4)), 5_040)
for n in range(1, 10):
    for p in range(1, n + 1):
        assert perm(n, p) == perm(n, p - 1) * (n - p + 1)
print("  ✓ Q4 A(n,p)/A(n,p-1) = n-p+1 vérifiée pour n ≤ 9")
ok("Q5 bureau parmi 15", compte(permutations(range(15), 3)), 2_730)

print("EXERCICE 1266 — combinaisons")
ok("Q1 C(8,3)", compte(combinations(range(8), 3)), 56)
ok("Q2 C(10,3)", comb(10, 3), 120)
ok("Q2 C(10,7)", comb(10, 7), 120)
ok("Q3 C(52,5)", comb(52, 5), 2_598_960)
ok("Q3 52x51x50x49x48", 52 * 51 * 50 * 49 * 48, 311_875_200)
ok("Q4 C(7,3)", comb(7, 3), 35)
ok("Q4 C(7,4)", comb(7, 4), 35)
ok("Q4 7x6x5", 7 * 6 * 5, 210)

print("EXERCICE 1267 — problèmes mixtes")
ok("Q1 C(12,4)", compte(combinations(range(12), 4)), 495)
ok("Q1 12x11x10x9", 12 * 11 * 10 * 9, 11_880)
ok("Q2 MATHS", compte(permutations("MATHS")), 120)
ok("Q3 menus 5x8x4", 5 * 8 * 4, 160)
ok("Q4 C(10,5)", comb(10, 5), 252)
ok("Q4 10x9x8x7x6", 10 * 9 * 8 * 7 * 6, 30_240)
equipes = {frozenset([frozenset(c), frozenset(set(range(10)) - set(c))]) for c in combinations(range(10), 5)}
ok("Q4 deux équipes non distinguées (énumération)", len(equipes), 126)
for n in range(3, 15):
    segments = comb(n, 2)
    cotes = n
    assert segments - cotes == n * (n - 3) // 2
ok("Q5 diagonales de l'hexagone", comb(6, 2) - 6, 9)
ok("Q5 segments de l'hexagone", comb(6, 2), 15)

print("EXERCICE 1268 — applications avancées")
urne = ["R"] * 5 + ["B"] * 3
ok("Q1 exactement 2 rouges", compte(combinations(range(8), 4), lambda t: sum(urne[i] == "R" for i in t) == 2), 30)
ok("Q2 5^4", compte(product(range(1, 6), repeat=4)), 625)
ok("Q3 C(8,3)C(6,2)", comb(8, 3) * comb(6, 2), 840)
sol = [n for n in range(2, 200) if comb(n, 2) == 45]
ok("Q4 C(n,2)=45", sol, [10])
ok("Q4 discriminant", 1 + 4 * 90, 361)
# Q5 : 6 caractères, 3 lettres (répétitions permises) et 3 chiffres (répétitions permises), ordre quelconque
ok("Q5 C(6,3) x 26^3 x 10^3", comb(6, 3) * 26 ** 3 * 10 ** 3, 351_520_000)
ok("Q5 26^3", 26 ** 3, 17_576)
# contrôle par énumération sur un alphabet réduit (2 lettres, 2 chiffres) : même formule
petit = compte(product("ab01", repeat=6), lambda w: sum(c in "ab" for c in w) == 3)
ok("Q5 contrôle réduit C(6,3) x 2^3 x 2^3", petit, comb(6, 3) * 2 ** 3 * 2 ** 3)

print("EXERCICE 1269 — synthèse")
ok("Q1 parties de {a,b,c,d}", compte(product([0, 1], repeat=4)), 16)
ok("Q1 1+4+6+4+1", sum(comb(4, k) for k in range(5)), 16)
H, F = 7, 5
membres = ["H"] * H + ["F"] * F
ok("Q2 au moins 2 femmes (énumération)",
   compte(combinations(range(12), 5), lambda c: sum(membres[i] == "F" for i in c) >= 2), 596)
ok("Q2 cas 2F", comb(5, 2) * comb(7, 3), 350)
ok("Q2 cas 3F", comb(5, 3) * comb(7, 2), 210)
ok("Q2 cas 4F", comb(5, 4) * comb(7, 1), 35)
ok("Q2 cas 5F", comb(5, 5) * comb(7, 0), 1)
ok("Q2 complémentaire", comb(12, 5) - comb(7, 5) - 5 * comb(7, 4), 596)
ok("Q3 A(20,3)", perm(20, 3), 6_840)
ok("Q4 RRRBBVVV (énumération)", len(set(permutations("RRRBBVVV"))), 560)
ok("Q4 C(8,3)C(5,2)", comb(8, 3) * comb(5, 2), 560)
ok("Q4 8!/(3!2!3!)", f(8) // (f(3) * f(2) * f(3)), 560)

print("EXERCICE 1270 — applications multiples")
membres = ["H"] * 15 + ["F"] * 10
ok("Q1 au moins un H et une F (énumération)",
   compte(combinations(range(25), 5), lambda c: 0 < sum(membres[i] == "F" for i in c) < 5), 49_875)
ok("Q1 C(25,5)", comb(25, 5), 53_130)
ok("Q1 C(15,5)", comb(15, 5), 3_003)
ok("Q1 C(10,5)", comb(10, 5), 252)
ok("Q2 RRRRBBBVVV (énumération)", len(set(permutations("RRRRBBBVVV"))), 4_200)
ok("Q2 C(10,4)C(6,3)", comb(10, 4) * comb(6, 3), 4_200)
ok("Q2 C(10,4)", comb(10, 4), 210)
ok("Q2 C(6,3)", comb(6, 3), 20)
ok("Q3 A(26,3) x 10^3", perm(26, 3) * 10 ** 3, 15_600_000)
ok("Q4 C(16,4)", comb(16, 4), 1_820)
ok("Q4 16x15x14x13", 16 * 15 * 14 * 13, 43_680)

print("EXERCICE 1271 — problèmes combinés")
ok("Q1 C(8,4) A(26,4) 10^4", comb(8, 4) * perm(26, 4) * 10 ** 4, 251_160_000_000)
ok("Q1 A(26,4)", perm(26, 4), 358_800)
ok("Q2 A(30,4)", perm(30, 4), 657_720)
triplets = [(r, b, v) for r in range(6) for b in range(5) for v in range(4) if r + b + v == 6]
ok("Q3 triplets (r,b,v)", len(triplets), 18)
par_r = {r: sum(1 for t in triplets if t[0] == r) for r in range(6)}
ok("Q3 répartition selon r (0..5)", [par_r[r] for r in range(6)], [2, 3, 4, 4, 3, 2])
# contrôle : sous-multiensembles de taille 6 d'un sac de 12 boules identiques par couleur
sac = "RRRRRBBBBVVV"
ok("Q3 énumération", len({tuple(sorted(sac[i] for i in c)) for c in combinations(range(12), 6)}), 18)
ok("Q4 C(20,10)", comb(20, 10), 184_756)

print("EXERCICE 1272 — devoir surveillé")
ok("A1 4x6x5", 4 * 6 * 5, 120)
ok("A2 7!", f(7), 5_040)
ok("B1 A(12,3)", perm(12, 3), 1_320)
ok("B2 C(15,5)", comb(15, 5), 3_003)
ok("B2 15x14x13x12x11", 15 * 14 * 13 * 12 * 11, 360_360)
ok("C1 A(26,2) x 10^3", compte(permutations(LETTRES, 2)) * 10 ** 3, 650_000)
ok("C2 RRRRBBBVV (énumération)", len(set(permutations("RRRRBBBVV"))), 1_260)
ok("C2 C(9,4)C(5,3)", comb(9, 4) * comb(5, 3), 1_260)
ok("C2 9!/(4!3!2!)", f(9) // (f(4) * f(3) * f(2)), 1_260)
membres = ["H"] * 12 + ["F"] * 8
ok("D1 au moins 2 femmes (énumération)",
   compte(combinations(range(20), 4), lambda c: sum(membres[i] == "F" for i in c) >= 2), 2_590)
ok("D1 2F", comb(8, 2) * comb(12, 2), 1_848)
ok("D1 3F", comb(8, 3) * comb(12, 1), 672)
ok("D1 4F", comb(8, 4), 70)
ok("D1 complémentaire", comb(20, 4) - comb(12, 4) - 8 * comb(12, 3), 2_590)
ok("D2 C(7,3) A(26,3) 10^4", comb(7, 3) * perm(26, 3) * 10 ** 4, 5_460_000_000)
ok("E2a C(16,8)", comb(16, 8), 12_870)


def appariements(eq):
    if not eq:
        return 1
    premier, reste = eq[0], eq[1:]
    return sum(appariements(reste[:i] + reste[i + 1:]) for i in range(len(reste)))


ok("E2b appariements de 8 équipes (récursif)", appariements(list(range(8))), 105)
ok("E2b 28x15x6x1/4!", 28 * 15 * 6 * 1 // 24, 105)
ok("E2b 7x5x3x1", 7 * 5 * 3 * 1, 105)
ok("E2c C(8,4)", comb(8, 4), 70)
ok("E2c remarque : vainqueurs des 4 matchs fixés", 2 ** 4, 16)

print("COMPLÉMENTS DES CORRIGÉS RÉÉCRITS")
ok("1266 Q4 7x6x5x4 / 24", 7 * 6 * 5 * 4 // 24, 35)
ok("1266 Q5 C(8,2)", comb(8, 2), 8 * 7 // 2)
ok("1268 Q5 sans le choix des positions", 26 ** 3 * 10 ** 3, 17_576_000)
ok("1272 D1 C(20,4)", comb(20, 4), 4_845)
ok("1272 D1 C(12,4)", comb(12, 4), 495)
ok("1272 D1 8 x C(12,3)", 8 * comb(12, 3), 1_760)
ok("1272 D2 en écriture scientifique", 5_460_000_000, int(5.46e9))
ok("1272 E2b C(8,2)C(6,2)C(4,2)C(2,2)", comb(8, 2) * comb(6, 2) * comb(4, 2) * comb(2, 2), 2_520)
ok("1269 Q2 C(12,5)", comb(12, 5), 792)
ok("1269 Q2 C(7,5)", comb(7, 5), 21)
ok("1269 Q2 5 x C(7,4)", 5 * comb(7, 4), 175)
ok("1269 Q4 C(8,3)", comb(8, 3), 56)
ok("1269 Q4 C(5,2)", comb(5, 2), 10)
ok("1270 Q5 n=3 : 1+3+3+1", sum(comb(3, k) for k in range(4)), 8)
ok("1271 Q1 ordre de grandeur 2,5e11", round(251_160_000_000 / 1e11, 1), 2.5)
ok("1271 Q4 équipes distinguées = 2 x non distinguées", comb(20, 10), 2 * (comb(20, 10) // 2))
ok("1267 Q4 équipes distinguées", comb(10, 5), 252)
assert sum(1 for t in triplets) == sum(par_r.values())

print("FINITION 2026-11-02 (exercices réécrits, ajoutés, figures)")
from fractions import Fraction as Fr
import sympy as sp

# 1267 Q3 : nombres de 3 chiffres distincts, premier non nul
ok("1267 Q3 énumération", compte(range(100, 1000), lambda x: len(set(str(x))) == 3), 648)
ok("1267 Q3 9x9x8", 9 * 9 * 8, 648)
ok("1267 Q3 complémentaire 720 - 72", perm(10, 3) - perm(9, 2), 648)
# 1271 Q1 : chemins (énumération des mots D/H)
def chemins(dx, dy, passage=None):
    n = 0
    for pos_h in combinations(range(dx + dy), dy):
        x = y = 0
        par = passage is None or passage == (0, 0)
        for i in range(dx + dy):
            if i in pos_h:
                y += 1
            else:
                x += 1
            if passage is not None and (x, y) == passage:
                par = True
        n += par
    return n
ok("1271 Q1a chemins O->B(5;4)", chemins(5, 4), 126)
ok("1271 Q1a C(9,4)", comb(9, 4), 126)
ok("1271 Q1a 9x8x7x6 = 3024", 9 * 8 * 7 * 6, 3_024)
ok("1271 Q1b par C(2;2) (énumération)", chemins(5, 4, (2, 2)), 60)
ok("1271 Q1b C(4,2) x C(5,2)", comb(4, 2) * comb(5, 2), 60)
ok("1271 Q1c évitent C", 126 - 60, 66)
# 1269 Q4 : anagrammes de BANANE
ok("1269 Q4 énumération", len(set(permutations("BANANE"))), 180)
ok("1269 Q4 15 x 6 x 2", comb(6, 2) * comb(4, 2) * 2, 180)
ok("1269 Q4 6!/(2!2!)", f(6) // (f(2) * f(2)), 180)
# figures : valeurs écrites
ok("fig. complementaire 53130-3003-252", comb(25, 5) - comb(15, 5) - comb(10, 5), 49_875)
ok("fig. positions_mdp 20 x 26^3 x 10^3", comb(6, 3) * 26 ** 3 * 10 ** 3, 351_520_000)
ok("fig. positions_boules 126 x 10", comb(9, 4) * comb(5, 3), 1_260)
ok("fig. symetrie C(10,3) = C(10,7)", comb(10, 3), comb(10, 7))
# nouveau-1 : prélèvements (énumération sur un lot de 20 composants, 0..3 défectueux)
lot = list(range(20))
defect = lambda c: c < 4
ok("n1 Q1 C(20,3)", compte(combinations(lot, 3)), 1_140)
ok("n1 Q1 6840/6", 20 * 19 * 18 // 6, 1_140)
ok("n1 Q2a exactement 1 défectueux", compte(combinations(lot, 3), lambda t: sum(map(defect, t)) == 1), 480)
ok("n1 Q2a C(16,2)", comb(16, 2), 120)
ok("n1 Q2b 480/1140 = 8/19", Fr(480, 1140), Fr(8, 19))
ok("n1 Q2b ≈ 0,421", round(8 / 19, 3), 0.421)
ok("n1 Q3 aucun C(16,3)", compte(combinations(lot, 3), lambda t: not any(map(defect, t))), 560)
ok("n1 Q3 560/1140 = 28/57", Fr(560, 1140), Fr(28, 57))
ok("n1 Q3 au moins un = 29/57", 1 - Fr(28, 57), Fr(29, 57))
ok("n1 Q3 ≈ 0,509", round(29 / 57, 3), 0.509)
ok("n1 Q4 20^3", compte(product(lot, repeat=3)), 8_000)
ok("n1 Q5a exactement 1 (énumération)", compte(product(lot, repeat=3), lambda t: sum(map(defect, t)) == 1), 3_072)
ok("n1 Q5a 4 x 16 x 16", 4 * 16 * 16, 1_024)
ok("n1 Q5b 3072/8000", Fr(3072, 8000), Fr(384, 1000))
ok("n1 Q5b binomiale exacte", sp.binomial(3, 1) * sp.Rational(1, 5) * sp.Rational(4, 5) ** 2, sp.Rational(384, 1000))
ok("n1 Q6 16^3", 16 ** 3, 4_096)
ok("n1 Q6 aucun 0,512", Fr(4096, 8000), Fr(512, 1000))
ok("n1 Q6 au moins un 0,488", 1 - Fr(4096, 8000), Fr(488, 1000))
assert 29 / 57 > 0.488
# nouveau-2 : code Python EXÉCUTÉ
code_n2 = '''
def suivante(L):
    M = [1]
    for k in range(1, len(L)):
        M.append(L[k-1] + L[k])
    M.append(1)
    return M

def ligne(n):
    L = [1]
    for i in range(n):
        L = suivante(L)
    return L
'''
espace = {}
exec(code_n2, espace)
ok("n2 Q1 ligne 7", espace["ligne"](7), [comb(7, k) for k in range(8)])
ok("n2 Q1 ligne 7 écrite", espace["ligne"](7), [1, 7, 21, 35, 35, 21, 7, 1])
ok("n2 Q1 C(7,3)", comb(7, 3), 35)
ok("n2 Q2a suivante([1,3,3,1])", espace["suivante"]([1, 3, 3, 1]), [1, 4, 6, 4, 1])
ok("n2 Q3 ligne(0)", espace["ligne"](0), [1])
ok("n2 Q3 ligne(3)", espace["ligne"](3), [1, 3, 3, 1])
ok("n2 Q4 ligne(10) affichée", espace["ligne"](10), [1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1])
ok("n2 Q4a sum(ligne(10))", sum(espace["ligne"](10)), 2 ** 10)
ok("n2 Q4b ligne(10)[3] = C(10,3)", espace["ligne"](10)[3], comb(10, 3))
ok("n2 Q4b 120", comb(10, 3), 120)
ok("n2 figure : 15 + 20 = 35", comb(6, 2) + comb(6, 3), comb(7, 3))
for n in range(30):
    assert espace["ligne"](n) == [comb(n, k) for k in range(n + 1)]
ok("n2 ligne(n) = coefficients binomiaux pour n < 30", True, True)

print(f"\n{N_OK} résultats vérifiés : tout est juste.")
