# -*- coding: utf-8 -*-
"""Vérification mathématique de la notion 268 (5e : lettres, formules et motifs).

    python verif_268.py

1. Contrôles explicites (sympy, valeurs exactes) de chaque réponse des exercices,
   du cours et de la fiche ; formules des motifs comparées à un comptage direct
   des objets dessinés (allumettes, carreaux, chaises) ; formules de tableur
   exécutées par un mini-interpréteur.
2. Contrôle automatique : toute égalité purement numérique écrite entre $…$ dans
   les fichiers (chaînes « a = b = c », « ≠ ») est recalculée exactement.
3. Structure : 10 exercices, progression, corrigés complets, aucune mention du brevet.
"""
import re
import sys
from fractions import Fraction
from pathlib import Path

import sympy as sp

ICI = Path(__file__).resolve().parent
ok, ko = 0, []


def check(cond, msg):
    global ok
    if cond:
        ok += 1
    else:
        ko.append(msg)


x, n, c, L, l, a, b = sp.symbols("x n c L l a b")
D = sp.Rational

# ===================================================================== cours / fiche
check((2 * 3, 2 * 10) == (6, 20), "cours : prix des cahiers")
check(2 * 7 + 2 * 3 == 20 and 7 * 3 == 21, "cours : rectangle 7 × 3")
check(15 + 4 * 10 == 55, "cours : escalade 10 séances")
check(all(3 * k + 1 == 1 + 3 * k for k in range(1, 50)), "cours : 1 + 3n = 3n + 1")
check([3 * k + 1 for k in (1, 2, 3)] == [4, 7, 10], "cours : motif 4, 7, 10")
check(3 * 20 + 1 == 61, "cours : étape 20")
check(3 * 2 + 1 == 7 and 3 * 4 + 1 == 13 and 13 != 2 * 7, "cours : doubler l'étape")
E = 5 * a**2 - 2 * a + 1
check(E.subs(a, 3) == 40 and 5 * 9 == 45 and 45 - 6 + 1 == 40, "cours : 5a²-2a+1 pour a=3")
check((5 * 3)**2 == 225 and 5 * 3**2 == 45, "cours : 5×3² ≠ 15²")
eg = (4 * x - 3, 2 * x + 5)
check(eg[0].subs(x, 4) == 13 == eg[1].subs(x, 4), "cours : égalité vraie pour x=4")
check((eg[0].subs(x, 2), eg[1].subs(x, 2)) == (5, 9), "cours : égalité fausse pour x=2")
check(sp.solve(sp.Eq(*eg), x) == [4], "cours : seule solution 4")
check(5 * (6 + 4) == 50 and 6 + 4 * 5 == 26, "cours : programme avec 6")
check(6**2 == 36 and 2 * 6 == 12 and 4 * 7 == 28, "cours : a²≠2a, 4×7")

# ===================================================================== mini-tableur
def tableur(formule, cellules):
    """Évalue une formule de tableur simple (=…, *, /, ^, +, -, parenthèses, références A2…)."""
    assert formule.startswith("=")
    expr = formule[1:]
    assert re.fullmatch(r"[A-Z0-9*+\-/^().]+", expr), formule
    # une référence collée à un nombre (3A2) est une erreur de syntaxe
    if re.search(r"\d[A-Z]", expr):
        raise SyntaxError("signe * manquant : " + formule)
    expr = re.sub(r"([A-Z]+\d+)", lambda m: "(%s)" % cellules[m.group(1)], expr).replace("^", "**")
    return sp.nsimplify(eval(expr, {"__builtins__": {}}))


def recopie(formule, k):
    """Recopie vers le bas de k lignes : les numéros de ligne augmentent de k."""
    return re.sub(r"([A-Z]+)(\d+)", lambda m: m.group(1) + str(int(m.group(2)) + k), formule)


check([tableur(recopie("=3*A2+1", k), {"A%d" % (2 + k): k + 1}) for k in range(5)] == [4, 7, 10, 13, 16],
      "cours : tableur =3*A2+1")
try:
    tableur("=3A2+1", {"A2": 1})
    check(False, "cours : =3A2+1 devrait être refusé")
except SyntaxError:
    check(True, "")

# ===================================================================== 2854
X = sp.Symbol("x")
check((2 * (X + 5)).subs(X, 3) == 16 and (2 * X + 5).subs(X, 3) == 11, "2854 Q4")
check(4 * 7 == 28 and 3**2 == 9 and 2 * 3 == 6, "2854 : 28, x² et 2x pour 3")
check(sp.simplify(6 * x - sp.Mul(x, 6)) == 0 and sp.simplify(1 * x - x) == 0, "2854 Q2")

# ===================================================================== 2861
A_, B_, C_, D_ = 3 * x + 5, x**2 + 2, 2 * (x - 1), 5 * x**2
check([e.subs(x, 4) for e in (A_, B_, C_, D_)] == [17, 18, 6, 80], "2861 Q1")
check(A_.subs(x, D(5, 2)) == D(25, 2) and B_.subs(x, D(5, 2)) == D(33, 4), "2861 Q2 (12,5 et 8,25)")
check((5 * 4)**2 == 400 and 5 * 4**2 == 80, "2861 Q3")
G, Dr = 3 * x + 5, x**2 + 1
check(G.subs(x, 4) == 17 == Dr.subs(x, 4), "2861 Q4a")
check((G.subs(x, 2), Dr.subs(x, 2)) == (11, 5), "2861 Q4b")
check(set(sp.solve(sp.Eq(G, Dr), x)) == {-1, 4}, "2861 : solutions -1 et 4 (2 est bien un contre-exemple)")


# ===================================================================== 2852 : comptage direct des allumettes
def allumettes_triangles(nb):
    """Arêtes (segments) d'une bande de nb triangles alternés, comptées sans doublon."""
    s = set()
    for k in range(nb):
        if k % 2 == 0:
            B0, B1, T = ("B", k // 2), ("B", k // 2 + 1), ("T", k // 2)
            tri = [(B0, B1), (B1, T), (B0, T)]
        else:
            T0, T1, B1 = ("T", k // 2), ("T", k // 2 + 1), ("B", k // 2 + 1)
            tri = [(T0, T1), (T0, B1), (B1, T1)]
        for e in tri:
            s.add(frozenset(e))
    return len(s)


check([allumettes_triangles(k) for k in range(1, 6)] == [3, 5, 7, 9, 11], "2852 Q1-Q2 comptage")
check(all(allumettes_triangles(k) == 2 * k + 1 for k in range(1, 80)), "2852 Q3 formule 2n+1")
check(2 * 10 + 1 == 21 and 2 * 50 + 1 == 101, "2852 Q4")
check(2 * 20 + 1 == 41 and 2 * 21 == 42, "2852 Q5")


def allumettes_carres(nb):
    s = set()
    for k in range(nb):
        for e in (((k, 0), (k + 1, 0)), ((k, 1), (k + 1, 1)), ((k, 0), (k, 1)), ((k + 1, 0), (k + 1, 1))):
            s.add(frozenset(e))
    return len(s)


check(all(allumettes_carres(k) == 3 * k + 1 for k in range(1, 80)), "cours : carrés accolés 3n+1 (comptage)")

# ===================================================================== 2856
P_carre, P_rect, P_tri, P_hex = 4 * c, 2 * L + 2 * l, 3 * a, 6 * b
val = {c: 6, L: D(17, 2), l: 4, a: 7, b: D(7, 2)}
check(P_carre.subs(val) == 24 and (c**2).subs(val) == 36, "2856 carré")
check(P_rect.subs(val) == 25 and (L * l).subs(val) == 34, "2856 rectangle")
check(P_tri.subs(val) == 21 and P_hex.subs(val) == 21, "2856 triangle / hexagone")
check(2 * D(17, 2) == 17 and 17 + 8 == 25, "2856 étape rectangle")
check(4 * 4 == 4**2 == 16 and (4 * 6, 6**2) == (24, 36), "2856 Q4a")

# ===================================================================== 2853
PA = lambda v: v * 4 + 3
PB = lambda v: (v + 3) * 4
check((PA(5), PB(5)) == (23, 32), "2853 Q1")
check((PA(D(5, 2)), PB(D(5, 2))) == (13, 22) and D(5, 2) + 3 == D(11, 2), "2853 Q2")
check(sp.expand(PA(x) - (4 * x + 3)) == 0 and sp.expand(PB(x) - 4 * (x + 3)) == 0, "2853 Q3")
check(all(((v * 5) - 2 == 5 * v - 2) and ((v - 2) * 5 == 5 * (v - 2)) for v in range(-5, 10)), "2853 Q4")
check((x**2 + 6).subs(x, D(3, 2)) == D(33, 4) and D(3, 2)**2 == D(9, 4), "2853 Q5 (8,25)")
check(5 + 3 * 4 == 17, "2853 erreur fréquente : x + 3 × 4 = 17 pour x = 5")

# ===================================================================== 2859
Bv = [tableur(recopie("=3*A2+4", k), {"A%d" % (2 + k): k}) for k in range(6)]
Cv = [tableur(recopie("=A2*A2", k), {"A%d" % (2 + k): k}) for k in range(6)]
Cv2 = [tableur(recopie("=A2^2", k), {"A%d" % (2 + k): k}) for k in range(6)]
check(Bv == [4, 7, 10, 13, 16, 19], "2859 colonne B")
check(Cv == Cv2 == [0, 1, 4, 9, 16, 25], "2859 colonne C")
check(recopie("=3*A2+4", 3) == "=3*A5+4", "2859 Q3 recopie en B5")
check([k for k in range(6) if Bv[k] == Cv[k]] == [4], "2859 Q5 seule ligne x = 4")
try:
    tableur("=3A2+4", {"A2": 0})
    check(False, "2859 Q6 =3A2+4 devrait être refusé")
except SyntaxError:
    check(True, "")

# ===================================================================== 2872
Lf, Cf = 5 * n, 3 * n + 12
check((Lf.subs(n, 4), Cf.subs(n, 4)) == (20, 24), "2872 Q1")
check([Lf.subs(n, k) for k in (2, 4, 6, 8, 10)] == [10, 20, 30, 40, 50], "2872 Q3 L")
check([Cf.subs(n, k) for k in (2, 4, 6, 8, 10)] == [18, 24, 30, 36, 42], "2872 Q3 C")
check(Lf.subs(n, 6) == Cf.subs(n, 6) == 30 and sp.solve(sp.Eq(Lf, Cf), n) == [6], "2872 Q4")
check(Cf.subs(n, 2) > Lf.subs(n, 2), "2872 Q5 contre-exemple")
check(all(Cf.subs(n, k) < Lf.subs(n, k) for k in range(7, 100)) and all(Cf.subs(n, k) > Lf.subs(n, k) for k in range(0, 6)),
      "2872 Q5 : carte avantageuse au-delà de 6 entrées")
check((Lf.subs(n, 15), Cf.subs(n, 15), Lf.subs(n, 15) - Cf.subs(n, 15)) == (75, 57, 18), "2872 Q6")


# ===================================================================== 2866 : comptage direct
def bordure(k):
    N = k + 2
    return sum(1 for i in range(N) for j in range(N) if i in (0, N - 1) or j in (0, N - 1))


check([bordure(k) for k in (1, 2, 3)] == [8, 12, 16], "2866 Q1")
check(3 + 3 + 1 + 1 == 8 and 4 + 4 + 2 + 2 == 12 and 5 + 5 + 3 + 3 == 16, "2866 Q1 détail")
check(all(bordure(k) == 4 * k + 4 for k in range(1, 80)), "2866 Q2 formule 4n+4")
check(4 * 10 + 4 == 44 and 4 * 25 + 4 == 104, "2866 Q4")
check([k for k in range(1, 200) if 4 * k + 4 == 64] == [15] and (64 - 4) // 4 == 15, "2866 Q5")
check([k for k in range(1, 200) if 4 * k + 4 == 50] == [] and 46 % 4 != 0 and (4 * 11 + 4, 4 * 12 + 4) == (48, 52),
      "2866 Q6")
check(4 * (3 + 2) == 20, "2866 erreur fréquente")


# ===================================================================== 2867 : comptage direct des chaises
def chaises_comptees(k):
    """Côtés libres de k tables carrées alignées (cases (0..k-1, 0))."""
    tables = {(i, 0) for i in range(k)}
    libres = 0
    for (i, j) in tables:
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (i + di, j + dj) not in tables:
                libres += 1
    return libres


check([chaises_comptees(k) for k in (1, 2, 3, 4)] == [4, 6, 8, 10], "2867 Q1")
check(all(chaises_comptees(k) == 2 * k + 2 for k in range(1, 80)), "2867 Q2 formule 2n+2")
cui = lambda v: (v + 2) * 2
check(cui(3) == 10 and chaises_comptees(3) == 8, "2867 Q3-Q4 programme faux")
check(tableur("=2*A2+2", {"A2": 30}) == 62 == chaises_comptees(30), "2867 Q5-Q6")
check([k for k in range(1, 200) if 2 * k + 2 == 50] == [24] and (50 - 2) // 2 == 24, "2867 Q7")
check(4 * 3 == 12, "2867 erreur fréquente")

# ===================================================================== 2868
Pp, Ap = 2 * x + 2 * (x + 5), x * (x + 5)
check((Pp.subs(x, 4), Ap.subs(x, 4)) == (26, 36), "2868 Q3")
check([Pp.subs(x, k) for k in (3, 4, 5, 6)] == [22, 26, 30, 34], "2868 Q4 B")
check([Ap.subs(x, k) for k in (3, 4, 5, 6)] == [24, 36, 50, 66], "2868 Q4 C")
check([tableur(recopie("=2*A2+2*(A2+5)", k), {"A%d" % (2 + k): v}) for k, v in enumerate((3, 4, 5, 6))] == [22, 26, 30, 34],
      "2868 formule B2")
check([tableur(recopie("=A2*(A2+5)", k), {"A%d" % (2 + k): v}) for k, v in enumerate((3, 4, 5, 6))] == [24, 36, 50, 66],
      "2868 formule C2")
check(sp.solve(sp.Eq(Pp, 34), x) == [6] and 6 + 5 == 11, "2868 Q5")
check((Ap.subs(x, 5), Pp.subs(x, 5)) == (50, 30), "2868 Q6")
check(2 * 4 + 5 == 13 and 2 * (4 + 5) == 18, "2868 erreur fréquente")
check(6 + 16 == 22 and 8 + 18 == 26 and 10 + 20 == 30 and 12 + 22 == 34, "2868 détail des périmètres")


# ===================================================================== contrôle automatique des égalités numériques
def tex_vers_py(s):
    s = s.replace("{,}", ".").replace(r"\times", "*").replace(r"\div", "/")
    s = s.replace(r"\left", "").replace(r"\right", "").replace(r"\,", "").replace(r"\quad", " ")
    s = re.sub(r"\\text\{[^}]*\}", " ", s)
    s = re.sub(r"\^\{?(\d+)\}?", r"**\1", s)
    s = re.sub(r"(\d)\s*\(", r"\1*(", s)
    s = s.replace("€", "")
    return s.strip()


NUM = re.compile(r"^[\d.\s+\-*/()]+$")


def egalites(texte, ou):
    """Recalcule les chaînes d'égalités purement numériques."""
    global ok
    vus = 0
    blocs = re.findall(r"\$\$(.+?)\$\$", texte, re.S) + re.findall(r"(?<!\$)\$([^$\n]+)\$(?!\$)", texte)
    for m in blocs:
        for ligne in re.split(r"\\\\|\\qquad|&(?=\s*[A-Za-z\\])", m):
            ligne = ligne.replace("&", "")
            ligne = re.sub(r"\\begin\{aligned\}|\\end\{aligned\}", "", ligne)
            for rel in (r"\neq", r"\ne"):
                if rel in ligne:
                    g, d = ligne.split(rel, 1)
                    g, d = tex_vers_py(g.split("=")[-1]), tex_vers_py(d.split("=")[0])
                    if NUM.match(g) and NUM.match(d) and g and d:
                        vus += 1
                        if Fraction(str(sp.nsimplify(eval(g)))) == Fraction(str(sp.nsimplify(eval(d)))):
                            ko.append(f"{ou} : « {ligne.strip()} » (≠ faux)")
                        else:
                            ok += 1
                    ligne = ""
                    break
            membres = [tex_vers_py(p) for p in ligne.split("=")]
            membres = [p for p in membres if p]
            nums = [p for p in membres if NUM.match(p)]
            if len(nums) >= 2 and len(nums) == len(membres):
                vals = [sp.nsimplify(eval(p)) for p in nums]
                vus += 1
                if all(v == vals[0] for v in vals):
                    ok += 1
                else:
                    ko.append(f"{ou} : « {ligne.strip()} » → {vals}")
    return vus


total_auto = 0
for nom in ("cours_263.txt", "fiche_183.txt", "exercices.txt"):
    t = (ICI / nom).read_text(encoding="utf-8")
    total_auto += egalites(t, nom)
check(total_auto >= 80, f"contrôle automatique : seulement {total_auto} égalités lues")

# ===================================================================== structure
ex = (ICI / "exercices.txt").read_text(encoding="utf-8")
blocs = [b.strip() for b in re.split(r"^===[ \t]*$", ex, flags=re.M) if b.strip()]
check(len(blocs) == 10, f"{len(blocs)} exercices (10 attendus)")
types = [re.match(r"=== (\w+)", b).group(1) for b in blocs]
check(types == ["Découverte"] * 3 + ["Entraînement"] * 3 + ["Problème"] * 2 + ["Synthèse"] * 2, f"progression {types}")
retires = {int(m) for m in re.findall(r"^(\d+)", (ICI / "exercices_retires.txt").read_text(encoding="utf-8"), re.M)}
ids = [int(re.search(r"^Id: (\d+)", b, re.M).group(1)) for b in blocs]
check(len(retires) == 11 and not (retires & set(ids)) and len(set(ids) | retires) == 21, "Id gardés / retirés")
for b in blocs:
    eid = re.search(r"^Id: (\S+)", b, re.M).group(1)
    et = b.split("Étapes:", 1)[1].split("Solution:", 1)[0]
    nq = len(re.findall(r"^\d+\. ", b.split("Énoncé:", 1)[1].split("Étapes:", 1)[0], re.M))
    check(len(re.findall(r"^## Question", et, re.M)) == nq, f"{eid} : {nq} questions / corrigés")
    check(et.count("::: methode") >= nq and et.count("::: resultat") >= nq, f"{eid} : méthode et résultat par question")
    check("::: attention" in et or "::: retenir" in et, f"{eid} : erreur fréquente")
    sol = b.split("Solution:", 1)[1]
    check(len(re.findall(r"^\d+\. ", sol, re.M)) == nq, f"{eid} : solution courte complète")
for nom in ("cours_263.txt", "fiche_183.txt", "exercices.txt"):
    check("brevet" not in (ICI / nom).read_text(encoding="utf-8").lower(), f"{nom} : mention du brevet")

print(f"{ok} contrôles justes, {len(ko)} erreur(s) ; {total_auto} égalités numériques recalculées automatiquement")
for e in ko:
    print("  ✗", e)
sys.exit(1 if ko else 0)
