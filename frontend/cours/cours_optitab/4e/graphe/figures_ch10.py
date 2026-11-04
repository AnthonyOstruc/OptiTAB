# -*- coding: utf-8 -*-
"""Figures du chapitre 10 (statistiques et diagrammes) — 4ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig4e import (new_fig, _save, tableau, barres, BLUE, ORANGE, GREEN, DARK, NEUTRAL, GRID,
                   DIR_COURS, DIR_EXOS)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Rectangle, FancyBboxPatch

C = lambda f: os.path.join(DIR_COURS, f)  # noqa: E731
X = lambda f: os.path.join(DIR_EXOS, f)   # noqa: E731
PAL = [BLUE, ORANGE, GREEN, "#8e44ad", "#c0392b", "#16a085"]
LPAL = ["#d6eafc", "#fdebd0", "#e8f5e9", "#efe3f5", "#f9dcd8", "#d5f2ec"]


def camembert(path, labels, valeurs, titre=None, angles=True, w=7.6, h=5.6):
    fig, ax = new_fig(w, h)
    tot = sum(valeurs)
    a = 90.0
    for i, (lab, v) in enumerate(zip(labels, valeurs)):
        ang = 360 * v / tot
        ax.add_patch(Wedge((0, 0), 2, a - ang, a, facecolor=LPAL[i % 6], edgecolor=PAL[i % 6], lw=2))
        am = np.radians(a - ang / 2)
        txt = f"{lab}\n{ang:g}°".replace(".", ",") if angles else lab
        ax.text(2.65 * np.cos(am), 2.55 * np.sin(am), txt, ha="center", va="center", fontsize=11.5,
                color=PAL[i % 6], fontweight="bold")
        a -= ang
    if titre:
        ax.text(0, 3.35, titre, ha="center", fontsize=12.5, color=DARK, fontweight="bold")
    ax.set_xlim(-3.9, 3.9)
    ax.set_ylim(-3.1, 3.7 if titre else 3.1)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


# ------------------------------------------------------------------ cours
barres(C("statistiques_4e_batons.png"), ["0", "1", "2", "3", "4"], [4, 9, 7, 3, 2],
       ylabel="Effectif (nombre d'élèves)", w=8.0, h=4.4)
camembert(C("statistiques_4e_circulaire.png"), ["à pied", "vélo", "bus", "voiture"],
          [30, 15, 40, 15], titre="Mode de transport (angle = fréquence × 360°)")


def serie_ordonnee(path, vals, med_idx, med_txt, titre=None):
    fig, ax = new_fig(9.6, 2.4)
    n = len(vals)
    for i, v in enumerate(vals):
        hl = i in med_idx
        ax.add_patch(FancyBboxPatch((i * 1.15, 0), 0.9, 0.9, boxstyle="round,pad=0.04",
                                    facecolor="#e8f5e9" if hl else "white",
                                    edgecolor=GREEN if hl else BLUE, lw=2 if hl else 1.4))
        ax.text(i * 1.15 + 0.45, 0.45, str(v), ha="center", va="center", fontsize=14,
                color=GREEN if hl else DARK, fontweight="bold" if hl else "normal")
    ax.text((n - 1) * 1.15 / 2 + 0.45, -0.45, med_txt, ha="center", va="top", fontsize=12.5,
            color=GREEN, fontweight="bold")
    if titre:
        ax.text((n - 1) * 1.15 / 2 + 0.45, 1.3, titre, ha="center", fontsize=12, color=DARK)
    ax.set_xlim(-0.3, n * 1.15)
    ax.set_ylim(-1.2, 1.7 if titre else 1.1)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


serie_ordonnee(C("statistiques_4e_mediane.png"), [5, 7, 9, 9, 11, 12, 15], [3],
               "7 valeurs : la médiane est la 4e, soit 9", titre="Série rangée dans l'ordre croissant")
serie_ordonnee(X("statistiques_4e_mediane_solution.png"), [5, 7, 9, 9, 11, 12, 15, 20], [3, 4],
               "8 valeurs : médiane = (9 + 11) : 2 = 10")

# ------------------------------------------------------------------ exercices
tableau(X("statistiques_4e_sports.png"),
        [["Sport préféré", "football", "basket", "natation", "danse", "tennis"],
         ["Effectif", "8", "5", "4", "6", "2"]], larg_col=[2.6, 1.6, 1.4, 1.6, 1.3, 1.3])
barres(X("statistiques_4e_fratrie.png"), ["0", "1", "2", "3", "4"], [4, 9, 7, 3, 2],
       ylabel="Nombre d'élèves", w=8.0, h=4.4)
camembert(X("statistiques_4e_transport_solution.png"), ["à pied", "vélo", "bus", "voiture"],
          [30, 15, 40, 15])
tableau(X("statistiques_4e_pointures.png"),
        [["Pointure", "36", "37", "38", "39", "40"], ["Effectif", "3", "5", "8", "6", "3"]],
        larg_col=[2.0] + [1.2] * 5)


def deux_villes(path):
    jours = ["lun", "mar", "mer", "jeu", "ven", "sam", "dim"]
    A = [12, 14, 15, 13, 16, 14, 14]
    B = [6, 10, 18, 22, 20, 12, 10]
    fig, ax = new_fig(8.8, 4.6)
    x = np.arange(7)
    ax.bar(x - 0.2, A, width=0.38, color=BLUE, label="ville A", zorder=3)
    ax.bar(x + 0.2, B, width=0.38, color=ORANGE, label="ville B", zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(jours, fontsize=11.5, color=DARK)
    ax.set_ylabel("température (°C)", fontsize=12, color=DARK)
    ax.yaxis.grid(True, color=GRID, zorder=0)
    ax.legend(fontsize=11.5, frameon=False, ncol=2, loc="upper left")
    ax.set_ylim(0, 25)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for i in range(7):
        ax.text(i - 0.2, A[i] + 0.3, str(A[i]), ha="center", fontsize=9.5, color=BLUE)
        ax.text(i + 0.2, B[i] + 0.3, str(B[i]), ha="center", fontsize=9.5, color=ORANGE)
    _save(fig, path)


deux_villes(X("statistiques_4e_deux_villes.png"))
barres(X("statistiques_4e_notes.png"), ["6", "8", "10", "12", "14", "16", "18"], [2, 3, 5, 6, 4, 3, 2],
       ylabel="Nombre d'élèves", w=8.4, h=4.4)


def tableur(path):
    fig, ax = new_fig(7.4, 5.2)
    rows = [["", "A", "B"], ["1", "Jour", "Glaces vendues"], ["2", "lundi", "45"], ["3", "mardi", "52"],
            ["4", "mercredi", "38"], ["5", "jeudi", "61"], ["6", "vendredi", "70"], ["7", "samedi", "84"],
            ["8", "dimanche", "57"], ["9", "Total", "=SOMME(B2:B8)"], ["10", "Moyenne", "?"]]
    ws = [0.7, 2.4, 3.2]
    for i, r in enumerate(rows):
        x = 0
        for j, t in enumerate(r):
            head = i == 0 or j == 0
            fc = "#e6e6e6" if head else ("#fdebd0" if (i >= 9 and j == 2) else "white")
            ax.add_patch(Rectangle((x, -i * 0.5), ws[j], -0.5, facecolor=fc, edgecolor="#9e9e9e", lw=1))
            ax.text(x + (ws[j] / 2 if head else 0.1), -i * 0.5 - 0.25, t, ha="center" if head else "left",
                    va="center", fontsize=11.5, color=ORANGE if (i >= 9 and j == 2) else DARK,
                    fontweight="bold" if (i == 1 or i >= 9) and not head else "normal",
                    family="DejaVu Sans Mono" if t.startswith("=") else None)
            x += ws[j]
    ax.set_xlim(-0.1, sum(ws) + 0.1)
    ax.set_ylim(-len(rows) * 0.5 - 0.1, 0.1)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


tableur(X("statistiques_4e_tableur.png"))
barres(X("statistiques_4e_ecrans.png"), ["[0 ; 1[", "[1 ; 2[", "[2 ; 3[", "[3 ; 4[", "[4 ; 5["],
       [12, 25, 30, 18, 15], ylabel="Nombre d'élèves", w=8.4, h=4.4)
camembert(X("statistiques_4e_vacances_solution.png"), ["mer", "montagne", "campagne", "ville"],
          [86, 48, 36, 30])


def trompeur(path, honnete=False):
    fig, ax = new_fig(6.4, 4.4)
    ans, v = ["2022", "2023"], [102, 106]
    ax.bar([0, 1], v, width=0.55, color=[BLUE, ORANGE], zorder=3)
    if honnete:
        ax.set_ylim(0, 120)
    else:
        ax.set_ylim(100, 107)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(ans, fontsize=12.5)
    ax.set_ylabel("ventes (milliers d'articles)", fontsize=11.5, color=DARK)
    ax.yaxis.grid(True, color=GRID, zorder=0)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.set_title("axe commençant à 0" if honnete else "graphique publié par l'entreprise", fontsize=12,
                 color=GREEN if honnete else DARK, fontweight="bold")
    _save(fig, path)


trompeur(X("statistiques_4e_trompeur.png"))
trompeur(X("statistiques_4e_trompeur_solution.png"), honnete=True)
barres(X("statistiques_4e_pluie.png"), ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"],
       [52, 45, 48, 55, 68, 50, 35, 30, 55, 70, 80, 65], ylabel="Précipitations (mm)", w=9.0, h=4.4)


def trajets(path):
    A = [24, 25, 26, 25, 25, 24, 26, 25, 25, 25]
    B = [18, 19, 35, 20, 18, 40, 19, 18, 21, 22]
    fig, ax = new_fig(8.8, 4.4)
    x = np.arange(1, 11)
    ax.plot(x, A, lw=2.2, color=BLUE, marker="o", label="itinéraire A")
    ax.plot(x, B, lw=2.2, color=ORANGE, marker="s", label="itinéraire B")
    ax.axhline(30, color="#c0392b", lw=1.4, ls="--")
    ax.text(10.4, 30.6, "30 min", color="#c0392b", fontsize=11, ha="right")
    ax.set_xticks(x)
    ax.set_xlabel("jour", fontsize=12, color=DARK)
    ax.set_ylabel("durée du trajet (min)", fontsize=12, color=DARK)
    ax.yaxis.grid(True, color=GRID)
    ax.legend(fontsize=11, frameon=False, loc="upper left")
    ax.set_ylim(10, 45)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    _save(fig, path)


trajets(X("statistiques_4e_trajets.png"))
tableau(X("statistiques_4e_ages.png"),
        [["Âge (ans)", "12", "13", "14", "15", "16", "17"], ["Effectif", "5", "8", "10", "7", "6", "4"]],
        larg_col=[2.0] + [1.1] * 6)
