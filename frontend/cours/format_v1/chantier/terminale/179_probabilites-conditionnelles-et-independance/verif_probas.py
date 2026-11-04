# -*- coding: utf-8 -*-
"""Vérification exacte (fractions) de tous les résultats de la notion
« Probabilités conditionnelles et indépendance » (cours, fiche, exercices et figures).

    python verif_probas.py      → « TOUT EST JUSTE » ou la liste des écarts
"""
from fractions import Fraction as Fr
from itertools import product
from math import comb

D = lambda s: Fr(s.replace(",", "."))  # décimal écrit à la française → fraction exacte
erreurs = []


def egal(nom, calcule, attendu):
    if calcule != attendu:
        erreurs.append(f"{nom} : calculé {calcule} ({float(calcule):.6f}), écrit {attendu} ({float(attendu):.6f})")


def proche(nom, calcule, attendu, tol=Fr(1, 2000)):
    if abs(calcule - attendu) > tol:
        erreurs.append(f"{nom} : calculé {float(calcule):.6f}, écrit {float(attendu)}")


def arbre2(pa, pab, pnab):
    """P(A), P_A(B), P_Ā(B) → (P(A∩B), P(A∩B̄), P(Ā∩B), P(Ā∩B̄), P(B))."""
    q = [pa * pab, pa * (1 - pab), (1 - pa) * pnab, (1 - pa) * (1 - pnab)]
    assert sum(q) == 1
    return q + [q[0] + q[2]]


# ------------------------------------------------------------------ COURS
q = arbre2(D("0,02"), D("0,95"), D("0,1"))
egal("cours dépistage P(M∩T)", q[0], D("0,019"))
egal("cours dépistage P(M∩T̄)", q[1], D("0,001"))
egal("cours dépistage P(M̄∩T)", q[2], D("0,098"))
egal("cours dépistage P(M̄∩T̄)", q[3], D("0,882"))
egal("cours dépistage P(T)", q[4], D("0,117"))
egal("cours dépistage P_T(M) = 19/117", q[0] / q[4], Fr(19, 117))
proche("cours dépistage P_T(M) ≈ 0,162", q[0] / q[4], D("0,162"))
egal("cours dépistage P_T̄(M) = 1/883", q[1] / (1 - q[4]), Fr(1, 883))
# dé : A pair, B ≤ 2
de = range(1, 7)
pA = Fr(sum(1 for x in de if x % 2 == 0), 6)
pB = Fr(sum(1 for x in de if x <= 2), 6)
pAB = Fr(sum(1 for x in de if x % 2 == 0 and x <= 2), 6)
egal("cours dé P(A∩B)", pAB, Fr(1, 6))
egal("cours dé P(A)P(B)", pA * pB, Fr(1, 6))
# dé : A pair, C ≤ 3 (non indépendants)
pC = Fr(3, 6)
pAC = Fr(sum(1 for x in de if x % 2 == 0 and x <= 3), 6)
egal("cours dé P(A∩C)", pAC, Fr(1, 6))
egal("cours dé P(A)P(C)", pA * pC, Fr(1, 4))
# penalties
p, qq = D("0,6"), D("0,4")
chemins = {"".join(c): 1 for c in product("SE", repeat=3)}
for c in chemins:
    v = Fr(1)
    for l in c:
        v *= p if l == "S" else qq
    chemins[c] = v
attendus = {"SSS": "0,216", "SSE": "0,144", "SES": "0,144", "SEE": "0,096",
            "ESS": "0,144", "ESE": "0,096", "EES": "0,096", "EEE": "0,064"}
for c, v in attendus.items():
    egal(f"cours penalties {c}", chemins[c], D(v))
egal("cours penalties exactement 2", sum(v for c, v in chemins.items() if c.count("S") == 2), D("0,432"))
egal("cours penalties au moins 1", 1 - qq ** 3, D("0,936"))
# partition : exemple numérique du cours (trois ateliers)
pb = D("0,5") * D("0,02") + D("0,3") * D("0,03") + D("0,2") * D("0,05")
egal("cours partition P(B)", pb, D("0,029"))
egal("cours partition P_B(A3)", D("0,2") * D("0,05") / pb, Fr(10, 29))

# ------------------------------------------------------------------ 1283 (DS)
egal("1283 A1 P_B(A)", D("0,15") / D("0,4"), D("0,375"))
egal("1283 A1 P_A(B)", D("0,15") / D("0,5"), D("0,3"))
egal("1283 A2", Fr(1, 13), Fr(1, 13))
q = [Fr(4, 10) * Fr(3, 9), Fr(4, 10) * Fr(6, 9), Fr(6, 10) * Fr(4, 9), Fr(6, 10) * Fr(5, 9)]
egal("1283 B1 RR", q[0], Fr(2, 15)); egal("1283 B1 RB", q[1], Fr(4, 15))
egal("1283 B1 BR", q[2], Fr(4, 15)); egal("1283 B1 BB", q[3], Fr(1, 3))
egal("1283 B1 différentes", q[1] + q[2], Fr(8, 15))
n2 = sum(1 for c in product("FP", repeat=3) if c.count("F") == 2)
egal("1283 B2", Fr(n2, 8), Fr(3, 8))
O = list(product(de, de))
A = {o for o in O if o[0] % 2 == 0}; B = {o for o in O if o[1] > 3}
egal("1283 C1 P(A∩B)", Fr(len(A & B), 36), Fr(1, 4))
egal("1283 C1 P(A)P(B)", Fr(len(A), 36) * Fr(len(B), 36), Fr(1, 4))
egal("1283 C2", D("0,6") + D("0,5") - D("0,6") * D("0,5"), D("0,8"))
q = arbre2(D("0,6"), D("0,01"), D("0,03"))
egal("1283 D1 M1∩D", q[0], D("0,006")); egal("1283 D1 M1∩D̄", q[1], D("0,594"))
egal("1283 D1 M2∩D", q[2], D("0,012")); egal("1283 D1 M2∩D̄", q[3], D("0,388"))
egal("1283 D1 P(D)", q[4], D("0,018"))
egal("1283 E1 P_D(M2)", q[2] / q[4], Fr(2, 3))
q = arbre2(D("0,55"), D("0,75"), D("0,6"))
egal("1283 D2 F∩S", q[0], D("0,4125")); egal("1283 D2 F∩S̄", q[1], D("0,1375"))
egal("1283 D2 G∩S", q[2], D("0,27")); egal("1283 D2 G∩S̄", q[3], D("0,18"))
egal("1283 D2 P(S)", q[4], D("0,6825"))
q = arbre2(D("0,04"), D("0,97"), D("0,08"))
egal("1283 E2 M∩T", q[0], D("0,0388")); egal("1283 E2 M∩T̄", q[1], D("0,0012"))
egal("1283 E2 M̄∩T", q[2], D("0,0768")); egal("1283 E2 M̄∩T̄", q[3], D("0,8832"))
egal("1283 E2 P(T)", q[4], D("0,1156"))
egal("1283 E2 P_T(M) = 97/289", q[0] / q[4], Fr(97, 289))
proche("1283 E2 ≈ 0,336", q[0] / q[4], D("0,336"))

# ------------------------------------------------------------------ 1280
q = [Fr(5, 8) * Fr(4, 7), Fr(5, 8) * Fr(3, 7), Fr(3, 8) * Fr(5, 7), Fr(3, 8) * Fr(2, 7)]
egal("1280 Q1 RR", q[0], Fr(5, 14)); egal("1280 Q1 RV", q[1], Fr(15, 56))
egal("1280 Q1 VR", q[2], Fr(15, 56)); egal("1280 Q1 VV", q[3], Fr(3, 28))
assert sum(q) == 1
S10 = {o for o in O if sum(o) == 10}; S6 = {o for o in O if o[0] == 6}
egal("1280 Q2 P(S10)", Fr(len(S10), 36), Fr(1, 12))
egal("1280 Q2", Fr(len(S10 & S6), len(S10)), Fr(1, 3))
q = arbre2(Fr(18, 30), Fr(10, 18), Fr(8, 12))
egal("1280 Q3 F∩S", q[0], Fr(1, 3)); egal("1280 Q3 F∩S̄", q[1], Fr(4, 15))
egal("1280 Q3 G∩S", q[2], Fr(4, 15)); egal("1280 Q3 G∩S̄", q[3], Fr(2, 15))
egal("1280 Q3 P(S)", q[4], Fr(3, 5)); egal("1280 Q3 effectifs", Fr(18, 30), Fr(3, 5))
q = arbre2(D("0,05"), D("0,98"), D("0,05"))
egal("1280 Q4 M∩T", q[0], D("0,049")); egal("1280 Q4 M∩T̄", q[1], D("0,001"))
egal("1280 Q4 M̄∩T", q[2], D("0,0475")); egal("1280 Q4 M̄∩T̄", q[3], D("0,9025"))
egal("1280 Q4 P(T)", q[4], D("0,0965"))
egal("1280 Q5", Fr(3, 51), Fr(1, 17))

# ------------------------------------------------------------------ 1273
egal("1273 Q1 P_B(A)", D("0,2") / D("0,4"), D("0,5"))
egal("1273 Q1 P_A(B)", D("0,2") / D("0,6"), Fr(1, 3))
S9 = {o for o in O if sum(o) > 9}
egal("1273 Q2 card", Fr(len(S9)), Fr(6))
egal("1273 Q2", Fr(len(S9 & S6), len(S9)), Fr(1, 2))
egal("1273 Q3", Fr(3, 9), Fr(1, 3))
egal("1273 Q4", D("0,7") * D("0,3"), D("0,21"))
egal("1273 Q5", Fr(3, 12), Fr(1, 4))

# ------------------------------------------------------------------ 1281
A = {o for o in O if o[0] % 2 == 0}; B = {o for o in O if o[1] % 2 == 1}
egal("1281 Q1 P(A∩B)", Fr(len(A & B), 36), Fr(1, 4))
egal("1281 Q1 P(A)P(B)", Fr(len(A), 36) * Fr(len(B), 36), Fr(1, 4))
q = [Fr(3, 5) * Fr(3, 5), Fr(3, 5) * Fr(2, 5), Fr(2, 5) * Fr(3, 5), Fr(2, 5) * Fr(2, 5)]
egal("1281 Q2 RR", q[0], Fr(9, 25)); egal("1281 Q2 RB", q[1], Fr(6, 25))
egal("1281 Q2 BB", q[3], Fr(4, 25))
egal("1281 Q3", Fr(sum(1 for c in product("PF", repeat=3) if c.count("P") == 2), 8), Fr(3, 8))
egal("1281 Q4", D("0,4") + D("0,6") - D("0,4") * D("0,6"), D("0,76"))
q = arbre2(D("0,9"), D("0,8"), D("0,8"))
egal("1281 Q5 C1∩C2", q[0], D("0,72")); egal("1281 Q5 C1∩C̄2", q[1], D("0,18"))
egal("1281 Q5 C̄1∩C2", q[2], D("0,08")); egal("1281 Q5 C̄1∩C̄2", q[3], D("0,02"))

# ------------------------------------------------------------------ 1274
egal("1274 Q1", D("0,4") * D("0,5"), D("0,2"))
egal("1274 Q2", Fr(1, 6) * Fr(1, 6), Fr(1, 36))
# 1274 Q3 réécrite le 2026-11-02 (ancienne question = doublon de 1281 Q4) : voir FINITION
egal("1274 Q5", D("0,5") * (1 - D("0,4")), D("0,3"))
egal("1274 Q6 P(A)P(B)", Fr(1, 2) * Fr(1, 6), Fr(1, 12))

# ------------------------------------------------------------------ 1282
pa, pb_, pc = D("0,5"), D("0,3"), D("0,2")
d = [pa * D("0,01"), pb_ * D("0,02"), pc * D("0,04")]
egal("1282 Q1 A∩D", d[0], D("0,005")); egal("1282 Q1 B∩D", d[1], D("0,006")); egal("1282 Q1 C∩D", d[2], D("0,008"))
egal("1282 Q1 A∩D̄", pa * D("0,99"), D("0,495")); egal("1282 Q1 B∩D̄", pb_ * D("0,98"), D("0,294"))
egal("1282 Q1 C∩D̄", pc * D("0,96"), D("0,192"))
egal("1282 Q1a P(D)", sum(d), D("0,019"))
egal("1282 Q1b P_D(C) = 8/19", d[2] / sum(d), Fr(8, 19)); proche("1282 Q1b ≈ 0,421", d[2] / sum(d), D("0,421"))
egal("1282 Q2 combinaisons", Fr(comb(4, 2) * 48, comb(52, 3)), Fr(72, 5525))
egal("1282 Q2 arbre", 3 * Fr(4, 52) * Fr(3, 51) * Fr(48, 50), Fr(72, 5525))
egal("1282 Q2 chemin", Fr(4, 52) * Fr(3, 51) * Fr(48, 50), Fr(24, 5525))
egal("1282 Q2 C(52,3)", Fr(comb(52, 3)), Fr(22100))
proche("1282 Q2 ≈ 0,0130", Fr(72, 5525), D("0,0130"), Fr(1, 20000))
q = arbre2(D("0,03"), D("0,96"), D("0,06"))
egal("1282 Q3 M∩T", q[0], D("0,0288")); egal("1282 Q3 M∩T̄", q[1], D("0,0012"))
egal("1282 Q3 M̄∩T", q[2], D("0,0582")); egal("1282 Q3 M̄∩T̄", q[3], D("0,9118"))
egal("1282 Q3a P(T)", q[4], D("0,087"))
egal("1282 Q3b P_T(M) = 48/145", q[0] / q[4], Fr(48, 145)); proche("1282 Q3b ≈ 0,331", q[0] / q[4], D("0,331"))
egal("1282 Q4 RRR", Fr(5, 8) * Fr(4, 7) * Fr(3, 6), Fr(5, 28))
egal("1282 Q4", 1 - Fr(5, 28), Fr(23, 28))
egal("1282 Q5", 1 - Fr(5, 6) ** 4, Fr(671, 1296)); egal("1282 Q5 (5/6)^4", Fr(5, 6) ** 4, Fr(625, 1296))
proche("1282 Q5 ≈ 0,518", Fr(671, 1296), D("0,518"))

# ------------------------------------------------------------------ 1279
q = [Fr(3, 5) * Fr(2, 4), Fr(3, 5) * Fr(2, 4), Fr(2, 5) * Fr(3, 4), Fr(2, 5) * Fr(1, 4)]
egal("1279 Q1 RR", q[0], Fr(3, 10)); egal("1279 Q1 RB", q[1], Fr(3, 10))
egal("1279 Q1 BR", q[2], Fr(3, 10)); egal("1279 Q1 BB", q[3], Fr(1, 10))
egal("1279 Q2", Fr(1, 4) + Fr(1, 4), Fr(1, 2))
q = [Fr(2, 5) * Fr(2, 5), Fr(2, 5) * Fr(3, 5), Fr(3, 5) * Fr(2, 5), Fr(3, 5) * Fr(3, 5)]
egal("1279 Q3 BB", q[0], Fr(4, 25)); egal("1279 Q3 BN", q[1], Fr(6, 25)); egal("1279 Q3 NN", q[3], Fr(9, 25))
egal("1279 Q3", q[1] + q[2], Fr(12, 25))
pj = {"V": Fr(2, 5), "J": Fr(2, 5), "R": Fr(1, 5)}
egal("1279 Q4", sum(v * v for v in pj.values()), Fr(9, 25))
for a in "VJR":
    for b in "VJR":
        pass  # produits affichés sur la figure : vérifiés ci-dessous
fig_q4 = {("V", "V"): Fr(4, 25), ("V", "J"): Fr(4, 25), ("V", "R"): Fr(2, 25), ("J", "V"): Fr(4, 25),
          ("J", "J"): Fr(4, 25), ("J", "R"): Fr(2, 25), ("R", "V"): Fr(2, 25), ("R", "J"): Fr(2, 25), ("R", "R"): Fr(1, 25)}
for (a, b), v in fig_q4.items():
    egal(f"1279 Q4 figure {a}{b}", pj[a] * pj[b], v)
# Q5 : 4 R, 6 B, 3 tirages sans remise
def chemins_sans_remise(r, b, n):
    out = {}
    for c in product("RB", repeat=n):
        rr, bb, v = r, b, Fr(1)
        for l in c:
            tot = rr + bb
            if l == "R":
                v *= Fr(rr, tot); rr -= 1
            else:
                v *= Fr(bb, tot); bb -= 1
        out["".join(c)] = v
    return out
c5 = chemins_sans_remise(4, 6, 3)
fig_q5 = {"RRR": Fr(1, 30), "RRB": Fr(1, 10), "RBR": Fr(1, 10), "RBB": Fr(1, 6),
          "BRR": Fr(1, 10), "BRB": Fr(1, 6), "BBR": Fr(1, 6), "BBB": Fr(1, 6)}
for k, v in fig_q5.items():
    egal(f"1279 Q5 figure {k}", c5[k], v)
egal("1279 Q5", 1 - c5["BBB"], Fr(5, 6))

# ------------------------------------------------------------------ 1275 / 1276
pm = [D("0,40"), D("0,35"), D("0,25")]; pd = [D("0,02"), D("0,03"), D("0,05")]
inter = [a * b for a, b in zip(pm, pd)]
egal("1275 Q1 M1∩D", inter[0], D("0,008")); egal("1275 Q1 M2∩D", inter[1], D("0,0105"))
egal("1275 Q1 M3∩D", inter[2], D("0,0125"))
egal("1275 Q1 M1∩D̄", pm[0] * (1 - pd[0]), D("0,392")); egal("1275 Q1 M2∩D̄", pm[1] * (1 - pd[1]), D("0,3395"))
egal("1275 Q1 M3∩D̄", pm[2] * (1 - pd[2]), D("0,2375"))
egal("1275 Q1 P(D)", sum(inter), D("0,031"))
egal("1276 Q1 P_D(M3) = 25/62", inter[2] / sum(inter), Fr(25, 62)); proche("1276 Q1 ≈ 0,403", inter[2] / sum(inter), D("0,403"))
q = arbre2(D("0,6"), D("0,7"), D("0,5"))
egal("1275 Q2 F∩M", q[0], D("0,42")); egal("1275 Q2 F∩M̄", q[1], D("0,18"))
egal("1275 Q2 G∩M", q[2], D("0,2")); egal("1275 Q2 G∩M̄", q[3], D("0,2")); egal("1275 Q2 P(M)", q[4], D("0,62"))
q = arbre2(D("0,02"), D("0,95"), D("0,1"))
egal("1275 Q3 P(T)", q[4], D("0,117"))
egal("1276 Q2 P_T(M) = 19/117", q[0] / q[4], Fr(19, 117)); proche("1276 Q2 ≈ 0,162", q[0] / q[4], D("0,162"))
q = arbre2(Fr(1, 2), Fr(3, 5), Fr(1, 5))
egal("1275 Q4 A∩R", q[0], Fr(3, 10)); egal("1275 Q4 A∩R̄", q[1], Fr(1, 5))
egal("1275 Q4 B∩R", q[2], Fr(1, 10)); egal("1275 Q4 B∩R̄", q[3], Fr(2, 5)); egal("1275 Q4 P(R)", q[4], Fr(2, 5))
egal("1276 Q3 P_R(A)", q[0] / q[4], Fr(3, 4))
q = arbre2(D("0,7"), D("0,9"), D("0,3"))
egal("1275 Q5 R∩S", q[0], D("0,63")); egal("1275 Q5 R∩S̄", q[1], D("0,07"))
egal("1275 Q5 R̄∩S", q[2], D("0,09")); egal("1275 Q5 R̄∩S̄", q[3], D("0,21")); egal("1275 Q5 P(S)", q[4], D("0,72"))
egal("1276 Q4 P_S(R)", q[0] / q[4], D("0,875"))

# ------------------------------------------------------------------ 1277
c7 = chemins_sans_remise(5, 3, 3)
fig_1277 = {"RRR": Fr(5, 28), "RRB": Fr(5, 28), "RBR": Fr(5, 28), "RBB": Fr(5, 56),
            "BRR": Fr(5, 28), "BRB": Fr(5, 56), "BBR": Fr(5, 56), "BBB": Fr(1, 56)}
for k, v in fig_1277.items():
    egal(f"1277 figure {k}", c7[k], v)
egal("1277 Q1", c7["RRR"], Fr(5, 28))
egal("1277 Q2", sum(v for k, v in c7.items() if k.count("R") == 2), Fr(15, 28))
egal("1277 Q3", 1 - c7["RRR"], Fr(23, 28))
egal("1277 Q4", Fr(3, 7) * Fr(2, 6), Fr(1, 7))
egal("1277 Q4 (définition)", (c7["RBB"]) / Fr(5, 8), Fr(1, 7))
egal("1277 Q5", sum(v for k, v in c7.items() if k[2] == "R"), Fr(5, 8))
egal("1277 Q5 /336", sum(v for k, v in c7.items() if k[2] == "R") * 336, Fr(210))

# ------------------------------------------------------------------ 1278
J = list(product(range(1, 5), repeat=2))
egal("1278 Q1", Fr(len(J)), Fr(16))
egal("1278 Q2", Fr(sum(1 for a, b in J if a == b), 16), Fr(1, 4))
egal("1278 Q3", Fr(sum(1 for a, b in J if a + b == 5), 16), Fr(1, 4))
egal("1278 Q4", Fr(sum(1 for a, b in J if (a * b) % 2 == 0), 16), Fr(3, 4))
sp = [(a, b) for a, b in J if (a + b) % 2 == 0]
egal("1278 Q5 card", Fr(len(sp)), Fr(8))
egal("1278 Q5", Fr(sum(1 for a, b in sp if a % 2 == 0 and b % 2 == 0), len(sp)), Fr(1, 2))

# ================================================================== FINITION 2026-11-02
import sympy as sp

# cours IV : tableau croisé urne × roue (produits, somme 1)
ligne = {"R": D("0,3"), "B": D("0,7")}
col = {1: D("0,5"), 2: D("0,3"), 3: D("0,2")}
ecrit = {("R", 1): "0,15", ("R", 2): "0,09", ("R", 3): "0,06", ("B", 1): "0,35", ("B", 2): "0,21", ("B", 3): "0,14"}
for (l, c), v in ecrit.items():
    egal(f"cours tableau {l}{c}", ligne[l] * col[c], D(v))
egal("cours tableau somme", sum(ligne[l] * col[c] for l in ligne for c in col), Fr(1))
# cours IV : lien binomiale (penalties)
egal("cours B(3;0,6) P(X=2)", comb(3, 2) * D("0,6") ** 2 * D("0,4"), D("0,432"))

# 1273 Q1 : tableau croisé
pA, pB, pAB = D("0,6"), D("0,4"), D("0,2")
for nom, v, e in [("A∩B̄", pA - pAB, "0,4"), ("Ā∩B", pB - pAB, "0,2"), ("Ā∩B̄", 1 - pA - pB + pAB, "0,2"),
                  ("B̄", 1 - pB, "0,6"), ("Ā", 1 - pA, "0,4")]:
    egal(f"1273 Q1 tableau {nom}", v, D(e))
# 1273 Q2 : figure (cases colorées) par énumération
De = list(product(range(1, 7), repeat=2))
Bc = [(a, b) for a, b in De if a + b > 9]
egal("1273 figure B", Fr(len(Bc)), Fr(6))
egal("1273 figure A∩B", Fr(sum(1 for a, b in Bc if a == 6)), Fr(3))

# 1274 Q1 : tableau croisé
pA, pB, pAB = D("0,4"), D("0,5"), D("0,2")
for nom, v, e in [("A∩B̄", pA - pAB, "0,2"), ("Ā∩B", pB - pAB, "0,3"), ("Ā∩B̄", 1 - pA - pB + pAB, "0,3"),
                  ("Ā", 1 - pA, "0,6"), ("B̄", 1 - pB, "0,5")]:
    egal(f"1274 Q1 tableau {nom}", v, D(e))
egal("1274 Q1 P_A(B)", pAB / pA, pB)
# 1274 Q3 réécrite : P(A ∪ B) = 0,58 avec A, B indépendants, P(A) = 0,3 → P(B)
x = sp.symbols("x")
sol = sp.solve(sp.Rational(3, 10) + x - sp.Rational(3, 10) * x - sp.Rational(58, 100), x)
egal("1274 Q3 P(B)", Fr(str(sol[0])), D("0,4"))
egal("1274 Q3 0,28/0,7", D("0,28") / D("0,7"), D("0,4"))
egal("1274 Q3 vérif P(A∩B)", D("0,3") * D("0,4"), D("0,12"))
egal("1274 Q3 vérif réunion", D("0,3") + D("0,4") - D("0,12"), D("0,58"))
# 1274 Q6 : figure
egal("1274 figure P(A)P(B)", Fr(3, 6) * Fr(1, 6), Fr(1, 12))

# 1278 Q5 : figure (8 cases S, 4 cases E)
egal("1278 figure S", Fr(sum(1 for a, b in J if (a + b) % 2 == 0)), Fr(8))
egal("1278 figure E", Fr(sum(1 for a, b in J if a % 2 == 0 and b % 2 == 0)), Fr(4))

# 1279 Q1 : arbre à compléter (valeurs en vert)
for nom, v, e in [("R1", Fr(3, 5), Fr(3, 5)), ("RR", Fr(3, 5) * Fr(2, 4), Fr(3, 10)), ("RB", Fr(3, 5) * Fr(2, 4), Fr(3, 10)),
                  ("BR", Fr(2, 5) * Fr(3, 4), Fr(3, 10)), ("BB", Fr(2, 5) * Fr(1, 4), Fr(1, 10))]:
    egal(f"1279 Q1 figure {nom}", v, e)

# 1280 Q3 : tableau croisé des effectifs
egal("1280 tableau F∩S̄", Fr(18 - 10), Fr(8))
egal("1280 tableau G∩S̄", Fr(12 - 8), Fr(4))
egal("1280 tableau S", Fr(10 + 8, 30), Fr(3, 5))
egal("1280 tableau P_F(S)", Fr(10, 18), Fr(5, 9))

# nouveau-1 : trois feux indépendants (0,6 ; 0,5 ; 0,7), puis B(4 ; 0,6)
pf = [D("0,6"), D("0,5"), D("0,7")]
chem = {}
for t in product([1, 0], repeat=3):
    pr = Fr(1)
    for i, v in enumerate(t):
        pr *= pf[i] if v else 1 - pf[i]
    chem[t] = pr
egal("n1 somme des chemins", sum(chem.values()), Fr(1))
egal("n1 Q2", chem[(1, 1, 1)], D("0,21"))
for t, e in [((1, 1, 0), "0,09"), ((1, 0, 1), "0,21"), ((0, 1, 1), "0,14")]:
    egal(f"n1 Q3 chemin {t}", chem[t], D(e))
egal("n1 Q3", sum(v for t, v in chem.items() if sum(t) == 2), D("0,44"))
egal("n1 Q4 aucun", chem[(0, 0, 0)], D("0,06"))
egal("n1 Q4", 1 - chem[(0, 0, 0)], D("0,94"))
# figure du corrigé : « k verts : p » pour chaque feuille
ecrit_fig = {(1, 1, 1): "0,21", (1, 1, 0): "0,09", (1, 0, 1): "0,21", (1, 0, 0): "0,09",
             (0, 1, 1): "0,14", (0, 1, 0): "0,06", (0, 0, 1): "0,14", (0, 0, 0): "0,06"}
for t, e in ecrit_fig.items():
    egal(f"n1 figure {t}", chem[t], D(e))
# Q5 : les chemins à deux verts n'ont pas la même probabilité
assert len({v for t, v in chem.items() if sum(t) == 2}) == 3
# Partie B
egal("n1 Q7 P(X=2)", comb(4, 2) * D("0,6") ** 2 * D("0,4") ** 2, D("0,3456"))
egal("n1 Q7 6×0,36×0,16", 6 * D("0,36") * D("0,16"), D("0,3456"))
egal("n1 Q7 0,4^4", D("0,4") ** 4, D("0,0256"))
egal("n1 Q7 P(X>=1)", 1 - D("0,4") ** 4, D("0,9744"))
egal("n1 Q7 C(4,2)", Fr(comb(4, 2)), Fr(6))

if erreurs:
    print("ÉCARTS :")
    for e in erreurs:
        print("  ✗", e)
else:
    print("TOUT EST JUSTE")
