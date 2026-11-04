# -*- coding: utf-8 -*-
"""Vérification de la notion 178 « Notion de fonction (Python) ».

1. Tous les blocs ```python des fichiers finaux : lignes <= 30 caractères,
   syntaxe correcte.
2. Chaque résultat annoncé (cours, fiche, exercices) recalculé en exécutant
   le code, avec des tirages imposés quand l'énoncé les fixe.
"""
import math
import random
import re
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
FICHIERS = ["cours_220.txt", "fiche_136.txt", "exercices.txt"]
ERREURS = []


def ok(cond, msg):
    if not cond:
        ERREURS.append(msg)


# ---------------------------------------------------------------- 1. code
for nom in FICHIERS:
    texte = (ICI / nom).read_text(encoding="utf-8")
    for bloc in re.findall(r"```python\n(.*?)```", texte, re.S):
        lignes = bloc.split("\n")
        retrait = min((len(l) - len(l.lstrip()) for l in lignes if l.strip()), default=0)
        code = "\n".join(l[retrait:] for l in lignes)
        for l in code.split("\n"):
            ok(len(l.rstrip()) <= 30, f"{nom} : ligne de code > 30 car. : {l!r}")
        try:
            compile(code, nom, "exec")
        except SyntaxError as e:
            ERREURS.append(f"{nom} : erreur de syntaxe {e} dans\n{code}")


class De:
    """randint / random imposés (suite de valeurs)."""

    def __init__(self, valeurs):
        self.v = list(valeurs)

    def randint(self, a, b):
        x = self.v.pop(0)
        assert a <= x <= b
        return x


# ---------------------------------------------------------------- 2. cours
def f(x):
    return 3 * x + 2


def prix_ttc(ht, t):
    return ht * (1 + t / 100)


def est_pair(n):
    return n % 2 == 0


def tarif(age):
    if age < 12:
        return 5
    elif age < 18:
        return 8
    else:
        return 11


ok(f(4) == 14, "f(4)")
ok(prix_ttc(50, 20) == 60.0 and repr(prix_ttc(50, 20)) == "60.0", "prix_ttc(50, 20)")
ok(prix_ttc(20, 50) == 30.0, "prix_ttc(20, 50)")
ok(est_pair(7) is False and tarif(15) == 8, "est_pair / tarif")
# moyenne et écart type théoriques d'un dé
m_th = sum(range(1, 7)) / 6
e_th = math.sqrt(sum(k * k for k in range(1, 7)) / 6 - m_th ** 2)
ok(m_th == 3.5 and abs(e_th - 1.7078) < 1e-4, "moyenne / écart type théoriques")
ok(abs(1 / 6 - 0.167) < 5e-4, "1/6 ≈ 0,167")

# figures : données de simulation
sys.path.insert(0, str(ICI / "figures"))
import figures as FIG  # noqa: E402
ok(abs(FIG.SIX[-1][1] - 1 / 6) < 0.02, "figure fréquence du 6 : fin proche de 1/6")
ok(max(f for _, f in FIG.SIX) <= 0.35, "figure fréquence du 6 : ymax")
ok(abs(FIG.TIR[-1][1] - 0.707) < 5e-4, "figure tir : fréquence finale 0,707")
ok(max(f for _, f in FIG.TIR) <= 1.0, "figure tir : ymax")

# ---------------------------------------------------------------- 3. exercices
# 1942
def gain_jeu(mise, de):
    return mise if de >= 4 else -mise


ok(gain_jeu(4, 4) == 4 and gain_jeu(4, 2) == -4, "1942 Q1")
serie = [3, 1, 6, 2, 3]
m = sum(serie) / 5
V = sum(x * x for x in serie) / 5 - m * m
ok(m == 3 and sum(x * x for x in serie) == 59 and abs(V - 2.8) < 1e-12, "1942 Q4 m, V")
ok(round(math.sqrt(V), 2) == 1.67, "1942 Q4 sigma")
ok(abs(sum((x - m) ** 2 for x in serie) / 5 - V) < 1e-12, "1942 Q4 V par la définition")

# 1936
ok(3 * 4 == 12 and 3 * 4 + 1 == 13 and 10 + 1 == 11 and (-3) ** 2 == 9, "1936")

# 1937
def affine(a, b, x):
    return a * x + b


ok(7 + 5 == 12, "1937 Q1")
ok(affine(3, -1, 4) == 11 and affine(-1, 4, 3) == 1, "1937 Q2-Q3")
ok(affine(2, -7, 5) == 3, "1937 Q4")
ok(repr(8 * 2.5) == "20.0", "1937 Q5")

# 1938
def mystere(x):
    y = x + 5
    y = y * 3
    return y


ok(mystere(2) == 21 and all(mystere(x) == 3 * x + 15 for x in range(-5, 6)), "1938 Q1-Q2")
ok((7 + 3) * (7 - 3) == 40 == 7 ** 2 - 3 ** 2, "1938 Q3-Q4")
ok(4 * 2 + 10 == 18, "1938 Q5")

# 1939
ok(round(2 * math.pi * 5, 2) == 31.42, "1939 Q1")
ok(repr(4 * 3 / 2) == "6.0", "1939 Q2")


def f1939(x):
    y = x ** 2
    y = y - 4 * x
    y = y + 3
    return y


ok(f1939(1) == 0 and f1939(3) == 0, "1939 Q3")
ok(all(f1939(x) == x * x - 4 * x + 3 for x in range(-5, 6)), "1939 Q3 b")
ok(1 - 4 + 7 == 4, "1939 Q4")
ok(repr(math.sqrt(3 ** 2 + 4 ** 2)) == "5.0", "1939 Q5")

# 1940 : valeurs de deux dés, 2 * randint pair
ok(sorted({a + b for a in range(1, 7) for b in range(1, 7)}) == list(range(2, 13)), "1940 Q2")
ok(all((2 * a) % 2 == 0 for a in range(1, 7)), "1940 attention")

# 1941 : exécution avec 2, 5, 2
de = De([2, 5, 2])
s = s2 = 0
for _ in range(3):
    x = de.randint(1, 6)
    s, s2 = s + x, s2 + x * x
m = s / 3
v = s2 / 3 - m * m
ok((s, s2, m, v) == (9, 33, 3.0, 2.0) and round(v ** 0.5, 3) == 1.414, "1941 Q3")


def stats_des(n, gen):
    s = s2 = 0
    for _ in range(n):
        x = gen.randint(1, 6)
        s, s2 = s + x, s2 + x * x
    m = s / n
    return m, (s2 / n - m * m) ** 0.5


m, e = stats_des(10000, random.Random(41))
ok((round(m, 4), round(e, 3)) == (3.475, 1.713), f"1941 Q4 sortie annoncée : {m:.4f}, {e:.4f}")
ok(abs(e - e_th) < 0.01 and abs(m - 3.5) < 0.03, "1941 Q4 : valeurs plausibles")

# 1943
def gain_tombola(num):
    if num == 20:
        return 50
    elif num % 5 == 0:
        return 10
    return 0


g = [gain_tombola(t) for t in [7, 10, 20, 3, 15]]
ok(g == [0, 10, 50, 0, 10] and sum(g) == 70 and sum(g) / 5 == 14.0, "1943 Q4")
ok(sum(gain_tombola(k) > 0 for k in range(1, 21)) / 20 == 0.2, "1943 Q5")

# nouveau-1
ok(abs(500 * 0.85 - 425) < 1e-9, "nouveau-1 Q5")

# nouveau-2
ok(5 + 1 == 6 and 2 * 5 + 1 == 11, "nouveau-2 Q1")
ok(4 + 6 / 2 == 7 and (4 + 6) / 2 == 5.0, "nouveau-2 Q5")
ok(abs(600 / 6 - 100) < 1e-9, "nouveau-2 Q2")

# ================================================================ 4. EXÉCUTION RÉELLE
# (finition 2026-11-02) Chaque bloc ```python des fichiers est exécuté tel
# qu'il est écrit ; les fonctions ainsi définies sont appelées et leurs
# résultats (et leurs affichages) comparés à ceux annoncés dans le texte.
import contextlib
import io
import textwrap

N_EXEC = 0


def blocs_de(texte):
    return [textwrap.dedent(b) for b in re.findall(r"```python\n(.*?)```", texte, re.S)]


def exercice(eid):
    t = (ICI / "exercices.txt").read_text(encoding="utf-8")
    for b in re.split(r"^===[ \t]*$", t, flags=re.M):
        if re.search(rf"^Id:\s*{eid}\s*$", b, re.M):
            return blocs_de(b)
    raise KeyError(eid)


def run(*codes, imports=True):
    """Exécute des blocs dans un espace de noms neuf ; renvoie cet espace."""
    global N_EXEC
    ns = {}
    if imports:
        exec("from random import randint, random\nfrom math import sqrt, pi", ns)
    for c in codes:
        exec(c, ns)
        N_EXEC += 1
    return ns


def sortie(fn, *args):
    """(valeur renvoyée, texte affiché) d'un appel."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        v = fn(*args)
    return v, buf.getvalue()


def force(ns, valeurs):
    """Remplace randint par une suite de tirages imposés."""
    it = iter(valeurs)
    ns["randint"] = lambda a, b: next(it)


def avec(blocs, mot):
    r = [b for b in blocs if mot in b]
    assert r, mot
    return r


# ---- cours (tous les blocs ensemble, dans l'ordre)
cours = blocs_de((ICI / "cours_220.txt").read_text(encoding="utf-8"))
C = run(*cours)
ok(C["f"](4) == 14, "exec cours f(4)")
ok(repr(C["prix_ttc"](50, 20)) == "60.0" and C["prix_ttc"](20, 50) == 30.0, "exec cours prix_ttc")
ok(C["est_pair"](7) is False and C["tarif"](15) == 8, "exec cours est_pair / tarif")
random.seed(5)
ok(0 <= C["frequence_six"](1000) <= 1 and C["epreuve"](1) == 1 and C["epreuve"](0) == 0, "exec cours aléatoire")
random.seed(2026)
m_c, e_c = C["moyenne_ecart_type"](10000)
ok(abs(m_c - 3.5) < 0.05 and abs(e_c - 1.71) < 0.03, f"exec cours moyenne_ecart_type(10000) = {m_c}, {e_c}")
fiche = run(*blocs_de((ICI / "fiche_136.txt").read_text(encoding="utf-8")))
ok(fiche["f"](4) == 14, "exec fiche f(4)")

# ---- 1936
B = exercice(1936)
X = run(*B)
ok(X["triple"](4) == 12 and X["triple"](4) + 1 == 13, "exec 1936 Q1-Q2")
v, aff = sortie(X["triple_b"], 4)
ok(v is None and aff == "12\n", "exec 1936 Q3 : affiche 12, renvoie None")
ok(X["suivant"](10) == 11 and X["carre"](-3) == 9, "exec 1936 Q4-Q5")

# ---- 1937
X = run(*exercice(1937))
ok(X["somme"](7, 5) == 12, "exec 1937 Q1")
ok(X["affine"](3, -1, 4) == 11 and X["affine"](-1, 4, 3) == 1 and X["affine"](2, -7, 5) == 3, "exec 1937 Q2-Q4")
ok(repr(X["aire_rectangle"](8, 2.5)) == "20.0", "exec 1937 Q5 : 20.0")

# ---- 1938
X = run(*exercice(1938))
ok(X["mystere"](2) == 21, "exec 1938 Q1")
ok([X["mystere"](t) for t in range(-6, 2)] == [-3, 0, 3, 6, 9, 12, 15, 18], "exec 1938 table de valeurs")
ok(X["calcul"](7, 3) == 40 and X["double_puis_ajoute"](4, 10) == 18, "exec 1938 Q3-Q5")
ok(FIG.PTS_MYSTERE == [(t, X["mystere"](t)) for t in range(-6, 2)], "figure 1938 = valeurs de mystere")

# ---- 1939 (version fausse et version corrigée exécutées séparément)
B = exercice(1939)
peri = run(avec(B, "return 2 * pi * r")[0])
ok(round(peri["perimetre"](5), 2) == 31.42, "exec 1939 Q1 perimetre(5) ≈ 31,42")
faux, juste = (run(b) for b in avec(B, "def aire_triangle"))
ok(faux["aire_triangle"](4, 3) == 12 and repr(juste["aire_triangle"](4, 3)) == "6.0", "exec 1939 Q2 : 12 puis 6.0")
X = run(*avec(B, "def f(x)"), *avec(B, "def g(x)"))
ok(X["f"](1) == 0 and X["f"](3) == 0 and X["g"](1) == 4, "exec 1939 Q3-Q4")
ok([X["f"](t) for t in range(-1, 6)] == [8, 3, 0, -1, 0, 3, 8], "exec 1939 points de f")
ok(FIG.PTS_F == [(t, X["f"](t)) for t in range(-1, 6)] and FIG.PTS_G == [(t, X["g"](t)) for t in range(-1, 6)], "figures 1939 = valeurs de f et g")
D = run(avec(B, "def distance")[0])
ok(repr(D["distance"](0, 0, 3, 4)) == "5.0", "exec 1939 Q5 : 5.0")

# ---- 1940
X = run(*exercice(1940))
random.seed(1)
ok({X["lancer_de"]() for _ in range(2000)} == set(range(1, 7)), "exec 1940 Q1 valeurs 1 à 6")
ok({X["deux_des"]() for _ in range(5000)} == set(range(2, 13)), "exec 1940 Q2 valeurs 2 à 12")
k = X["nombre_piles"](100)
ok(isinstance(k, int) and 0 <= k <= 100 and 0 <= X["freq_piles"](100) <= 1, "exec 1940 Q3-Q4")
ok(0 <= X["nombre_six"](100) <= 100, "exec 1940 Q5")
ok(FIG.FREQ_DEUX[5][0] == 7 and max(FIG.FREQ_DEUX, key=lambda t: t[1])[0] == 7, "figure 1940 : 7 la plus fréquente")
ok(abs(sum(f for _, f in FIG.FREQ_DEUX) - 1) < 1e-9, "figure 1940 : somme des fréquences = 1")

# ---- 1941
B = exercice(1941)
X = run(B[0])
force(X, [2, 5, 2])
m3, e3 = X["stats_des"](3)
ok(m3 == 3.0 and round(e3, 3) == 1.414, "exec 1941 Q3 avec 2, 5, 2")
X = run(B[0])
random.seed(41)
m41, e41 = X["stats_des"](10000)
ok(round(m41, 3) == 3.475 and round(e41, 3) == 1.713, f"exec 1941 Q4 sortie annoncée : {m41}, {e41}")
ok((FIG.M_STATS, FIG.E_STATS) == (m41, e41), "figure 1941 = sortie de stats_des(10000)")
ok(round(m41 - e41, 2) == 1.76 and round(m41 + e41, 2) == 5.19, "figure 1941 bande m ± σ")
random.seed(3)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(B[1], X)
lignes = buf.getvalue().split()
ok(len(lignes) == 2, "exec 1941 Q5 : m, e = stats_des(1000) puis deux print")

# ---- 1942
X = run(*exercice(1942))
force(X, [4])
ok(X["gain_jeu"](4) == 4, "exec 1942 Q1 dé 4")
force(X, [2])
ok(X["gain_jeu"](4) == -4, "exec 1942 Q1 dé 2")
force(X, [6, 1, 4])
ok(X["gain_total"](2, 3) == 2, "exec 1942 Q2 (6, 1, 4) : +2 - 2 + 2")
force(X, [3, 1, 6, 2, 3])
ok(X["moyenne_des"](5) == 3.0, "exec 1942 Q3 (3, 1, 6, 2, 3)")
force(X, [2, 3, 6, 5])
ok(X["frequence_pair"](4) == 0.5, "exec 1942 Q5")
X = run(*exercice(1942))
random.seed(1942)
ok(FIG.PAIR == [(n, X["frequence_pair"](n)) for n in range(10, 3001, 10)], "figure 1942 = appels réels de frequence_pair")

# ---- 1943
X = run(*exercice(1943))
force(X, [7, 10, 20, 3, 15])
ok(X["gains"](5) == (70, 14.0), "exec 1943 Q4 : (70, 14.0)")
force(X, [20, 5, 4])
ok([X["tirage"](), X["tirage"](), X["tirage"]()] == [50, 10, 0], "exec 1943 Q1")
X = run(*exercice(1943))
random.seed(1943)
ok(FIG.GAGNANTS == [(n, X["nb_gagnants"](n) / n) for n in range(10, 3001, 10)], "figure 1943 = appels réels de nb_gagnants")
ok(sum(X["tirage"]() > 0 for _ in range(20000)) / 20000 - 0.2 < 0.02, "exec 1943 Q5 fréquence ≈ 0,2")

# ---- 3741
B = exercice(3741)
X = run(*B[:3])
random.seed(7)
ok(X["lancer_franc"]() in (0, 1) and 0 <= X["freq_reussite"](100) <= 1, "exec 3741 Q2-Q4")
Y = run(*B[3:])
random.seed(85)
r = Y["nb_reussites"](500, 0.85)
ok(380 <= r <= 470, f"exec 3741 Q5 nb_reussites(500, 0.85) = {r}")

# ---- 3742 : les fonctions fausses produisent bien les effets décrits
B = exercice(3742)
X = run(B[0])
v, aff = sortie(X["double"], 5)
ok(v is None and aff == "10\n", "exec 3742 Q1 : affiche 10, renvoie None")
try:
    with contextlib.redirect_stdout(io.StringIO()):
        X["double"](5) + 1
    ok(False, "exec 3742 Q1 : None + 1 devrait échouer")
except TypeError:
    pass
X = run(B[1])
force(X, [6, 6, 6, 2])
ok(X["nb_six"](4) == 0, "exec 3742 Q2 : compteur remis à 0, dernier lancer 2 -> 0")
X = run(B[2])
force(X, [4, 6, 6])
ok(X["somme_des"](3) == 4, "exec 3742 Q3 : un seul lancer additionné")
X = run(B[3], imports=False)
try:
    X["de"]()
    ok(False, "exec 3742 Q4 : NameError attendu")
except NameError as err:
    ok("randint" in str(err), "exec 3742 Q4 : message NameError")
X = run(B[4])
ok(repr(X["moyenne"](4, 6)) == "7.0", "exec 3742 Q5 : 7.0")
corr = {nom: run(b) for nom, b in zip(["double", "nb_six", "somme_des", "de", "moyenne"], B[5:10])}
ok(corr["double"]["double"](5) + 1 == 11, "exec 3742 Q1 corrigée : y = 11")
force(corr["nb_six"], [6, 6, 6, 2])
ok(corr["nb_six"]["nb_six"](4) == 3, "exec 3742 Q2 corrigée")
force(corr["somme_des"], [4, 6, 6])
ok(corr["somme_des"]["somme_des"](3) == 16, "exec 3742 Q3 corrigée")
ok(corr["de"]["de"]() in range(1, 7), "exec 3742 Q4 corrigée")
ok(repr(corr["moyenne"]["moyenne"](4, 6)) == "5.0", "exec 3742 Q5 corrigée : 5.0")
corr["nb_six"]["randint"] = random.randint  # retour au vrai hasard
random.seed(600)
ok(80 <= corr["nb_six"]["nb_six"](600) <= 120, "exec 3742 Q2 : nb_six(600) proche de 100")

if ERREURS:
    print("\n".join(ERREURS))
    sys.exit(1)
print(f"Toutes les vérifications sont correctes ({N_EXEC} blocs de code exécutés).")
