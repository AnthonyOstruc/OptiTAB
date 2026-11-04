# -*- coding: utf-8 -*-
"""Figures du chapitre 9 (relier des grandeurs, lire des graphiques) — 4ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig4e import (new_fig, _save, tableau, graphe, BLUE, ORANGE, GREEN, DARK, NEUTRAL,
                   DIR_COURS, DIR_EXOS)
import numpy as np
from matplotlib.patches import Rectangle, Polygon, Ellipse

C = lambda f: os.path.join(DIR_COURS, f)  # noqa: E731
X = lambda f: os.path.join(DIR_EXOS, f)   # noqa: E731
LBLUE, LORANGE, LGREEN = "#d6eafc", "#fdebd0", "#e8f5e9"
PURP = "#8e44ad"


def ligne(pts, col=BLUE, marker=True, lw=2.6):
    def f(ax):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, lw=lw, color=col, zorder=3)
        if marker:
            ax.scatter(xs, ys, s=30, color=col, zorder=4)
    return f


def lecture(ax, x, y, col=GREEN, x0=0, y0=0):
    ax.plot([x, x], [y0, y], lw=1.6, color=col, ls="--", zorder=2)
    ax.plot([x0, x], [y, y], lw=1.6, color=col, ls="--", zorder=2)
    ax.scatter([x], [y], s=60, color=col, zorder=6)


def combine(*fs):
    def f(ax):
        for g in fs:
            g(ax)
    return f


# ------------------------------------------------------------------ températures
TEMP = [(0, 4), (3, 2), (6, 1), (9, 6), (12, 12), (15, 14), (18, 10), (21, 7), (24, 5)]
graphe(C("graphiques_4e_temperature.png"), curves=[], extra=combine(ligne(TEMP),
       lambda ax: lecture(ax, 15, 14, ORANGE),
       lambda ax: ax.text(15.3, 14.6, "maximum : 14 °C à 15 h", color=ORANGE, fontsize=11.5,
                          fontweight="bold")),
       xb=(-1, 25.5), yb=(-1.5, 17), xt=3, yt=2, xlabel="heure (h)", ylabel="température (°C)",
       w=8.6, h=5.0)
graphe(X("graphiques_4e_temperature.png"), curves=[], extra=ligne(TEMP),
       xb=(-1, 25.5), yb=(-1.5, 17), xt=3, yt=2, xlabel="heure (h)", ylabel="température (°C)",
       w=8.6, h=5.0)
graphe(X("graphiques_4e_temperature_solution.png"), curves=[],
       extra=combine(ligne(TEMP), lambda ax: lecture(ax, 9, 6), lambda ax: lecture(ax, 11, 10, ORANGE),
                     lambda ax: lecture(ax, 18, 10, ORANGE),
                     lambda ax: ax.text(9.3, 4.6, "9 h → 6 °C", color=GREEN, fontsize=11.5,
                                        fontweight="bold"),
                     lambda ax: ax.text(19.0, 10.8, "10 °C à 11 h et à 18 h", color=ORANGE,
                                        fontsize=11.5, fontweight="bold")),
       xb=(-1, 25.5), yb=(-1.5, 17), xt=3, yt=2, xlabel="heure (h)", ylabel="température (°C)",
       w=8.6, h=5.0)


# ------------------------------------------------------------------ carré : P et A
def carre_ext(ax):
    cs = [1, 2, 3, 4, 5]
    ax.scatter(cs, [4 * c for c in cs], s=55, color=BLUE, zorder=5)
    ax.scatter(cs, [c * c for c in cs], s=55, color=ORANGE, zorder=5)
    xs = np.linspace(0, 5.3, 100)
    ax.plot(xs, 4 * xs, lw=1.6, color=BLUE, ls="--")
    ax.plot(xs, xs ** 2, lw=1.6, color=ORANGE, ls="--")
    ax.text(5.35, 21, "périmètre $P = 4c$", color=BLUE, fontsize=12, fontweight="bold", ha="right")
    ax.text(3.0, 4.0, "aire $A = c^2$", color=ORANGE, fontsize=12, fontweight="bold")
    lecture(ax, 4, 16, GREEN)
    ax.text(4.1, 13.6, "$P = A = 16$\npour $c = 4$", color=GREEN, fontsize=11.5, fontweight="bold")


graphe(C("graphiques_4e_construction.png"), curves=[], extra=carre_ext, xb=(-0.4, 5.8), yb=(-2, 27),
       xt=1, yt=2, xlabel="côté $c$ (cm)", ylabel="", w=8.2, h=5.4)
graphe(X("graphiques_4e_carre_solution.png"), curves=[], extra=carre_ext, xb=(-0.4, 5.8),
       yb=(-2, 27), xt=1, yt=2, xlabel="côté $c$ (cm)", ylabel="", w=8.2, h=5.4)

# ------------------------------------------------------------------ plante
PLANTE = [(0, 2), (1, 3), (2, 5), (3, 8), (4, 12), (5, 15), (6, 17), (7, 18), (8, 18.5)]
graphe(X("graphiques_4e_plante.png"), curves=[], extra=ligne(PLANTE, GREEN),
       xb=(-0.4, 8.8), yb=(-1.5, 21), xt=1, yt=2, xlabel="semaine", ylabel="hauteur (cm)",
       w=8.2, h=5.0)

# ------------------------------------------------------------------ baignoire
BAIN = [(0, 0), (10, 30), (12, 30), (12, 38), (25, 38), (25, 30), (28, 30), (40, 0)]
graphe(X("graphiques_4e_baignoire.png"), curves=[], extra=ligne(BAIN, BLUE, marker=False),
       xb=(-1, 43), yb=(-3, 44), xt=2, yt=5, xlabel="temps (min)", ylabel="hauteur d'eau (cm)",
       w=8.6, h=5.0)

# ------------------------------------------------------------------ taxi
graphe(X("graphiques_4e_taxi_solution.png"),
       curves=[(lambda d: 2.5 + 1.2 * d, 0, 21, BLUE)],
       extra=combine(lambda ax: lecture(ax, 7, 10.9, GREEN),
                     lambda ax: ax.text(7.3, 9.0, "7 km → 10,90 €", color=GREEN, fontsize=11.5,
                                        fontweight="bold"),
                     lambda ax: ax.scatter([0, 5, 10, 15, 20], [2.5, 8.5, 14.5, 20.5, 26.5], s=50,
                                           color=ORANGE, zorder=6)),
       xb=(-1, 22.5), yb=(-2, 30), xt=2, yt=2, xlabel="distance (km)", ylabel="prix (€)",
       w=8.4, h=5.4)


# ------------------------------------------------------------------ trois graphiques à associer
def trois_graphes(path):
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 3, figsize=(11.0, 3.8))
    fig.patch.set_facecolor("white")
    data = [("graphique 1", lambda t: 20 * t - 5 * t * t, (0, 4), (0, 22), "temps (s)", "hauteur (m)", ORANGE),
            ("graphique 2", lambda t: 25 * t, (0, 4), (0, 105), "temps (h)", "distance (km)", BLUE),
            ("graphique 3", lambda t: 800 - 200 * t, (0, 4), (0, 850), "temps (h)", "volume (L)", GREEN)]
    for ax, (tit, f, xb, yb, xl, yl, col) in zip(axs, data):
        xs = np.linspace(*xb, 100)
        ax.plot(xs, f(xs), lw=2.6, color=col)
        ax.set_xlim(*xb)
        ax.set_ylim(*yb)
        ax.set_title(tit, fontsize=14, color=DARK, fontweight="bold")
        ax.set_xlabel(xl, fontsize=11, color=DARK)
        ax.set_ylabel(yl, fontsize=11, color=DARK)
        ax.grid(True, color="#d5dde3", lw=0.7)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.tick_params(labelsize=11, colors=DARK)
    fig.tight_layout()
    _save(fig, path)


trois_graphes(X("graphiques_4e_trois_graphes.png"))

# ------------------------------------------------------------------ vitesse d'une voiture
VIT = [(0, 0), (10, 50), (40, 50), (50, 0), (60, 0)]
graphe(X("graphiques_4e_vitesse.png"), curves=[], extra=ligne(VIT, PURP),
       xb=(-1.5, 63), yb=(-4, 60), xt=5, yt=10, xlabel="temps (s)", ylabel="vitesse (km/h)",
       w=8.4, h=4.8)


# ------------------------------------------------------------------ récipients
def recipients(path):
    fig, ax = new_fig(8.0, 4.2)
    ax.add_patch(Rectangle((0, 0), 2.2, 4, facecolor=LBLUE, edgecolor=BLUE, lw=2))
    ax.text(1.1, -0.4, "récipient A\n(cylindre)", ha="center", va="top", fontsize=12, color=BLUE,
            fontweight="bold")
    ax.add_patch(Polygon([(5.5, 0), (6.1, 0), (7.6, 4), (4.0, 4)], closed=True, facecolor=LORANGE,
                         edgecolor=ORANGE, lw=2))
    ax.text(5.8, -0.4, "récipient B\n(évasé vers le haut)", ha="center", va="top", fontsize=12,
            color=ORANGE, fontweight="bold")
    ax.set_xlim(-0.5, 8.2)
    ax.set_ylim(-1.5, 4.4)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


recipients(X("graphiques_4e_recipients.png"))
graphe(X("graphiques_4e_recipients_graphe.png"),
       curves=[(lambda v: v / 80, 0, 1600, BLUE, ("$\\mathcal{C}_1$", 1200)),
               (lambda v: 1.71 * v ** (1 / 3), 0, 1600, ORANGE, ("$\\mathcal{C}_2$", 450))],
       xb=(-60, 1700), yb=(-1.5, 22), xt=200, yt=2, xlabel="volume versé (cm³)",
       ylabel="hauteur d'eau (cm)", w=8.6, h=5.2)

# ------------------------------------------------------------------ course
graphe(X("graphiques_4e_course.png"),
       curves=[(lambda t: 4 * t, 0, 150, BLUE, ("Ana", 120)),
               (lambda t: 5 * (t - 20), 20, 140, ORANGE, ("Ben", 75))],
       xb=(-5, 160), yb=(-30, 660), xt=10, yt=50, xlabel="temps (s)", ylabel="distance (m)",
       w=8.8, h=5.4)
graphe(X("graphiques_4e_course_solution.png"),
       curves=[(lambda t: 4 * t, 0, 150, BLUE), (lambda t: 5 * (t - 20), 20, 140, ORANGE)],
       extra=combine(lambda ax: lecture(ax, 100, 400, GREEN),
                     lambda ax: ax.text(102, 360, "rencontre : 100 s, 400 m", color=GREEN,
                                        fontsize=11.5, fontweight="bold"),
                     lambda ax: lecture(ax, 140, 600, ORANGE),
                     lambda ax: lecture(ax, 150, 600, BLUE),
                     lambda ax: ax.text(60, 620, "arrivée : Ben 140 s ; Ana 150 s", color=DARK,
                                        fontsize=11.5, fontweight="bold")),
       xb=(-5, 160), yb=(-30, 680), xt=10, yt=50, xlabel="temps (s)", ylabel="distance (m)",
       w=8.8, h=5.4)

# ------------------------------------------------------------------ population
POP = [(1950, 8000), (1960, 9500), (1970, 12000), (1980, 15500), (1990, 17000), (2000, 16500),
       (2010, 18000), (2020, 21000)]
graphe(X("graphiques_4e_population.png"), curves=[],
       extra=ligne([(a - 1950, p / 1000) for a, p in POP], BLUE),
       xb=(-3, 74), yb=(-1.5, 24), xt=10, yt=2, xlabel="années après 1950",
       ylabel="population (milliers)", w=8.6, h=5.0)


# ------------------------------------------------------------------ aire du rectangle (périmètre 20)
def aire_rect(ax):
    xs = list(range(0, 11))
    ax.scatter(xs, [x * (10 - x) for x in xs], s=45, color=ORANGE, zorder=5)
    lecture(ax, 5, 25, GREEN)
    ax.text(5.2, 26.2, "maximum : 25 cm² pour $x = 5$", color=GREEN, fontsize=11.5, fontweight="bold")
    ax.plot([0, 10], [16, 16], lw=1.4, color=PURP, ls=":")
    ax.text(10.1, 16, "$A = 16$ pour\n$x = 2$ ou $x = 8$", color=PURP, fontsize=11, va="center")


graphe(X("graphiques_4e_aire_rectangle_solution.png"),
       curves=[(lambda x: x * (10 - x), 0, 10, BLUE)], extra=aire_rect,
       xb=(-0.5, 12.8), yb=(-2, 29), xt=1, yt=2, xlabel="largeur $x$ (cm)", ylabel="aire (cm²)",
       w=8.6, h=5.2)

# ------------------------------------------------------------------ location de vélos
graphe(X("graphiques_4e_velos.png"),
       curves=[(lambda h: 3 * h, 0, 9, BLUE, ("tarif A", 7.2)),
               (lambda h: 10 + h, 0, 9, ORANGE, ("tarif B", 2.0))],
       xb=(-0.4, 9.6), yb=(-1.5, 29), xt=1, yt=2, xlabel="durée (h)", ylabel="prix (€)",
       w=8.4, h=5.2)

# ------------------------------------------------------------------ ballon lancé
graphe(X("graphiques_4e_ballon.png"),
       curves=[(lambda t: -5 * t * t + 20 * t, 0, 4, ORANGE)],
       xb=(-0.2, 4.5), yb=(-1.5, 23), xt=0.5, yt=2, xlabel="temps (s)", ylabel="hauteur (m)",
       w=8.2, h=5.0)

# ------------------------------------------------------------------ croissance du bébé
BEBE = [(0, 3.4), (1, 4.5), (2, 5.6), (3, 6.4), (4, 7.0), (5, 7.5), (6, 7.9), (7, 8.3), (8, 8.6),
        (9, 8.9), (10, 9.2), (11, 9.4), (12, 9.6)]
graphe(X("graphiques_4e_bebe.png"), curves=[], extra=ligne(BEBE, PURP),
       xb=(-0.5, 12.8), yb=(-0.6, 11), xt=1, yt=1, xlabel="âge (mois)", ylabel="masse (kg)",
       w=8.4, h=5.0)

# ------------------------------------------------------------------ trajet de Léa
LEA = [(0, 0), (15, 4), (25, 4), (45, 9), (60, 9), (90, 0)]
graphe(X("graphiques_4e_lea.png"), curves=[], extra=ligne(LEA, BLUE),
       xb=(-2, 95), yb=(-0.8, 10.5), xt=5, yt=1, xlabel="temps (min)",
       ylabel="distance à la maison (km)", w=8.8, h=5.0)


# ------------------------------------------------------------------ trois vases et trois courbes
def vases(path):
    fig, ax = new_fig(9.0, 3.6)
    ax.add_patch(Rectangle((0, 0), 1.0, 3, facecolor=LBLUE, edgecolor=BLUE, lw=2))
    ax.text(0.5, -0.35, "vase 1", ha="center", va="top", fontsize=12, color=BLUE, fontweight="bold")
    ax.add_patch(Rectangle((2.6, 0), 1.55, 3, facecolor=LGREEN, edgecolor=GREEN, lw=2))
    ax.text(3.375, -0.35, "vase 2", ha="center", va="top", fontsize=12, color=GREEN, fontweight="bold")
    ax.add_patch(Polygon([(5.6, 3), (7.6, 3), (6.8, 0), (6.4, 0)], closed=True, facecolor=LORANGE,
                         edgecolor=ORANGE, lw=2))
    ax.text(6.6, -0.35, "vase 3", ha="center", va="top", fontsize=12, color=ORANGE, fontweight="bold")
    ax.text(4.3, 3.45, "même hauteur, remplis avec le même robinet", ha="center", fontsize=11.5,
            color=DARK)
    ax.set_xlim(-0.4, 9.0)
    ax.set_ylim(-1.0, 3.9)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


vases(X("graphiques_4e_vases.png"))


def vases_graphes(path):
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 3, figsize=(11.0, 3.8))
    fig.patch.set_facecolor("white")
    fs = [("courbe a", lambda t: 30 * (t / 16.5) ** 0.5), ("courbe b", lambda t: 3 * t),
          ("courbe c", lambda t: 1.25 * t)]
    for ax, (tit, f) in zip(axs, fs):
        xs = np.linspace(0, 24, 200)
        ys = np.minimum(f(xs), 30)
        ax.plot(xs, ys, lw=2.6, color=DARK)
        ax.set_xlim(0, 25)
        ax.set_ylim(0, 33)
        ax.set_title(tit, fontsize=14, color=DARK, fontweight="bold")
        ax.set_xlabel("temps (s)", fontsize=11, color=DARK)
        ax.set_ylabel("hauteur (cm)", fontsize=11, color=DARK)
        ax.grid(True, color="#d5dde3", lw=0.7)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        ax.tick_params(labelsize=11, colors=DARK)
    fig.tight_layout()
    _save(fig, path)


vases_graphes(X("graphiques_4e_vases_courbes.png"))

# ------------------------------------------------------------------ four
FOUR_T = np.linspace(40, 75, 60)
def four(ax):
    ax.plot([0, 10, 40], [20, 200, 200], lw=2.6, color=ORANGE, zorder=3)
    ax.plot(FOUR_T, 20 + 180 * np.exp(-(FOUR_T - 40) / 22.0), lw=2.6, color=ORANGE, zorder=3)


graphe(X("graphiques_4e_four.png"), curves=[], extra=four, xb=(-2, 78), yb=(-12, 225), xt=5,
       yt=20, xlabel="temps (min)", ylabel="température (°C)", w=8.6, h=5.0)


# ------------------------------------------------------------------ enclos
def enclos(path):
    fig, ax = new_fig(7.6, 3.8)
    ax.add_patch(Rectangle((-0.5, 3), 9, 0.4, facecolor="#bdbdbd", edgecolor=DARK, hatch="//"))
    ax.text(4, 3.75, "mur", ha="center", fontsize=12, color=DARK, fontweight="bold")
    ax.plot([1, 1, 7, 7], [3, 0, 0, 3], lw=3, color=GREEN)
    ax.add_patch(Rectangle((1, 0), 6, 3, facecolor=LGREEN, edgecolor="none"))
    ax.text(0.75, 1.5, "$x$", ha="right", va="center", fontsize=15, color=DARK)
    ax.text(7.25, 1.5, "$x$", ha="left", va="center", fontsize=15, color=DARK)
    ax.text(4, -0.35, "$40 - 2x$", ha="center", va="top", fontsize=15, color=DARK)
    ax.text(4, 1.5, "enclos", ha="center", va="center", fontsize=13, color=GREEN, fontweight="bold")
    ax.set_xlim(-0.8, 8.8)
    ax.set_ylim(-1.0, 4.2)
    ax.set_aspect("equal")
    ax.axis("off")
    _save(fig, path)


enclos(X("graphiques_4e_enclos.png"))

# ------------------------------------------------------------------ coût et recette
graphe(X("graphiques_4e_cout_recette.png"),
       curves=[(lambda x: 200 + 5 * x, 0, 100, ORANGE, ("coût", 80)),
               (lambda x: 9 * x, 0, 100, GREEN, ("recette", 25))],
       xb=(-3, 106), yb=(-30, 960), xt=10, yt=100, xlabel="nombre d'objets",
       ylabel="montant (€)", w=8.6, h=5.2)

# ------------------------------------------------------------------ fréquence cardiaque
FC = [(0, 70), (5, 72), (10, 150), (30, 158), (35, 180), (40, 120), (45, 90)]
graphe(X("graphiques_4e_cardiaque.png"), curves=[], extra=ligne(FC, "#c0392b"),
       xb=(-1.5, 47), yb=(-8, 200), xt=5, yt=20, xlabel="temps (min)",
       ylabel="fréquence cardiaque (bpm)", w=8.6, h=5.0)

# ------------------------------------------------------------------ basket
graphe(X("graphiques_4e_basket.png"),
       curves=[(lambda x: -0.2 * x * x + 1.6 * x + 2, 0, 8, ORANGE)],
       extra=lambda ax: (ax.plot([7.25, 7.25], [0, 3.05], lw=2, color=DARK),
                         ax.plot([7.0, 7.5], [3.05, 3.05], lw=3, color="#c0392b"),
                         ax.text(7.35, 2.0, "panier\n3,05 m", fontsize=10.5, color=DARK)),
       xb=(-0.3, 8.6), yb=(-0.4, 6.2), xt=1, yt=0.5, xlabel="distance horizontale (m)",
       ylabel="hauteur (m)", w=8.6, h=5.0)
