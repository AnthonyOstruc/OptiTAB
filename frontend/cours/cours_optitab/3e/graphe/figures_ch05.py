# -*- coding: utf-8 -*-
"""Figures du chapitre 5 (Équations) — 3ème OptiTAB."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig3e import new_fig, finish, BLUE, ORANGE, GREEN, DARK, DIR_COURS, DIR_EXOS
import matplotlib.patches as mp


def balance():
    """Modèle de la balance : 5x − 7 = 2x + 8."""
    fig, ax = new_fig(8.4, 4.2)
    # fléau et pivot
    ax.plot([-3.4, 3.4], [2.0, 2.0], lw=3.0, color=DARK, solid_capstyle="round")
    ax.add_patch(mp.Polygon([(-0.35, 0.3), (0.35, 0.3), (0, 2.0)], closed=True,
                            facecolor="#b0bec5", edgecolor=DARK, lw=1.5))
    ax.plot([-4.2, 4.2], [0.3, 0.3], lw=2.0, color="0.45")
    # plateaux
    for cx, txt, col in [(-2.6, r"$5x - 7$", BLUE), (2.6, r"$2x + 8$", ORANGE)]:
        ax.plot([cx, cx], [1.52, 2.0], lw=1.6, color=DARK)
        ax.add_patch(mp.FancyBboxPatch((cx - 1.15, 0.95), 2.3, 0.6,
                     boxstyle="round,pad=0.05", facecolor="white",
                     edgecolor=col, lw=2.2))
        ax.text(cx, 1.25, txt, fontsize=16, ha="center", va="center",
                color=col, fontweight="bold")
    ax.text(0, 3.0, "Une équation est une balance en équilibre :", fontsize=12.5,
            ha="center", color=DARK, fontweight="bold")
    ax.text(0, 2.55, "on effectue la même opération sur les deux plateaux",
            fontsize=11.5, ha="center", color=DARK, style="italic")
    ax.text(0, -0.35, r"$5x - 7 = 2x + 8 \;\Rightarrow\; 3x = 15 \;\Rightarrow\; x = 5$",
            fontsize=13.5, ha="center", color=GREEN, fontweight="bold")
    finish(fig, ax, os.path.join(DIR_COURS, "equations_3e_balance.png"),
           [(-4.5, -0.8), (4.5, 3.3)], margin=0.2, equal=False)


def rectangle():
    """Rectangle de périmètre 58, longueur x + 7, largeur x."""
    fig, ax = new_fig(7.6, 4.2)
    L, H = 5.4, 3.0
    ax.add_patch(mp.Rectangle((0, 0), L, H, facecolor="#e8f4fd",
                              edgecolor=BLUE, lw=2.4))
    ax.annotate("", xy=(L, -0.4), xytext=(0, -0.4),
                arrowprops=dict(arrowstyle="<->", lw=1.5, color=ORANGE))
    ax.text(L / 2, -0.8, "longueur : $x + 7$", fontsize=13.5, ha="center",
            color=ORANGE, fontweight="bold")
    ax.annotate("", xy=(-0.4, H), xytext=(-0.4, 0),
                arrowprops=dict(arrowstyle="<->", lw=1.5, color=BLUE))
    ax.text(-0.75, H / 2, "largeur : $x$", fontsize=13.5, va="center", ha="center",
            color=BLUE, fontweight="bold", rotation=90)
    ax.text(L / 2, H / 2, "périmètre : 58 cm", fontsize=13.5, ha="center",
            va="center", color=DARK, fontweight="bold")
    finish(fig, ax, os.path.join(DIR_EXOS, "equations_3e_rectangle.png"),
           [(-1.3, -1.2), (L + 0.4, H + 0.4)], margin=0.15)


def aires():
    """Carré (x+2) et rectangle x × (x+5) de même aire."""
    fig, ax = new_fig(8.8, 4.0)
    c = 2.6
    ax.add_patch(mp.Rectangle((0, 0), c, c, facecolor="#e8f4fd", edgecolor=BLUE, lw=2.2))
    ax.text(c / 2, c / 2, "aire ?", fontsize=12.5, ha="center", va="center", color=BLUE)
    ax.text(c / 2, -0.45, "$x + 2$", fontsize=13.5, ha="center", color=BLUE,
            fontweight="bold")
    ax.text(-0.45, c / 2, "$x + 2$", fontsize=13.5, va="center", ha="center",
            color=BLUE, fontweight="bold", rotation=90)
    Lx, Hx = 3.9, 1.75
    x0 = c + 1.6
    ax.add_patch(mp.Rectangle((x0, 0), Lx, Hx, facecolor="#fdebd0",
                              edgecolor="#e67e22", lw=2.2))
    ax.text(x0 + Lx / 2, Hx / 2, "même aire", fontsize=12.5, ha="center",
            va="center", color="#e67e22")
    ax.text(x0 + Lx / 2, -0.45, "$x + 5$", fontsize=13.5, ha="center",
            color="#e67e22", fontweight="bold")
    ax.text(x0 - 0.45, Hx / 2, "$x$", fontsize=13.5, va="center", ha="center",
            color="#e67e22", fontweight="bold", rotation=90)
    ax.text((c + x0 + Lx) / 2 - 1.2, c + 0.55, r"$(x+2)^2 = x(x+5)$",
            fontsize=14.5, ha="center", color=DARK, fontweight="bold")
    finish(fig, ax, os.path.join(DIR_EXOS, "equations_3e_aires.png"),
           [(-1.0, -1.0), (x0 + Lx + 0.4, c + 1.0)], margin=0.15)


balance()
rectangle()
aires()
print("Figures chapitre 5 : OK")
