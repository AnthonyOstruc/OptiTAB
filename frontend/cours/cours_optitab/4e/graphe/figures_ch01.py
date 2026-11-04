# -*- coding: utf-8 -*-
"""Figures du chapitre 1 (nombres relatifs) — 4ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig4e import (new_fig, _save, tableau, droite_graduee, thermometre, BLUE, ORANGE,
                   GREEN, DARK, NEUTRAL, GRID, DIR_COURS, DIR_EXOS)
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Ellipse

C = lambda f: os.path.join(DIR_COURS, f)  # noqa: E731
X = lambda f: os.path.join(DIR_EXOS, f)   # noqa: E731
M = "−"  # vrai signe moins typographique


# ------------------------------------------------------------------ cours
droite_graduee(C("relatifs_4e_droite.png"), -6, 6, 1,
               points=[("$-4$", -4, ORANGE), ("$4$", 4, ORANGE)],
               fleches=[(0, -4, "distance à zéro : 4", ORANGE, 0.9),
                        (0, 4, "distance à zéro : 4", ORANGE, 0.9)],
               sous="$-4$ et $4$ sont opposés : même distance à zéro, signes contraires")

tableau(C("relatifs_4e_signes.png"),
        [["×", "nombre positif", "nombre négatif"],
         ["nombre positif", "positif (+)", "négatif (−)"],
         ["nombre négatif", "négatif (−)", "positif (+)"]],
        larg_col=[2.6, 2.6, 2.6], surligne=[(2, 2)], titre="La règle des signes (× et :)")


def priorites():
    fig, ax = new_fig(10.5, 2.6)
    etapes = [("1", "Parenthèses\n(les plus intérieures d'abord)", BLUE),
              ("2", "Multiplications et divisions\nde gauche à droite", ORANGE),
              ("3", "Additions et soustractions\nde gauche à droite", GREEN)]
    for i, (n, txt, col) in enumerate(etapes):
        x = i * 3.6
        ax.add_patch(FancyBboxPatch((x, 0), 3.0, 1.5, boxstyle="round,pad=0.08",
                                    facecolor="white", edgecolor=col, lw=2.2))
        ax.text(x + 0.32, 1.18, n, fontsize=17, color=col, fontweight="bold", va="center")
        ax.text(x + 1.6, 0.68, txt, fontsize=11.5, color=DARK, ha="center", va="center")
        if i < 2:
            ax.add_patch(FancyArrowPatch((x + 3.12, 0.75), (x + 3.5, 0.75),
                                         arrowstyle="-|>", mutation_scale=16, lw=2,
                                         color=NEUTRAL))
    ax.set_xlim(-0.2, 10.4)
    ax.set_ylim(-0.2, 1.75)
    ax.axis("off")
    _save(fig, C("relatifs_4e_priorites.png"))


priorites()

# ------------------------------------------------------------------ exercices
thermometre(X("relatifs_4e_thermometres.png"),
            [("Lille  " + M + "4 °C", -4, BLUE), ("Strasbourg  " + M + "7 °C", -7, ORANGE),
             ("Brest  3 °C", 3, GREEN)], lo=-10, hi=10, pas=2,
            titre="Relevés à 6 h")

tableau(X("relatifs_4e_motif.png"),
        [["$a$", "$3$", "$2$", "$1$", "$0$", "$-1$", "$-2$", "$-3$"],
         ["$a \\times (-2)$", "$-6$", "?", "?", "?", "?", "?", "?"]],
        larg_col=[1.9] + [1.05] * 7, entete_col=False)
tableau(X("relatifs_4e_motif_solution.png"),
        [["$a$", "$3$", "$2$", "$1$", "$0$", "$-1$", "$-2$", "$-3$"],
         ["$a \\times (-2)$", "$-6$", "$-4$", "$-2$", "$0$", "$2$", "$4$", "$6$"]],
        larg_col=[1.9] + [1.05] * 7, entete_col=False,
        vert=[(1, j) for j in range(2, 8)])

tableau(X("relatifs_4e_semaine.png"),
        [["Jour", "lun.", "mar.", "mer.", "jeu.", "ven.", "sam.", "dim."],
         ["Temp. (°C)", "$-6$", "$-2$", "$1$", "$-4$", "$3$", "$-1$", "$-5$"]],
        larg_col=[2.0] + [1.05] * 7, entete_col=True)


def montagne():
    fig, ax = new_fig(8.6, 5.0)
    xs = np.array([0, 2.2, 4.2, 5.6, 7.0, 9.0])
    ys = np.array([400, 1300, 2100, 2600, 2900, 3200])
    ax.fill_between([0, 9.4], [0, 0], [400, 400], color="#eef3f6")
    ax.plot(xs, ys, lw=2.6, color=BLUE)
    ax.fill_between(xs, 0, ys, color="#e8f4fd", zorder=0)
    pts = [(0, 400, "Village : 400 m\n12 °C", (8, 8)),
           (7.0, 2900, "Refuge : 2 900 m", (-128, 4)),
           (9.0, 3200, "Sommet : 3 200 m", (-128, 8))]
    for x, y, t, off in pts:
        ax.scatter([x], [y], s=55, color=ORANGE, zorder=5)
        ax.annotate(t, (x, y), textcoords="offset points", xytext=off, fontsize=11.5,
                    color=DARK, fontweight="bold")
    ax.text(4.6, 650, "La température baisse de 0,6 °C\nchaque fois que l'on monte de 100 m",
            fontsize=11.5, color=ORANGE, ha="center",
            bbox=dict(fc="white", ec=ORANGE, boxstyle="round,pad=0.4"))
    ax.set_xlim(-0.3, 9.6)
    ax.set_ylim(0, 3700)
    ax.axis("off")
    _save(fig, X("relatifs_4e_montagne.png"))


montagne()


def sous_marin(path, solution=False):
    fig, ax = new_fig(7.4, 6.4)
    ax.axhspan(-300, 0, color="#e3f2fd", zorder=0)
    ax.axhspan(0, 140, color="#fbfdff", zorder=0)
    ax.plot([-1, 6], [0, 0], lw=2.2, color=BLUE)
    ax.text(5.9, 6, "niveau de la mer : 0 m", ha="right", va="bottom", fontsize=11,
            color=BLUE)
    for h in range(-300, 141, 50):
        if h:
            ax.plot([-0.12, 0.12], [h, h], lw=1.2, color=NEUTRAL)
            ax.text(-0.25, h, f"{h}".replace("-", M), ha="right", va="center", fontsize=10,
                    color=DARK)
    ax.plot([0, 0], [-300, 140], lw=1.4, color=NEUTRAL)
    ax.text(0, 150, "altitude (m)", ha="center", fontsize=11, color=DARK)
    # sous-marin
    ax.add_patch(Ellipse((2.0, -240), 1.5, 22, facecolor=ORANGE, edgecolor=DARK, lw=1.2))
    ax.add_patch(Polygon([(1.85, -229), (2.25, -229), (2.2, -218), (1.9, -218)], closed=True,
                         facecolor=ORANGE, edgecolor=DARK, lw=1.2))
    ax.text(3.2, -240, "sous-marin : " + M + "240 m\nmonte de 12 m/min", fontsize=11,
            color=ORANGE, va="center", fontweight="bold")
    # drone
    ax.add_patch(Polygon([(1.6, 85), (2.4, 85), (2.2, 95), (1.8, 95)], closed=True,
                         facecolor=DARK, edgecolor=DARK))
    ax.plot([1.4, 2.6], [97, 97], lw=2, color=DARK)
    ax.text(3.2, 90, "drone : 85 m\ndescend de 5 m/min", fontsize=11, color=DARK,
            va="center", fontweight="bold")
    if solution:
        ax.scatter([2.0, 2.0], [-144, 45], s=70, color=GREEN, zorder=6)
        ax.annotate("", xy=(2.0, -150), xytext=(2.0, -222),
                    arrowprops=dict(arrowstyle="-|>", lw=2, color=GREEN))
        ax.annotate("", xy=(2.0, 52), xytext=(2.0, 80),
                    arrowprops=dict(arrowstyle="-|>", lw=2, color=GREEN))
        ax.text(3.2, -144, "après 8 min : " + M + "144 m", color=GREEN, fontsize=11.5,
                va="center", fontweight="bold")
        ax.text(3.2, 45, "après 8 min : 45 m", color=GREEN, fontsize=11.5, va="center",
                fontweight="bold")
        ax.annotate("", xy=(5.6, 45), xytext=(5.6, -144),
                    arrowprops=dict(arrowstyle="<->", lw=1.8, color=GREEN))
        ax.text(5.75, -50, "écart :\n189 m", color=GREEN, fontsize=11.5,
                fontweight="bold", va="center")
    ax.set_xlim(-1.3, 6.8)
    ax.set_ylim(-310, 170)
    ax.axis("off")
    _save(fig, path)


sous_marin(X("relatifs_4e_sousmarin.png"))
sous_marin(X("relatifs_4e_sousmarin_solution.png"), solution=True)

tableau(X("relatifs_4e_carre_magique.png"),
        [["$a$", "$-4$", "$b$"], ["$-2$", "$0$", "$2$"], ["$c$", "$4$", "$-3$"]],
        larg_col=[1.3] * 3, haut=1.1, entete_col=False, entete_lig=False, fs=16,
        surligne=[(0, 0), (0, 2), (2, 0)])
tableau(X("relatifs_4e_carre_magique_solution.png"),
        [["$3$", "$-4$", "$1$"], ["$-2$", "$0$", "$2$"], ["$-1$", "$4$", "$-3$"]],
        larg_col=[1.3] * 3, haut=1.1, entete_col=False, entete_lig=False, fs=16,
        vert=[(0, 0), (0, 2), (2, 0)])


def pyramide(path, rangs, vert=(), titre=None):
    """rangs : de bas en haut ; chaque brique = produit des deux briques sous elle."""
    fig, ax = new_fig(8.0, 4.6)
    w, h = 1.8, 0.9
    n0 = len(rangs[0])
    for i, rang in enumerate(rangs):
        x0 = i * w / 2
        for j, val in enumerate(rang):
            x, y = x0 + j * w, i * h
            ok = (i, j) in vert
            ax.add_patch(Polygon([(x, y), (x + w, y), (x + w, y + h), (x, y + h)],
                                 closed=True, facecolor="#e8f5e9" if ok else
                                 ("#fdebd0" if val == "?" else "white"),
                                 edgecolor=BLUE, lw=1.6))
            ax.text(x + w / 2, y + h / 2, val, ha="center", va="center", fontsize=15,
                    color=GREEN if ok else (ORANGE if val == "?" else DARK),
                    fontweight="bold")
    if titre:
        ax.text(0, len(rangs) * h - 0.3, titre, fontsize=14, color=BLUE, fontweight="bold")
    ax.set_xlim(-0.1, n0 * w + 0.1)
    ax.set_ylim(-0.1, len(rangs) * h + 0.1)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


pyramide(X("relatifs_4e_pyramide.png"),
         [["$-2$", "$3$", "$-1$", "$4$"], ["?", "?", "?"], ["?", "?"], ["?"]],
         titre="Pyramide 1")
pyramide(X("relatifs_4e_pyramide_solution.png"),
         [["$-2$", "$3$", "$-1$", "$4$"], ["$-6$", "$-3$", "$-4$"], ["$18$", "$12$"],
          ["$216$"]],
         vert=[(1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (3, 0)], titre="Pyramide 1")
pyramide(X("relatifs_4e_pyramide2.png"),
         [["$5$", "?", "$-2$"], ["$-15$", "?"], ["?"]], titre="Pyramide 2")
pyramide(X("relatifs_4e_pyramide2_solution.png"),
         [["$5$", "$-3$", "$-2$"], ["$-15$", "$6$"], ["$-90$"]],
         vert=[(0, 1), (1, 1), (2, 0)], titre="Pyramide 2")


def profil(path, solution=False):
    fig, ax = new_fig(9.0, 4.8)
    var = [320, -150, 410, -275, -305]
    alt = [850]
    for v in var:
        alt.append(alt[-1] + v)
    xs = np.arange(len(alt)) * 2.0
    ax.plot(xs, alt, lw=2.6, color=BLUE, marker="o", ms=7, mfc=ORANGE, mec=ORANGE)
    noms = ["D", "A", "B", "C", "E", "F"]
    for i, (x, y) in enumerate(zip(xs, alt)):
        lab = f"${noms[i]}$"
        if solution or i == 0:
            lab += f"\n{y} m"
        off = [(-14, 8), (0, 10), (0, -38), (0, 10), (12, -2), (0, -38)][i]
        ax.annotate(lab, (x, y), textcoords="offset points", xytext=off,
                    ha="left" if i == 4 else ("right" if i == 0 else "center"), fontsize=11.5,
                    color=GREEN if (solution and i) else DARK, fontweight="bold")
    for i, v in enumerate(var):
        xm, ym = (xs[i] + xs[i + 1]) / 2, (alt[i] + alt[i + 1]) / 2
        s = f"+{v} m" if v > 0 else f"{M}{-v} m"
        ax.text(xm + (-0.2 if v > 0 else 0.2), ym + 45, s, fontsize=11,
                color=ORANGE, ha="right" if v > 0 else "left", va="center",
                fontweight="bold")
    ax.set_xlim(-0.8, xs[-1] + 0.8)
    ax.set_ylim(600, 1600)
    ax.axis("off")
    _save(fig, path)


profil(X("relatifs_4e_profil.png"))
profil(X("relatifs_4e_profil_solution.png"), solution=True)

droite_graduee(X("relatifs_4e_fuseaux.png"), -8, 9, 1,
               points=[("LA", -8, ORANGE), ("NY", -5, ORANGE), ("Paris", 1, BLUE),
                       ("Tokyo", 9, ORANGE)], w=10.5, h=1.8,
               sous="Décalage horaire par rapport à l'heure universelle (UTC), en heures")
droite_graduee(X("relatifs_4e_fuseaux_solution.png"), -8, 9, 1,
               points=[("LA", -8, ORANGE), ("NY", -5, ORANGE), ("Paris", 1, BLUE),
                       ("Tokyo", 9, ORANGE)], w=10.5, h=2.4,
               fleches=[(1, -5, M + "6 h", GREEN, 1.6), (1, 9, "+8 h", GREEN, 1.6)],
               sous="De Paris à New York : " + M + "6 h ; de Paris à Tokyo : +8 h")
