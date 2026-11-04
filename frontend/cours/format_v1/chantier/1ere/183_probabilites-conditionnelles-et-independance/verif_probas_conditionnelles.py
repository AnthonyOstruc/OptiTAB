# -*- coding: utf-8 -*-
"""Vérification (sympy) de tous les calculs de la notion 183
« Probabilités conditionnelles et indépendance » (Première spécialité).

Chaque valeur citée dans cours_171.txt, fiche_83.txt et exercices.txt est
recalculée ici. Les simulations sont rejouées avec les fonctions de
figures/figures.py (mêmes graines que les figures).

    python verif_probas_conditionnelles.py   → verif_log.txt
"""
import sys
from itertools import product
from pathlib import Path

from sympy import Rational as R, expand, nsimplify, solve, symbols, Symbol
from sympy.logic.boolalg import Boolean

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI / "figures"))
import figures as FIG  # noqa: E402

N_OK = 0
ERREURS = []


def ok(etiquette, calcule, attendu, tol=None):
    """Compare une valeur calculée à la valeur écrite dans le texte."""
    global N_OK
    if isinstance(calcule, Boolean):
        calcule = bool(calcule)
    c = nsimplify(calcule) if not isinstance(calcule, (bool, str)) else calcule
    a = nsimplify(attendu) if not isinstance(attendu, (bool, str)) else attendu
    if tol is None:
        bon = (c == a)
    else:
        bon = abs(float(c) - float(a)) <= tol
    if bon:
        N_OK += 1
    else:
        ERREURS.append(f"{etiquette} : calculé {c} ≠ attendu {a}")


def d(s):
    """Décimal écrit à la française → Rational exact."""
    return R(s.replace(",", "."))


def arrondi(x, n):
    return round(float(x), n)


def arbre2(pa, pb_a, pb_abar):
    """Arbre A / Ā puis B / B̄ : renvoie les 4 chemins, P(B), P_B(A), P_B̄(Ā)."""
    pab = pa * pb_a
    pabb = pa * (1 - pb_a)
    pnab = (1 - pa) * pb_abar
    pnabb = (1 - pa) * (1 - pb_abar)
    pb = pab + pnab
    return dict(ab=pab, abb=pabb, nab=pnab, nabb=pnabb, b=pb, a_sachant_b=pab / pb,
                nbarre=1 - pb, na_sachant_nb=pnabb / (1 - pb), a_sachant_nb=pabb / (1 - pb))


# =========================================================== COURS
# Tableau croisé 200 élèves
F_T, F_nT, G_T, G_nT = 45, 75, 30, 50
ok("cours effectif F", F_T + F_nT, 120)
ok("cours effectif G", G_T + G_nT, 80)
ok("cours effectif T", F_T + G_T, 75)
ok("cours effectif non T", F_nT + G_nT, 125)
ok("cours P_F(T)", R(45, 120), d("0,375"))
ok("cours P_F(T) fraction", R(45, 120), R(3, 8))
ok("cours P_T(F)", R(45, 75), d("0,6"))
ok("cours P(F∩T)", R(45, 200), d("0,225"))
ok("cours P(F)", R(120, 200), d("0,6"))
ok("cours P(T)", R(75, 200), d("0,375"))
ok("cours indépendance F,T", R(120, 200) * R(75, 200), R(45, 200))
ok("cours P_F(T) = P(T)", R(45, 120), R(75, 200))
ok("cours P_F(non T)", 1 - R(45, 120), d("0,625"))
ok("cours P_G(T)", R(30, 80), d("0,375"))
# Exemple bus
bus = arbre2(d("0,3"), d("0,8"), d("0,1"))
ok("cours bus A∩B", bus["ab"], d("0,24"))
ok("cours bus A∩B̄", bus["abb"], d("0,06"))
ok("cours bus Ā∩B", bus["nab"], d("0,07"))
ok("cours bus Ā∩B̄", bus["nabb"], d("0,63"))
ok("cours bus somme chemins", bus["ab"] + bus["abb"] + bus["nab"] + bus["nabb"], 1)
ok("cours bus P(B)", bus["b"], d("0,31"))
ok("cours bus P_B(A) fraction", bus["a_sachant_b"], R(24, 31))
ok("cours bus P_B(A) arrondi", arrondi(bus["a_sachant_b"], 3), 0.774)
# Dépistage (cours)
dep = arbre2(d("0,02"), d("0,95"), d("0,05"))
ok("cours dep M∩T", dep["ab"], d("0,019"))
ok("cours dep M∩T̄", dep["abb"], d("0,001"))
ok("cours dep M̄∩T", dep["nab"], d("0,049"))
ok("cours dep M̄∩T̄", dep["nabb"], d("0,931"))
ok("cours dep P(T)", dep["b"], d("0,068"))
ok("cours dep P_T(M)", dep["a_sachant_b"], R(19, 68))
ok("cours dep P_T(M) arrondi", arrondi(dep["a_sachant_b"], 3), 0.279)
ok("cours dep P_T(M̄) arrondi", arrondi(1 - dep["a_sachant_b"], 2), 0.72)
# tableau sur 10 000 personnes
ok("cours 10000 malades", 10000 * d("0,02"), 200)
ok("cours 10000 M∩T", 200 * d("0,95"), 190)
ok("cours 10000 M∩T̄", 200 * d("0,05"), 10)
ok("cours 10000 sains", 10000 - 200, 9800)
ok("cours 10000 M̄∩T", 9800 * d("0,05"), 490)
ok("cours 10000 M̄∩T̄", 9800 * d("0,95"), 9310)
ok("cours 10000 T", 190 + 490, 680)
ok("cours 10000 T̄", 10 + 9310, 9320)
ok("cours 10000 P_T(M)", R(190, 680), R(19, 68))
# Indépendance (dé)
de = range(1, 7)
A = {k for k in de if k % 2 == 0}
B = {k for k in de if k <= 2}
C = {k for k in de if k <= 3}
P = lambda E: R(len(E), 6)  # noqa: E731
ok("cours dé P(A∩B)", P(A & B), R(1, 6))
ok("cours dé P(A)P(B)", P(A) * P(B), R(1, 6))
ok("cours dé P(A∩C)", P(A & C), R(1, 6))
ok("cours dé P(A)P(C)", P(A) * P(C), R(1, 4))
ok("cours dé P_B(A)", P(A & B) / P(B), R(1, 2))
# Démonstration A, B̄ : vérification symbolique
pa_, pb_ = symbols("p_A p_B")
ok("démonstration A et B̄", expand((pa_ - pa_ * pb_) - pa_ * (1 - pb_)), 0)
# Urne avec remise 3 R, 2 B
r, b = R(3, 5), R(2, 5)
ok("cours remise RR", r * r, R(9, 25))
ok("cours remise RB", r * b, R(6, 25))
ok("cours remise BR", b * r, R(6, 25))
ok("cours remise BB", b * b, R(4, 25))
ok("cours remise même couleur", r * r + b * b, R(13, 25))
ok("cours remise couleurs différentes", 2 * r * b, R(12, 25))
ok("cours remise total", r * r + 2 * r * b + b * b, 1)
ok("cours remise P(R2)", r * r + b * r, R(3, 5))
# Simulation du cours
pts, f, nt, nmt = FIG.simulation_depistage(100000)
ok("cours simulation freq(100000) ≈ 0,284", round(f, 3), 0.284)
ok("cours simulation nombre de positifs", nt, 6774)
ok("cours simulation malades positifs", nmt, 1922)
ok("cours simulation proche de 19/68", abs(f - 19 / 68) < 0.01, True)
ok("cours simulation freq(1000)", round(FIG.simulation_depistage(1000)[1], 3), 0.305)

# =========================================================== nouveau-1 : tableau croisé
AM, AnM, AT = 120, 200 - 120, 200
nAnM, TOT = 195, 500
nAT = TOT - AT
nAM = nAT - nAnM
TM = AM + nAM
TnM = AnM + nAnM
ok("n1 A∩M̄", AnM, 80)
ok("n1 total Ā", nAT, 300)
ok("n1 Ā∩M", nAM, 105)
ok("n1 total M", TM, 225)
ok("n1 total M̄", TnM, 275)
ok("n1 contrôle", TM + TnM, 500)
ok("n1 P(A)", R(AT, TOT), d("0,4"))
ok("n1 P(M)", R(TM, TOT), d("0,45"))
ok("n1 P(A∩M)", R(AM, TOT), d("0,24"))
ok("n1 P_A(M)", R(AM, AT), d("0,6"))
ok("n1 P_M(A)", R(AM, TM), R(8, 15))
ok("n1 P_M(A) arrondi", arrondi(R(AM, TM), 3), 0.533)
ok("n1 P_Ā(M)", R(nAM, nAT), d("0,35"))
ok("n1 P_M̄(Ā)", R(nAnM, TnM), R(39, 55))
ok("n1 P_M̄(Ā) arrondi", arrondi(R(nAnM, TnM), 3), 0.709)
ok("n1 P(A)P(M)", R(AT, TOT) * R(TM, TOT), d("0,18"))
ok("n1 non indépendants", R(AT, TOT) * R(TM, TOT) != R(AM, TOT), True)

# =========================================================== nouveau-3 : arbre internes / sport
n3 = arbre2(d("0,35"), d("0,6"), d("0,3"))
ok("n3 P(Ī)", 1 - d("0,35"), d("0,65"))
ok("n3 P_I(S̄)", 1 - d("0,6"), d("0,4"))
ok("n3 P_Ī(S̄)", 1 - d("0,3"), d("0,7"))
ok("n3 I∩S", n3["ab"], d("0,21"))
ok("n3 I∩S̄", n3["abb"], d("0,14"))
ok("n3 Ī∩S", n3["nab"], d("0,195"))
ok("n3 Ī∩S̄", n3["nabb"], d("0,455"))
ok("n3 P(S)", n3["b"], d("0,405"))
ok("n3 P(S̄)", n3["nbarre"], d("0,595"))
ok("n3 P_S(I)", n3["a_sachant_b"], R(14, 27))
ok("n3 P_S(I) arrondi", arrondi(n3["a_sachant_b"], 3), 0.519)
ok("n3 P_S̄(I)", n3["a_sachant_nb"], R(4, 17))
ok("n3 P_S̄(I) arrondi", arrondi(n3["a_sachant_nb"], 3), 0.235)
ok("n3 non indépendants", d("0,35") * n3["b"] != n3["ab"], True)

# =========================================================== nouveau-2 : lancers francs + simulation
n2 = arbre2(d("0,7"), d("0,8"), d("0,6"))
ok("n2 R1∩R2", n2["ab"], d("0,56"))
ok("n2 R1∩R̄2", n2["abb"], d("0,14"))
ok("n2 R̄1∩R2", n2["nab"], d("0,18"))
ok("n2 R̄1∩R̄2", n2["nabb"], d("0,12"))
ok("n2 P(R2)", n2["b"], d("0,74"))
ok("n2 P_R2(R1)", n2["a_sachant_b"], R(28, 37))
ok("n2 P_R2(R1) arrondi", arrondi(n2["a_sachant_b"], 3), 0.757)
ok("n2 P(R1)P(R2)", d("0,7") * d("0,74"), d("0,518"))
ok("n2 non indépendants", d("0,7") * d("0,74") != d("0,56"), True)
ok("n2 version indépendante P(R1∩R2)", d("0,7") * d("0,7"), d("0,49"))
ok("n2 version indépendante P(R2)", d("0,7") * d("0,7") + d("0,3") * d("0,7"), d("0,7"))
_, a, b2 = FIG.simulation_lancers(10000)
ok("n2 simulation fréquence R2", round(a, 4), 0.7409)
ok("n2 simulation fréquence R1 parmi R2", round(b2, 4), 0.7562)
ok("n2 écart 1", round(abs(a - 0.74), 4), 0.0009)
ok("n2 écart 2", round(abs(b2 - 28 / 37), 3), 0.001)

# =========================================================== 1302 : calculs de base
ok("1302 Q1 P_A(B)", d("0,2") / d("0,6"), R(1, 3))
ok("1302 Q1 P_B(A)", d("0,2") / d("0,4"), d("0,5"))
ok("1302 Q1 P_A(B̄)", 1 - d("0,2") / d("0,6"), R(2, 3))
ok("1302 Q2 P(A∩B)", d("0,3") * d("0,7"), d("0,21"))
ok("1302 Q2 P_B(Ā)", 1 - d("0,7"), d("0,3"))
ok("1302 Q2 P(Ā∩B)", d("0,3") * d("0,3"), d("0,09"))
ok("1302 Q2 contrôle", d("0,21") + d("0,09"), d("0,3"))
issues = list(product(range(1, 7), repeat=2))
S = [i for i in issues if sum(i) >= 9]
D6 = [i for i in issues if i[0] == 6]
SD = [i for i in S if i[0] == 6]
ok("1302 Q3 card S", len(S), 10)
ok("1302 Q3 card D", len(D6), 6)
ok("1302 Q3 card S∩D", len(SD), 4)
ok("1302 Q3 P(S)", R(len(S), 36), R(5, 18))
ok("1302 Q3 P_S(D)", R(len(SD), len(S)), R(2, 5))
ok("1302 Q3 P_D(S)", R(len(SD), len(D6)), R(2, 3))
ok("1302 Q3 P(S∩D)", R(len(SD), 36), R(1, 9))
ok("1302 Q3 P(D) P_D(S)", R(1, 6) * R(2, 3), R(1, 9))
cartes = [(v, c) for v in ["7", "8", "9", "10", "V", "D", "R", "A"] for c in "TCKP"]
ok("1302 Q4 32 cartes", len(cartes), 32)
Fg = [x for x in cartes if x[0] in "VDR"]
Co = [x for x in cartes if x[1] == "C"]
FC = [x for x in Fg if x[1] == "C"]
ok("1302 Q4 figures", len(Fg), 12)
ok("1302 Q4 cœurs", len(Co), 8)
ok("1302 Q4 figures cœur", len(FC), 3)
ok("1302 Q4 P_F(C)", R(len(FC), len(Fg)), R(1, 4))
ok("1302 Q4 P_C(F)", R(len(FC), len(Co)), R(3, 8))
ok("1302 Q4 P(C)", R(len(Co), 32), R(1, 4))
ok("1302 Q4 P(F)", R(len(Fg), 32), R(3, 8))

# =========================================================== 1303 : indépendance
ok("1303 Q1 produit", d("0,4") * d("0,5"), d("0,2"))
ok("1303 Q1 A∩B̄", d("0,4") - d("0,2"), d("0,2"))
ok("1303 Q1 Ā∩B", d("0,5") - d("0,2"), d("0,3"))
ok("1303 Q1 Ā", 1 - d("0,4"), d("0,6"))
ok("1303 Q1 Ā∩B̄", d("0,6") - d("0,3"), d("0,3"))
ok("1303 Q1 B̄", 1 - d("0,5"), d("0,5"))
ok("1303 Q1 Ā,B̄ indépendants", d("0,6") * d("0,5"), d("0,3"))
ok("1303 Q1 A,B̄ indépendants", d("0,4") * d("0,5"), d("0,2"))
ok("1303 Q2 produit", d("0,3") * d("0,6"), d("0,18"))
ok("1303 Q2 non indépendants", d("0,3") * d("0,6") != d("0,15"), True)
ok("1303 Q2 P_A(B)", d("0,15") / d("0,3"), d("0,5"))
A3 = {2, 4, 6}
B3 = {1, 2}
C3 = {3}
ok("1303 Q3 P(A∩B)", P(A3 & B3), R(1, 6))
ok("1303 Q3 P(A)P(B)", P(A3) * P(B3), R(1, 6))
ok("1303 Q3 A∩C vide", len(A3 & C3), 0)
ok("1303 Q3 P(A)P(C)", P(A3) * P(C3), R(1, 12))
ok("1303 Q5 P(A∩B̄)", d("0,5") * (1 - d("0,4")), d("0,3"))
ok("1303 Q5 P(A∩B)", d("0,5") * d("0,4"), d("0,2"))
ok("1303 Q5 P(A∪B)", d("0,5") + d("0,4") - d("0,2"), d("0,7"))
ok("1303 Q5 P(Ā∩B̄)", d("0,5") * d("0,6"), d("0,3"))
ok("1303 Q5 P(A∪B) par contraire", 1 - d("0,5") * d("0,6"), d("0,7"))

# =========================================================== 1310 : détecteurs indépendants
p1, p2 = d("0,9"), d("0,8")
ok("1310 D1∩D2", p1 * p2, d("0,72"))
ok("1310 D1∩D̄2", p1 * (1 - p2), d("0,18"))
ok("1310 D̄1∩D2", (1 - p1) * p2, d("0,08"))
ok("1310 D̄1∩D̄2", (1 - p1) * (1 - p2), d("0,02"))
ok("1310 exactement un", p1 * (1 - p2) + (1 - p1) * p2, d("0,26"))
ok("1310 au moins un", 1 - (1 - p1) * (1 - p2), d("0,98"))
ok("1310 au moins un (somme)", p1 * p2 + p1 * (1 - p2) + (1 - p1) * p2, d("0,98"))
ok("1310 P_alarme(deux)", (p1 * p2) / d("0,98"), R(36, 49))
ok("1310 P_alarme(deux) arrondi", arrondi(R(36, 49), 3), 0.735)
x = Symbol("p")
ok("1310 seuil p", solve(1 - (1 - p1) * (1 - x) - d("0,99"), x)[0], d("0,9"))

# =========================================================== 1309 : commandes en ligne
t = arbre2(d("0,4"), d("0,15"), d("0,05"))
ok("1309 P(T̄)", 1 - d("0,4"), d("0,6"))
ok("1309 T∩R", t["ab"], d("0,06"))
ok("1309 T∩R̄", t["abb"], d("0,34"))
ok("1309 T̄∩R", t["nab"], d("0,03"))
ok("1309 T̄∩R̄", t["nabb"], d("0,57"))
ok("1309 P(R)", t["b"], d("0,09"))
ok("1309 P_R(T)", t["a_sachant_b"], R(2, 3))
ok("1309 P_R(T) arrondi", arrondi(t["a_sachant_b"], 3), 0.667)
ok("1309 P(R̄)", t["nbarre"], d("0,91"))
ok("1309 P_R̄(T̄)", t["na_sachant_nb"], R(57, 91))
ok("1309 P_R̄(T̄) arrondi", arrondi(t["na_sachant_nb"], 3), 0.626)
ok("1309 P(T)P(R)", d("0,4") * d("0,09"), d("0,036"))

# =========================================================== 1311 : trois chaînes
pc = {"A": (d("0,5"), d("0,01")), "B": (d("0,3"), d("0,02")), "C": (d("0,2"), d("0,04"))}
ok("1311 partition", sum(v[0] for v in pc.values()), 1)
inter = {k: v[0] * v[1] for k, v in pc.items()}
ok("1311 A∩D", inter["A"], d("0,005"))
ok("1311 B∩D", inter["B"], d("0,006"))
ok("1311 C∩D", inter["C"], d("0,008"))
ok("1311 A∩D̄", d("0,5") * d("0,99"), d("0,495"))
ok("1311 B∩D̄", d("0,3") * d("0,98"), d("0,294"))
ok("1311 C∩D̄", d("0,2") * d("0,96"), d("0,192"))
pD = sum(inter.values())
ok("1311 P(D)", pD, d("0,019"))
ok("1311 P_D(A)", inter["A"] / pD, R(5, 19))
ok("1311 P_D(B)", inter["B"] / pD, R(6, 19))
ok("1311 P_D(C)", inter["C"] / pD, R(8, 19))
ok("1311 P_D(A) arrondi", arrondi(R(5, 19), 3), 0.263)
ok("1311 P_D(B) arrondi", arrondi(R(6, 19), 3), 0.316)
ok("1311 P_D(C) arrondi", arrondi(R(8, 19), 3), 0.421)
ok("1311 somme P_D", R(5, 19) + R(6, 19) + R(8, 19), 1)
ok("1311 P(D̄)", 1 - pD, d("0,981"))
ok("1311 P_D̄(A)", d("0,495") / d("0,981"), R(165, 327))
ok("1311 P_D̄(A) arrondi", arrondi(d("0,495") / d("0,981"), 3), 0.505)
q = pD
ok("1311 B D1∩D2", q * q, d("0,000361"))
ok("1311 B D1∩D̄2", q * (1 - q), d("0,018639"))
ok("1311 B D̄1∩D̄2", (1 - q) ** 2, d("0,962361"))
ok("1311 B au moins une", 1 - (1 - q) ** 2, d("0,037639"))
ok("1311 B aucune arrondi", arrondi((1 - q) ** 2, 3), 0.962)
ok("1311 B au moins une arrondi", arrondi(1 - (1 - q) ** 2, 3), 0.038)
ok("1311 B exactement une", 2 * q * (1 - q), d("0,037278"))
ok("1311 B exactement une arrondi", arrondi(2 * q * (1 - q), 3), 0.037)
ok("1311 B contrôle", d("0,037278") + d("0,000361"), d("0,037639"))
ok("1311 C 0,2y ≤ 0,004", d("0,015") - d("0,005") - d("0,006"), d("0,004"))
y = Symbol("y")
ok("1311 C seuil", solve(d("0,005") + d("0,006") + d("0,2") * y - d("0,015"), y)[0], d("0,02"))

# =========================================================== 1308 : urne 3 R 2 B sans remise
RR, RB, BR, BB = R(3, 5) * R(2, 4), R(3, 5) * R(2, 4), R(2, 5) * R(3, 4), R(2, 5) * R(1, 4)
ok("1308 RR", RR, R(3, 10))
ok("1308 RB", RB, R(3, 10))
ok("1308 BR", BR, R(3, 10))
ok("1308 BB", BB, R(1, 10))
ok("1308 somme", RR + RB + BR + BB, 1)
ok("1308 même couleur", RR + BB, R(2, 5))
ok("1308 P(R2)", RR + BR, R(3, 5))
ok("1308 P_R2(R1)", RR / (RR + BR), R(1, 2))
ok("1308 au moins une bleue", 1 - RR, R(7, 10))

# =========================================================== 1305 : dépistage
dA = arbre2(d("0,01"), d("0,98"), d("0,03"))
ok("1305 M∩T", dA["ab"], d("0,0098"))
ok("1305 M∩T̄", dA["abb"], d("0,0002"))
ok("1305 M̄∩T", dA["nab"], d("0,0297"))
ok("1305 M̄∩T̄", dA["nabb"], d("0,9603"))
ok("1305 P(T)", dA["b"], d("0,0395"))
ok("1305 P_T(M)", dA["a_sachant_b"], R(98, 395))
ok("1305 P_T(M) arrondi", arrondi(dA["a_sachant_b"], 3), 0.248)
ok("1305 P_T(M̄)", 1 - dA["a_sachant_b"], R(297, 395))
ok("1305 P_T(M̄) arrondi", arrondi(1 - dA["a_sachant_b"], 3), 0.752)
ok("1305 P(T̄)", dA["nbarre"], d("0,9605"))
ok("1305 P_T̄(M̄)", dA["na_sachant_nb"], R(9603, 9605))
ok("1305 P_T̄(M̄) arrondi", arrondi(dA["na_sachant_nb"], 4), 0.9998)
# tableau 100 000
Nn = 100000
mal = Nn * d("0,01")
ok("1305 malades", mal, 1000)
ok("1305 M∩T", mal * d("0,98"), 980)
ok("1305 M∩T̄", mal * d("0,02"), 20)
ok("1305 sains", Nn - mal, 99000)
ok("1305 M̄∩T", 99000 * d("0,03"), 2970)
ok("1305 M̄∩T̄", 99000 * d("0,97"), 96030)
ok("1305 T", 980 + 2970, 3950)
ok("1305 T̄", 20 + 96030, 96050)
ok("1305 total", 3950 + 96050, Nn)
ok("1305 tableau P_T(M)", R(980, 3950), R(98, 395))
ok("1305 faux positifs sur 4", arrondi(R(2970, 3950), 2), 0.75)
dC = arbre2(d("0,2"), d("0,98"), d("0,03"))
ok("1305 C M∩T", dC["ab"], d("0,196"))
ok("1305 C M∩T̄", dC["abb"], d("0,004"))
ok("1305 C M̄∩T", dC["nab"], d("0,024"))
ok("1305 C M̄∩T̄", dC["nabb"], d("0,776"))
ok("1305 C P(T)", dC["b"], d("0,22"))
ok("1305 C P_T(M)", dC["a_sachant_b"], R(49, 55))
ok("1305 C P_T(M) arrondi", arrondi(dC["a_sachant_b"], 3), 0.891)

# =========================================================== 1304 : trajets et retards
tr = {"V": (d("0,45"), d("0,04")), "B": (d("0,35"), d("0,12")), "A": (d("0,2"), d("0,06"))}
ok("1304 partition", sum(v[0] for v in tr.values()), 1)
ok("1304 P(A)", 1 - d("0,45") - d("0,35"), d("0,2"))
it = {k: v[0] * v[1] for k, v in tr.items()}
ok("1304 V∩R", it["V"], d("0,018"))
ok("1304 B∩R", it["B"], d("0,042"))
ok("1304 A∩R", it["A"], d("0,012"))
ok("1304 V∩R̄", d("0,45") * d("0,96"), d("0,432"))
ok("1304 B∩R̄", d("0,35") * d("0,88"), d("0,308"))
ok("1304 A∩R̄", d("0,2") * d("0,94"), d("0,188"))
pR = sum(it.values())
ok("1304 P(R)", pR, d("0,072"))
ok("1304 moyenne fausse", arrondi((d("0,04") + d("0,12") + d("0,06")) / 3, 3), 0.073)
ok("1304 moyenne ≠ P(R)", (d("0,04") + d("0,12") + d("0,06")) / 3 != pR, True)
ok("1304 P_R(B)", it["B"] / pR, R(7, 12))
ok("1304 P_R(B) arrondi", arrondi(R(7, 12), 3), 0.583)
ok("1304 P_R(V)", it["V"] / pR, d("0,25"))
ok("1304 P_R(A)", it["A"] / pR, R(1, 6))
ok("1304 P_R(A) arrondi", arrondi(R(1, 6), 3), 0.167)
ok("1304 somme P_R", R(7, 12) + R(3, 12) + R(2, 12), 1)
ok("1304 P(R̄)", 1 - pR, d("0,928"))
ok("1304 P_R̄(V)", d("0,432") / d("0,928"), R(27, 58))
ok("1304 P_R̄(V) arrondi", arrondi(R(27, 58), 3), 0.466)
z = Symbol("z")
sz = solve(d("0,018") + d("0,35") * z + d("0,012") - d("0,05"), z)[0]
ok("1304 seuil exact", sz, R(2, 35))
ok("1304 seuil arrondi", arrondi(sz, 3), 0.057)
ok("1304 0,35 p ≤ 0,02", d("0,05") - d("0,018") - d("0,012"), d("0,02"))

# =========================================================== 1306 : avec / sans remise (5 R, 3 B)
s_RR, s_RB, s_BR, s_BB = R(5, 8) * R(4, 7), R(5, 8) * R(3, 7), R(3, 8) * R(5, 7), R(3, 8) * R(2, 7)
ok("1306 sans RR", s_RR, R(5, 14))
ok("1306 sans RR non simplifié", s_RR, R(20, 56))
ok("1306 sans RB", s_RB, R(15, 56))
ok("1306 sans BR", s_BR, R(15, 56))
ok("1306 sans BB", s_BB, R(3, 28))
ok("1306 sans somme", s_RR + s_RB + s_BR + s_BB, 1)
ok("1306 sans une rouge", s_RB + s_BR, R(15, 28))
ok("1306 sans P(R2)", s_RR + s_BR, R(5, 8))
ok("1306 sans P_R2(R1)", s_RR / (s_RR + s_BR), R(4, 7))
ok("1306 sans P(R1)P(R2)", R(5, 8) * R(5, 8), R(25, 64))
ok("1306 sans non indépendants", R(25, 64) != R(5, 14), True)
ok("1306 sans même couleur", s_RR + s_BB, R(13, 28))
ok("1306 sans même couleur arrondi", arrondi(R(13, 28), 3), 0.464)
a_RR, a_RB, a_BB = R(5, 8) ** 2, R(5, 8) * R(3, 8), R(3, 8) ** 2
ok("1306 avec RR", a_RR, R(25, 64))
ok("1306 avec RB", a_RB, R(15, 64))
ok("1306 avec BB", a_BB, R(9, 64))
ok("1306 avec une rouge", 2 * a_RB, R(15, 32))
ok("1306 avec P(R2)", a_RR + a_RB, R(5, 8))
ok("1306 avec P_R2(R1)", a_RR / R(5, 8), R(5, 8))
ok("1306 avec même couleur", a_RR + a_BB, R(17, 32))
ok("1306 avec même couleur arrondi", arrondi(R(17, 32), 3), 0.531)
ok("1306 comparaison", R(17, 32) > R(13, 28), True)
ok("1306 au moins une bleue sans", 1 - s_RR, R(9, 14))
ok("1306 au moins une bleue avec", 1 - a_RR, R(39, 64))

# =========================================================== 1307 : jetons 1 à 4, avec remise
J = list(product(range(1, 5), repeat=2))
Pj = lambda E: R(len(E), 16)  # noqa: E731
ok("1307 issues", len(J), 16)
ok("1307 issue", R(1, 4) * R(1, 4), R(1, 16))
ok("1307 identiques", Pj([i for i in J if i[0] == i[1]]), R(1, 4))
ok("1307 somme 5", Pj([i for i in J if sum(i) == 5]), R(1, 4))
ok("1307 produit pair", Pj([i for i in J if (i[0] * i[1]) % 2 == 0]), R(3, 4))
ok("1307 produit impair", R(1, 2) * R(1, 2), R(1, 4))
Sp = [i for i in J if sum(i) % 2 == 0]
DP = [i for i in J if i[0] % 2 == 0 and i[1] % 2 == 0]
A1 = [i for i in J if i[0] % 2 == 0]
ok("1307 somme paire", Pj(Sp), R(1, 2))
ok("1307 deux pairs", Pj(DP), R(1, 4))
ok("1307 P_S(deux pairs)", R(len(DP), len(Sp)), R(1, 2))
ok("1307 A∩S", Pj([i for i in A1 if i in Sp]), R(1, 4))
ok("1307 P(A)P(S)", Pj(A1) * Pj(Sp), R(1, 4))
ok("1307 sommes paires par arbre", R(1, 4) + R(1, 4), R(1, 2))

# =========================================================== 1312 : DS
CB, CT, BT, TT = 168, 280, 240, 400
ok("1312 C∩B̄", CT - CB, 112)
ok("1312 C̄", TT - CT, 120)
ok("1312 C̄∩B", BT - CB, 72)
ok("1312 B̄", TT - BT, 160)
ok("1312 C̄∩B̄", (TT - CT) - (BT - CB), 48)
ok("1312 C̄∩B̄ bis", (TT - BT) - (CT - CB), 48)
ok("1312 P(C)", R(CT, TT), d("0,7"))
ok("1312 P(B)", R(BT, TT), d("0,6"))
ok("1312 P(C∩B)", R(CB, TT), d("0,42"))
ok("1312 P_C(B)", R(CB, CT), d("0,6"))
ok("1312 P_B(C)", R(CB, BT), d("0,7"))
ok("1312 indépendants", R(CT, TT) * R(BT, TT), R(CB, TT))
ok("1312 P_C̄(B)", R(72, 120), d("0,6"))
m12 = arbre2(d("0,6"), d("0,01"), d("0,03"))
ok("1312 M1∩D", m12["ab"], d("0,006"))
ok("1312 M1∩D̄", m12["abb"], d("0,594"))
ok("1312 M2∩D", m12["nab"], d("0,012"))
ok("1312 M2∩D̄", m12["nabb"], d("0,388"))
ok("1312 P(D)", m12["b"], d("0,018"))
ok("1312 P_D(M2)", m12["nab"] / m12["b"], R(2, 3))
ok("1312 P_D(M2) arrondi", arrondi(R(2, 3), 3), 0.667)
ok("1312 P(D̄)", m12["nbarre"], d("0,982"))
ok("1312 P_D̄(M1)", m12["abb"] / m12["nbarre"], R(297, 491))
ok("1312 P_D̄(M1) arrondi", arrondi(R(297, 491), 3), 0.605)
q2 = d("0,018")
ok("1312 C D1∩D2", q2 * q2, d("0,000324"))
ok("1312 C D1∩D̄2", q2 * (1 - q2), d("0,017676"))
ok("1312 C D̄1∩D̄2", (1 - q2) ** 2, d("0,964324"))
ok("1312 C au moins une", 1 - (1 - q2) ** 2, d("0,035676"))
ok("1312 C au moins une arrondi", arrondi(1 - (1 - q2) ** 2, 3), 0.036)
ok("1312 B1 P(M2)", 1 - d("0,6"), d("0,4"))

# =========================================================== compléments
ok("1305 A4 environ 75 %", arrondi(R(297, 395), 2), 0.75)
ok("1306 A4 produits en croix 350 et 320", (25 * 14, 5 * 64) == (350, 320), True)
ok("1302 Q3 1+2+3+4", 1 + 2 + 3 + 4, len(S))
ok("1310 Q6 étape", (d("0,01") / d("0,1")), d("0,1"))
ok("cours faux positifs 490 sur 680", 490 + 190, 680)


# =========================================================== codes Python des textes, exécutés tels quels
def blocs_python(fichier):
    txt = (ICI / fichier).read_text(encoding="utf-8")
    morceaux = txt.split("```python")[1:]
    return [m.split("```")[0] for m in morceaux]


import random  # noqa: E402

code_cours = [b for b in blocs_python("cours_171.txt") if "def freq" in b][0]
ns = {}
exec(code_cours, ns)
random.seed(2026)
f_txt = ns["freq"](100000)
ok("code du cours exécuté : freq(100000) = simulation des figures", f_txt, FIG.simulation_depistage(100000)[1])
ok("code du cours exécuté : freq(100000) ≈ 0,284", round(f_txt, 3), 0.284)

code_n2 = [b for b in blocs_python("exercices.txt") if "def simulation" in b][0]
ns = {}
exec(code_n2, ns)
random.seed(7)
sortie = ns["simulation"](10000)
ok("code de nouveau-2 exécuté : affichage cité", repr(sortie), "(0.7409, 0.7562424078823053)")
code_n2b = [b for b in blocs_python("exercices.txt") if "def deux_lancers" in b and "def simulation" not in b][0]
ns2 = {"random": random.random}
exec(code_n2b, ns2)
random.seed(1)
tirs = [ns2["deux_lancers"]() for _ in range(200000)]
ok("nouveau-2 Q7 fréquence R1∩R2 ≈ 0,49", abs(sum(a and b for a, b in tirs) / 200000 - 0.49) < 0.005, True)
ok("nouveau-2 Q7 fréquence R2 ≈ 0,7", abs(sum(b for a, b in tirs) / 200000 - 0.7) < 0.005, True)
for b in blocs_python("cours_171.txt") + blocs_python("exercices.txt"):
    ok("ligne de code ≤ 40 caractères", max(len(l) for l in b.splitlines()) <= 40, True)

# =========================================================== bilan
lignes = [f"{N_OK} contrôles réussis, {len(ERREURS)} erreur(s)"] + ERREURS
Path(ICI / "verif_log.txt").write_text("\n".join(lignes) + "\n", encoding="utf-8")
print("\n".join(lignes))
sys.exit(1 if ERREURS else 0)
