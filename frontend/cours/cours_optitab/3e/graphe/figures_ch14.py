# -*- coding: utf-8 -*-
"""Figures du chapitre 14 (Trigonométrie) — 3ème OptiTAB."""
import os
import sys
from math import radians, tan, cos, sin, atan2, degrees

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig3e import (new_fig, finish, dot_label, seg_label, right_angle, angle_arc,
                   BLUE, ORANGE, GREEN, DARK, NEUTRAL, DIR_COURS, DIR_EXOS)
import numpy as np
import matplotlib.patches as mp


def tri(path, ang_B=35, ab=5.2, labels=(), angle_label=None, show_roles=False,
        w=7.6, h=5.0):
    """Triangle ABC rectangle en A, A en bas à gauche, B en bas à droite, C en haut à gauche."""
    A = np.array([0.0, 0.0])
    B = np.array([ab, 0.0])
    C = np.array([0.0, ab * tan(radians(ang_B))])
    fig, ax = new_fig(w, h)
    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], lw=2.4, color=BLUE)
    right_angle(ax, A, (1, 0), (0, 1), size=0.3)
    angle_arc(ax, B, A - B, C - B, r=0.8, color=ORANGE, lw=2.0,
              label=angle_label, label_r=1.35, fs=13)
    for P, nom, off in [(A, "A", (-16, -16)), (B, "B", (8, -14)), (C, "C", (-16, 6))]:
        dot_label(ax, P, f"${nom}$", *off, color=DARK, s=40)
    if show_roles:
        seg_label(ax, A, B, "côté adjacent à $\\widehat{B}$", side=-1, offset=0.42,
                  color=GREEN, fs=12.5, weight="bold")
        seg_label(ax, A, C, "côté opposé\nà $\\widehat{B}$", side=1, offset=1.15,
                  color=ORANGE, fs=12.5, weight="bold")
        seg_label(ax, B, C, "hypoténuse", side=-1, offset=0.95, color=BLUE, fs=12.5,
                  weight="bold")
    for seg, txt, kw in labels:
        P = {"A": A, "B": B, "C": C}
        seg_label(ax, P[seg[0]], P[seg[1]], txt, **kw)
    finish(fig, ax, path, [A, B, C], margin=1.3)


# Cours : les trois côtés pour l'angle B
tri(os.path.join(DIR_COURS, "trigonometrie_3e_cotes.png"), ang_B=36, ab=5.6,
    angle_label="$\\widehat{B}$", show_roles=True, w=8.0, h=5.4)

D = dict(color=DARK, fs=12.5)
I = dict(color=ORANGE, fs=13.5, weight="bold")

# Exercices génériques
tri(os.path.join(DIR_EXOS, "trigonometrie_3e_30.png"), ang_B=30, ab=5.6,
    angle_label="30°",
    labels=[("BC", "$BC = 12$ cm", dict(side=-1, offset=0.5, **D)),
            ("AC", "$AC = $ ?", dict(side=1, offset=0.8, **I))])
tri(os.path.join(DIR_EXOS, "trigonometrie_3e_angle.png"), ang_B=53.13, ab=4.2,
    angle_label="?",
    labels=[("AB", "$AB = 6$ cm", dict(side=-1, offset=0.4, **D)),
            ("BC", "$BC = 10$ cm", dict(side=-1, offset=0.5, **D))])


def batiment():
    fig, ax = new_fig(8.6, 5.6)
    ax.plot([-1, 11], [0, 0], lw=2.2, color=NEUTRAL)
    # bâtiment à x = 10, hauteur 7.2 (échelle 0.4)
    ax.add_patch(mp.Rectangle((10, 0), 1.6, 6.9, facecolor="#d6eafc", edgecolor=BLUE, lw=2))
    for yy in np.arange(0.8, 6.5, 1.0):
        for xx in (10.3, 10.95):
            ax.add_patch(mp.Rectangle((xx, yy), 0.35, 0.5, facecolor="white", edgecolor=BLUE, lw=0.8))
    # appareil
    ax.plot([0, 0], [0, 0.64], lw=3, color=DARK)
    O = np.array([0, 0.64])
    S = np.array([10, 6.9])
    ax.plot([O[0], S[0]], [O[1], S[1]], lw=1.8, color=ORANGE, linestyle="--")
    ax.plot([O[0], 10], [O[1], O[1]], lw=1.4, color=NEUTRAL, linestyle=":")
    angle_arc(ax, O, (1, 0), S - O, r=1.6, color=ORANGE, lw=2, label="32°",
              label_r=2.3, fs=12.5)
    right_angle(ax, (10, O[1]), (-1, 0), (0, 1), size=0.3)
    ax.annotate("", xy=(10, -0.5), xytext=(0, -0.5),
                arrowprops=dict(arrowstyle="<->", lw=1.4, color=DARK))
    ax.text(5, -1.0, "25 m", ha="center", fontsize=12.5, color=DARK)
    ax.text(-0.25, 0.3, "1,6 m", ha="right", fontsize=11.5, color=DARK)
    ax.text(12.0, 3.4, "$h = $ ?", fontsize=14, color=ORANGE, fontweight="bold")
    finish(fig, ax, os.path.join(DIR_EXOS, "trigonometrie_3e_batiment.png"),
           [(-1.6, -1.4), (13.4, 7.2)], margin=0.2)


batiment()


def toit():
    fig, ax = new_fig(8.2, 4.8)
    hh = 4 * tan(radians(35))
    G, Dd, S, Hh = np.array([0, 0]), np.array([8, 0]), np.array([4, hh]), np.array([4, 0])
    ax.add_patch(mp.Polygon([G, Dd, S], closed=True, facecolor="#fdebd0", edgecolor=ORANGE, lw=2.4))
    ax.plot([S[0], Hh[0]], [S[1], Hh[1]], lw=1.8, color=BLUE, linestyle="--")
    right_angle(ax, Hh, (1, 0), (0, 1), size=0.25)
    angle_arc(ax, G, (1, 0), S - G, r=1.0, color=GREEN, lw=2, label="35°",
              label_r=1.6, fs=12.5)
    ax.annotate("", xy=(8, -0.4), xytext=(0, -0.4),
                arrowprops=dict(arrowstyle="<->", lw=1.4, color=DARK))
    ax.text(4, -0.85, "base : 8 m", ha="center", fontsize=12.5, color=DARK)
    ax.text(4.2, hh / 2, "hauteur ?", fontsize=12, color=BLUE, fontweight="bold")
    seg_label(ax, S, Dd, "versant ?", side=1, offset=0.85, color=ORANGE, fs=12.5,
              weight="bold")
    finish(fig, ax, os.path.join(DIR_EXOS, "trigonometrie_3e_toit.png"),
           [(-0.5, -1.2), (8.5, hh + 0.4)], margin=0.2)


toit()


def cable():
    fig, ax = new_fig(6.4, 6.2)
    A, B = np.array([0., 0.]), np.array([-2.2, 0.])
    C = np.array([0., 2.2 * tan(radians(65))])
    ax.plot([-3, 0.8], [0, 0], lw=2.2, color=NEUTRAL)
    ax.plot([0, 0], [0, C[1] + 0.3], lw=5, color=DARK)  # poteau
    ax.plot([B[0], C[0]], [B[1], C[1]], lw=2.4, color=ORANGE)
    right_angle(ax, A, (-1, 0), (0, 1), size=0.28)
    angle_arc(ax, B, A - B, C - B, r=0.8, color=GREEN, lw=2, label="65°",
              label_r=1.3, fs=12.5)
    for P, nom, off in [(A, "A", (8, -16)), (B, "B", (-14, -16)), (C, "C", (10, 0))]:
        dot_label(ax, P, f"${nom}$", *off, color=DARK, s=40)
    seg_label(ax, B, C, "câble : 18 m", side=1, offset=1.7, color=ORANGE, fs=12.5,
              weight="bold")
    finish(fig, ax, os.path.join(DIR_EXOS, "trigonometrie_3e_cable.png"),
           [(-3.2, -0.8), (1.2, C[1] + 0.6)], margin=0.2)


cable()
print("Figures chapitre 14 : OK")
