# -*- coding: utf-8 -*-
"""Vérification des contenus de la notion 253 « Sujets type brevet » (3e).

    python verif_253.py            (depuis ce dossier ; sortie : verif_log.txt)

Partie A (sujets 01 à 05, cours, fiche) :
  - chaque résultat numérique des corrigés est recalculé avec sympy ;
  - les scripts Scratch des sujets (figures/figures.py) sont traduits en Python
    et EXÉCUTÉS (module figures/scratch.py) ;
  - le barème est RELU dans exercices.txt : tableau de l'énoncé, titres des
    exercices (énoncé et corrigé), blocs « Barème » du corrigé ; total 20 =
    6 (automatismes) + 12 (exercices) + 2 (rédaction) ;
  - les valeurs tracées dans les figures sont comparées aux résultats.
Partie B (sujets 06 à 10, fonctions sujet_06 … sujet_10, même modèle) :
  - barème relu (bareme), calculs sympy, arrondis recalculés ;
  - scripts Scratch EXÉCUTÉS (S06 : répéter jusqu'à, variantes de seuil et de boucle ;
    S08 : si … alors … sinon, script corrigé) ;
  - isométries de la question de transformation (S07) testées une à une ;
  - données des tableaux de l'énoncé relues dans le texte et comparées aux figures ;
  - partie_b_figures : plus aucune ancienne image (ligne « Image: »), figures produites.
"""
import math
import re
import sys
from fractions import Fraction as Fr
from pathlib import Path

import sympy as sp

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI / "figures"))
sys.path.insert(0, str(ICI.parents[2] / "outils"))

import figures as FG  # noqa: E402
from scratch import executer  # noqa: E402

N_OK = [0]
ERREURS = []
LOG = []


def ok(cond, msg):
    if cond:
        N_OK[0] += 1
    else:
        ERREURS.append(msg)
    LOG.append(("OK  " if cond else "ERR ") + msg)


def egal(a, b, msg):
    a, b = sp.nsimplify(a) if isinstance(a, (int, Fr)) else a, b
    ok(sp.simplify(sp.sympify(a) - sp.sympify(b)) == 0, f"{msg} : {a} = {b}")


def proche(a, b, tol, msg):
    ok(abs(float(a) - float(b)) <= tol, f"{msg} : {float(a):.6g} ≈ {b}")


def arrondi(x, n):
    """Arrondi « scolaire » (demi vers le haut) de x à n décimales."""
    q = sp.Rational(10) ** n
    return sp.floor(sp.nsimplify(x) * q + sp.Rational(1, 2)) / q if not isinstance(x, float) else \
        math.floor(x * 10 ** n + .5) / 10 ** n


x, n, p, h = sp.symbols("x n p h")
pi = sp.pi
deg = sp.pi / 180


# ============================================================ texte des sujets
TEXTE = (ICI / "exercices.txt").read_text(encoding="utf-8")


def bloc(eid):
    for b in re.findall(r"^=== .*?^===[ \t]*$", TEXTE, flags=re.S | re.M):
        if re.search(rf"^Id:\s*{eid}\s*$", b, re.M):
            return b
    raise KeyError(eid)


def nombre(s):
    s = s.replace("{,}", ".").replace("$", "").replace(",", ".").strip()
    return Fr(s)


def bareme(eid):
    """Relit le barème d'un sujet au nouveau format et le contrôle."""
    b = bloc(eid)
    en = b[b.index("Énoncé:"):b.index("Étapes:")]
    et = b[b.index("Étapes:"):b.index("Solution:")]
    sol = b[b.index("Solution:"):]
    # tableau de l'énoncé
    lignes = re.findall(r"^\| (Partie 1|Exercice \d|Rédaction|\*\*Total\*\*) \|[^|]*\| ([^|]+) \|$", en, re.M)
    tab = {k: nombre(v) for k, v in lignes}
    ok(tab.get("Partie 1") == 6, f"{eid} : partie 1 sur 6 points dans le tableau")
    ok(tab.get("Rédaction") == 2, f"{eid} : rédaction sur 2 points dans le tableau")
    ex = {k: v for k, v in tab.items() if k.startswith("Exercice")}
    ok(sum(ex.values()) == 12, f"{eid} : exercices de la partie 2 = {sum(ex.values())} (attendu 12)")
    ok(tab.get("**Total**") == 20 and sum(v for k, v in tab.items() if k != "**Total**") == 20,
       f"{eid} : total du tableau = 20")
    ok(re.search(r"\(14 points, 1\sh\s40\)", en) is not None and "(6 points, 20 minutes)" in en,
       f"{eid} : titres des deux parties (6 / 14 points)")
    # titres des exercices dans l'énoncé et dans le corrigé
    t_en = {f"Exercice {a}": nombre(c) for a, c in re.findall(r"^### Exercice (\d) : .*\((\d+(?:,\d+)?) points?\)$", en, re.M)}
    t_et = {f"Exercice {a}": nombre(c) for a, c in re.findall(r"^## Exercice (\d) : .*\((\d+(?:,\d+)?) points?\)$", et, re.M)}
    ok(t_en == ex, f"{eid} : points des titres d'exercices de l'énoncé = tableau ({t_en})")
    ok(t_et == ex, f"{eid} : points des titres d'exercices du corrigé = tableau ({t_et})")
    # questions de chaque exercice (énoncé) et barème détaillé (corrigé)
    parts = re.split(r"^### Exercice (\d) : .*$", en, flags=re.M)
    nq = {}
    for k in range(1, len(parts), 2):
        corps = parts[k + 1].split("Étapes:")[0]
        nq[f"Exercice {parts[k]}"] = len(re.findall(r"^\d+\. ", corps, re.M))
    ok(len(re.findall(r"^### Question \d+$", en, re.M)) == 10, f"{eid} : 10 questions d'automatismes")
    corr = re.split(r"^## Exercice (\d) : .*$", et, flags=re.M)
    for k in range(1, len(corr), 2):
        nom = f"Exercice {corr[k]}"
        m = re.search(r"::: point Barème\n(.*?)\n:::", corr[k + 1], re.S)
        ok(m is not None, f"{eid} {nom} : bloc Barème présent")
        if not m:
            continue
        txt = m.group(1)
        if "par question" in txt:
            v = nombre(re.search(r"\$([\d{},]+)\$ point", txt).group(1))
            total = v * nq[nom]
        else:
            vals = re.findall(r"Q(\d+) : \$([\d{},]+)\$ point", txt)
            ok([int(a) for a, _ in vals] == list(range(1, nq[nom] + 1)),
               f"{eid} {nom} : une note par question ({len(vals)} pour {nq[nom]} questions)")
            total = sum(nombre(c) for _, c in vals)
        ok(total == ex[nom], f"{eid} {nom} : barème détaillé {total} = {ex[nom]}")
        nq_corr = len(re.findall(r"^## Question \d+ ", corr[k + 1], re.M))
        ok(nq_corr == nq[nom], f"{eid} {nom} : {nq_corr} questions corrigées pour {nq[nom]} posées")
    ok("## Rédaction (2 points)" in et, f"{eid} : rubrique Rédaction (2 points) dans le corrigé")
    # partie 1 : 10 questions corrigées, 10 réponses courtes
    p1 = et[:et.index("## Exercice 1")]
    ok(len(re.findall(r"^## Question \d+ ", p1, re.M)) == 10, f"{eid} : 10 automatismes corrigés")
    ok("$0{,}6$ point par question" in p1, f"{eid} : barème 0,6 × 10 = 6 de la partie 1")
    ok(len(re.findall(r"^\*\*(Partie 1|Exercice \d)\*\*$", sol, re.M)) == 1 + len(ex), f"{eid} : solution par partie")
    # indentation parasite (conversion automatique) supprimée
    ok(not re.search(r"^ {3}\*\*", b, re.M), f"{eid} : aucune ligne indentée de la conversion automatique")
    # images : les positions utilisées existent dans correspondance.json
    import json
    corresp = json.loads((ICI / "figures" / "correspondance.json").read_text(encoding="utf-8"))["exercices"][str(eid)]
    pos = sorted({int(k) for k in re.findall(r"\[IMAGE_(\d+)\]", b)})
    ok(pos == sorted(int(k) for k in corresp), f"{eid} : images appelées {pos} = correspondance")
    for k, v in corresp.items():
        ok(v["fichier"].startswith("brevet_3e_s%02d_" % (eid - 2547)), f"{eid} : nom de figure {v['fichier']}")
    return ex


# ============================================================ SUJET 01 (Id 2548)
def sujet_01():
    bareme(2548)
    # partie 1
    egal(-7 + 3 * 5, 8, "S01 P1 Q1")
    egal(Fr(2, 3) + Fr(1, 6), Fr(5, 6), "S01 P1 Q2")
    egal(sp.Rational(45, 10) * 10 ** 5, 450000, "S01 P1 Q3 (B)")
    egal(sp.expand(3 * (x - 4)), 3 * x - 12, "S01 P1 Q4")
    ok(sp.solve(5 * x + 2 - 37, x) == [7], "S01 P1 Q5 : x = 7")
    egal(sp.Rational(15, 100) * 80, 12, "S01 P1 Q6")
    egal(2 * (-2) + 1, -3, "S01 P1 Q7")
    egal(sp.Rational(25, 100) * 60, 15, "S01 P1 Q8")
    ok(sorted([11, 4, 2, 8, 5])[2] == 5, "S01 P1 Q10 : médiane 5")
    # Ex1
    ok(sp.factorint(168) == {2: 3, 3: 1, 7: 1} and sp.factorint(126) == {2: 1, 3: 2, 7: 1}, "S01 Ex1 Q1 : décompositions")
    ok(sp.gcd(168, 126) == 42 and 168 // 42 == 4 and 126 // 42 == 3, "S01 Ex1 Q2 : 42 carnets (4 + 3)")
    egal(42 * sp.Rational(45, 10) - 78, 111, "S01 Ex1 Q3 : bénéfice")
    egal(5 * sp.Rational(9, 10), sp.Rational(45, 10), "S01 Ex1 Q4 : même prix")
    # Ex2
    BC = sp.sqrt(12 ** 2 + 9 ** 2)
    egal(BC, 15, "S01 Ex2 Q1 : BC")
    egal(sp.Rational(4, 12) * 9, 3, "S01 Ex2 Q2 : AN")
    egal(sp.Rational(4, 12) * 15, 5, "S01 Ex2 Q2 : MN")
    egal(sp.Rational(12 * 9, 2), 54, "S01 Ex2 Q3 : aire ABC")
    egal(sp.Rational(4 * 3, 2), 6, "S01 Ex2 Q3 : aire AMN")
    egal(54 - 6, 48, "S01 Ex2 Q4a")
    egal(sp.Rational(1, 3) ** 2 * 54, 6, "S01 Ex2 Q4b : k² × 54")
    ok(abs(math.hypot(FG.VB[0] - FG.VC[0], FG.VB[1] - FG.VC[1]) / FG.U1 - 15) < 1e-9, "S01 figure voile : BC = 15")
    ok(abs(FG.VN[1] / FG.U1 - 3) < 1e-9 and abs(FG.VM[0] / FG.U1 - 4) < 1e-9, "S01 figure voile : AM = 4, AN = 3")
    # Ex3
    egal(18 + 7 * 4, 46, "S01 Ex3 Q1 A")
    egal(10 * 4, 40, "S01 Ex3 Q1 B")
    ok(sp.solve(18 + 7 * n - 10 * n, n) == [6], "S01 Ex3 Q3 : n = 6")
    egal(10 * 6, 60, "S01 Ex3 Q3 : 60 €")
    ok(max(k for k in range(1, 16) if 18 + 7 * k <= 90) == 10, "S01 Ex3 Q4 : 10 jours chez A")
    ok(max(k for k in range(1, 16) if 10 * k <= 90) == 9, "S01 Ex3 Q4 : 9 jours chez B")
    proche(sp.Rational(72, 7), 10.3, .05, "S01 Ex3 Q4 : 72/7")
    # Ex4
    sc = {0: 2, 1: 5, 2: 8, 3: 5}
    serie = sorted(v for v, e in sc.items() for _ in range(e))
    ok(len(serie) == 20, "S01 Ex4 : effectif 20")
    egal(sp.Rational(sum(serie), 20), sp.Rational(9, 5), "S01 Ex4 Q1 : moyenne 1,8")
    ok(serie[9] == serie[10] == 2, "S01 Ex4 Q2 : médiane 2")
    egal(Fr(3, 4) ** 2, Fr(9, 16), "S01 Ex4 Q4")
    egal(2 * Fr(3, 4) * Fr(1, 4), Fr(3, 8), "S01 Ex4 Q5")
    ok(FG.P1_S01 == {"R": Fr(3, 4), "B": Fr(1, 4)}, "S01 figure arbre : probabilités")


# ============================================================ SUJET 02 (Id 2549)
def sujet_02():
    bareme(2549)
    egal(18 - 4 * 3, 6, "S02 P1 Q1")
    egal(Fr(3, 5) / Fr(9, 10), Fr(2, 3), "S02 P1 Q2")
    egal(sp.Integer(10) ** 3 * sp.Integer(10) ** -5, sp.Integer(10) ** -2, "S02 P1 Q3 (B)")
    ok(sp.Integer(100) ** -2 != sp.Integer(10) ** -2, "S02 P1 Q3 : D différente de B")
    ok(sp.factorint(60) == {2: 2, 3: 1, 5: 1}, "S02 P1 Q4")
    egal(sp.expand((x - 7) * (x + 7)), x ** 2 - 49, "S02 P1 Q5")
    ok(sp.solve(x + 8 - 3, x) == [-5], "S02 P1 Q6")
    egal(50 * sp.Rational(112, 100), 56, "S02 P1 Q7")
    ok(sp.solve(-3 * x - 12, x) == [-4], "S02 P1 Q8")
    egal(sp.Rational(24, 10) * 1000, 2400, "S02 P1 Q9")
    egal(9 - (-2), 11, "S02 P1 Q10 (B)")
    # Ex1
    BC = sp.sqrt(4 ** 2 + sp.Rational(5, 2) ** 2)
    egal(BC ** 2, sp.Rational(89, 4), "S02 Ex1 Q1 : BC² = 22,25")
    proche(BC, 4.7170, 5e-5, "S02 Ex1 Q1 : BC")
    ok(arrondi(float(BC), 2) == 4.72, "S02 Ex1 Q1 : BC ≈ 4,72")
    ang = math.degrees(math.atan(2.5 / 4))
    proche(ang, 32.005, 5e-4, "S02 Ex1 Q2 : angle")
    ok(round(ang) == 32, "S02 Ex1 Q2 : 32°")
    A = 6 * BC
    proche(A, 28.302, 5e-4, "S02 Ex1 Q3 : aire")
    ok(arrondi(float(A), 2) == 28.30, "S02 Ex1 Q3 : 28,30")
    proche(A * sp.Rational(108, 100), 30.566, 5e-4, "S02 Ex1 Q4 : surface + 8 %")
    proche(A * sp.Rational(108, 100) / 2, 15.28, 5e-3, "S02 Ex1 Q4 : 15,28")
    ok(math.ceil(float(A * sp.Rational(108, 100) / 2)) == 16, "S02 Ex1 Q4 : 16 plaques")
    # Ex2
    V = pi * 4 ** 2 * 20
    egal(V, 320 * pi, "S02 Ex2 Q1")
    proche(V, 1005.31, 5e-3, "S02 Ex2 Q1 : 1005,31")
    ok(round(float(V)) == 1005, "S02 Ex2 Q1 : 1 005 mL")
    egal(sp.Rational(9, 10) * V, 288 * pi, "S02 Ex2 Q2 : 288π")
    proche(288 * pi, 904.78, 5e-3, "S02 Ex2 Q2 : 904,78 mL")
    proche(288 * pi / 50, 18.096, 5e-4, "S02 Ex2 Q2 : durée")
    ok(arrondi(float(288 * pi / 50), 1) == 18.1, "S02 Ex2 Q2 : 18,1 s")
    Vm = sp.Rational(3, 4) ** 3 * V
    egal(Vm, 135 * pi, "S02 Ex2 Q3 : 135π")
    egal(pi * 3 ** 2 * 15, 135 * pi, "S02 Ex2 Q3 : rayon 3, hauteur 15")
    egal(sp.Rational(3, 4) ** 3, sp.Rational(421875, 1000000), "S02 Ex2 Q3 : 0,421875")
    proche(135 * pi, 424.12, 5e-3, "S02 Ex2 Q3 : 424,12")
    ok(round(float(135 * pi)) == 424, "S02 Ex2 Q3 : 424 mL")
    # Ex3 : exécution du script Scratch
    r = executer({"Lutin": [FG.DEF_S02, FG.MAIN_S02]})
    lut = r.lutins["lutin"]
    ok(r.vars["c"] == 30, f"S02 Ex3 Q4 : c final = {r.vars['c']}")
    ok((round(lut.x, 6), round(lut.y, 6)) == (90, 0), f"S02 Ex3 Q5 : position finale ({lut.x} ; {lut.y})")
    segs = lut.segments
    ok(len(segs) == 16, f"S02 Ex3 : 16 côtés tracés ({len(segs)})")
    cotes = [round(math.hypot(b[0] - a[0], b[1] - a[1]), 6) for a, b in segs]
    ok([cotes[4 * k] for k in range(4)] == [10, 15, 20, 25], f"S02 Ex3 Q1 : côtés {sorted(set(cotes))}")
    egal(sum(cotes), 280, "S02 Ex3 Q2 : somme des périmètres (longueur tracée)")
    # distance stylo relevé = chemin total parcouru − longueur tracée (positions de l'exécution)
    pos = lut.positions
    total = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pos, pos[1:]))
    leve = round(total - sum(cotes), 6)
    egal(leve, 90, "S02 Ex3 Q3 : distance stylo relevé")
    ok(abs(lut.x - leve) < 1e-9, "S02 Ex3 Q3/Q5 : abscisse finale = distance stylo relevé")
    # Ex4
    pA, pB = Fr(3, 4), Fr(1, 4)
    egal(pA * Fr(1, 2), Fr(3, 8), "S02 Ex4 Q2 : A et rouge")
    egal(pB * Fr(1, 2), Fr(1, 8), "S02 Ex4 Q2 : B et bleue")
    egal(Fr(3, 8) + Fr(1, 8), Fr(1, 2), "S02 Ex4 Q3")
    egal(50 * 6 - 100 * 2, 100, "S02 Ex4 Q5 : bilan")
    egal(sp.Rational(100, 100), 1, "S02 Ex4 Q5 : par partie")
    ok("".join(sorted("AABA")) == "AAAB", "S02 figure roue : 3 A et 1 B")


# ============================================================ SUJET 03 (Id 2550)
def sujet_03():
    bareme(2550)
    egal((-3) * (-4) + 2, 14, "S03 P1 Q1")
    egal(Fr(3, 4) - Fr(1, 3), Fr(5, 12), "S03 P1 Q2")
    egal(sp.Integer(2) ** 3 * 2 ** 4, sp.Integer(2) ** 7, "S03 P1 Q3 (C)")
    ok(not sp.isprime(91) and 7 * 13 == 91, "S03 P1 Q4 : 91 = 7 × 13")
    egal(3 * (2 * x + 3), 6 * x + 9, "S03 P1 Q5")
    ok(sp.solve(2 * x - 5 - 9, x) == [7], "S03 P1 Q6")
    egal(40 * sp.Rational(75, 100), 30, "S03 P1 Q7")
    egal(-2 * 3 + 5, -1, "S03 P1 Q8")
    egal(80 * sp.Rational(3, 2), 120, "S03 P1 Q9")
    T1, T2 = FG.T1_S03, FG.T2_S03
    ok(all((a[0] + b[0], a[1] + b[1]) == (0, 0) for a, b in zip(T1, T2)), "S03 P1 Q10 : symétrie de centre O")
    ok(sorted(T2) != sorted((-a, b) for a, b in T1) and sorted(T2) != sorted((a, -b) for a, b in T1),
       "S03 P1 Q10 : pas une symétrie d'axe vertical ou horizontal par O")
    ok(sorted(T2) != sorted((4 - a, b) for a, b in T1), "S03 P1 Q10 : pas la symétrie d'axe (d) : x = 2")
    ok(sorted(T2) != sorted((b, -a) for a, b in T1) and sorted(T2) != sorted((-b, a) for a, b in T1),
       "S03 P1 Q10 : pas une rotation de 90°")
    # Ex1
    egal(sp.Rational(12600, 45), 280, "S03 Ex1 Q1")
    egal(sp.Rational(15, 100) * 12600, 1890, "S03 Ex1 Q2 : aide")
    egal(sp.Rational(12600 - 1890, 45), 238, "S03 Ex1 Q2 : par élève")
    egal(sp.Rational(85, 100) * 280, 238, "S03 Ex1 Q2 : 85 % de 280")
    egal(sp.Rational(238, 4), sp.Rational(595, 10), "S03 Ex1 Q3")
    egal(sp.Rational(10710, 40), sp.Rational(26775, 100), "S03 Ex1 Q4")
    egal((sp.Rational(26775, 100) - 238) / 238, sp.Rational(125, 1000), "S03 Ex1 Q4 : +12,5 %")
    # Ex2 : courbe (0,0) (2,180) (2,5;180) (4,300)
    egal(sp.Rational(180, 2), 90, "S03 Ex2 Q3")
    egal(sp.Rational(300 - 180) / (4 - sp.Rational(5, 2)), 80, "S03 Ex2 Q5")
    egal(sp.Rational(300, 4), 75, "S03 Ex2 : moyenne globale (non demandée)")
    ok("(0,0) (2,180) (2.5,180) (4,300)" in FG.FIGURES["brevet_3e_s03_trajet"], "S03 figure trajet : points")
    # Ex3
    ST = sp.Rational(96, 10) * sp.Rational(3, 2) / 2
    egal(ST, sp.Rational(72, 10), "S03 Ex3 Q2 : ST = 7,2")
    OT = sp.sqrt(sp.Rational(96, 10) ** 2 + ST ** 2)
    egal(OT, 12, "S03 Ex3 Q3 : OT = 12")
    egal(sp.Rational(96, 10) ** 2, sp.Rational(9216, 100), "S03 Ex3 Q3 : 92,16")
    egal(ST ** 2, sp.Rational(5184, 100), "S03 Ex3 Q3 : 51,84")
    OH = sp.sqrt(2 ** 2 + sp.Rational(3, 2) ** 2)
    egal(OH, sp.Rational(5, 2), "S03 Ex3 Q3 (variante) : OH = 2,5")
    egal(OH * sp.Rational(96, 10) / 2, 12, "S03 Ex3 Q3 (variante) : OT = 12")
    a = math.degrees(math.atan(7.2 / 9.6))
    proche(a, 36.87, 5e-3, "S03 Ex3 Q4")
    ok(round(a) == 37, "S03 Ex3 Q4 : 37°")
    proche(math.atan(0.75), 0.64, 5e-3, "S03 Ex3 Q4 : 0,64 rad")
    SH, SB, SO_, ST_ = FG.SH, FG.SB, FG.SO_, FG.ST_
    col = (SH[0] - SO_[0]) * (ST_[1] - SO_[1]) - (SH[1] - SO_[1]) * (ST_[0] - SO_[0])
    ok(abs(col) < 1e-9, "S03 figure statue : H sur le rayon [OT]")
    # Ex4
    act = dict(FG.ACT_S03)
    ok(sum(act.values()) == 48, "S03 Ex4 Q1 : total 48")
    egal(sp.Rational(act["Musée"], 48), sp.Rational(375, 1000), "S03 Ex4 Q2")
    egal(sp.Rational(act["Musée"], 48) * 360, 135, "S03 Ex4 Q3")
    egal(1 - sp.Rational(act["Plage"], 48), sp.Rational(5, 6), "S03 Ex4 Q4")
    egal(sp.Rational(act["Parc"] + act["Spectacle"], 48), sp.Rational(11, 24), "S03 Ex4 Q5")
    ok([e * 360 // 48 for _, e in FG.ACT_S03] == [135, 90, 75, 60], "S03 figure diagramme : angles")
    en = bloc(2550)
    ok(all(re.search(rf"\| \d \| {n_} \| \${e}\$ \|", en) for n_, e in act.items()),
       "S03 Ex4 : tableau du tableur = données de la figure")


# ============================================================ SUJET 04 (Id 2551)
def sujet_04():
    bareme(2551)
    egal(5 - 2 * (3 - 7), 13, "S04 P1 Q1")
    egal(Fr(2, 5) * Fr(15, 4), Fr(3, 2), "S04 P1 Q2")
    egal(sp.Rational(32, 10) * sp.Rational(1, 10 ** 4), sp.Rational(32, 100000), "S04 P1 Q3 (B)")
    egal(sp.expand((x + 2) * (x - 3)), x ** 2 - x - 6, "S04 P1 Q5")
    ok(sp.solve(3 * x + 4 - (x - 6), x) == [-5], "S04 P1 Q6")
    egal(64 / sp.Rational(8, 10), 80, "S04 P1 Q7")
    egal(64 * sp.Rational(12, 10), sp.Rational(768, 10), "S04 P1 Q7 : piège 76,80")
    egal((-4) ** 2, 16, "S04 P1 Q8")
    egal(sp.Rational(35, 10) * 10000, 35000, "S04 P1 Q9 (C)")
    egal(sp.Rational(8 + 12 + 10 + 14, 4), 11, "S04 P1 Q10")
    # Ex1
    egal(sp.sqrt(12 ** 2 + 9 ** 2), 15, "S04 Ex1 Q1")
    egal(sp.Rational(9 * 6, 2), 27, "S04 Ex1 Q2")
    egal(12 * 9 - 27, 81, "S04 Ex1 Q3")
    egal(sp.Rational(81, 25), sp.Rational(324, 100), "S04 Ex1 Q4 : 3,24 kg")
    ok(math.ceil(81 / 25) == 4, "S04 Ex1 Q4 : 4 sacs")
    egal(4 * sp.Rational(79, 10), sp.Rational(316, 10), "S04 Ex1 Q4 : 31,60 €")
    egal(2 * (12 + 9), 42, "S04 Ex1 Q5 : périmètre")
    ok(math.ceil(42 / 10) == 5, "S04 Ex1 Q5 : 5 rouleaux")
    # Ex2
    V = pi * sp.Rational(8, 10) ** 2 * sp.Rational(3, 2)
    egal(V, sp.Rational(96, 100) * pi, "S04 Ex2 Q1 : 0,96π")
    proche(V, 3.01593, 5e-6, "S04 Ex2 Q1 : 3,01593 m³")
    ok(round(float(V) * 1000) == 3016, "S04 Ex2 Q1 : 3 016 L")
    egal(60 * 12, 720, "S04 Ex2 Q2")
    pp = sp.solve(60 * p - 960 * pi, p)[0]
    egal(pp, 16 * pi, "S04 Ex2 Q4 : p = 16π")
    ok(arrondi(float(pp), 1) == 50.3, "S04 Ex2 Q4 : 50,3 mm")
    hh = sp.solve(pi * sp.Rational(8, 10) ** 2 * h - sp.Rational(72, 100), h)[0]
    proche(hh, 0.358, 5e-4, "S04 Ex2 Q5 : h")
    ok(round(float(hh) * 100) == 36, "S04 Ex2 Q5 : 36 cm")
    ok(abs(FG.H_EAU - float(hh)) < 1e-12, "S04 figure citerne : hauteur d'eau")
    # Ex3
    sf = 5.2 * math.sin(math.radians(35))
    gf = 5.2 * math.cos(math.radians(35))
    proche(sf, 2.9826, 5e-5, "S04 Ex3 Q2")
    ok(arrondi(sf, 2) == 2.98, "S04 Ex3 Q2 : 2,98")
    proche(gf, 4.2596, 5e-5, "S04 Ex3 Q3 : GF")
    ok(arrondi(gf, 2) == 4.26 and arrondi(2 * gf, 2) == 8.52, "S04 Ex3 Q3 : 4,26 et 8,52")
    proche(2 * gf, 8.5192, 5e-5, "S04 Ex3 Q3 : GD")
    egal(180 - 2 * 35, 110, "S04 Ex3 Q4")
    ok(abs(FG.KS[0] - FG.KF[0]) < 1e-12 and abs(FG.KD[0] - 2 * FG.KF[0]) < 1e-12, "S04 figure toit : F milieu, SF ⟂ GD")
    # Ex4 : exécution du script
    for e, att in ((5, 16), (-3, 0), (3, 0), (7, 40), (-7, 40)):
        r = executer({"Lutin": [FG.SCRIPT_S04]}, entrees=[e])
        ok(r.dits == [att], f"S04 Ex4 : script avec {e} → {r.dits} (attendu {att})")
    egal(sp.expand((x - 3) * (x + 3)), x ** 2 - 9, "S04 Ex4 Q3")
    ok(sorted(sp.solve((x - 3) * (x + 3), x)) == [-3, 3], "S04 Ex4 Q4")
    ok(sorted(sp.solve(x ** 2 - 9 - 40, x)) == [-7, 7], "S04 Ex4 Q5")


# ============================================================ SUJET 05 (Id 2552)
def sujet_05():
    bareme(2552)
    egal(-2 - (-9), 7, "S05 P1 Q1")
    egal(Fr(7, 8) * 64, 56, "S05 P1 Q2")
    egal((sp.Integer(10) ** 2) ** 3, sp.Integer(10) ** 6, "S05 P1 Q3 (B)")
    ok(sp.divisors(18) == [1, 2, 3, 6, 9, 18], "S05 P1 Q4")
    egal(x * (x + 5), x ** 2 + 5 * x, "S05 P1 Q5")
    ok(sp.solve(x / 4 - sp.Rational(5, 2), x) == [10], "S05 P1 Q6")
    egal(sp.Rational(30, 100) * 250, 75, "S05 P1 Q7")
    egal(sp.Rational(7, 2) * 2, 7, "S05 P1 Q8")
    egal(1 + sp.Rational(45, 60), sp.Rational(175, 100), "S05 P1 Q9 (B)")
    egal(sp.Rational(5, 3 + 5 + 2), sp.Rational(1, 2), "S05 P1 Q10")
    # Ex1
    A_, B_, C_ = (lambda k: 15 * k), (lambda k: 20 + 10 * k), (lambda k: 60)
    ok((A_(3), B_(3), C_(3)) == (45, 50, 60), "S05 Ex1 Q1")
    ok(sp.solve(20 + 10 * n - 15 * n, n) == [4], "S05 Ex1 Q3a : n = 4")
    ok(A_(4) == B_(4) == C_(4) == 60, "S05 Ex1 Q3b : trois formules à 60 €")
    ok((A_(7), B_(7), C_(7)) == (105, 90, 60), "S05 Ex1 Q4")
    ok(min(k for k in range(1, 30) if all(C_(j) < min(A_(j), B_(j)) for j in range(k, 30))) == 5,
       "S05 Ex1 Q5 : C strictement le moins cher à partir de 5")
    ok(all(not (C_(k) < min(A_(k), B_(k))) for k in range(1, 5)), "S05 Ex1 Q5 : pas avant 5")
    for e, att in ((7, 90), (3, 50), (0, 20)):
        r = executer({"Lutin": [FG.SCRIPT_S05]}, entrees=[e])
        ok(r.dits == [att], f"S05 Ex1 Q6 : script (case A remplie) avec {e} → {r.dits} (attendu {att})")
    # Ex2
    ok((1200 / 50, 800 / 50) == (24, 16), "S05 Ex2 Q1")
    ok((12 * 8, 24 * 16) == (96, 384), "S05 Ex2 Q2")
    egal(sp.Rational(96 * 10000, 384), 2500, "S05 Ex2 Q3")
    egal(sp.sqrt(6 ** 2 + 8 ** 2), 10, "S05 Ex2 Q4")
    a = math.degrees(math.atan(8 / 6))
    proche(a, 53.13, 5e-3, "S05 Ex2 Q5")
    ok(round(a) == 53, "S05 Ex2 Q5 : 53°")
    # Ex3
    s = FG.SPECT
    ok(s == [4200, 6800, 5400] and sum(s) == 16400, "S05 Ex3 Q1")
    proche(sp.Rational(16400, 3), 5466.67, 5e-3, "S05 Ex3 Q2")
    ok(round(16400 / 3) == 5467, "S05 Ex3 Q2 : 5 467")
    proche(sp.Rational(2600, 4200) * 100, 61.90, 5e-3, "S05 Ex3 Q3")
    ok(arrondi(2600 / 4200 * 100, 1) == 61.9, "S05 Ex3 Q3 : 61,9 %")
    proche(sp.Rational(5400, 16400) * 100, 32.93, 5e-3, "S05 Ex3 Q4")
    ok(arrondi(5400 / 16400 * 100, 1) == 32.9, "S05 Ex3 Q4 : 32,9 %")
    egal(16400 * sp.Rational(108, 100), 17712, "S05 Ex3 Q5")
    # Ex4
    egal(sp.Rational(1, 500), sp.Rational(2, 1000), "S05 Ex4 Q1")
    egal(sp.Rational(1 + 9 + 40, 500), sp.Rational(1, 10), "S05 Ex4 Q2")
    egal(1 - sp.Rational(1, 10), sp.Rational(9, 10), "S05 Ex4 Q3")
    egal(500 * 2, 1000, "S05 Ex4 Q4 : recette")
    egal(300 + 9 * 40 + 40 * 5, 860, "S05 Ex4 Q4 : lots")
    egal(1000 - 860, 140, "S05 Ex4 Q4 : bénéfice")
    pp = sp.solve(500 * p - 860 - 400, p)[0]
    egal(pp, sp.Rational(252, 100), "S05 Ex4 Q5 : p = 2,52")
    egal(500 * sp.Rational(251, 100) - 860, 395, "S05 Ex4 Q5 : à 2,51 €, 395 €")


# ============================================================ PARTIE B : outils
def enonce(eid):
    b = bloc(eid)
    return b[b.index("Énoncé:"):b.index("Étapes:")]


def etapes(eid):
    b = bloc(eid)
    return b[b.index("Étapes:"):b.index("Solution:")]


def dans(eid, morceau, msg):
    ok(morceau in bloc(eid), f"{msg} : « {morceau[:60]} » présent dans le texte")


def tri_isometries(T1, T2):
    """Liste des isométries simples (symétrie centrale O, translation, symétrie axiale,
    rotation de 90°) qui envoient l'ENSEMBLE T1 sur l'ENSEMBLE T2."""
    S1, S2 = sorted(T1), sorted(T2)
    res = []
    if sorted((-a, -b) for a, b in T1) == S2:
        res.append("symétrie centrale")
    if any(sorted((a + q[0] - p[0], b + q[1] - p[1]) for a, b in T1) == S2 for p in T1 for q in T2):
        res.append("translation")
    if sorted((-b, a) for a, b in T1) == S2:
        res.append("rotation +90")
    if sorted((b, -a) for a, b in T1) == S2:
        res.append("rotation -90")
    return res


def aire_signee(T):
    (a, b), (c, d), (e, g) = T
    return (c - a) * (g - b) - (d - b) * (e - a)


# ============================================================ SUJET 06 (Id 2553)
def script_s06(seuil, mult=2, pas=20, boucle=None):
    corps = [FG.Mettre("n", FG.Op(FG.V("n"), "*", mult)), FG.Ajouter("t", pas)]
    b = FG.Repeter(boucle, corps) if boucle else FG.JusquA(FG.Cmp(FG.V("n"), ">", seuil), corps)
    return [FG.Drapeau(), FG.Mettre("n", 5000), FG.Mettre("t", 0), b, FG.Dire(FG.V("t"))]


def sujet_06():
    bareme(2553)
    # partie 1
    egal(4 * sp.Rational(-25, 10), -10, "S06 P1 Q1")
    egal(1 - Fr(3, 7), Fr(4, 7), "S06 P1 Q2")
    egal(5 * 10 ** 3 + 2 * 10 ** 2, 5200, "S06 P1 Q3 (B)")
    ok(7 * 10 ** 5 != 5200 and 10 ** 5 != 5200 and 520 != 5200, "S06 P1 Q3 : distracteurs A, C, D faux")
    egal(sp.sqrt(9 + 16), 5, "S06 P1 Q4")
    ok(sp.sqrt(9) + sp.sqrt(16) == 7, "S06 P1 Q4 : piège √9 + √16 = 7")
    egal(sp.expand((x - 5) ** 2), x ** 2 - 10 * x + 25, "S06 P1 Q5")
    ok(sp.solve(4 * (x - 1) - 12, x) == [4], "S06 P1 Q6 : x = 4")
    egal(sp.Rational(150, 2), 75, "S06 P1 Q7")
    ok(sp.solve(3 * x - 4 - 11, x) == [5], "S06 P1 Q8 : antécédent 5")
    egal(10 ** 3, 1000, "S06 P1 Q9 (C) : 1 dm³ = 10 × 10 × 10 cm³")
    egal(1 - sp.Rational(35, 100), sp.Rational(65, 100), "S06 P1 Q10")
    # Ex1 : l'aquarium
    V = 80 * 35 * 40
    egal(V, 112000, "S06 Ex1 Q1 : 112 000 cm³")
    egal(sp.Rational(V, 1000), 112, "S06 Ex1 Q1 : 112 L")
    egal(sp.Rational(9, 10) * 112, sp.Rational(1008, 10), "S06 Ex1 Q2 : 100,8 L")
    m = sp.Rational(1008, 10) + 25 + 12
    egal(m, sp.Rational(1378, 10), "S06 Ex1 Q3 : 137,8 kg")
    ok(m < 150, "S06 Ex1 Q3 : 137,8 < 150")
    egal(80 * 35, 2800, "S06 Ex1 Q4 : aire de base")
    egal(sp.Rational(100800, 2800), 36, "S06 Ex1 Q4 : 36 cm")
    egal(sp.Rational(9, 10) * 40, 36, "S06 Ex1 Q4 : 90 % de 40 cm")
    Vb = sp.Rational(4, 3) * pi * 9 ** 3
    egal(Vb, 972 * pi, "S06 Ex1 Q5 : boule = 972π")
    proche(Vb, 3053.6, .05, "S06 Ex1 Q5 : 3 053,6 cm³")
    dh = Vb / 2800
    proche(dh, 1.09, .005, "S06 Ex1 Q5 : montée de l'eau")
    ok(arrondi(float(36 + dh), 1) == 37.1 and float(36 + dh) < 40, "S06 Ex1 Q5 : 37,1 cm < 40 cm")
    ok("$36$ cm" in FG.FIGURES["brevet_3e_s06_aquarium_corrige"], "S06 figure aquarium : eau à 36 cm")
    # Ex2 : les bactéries
    ok([5000 * 2 ** k for k in (1, 2, 3)] == [10000, 20000, 40000], "S06 Ex2 Q1")
    ok(sp.Rational(10000, 20) == 500 and sp.Rational(40000, 60) != 500, "S06 Ex2 Q2 : pas proportionnel")
    proche(sp.Rational(40000, 60), 666.7, .05, "S06 Ex2 Q2 : 666,7")
    ok(180 // 20 == 9 and 180 % 20 == 0, "S06 Ex2 Q3 : 9 périodes")
    egal(5000 * 2 ** 9, 2560000, "S06 Ex2 Q3 : 2 560 000")
    egal(sp.Rational(256, 100) * 10 ** 6, 2560000, "S06 Ex2 Q3 : 2,56 × 10⁶")
    egal(2560000 * sp.Rational(2, 10 ** 6), sp.Rational(512, 100), "S06 Ex2 Q4 : 5,12 m")
    # Ex3 : le microscope
    egal(sp.Rational(15, 1000) * 400, 6, "S06 Ex3 Q1")
    egal(sp.Rational(92, 10) / 400, sp.Rational(23, 1000), "S06 Ex3 Q2 : 0,023 mm")
    egal(sp.Rational(23, 1000) * 1000, 23, "S06 Ex3 Q2 : 23 µm")
    egal(400 ** 2, 160000, "S06 Ex3 Q3")
    egal(sp.Rational(15, 10) * sp.Rational(16, 10), sp.Rational(24, 10), "S06 Ex3 Q4 : 1,5 × 1,6")
    egal(sp.Rational(15, 10) * sp.Rational(1, 10 ** 4) * 160000, 24, "S06 Ex3 Q4 : 24 mm²")
    egal(sp.Rational(15, 1000) / 1000, sp.Rational(15, 10) / 10 ** 5, "S06 Ex3 Q5 : 1,5 × 10⁻⁵ m")
    # Ex4 : exécution des scripts
    r = executer({"Lutin": [FG.SCRIPT_S06]})
    ok(r.dits == [160] and r.vars["n"] == 1280000, f"S06 Ex4 Q3 : le lutin dit {r.dits}, n = {r.vars['n']}")
    r0 = executer({"Lutin": [script_s06(10 ** 6)]})
    ok(r0.dits == r.dits, "S06 Ex4 : la variante reconstruite redonne le script de l'énoncé")
    r1 = executer({"Lutin": [script_s06(None, boucle=1)]})
    r2 = executer({"Lutin": [script_s06(None, boucle=2)]})
    r3 = executer({"Lutin": [script_s06(None, boucle=3)]})
    ok([(r_.vars["n"], r_.vars["t"]) for r_ in (r1, r2, r3)] == [(10000, 20), (20000, 40), (40000, 60)],
       "S06 Ex4 Q2 : tableau des trois premiers passages")
    ok(5000 * 2 ** 7 <= 10 ** 6 < 5000 * 2 ** 8, "S06 Ex4 Q3 : 8 passages")
    r4 = executer({"Lutin": [script_s06(10 ** 7)]})
    ok(r4.dits == [220], f"S06 Ex4 Q4 : seuil 10 000 000 → {r4.dits}")
    ok(5000 * 2 ** 10 <= 10 ** 7 < 5000 * 2 ** 11, "S06 Ex4 Q4 : 11 passages")
    r5 = executer({"Lutin": [FG.SCRIPT_S06_TRIPLE]})
    ok(r5.dits == [150] and r5.vars["n"] == 1215000, f"S06 Ex4 Q5 : culture qui triple → {r5.dits}")
    ok(5000 * 3 ** 4 == 405000 and 5000 * 3 ** 5 == 1215000, "S06 Ex4 Q5 : 3⁴ et 3⁵")
    dans(2553, "On remplace $1000000$ par $10000000$", "S06 Ex4 Q4")


# ============================================================ SUJET 07 (Id 2554)
def sujet_07():
    bareme(2554)
    egal((-5) ** 2 - 3 ** 2, 16, "S07 P1 Q1")
    egal(Fr(5, 6) * Fr(3, 10), Fr(1, 4), "S07 P1 Q2")
    egal(sp.Rational(24, 10) * 10 ** 5 * 5 * sp.Rational(1, 100), sp.Rational(12, 10) * 10 ** 4, "S07 P1 Q3 (B)")
    ok(2025 % 9 == 0 and 2025 == 9 * 225 and 2 + 0 + 2 + 5 == 9, "S07 P1 Q4 : 2 025 = 9 × 225")
    egal(sp.expand((2 * x + 1) ** 2), 4 * x ** 2 + 4 * x + 1, "S07 P1 Q5")
    ok(sorted(sp.solve((x + 2) * (x - 5), x)) == [-2, 5], "S07 P1 Q6")
    egal(60 * sp.Rational(105, 100), 63, "S07 P1 Q7")
    egal((-3) ** 2 - 1, 8, "S07 P1 Q8")
    egal(2 * 60 + 20, 140, "S07 P1 Q9 (B)")
    T1, T2 = FG.T1_S07, FG.T2_S07
    ok(tri_isometries(T1, T2) == ["rotation +90"], f"S07 P1 Q10 : seule la rotation de +90° convient ({tri_isometries(T1, T2)})")
    ok(aire_signee(T1) * aire_signee(T2) > 0 and len({abs(T1[1][0] - T1[0][0]), abs(T1[2][1] - T1[0][1])}) == 2,
       "S07 P1 Q10 : même orientation, triangle non isocèle (pas de symétrie axiale)")
    ok(T1[1] == (4, 1) and T2[1] == (-1, 4), "S07 P1 Q10 : sommets cités dans le corrigé")
    # Ex1 : la grande roue
    ok((27 - 25, 27 + 25) == (2, 52), "S07 Ex1 Q1")
    egal(2 * pi * 25, 50 * pi, "S07 Ex1 Q2 : 50π")
    ok(round(float(50 * pi)) == 157, "S07 Ex1 Q2 : 157 m")
    ok(arrondi(float(5 * pi), 2) == 15.71, "S07 Ex1 Q3 : 15,71 m/min")
    proche(300 * pi, 942.5, .05, "S07 Ex1 Q3 : 942,5 m en 1 h")
    ok(arrondi(float(300 * pi / 1000), 2) == 0.94, "S07 Ex1 Q3 : 0,94 km/h")
    egal(sp.Rational(60, 360) * 10, sp.Rational(10, 6), "S07 Ex1 Q4 : 10/6 min")
    egal(sp.Rational(4, 6) * 60, 40, "S07 Ex1 Q4 : 1 min 40 s")
    egal(25 * sp.cos(60 * deg), sp.Rational(25, 2), "S07 Ex1 Q5 : OH = 12,5")
    egal(27 - sp.Rational(25, 2), sp.Rational(29, 2), "S07 Ex1 Q6 : 14,5 m")
    U = FG.U7
    ok(abs(FG.RM[1] - FG.RH[1]) < 1e-12 and abs(FG.RH[1] / U - 14.5) < 1e-9 and abs(FG.RO[1] / U - 27) < 1e-9,
       "S07 figure roue : MH horizontale, H à 14,5 m, O à 27 m")
    ok(abs(math.hypot(FG.RM[0] - FG.RO[0], FG.RM[1] - FG.RO[1]) / U - 25) < 1e-9, "S07 figure roue : OM = 25 m")
    ang = math.degrees(math.atan2(FG.RM[0] - FG.RO[0], FG.RO[1] - FG.RM[1]))
    proche(ang, 60, 1e-9, "S07 figure roue : angle POM")
    # Ex2 : le grand huit
    hh = -sp.Rational(1, 2) * x ** 2 + 6 * x + 2
    egal(hh.subs(x, 0), 2, "S07 Ex2 Q1")
    ok(sp.solve(sp.diff(hh, x), x) == [6] and hh.subs(x, 6) == 20, "S07 Ex2 Q2 : maximum 20 en 6")
    egal(hh.subs(x, 4), 18, "S07 Ex2 Q3 : h(4)")
    egal(hh.subs(x, 10), 12, "S07 Ex2 Q3 : h(10)")
    ok(sorted(sp.solve(hh - 18, x)) == [4, 8], "S07 Ex2 Q4 : h(t) = 18 pour t = 4 et t = 8")
    ok(all(hh.subs(x, t) > 18 for t in (sp.Rational(9, 2), 5, 6, 7, sp.Rational(15, 2)))
       and all(hh.subs(x, t) < 18 for t in (0, 3, 9, 12)), "S07 Ex2 Q5 : au-dessus de 18 m entre 4 et 8 s")
    ok("{-0.5*x^2+6*x+2}" in FG.FIGURES["brevet_3e_s07_grand_huit"], "S07 figure : bonne fonction tracée")
    dans(2554, "h(t) = -0{,}5t^2 + 6t + 2", "S07 Ex2 : fonction de l'énoncé")
    # Ex3 : les glaces
    Vc = sp.Rational(1, 3) * pi * 3 ** 2 * 12
    egal(Vc, 36 * pi, "S07 Ex3 Q1 : 36π")
    ok(round(float(Vc)) == 113, "S07 Ex3 Q1 : 113 cm³")
    Vd = sp.Rational(1, 2) * sp.Rational(4, 3) * pi * 3 ** 3
    egal(Vd, 18 * pi, "S07 Ex3 Q2 : 18π")
    ok(round(float(Vd)) == 57, "S07 Ex3 Q2 : 57 cm³")
    egal(Vc + Vd, 54 * pi, "S07 Ex3 Q3 : 54π")
    ok(round(float(54 * pi)) == 170 and round(float(Vc)) + round(float(Vd)) == 170, "S07 Ex3 Q3 : 170 cm³")
    proche(5000 / (54 * pi), 29.47, .005, "S07 Ex3 Q4 : 29,47")
    ok(math.floor(float(5000 / (54 * pi))) == 29, "S07 Ex3 Q4 : 29 cornets")
    proche(29 * 54 * pi, 4920, 1, "S07 Ex3 Q4 : 4 920 cm³")
    egal(sp.Rational(2, 3) ** 3, sp.Rational(8, 27), "S07 Ex3 Q5 : k³")
    egal(sp.Rational(8, 27) * 54 * pi, 16 * pi, "S07 Ex3 Q5 : 16π")
    egal(sp.Rational(1, 3) * pi * 2 ** 2 * 8 + sp.Rational(2, 3) * pi * 2 ** 3, 16 * pi, "S07 Ex3 Q5 : rayon 2, hauteur 8")
    proche(16 * pi, 50.3, .05, "S07 Ex3 Q5 : 50,3 cm³")
    ok(round(8 / 27 * 100) == 30, "S07 Ex3 Q5 : environ 30 %")
    # Ex4 : la pêche aux canards
    dans(2554, "| Nombre de canards | $2$ | $6$ | $12$ |", "S07 Ex4 : tableau")
    egal(Fr(2, 20), Fr(1, 10), "S07 Ex4 Q1")
    egal(Fr(2 + 6, 20), Fr(2, 5), "S07 Ex4 Q2")
    egal(1 - Fr(2, 5), Fr(12, 20), "S07 Ex4 Q3")
    ok(sp.solve(sp.Integer(8) / (20 + x) - sp.Rational(1, 4), x) == [12], "S07 Ex4 Q4 : 12 canards")
    egal(sp.Rational(129, 300), sp.Rational(43, 100), "S07 Ex4 Q5 : fréquence")
    egal(sp.Rational(2, 5) * 300, 120, "S07 Ex4 Q5 : 120 attendues")


# ============================================================ SUJET 08 (Id 2555)
def sujet_08():
    bareme(2555)
    egal(sp.Integer(12) / (-4) + 7, 4, "S08 P1 Q1")
    egal(Fr(3, 4) / Fr(3, 8), 2, "S08 P1 Q2")
    egal(sp.Integer(10) ** 5 / sp.Integer(10) ** 2, sp.Integer(10) ** 3, "S08 P1 Q3 (A)")
    ok(sp.gcd(84, 126) == 42 and sp.factorint(84) == {2: 2, 3: 1, 7: 1} and sp.factorint(126) == {2: 1, 3: 2, 7: 1},
       "S08 P1 Q4 : décompositions et PGCD 42")
    egal(sp.Rational(84, 126), sp.Rational(2, 3), "S08 P1 Q4")
    egal(sp.expand(3 * x - 2 * (x - 4)), x + 8, "S08 P1 Q5")
    ok(sp.solve(7 - 2 * x - 1, x) == [3], "S08 P1 Q6")
    egal(sp.Rational(18, 24) * 100, 75, "S08 P1 Q7")
    egal(sp.Rational(72, 10) / 3 * 5, 12, "S08 P1 Q8")
    egal(10 / sp.Rational(50, 60), 12, "S08 P1 Q9 (B)")
    egal(sp.Rational(1, 2) ** 2, sp.Rational(1, 4), "S08 P1 Q10")
    # Ex1 : le parcours
    AB, BC, CA = sp.Rational(12, 10), sp.Rational(9, 10), sp.Rational(15, 10)
    egal(CA ** 2, sp.Rational(225, 100), "S08 Ex1 Q1 : CA²")
    egal(AB ** 2 + BC ** 2, sp.Rational(225, 100), "S08 Ex1 Q1 : AB² + BC²")
    egal(AB + BC + CA, sp.Rational(36, 10), "S08 Ex1 Q2")
    egal(3 * (AB + BC + CA) / 12 * 60, 54, "S08 Ex1 Q3 : 54 min")
    ok(10 * 60 + 15 + 54 == 11 * 60 + 9, "S08 Ex1 Q4 : 11 h 09")
    a = math.degrees(math.atan(0.9 / 1.2))
    proche(a, 36.87, 5e-3, "S08 Ex1 Q5")
    ok(round(a) == 37 and abs(math.degrees(math.acos(1.2 / 1.5)) - a) < 1e-9, "S08 Ex1 Q5 : 37° (tan ou cos)")
    U = FG.U8
    ok(abs(math.dist(FG.PA, FG.PB) / U - 1.2) < 1e-9 and abs(math.dist(FG.PB, FG.PC) / U - .9) < 1e-9
       and abs(math.dist(FG.PA, FG.PC) / U - 1.5) < 1e-9, "S08 figure parcours : longueurs")
    # Ex2 : les dons
    D = sp.Rational(3, 2) * x + 8
    egal(D.subs(x, sp.Rational(108, 10)), sp.Rational(242, 10), "S08 Ex2 Q1 : 24,20 €")
    ok(sp.solve(D - 20, x) == [8], "S08 Ex2 Q3 : 8 km")
    ok(D.subs(x, 0) == 8 and sp.Rational(20, 8) != sp.Rational(242, 108), "S08 Ex2 Q4 : pas proportionnel")
    proche(sp.Rational(242, 108), 2.24, .005, "S08 Ex2 Q4 : 2,24")
    egal(245 * D.subs(x, 9), sp.Rational(52675, 10), "S08 Ex2 Q5 : 5 267,50 €")
    egal(245 * 8 + sp.Rational(3, 2) * 245 * 9, sp.Rational(52675, 10), "S08 Ex2 Q5 : 1 960 + 3 307,50")
    ok(245 * D.subs(x, 9) >= 5000, "S08 Ex2 Q5 : objectif atteint")
    ok("{1.5*x+8}" in FG.FIGURES["brevet_3e_s08_dons_corrige"], "S08 figure dons : bonne droite")
    # Ex3 : les temps
    temps = [51, 42, 58, 47, 60, 45, 53, 66, 48, 55, 50]
    dans(2555, " ; ".join(f"${v}$" for v in temps), "S08 Ex3 : série de l'énoncé")
    s = sorted(temps)
    ok(len(s) == 11 and s[5] == 51, "S08 Ex3 Q1 : médiane 51")
    ok(temps[5] == 45, "S08 Ex3 Q1 : piège (6e valeur non rangée = 45)")
    ok(sum(s[:6]) == 283 and sum(s[6:]) == 292 and sum(s) == 575, "S08 Ex3 Q2 : sommes partielles")
    ok(arrondi(575 / 11, 1) == 52.3, "S08 Ex3 Q2 : 52,3")
    ok(s[-1] - s[0] == 24, "S08 Ex3 Q3")
    ok(len([v for v in temps if v < 575 / 11]) == 6, "S08 Ex3 Q4 : 6 coureurs")
    egal(sp.Rational(108, 10) / sp.Rational(42, 60), sp.Rational(108, 7), "S08 Ex3 Q5")
    ok(arrondi(10.8 / 0.7, 1) == 15.4, "S08 Ex3 Q5 : 15,4 km/h")
    # Ex4 : exécution du script
    egal(sp.Rational(108, 10) * 60, 648, "S08 Ex4 Q1 : 10,8 × 60 = 648")
    for t, att in ((54, "Objectif manqué"), (45, "Objectif atteint !"), (60, "Objectif manqué"), (50, "Objectif atteint !")):
        r = executer({"Lutin": [FG.SCRIPT_S08]}, entrees=[t])
        ok(r.dits == [att], f"S08 Ex4 : script avec t = {t} → {r.dits}")
    ok(executer({"Lutin": [FG.SCRIPT_S08]}, entrees=[45]).vars["v"] == 14.4, "S08 Ex4 Q3 : v = 14,4")
    ok(all((648 / t > 12) == (t < 54) for t in range(1, 200)), "S08 Ex4 Q4 : objectif atteint ⇔ durée < 54 min")
    for t, att in ((54, "Objectif atteint !"), (60, "Objectif manqué"), (45, "Objectif atteint !")):
        r = executer({"Lutin": [FG.SCRIPT_S08_CORR]}, entrees=[t])
        ok(r.dits == [att], f"S08 Ex4 Q5 : script corrigé avec t = {t} → {r.dits}")


# ============================================================ SUJET 09 (Id 2556)
def sujet_09():
    bareme(2556)
    egal(2 * 3 ** 2, 18, "S09 P1 Q1")
    egal(Fr(2, 3) + Fr(3, 4), Fr(17, 12), "S09 P1 Q2")
    egal(sp.Rational(45, 10) * sp.Rational(1, 1000), sp.Rational(45, 10000), "S09 P1 Q3 (C)")
    ok(list(sp.primerange(20, 31)) == [23, 29], "S09 P1 Q4")
    egal(sp.expand((2 * x - 5) * (2 * x + 5)), 4 * x ** 2 - 25, "S09 P1 Q5")
    ok(sorted(sp.solve(x ** 2 - 49, x)) == [-7, 7], "S09 P1 Q6")
    egal(120 * sp.Rational(1, 4), 30, "S09 P1 Q7")
    ok((5 - 3, 3) == (2, 3), "S09 P1 Q8 (B) : a = 2, b = 3")
    egal(sp.Rational(5, 2) * 3, sp.Rational(15, 2), "S09 P1 Q9")
    egal(sp.Rational(4, 32), sp.Rational(1, 8), "S09 P1 Q10")
    # Ex1 : panneaux solaires
    egal(6 * sp.Rational(9, 2), 27, "S09 Ex1 Q1")
    egal(sp.Rational(9, 2) * sp.sin(30 * deg), sp.Rational(9, 4), "S09 Ex1 Q2 : RH = 2,25")
    PH = sp.Rational(9, 2) * sp.cos(30 * deg)
    proche(PH, 3.897, 5e-4, "S09 Ex1 Q3")
    ok(arrondi(float(PH), 2) == 3.90, "S09 Ex1 Q3 : 3,90 m")
    egal(PH ** 2, sp.Rational(81, 4) - sp.Rational(81, 16), "S09 Ex1 Q3 : vérification par Pythagore")
    egal(sp.Rational(81, 4) - sp.Rational(81, 16), sp.Rational(151875, 10000), "S09 Ex1 Q3 : 15,187 5")
    egal(27 * 150, 4050, "S09 Ex1 Q4 : kWh")
    egal(4050 * sp.Rational(1, 4), sp.Rational(10125, 10), "S09 Ex1 Q4 : 1 012,50 €")
    proche(9000 / 1012.5, 8.89, .005, "S09 Ex1 Q5")
    ok(8 * 1012.5 == 8100 < 9000 <= 9 * 1012.5 == 9112.5, "S09 Ex1 Q5 : 9 années")
    ok(abs(FG._ph9 - 4.5 * math.cos(math.radians(30))) < 1e-12, "S09 figure toit : PH")
    # Ex2 : deux offres
    A = sp.Rational(22, 100) * x + 12
    B = sp.Rational(19, 100) * x + 18
    ok((A.subs(x, 300), B.subs(x, 300)) == (78, 75), "S09 Ex2 Q1")
    ok(sp.solve(A - B, x) == [200] and A.subs(x, 200) == B.subs(x, 200) == 56, "S09 Ex2 Q3 : 200 kWh, 56 €")
    ok((A.subs(x, 150), B.subs(x, 150)) == (45, sp.Rational(93, 2)), "S09 Ex2 Q4 : 45 € et 46,50 €")
    ok(all(A.subs(x, k) < B.subs(x, k) for k in range(0, 200, 10)) and all(A.subs(x, k) > B.subs(x, k) for k in range(210, 501, 10)),
       "S09 Ex2 Q5 : A avant 200 kWh, B après")
    f_ = FG.FIGURES["brevet_3e_s09_offres"]
    ok("{0.22*x+12}" in f_ and "{0.19*x+18}" in f_, "S09 figure offres : bonnes droites")
    # Ex3 : les combles
    egal(8 * 8 * sp.Rational(5, 2), 160, "S09 Ex3 Q1")
    egal(sp.Rational(1, 3) * 8 ** 2 * 3, 64, "S09 Ex3 Q2")
    egal(sp.Rational(64, 160) * 100, 40, "S09 Ex3 Q3")
    ok(round(64 / 224 * 100) == 29, "S09 Ex3 Q3 : piège 29 %")
    egal(sp.sqrt(3 ** 2 + 4 ** 2), 5, "S09 Ex3 Q4 : SM = 5")
    egal(4 * sp.Rational(8 * 5, 2), 80, "S09 Ex3 Q5 : 80 m²")
    ok(math.ceil(80 / 12) == 7 and 6 * 12 < 80, "S09 Ex3 Q5 : 7 rouleaux")
    # Ex4 : le tableur
    en = enonce(2556)
    lus = {nom: int(v) for nom, v in re.findall(r"^\| \d+ \| (\w+) \| \$(\d+)\$ \|  \|$", en, re.M)}
    ok(list(lus) == FG.MOIS and list(lus.values()) == FG.CONSO, "S09 Ex4 : tableau de l'énoncé = données de la figure")
    c = FG.CONSO
    ok([sum(c[k:k + 3]) for k in (0, 3, 6, 9)] == [1120, 650, 530, 1020] and sum(c) == 3320,
       "S09 Ex4 Q2 : sommes par trimestres et 3 320 kWh")
    ok(round(3320 / 12) == 277, "S09 Ex4 Q3 : 277 kWh")
    s = sorted(c)
    ok(s[5] == 260 and s[6] == 270 and (s[5] + s[6]) / 2 == 265, "S09 Ex4 Q4 : médiane 265")
    ok(c[11] + c[0] + c[1] == 1210, "S09 Ex4 Q5 : hiver 1 210 kWh")
    ok(arrondi(1210 / 3320 * 100, 1) == 36.4, "S09 Ex4 Q5 : 36,4 %")
    egal(420 * sp.Rational(1, 4), 105, "S09 Ex4 Q1 : piège 105 €")


# ============================================================ SUJET 10 (Id 2557)
def sujet_10():
    bareme(2557)
    egal(-8 + 5 * (-2), -18, "S10 P1 Q1")
    egal(Fr(5, 12) - Fr(1, 4), Fr(1, 6), "S10 P1 Q2")
    egal(6 * sp.Integer(10) ** 4 / (3 * sp.Integer(10) ** -2), 2 * sp.Integer(10) ** 6, "S10 P1 Q3 (B)")
    ok(sp.gcd(24, 36) == 12, "S10 P1 Q4")
    egal(sp.expand(-2 * (3 * x - 5)), -6 * x + 10, "S10 P1 Q5")
    ok(sp.solve(5 * x - 3 - (2 * x + 9), x) == [4], "S10 P1 Q6")
    ok(4 * 25000 == 100000 and 100000 / 100 / 1000 == 1, "S10 P1 Q7 : 1 km")
    egal(5 - 8, -3, "S10 P1 Q8")
    egal(10 * sp.Rational(1852, 1000), sp.Rational(1852, 100), "S10 P1 Q9")
    ok(FG.T2_S10 == [(-2 * a, -2 * b) for a, b in FG.T1_S10] and FG.T1_S10[0] == (1, 1) and FG.T2_S10[0] == (-2, -2),
       "S10 P1 Q10 : homothétie de rapport -2 (sommet cité dans le corrigé)")
    ok(sorted(FG.T2_S10) != sorted((2 * a, 2 * b) for a, b in FG.T1_S10), "S10 P1 Q10 : pas le rapport 2")
    # Ex1 : le phare
    AP = 45 / math.tan(math.radians(8))
    BP = 45 / math.tan(math.radians(15))
    proche(AP, 320.19, 5e-3, "S10 Ex1 Q1")
    ok(round(AP) == 320 and round(BP) == 168, "S10 Ex1 Q1-Q2 : 320 m et 168 m")
    proche(BP, 167.94, 5e-3, "S10 Ex1 Q2")
    proche(AP - BP, 152.25, 5e-3, "S10 Ex1 Q3")
    ok(round(AP - BP) == 152, "S10 Ex1 Q3 : 152 m")
    proche((AP - BP) * 30, 4567.5, .05, "S10 Ex1 Q4 : 4 567,5 m en 1 h")
    ok(arrondi((AP - BP) * 30 / 1000, 1) == 4.6 and arrondi(152 * 30 / 1000, 1) == 4.6, "S10 Ex1 Q4 : 4,6 km/h")
    ok(arrondi((AP - BP) * 30 / 1000 / 1.852, 1) == 2.5, "S10 Ex1 Q5 : 2,5 nœuds")
    proche(4.5675 / 1.852, 2.47, .005, "S10 Ex1 Q5 : 2,47")
    dans(2557, "La figure n'est pas à l'échelle", "S10 Ex1 : angles dessinés agrandis")
    # Ex2 : la traversée
    ok((FG.LON_D, FG.LON_F) == (-40, -10) and FG.LON_F - FG.LON_D == 30, "S10 Ex2 Q1 : 40° O, 10° O, écart 30°")
    egal(2 * pi * 6371, 12742 * pi, "S10 Ex2 Q2 : périmètre")
    proche(12742 * pi, 40030.2, .05, "S10 Ex2 Q2 : 40 030,2 km")
    arc_ = sp.Rational(30, 360) * 12742 * pi
    proche(arc_, 3335.8, .05, "S10 Ex2 Q2 : arc")
    ok(round(float(arc_)) == 3336, "S10 Ex2 Q2 : 3 336 km")
    egal(8 * sp.Rational(1852, 1000), sp.Rational(14816, 1000), "S10 Ex2 Q3")
    t = float(arc_) / 14.816
    proche(t, 225.2, .05, "S10 Ex2 Q4")
    ok(round(t) == 225 and 225 == 9 * 24 + 9, "S10 Ex2 Q4 : 9 jours et 9 heures")
    Vt = sp.Rational(4, 3) * pi * 6371 ** 3
    proche(Vt / 10 ** 12, 1.0832, 5e-5, "S10 Ex2 Q5 : 1,083 2 × 10¹²")
    ok(arrondi(float(Vt / 10 ** 12), 2) == 1.08, "S10 Ex2 Q5 : 1,08 × 10¹² km³")
    # Ex3 : la voile
    egal(sp.sqrt(6 ** 2 + sp.Rational(9, 2) ** 2), sp.Rational(15, 2), "S10 Ex3 Q1 : TB = 7,5")
    egal(sp.Rational(6 * 9, 4), sp.Rational(27, 2), "S10 Ex3 Q2 : 13,5 m²")
    egal(sp.Rational(4, 6), sp.Rational(5, 1) / sp.Rational(15, 2), "S10 Ex3 Q3 : TR/TM = TS/TB")
    egal(sp.Rational(2, 3) * sp.Rational(9, 2), 3, "S10 Ex3 Q4 : RS = 3")
    egal(sp.Rational(4, 9) * sp.Rational(27, 2), 6, "S10 Ex3 Q5 : aire TRS")
    egal(sp.Rational(4 * 3, 2), 6, "S10 Ex3 Q5 : vérification TR × RS / 2")
    U = FG.U10
    T_, S_, B_, R_, M_ = FG.VT10, FG.VS10, FG.VB10, FG.VR10, FG.VM10
    col = (S_[0] - T_[0]) * (B_[1] - T_[1]) - (S_[1] - T_[1]) * (B_[0] - T_[0])
    ok(abs(col) < 1e-12 and abs(math.dist(T_, S_) / U - 5) < 1e-9 and abs(math.dist(T_, R_) / U - 4) < 1e-9
       and abs(math.dist(R_, S_) / U - 3) < 1e-9 and abs(math.dist(T_, B_) / U - 7.5) < 1e-9,
       "S10 figure voile : S sur [TB], TS = 5, TR = 4, RS = 3, TB = 7,5")
    # Ex4 : la marée (h(t) = 3,5 + 2,5 cos(30t °))
    hm = sp.Rational(7, 2) + sp.Rational(5, 2) * sp.cos(30 * x * deg)
    ok(hm.subs(x, 0) == 6 and hm.subs(x, 6) == 1 and hm.subs(x, 12) == 6, "S10 Ex4 Q1-Q2 : 6 m à 0 h, 1 m à 6 h")
    ok(all(float(hm.subs(x, k / 10)) >= 1 for k in range(0, 121)), "S10 Ex4 Q2 : minimum 1 m")
    egal(6 - 1, 5, "S10 Ex4 Q3 : marnage")
    ok(hm.subs(x, 4) == sp.Rational(9, 4) and hm.subs(x, 8) == sp.Rational(9, 4), "S10 Ex4 Q4 : 2,25 m à 4 h et à 8 h")
    ok(all(float(hm.subs(x, k / 10)) < 2.25 for k in range(41, 80)) and all(float(hm.subs(x, k / 10)) > 2.25 for k in list(range(0, 40)) + list(range(81, 121))),
       "S10 Ex4 Q4 : sous 2,25 m seulement entre 4 h et 8 h")
    ok(hm.subs(x, 3) == sp.Rational(7, 2) and 6 - sp.Rational(7, 2) == sp.Rational(5, 2), "S10 Ex4 Q5 : baisse de 2,5 m = 5 / 2")
    ok("{3.5+2.5*cos(30*x)}" in FG.FIGURES["brevet_3e_s10_marees"], "S10 figure marée : bonne courbe")


def partie_b_figures():
    """Aucune image en ligne conservée dans la notion ; figures de 06-10 présentes et bien nommées."""
    import json
    corresp = json.loads((ICI / "figures" / "correspondance.json").read_text(encoding="utf-8"))
    for eid in range(2553, 2558):
        b = bloc(eid)
        ok("Image:" not in b, f"{eid} : plus de ligne « Image: » (anciennes images matplotlib)")
        for k, v in corresp["exercices"][str(eid)].items():
            ok((ICI / "figures" / "images" / v["fichier"]).exists(), f"{eid} : figure {v['fichier']} produite")
            ok(len(v["alt"]) >= 15, f"{eid} : texte alternatif de la position {k}")
            ok(v["fichier"].replace(".png", "") in FG.FIGURES, f"{eid} : {v['fichier']} définie dans figures.py")
    meta = json.loads((ICI / "source_en_ligne" / "meta.json").read_text(encoding="utf-8"))
    for ex in meta["exercices"]:
        pos = {int(k) for k in corresp["exercices"].get(str(ex["id"]), {})}
        appel = {int(k) for k in re.findall(r"\[IMAGE_(\d+)\]", bloc(ex["id"]))}
        ok(appel <= pos, f"{ex['id']} : chaque image appelée est une figure neuve (aucune image en ligne conservée)")


# ============================================================ cours et fiche
def cours_fiche():
    c = (ICI / "cours_248.txt").read_text(encoding="utf-8")
    fi = (ICI / "fiche_168.txt").read_text(encoding="utf-8")
    ok(c.startswith("Titre: Méthode : réussir l'épreuve de mathématiques du brevet"), "cours : titre")
    ok("$6$ points, $20$ minutes" in c and re.search(r"\$14\$ points, 1\sh\s40", c) and "**$2$ points**" in c,
       "cours : format 6 / 14 dont 2")
    egal(5 - 2 * (3 - 7), 13, "cours : priorités")
    egal(Fr(3, 5) / Fr(9, 10), Fr(2, 3), "cours : division de fractions")
    egal(sp.expand((x + 2) * (x - 3)), x ** 2 - x - 6, "cours : développement")
    egal(sp.factor(x ** 2 + 5 * x), x * (x + 5), "cours : factorisation")
    egal(80 * sp.Rational(3, 2), 120, "cours : vitesse")
    egal(9 - (-2), 11, "cours : étendue")
    egal(sp.Rational(25, 10) / 4, sp.Rational(625, 1000), "cours : tan = 0,625")
    ok(round(math.degrees(math.atan(.625))) == 32, "cours : 32°")
    egal(sp.Rational(100, 12), sp.Rational(25, 3), "cours : ≈ 8 min par point (100 min / 12 points)")
    ok(abs(math.cos(math.radians(60)) - .5) < 1e-12, "cours : cos 60° = 0,5")
    ok(fi.startswith("Titre: Résumé : l'essentiel pour le jour du brevet"), "fiche : titre")
    egal(sp.expand((x + 3) ** 2), x ** 2 + 6 * x + 9, "fiche : (a + b)²")
    egal(sp.Rational(1000, 3600), sp.Rational(1, 36) * 10, "fiche : 1 m/s = 3,6 km/h")
    egal(sp.Rational(32, 10) * sp.Rational(1, 10000), sp.Rational(32, 100000), "fiche : 0,000 32")
    r = sp.symbols("r", positive=True)
    ok(sp.integrate(4 * pi * r ** 2, (r, 0, r)) == sp.Rational(4, 3) * pi * r ** 3, "fiche : volume de la boule")


if __name__ == "__main__":
    for fn in (sujet_01, sujet_02, sujet_03, sujet_04, sujet_05, sujet_06, sujet_07, sujet_08, sujet_09, sujet_10,
               partie_b_figures, cours_fiche):
        try:
            fn()
        except Exception as e:  # une erreur de script est une erreur de vérification
            ERREURS.append(f"{fn.__name__} : exception {e!r}")
            LOG.append(f"ERR {fn.__name__} : exception {e!r}")
    LOG.append("")
    LOG.append(f"{N_OK[0]} contrôle(s) réussi(s), {len(ERREURS)} erreur(s)")
    (ICI / "verif_log.txt").write_text("\n".join(LOG) + "\n", encoding="utf-8")
    for e in ERREURS:
        print("✗", e)
    print(f"{N_OK[0]} contrôle(s) réussi(s), {len(ERREURS)} erreur(s)")
    sys.exit(1 if ERREURS else 0)
