# -*- coding: utf-8 -*-
"""Figures du chapitre 15 (Transformations et homothéties) — 3ème OptiTAB."""
import os
import sys
from math import cos, sin, pi, radians

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig3e import (new_fig, setup_repere, BLUE, ORANGE, GREEN, DARK, NEUTRAL,
                   DIR_COURS, DIR_EXOS, ROOT)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mp


def save(fig, path):
    fig.savefig(path, dpi=175, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", os.path.relpath(path, ROOT))


def poly(ax, pts, col, face, labels=None, prime=False, lw=2.2):
    ax.add_patch(mp.Polygon(pts, closed=True, facecolor=face, edgecolor=col, lw=lw,
                            alpha=0.9, zorder=3))
    if labels:
        for (x, y), n in zip(pts, labels):
            ax.scatter([x], [y], s=28, color=col, zorder=5)
            ax.annotate(n + ("'" if prime else ""), (x, y), textcoords="offset points",
                        xytext=(5, 5), fontsize=12, color=col, fontweight="bold")


def repere(xb, yb, w=7.6, h=6.0):
    fig, ax = new_fig(w, h)
    setup_repere(ax, xb, yb)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


T = [(2, 1), (4, 1), (3, 3)]
LAB = ["A", "B", "C"]

# Cours — les quatre transformations sur un même motif
def quatre():
    fig, axes = plt.subplots(2, 2, figsize=(10, 9.4))
    fig.patch.set_facecolor("white")
    configs = [
        ("Symétrie axiale (axe des ordonnées)", [(-x, y) for x, y in T], "axe"),
        ("Symétrie centrale (centre O)", [(-x, -y) for x, y in T], "centre"),
        ("Translation (3 à droite, 1 en haut)", [(x + 3 - 5, y + 1 - 4) for x, y in T], "trans"),
        ("Rotation de 90° autour de O", [(-y, x) for x, y in T], "rot"),
    ]
    for ax, (titre, img, kind) in zip(axes.flat, configs):
        src = T if kind != "trans" else [(x - 5, y - 4) for x, y in T]
        setup_repere(ax, (-5.5, 5.5), (-4.5, 4.5), unit_labels=False)
        ax.set_aspect("equal")
        ax.axis("off")
        poly(ax, src, BLUE, "#d6eafc")
        poly(ax, img, ORANGE, "#fdebd0")
        if kind == "axe":
            ax.plot([0, 0], [-4.4, 4.4], lw=2.4, color=GREEN)
        if kind == "trans":
            ax.annotate("", xy=(src[0][0] + 3, src[0][1] + 1), xytext=src[0],
                        arrowprops=dict(arrowstyle="-|>", lw=2, color=GREEN))
        if kind in ("centre", "rot"):
            ax.scatter([0], [0], s=60, color=GREEN, zorder=6)
            ax.annotate("O", (0, 0), textcoords="offset points", xytext=(-18, 6),
                        fontsize=12, color=GREEN, fontweight="bold")
        if kind == "rot":
            ax.add_patch(mp.Arc((0, 0), 3.2, 3.2, theta1=20, theta2=110, lw=1.8,
                                color=GREEN))
            ax.annotate("", xy=(-0.55, 1.5), xytext=(-0.45, 1.52),
                        arrowprops=dict(arrowstyle="-|>", lw=1.8, color=GREEN))
        ax.set_title(titre, fontsize=12.5, color=DARK, fontweight="bold")
    fig.tight_layout()
    save(fig, os.path.join(DIR_COURS, "transformations_3e_quatre.png"))


quatre()


# Cours — homothéties de rapport 2 et -1,5 (centre O)
def homotheties():
    fig, ax = repere((-6.5, 8.5), (-6, 7.5), w=8.4, h=7.0)
    src = T
    poly(ax, src, BLUE, "#d6eafc", LAB)
    poly(ax, [(2 * x, 2 * y) for x, y in src], ORANGE, "#fdebd0", LAB, prime=True)
    poly(ax, [(-1.5 * x, -1.5 * y) for x, y in src], GREEN, "#c8e6c9")
    for x, y in src:
        ax.plot([-1.5 * x, 2 * x], [-1.5 * y, 2 * y], lw=0.9, color=NEUTRAL,
                linestyle=":", zorder=2)
    ax.scatter([0], [0], s=60, color=DARK, zorder=6)
    ax.annotate("O", (0, 0), textcoords="offset points", xytext=(-14, 6),
                fontsize=12, color=DARK, fontweight="bold")
    ax.text(4.6, 6.6, "rapport $k = 2$", fontsize=12.5, color=ORANGE, fontweight="bold")
    ax.text(-6.2, -5.6, "rapport $k = -1{,}5$", fontsize=12.5, color=GREEN,
            fontweight="bold")
    save(fig, os.path.join(DIR_COURS, "transformations_3e_homotheties.png"))


homotheties()


# Exercices — quadrillage avec le triangle source (à construire)
def exo_source(name, src, xb, yb, extra=None, labels=LAB):
    fig, ax = repere(xb, yb)
    poly(ax, src, BLUE, "#d6eafc", labels)
    if extra:
        extra(ax)
    save(fig, os.path.join(DIR_EXOS, name))


def exo_solution(name, src, img, xb, yb, extra=None, labels=LAB):
    fig, ax = repere(xb, yb)
    poly(ax, src, BLUE, "#d6eafc", labels)
    poly(ax, img, GREEN, "#c8e6c9", labels, prime=True)
    if extra:
        extra(ax)
    save(fig, os.path.join(DIR_EXOS, name))


axe_y = lambda ax: ax.plot([0, 0], [-0.8, 4.6], lw=2.4, color=ORANGE)  # noqa: E731
exo_source("transformations_3e_sym_axe.png", T, (-5.5, 5.5), (-1, 4.8), axe_y)
exo_solution("transformations_3e_sym_axe_sol.png", T, [(-x, y) for x, y in T],
             (-5.5, 5.5), (-1, 4.8), axe_y)


def centre_O(ax):
    ax.scatter([0], [0], s=60, color=ORANGE, zorder=6)
    ax.annotate("O", (0, 0), textcoords="offset points", xytext=(-18, 6),
                fontsize=12, color=ORANGE, fontweight="bold")


exo_source("transformations_3e_rotation.png", T, (-4.5, 5.5), (-1.5, 5.5), centre_O)
exo_solution("transformations_3e_rotation_sol.png", T, [(-y, x) for x, y in T],
             (-4.5, 5.5), (-1.5, 5.5), centre_O)

T2 = [(1, 2), (3, 2), (2, 4)]


def vect(ax):
    ax.annotate("", xy=(3, 1), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", lw=2.2, color=ORANGE))
    ax.annotate("P", (0, 0), textcoords="offset points", xytext=(-14, -14),
                fontsize=12, color=ORANGE, fontweight="bold")
    ax.annotate("Q", (3, 1), textcoords="offset points", xytext=(6, -12),
                fontsize=12, color=ORANGE, fontweight="bold")


exo_solution("transformations_3e_translation_sol.png", T2, [(x + 3, y + 1) for x, y in T2],
             (-1, 7.5), (-1, 6), vect)

src_h = T
exo_solution("transformations_3e_homothetie_sol.png", src_h, [(2 * x, 2 * y) for x, y in src_h],
             (-1, 9.5), (-1, 7), centre_O)
exo_solution("transformations_3e_homothetie_neg_sol.png", src_h,
             [(-1.5 * x, -1.5 * y) for x, y in src_h], (-7, 5.5), (-5.5, 4), centre_O)


def rosace():
    fig, ax = new_fig(6.4, 6.4)
    for k in range(8):
        a = radians(45 * k)
        pts = [(0, 0), (2.6 * cos(a - 0.22), 2.6 * sin(a - 0.22)),
               (3.2 * cos(a), 3.2 * sin(a)), (2.6 * cos(a + 0.22), 2.6 * sin(a + 0.22))]
        ax.add_patch(mp.Polygon(pts, closed=True,
                                facecolor=ORANGE if k == 0 else ("#d6eafc" if k % 2 else "#fdebd0"),
                                edgecolor=BLUE, lw=1.6))
    ax.scatter([0], [0], s=40, color=DARK, zorder=5)
    ax.annotate("O", (0, 0), textcoords="offset points", xytext=(6, -14), fontsize=12,
                color=DARK, fontweight="bold")
    ax.set_xlim(-3.6, 3.6)
    ax.set_ylim(-3.6, 3.6)
    ax.set_aspect("equal")
    ax.axis("off")
    save(fig, os.path.join(DIR_EXOS, "transformations_3e_rosace.png"))


rosace()


def frise():
    fig, ax = new_fig(9.6, 2.4)
    for k in range(6):
        x0 = 4 * k
        pts = [(x0, 0), (x0 + 2.4, 0), (x0 + 1.2, 2.0), (x0 + 0.4, 1.0)]
        ax.add_patch(mp.Polygon(pts, closed=True,
                                facecolor=ORANGE if k == 0 else "#d6eafc",
                                edgecolor=BLUE, lw=1.6))
        ax.text(x0 + 1.1, -0.6, f"motif {k + 1}", fontsize=10, ha="center", color=DARK)
    ax.annotate("", xy=(4, 2.4), xytext=(0, 2.4), arrowprops=dict(arrowstyle="<->", lw=1.4, color=GREEN))
    ax.text(2, 2.6, "4 cm", ha="center", fontsize=11, color=GREEN, fontweight="bold")
    ax.set_xlim(-0.5, 23.5)
    ax.set_ylim(-1.0, 3.1)
    ax.set_aspect("equal")
    ax.axis("off")
    save(fig, os.path.join(DIR_EXOS, "transformations_3e_frise.png"))


frise()
print("Figures chapitre 15 : OK")
