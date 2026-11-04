# -*- coding: utf-8 -*-
"""Vérification de la notion « Notion de liste » (Première) : chaque programme est EXÉCUTÉ.

    python verif_listes.py

1. Chaque bloc ```python des fichiers finaux (cours, fiche, exercices) est
   exécuté dans un espace de noms neuf. S'il est suivi d'un bloc ```console
   (seules des lignes vides ou « ::: » entre les deux), l'affichage obtenu doit
   être IDENTIQUE au texte du bloc console. Un bloc sans affichage annoncé doit
   s'exécuter sans erreur (les « ... » des programmes à compléter sont une
   instruction Python valide).
2. Les nombres annoncés dans le texte (tableaux, calculs, figures) sont
   recalculés par les assertions de la partie 2 (sympy pour l'algèbre).
3. Largeur sur téléphone : lignes de code ≤ 35 caractères au premier niveau,
   ≤ 31 dans un encadré, ≤ 29 dans une étape (mesures de la notion Terminale 99).
Code de sortie 0 seulement si tout est juste.
"""
import contextlib
import importlib.util
import io
import re
import sys
from fractions import Fraction
from pathlib import Path

import sympy as sp

ICI = Path(__file__).resolve().parent
FICHIERS = ["cours_152.txt", "fiche_62.txt", "exercices.txt"]
LARGEUR = {"haut": 35, "encadre": 31, "etape": 29}

FENCE = re.compile(r"^(\s*)```\s*([A-Za-z0-9_+-]*)\s*$")


def blocs(texte):
    """Blocs de code (langage, n° de ligne, code, ligne de fin, contexte d'encadré)."""
    lignes = texte.split("\n")
    out, i, pile = [], 0, []
    while i < len(lignes):
        l = lignes[i]
        m = FENCE.match(l)
        if m and m.group(2):
            base = len(m.group(1))
            corps, j = [], i + 1
            while j < len(lignes) and not re.match(r"^\s*```\s*$", lignes[j]):
                x = lignes[j]
                corps.append(x[base:] if x[:base].strip() == "" else x.lstrip())
                j += 1
            ctx = "haut" if not pile else ("etape" if pile[-1] in ("etape", "point") else "encadre")
            out.append((m.group(2), i + 1, "\n".join(corps).rstrip("\n"), j, ctx))
            i = j + 1
            continue
        s = l.strip()
        if re.match(r"^:::\s*\S", s):
            pile.append(s[3:].split()[0])
        elif s == ":::" and pile:
            pile.pop()
        elif re.match(r"^(Énoncé|Étapes|Solution):", s) or s.startswith("==="):
            pile = []
        i += 1
    return out, lignes


def executer(code, ns=None):
    """Exécute le code ; un bloc commençant par « # suite du programme » reprend
    l'espace de noms du programme précédent (ns)."""
    tampon = io.StringIO()
    if ns is None:
        ns = {"__name__": "__main__"}
    erreur = None
    with contextlib.redirect_stdout(tampon):
        try:
            exec(compile(code, "<bloc>", "exec"), ns)
        except Exception as e:  # noqa: BLE001
            erreur = f"{type(e).__name__}: {e}"
    sortie = tampon.getvalue().rstrip("\n")
    return sortie, erreur, ns


def verifier_fichier(nom, problemes):
    texte = (ICI / nom).read_text(encoding="utf-8")
    liste, lignes = blocs(texte)
    n_ok = n_compare = 0
    precedent = None
    for k, (lang, no, code, fin, ctx) in enumerate(liste):
        for l in code.split("\n"):
            if len(l) > LARGEUR[ctx]:
                problemes.append(f"{nom} l.{no} : ligne trop longue pour un téléphone "
                                 f"({len(l)} > {LARGEUR[ctx]} car., {ctx}) : {l}")
        if lang != "python":
            continue
        suivant = liste[k + 1] if k + 1 < len(liste) else None
        attendu = None
        if suivant and suivant[0] == "console":
            entre = lignes[fin + 1: suivant[1] - 1]
            if all(not x.strip() or x.strip().startswith(":::") for x in entre):
                attendu = suivant[2]
        suite = code.startswith("# suite du programme")
        if suite and precedent is None:
            problemes.append(f"{nom} l.{no} : « suite du programme » sans programme précédent")
        sortie, erreur, precedent = executer(code, dict(precedent) if suite and precedent else None)
        if erreur:
            problemes.append(f"{nom} l.{no} : erreur à l'exécution : {erreur}")
        elif attendu is not None and sortie != attendu:
            problemes.append(f"{nom} l.{no} : affichage différent\n--- obtenu ---\n{sortie}\n--- annoncé ---\n{attendu}")
        else:
            n_ok += 1
            n_compare += attendu is not None
    consoles_orphelines = [b for k, b in enumerate(liste) if b[0] == "console"
                           and not (k > 0 and liste[k - 1][0] == "python")]
    for b in consoles_orphelines:
        problemes.append(f"{nom} l.{b[1]} : bloc console qui ne suit pas un programme")
    n_py = sum(1 for b in liste if b[0] == "python")
    return n_ok, n_py, n_compare


# ---------------------------------------------------------------- partie 2
def charger_figures():
    spec = importlib.util.spec_from_file_location("figures_notion", ICI / "figures" / "figures.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def assertions():
    pb = []
    n = [0]

    def egal(desc, obtenu, attendu):
        n[0] += 1
        if obtenu != attendu:
            pb.append(f"{desc} : obtenu {obtenu!r}, annoncé {attendu!r}")

    def erreur(f):
        try:
            f()
        except Exception as e:  # noqa: BLE001
            return f"{type(e).__name__}: {e}"
        return None

    F = charger_figures()
    x, h, k, m = sp.symbols("x h k n")

    # ---- cours
    notes = [12, 15, 9, 14, 10]
    egal("cours notes[5]", erreur(lambda: notes[5]), "IndexError: list index out of range")
    egal("cours indices négatifs", all(notes[-j] == notes[5 - j] for j in range(1, 6)), True)
    egal("cours list(range(5))", list(range(5)), [0, 1, 2, 3, 4])
    egal("cours append None", [1].append(2), None)
    u = [1]
    for _ in range(5):
        u.append(2 * u[-1] + 1)
    egal("cours u_n = 2^(n+1) - 1", u, [2 ** (j + 1) - 1 for j in range(6)])
    egal("figure liste_append", F.U_COURS, [1, 3, 7, 15, 31])
    egal("cours suite arithmétique 3n + 2", [3 * j + 2 for j in range(5)], [2, 5, 8, 11, 14])
    egal("cours moyenne 60/5", Fraction(60, 5), 12)
    egal("cours fréquence 3/5", Fraction(3, 5), Fraction(6, 10))
    # suite u_{n+1} = 0,5 u_n + 2 : valeurs citées et figure (u_0 … u_8)
    v = [Fraction(1)]
    for _ in range(8):
        v.append(v[-1] / 2 + 2)
    egal("cours u_1…u_4", [float(t) for t in v[1:5]], [2.5, 3.25, 3.625, 3.8125])
    egal("cours somme u_0…u_4", float(sum(v[:5])), 14.1875)
    egal("figure suite_nuage", F.U_NUAGE, [float(t) for t in v])
    egal("cours suite croissante, < 4", all(v[j] < v[j + 1] < 4 for j in range(8)), True)
    # tableau de valeurs de x² − 2x
    egal("cours tableau f(x) = x² - 2x", [t * t - 2 * t for t in range(-2, 5)], [8, 3, 0, -1, 0, 3, 8])
    egal("cours pas 0,5 sur [-2 ; 4]", [-2 + 0.5 * j for j in range(13)][-1], 4.0)
    # simulation du dé
    R, E = F.simulation_de()
    egal("cours effectifs", E, [160, 166, 165, 163, 183, 163])
    egal("cours fréquence de 6", E[5] / 1000, 0.163)
    egal("cours moyenne des faces", sum(R) / 1000, 3.532)
    egal("cours 1/6 arrondi", round(1 / 6, 3), 0.167)
    egal("cours moyenne théorique", Fraction(sum(range(1, 7)), 6), Fraction(7, 2))
    # sécantes de x² en 1
    taux = sp.simplify(((1 + h) ** 2 - 1) / h)
    egal("cours taux de x² en 1", sp.expand(taux), 2 + h)
    egal("cours f'(1)", sp.diff(x ** 2, x).subs(x, 1), 2)

    # ---- exercice 1063
    T = [14, 17, 12, 19, 16, 11, 15]
    egal("1063 len", len(T), 7)
    egal("1063 Q2", (T[0], T[3], T[-1], T[len(T) - 2]), (14, 19, 15, 11))
    egal("1063 indice du min", T.index(min(T)), 5)
    egal("1063 T[7]", erreur(lambda: T[7]), "IndexError: list index out of range")

    # ---- exercice 1065
    egal("1065 multiples de 5", [j for j in range(31) if j % 5 == 0], [0, 5, 10, 15, 20, 25, 30])
    egal("1065 v", F.suite_recurrente(2, 4, lambda t: 3 * t - 2), [2, 4, 10, 28, 82])

    # ---- exercice 1064
    etats = F.ex1064_liste()
    egal("1064 états (figure)", etats[-1], [3, 3, 5, 9, 15])
    egal("1064 valeurs ajoutées", [e[-1] for e in etats[1:]], [3, 5, 9, 15])
    egal("1064 L[-1] avant", [e[-1] for e in etats[:-1]], [3, 3, 5, 9])
    egal("1064 u_10 par la formule", 3 + 2 * sum(range(10)), 93)

    # ---- exercice 1067
    P = [12, 0, 5, 23, 0, 8, 17, 0, 3, 9]
    egal("1067 total", 12 + 0 + 5 + 23 + 0 + 8 + 17 + 0 + 3 + 9, 77)
    egal("1067 jours > 10", [i + 1 for i in range(10) if P[i] > 10], [1, 4, 7])

    # ---- exercice 1066
    U = F.U_1066
    egal("1066 termes", U, [5, 7, 11, 19, 35, 67])
    egal("1066 formule explicite", all(U[j] == 2 ** (j + 1) + 3 for j in range(6)), True)
    egal("1066 récurrence ⇔ formule", sp.simplify(2 * (2 ** (m + 1) + 3) - 3 - (2 ** (m + 2) + 3)), 0)
    egal("1066 somme", sum(U), 144)
    egal("1066 croissante", all(U[j] < U[j + 1] for j in range(5)), True)

    # ---- exercice nouveau-1
    egal("n1 X", F.X_N1, [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
    egal("n1 Y", F.Y_N1, [3.0, 1.25, 0.0, -0.75, -1.0, -0.75, 0.0, 1.25, 3.0])
    egal("n1 f(0,5) et f(1,5)", (F.f_n1(0.5), F.f_n1(1.5)), (1.25, -0.75))
    egal("n1 forme canonique", sp.expand((x - 2) ** 2 - 1), x ** 2 - 4 * x + 3)

    # ---- exercice nouveau-2
    S, E2 = F.simulation_deux_des()
    egal("n2 longueur", len(S), 1000)
    egal("n2 effectif de 7", E2[5], 172)
    egal("n2 moyenne", sum(S) / len(S), 7.008)
    egal("n2 P(S = 7)", Fraction(sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 7), 36),
         Fraction(1, 6))
    egal("n2 probabilités de la figure", F.P_2DES,
         [sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == s) / 36 for s in range(2, 13)])
    egal("n2 E[7] = somme 9", E2[7], sum(1 for t in S if t == 9))

    # ---- exercice nouveau-3
    g = x ** 2 - 3 * x
    egal("n3 g(2)", g.subs(x, 2), -2)
    egal("n3 g(2 + h)", sp.expand(g.subs(x, 2 + h)), h ** 2 + h - 2)
    egal("n3 taux", sp.simplify((g.subs(x, 2 + h) - g.subs(x, 2)) / h), h + 1)
    egal("n3 g'(2)", sp.diff(g, x).subs(x, 2), 1)
    egal("n3 tangente", sp.expand(sp.diff(g, x).subs(x, 2) * (x - 2) + g.subs(x, 2)), x - 4)
    egal("n3 M1, M2 sur la courbe", (g.subs(x, 3), g.subs(x, sp.Rational(5, 2))), (0, sp.Rational(-5, 4)))

    # ---- exercice nouveau-4
    un = m ** 2 - 7 * m + 1
    egal("n4 u_{n+1} - u_n", sp.expand(un.subs(m, m + 1) - un), 2 * m - 6)
    egal("n4 figure", F.U_N4, [j * j - 7 * j + 1 for j in range(9)])
    egal("n4 u_3, u_4, u_7", (F.U_N4[3], F.U_N4[4], F.U_N4[7]), (-11, -11, 1))
    egal("n4 IndexError avec range(len(U))",
         erreur(lambda: [F.U_N4[i + 1] - F.U_N4[i] for i in range(8)]) is None, True)  # U a 9 termes ici
    Uc = F.U_N4[:8]
    egal("n4 range(len(U)) sur 8 termes", erreur(lambda: [Uc[i + 1] - Uc[i] for i in range(len(Uc))]),
         "IndexError: list index out of range")

    # ---- exercice 4948 : attention ajoutée le 2026-11-03 (taux(0))
    def g4948(t):
        return t**2 - 3 * t
    egal("4948 taux(0)", erreur(lambda: (g4948(2 + 0) - g4948(2)) / 0), "ZeroDivisionError: division by zero")

    # ================= enrichissement du 2026-11-03
    # ---- nouveau-1 (figures exn5) : série de notes
    Xn, Nn, Ln = F.X_N5, F.N_N5, F.L_N5
    egal("E1 listes", (Xn, Nn), ([8, 10, 12, 14, 16], [1, 4, 7, 5, 3]))
    egal("E1 X[2], N[2]", (Xn[2], Nn[2]), (12, 7))
    egal("E1 effectif total", sum(Nn), 20)
    egal("E1 L", Ln, [8] + [10] * 4 + [12] * 7 + [14] * 5 + [16] * 3)
    egal("E1 L[0], L[4], L[5], L[-1]", (Ln[0], Ln[4], Ln[5], Ln[-1]), (8, 10, 12, 16))
    egal("E1 indices des blocs", [Ln.index(v) for v in Xn], [0, 1, 5, 12, 17])
    egal("E1 L croissante", all(Ln[j] <= Ln[j + 1] for j in range(19)), True)
    egal("E1 médiane", sp.Rational(Ln[9] + Ln[10], 2), 12)
    mq = sp.Rational(sum(a * b for a, b in zip(Xn, Nn)), sum(Nn))
    egal("E1 somme pondérée", sum(a * b for a, b in zip(Xn, Nn)), 250)
    egal("E1 moyenne", mq, sp.Rational(25, 2))
    egal("E1 moyenne via L", sum(Ln) / len(Ln), 12.5)
    ecarts = [a - mq for a in Xn]
    egal("E1 écarts", ecarts, [sp.Rational(v, 2) for v in (-9, -5, -1, 3, 7)])
    egal("E1 carrés", [e**2 for e in ecarts], [sp.Rational(v, 4) for v in (81, 25, 1, 9, 49)])
    egal("E1 20V", sum(b * e**2 for b, e in zip(Nn, ecarts)), 95)
    Vq = sp.Rational(95, 20)
    egal("E1 V = E(X²) - m²", sp.Rational(sum(b * a * a for a, b in zip(Xn, Nn)), 20) - mq**2, Vq)
    egal("E1 s arrondi", round(float(sp.sqrt(Vq)), 2), 2.18)
    egal("E1 2s arrondi", round(float(2 * sp.sqrt(Vq)), 2), 4.36)
    egal("E1 bornes", (round(F.BORNES_N5[0], 2), round(F.BORNES_N5[1], 2)), (8.14, 16.86))
    egal("E1 bornes (sympy)", (round(float(mq - 2 * sp.sqrt(Vq)), 2), round(float(mq + 2 * sp.sqrt(Vq)), 2)),
         (8.14, 16.86))
    dans = [v for v in Ln if mq - 2 * sp.sqrt(Vq) <= v <= mq + 2 * sp.sqrt(Vq)]
    egal("E1 notes dans l'intervalle", (len(dans), sp.Rational(len(dans), 20)), (19, sp.Rational(19, 20)))
    egal("E1 seule la note 8 est dehors", sorted(set(Ln) - set(dans)), [8])
    egal("E1 parenthèses : X[i] - m**2 ≠ (X[i] - m)**2", 8 - 12.5**2 != (8 - 12.5)**2, True)

    # ---- nouveau-2 (figure exn6) : Syracuse
    vol = F.vol_syracuse
    egal("E2 vol(6)", vol(6), [6, 3, 10, 5, 16, 8, 4, 2, 1])
    egal("E2 vol(6) temps, altitude", (len(vol(6)) - 1, max(vol(6))), (8, 16))
    egal("E2 vol(7)", vol(7), [7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1])
    egal("E2 vol(7) : 17 termes, 16 étapes, 52 au rang 5",
         (len(vol(7)), len(vol(7)) - 1, max(vol(7)), vol(7).index(52)), (17, 16, 52, 5))
    egal("E2 figure = vol(7)", F.VOL7, vol(7))

    def vol_decimal(N):
        L = [N]
        while L[-1] != 1:
            u = L[-1]
            L.append(u / 2 if u % 2 == 0 else 3 * u + 1)
        return L
    egal("E2 avec u / 2 : décimaux", vol_decimal(6)[:3], [6, 3.0, 10.0])
    egal("E2 avec u / 2 : affichage", repr(vol_decimal(6)[:3]), "[6, 3.0, 10.0]")
    T10 = [len(vol(j)) - 1 for j in range(1, 11)]
    egal("E2 T (1 à 10)", T10, [0, 1, 7, 2, 5, 8, 16, 3, 19, 6])
    T30 = [len(vol(j)) - 1 for j in range(1, 31)]
    egal("E2 max 1 à 30", (T30.index(max(T30)) + 1, max(T30), max(vol(27))), (27, 111, 9232))
    egal("E2 autres temps de vol < 25", max(t for j, t in enumerate(T30) if j != 26) < 25, True)

    # ---- nouveau-3 (figure exn7) : deux placements
    nn = sp.symbols("n", integer=True, nonnegative=True)
    q = sp.Rational(104, 100)
    an = 1000 + 60 * nn
    bn = 1000 * q**nn
    egal("E3 a1, a2, b1, b2", (an.subs(nn, 1), an.subs(nn, 2), bn.subs(nn, 1), bn.subs(nn, 2)),
         (1060, 1120, 1040, sp.Rational(54080, 50)))
    egal("E3 b2 = 1081,6", bn.subs(nn, 2), sp.Rational(10816, 10))
    egal("E3 a_{n+1} - a_n", sp.simplify(an.subs(nn, nn + 1) - an), 60)
    egal("E3 b_{n+1} / b_n", sp.simplify(bn.subs(nn, nn + 1) / bn), q)
    egal("E3 a10, b10", (an.subs(nn, 10), round(float(bn.subs(nn, 10)), 2)), (1600, 1480.24))
    egal("E3 listes (figure)", (F.A_N7, len(F.B_N7)), ([1000 + 60 * j for j in range(31)], 31))
    egal("E3 récurrence = explicite", all(abs(F.B_N7[j] - 1000 * 1.04**j) < 1e-9 for j in range(31)), True)
    egal("E3 B[10] arrondi", round(F.B_N7[10], 2), 1480.24)
    egal("E3 premier n tel que b_n > a_n (exact)",
         next(j for j in range(31) if bn.subs(nn, j) > an.subs(nn, j)), 21)
    egal("E3 b_n < a_n pour 1 ≤ n ≤ 20, b_n > a_n pour 21 ≤ n ≤ 30",
         all(bn.subs(nn, j) < an.subs(nn, j) for j in range(1, 21))
         and all(bn.subs(nn, j) > an.subs(nn, j) for j in range(21, 31)), True)
    egal("E3 a20, b20, a21, b21",
         (an.subs(nn, 20), round(float(bn.subs(nn, 20)), 2), an.subs(nn, 21), round(float(bn.subs(nn, 21)), 2)),
         (2200, 2191.12, 2260, 2278.77))
    egal("E3 B[0] < A[0] faux (erreur fréquente)", F.B_N7[0] < F.A_N7[0], False)
    egal("E3 b_{n+1} - b_n", sp.simplify(bn.subs(nn, nn + 1) - bn - 40 * q**nn), 0)
    egal("E3 I[10], I[11]", (round(float(40 * q**10), 2), round(float(40 * q**11), 2)), (59.21, 61.58))
    egal("E3 premier k tel que I[k] > 60", next(j for j in range(30) if 40 * q**j > 60), 11)
    D = [an.subs(nn, j) - bn.subs(nn, j) for j in range(31)]
    egal("E3 retard maximal au rang 11", max(range(31), key=lambda j: D[j]), 11)
    egal("E3 retard a11 - b11", round(float(D[11]), 2), 120.55)
    egal("E3 a11, b11", (an.subs(nn, 11), round(float(bn.subs(nn, 11)), 2)), (1660, 1539.45))
    return pb, n[0]


def main():
    problemes = []
    for nom in FICHIERS:
        ok, n_py, n_cmp = verifier_fichier(nom, problemes)
        print(f"{nom} : {ok}/{n_py} programme(s) exécuté(s) sans erreur, "
              f"dont {n_cmp} avec l'affichage annoncé comparé à l'affichage réel")
    pb, n = assertions()
    print(f"assertions : {n} contrôle(s) de valeurs")
    problemes += pb
    for p in problemes:
        print("✗", p)
    print("OK" if not problemes else f"{len(problemes)} problème(s)")
    return 1 if problemes else 0


if __name__ == "__main__":
    sys.exit(main())
