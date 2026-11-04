# -*- coding: utf-8 -*-
"""Figures du chapitre 18 (algorithmique et programmation) — 4ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig4e import _save, tableau, BLUE, ORANGE, GREEN, DARK, NEUTRAL, DIR_COURS, DIR_EXOS
from scratch4e import figure_scripts, pile, mesurer, hauteur, Tortue, U
import matplotlib.pyplot as plt
import numpy as np

C = lambda f: os.path.join(DIR_COURS, f)  # noqa: E731
X = lambda f: os.path.join(DIR_EXOS, f)   # noqa: E731
DRAP = ("hat", "quand le drapeau vert est cliqué", "evt")
STYLO = ("cmd", "stylo en position d'écriture", "sty")
EFF = ("cmd", "effacer tout", "sty")


def scripts(path, piles, titres=None, vertical=False):
    figure_scripts(path, piles, titres, sauver=_save, vertical=vertical)


def bornes(traits, marge=30, pas=50):
    xs = [p[0] for t in traits for p in t]
    ys = [p[1] for t in traits for p in t]
    arr = lambda v, f: f(v / pas) * pas  # noqa: E731
    return ((arr(min(xs) - marge, np.floor), arr(max(xs) + marge, np.ceil)),
            (arr(min(ys) - marge, np.floor), arr(max(ys) + marge, np.ceil)))


def scene(path, traits, xb, yb, pas=50, points=(), etiq=100, w=5.2, h=None, couleur=BLUE, depart=None, titre=None,
          extra=None):
    h = h or w * (yb[1] - yb[0]) / (xb[1] - xb[0])
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor("white")
    ax.add_patch(plt.Rectangle((xb[0], yb[0]), xb[1] - xb[0], yb[1] - yb[0], facecolor="#fbfcfc", edgecolor=NEUTRAL,
                               lw=1.2, zorder=0))
    for x in np.arange(np.ceil(xb[0] / pas) * pas, xb[1] + 1e-9, pas):
        ax.plot([x, x], yb, lw=0.6, color="#d5d8dc", zorder=0)
    for y in np.arange(np.ceil(yb[0] / pas) * pas, yb[1] + 1e-9, pas):
        ax.plot(xb, [y, y], lw=0.6, color="#d5d8dc", zorder=0)
    if xb[0] < 0 < xb[1]:
        ax.plot([0, 0], yb, lw=1.1, color=NEUTRAL, zorder=1)
    if yb[0] < 0 < yb[1]:
        ax.plot(xb, [0, 0], lw=1.1, color=NEUTRAL, zorder=1)
    for x in np.arange(np.ceil(xb[0] / etiq) * etiq, xb[1] + 1e-9, etiq):
        ax.text(x, yb[0] - 0.015 * (yb[1] - yb[0]), f"{x + 0.0:g}".replace("-", "−"), fontsize=8.5, ha="center",
                va="top", color=NEUTRAL)
    for y in np.arange(np.ceil(yb[0] / etiq) * etiq, yb[1] + 1e-9, etiq):
        ax.text(xb[0] - 0.012 * (xb[1] - xb[0]), y, f"{y + 0.0:g}".replace("-", "−"), fontsize=8.5, ha="right",
                va="center", color=NEUTRAL)
    for (a, b) in traits:
        ax.plot([a[0], b[0]], [a[1], b[1]], lw=3, color=couleur, solid_capstyle="round", zorder=3)
    for (x, y), n, d in points:
        ax.scatter([x], [y], s=30, color=DARK, zorder=5)
        ax.annotate(n, (x, y), textcoords="offset points", xytext=d, fontsize=10.5, color=DARK, fontweight="bold",
                    ha="center", va="center")
    if depart is not None:
        ax.scatter([depart[0]], [depart[1]], s=110, marker="o", facecolor=ORANGE, edgecolor="#a04000", zorder=6)
    if titre:
        ax.text((xb[0] + xb[1]) / 2, yb[1] + 0.03 * (yb[1] - yb[0]), titre, fontsize=11.5, ha="center", va="bottom",
                color=DARK, fontweight="bold")
    if extra:
        extra(ax)
    ax.set_xlim(xb[0] - 0.02 * (xb[1] - xb[0]), xb[1] + 0.02 * (xb[1] - xb[0]))
    ax.set_ylim(yb[0] - 0.08 * (yb[1] - yb[0]), yb[1] + 0.1 * (yb[1] - yb[0]))
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


def polygone(t, n, c):
    for _ in range(n):
        t.avancer(c)
        t.horaire(360 / n)


# ======================================================================= COURS
def categories(path):
    exemples = [("hat", "quand le drapeau vert est cliqué", "evt", "Événements : démarrer un script"),
                ("cmd", "avancer de (10) pas", "mvt", "Mouvement : déplacer le lutin"),
                ("cmd", "dire (Bonjour !) pendant (2) secondes", "app", "Apparence : parler, changer de costume"),
                ("cmd", "stylo en position d'écriture", "sty", "Stylo : dessiner"),
                ("cmd", "attendre (1) secondes", "ctrl", "Contrôle : boucles, conditions, attente"),
                ("cmd", "demander (Ton prénom ?) et attendre", "cap", "Capteurs : questions, touches, contacts"),
                ("cmd", "mettre [score] à «score + 1»", "var", "Variables et opérateurs : calculer, mémoriser")]
    W = max(mesurer([e[:3]]) for e in exemples) + 9.6
    H = sum(hauteur([e[:3]]) + 0.35 for e in exemples) + 0.4
    fig = plt.figure(figsize=(W * U, H * U))
    ax = fig.add_axes([0, 0, 1, 1])
    y = H - 0.25
    wmax = max(mesurer([e[:3]]) for e in exemples)
    for e in exemples:
        pile(ax, [e[:3]], 0.3, y)
        hb = hauteur([e[:3]])
        ax.text(wmax + 0.9, y - hb / 2 - (0.1 if e[0] == "hat" else 0), e[3], fontsize=11.5, va="center", color=DARK)
        y -= hb + 0.35
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


categories(C("prog_4e_categories.png"))

S_CARRE = [DRAP, EFF, ("cmd", "aller à x: (0) y: (0)", "mvt"), ("cmd", "s'orienter à (90)", "mvt"), STYLO,
           ("c", "répéter (4) fois", "ctrl", [("cmd", "avancer de (100) pas", "mvt"),
                                              ("cmd", "tourner ↻ de (90) degrés", "mvt")])]
scripts(C("prog_4e_boucle.png"), [S_CARRE])
t = Tortue()
t.stylo = True
polygone(t, 4, 100)
scene(C("prog_4e_boucle_dessin.png"), t.traits, (-50, 150), (-150, 50), depart=(0, 0), titre="Le lutin dessine un carré")

S_AGE = [DRAP, ("cmd", "demander (Quel âge as-tu ?) et attendre", "cap"),
         ("ce", "si ⟨réponse > 17⟩ alors", "ctrl", [("cmd", "dire (Tu es majeur.)", "app")],
          [("cmd", "dire (Tu es mineur.)", "app")])]
scripts(C("prog_4e_condition.png"), [S_AGE])
S_CALC = [DRAP, ("cmd", "demander (Choisis un nombre) et attendre", "cap"), ("cmd", "mettre [x] à {réponse}", "var"),
          ("cmd", "mettre [y] à «x * 3»", "var"), ("cmd", "mettre [y] à «y - 5»", "var"),
          ("cmd", "dire {y} pendant (2) secondes", "app")]
scripts(C("prog_4e_variables.png"), [S_CALC])

# ================================================================== DÉCOUVERTE
scripts(X("prog_4e_d1_script.png"), [S_CARRE])
scene(X("prog_4e_d1_solution.png"), t.traits, (-50, 150), (-150, 50), depart=(0, 0),
      points=[((0, 0), "(0 ; 0)", (-22, 10)), ((100, 0), "(100 ; 0)", (22, 10)), ((100, -100), "(100 ; −100)", (30, -10)),
              ((0, -100), "(0 ; −100)", (-28, -10))], titre="Un carré de côté 100")
scripts(X("prog_4e_d2_script.png"), [S_CALC])

S_SOMME = [DRAP, ("cmd", "mettre [compteur] à (0)", "var"), ("cmd", "mettre [somme] à (0)", "var"),
           ("c", "répéter (5) fois", "ctrl", [("cmd", "ajouter (1) à [compteur]", "var"),
                                              ("cmd", "ajouter {compteur} à [somme]", "var")]),
           ("cmd", "dire {somme} pendant (2) secondes", "app")]
scripts(X("prog_4e_d3_script.png"), [S_SOMME])
tableau(X("prog_4e_d3_tableau.png"),
        [["tour", "1", "2", "3", "4", "5"], ["compteur", "1", "2", "3", "4", "5"],
         ["somme", "1", "3", "6", "10", "15"]],
        larg_col=[2.4] + [1.2] * 5, vert=[(2, j) for j in range(1, 6)], titre="Suivi des variables à la fin de chaque tour")
scripts(X("prog_4e_d4_script.png"), [S_AGE])

S_TRI = [DRAP, EFF, ("cmd", "aller à x: (-100) y: (0)", "mvt"), STYLO, ("cmd", "aller à x: (0) y: (100)", "mvt"),
         ("cmd", "aller à x: (100) y: (0)", "mvt"), ("cmd", "aller à x: (-100) y: (0)", "mvt"),
         ("cmd", "relever le stylo", "sty")]
scripts(X("prog_4e_d5_script.png"), [S_TRI])
scene(X("prog_4e_d5_solution.png"), [((-100, 0), (0, 100)), ((0, 100), (100, 0)), ((100, 0), (-100, 0))],
      (-150, 150), (-50, 150), points=[((-100, 0), "A(−100 ; 0)", (0, -14)), ((100, 0), "B(100 ; 0)", (0, -14)),
                                        ((0, 100), "C(0 ; 100)", (0, 12))], titre="Le triangle ABC")

S_DOUBLE = [DRAP, ("cmd", "mettre [n] à (1)", "var"), ("cmd", "mettre [étapes] à (0)", "var"),
            ("c", "répéter jusqu'à ⟨n > 100⟩", "ctrl", [("cmd", "mettre [n] à «n * 2»", "var"),
                                                        ("cmd", "ajouter (1) à [étapes]", "var")]),
            ("cmd", "dire {n} pendant (2) secondes", "app")]
scripts(X("prog_4e_d6_script.png"), [S_DOUBLE])
tableau(X("prog_4e_d6_tableau.png"),
        [["étapes", "0", "1", "2", "3", "4", "5", "6", "7"], ["n", "1", "2", "4", "8", "16", "32", "64", "128"]],
        larg_col=[2.0] + [1.0] * 8, vert=[(1, 8)], titre="n > 100 pour la première fois : arrêt")

S_TRIEQ = [DRAP, EFF, STYLO, ("c", "répéter (3) fois", "ctrl", [("cmd", "avancer de (100) pas", "mvt"),
                                                                ("cmd", "tourner ↻ de (120) degrés", "mvt")])]
scripts(X("prog_4e_d7_script.png"), [S_TRIEQ])

# ================================================================ ENTRAÎNEMENT
S_POLY_DEF = [("hat", "définir polygone (n) (côté)", "mes"),
              ("c", "répéter {n} fois", "ctrl", [("cmd", "avancer de {côté} pas", "mvt"),
                                                 ("cmd", "tourner ↻ de «360 / n» degrés", "mvt")])]
S_POLY_MAIN = [DRAP, EFF, STYLO, ("cmd", "polygone (5) (80)", "mes")]
scripts(X("prog_4e_e1_script.png"), [S_POLY_MAIN, S_POLY_DEF], ["Programme principal", "Bloc personnalisé"])


def trois_polygones(path):
    traits = []
    departs = []
    for n, c, x0 in [(5, 80, -260), (6, 70, -80), (8, 55, 110)]:
        t = Tortue(x0, 0)
        t.stylo = True
        polygone(t, n, c)
        traits += t.traits
        departs.append((x0, n))
    xb, yb = bornes(traits, 30)
    yb = (yb[0] - 50, yb[1])
    scene(path, traits, xb, yb, pas=50, w=7.6,
          extra=lambda ax: [ax.text(x0 + 45, yb[0] + 18, f"n = {n} : {360 // n}°", ha="center", va="bottom",
                                    fontsize=11.5, color=DARK, fontweight="bold") for x0, n in departs])


trois_polygones(X("prog_4e_e1_solution.png"))

S_ETOILE = [DRAP, EFF, ("cmd", "aller à x: (-75) y: (20)", "mvt"), ("cmd", "s'orienter à (90)", "mvt"), STYLO,
            ("c", "répéter (5) fois", "ctrl", [("cmd", "avancer de (150) pas", "mvt"),
                                               ("cmd", "tourner ↻ de (144) degrés", "mvt")])]
scripts(X("prog_4e_e2_script.png"), [S_ETOILE])
t = Tortue(-75, 20)
t.stylo = True
for _ in range(5):
    t.avancer(150)
    t.horaire(144)
xb, yb = bornes(t.traits, 25)
scene(X("prog_4e_e2_solution.png"), t.traits, xb, yb, pas=50, depart=(-75, 20), titre="Une étoile à 5 branches")

S_FRISE = [DRAP, EFF, ("cmd", "aller à x: (-200) y: (0)", "mvt"), ("cmd", "s'orienter à (90)", "mvt"),
           ("c", "répéter (6) fois", "ctrl",
            [STYLO, ("c", "répéter (4) fois", "ctrl", [("cmd", "avancer de (30) pas", "mvt"),
                                                       ("cmd", "tourner ↺ de (90) degrés", "mvt")]),
             ("cmd", "relever le stylo", "sty"), ("cmd", "avancer de (60) pas", "mvt")])]
scripts(X("prog_4e_e3_script.png"), [S_FRISE])
t = Tortue(-200, 0)
for _ in range(6):
    t.stylo = True
    for _ in range(4):
        t.avancer(30)
        t.antihoraire(90)
    t.stylo = False
    t.avancer(60)
scene(X("prog_4e_e3_solution.png"), t.traits, (-220, 200), (-40, 70), pas=20, etiq=100, w=8.0, depart=(-200, 0),
      points=[((t.x, t.y), "arrivée (160 ; 0)", (0, -16))], titre="Une frise de 6 carrés")

S_A = [DRAP, ("cmd", "demander (Nombre ?) et attendre", "cap"), ("cmd", "mettre [x] à {réponse}", "var"),
       ("cmd", "mettre [r] à «(x + 3) * 2»", "var"), ("cmd", "dire {r} pendant (2) secondes", "app")]
S_B = [DRAP, ("cmd", "demander (Nombre ?) et attendre", "cap"), ("cmd", "mettre [x] à {réponse}", "var"),
       ("cmd", "mettre [r] à «2 * x + 6»", "var"), ("cmd", "dire {r} pendant (2) secondes", "app")]
scripts(X("prog_4e_e4_scripts.png"), [S_A, S_B], ["Programme A", "Programme B"])

S_DE = [DRAP, ("cmd", "mettre [succès] à (0)", "var"),
        ("c", "répéter (1000) fois", "ctrl",
         [("c", "si ⟨nombre aléatoire entre 1 et 6 = 6⟩ alors", "ctrl", [("cmd", "ajouter (1) à [succès]", "var")])]),
        ("cmd", "dire «succès / 1000» pendant (2) secondes", "app")]
scripts(X("prog_4e_e5_script.png"), [S_DE])

S_BUG = [DRAP, ("cmd", "aller à x: (0) y: (0)", "mvt"), ("cmd", "s'orienter à (90)", "mvt"),
         ("c", "répéter (4) fois", "ctrl", [("cmd", "avancer de (100) pas", "mvt"),
                                            ("cmd", "tourner ↻ de (60) degrés", "mvt")])]
scripts(X("prog_4e_e6_script.png"), [S_BUG])
t = Tortue()
t.stylo = True
for _ in range(4):
    t.avancer(100)
    t.horaire(60)
bug = t.traits
t2 = Tortue(260, 0)
t2.stylo = True
for _ in range(3):
    t2.avancer(100)
    t2.horaire(120)
scene(X("prog_4e_e6_solution.png"), bug + [((a[0], a[1]), (b[0], b[1])) for a, b in t2.traits], (-60, 420),
      (-200, 60), pas=50, w=7.4, depart=(0, 0),
      extra=lambda ax: [ax.text(290, -150, "avec 4 fois et 60° :\n4 côtés d'hexagone", ha="center", va="center",
                                fontsize=10.5, color=BLUE, fontweight="bold"),
                        ax.text(310, 30, "corrigé : 3 fois et 120°", ha="center", va="center", fontsize=10.5,
                                color=GREEN, fontweight="bold")])

S_CHAT = [DRAP, ("cmd", "dire (Bonjour !) pendant (2) secondes", "app"), ("cmd", "envoyer à tous [à toi]", "evt")]
S_CHIEN = [("hat", "quand je reçois [à toi]", "evt"), ("cmd", "dire (Salut !) pendant (2) secondes", "app"),
           ("cmd", "envoyer à tous [fin]", "evt")]
S_CHAT2 = [("hat", "quand je reçois [fin]", "evt"), ("cmd", "dire (Au revoir !) pendant (2) secondes", "app")]
scripts(X("prog_4e_e7_scripts.png"), [S_CHAT, S_CHIEN, S_CHAT2],
        ["Lutin Chat (script 1)", "Lutin Chien", "Lutin Chat (script 2)"], vertical=True)

# =================================================================== PROBLÈMES
S_MYST = [DRAP, ("cmd", "mettre [mystère] à «nombre aléatoire entre 1 et 100»", "var"),
          ("cmd", "mettre [essais] à (0)", "var"),
          ("c", "répéter jusqu'à ⟨réponse = mystère⟩", "ctrl",
           [("cmd", "demander (Propose un nombre) et attendre", "cap"), ("cmd", "ajouter (1) à [essais]", "var"),
            ("c", "si ⟨réponse < mystère⟩ alors", "ctrl", [("cmd", "dire (Trop petit !) pendant (1) secondes", "app")]),
            ("c", "si ⟨réponse > mystère⟩ alors", "ctrl", [("cmd", "dire (Trop grand !) pendant (1) secondes", "app")])]),
          ("cmd", "dire (Gagné !) pendant (2) secondes", "app")]
scripts(X("prog_4e_p1_script.png"), [S_MYST])

S_SPIR = [DRAP, EFF, ("cmd", "aller à x: (0) y: (0)", "mvt"), ("cmd", "s'orienter à (90)", "mvt"),
          ("cmd", "mettre [longueur] à (10)", "var"), STYLO,
          ("c", "répéter (10) fois", "ctrl", [("cmd", "avancer de {longueur} pas", "mvt"),
                                              ("cmd", "tourner ↺ de (90) degrés", "mvt"),
                                              ("cmd", "ajouter (10) à [longueur]", "var")])]
scripts(X("prog_4e_p2_script.png"), [S_SPIR])
t = Tortue()
t.stylo = True
L = 10
for _ in range(10):
    t.avancer(L)
    t.antihoraire(90)
    L += 10
scene(X("prog_4e_p2_solution.png"), t.traits, (-60, 70), (-60, 80), pas=10, etiq=50, w=5.4, depart=(0, 0),
      points=[((round(t.x), round(t.y)), "arrivée (50 ; 60)", (0, 12))], titre="La spirale")

S_MONNAIE = [DRAP, ("cmd", "demander (Somme à rendre en euros ?) et attendre", "cap"),
             ("cmd", "mettre [reste] à {réponse}", "var"), ("cmd", "mettre [pièces2] à (0)", "var"),
             ("c", "répéter jusqu'à ⟨reste < 2⟩", "ctrl", [("cmd", "ajouter (-2) à [reste]", "var"),
                                                           ("cmd", "ajouter (1) à [pièces2]", "var")]),
             ("cmd", "mettre [pièces1] à {reste}", "var"),
             ("cmd", "dire «regroupe pièces2 et pièces1» pendant (2) secondes", "app")]
scripts(X("prog_4e_p3_script.png"), [S_MONNAIE])

S_TEMP = [DRAP, ("cmd", "demander (Température en °C ?) et attendre", "cap"),
          ("cmd", "mettre [F] à «réponse * 1.8 + 32»", "var"), ("cmd", "dire {F} pendant (2) secondes", "app")]
scripts(X("prog_4e_p4_script.png"), [S_TEMP])

S_ROBOT = [DRAP, EFF, ("cmd", "aller à x: (0) y: (0)", "mvt"), STYLO,
           ("c", "répéter (3) fois", "ctrl", [("cmd", "ajouter (40) à x", "mvt"), ("cmd", "ajouter (30) à y", "mvt")]),
           ("c", "répéter (2) fois", "ctrl", [("cmd", "ajouter (-60) à x", "mvt")])]
scripts(X("prog_4e_p5_script.png"), [S_ROBOT])
scene(X("prog_4e_p5_solution.png"),
      [((0, 0), (40, 0)), ((40, 0), (40, 30)), ((40, 30), (80, 30)), ((80, 30), (80, 60)), ((80, 60), (120, 60)),
       ((120, 60), (120, 90)), ((120, 90), (60, 90)), ((60, 90), (0, 90))],
      (-20, 150), (-20, 110), pas=10, etiq=50, w=5.6, depart=(0, 0),
      points=[((40, 30), "(40 ; 30)", (-24, 10)), ((120, 90), "A(120 ; 90)", (0, 12)), ((0, 90), "B(0 ; 90)", (0, 12))],
      extra=lambda ax: ax.plot([0, 120], [0, 90], lw=1.6, color=GREEN, ls="--", zorder=2))

S_TAB = [DRAP, ("cmd", "mettre [x] à (-3)", "var"),
         ("c", "répéter (7) fois", "ctrl", [("cmd", "mettre [y] à «2 * x * x - 3»", "var"),
                                            ("cmd", "dire «regroupe x et y» pendant (1) secondes", "app"),
                                            ("cmd", "ajouter (1) à [x]", "var")])]
scripts(X("prog_4e_p6_script.png"), [S_TAB])
tableau(X("prog_4e_p6_tableau.png"),
        [["x", "−3", "−2", "−1", "0", "1", "2", "3"], ["y", "15", "5", "−1", "−3", "−1", "5", "15"]],
        larg_col=[1.2] + [1.1] * 7, vert=[(1, j) for j in range(1, 8)], titre="Valeurs affichées par le programme")

S_DES = [DRAP, ("cmd", "mettre [sept] à (0)", "var"),
         ("c", "répéter (1000) fois", "ctrl",
          [("cmd", "mettre [s] à «(aléatoire 1 à 6) + (aléatoire 1 à 6)»", "var"),
           ("c", "si ⟨s = 7⟩ alors", "ctrl", [("cmd", "ajouter (1) à [sept]", "var")])]),
         ("cmd", "dire «sept / 1000» pendant (2) secondes", "app")]
scripts(X("prog_4e_p7_script.png"), [S_DES])
lignes = [["+"] + [str(j) for j in range(1, 7)]] + [[str(i)] + [str(i + j) for j in range(1, 7)] for i in range(1, 7)]
tableau(X("prog_4e_p7_tableau.png"), lignes, larg_col=[1.0] * 7,
        vert=[(i, j) for i in range(1, 7) for j in range(1, 7) if i + j == 7],
        surligne=[(1, 1), (6, 6)], titre="Les 36 issues : 6 sommes égales à 7")
