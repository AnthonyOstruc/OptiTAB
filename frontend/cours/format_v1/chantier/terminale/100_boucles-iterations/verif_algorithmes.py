# -*- coding: utf-8 -*-
"""Vérification de la notion « Algorithmes du programme de Terminale » (ex « Boucles / Itérations »).

    python verif_algorithmes.py            # contrôle complet (code de sortie 0 si tout est juste)
    python verif_algorithmes.py --sorties  # affiche la sortie réelle de chaque programme
    python verif_algorithmes.py --remplir  # réécrit les blocs console avec la sortie réelle

1. Programmes (moteur_verif.py) : chaque programme Python du cours, de la fiche
   et de chaque exercice est EXÉCUTÉ ; chaque affichage imprimé est comparé à
   l'affichage réel ; les simulations doivent appeler seed(…) ; largeur des
   lignes de code limitée pour le téléphone ; boucle sans fin détectée.
2. Boucles annoncées comme infinies : rejouées au-delà de 10^6 tours.
3. Contrôles mathématiques (sympy, valeurs exactes) de toutes les valeurs
   écrites dans le texte et sur les figures.
"""
import math
import sys
from fractions import Fraction
from math import comb
from pathlib import Path

import sympy as sp

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import moteur_verif as mv  # noqa: E402

FICHIERS = ["cours_104.txt", "fiche_36.txt", "exercices.txt"]
erreurs = []
n_controles = 0


def chk(cond, msg):
    global n_controles
    n_controles += 1
    if not cond:
        erreurs.append("maths : " + msg)


# ------------------------------------------------------------------ 1. programmes
tot = {"programmes": 0, "affichages": 0, "trous": 0}
for nom in FICHIERS:
    p = ICI / nom
    if not p.exists():
        continue
    e, st = mv.analyser(p, remplir="--remplir" in sys.argv, montrer="--sorties" in sys.argv)
    erreurs += e
    for k in tot:
        tot[k] += st[k]
    print(f"{nom} : {st['programmes']} programme(s) exécuté(s), {st['affichages']} affichage(s) comparé(s), "
          f"{st['trous']} programme(s) à compléter")

# ------------------------------------------------------------------ 2. boucles infinies annoncées


def tours(u0, a, b, A, maxi=10 ** 6):
    """Nombre de tours de « while u <= A: u = a*u + b » en flottants (None si > maxi)."""
    u, n = u0, 0
    while u <= A:
        u = a * u + b
        n += 1
        if n > maxi:
            return None
    return n


def tours_bas(u0, a, b, A, maxi=10 ** 6):
    """Nombre de tours de « while u >= A: u = a*u + b » (None si > maxi)."""
    u, n = u0, 0
    while u >= A:
        u = a * u + b
        n += 1
        if n > maxi:
            return None
    return n


# ------------------------------------------------------------------ 3. maths
x, t, h = sp.symbols("x t h", real=True)
R = sp.Rational
COURS = (ICI / "cours_104.txt").read_text(encoding="utf-8")

# --- cours II : u0 = 1, u_{n+1} = 0,8 u_n + 2
u = [sp.Integer(1)]
for _ in range(20):
    u.append(R(4, 5) * u[-1] + 2)
chk(u[1:4] == [R(14, 5), R(106, 25), R(674, 125)], "cours : u1 = 2,8 ; u2 = 4,24 ; u3 = 5,392")
chk(sum(u[:4]) == R(1679, 125) and float(sum(u[:4])) == 13.432, "cours : somme = 13,432")
chk(all(u[k] == 10 - 9 * R(4, 5) ** k for k in range(21)), "cours : u_n = 10 - 9 × 0,8^n")
chk(min(k for k in range(21) if u[k] > 9) == 10, "cours : seuil 9 → 10")
chk(round(math.log(9) / -math.log(0.8), 2) == 9.85, "cours : ln 9 / -ln 0,8 ≈ 9,85")
chk(all(u[k] < 10 for k in range(21)), "cours : u_n < 10")
chk(tours(1, 0.8, 2, 10) is None, "cours : seuil(10) ne s'arrête pas (flottants)")
# --- dichotomie x^3 + x - 1
f = x ** 3 + x - 1
alpha = sp.nsolve(f, x, 0.7)
chk(sp.diff(f, x) == 3 * x ** 2 + 1 and f.subs(x, 0) == -1 and f.subs(x, 1) == 1, "cours : f(0), f(1), f'")
chk([sp.sign(f.subs(x, m)) for m in (R(1, 2), R(3, 4), R(5, 8), R(11, 16))] == [-1, 1, -1, 1],
    "cours : signes de f(m) dans le tableau")
chk(R(1, 2 ** 6) > R(1, 100) >= R(1, 2 ** 7), "cours : 7 tours pour 0,01")
chk(0.6796875 < alpha < 0.6875 and abs(float(alpha) - 0.682327804) < 1e-9, "cours : α ≈ 0,682327804")
# --- Newton
xs = [sp.Integer(1)]
for _ in range(4):
    xs.append(xs[-1] - f.subs(x, xs[-1]) / sp.diff(f, x).subs(x, xs[-1]))
chk(xs[1] == R(3, 4) and xs[2] == R(59, 86), "cours : x1 = 0,75 ; x2 = 59/86")
chk(abs(float(xs[4]) - float(alpha)) < 1e-9, "cours : x4 ≈ α à 1e-9")
# --- rectangles 1/x
for n, s_, S_ in ((4, 0.6345, 0.7595), (10, 0.6688, 0.7188), (100, 0.6907, 0.6957)):
    hh = R(1, n)
    S = sum(hh / (1 + k * hh) for k in range(n))
    s = sum(hh / (1 + k * hh) for k in range(1, n + 1))
    chk(round(float(s), 4) == s_ and round(float(S), 4) == S_, f"cours : rectangles n = {n}")
    chk(S - s == R(1, 2 * n) and s < sp.log(2) < S, f"cours : S - s = 1/(2n), encadrement de ln 2 (n = {n})")
chk(sp.integrate(1 / x, (x, 1, 2)) == sp.log(2) and round(math.log(2), 4) == 0.6931, "cours : ∫ 1/x = ln 2")
# --- seuils exp / ln
chk(round(math.log(2) / math.log(1.03), 2) == 23.45 and min(n for n in range(100) if R(103, 100) ** n > 2) == 24,
    "cours : capital doublé en 24 ans")
chk(round(float(1000 * R(103, 100) ** 24), 2) == 2032.79, "cours : 1000 × 1,03^24 ≈ 2032,79")
tc = sp.log(100) / R(3, 10)
chk(round(float(tc), 2) == 15.35 and math.ceil(float(tc)) == 16, "cours : t > ln 100 / 0,3 ≈ 15,35 → 16")
chk(math.ceil(float(tc) * 100) / 100 == 15.36, "cours : pas 0,01 → 15,36")
# --- loi binomiale B(10 ; 0,3)
P = [comb(10, k) * R(3, 10) ** k * R(7, 10) ** (10 - k) for k in range(11)]
chk(sum(P) == 1, "cours : somme des probabilités binomiales")
chk([round(float(p), 3) for p in P[:6]] == [0.028, 0.121, 0.233, 0.267, 0.2, 0.103], "cours : P(X = k) arrondis")
chk(round(float(sum(P[:5])), 4) == 0.8497 and round(float(sum(P[:6])), 4) == 0.9527, "cours : P(X ≤ 4), P(X ≤ 5)")
E_cours = [int(l.split()[1]) for l in mv.bloc_console_apres(COURS, "E[x] = E[x] + 1").splitlines()]
chk(sum(E_cours) == 1000 and len(E_cours) == 11, "cours : effectifs de la simulation (1000 valeurs)")
# --- Pascal, parties
lig = [[comb(n, k) for k in range(n + 1)] for n in range(6)]
chk(lig[5] == [1, 5, 10, 10, 5, 1] and comb(5, 2) == 10, "cours : ligne 5 du triangle")
chk(all(comb(n + 1, k) == comb(n, k - 1) + comb(n, k) for n in range(10) for k in range(1, n + 1)),
    "cours : relation de Pascal")
chk(comb(4, 2) == 6, "cours : 6 parties à 2 éléments de {a, b, c, d}")

chk(mv.bloc_console_apres(COURS, "R.append(bernoulli(0.3))").splitlines()[0].count("1") == 3, "cours : 3 succès dans R")

# ================================================================== exercices
EX = (ICI / "exercices.txt").read_text(encoding="utf-8")
n_ = sp.symbols("n", integer=True, nonnegative=True)
# --- 832 : u0 = 5, u_{n+1} = 0,5 u_n + 1
u = [sp.Integer(5)]
for _ in range(10):
    u.append(R(1, 2) * u[-1] + 1)
chk(u[1:5] == [R(7, 2), R(11, 4), R(19, 8), R(35, 16)], "832 : u1..u4 (3,5 ; 2,75 ; 2,375 ; 2,1875)")
chk([sum(u[:k + 1]) for k in range(4)] == [5, R(17, 2), R(45, 4), R(109, 8)], "832 : sommes partielles 5 ; 8,5 ; 11,25 ; 13,625")
chk(all(u[k] == 2 + 3 * R(1, 2) ** k for k in range(11)), "832 : u_n = 2 + 3 × 0,5^n")
# --- 831 : u_n = 20 × 0,7^n
w = lambda k: 20 * R(7, 10) ** k  # noqa: E731
chk(round(float(w(8)), 3) == 1.153 and round(float(w(9)), 3) == 0.807, "831 : u8 ≈ 1,153 ; u9 ≈ 0,807")
chk(min(k for k in range(50) if w(k) < 1) == 9 and min(k for k in range(50) if w(k) < R(1, 10)) == 15, "831 : seuils 1 → 9, 0,1 → 15")
chk(round(math.log(0.05) / math.log(0.7), 2) == 8.40 and round(math.log(0.005) / math.log(0.7), 2) == 14.85, "831 : 8,40 et 14,85")
# --- 835 : u0 = 2, u_{n+1} = 0,7 u_n + 2
u = [sp.Integer(2)]
for _ in range(30):
    u.append(R(7, 10) * u[-1] + 2)
chk(u[1] == R(17, 5) and u[2] == R(219, 50), "835 : u1 = 3,4 ; u2 = 4,38")
chk(all(u[k] == R(20, 3) - R(14, 3) * R(7, 10) ** k for k in range(31)), "835 : forme explicite")
chk(all(0 < u[k] < u[k + 1] < R(20, 3) for k in range(30)), "835 : 0 < u_n < u_{n+1} < 20/3")
chk(R(7, 10) * R(20, 3) + 2 == R(20, 3), "835 : 20/3 point fixe")
chk(min(k for k in range(31) if u[k] > 6) == 6 and round(float(u[5]), 2) == 5.88 and round(float(u[6]), 2) == 6.12, "835 : seuil 6 → 6")
chk(round(math.log(7) / -math.log(0.7), 2) == 5.46, "835 : ln 7 / -ln 0,7 ≈ 5,46")
chk(tours(2, 0.7, 2, 7) is None, "835 : seuil(7) ne s'arrête pas (flottants)")
# --- 833 : f(x) = e^x + x - 3
g = sp.exp(x) + x - 3
a833 = sp.nsolve(g, x, 0.8)
chk(g.subs(x, 0) == -2 and sp.simplify(g.subs(x, 1) - (sp.E - 2)) == 0 and round(float(sp.E - 2), 2) == 0.72, "833 : f(0), f(1)")
chk([round(float(g.subs(x, m)), 2) for m in (0.5, 0.75, 0.875)] == [-0.85, -0.13, 0.27], "833 : f(0,5), f(0,75), f(0,875)")
chk(0.7919921875 < a833 < 0.79296875 and 0.75 < a833 < 0.875, "833 : encadrements de α")
chk(2 ** 9 < 1000 <= 2 ** 10 and 2 ** 19 < 10 ** 6 <= 2 ** 20 and round(6 * math.log(10) / math.log(2), 1) == 19.9, "833 : 10 et 20 tours")
# --- 834 : B(10 ; 0,7)
P7 = [comb(10, k) * R(7, 10) ** k * R(3, 10) ** (10 - k) for k in range(11)]
chk(comb(10, 8) == 45 and [round(float(P7[k]), 4) for k in (8, 9, 10)] == [0.2335, 0.1211, 0.0282], "834 : P(X = 8), 9, 10")
chk(round(float(sum(P7[8:])), 3) == 0.383 and sum(k * P7[k] for k in range(11)) == 7, "834 : P(X ≥ 8) ≈ 0,383 ; E(X) = 7")
# --- nouveau-1 : Newton pour x² - 2
a = sp.Symbol("a", positive=True)
tg = 2 * a * (x - a) + a ** 2 - 2
chk(sp.simplify(sp.solve(tg, x)[0] - (a + 2 / a) / 2) == 0, "n1 : abscisse = (a + 2/a)/2")
xs = [sp.Integer(2)]
for _ in range(5):
    xs.append((xs[-1] + 2 / xs[-1]) / 2)
chk(xs[1] == R(3, 2) and xs[2] == R(17, 12), "n1 : x1 = 3/2, x2 = 17/12")
chk(abs(xs[5] - sp.sqrt(2)) < sp.Rational(1, 10 ** 15) and abs(xs[4] - sp.sqrt(2)) > sp.Rational(1, 10 ** 13),
    "n1 : 15 décimales au 5e tour, pas au 4e")
chk(str(sp.N(sp.sqrt(2), 16))[:17] == "1.414213562373095", "n1 : √2 ≈ 1,414213562373095")
chk(2 ** 29 < 10 ** 9 <= 2 ** 30 and round(9 * math.log(10) / math.log(2), 1) == 29.9, "n1 : 30 tours de dichotomie")
# --- nouveau-2 : rectangles pour x² sur [0 ; 1]
for n, s_, S_ in ((4, R(7, 32), R(15, 32)), (10, R(57, 200), R(77, 200)), (100, R(6567, 20000), R(6767, 20000))):
    s = sum(R(1, n) * (R(k, n)) ** 2 for k in range(n))
    S = sum(R(1, n) * (R(k, n)) ** 2 for k in range(1, n + 1))
    chk(s == s_ and S == S_ and S - s == R(1, n) and s < R(1, 3) < S, f"n2 : rectangles n = {n}")
chk(float(R(7, 32)) == 0.21875 and float(R(15, 32)) == 0.46875, "n2 : 0,21875 et 0,46875")
chk(sp.integrate(x ** 2, (x, 0, 1)) == R(1, 3), "n2 : I = 1/3")
# --- nouveau-3 : T(t) = 20 + 60 e^{-0,1 t}
T = 20 + 60 * sp.exp(-t / 10)
chk(sp.diff(T, t) == -6 * sp.exp(-t / 10) and sp.limit(T, t, sp.oo) == 20, "n3 : T' et limite")
chk(round(float(T.subs(t, 17)), 2) == 30.96 and round(float(T.subs(t, 18)), 2) == 29.92, "n3 : T(17), T(18)")
chk(len(sp.solve(sp.Eq(T, 30), t)) == 1 and sp.simplify(sp.solve(sp.Eq(T, 30), t)[0] - 10 * sp.log(6)) == 0 and round(float(10 * sp.log(6)), 2) == 17.92, "n3 : t = 10 ln 6")
chk(round(math.exp(5), 2) == 148.41 and math.log(148) <= 5 < math.log(149), "n3 : e^5 ≈ 148,41 → 149")
# --- nouveau-4 : surréservation
pb = lambda n, k: comb(n, k) * R(92, 100) ** k * R(8, 100) ** (n - k)  # noqa: E731
psur = lambda n: sum(pb(n, k) for k in range(201, n + 1))  # noqa: E731
chk(R(92, 100) * 210 == R(966, 5), "n4 : E(X_210) = 193,2")
chk(round(float(psur(210)), 4) == 0.0244 and round(float(psur(211)), 4) == 0.0453 and round(float(psur(212)), 4) == 0.0774,
    "n4 : P(X_n > 200) pour 210, 211, 212")
chk(max(n for n in range(200, 230) if psur(n) <= R(5, 100)) == 211 and all(psur(n) <= R(5, 100) for n in range(200, 212)),
    "n4 : 211 billets au plus")
cum = lambda k: 1 - sum(pb(210, j) for j in range(k + 1))  # noqa: E731
chk(cum(198) > R(5, 100) >= cum(199) and round(float(cum(199)), 4) == 0.0471, "n4 : k = 199")
# --- nouveau-5 : échantillons du dé
V = sum(R(k * k, 6) for k in range(1, 7)) - R(7, 2) ** 2
chk(V == R(35, 12) and round(math.sqrt(35 / 12), 4) == 1.7078 and round(math.sqrt(35 / 12) / 10, 4) == 0.1708, "n5 : σ et σ/√n")
d = 2 * math.sqrt(35 / 12) / 10
chk(round(d, 3) == 0.342 and round(3.5 - d, 3) == 3.158 and round(3.5 + d, 3) == 3.842, "n5 : intervalle [3,158 ; 3,842]")
sg = sp.Symbol("sigma", positive=True)
chk(sp.simplify(sg ** 2 / (100 * (2 * sg / 10) ** 2)) == R(1, 4), "n5 : majorant de Bienaymé-Tchebychev = 1/4")
# --- nouveau-6 : Pascal
chk([comb(6, k) for k in range(7)] == [1, 6, 15, 20, 15, 6, 1] and [comb(7, k) for k in range(8)] == [1, 7, 21, 35, 35, 21, 7, 1],
    "n6 : lignes 6 et 7")
chk(all(sum(comb(n, k) for k in range(n + 1)) == 2 ** n for n in range(12)) and comb(5, 3) == 10, "n6 : somme 2^n, C(5,3)")
# --- nouveau-7 : f(x) = 4x / (x + 1)
fx = 4 * x / (x + 1)
chk(sp.simplify(sp.diff(fx, x) - 4 / (x + 1) ** 2) == 0, "n7 : f'")
chk(set(sp.solve(sp.Eq(fx, x), x)) == {0, 3} and fx.subs(x, 3) == 3, "n7 : points fixes 0 et 3")
u = [R(1, 2)]
for _ in range(20):
    u.append(fx.subs(x, u[-1]))
chk(u[1] == R(4, 3) and all(0 < u[k] < u[k + 1] < 3 for k in range(20)), "n7 : u1 = 4/3, 0 < u_n < u_{n+1} < 3")
chk(all(sp.simplify(u[k] - 3 / (1 + 5 * R(1, 4) ** k)) == 0 for k in range(21)), "n7 : u_n = 3/(1 + 5 × 4^-n)")
chk(all(3 - u[k] == R(15, 4 ** k + 5) for k in range(21)), "n7 : 3 - u_n = 15/(4^n + 5)")
chk(min(k for k in range(21) if 3 - u[k] < R(1, 10 ** 4)) == 9 and round(math.log(149995) / math.log(4), 2) == 8.60, "n7 : rang 9")

# ------------------------------------------------------------------ bilan
print(f"{tot['programmes']} programme(s) exécuté(s), {tot['affichages']} affichage(s) comparé(s), "
      f"{tot['trous']} programme(s) à compléter non exécuté(s)")
print(f"{n_controles} contrôle(s) mathématique(s)")
for e in erreurs:
    print("  ✗", e)
print("OK : tout est vérifié" if not erreurs else f"{len(erreurs)} erreur(s)")
raise SystemExit(1 if erreurs else 0)
