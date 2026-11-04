# -*- coding: utf-8 -*-
"""Vérification de la notion « Algorithmes du programme de Première » (ex « Boucles / Itérations »).

    python verif_algorithmes.py            # contrôle complet
    python verif_algorithmes.py --sorties  # affiche la sortie réelle de chaque programme

1. Programmes : chaque document (cours, fiche, chaque exercice) est exécuté dans
   son propre espace de noms, bloc ```python après bloc, dans l'ordre du texte
   (Énoncé, puis Étapes, puis Solution). Le générateur aléatoire est initialisé
   avec la graine GRAINE au début de chaque document : les affichages des
   simulations sont ceux d'une exécution réelle, reproductible.
   Chaque bloc ```console doit être EXACTEMENT la sortie du dernier programme
   exécuté qui le précède. Un bloc contenant « … » est un programme à compléter
   (énoncé) : il n'est pas exécuté.
2. Boucles infinies annoncées (« ne se termine jamais ») : rejouées avec un
   compteur de tours, on vérifie qu'elles dépassent 10^6 tours.
3. Contrôles mathématiques (sympy) de toutes les valeurs écrites dans le texte.
"""
import contextlib
import io
import math
import random
import re
import sys
from pathlib import Path

import sympy as sp

ICI = Path(__file__).resolve().parent
GRAINE = 2026
CODE_RE = re.compile(r"^([ \t]*)```(python|console)[ \t]*\n(.*?)^[ \t]*```[ \t]*$", re.M | re.S)
SORTIES = "--sorties" in sys.argv
erreurs = []
n_controles = 0


def chk(cond, msg):
    global n_controles
    n_controles += 1
    if not cond:
        erreurs.append("maths : " + msg)


class TropLong(Exception):
    pass


def executer(code, ns, limite=5_000_000):
    """Exécute code dans ns ; arrêt si plus de `limite` lignes exécutées (boucle infinie)."""
    compteur = [0]

    def trace(frame, event, arg):
        if event == "line":
            compteur[0] += 1
            if compteur[0] > limite:
                raise TropLong
        return trace

    tampon = io.StringIO()
    sys.settrace(trace)
    try:
        with contextlib.redirect_stdout(tampon):
            exec(compile(code, "<bloc>", "exec"), ns)
    finally:
        sys.settrace(None)
    return tampon.getvalue()


def normal(t):
    return "\n".join(l.rstrip() for l in t.strip("\n").splitlines())


def documents():
    yield "cours", (ICI / "cours_151.txt").read_text(encoding="utf-8")
    yield "fiche", (ICI / "fiche_61.txt").read_text(encoding="utf-8")
    for bloc in re.split(r"^===[ \t]*$", (ICI / "exercices.txt").read_text(encoding="utf-8"), flags=re.M):
        if bloc.strip():
            yield "exercice " + re.search(r"^Id:\s*(\S+)", bloc, re.M).group(1), bloc


def blocs_code(texte):
    out = []
    for m in CODE_RE.finditer(texte):
        indent = len(m.group(1))
        corps = "\n".join(l[indent:] if l[:indent].strip() == "" else l for l in m.group(3).splitlines())
        out.append((m.group(2), corps, texte[:m.start()].count("\n") + 1))
    return out


# ------------------------------------------------------------------ 1. programmes
n_prog = n_aff = n_trous = 0
SORTIES_DOCS = {}
for nom, texte in documents():
    ns = {"__name__": "__main__"}
    random.seed(GRAINE)
    derniere = None          # sortie du dernier programme exécuté
    SORTIES_DOCS[nom] = []
    for genre, corps, ligne in blocs_code(texte):
        if genre == "python":
            if "…" in corps:
                n_trous += 1
                derniere = None
                continue
            n_prog += 1
            try:
                derniere = executer(corps, ns)
            except TropLong:
                erreurs.append(f"{nom} l.{ligne} : le programme ne s'arrête pas")
                derniere = None
                continue
            except Exception as e:  # noqa: BLE001
                erreurs.append(f"{nom} l.{ligne} : le programme échoue ({type(e).__name__} : {e})")
                derniere = None
                continue
            SORTIES_DOCS[nom].append(derniere)
            if SORTIES:
                print(f"--- {nom} l.{ligne}\n{derniere}", end="" if derniere.endswith("\n") else "\n")
        else:
            n_aff += 1
            if derniere is None:
                erreurs.append(f"{nom} l.{ligne} : affichage sans programme exécuté juste avant")
            elif normal(derniere) != normal(corps):
                erreurs.append(f"{nom} l.{ligne} : affichage différent de l'exécution\n"
                               f"      écrit  : {normal(corps)!r}\n      obtenu : {normal(derniere)!r}")

# ------------------------------------------------------------------ 2. boucles infinies annoncées


def tours_seuil(u0, a, b, A, maxi=10 ** 6):
    """Nombre de tours de « while u <= A: u = a*u + b » (None si > maxi)."""
    u, n = u0, 0
    while u <= A:
        u = a * u + b
        n += 1
        if n > maxi:
            return None
    return n


chk(tours_seuil(0, 0.5, 2, 5) is None, "cours : seuil(5) pour u_{n+1} = 0,5 u_n + 2 doit boucler indéfiniment")

# ------------------------------------------------------------------ 3. maths
n = sp.symbols("n", integer=True, nonnegative=True)
x, h = sp.symbols("x h", real=True)
R = sp.Rational

# --- cours II.1 : u0 = 0, u_{n+1} = 0,5 u_n + 2
u = [sp.Integer(0)]
for _ in range(10):
    u.append(R(1, 2) * u[-1] + 2)
chk(u[:6] == [0, 2, 3, R(7, 2), R(15, 4), R(31, 8)], "termes 0 ; 2 ; 3 ; 3,5 ; 3,75 ; 3,875")
chk(all(u[k] == 4 - 4 * R(1, 2) ** k for k in range(11)), "u_n = 4 - 4 × 0,5^n")
chk(all(u[k] < 4 for k in range(11)), "u_n < 4")
chk(min(k for k in range(11) if u[k] > R(39, 10)) == 6 and u[5] == R(31, 8) and u[6] == R(63, 16), "seuil 3,9 : rang 6")
# --- somme géométrique, factorielle
chk(sum(2 ** k for k in range(11)) == 2047 == 2 ** 11 - 1, "1 + 2 + … + 2^10 = 2047")
chk(sp.factorial(10) == 3628800, "10! = 3628800")
# --- seuil 2 × 1,5^n > 50
v = lambda k: 2 * R(3, 2) ** k  # noqa: E731
chk(min(k for k in range(30) if v(k) > 50) == 8, "seuil 50 : rang 8")
chk(round(float(v(7)), 2) == 34.17 and round(float(v(8)), 2) == 51.26, "u_7 ≈ 34,17 ; u_8 ≈ 51,26")
# --- tableau de valeurs et balayage
f = x ** 2 - 4 * x + 1
chk([f.subs(x, k) for k in range(-1, 6)] == [6, 1, -2, -3, -2, 1, 6], "tableau de valeurs de x² - 4x + 1")
chk(sp.expand((x - 2) ** 2 - 3 - f) == 0, "forme canonique (x - 2)² - 3")
chk(sp.discriminant(f, x) == 12, "Δ = 12")
r1 = 2 - sp.sqrt(3)
chk(set(sp.solve(f, x)) == {2 - sp.sqrt(3), 2 + sp.sqrt(3)}, "racines 2 ± √3")
chk(0.267 < float(r1) < 0.268 and 0.26 < float(r1) < 0.27 and 0.2 < float(r1) < 0.3 and round(float(r1), 4) == 0.2679,
    "2 - √3 ≈ 0,2679 dans les encadrements")
chk(sp.diff(f, x).subs(x, 1) < 0 and sp.solve(sp.diff(f, x), x) == [2], "f décroissante sur [0 ; 2]")
# --- sécantes
chk(sp.simplify(((x + h) ** 2 - x ** 2) / h - (2 * x + h)) == 0, "((x+h)² - x²)/h = 2x + h")
# --- Euler
chk([round(1.25 ** k, 4) for k in range(1, 9)] == [1.25, 1.5625, 1.9531, 2.4414, 3.0518, 3.8147, 4.7684, 5.9605],
    "Euler h = 0,25 : y_k = 1,25^k")
chk(round(math.exp(2), 2) == 7.39 and 1.25 ** 8 < math.exp(2), "e² ≈ 7,39 > 5,96")
chk(all((1 + 1 / k) ** k < math.e for k in (10, 100, 1000, 10 ** 6)), "(1 + 1/n)^n < e")
chk(round(math.e, 5) == 2.71828, "e ≈ 2,71828")
# --- Archimède
c = sp.Symbol("c", positive=True)
I_C = 1 - sp.sqrt(4 - c ** 2) / 2
chk(sp.simplify(c ** 2 / 4 + I_C ** 2 - (2 - sp.sqrt(4 - c ** 2))) == 0, "AC² = 2 - √(4 - c²)")
chk(sp.simplify(sp.sqrt(2 - sp.sqrt(4 - 1)) - 2 * sp.sin(sp.pi / 12)) == 0, "c_12 = 2 sin(π/12)")
cn, nn, demi = 1.0, 6, []
for _ in range(4):
    cn = math.sqrt(2 - math.sqrt(4 - cn ** 2))
    nn *= 2
    demi.append(nn * cn / 2)
chk(all(abs(demi[k] - (6 * 2 ** (k + 1)) * math.sin(math.pi / (6 * 2 ** (k + 1)))) < 1e-12 for k in range(4)),
    "p_n = n sin(π/n)")
chk(3.1410 < demi[3] < math.pi and float(sp.Rational(223, 71)) < math.pi < 22 / 7, "3,1410 < π ; 223/71 < π < 22/7")
# --- probabilités du cours
chk(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 7) == 6, "6 issues de somme 7")
chk(4 * R(1, 6) + 1 * R(2, 6) - 1 * R(3, 6) == R(1, 2), "E(X) = 0,5 (jeu de dé)")
chk(R(3, 5) * R(2, 4) + R(2, 5) * R(1, 4) == R(2, 5), "deux tirages : P(même couleur) = 0,4")

# ================================================================== exercices
# --- 1058 : u0 = 5, u_{n+1} = 2u_n - 3
u = [sp.Integer(5)]
for _ in range(8):
    u.append(2 * u[-1] - 3)
chk(u[:6] == [5, 7, 11, 19, 35, 67], "1058 : termes 5, 7, 11, 19, 35, 67")
chk(all(u[k] == 2 ** (k + 1) + 3 for k in range(9)), "1058 : u_n = 2^(n+1) + 3")
U = sp.Symbol("U")
chk(sp.expand((2 * U - 3) - 3 - 2 * (U - 3)) == 0, "1058 : v_{n+1} = 2 v_n")
# --- 1059
chk(sum(2 * k + 1 for k in range(50)) == 2500 == 50 * (1 + 99) // 2 and 2 * 49 + 1 == 99, "1059 : somme des impairs = 2500")
chk(sp.factorial(12) == 479001600 and sp.factorial(13) == 6227020800, "1059 : 12! et 13!")
chk(min(k for k in range(1, 30) if sp.factorial(k) > 10 ** 9) == 13, "1059 : plus petit n tel que n! > 10^9")
F = [0, 1]
while len(F) < 11:
    F.append(F[-1] + F[-2])
chk(F == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55], "1059 : Fibonacci F0..F10")
# --- 1061 : u0 = 1, u_{n+1} = 0,8 u_n + 3
u = [sp.Integer(1)]
for _ in range(30):
    u.append(R(4, 5) * u[-1] + 3)
chk(u[1] == R(19, 5) and u[2] == R(151, 25), "1061 : u1 = 3,8 ; u2 = 6,04")
chk(all(u[k] == 15 - 14 * R(4, 5) ** k for k in range(31)), "1061 : u_n = 15 - 14 × 0,8^n")
chk(sp.expand(R(4, 5) * U + 3 - 15 - R(4, 5) * (U - 15)) == 0, "1061 : v_{n+1} = 0,8 v_n")
chk(round(float(u[11]), 2) == 13.80 and round(float(u[12]), 2) == 14.04, "1061 : u11 ≈ 13,80 ; u12 ≈ 14,04")
chk(min(k for k in range(31) if u[k] > 14) == 12, "1061 : seuil 14 → 12")
chk(tours_seuil(1, 0.8, 3, 16) is None and tours_seuil(1, 0.8, 3, 15) is None, "1061 : seuil 16 (et 15) : boucle infinie")
chk(tours_seuil(1, 0.8, 3, 14.9) is not None, "1061 : seuil 14,9 atteint")
# --- 1060 : u0 = 20000, u_{n+1} = 1,03 u_n + 400
u = [sp.Integer(20000)]
for _ in range(20):
    u.append(R(103, 100) * u[-1] + 400)
chk(u[1] == 21000 and u[2] == 22030, "1060 : u1 = 21000 ; u2 = 22030")
chk(round(float(u[8]), 2) == 28892.34 and round(float(u[9]), 2) == 30159.11, "1060 : u8 ≈ 28892,34 ; u9 ≈ 30159,11")
chk(min(k for k in range(21) if u[k] > 30000) == 9 and min(k for k in range(21) if u[k] > 40000) == 16,
    "1060 : seuils 30000 → 9 (2034) et 40000 → 16 (2041)")
chk(all(u[k + 1] > u[k] for k in range(20)), "1060 : suite croissante")
# --- 1062 : dé puis urne
pS, pR_S, pR_nS = R(1, 6), R(3, 4), R(1, 4)
pR = pS * pR_S + (1 - pS) * pR_nS
chk(pR == R(1, 3) and pS * pR_S == R(1, 8) and (1 - pS) * pR_nS == R(5, 24), "1062 : P(R) = 1/3, P(S ∩ R) = 1/8")
chk(pS * pR_S / pR == R(3, 8), "1062 : P_R(S) = 3/8")
chk(pS * (1 - pR_S) == R(1, 24) and (1 - pS) * (1 - pR_nS) == R(5, 8), "1062 (figure) : P(S ∩ V) = 1/24, P(S̄ ∩ V) = 5/8")
chk([R(3, 5) * R(2, 4), R(3, 5) * R(2, 4), R(2, 5) * R(3, 4), R(2, 5) * R(1, 4)] == [R(6, 20)] * 3 + [R(2, 20)],
    "cours (arbre de l'urne) : 6/20, 6/20, 6/20, 2/20")
# --- nouveau-1 : f(x) = -x² + 6x - 4
g = -x ** 2 + 6 * x - 4
chk([g.subs(x, k) for k in range(7)] == [-4, 1, 4, 5, 4, 1, -4], "nouveau-1 : tableau de valeurs")
chk(sp.discriminant(g, x) == 20 and set(sp.solve(g, x)) == {3 - sp.sqrt(5), 3 + sp.sqrt(5)}, "nouveau-1 : Δ = 20, racines 3 ± √5")
chk(5.23 < float(3 + sp.sqrt(5)) < 5.24 and 0.76 < float(3 - sp.sqrt(5)) < 0.77, "nouveau-1 : encadrements")
chk(round(float(3 - sp.sqrt(5)), 4) == 0.7639 and round(float(3 + sp.sqrt(5)), 4) == 5.2361, "nouveau-1 : arrondis")
chk(sp.solve(sp.diff(g, x), x) == [3] and g.subs(x, 3) == 5 and g.subs(x, R(1, 100)) < 0, "nouveau-1 : sommet (3 ; 5), f(0,01) < 0")
# --- nouveau-2 : f(x) = x³
chk(sp.expand(((1 + h) ** 3 - 1) / h) == 3 + 3 * h + h ** 2, "nouveau-2 : taux = 3 + 3h + h²")
chk([3 + 3 * hh + hh ** 2 for hh in (R(1, 10), R(1, 100), R(1, 1000))] == [R(331, 100), R(30301, 10000), R(3003001, 1000000)],
    "nouveau-2 : 3,31 ; 3,0301 ; 3,003001")
tx = [sp.expand(((xx + R(1, 100)) ** 3 - xx ** 3) * 100) for xx in (0, R(1, 2), 1, R(3, 2))]
chk([round(float(t), 4) for t in tx] == [0.0001, 0.7651, 3.0301, 6.7951], "nouveau-2 : liste pour h = 0,01")
chk(all(abs(float(t) - 3 * float(xx) ** 2) < 0.05 for t, xx in zip(tx, (0, 0.5, 1, 1.5))), "nouveau-2 : écart < 0,05")
# --- nouveau-3 : Euler h = 0,5
chk([R(3, 2) ** k for k in range(1, 5)] == [R(3, 2), R(9, 4), R(27, 8), R(81, 16)] and float(R(81, 16)) == 5.0625,
    "nouveau-3 : 1,5 ; 2,25 ; 3,375 ; 5,0625")
chk(round(math.exp(2), 3) == 7.389, "nouveau-3 : e² ≈ 7,389")
# --- nouveau-4 : (1 + 1/n)^n
w = lambda k: (1 + R(1, k)) ** k  # noqa: E731
chk(w(1) == 2 and w(2) == R(9, 4) and w(3) == R(64, 27) and round(float(w(3)), 3) == 2.370, "nouveau-4 : u1, u2, u3")
chk([round(float(w(k)), 4) for k in range(1, 6)] == [2.0, 2.25, 2.3704, 2.4414, 2.4883], "nouveau-4 : u1..u5")
E = sp.E
chk(sp.N(E - w(134), 30) >= R(1, 100) and sp.N(E - w(135), 30) < R(1, 100), "nouveau-4 : seuil exact n = 135 (30 chiffres)")
chk(round(float(E - w(134)), 5) == 0.01007, "nouveau-4 : écart ≈ 0,01007 pour n = 134")
chk(all(1 + R(1, k ** k) <= 2 for k in range(1, 50)) and round(float(E - 2), 3) == 0.718, "nouveau-4 : 1 + 1/n^n ≤ 2, e - 2 ≈ 0,718")
# --- nouveau-5 : roue
loi = {-2: R(6, 10), 2: R(3, 10), 8: R(1, 10)}
chk(sum(loi.values()) == 1 and sum(k * p for k, p in loi.items()) == R(1, 5), "nouveau-5 : loi et E(G) = 0,2")
chk(loi[2] + loi[8] == R(2, 5), "nouveau-5 : P(G > 0) = 0,4")
# --- nouveau-6 : Archimède
chk(round(demi[0], 4) == 3.1058 and round(demi[1], 4) == 3.1326 and round(demi[2], 4) == 3.1394 and round(demi[3], 4) == 3.1410,
    "nouveau-6 : tableau des demi-périmètres")
chk(demi[2] <= 3.14 < demi[3], "nouveau-6 : 96 côtés pour dépasser 3,14")

# ------------------------------------------------------------------ bilan
print(f"{n_prog} programme(s) exécuté(s), {n_aff} affichage(s) comparé(s), {n_trous} programme(s) à compléter non exécuté(s)")
print(f"{n_controles} contrôle(s) mathématique(s)")
for e in erreurs:
    print("  ✗", e)
print("OK : tout est vérifié" if not erreurs else f"{len(erreurs)} erreur(s)")
raise SystemExit(1 if erreurs else 0)
