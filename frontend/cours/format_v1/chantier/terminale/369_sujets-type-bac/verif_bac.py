# -*- coding: utf-8 -*-
"""Vérification de tous les calculs de la notion 369 « Sujets type bac » (Terminale).

    python verif_bac.py            (écrit aussi verif_log.txt)

Sujet 01 (exercices.txt), cours de méthode (cours_370.txt), fiche (fiche_308.txt).
Toutes les valeurs de la loi binomiale sont CALCULÉES ici (math.comb), jamais recopiées ;
le barème est relu dans le texte du corrigé et additionné ; la fonction Python du corrigé
est extraite du texte et exécutée.
"""
import re
import sys
from math import comb, exp, log
from pathlib import Path

import sympy as sp

ICI = Path(__file__).resolve().parent
LOG = []
NB = [0, 0]  # contrôles, erreurs


def ok(cond, msg):
    NB[0] += 1
    if not cond:
        NB[1] += 1
    LOG.append(("OK  " if cond else "ERREUR ") + msg)


def arr(x, n):
    """Arrondi décimal « au plus proche » sur la valeur exacte (float suffisant ici)."""
    return round(float(x) + 0.0, n)


def egal(a, b, tol=1e-12):
    return abs(float(a) - float(b)) < tol


x, t, C = sp.symbols("x t C", real=True)
TXT = (ICI / "exercices.txt").read_text(encoding="utf-8")
COURS = (ICI / "cours_370.txt").read_text(encoding="utf-8")
FICHE = (ICI / "fiche_308.txt").read_text(encoding="utf-8")

# =========================================================================== EXERCICE 1
LOG.append("== Exercice 1 : probabilités")
pR, pRL, pNL = sp.Rational(7, 10), sp.Rational(5, 100), sp.Rational(12, 100)
pRinterL = pR * pRL
pNinterL = (1 - pR) * pNL
pL = pRinterL + pNinterL
ok(pRinterL == sp.Rational(35, 1000), "P(R∩L) = 0,035")
ok(pNinterL == sp.Rational(36, 1000), "P(R̄∩L) = 0,036")
ok(pL == sp.Rational(71, 1000), "P(L) = 0,071")
ok(pR * (1 - pRL) == sp.Rational(665, 1000) and (1 - pR) * (1 - pNL) == sp.Rational(264, 1000),
   "feuilles de l'arbre : P(R∩L̄) = 0,665 et P(R̄∩L̄) = 0,264")
ok(pR * pRL + pR * (1 - pRL) + (1 - pR) * pNL + (1 - pR) * (1 - pNL) == 1, "somme des 4 chemins = 1")
pLR = pNinterL / pL
ok(pLR == sp.Rational(36, 71) and arr(pLR, 3) == 0.507, f"P_L(R̄) = 36/71 ≈ {float(pLR):.5f} → 0,507")

n, p = 50, 0.071
loi50 = [comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)]
ok(abs(sum(loi50) - 1) < 1e-12, "somme de la loi B(50 ; 0,071) = 1")
ok(arr(loi50[0], 4) == 0.0252 and arr(loi50[1], 4) == 0.0962 and arr(loi50[2], 4) == 0.1801,
   f"P(X=0), P(X=1), P(X=2) ≈ {loi50[0]:.5f}, {loi50[1]:.5f}, {loi50[2]:.5f} (texte : 0,025 2 ; 0,096 2 ; 0,180 1)")
ok(egal(loi50[0], 0.929 ** 50, 1e-15) and comb(50, 2) == 1225, "P(X=0) = 0,929^50 et C(50,2) = 1225")
p2 = sum(loi50[:3])
ok(arr(p2, 3) == 0.301, f"P(X ≤ 2) ≈ {p2:.5f} → 0,301")
ok(arr(1 - p2, 3) == 0.699, f"P(X ≥ 3) ≈ {1 - p2:.5f} → 0,699")
ok(egal(n * p, 3.55, 1e-12), "E(X) = 50 × 0,071 = 3,55")
seuil_n = log(0.01) / log(0.929)
ok(62.5 < seuil_n < 62.54 and f"{seuil_n:.2f}" == "62.53", f"ln(0,01)/ln(0,929) ≈ {seuil_n:.4f} → 62,53")
nmin = next(k for k in range(1, 1000) if 1 - 0.929 ** k >= 0.99)
ok(nmin == 63, f"plus petit n tel que 1 − 0,929^n ≥ 0,99 : {nmin}")
ok(f"{1 - 0.929 ** 62:.4f}" == "0.9896" and f"{1 - 0.929 ** 63:.4f}" == "0.9903",
   f"vérification : 1 − 0,929^62 ≈ {1 - 0.929 ** 62:.5f} ; 1 − 0,929^63 ≈ {1 - 0.929 ** 63:.5f}")
ok(log(0.929) < 0, "ln(0,929) < 0 (changement de sens)")

# =========================================================================== EXERCICE 2
LOG.append("== Exercice 2 : vrai ou faux")
ok(comb(12, 3) == 220 and comb(5, 3) == 10 and comb(12, 3) - comb(5, 3) == 210, "A1 : C(12,3) − C(5,3) = 220 − 10 = 210 (VRAIE)")
ok(sum(comb(7, k) * comb(5, 3 - k) for k in range(1, 4)) == 210, "A1 : contrôle direct 1, 2 ou 3 femmes = 210")
ok(12 * 11 * 10 == 1320, "A1 : arrangements 12 × 11 × 10 = 1320 (piège)")
g = 4 * sp.exp(-2 * x)
ok(sp.simplify(sp.diff(g, x) - (-2 * g + 2)) != 0, "A2 : g = 4e^{-2x} n'est pas solution (FAUSSE)")
ok(sp.diff(g, x).subs(x, 0) == -8 and (-2 * g + 2).subs(x, 0) == -6, "A2 : g'(0) = −8 et −2g(0) + 2 = −6")
y = sp.Function("y")
sol = sp.dsolve(sp.Eq(y(x).diff(x), -2 * y(x) + 2), y(x), ics={y(0): 4})
ok(sp.simplify(sol.rhs - (3 * sp.exp(-2 * x) + 1)) == 0, f"A2 : solution avec y(0) = 4 : {sol.rhs}")
ok(sp.Rational(-2, -2) == 1, "A2 : −b/a = 1")
Sln = sp.solveset(sp.And(x > 2, x * (x - 2) <= 3), x, sp.S.Reals) if False else None
dom = sp.Interval.open(2, sp.oo)
ineq = sp.solveset(x ** 2 - 2 * x - 3 <= 0, x, sp.S.Reals)
ok(ineq == sp.Interval(-1, 3), "A3 : x² − 2x − 3 ≤ 0 ⟺ x ∈ [−1 ; 3]")
ok(sp.factor(x ** 2 - 2 * x - 3) == (x - 3) * (x + 1), "A3 : x² − 2x − 3 = (x + 1)(x − 3)")
ok(ineq.intersect(dom) == sp.Interval.Lopen(2, 3), "A3 : ensemble des solutions ]2 ; 3] (FAUSSE)")
for v in (2.5, 3):
    ok(log(v) + log(v - 2) <= log(3) + 1e-12, f"A3 : x = {v} est solution")
ok(log(3.01) + log(1.01) > log(3), "A3 : x = 3,01 n'est pas solution")
VM = sp.Rational(9, 3600)
ok(VM == sp.Rational(1, 400) and VM / sp.Rational(1, 4) == sp.Rational(1, 100), "A4 : V(M_n) = 0,0025 et 0,0025 / 0,5² = 0,01 (VRAIE)")

# =========================================================================== EXERCICE 3
LOG.append("== Exercice 3 : espace")
P = {"A": (0, 0, 0), "B": (1, 0, 0), "C": (1, 1, 0), "D": (0, 1, 0), "E": (0, 0, 1), "F": (1, 0, 1), "G": (1, 1, 1), "H": (0, 1, 1)}
M = {k: sp.Matrix(v) for k, v in P.items()}
for a, b in ("BD", "BE", "BG", "DE", "DG", "EG"):
    ok(sp.sqrt((M[b] - M[a]).dot(M[b] - M[a])) == sp.sqrt(2), f"{a}{b} = √2")
nv = sp.Matrix([1, -1, 1])
BE, BG = M["E"] - M["B"], M["G"] - M["B"]
ok(BE == sp.Matrix([-1, 0, 1]) and BG == sp.Matrix([0, 1, 1]), "BE(−1 ; 0 ; 1) et BG(0 ; 1 ; 1)")
ok(BE.cross(BG) != sp.zeros(3, 1), "BE et BG non colinéaires")
ok(nv.dot(BE) == 0 and nv.dot(BG) == 0, "n·BE = n·BG = 0")
plan = lambda q: q[0] - q[1] + q[2] - 1  # noqa: E731
ok(all(plan(P[k]) == 0 for k in "BEG") and plan(P["D"]) != 0, "(BEG) : x − y + z − 1 = 0 (D hors du plan)")
Q = M["D"] + t * nv
ts = sp.solve(plan(Q), t)
ok(ts == [sp.Rational(2, 3)], "intersection : 3t − 2 = 0, t = 2/3")
K = Q.subs(t, sp.Rational(2, 3))
ok(K == sp.Matrix([sp.Rational(2, 3), sp.Rational(1, 3), sp.Rational(2, 3)]), "K(2/3 ; 1/3 ; 2/3)")
ok(K == (M["B"] + M["E"] + M["G"]) / 3, "K = centre de gravité de BEG")
ok(Q.subs(t, 1) == M["F"], "t = 1 donne F : Δ = (DF)")
DK = sp.sqrt((K - M["D"]).dot(K - M["D"]))
ok(sp.simplify(DK - 2 * sp.sqrt(3) / 3) == 0, "DK = 2√3/3")
aire = sp.sqrt(3) / 4 * 2
ok(sp.simplify(aire - BE.cross(BG).norm() / 2) == 0 and aire == sp.sqrt(3) / 2, "aire(BEG) = √3/2")
V = sp.Rational(1, 3) * aire * DK
ok(sp.simplify(V - sp.Rational(1, 3)) == 0, "V = 1/3 × √3/2 × 2√3/3 = 1/3")
ok(sp.simplify(sp.sqrt(3) / 2 * 2 * sp.sqrt(3) / 3 - 1) == 0, "√3/2 × 2√3/3 = 6/6 = 1")
detV = abs(sp.Matrix.hstack(M["B"] - M["D"], M["E"] - M["D"], M["G"] - M["D"]).det()) / 6
ok(detV == sp.Rational(1, 3), "contrôle par le déterminant : V = 1/3")
coins = {"ABDE": "ABDE", "CBDG": "CBDG", "FBEG": "FBEG", "HDEG": "HDEG"}
for nom in coins:
    a, b, c, d = (M[k] for k in nom)
    vol = abs(sp.Matrix.hstack(b - a, c - a, d - a).det()) / 6
    ok(vol == sp.Rational(1, 6), f"tétraèdre de coin {nom} : 1/6")
ok(1 - 4 * sp.Rational(1, 6) == sp.Rational(1, 3), "1 − 4/6 = 1/3")

# =========================================================================== EXERCICE 4
LOG.append("== Exercice 4 : fonction, suite, intégrale")
f = x * sp.exp(-x)
ok(sp.limit(f, x, -sp.oo) == -sp.oo and sp.limit(f, x, sp.oo) == 0, "limites : −∞ en −∞, 0 en +∞")
fp, fpp = sp.diff(f, x), sp.diff(f, x, 2)
ok(sp.simplify(fp - (1 - x) * sp.exp(-x)) == 0, "f'(x) = (1 − x)e^{−x}")
ok(sp.simplify(fpp - (x - 2) * sp.exp(-x)) == 0, "f''(x) = (x − 2)e^{−x}")
ok(f.subs(x, 1) == sp.exp(-1) and f"{float(sp.exp(-1)):.3f}" == "0.368", "maximum f(1) = 1/e ≈ 0,368")
ok(sp.solve(fp, x) == [1], "f' s'annule seulement en 1")
ok(f.subs(x, 0) == 0, "f(0) = 0")
alpha = sp.nsolve(f - sp.Rational(1, 4), x, 0.35)
ok(0.35 < alpha < 0.36, f"α ≈ {float(alpha):.6f} ∈ ]0,35 ; 0,36[")
ok(f"{float(f.subs(x, 0.35)):.4f}" == "0.2466" and f"{float(f.subs(x, 0.36)):.4f}" == "0.2512",
   f"f(0,35) ≈ {float(f.subs(x, 0.35)):.5f} ; f(0,36) ≈ {float(f.subs(x, 0.36)):.5f}")
beta = sp.nsolve(f - sp.Rational(1, 4), x, 2.1)
ok(beta > 1, f"seconde solution de f(x) = 1/4 sur ]1 ; +∞[ : ≈ {float(beta):.4f}")
ok(sp.solve(fpp, x) == [2] and f"{float(f.subs(x, 2)):.3f}" == "0.271", "inflexion en 2, f(2) = 2e^{−2} ≈ 0,271")
ok(fpp.subs(x, 1.9) < 0 < fpp.subs(x, 2.1), "f'' change de signe en 2")
tang = fp.subs(x, 0) * (x - 0) + f.subs(x, 0)
ok(tang == x, "T : y = x")
ok(sp.simplify((x - f) - x * (1 - sp.exp(-x))) == 0, "x − f(x) = x(1 − e^{−x})")
ok(all(float(xx - f.subs(x, xx)) >= -1e-15 for xx in [-3, -1, -0.2, 0, 0.5, 1, 2, 3, 8]), "f(x) ≤ x (contrôle numérique, y compris x > 2)")
u = [sp.Integer(1)]
for _ in range(10):
    u.append(f.subs(x, u[-1]))
ok(u[1] == sp.exp(-1), "u_1 = 1/e")
ok(sp.simplify(u[2] - sp.exp(-1 - sp.exp(-1))) == 0 and f"{float(u[2]):.3f}" == "0.255", f"u_2 = e^(−1−1/e) ≈ {float(u[2]):.5f} → 0,255")
ok(all(0 < float(u[k + 1]) <= float(u[k]) <= 1 for k in range(10)), "0 < u_{n+1} ≤ u_n ≤ 1 pour n ≤ 9")
ok(f"{float(u[7]):.3f}" == "0.106" and f"{float(u[8]):.3f}" == "0.096", f"u_7 ≈ {float(u[7]):.5f} ; u_8 ≈ {float(u[8]):.5f}")
ok(sp.solve(sp.Eq(f, x), x) == [0], "f(ℓ) = ℓ ⟺ ℓ = 0")
# fonction Python du corrigé, extraite du texte et exécutée
code = re.search(r"```python\n(from math import exp\n\ndef seuil\(e\):\n.*?)```", TXT.split("Étapes:")[1], re.S).group(1)
espace = {}
exec(code, espace)
ok(espace["seuil"](0.1) == 8, f"seuil(0.1) du corrigé renvoie {espace['seuil'](0.1)}")
ok(all(len(l) <= 40 for l in code.splitlines()), "lignes de code ≤ 40 caractères")
I = sp.integrate(f, (x, 0, 1))
ok(sp.simplify(I - (1 - 2 / sp.E)) == 0 and f"{float(I):.3f}" == "0.264", f"I = 1 − 2/e ≈ {float(I):.5f}")
ipp = (-x * sp.exp(-x)).subs(x, 1) - (-x * sp.exp(-x)).subs(x, 0) + sp.integrate(sp.exp(-x), (x, 0, 1))
ok(sp.simplify(ipp - I) == 0, "intégration par parties détaillée : [−xe^{−x}] + ∫e^{−x}")
A = sp.integrate(x - f, (x, 0, 1))
ok(sp.simplify(A - (2 / sp.E - sp.Rational(1, 2))) == 0 and f"{float(A):.2f}" == "0.24", f"aire = 2/e − 1/2 ≈ {float(A):.5f} → 0,24")
ok(f"{float(I):.2f}" == "0.26", "I ≈ 0,26 (Solution)")

# =========================================================================== BARÈME
LOG.append("== Barème")
etapes = TXT.split("Étapes:")[1].split("Solution:")[0]
blocs = re.split(r"^## Exercice (\d)", etapes, flags=re.M)
totaux = {}
for k in range(1, len(blocs), 2):
    pts = re.findall(r"::: point Barème\n\$(\d+(?:\{,\}\d+)?)\$ point", blocs[k + 1])
    totaux[int(blocs[k])] = sum(float(v.replace("{,}", ".")) for v in pts)
    nq = len(re.findall(r"^## Question", blocs[k + 1], re.M))
    ok(len(pts) == nq, f"exercice {blocs[k]} : un barème par question ({len(pts)}/{nq})")
attendu = {1: 4, 2: 4, 3: 4, 4: 6}
for e, v in attendu.items():
    ok(abs(totaux.get(e, 0) - v) < 1e-9, f"exercice {e} : total du barème {totaux.get(e)} = {v}")
for e, titre_pts in re.findall(r"^## Exercice (\d) : .*\((\d) points\)", TXT, re.M):
    ok(attendu[int(e)] == int(titre_pts), f"titre de l'exercice {e} : {titre_pts} points")
ok(sum(attendu.values()) + 2 == 20, "4 + 4 + 4 + 6 + 2 (langue) = 20")
# détails internes des barèmes (sous-totaux)
for detail, total in ((["0{,}25", "0{,}25"], "0{,}5"), (["0{,}5", "0{,}25"], "0{,}75")):
    ok(sum(float(d.replace("{,}", ".")) for d in detail) == float(total.replace("{,}", ".")), f"sous-total {total}")
ok(abs(0.5 + 0.5 + 0.25 - 1.25) < 1e-12 and abs(0.75 + 0.25 - 1) < 1e-12 and abs(0.2 * 2 + 0.1 - 0.5) < 1e-12, "sous-totaux 1,25 ; 1 ; 0,5")

# =========================================================================== COURS
LOG.append("== Cours de méthode")
ok(sp.limit(sp.exp(x) - x ** 2, x, sp.oo) == sp.oo and sp.limit(x ** 2 / sp.exp(x), x, sp.oo) == 0, "e^x − x² → +∞ ; x²/e^x → 0")
ok(sp.limit(sp.exp(x) / x ** 5, x, sp.oo) == sp.oo and sp.limit(sp.log(x) / x, x, sp.oo) == 0
   and sp.limit(x * sp.log(x), x, 0, "+") == 0, "croissances comparées citées")
h = x ** 3 - 3 * x ** 2 + 1
ok(sp.expand(sp.diff(h, x) - (3 * x ** 2 - 6 * x)) == 0 and sp.expand(sp.diff(h, x, 2) - (6 * x - 6)) == 0
   and h.subs(x, 1) == -1 and sp.diff(h, x, 2).subs(x, 0.9) < 0 < sp.diff(h, x, 2).subs(x, 1.1),
   "x³ − 3x² + 1 : f' = 3x² − 6x, f'' = 6x − 6 change de signe en 1, inflexion (1 ; −1)")
w = [5.0]
for _ in range(60):
    w.append(0.5 * w[-1] + 1)
ok(all(v >= 2 for v in w) and all(w[k + 1] <= w[k] for k in range(60)) and abs(w[-1] - 2) < 1e-9, "u_0 = 5, u_{n+1} = 0,5u_n + 1 : ≥ 2, décroissante, limite 2")
code_c = re.search(r"```python\n(def seuil\(s\):\n.*?)```", COURS, re.S).group(1)
esp = {}
exec(code_c, esp)
ok(esp["seuil"](2.5) == next(k for k, v in enumerate(w) if v <= 2.5), f"seuil(2.5) du cours = {esp['seuil'](2.5)}")
ok(sp.integrate(x * sp.exp(x), (x, 0, 1)) == 1, "∫_0^1 x e^x dx = 1")
loi10 = [comb(10, k) * 0.3 ** k * 0.7 ** (10 - k) for k in range(11)]
ok(f"{loi10[2]:.3f}" == "0.233", f"B(10 ; 0,3) : P(X = 2) ≈ {loi10[2]:.5f}")
ok(f"{sum(loi10[:3]):.3f}" == "0.383", f"P(X ≤ 2) ≈ {sum(loi10[:3]):.5f}")
ok(f"{1 - 0.7 ** 10:.3f}" == "0.972" and abs(10 * 0.3 - 3) < 1e-12, "P(X ≥ 1) = 1 − 0,7^10 ≈ 0,972 ; E = 3")
Mx = sp.Matrix([3, 1, 5]); n2 = sp.Matrix([2, -1, 2])
Q2 = Mx + t * n2
expr = sp.expand(2 * Q2[0] - Q2[1] + 2 * Q2[2] - 3)
ok(expr == 12 + 9 * t, "2(3+2t) − (1−t) + 2(5+2t) − 3 = 12 + 9t")
H = Q2.subs(t, sp.Rational(-4, 3))
ok(H == sp.Matrix([sp.Rational(1, 3), sp.Rational(7, 3), sp.Rational(7, 3)]) and 2 * H[0] - H[1] + 2 * H[2] - 3 == 0, "H(1/3 ; 7/3 ; 7/3) dans le plan")
ok((H - Mx).norm() == 4 and n2.norm() == 3, "MH = 4/3 × ‖n‖ = 4")
ok(sp.Abs(2 * 3 - 1 + 2 * 5 - 3) / 3 == 4, "contrôle par la formule de distance : 4")

# =========================================================================== FICHE
LOG.append("== Fiche")
u_, v_ = sp.Function("u")(x), sp.Function("v")(x)
a, b, nn = sp.symbols("a b n", positive=True)
ok(sp.simplify(sp.diff(u_ ** nn, x) - nn * sp.diff(u_, x) * u_ ** (nn - 1)) == 0, "(u^n)' = n u' u^{n−1}")
ok(sp.simplify(sp.diff(sp.sqrt(u_), x) - sp.diff(u_, x) / (2 * sp.sqrt(u_))) == 0, "(√u)'")
ok(sp.simplify(sp.diff(sp.exp(u_), x) - sp.diff(u_, x) * sp.exp(u_)) == 0, "(e^u)'")
ok(sp.simplify(sp.diff(sp.log(u_), x) - sp.diff(u_, x) / u_) == 0, "(ln u)'")
ok(sp.simplify(sp.diff(sp.cos(a * x + b), x) + a * sp.sin(a * x + b)) == 0, "(cos(ax+b))'")
ok(sp.simplify(sp.diff(sp.sin(a * x + b), x) - a * sp.cos(a * x + b)) == 0, "(sin(ax+b))'")
ok(sp.simplify(sp.diff(u_ / v_, x) - (sp.diff(u_, x) * v_ - u_ * sp.diff(v_, x)) / v_ ** 2) == 0, "(u/v)'")
xp = sp.symbols("xp", positive=True)
prims = [(xp ** 3, xp ** 4 / 4), (1 / xp, sp.log(xp)), (1 / xp ** 2, -1 / xp), (1 / sp.sqrt(xp), 2 * sp.sqrt(xp)),
         (sp.exp(a * xp), sp.exp(a * xp) / a), (sp.cos(a * xp + b), sp.sin(a * xp + b) / a),
         (sp.sin(a * xp + b), -sp.cos(a * xp + b) / a)]
for fx, Fx in prims:
    ok(sp.simplify(sp.diff(Fx, xp) - fx) == 0, f"primitive de {fx} : {Fx}")
U = sp.Function("U")(xp)
ok(sp.simplify(sp.diff(U ** (nn + 1) / (nn + 1), xp) - sp.diff(U, xp) * U ** nn) == 0, "primitive de u'u^n")
ok(sp.simplify(sp.diff(sp.exp(U), xp) - sp.diff(U, xp) * sp.exp(U)) == 0 and sp.simplify(sp.diff(sp.log(U), xp) - sp.diff(U, xp) / U) == 0, "primitives de u'e^u et u'/u")
aa, bb = sp.symbols("aa bb", nonzero=True)
yy = C * sp.exp(aa * x) - bb / aa
ok(sp.simplify(sp.diff(yy, x) - (aa * yy + bb)) == 0, "y = Ce^{ax} − b/a solution de y' = ay + b")
ok(sp.expand_log(sp.log(a * b), force=True) == sp.log(a) + sp.log(b) and sp.expand_log(sp.log(a ** 5), force=True) == 5 * sp.log(a)
   and sp.expand_log(sp.log(sp.sqrt(a)), force=True) == sp.log(a) / 2, "propriétés de ln")
ok(sp.limit((sp.exp(x) - 1) / x, x, 0) == 1 and sp.limit(sp.log(1 + x) / x, x, 0) == 1, "nombres dérivés en 0")
q, N = sp.symbols("q N", positive=True)
ok(sp.simplify(sp.summation(q ** sp.Symbol("k"), (sp.Symbol("k"), 0, 6)) - (1 - q ** 7) / (1 - q)) == 0, "somme géométrique (n = 6)")
ok(all(comb(m, k) + comb(m, k + 1) == comb(m + 1, k + 1) for m in range(1, 15) for k in range(m)), "relation de Pascal")
ok(sp.factorial(10) / sp.factorial(7) == 720 and 2 ** 5 == sum(comb(5, k) for k in range(6)), "arrangements, 2^n parties")
ok(log(0.9) < 0, "ln(0,9) < 0 (réflexe de la fiche)")

# =========================================================================== FIGURES (valeurs tracées)
LOG.append("== Figures")
sys.path.insert(0, str(ICI / "figures"))
import figures as FIG  # noqa: E402
ok(abs(FIG.P_L - 0.071) < 1e-12 and abs(sum(FIG.V50[:3]) - p2) < 1e-15, "figures : P(L) et P(X ≤ 2) identiques au texte")
ok(abs(FIG.ALPHA - float(alpha)) < 1e-6, "figures : α tracé = α calculé")
ok(all(abs(FIG.U[k] - float(u[k])) < 1e-12 for k in range(4)), "figures : u_0 … u_3 tracés = suite")
ok("0{,}301" in FIG.FIGURES["ex1_binomiale"] and "0{,}383" in FIG.FIGURES["cours_binomiale"], "figures : étiquettes 0,301 et 0,383")
for lab in ("0{,}035", "0{,}665", "0{,}036", "0{,}264"):
    ok(lab in FIG.FIGURES["ex1_arbre"], f"figures : arbre complété contient {lab}")

out = "\n".join(LOG) + f"\n\n{NB[0]} contrôles, {NB[1]} erreur(s)\n"
(ICI / "verif_log.txt").write_text(out, encoding="utf-8")
print(out)
sys.exit(1 if NB[1] else 0)
